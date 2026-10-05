
import csv
import importlib
import sys
import time
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent   # .../SEAMPHONI_LITREVIEW/code
REPO_ROOT = SCRIPT_DIR.parent                  # .../SEAMPHONI_LITREVIEW
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT))

load_dotenv()

# --------------------------------------------------------------------------
# SETTINGS - edit these
# --------------------------------------------------------------------------
# File name (without .py) of your counts script, so the SAME queries are reused.
SEARCH_MODULE = "OpenAlex_search_new_counts"

# sort simply to have an idea of how important the papers mught be
SORT_BY = "cited_by_count:desc"

# Ask for confirmation if the pre-flight count says more than this many records.
CONFIRM_ABOVE = 20000

INCLUDE_ABSTRACT = False

API_KEY = os.getenv("API_KEY_OPENALEX")
MAILTO = os.getenv("MAILTO_OPENALEX")
BASE_URL = "https://api.openalex.org/works"
PER_PAGE = 200
SLEEP_BETWEEN_REQUESTS = 0.3
OUTPUT_CSV = REPO_ROOT / "results" / "papers_metadata.csv"

SELECT_FIELDS = [
    "id", "doi", "title", "language", "publication_year", "type",
    "primary_location", "primary_topic", "topics", "keywords", "authorships",
]


# --------------------------------------------------------------------------
# LOAD QUERIES FROM THE COUNTS SCRIPT
# --------------------------------------------------------------------------
QUERIES = importlib.import_module(SEARCH_MODULE).QUERIES


# --------------------------------------------------------------------------
# API HELPERS
# --------------------------------------------------------------------------
def get_json(params, max_retries=5):
    p = dict(params)
    if MAILTO:
        p["mailto"] = MAILTO
    if API_KEY:
        p["api_key"] = API_KEY
    for attempt in range(1, max_retries + 1):
        r = requests.get(BASE_URL, params=p, timeout=60)
        if r.status_code == 429:
            try:
                wait_s = r.json().get("retryAfter", 30)
            except ValueError:
                wait_s = 30
            print(f"  Rate limited (attempt {attempt}/{max_retries}). Waiting {wait_s + 3}s...")
            time.sleep(wait_s + 3)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"Still rate-limited after {max_retries} retries")


def make_filter(query):
    f = f"title_and_abstract.search:{query}"
    return f


def preflight_count(query):
    data = get_json({"filter": make_filter(query), "per-page": 1})
    return data.get("meta", {}).get("count", 0)


# --------------------------------------------------------------------------
# FLATTENING ONE WORK INTO A CSV ROW
# --------------------------------------------------------------------------
def uniq(seq):
    seen, out = set(), []
    for s in seq:
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out

def name_of(obj):
    return (obj or {}).get("display_name")


def flatten(work):
    source = (work.get("primary_location") or {}).get("source") or {}
    ptopic = work.get("primary_topic") or {}
    topics = work.get("topics") or []
    keywords = work.get("keywords") or []
    authors = uniq(name_of(a.get("author")) for a in (work.get("authorships") or []))

    topics_detail = [
        f"{t.get('display_name')} [{name_of(t.get('subfield'))} > "
        f"{name_of(t.get('field'))} > {name_of(t.get('domain'))}]"
        for t in topics
    ]

    row = {
        "OpenAlex_ID": (work.get("id") or "").replace("https://openalex.org/", ""),
        "DOI": (work.get("doi") or "").replace("https://doi.org/", ""),
        "Title": work.get("title"),
        "Year": work.get("publication_year"),
        "Language": work.get("language"),
        "Type": work.get("type"),
        "Journal": source.get("display_name"),
        "Primary_topic": ptopic.get("display_name"),
        "Primary_subfield": name_of(ptopic.get("subfield")),
        "Primary_field": name_of(ptopic.get("field")),
        "Primary_domain": name_of(ptopic.get("domain")),
        "Topics_detail": " | ".join(topics_detail),
        "Topics_subfields": "; ".join(uniq(name_of(t.get("subfield")) for t in topics)),
        "Topics_fields": "; ".join(uniq(name_of(t.get("field")) for t in topics)),
        "Topics_domains": "; ".join(uniq(name_of(t.get("domain")) for t in topics)),
        "Keywords": "; ".join(uniq(name_of(k) for k in keywords)),
        "Authors": "; ".join(authors),
        "N_authors": len(authors),
    }
    return row


# --------------------------------------------------------------------------
# DOWNLOAD ONE QUERY (cursor paging, no 10,000-record limit)
# --------------------------------------------------------------------------
def fetch_query(query, label, store):
    params = {
        "filter": make_filter(query),
        "per-page": PER_PAGE,
        "select": ",".join(SELECT_FIELDS),
        "cursor": "*",
    }
    if SORT_BY:
        params["sort"] = SORT_BY

    n_seen = 0
    while True:
        data = get_json(params)
        results = data.get("results", [])
        if not results:
            break
        for w in results:
            wid = w.get("id")
            if wid not in store:
                store[wid] = flatten(w)
                store[wid]["_labels"] = set()
            store[wid]["_labels"].add(label)
            n_seen += 1
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        params["cursor"] = cursor
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    return n_seen


def write_csv(store):
    if not store:
        print("Nothing to write.")
        return
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    base_cols = [k for k in next(iter(store.values())).keys() if k != "_labels"]
    fieldnames = base_cols + ["N_queries", "Query_labels"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in store.values():
            labels = sorted(rec["_labels"])
            row = {k: rec[k] for k in base_cols}
            row["N_queries"] = len(labels)
            row["Query_labels"] = "; ".join(labels)
            writer.writerow(row)
    print(f"Wrote {len(store)} unique papers to {OUTPUT_CSV}")


# --------------------------------------------------------------------------
# RUN
# --------------------------------------------------------------------------
def main():
    # Pre-flight: how many records will we pull?
    expected = 0
    print(f"Pre-flight count for {len(QUERIES)} queries...")
    for q in QUERIES:
        c = preflight_count(q["query"])
        expected += c
        print(f"  {c:>8}  {q['label']}")
        time.sleep(SLEEP_BETWEEN_REQUESTS)
    print(f"Total records to download (with overlaps): {expected}"
          f"  (~{expected // PER_PAGE + len(QUERIES)} API requests)")

    if expected > CONFIRM_ABOVE:
        if input("That is a lot. Proceed? [y/N] ").strip().lower() != "y":
            print("Aborted.")
            return

    store = {}   # OpenAlex ID -> row dict (de-duplicated across queries)
    try:
        for i, q in enumerate(QUERIES, start=1):
            n = fetch_query(q["query"], q["label"], store)
            print(f"[{i}/{len(QUERIES)}] {n:>8} records | {len(store)} unique so far | {q['label']}")
    finally:
        write_csv(store)   # saves whatever was collected, even if interrupted


if __name__ == "__main__":
    main()