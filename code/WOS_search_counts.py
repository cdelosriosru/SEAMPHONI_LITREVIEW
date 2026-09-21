# Objective: This script searches Web of Science (Starter API) and returns
# the count of papers found by query string and whether or not specific
# DOIs are present in the search. Mirrors the OpenAlex version.

import csv
import os
import sys
import time
from datetime import date, datetime
from itertools import combinations
from pathlib import Path

import requests
from dotenv import load_dotenv

# --------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent   # .../SEAMPHONI_LITREVIEW/code
REPO_ROOT = SCRIPT_DIR.parent                  # .../SEAMPHONI_LITREVIEW
sys.path.insert(0, str(REPO_ROOT))             # makes inputs/ importable — must run before the imports below

from site_publish import publish_update, auto_push, update_search_terms_section
from inputs.search_terms import TERM_GROUPS
from inputs.target_papers import TARGET_DOIS

load_dotenv()

# --------------------------------------------------------------------------
# CREDENTIALS AND BASIC SETTINGS
# --------------------------------------------------------------------------
API_KEY = os.getenv("WOS_API_KEY")
SLEEP_BETWEEN_QUERIES = 0.5
DATABASE_ID = "WOS"
BASE_URL = "https://api.clarivate.com/apis/wos-starter/v1/documents"
OUTPUT_CSV = REPO_ROOT / "results" / "wos_query_counts.csv"

HEADERS = {
    "X-ApiKey": API_KEY,
    "Accept": "application/json",
}

# --------------------------------------------------------------------------
# BUILDING QUERIES (unchanged from the OpenAlex script — same boolean logic,
# just wrapped in WoS's TS= field tag instead of an OpenAlex filter string)
# --------------------------------------------------------------------------

def or_join(terms):
    """Wrap each term in parentheses and join with OR."""
    return " OR ".join(f"({t})" for t in terms)


def build_query(group_names, term_groups=TERM_GROUPS):
    """
    Build a single query ANDing together the OR-joined term lists
    of each named group in group_names.
    e.g. build_query(["ES_core", "Ocean_context"])
      -> (ES_core terms OR'd) AND (Ocean_context terms OR'd)
    """
    parts = [or_join(term_groups[name]) for name in group_names]
    return " AND ".join(f"({p})" for p in parts)


def build_all_combinations(group_names_pool, min_groups=2, max_groups=None,
                            term_groups=TERM_GROUPS):
    """
    Generate one query per possible combination of groups from
    group_names_pool, from min_groups up to max_groups (default: all of them).
    Returns a list of dicts: {"groups": (...), "query": "..."}
    """
    if max_groups is None:
        max_groups = len(group_names_pool)

    queries = []
    for r in range(min_groups, max_groups + 1):
        for combo in combinations(group_names_pool, r):
            queries.append({
                "groups": combo,
                "query": build_query(combo, term_groups)
            })
    return queries


OCEAN_GROUP_NAMES = ["Ocean_context", "Ocean_acronyms", "Ocean_resources"]

def build_query_set(ocean_group_names, term_groups=TERM_GROUPS):
    """
    For each ocean group in ocean_group_names, build 4 queries:
      1. ES_valuation AND Ocean
      2. ES_valuation AND Ocean AND Management
      3. ES_core AND Ocean
      4. ES_core AND Ocean AND Management

    Returns a list of dicts: {"label": ..., "groups": (...), "query": "..."}
    """
    queries = []
    for ocean_name in ocean_group_names:
        template_specs = [
            ("valuation_only",        ["ES_valuation", ocean_name]),
            ("valuation_management",  ["ES_valuation", ocean_name, "Management"]),
            ("core_only",             ["ES_core", ocean_name]),
            ("core_management",       ["ES_core", ocean_name, "Management"]),
        ]
        for label, groups in template_specs:
            queries.append({
                "label": f"{ocean_name}_{label}",
                "groups": tuple(groups),
                "query": build_query(groups, term_groups)
            })
    return queries


QUERIES = build_query_set(OCEAN_GROUP_NAMES)


# --------------------------------------------------------------------------
# DEFINING HELPER FUNCTIONS TO RUN SEARCH IN WEB OF SCIENCE
# --------------------------------------------------------------------------

def to_ts_query(query):
    """Wrap a raw boolean term string in the WoS Topic (TS=) field tag."""
    return f"TS=({query})"


def get_count_for_wos_query(wos_query, database_id=DATABASE_ID, debug=False, max_retries=5):
    """Generic: return metadata.total for an arbitrary WoS query string (already field-tagged)."""
    params = {
        "db": database_id,
        "q": wos_query,
        "limit": 1,
        "page": 1,
    }

    for attempt in range(1, max_retries + 1):
        response = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)

        if response.status_code == 429:
            wait_s = int(response.headers.get("Retry-After", 30)) + 3
            print(f"  Rate limited (attempt {attempt}/{max_retries}). "
                  f"Waiting {wait_s}s before retrying...")
            time.sleep(wait_s)
            continue

        if debug:
            print("  URL:", response.url)
            print("  STATUS:", response.status_code)
            print("  BODY (first 500 chars):", response.text[:500])

        response.raise_for_status()
        data = response.json()
        return data.get("metadata", {}).get("total", 0)

    raise RuntimeError(f"Still rate-limited after {max_retries} retries: {wos_query}")


def get_count(query, debug=False, max_retries=5):
    """Wrapper: count of records matching the search query alone (Topic field)."""
    wos_query = to_ts_query(query)
    return get_count_for_wos_query(wos_query, debug=debug, max_retries=max_retries)


def check_target_dois(query, dois=TARGET_DOIS):
    """
    For a given search query, check which of the target DOIs are matched
    by that same search string (TS=(query) AND DO=(doi)).
    Returns (found_count, found_list) where found_list has one bool per DOI.
    """
    ts_query = to_ts_query(query)
    found_list = []
    for doi in dois:
        clean_doi = doi.replace("https://doi.org/", "").strip()
        combined_query = f'{ts_query} AND DO=("{clean_doi}")'
        try:
            count = get_count_for_wos_query(combined_query)
        except requests.RequestException as e:
            print(f"    DOI check failed for {clean_doi}: {e}")
            count = 0
        found_list.append(count > 0)
        time.sleep(SLEEP_BETWEEN_QUERIES)
    return sum(found_list), found_list


# --------------------------------------------------------------------------
# RUN SEARCH
# --------------------------------------------------------------------------

def main():
    if not API_KEY:
        raise RuntimeError("WOS_API_KEY not set — add it to your .env file.")

    rows = []
    total = 0

    # Build DOI column names once, e.g. "DOI_1", "DOI_2", ...
    doi_columns = [f"DOI_{i}" for i in range(1, len(TARGET_DOIS) + 1)]

    for i, q in enumerate(QUERIES, start=1):
        query = q["query"]
        label = q["label"]
        try:
            count = get_count(query, debug=False)
        except requests.HTTPError as e:
            print(f"[{i}/{len(QUERIES)}] ERROR for '{label}': {e}")
            print(f"  Response body: {e.response.text[:500] if e.response is not None else 'N/A'}")
            count = None
        except requests.RequestException as e:
            print(f"[{i}/{len(QUERIES)}] REQUEST FAILED for '{label}': {e}")
            count = None
        else:
            print(f"[{i}/{len(QUERIES)}] {count} papers  |  {label}")
            if count:
                total += count

        # Check target DOIs against this query
        found_count, found_list = check_target_dois(query)
        print(f"    Key papers found: {found_count}/{len(TARGET_DOIS)}  {found_list}")

        # Build the row: label, count, then one 0/1 column per DOI
        row = {
            "Query_label": label,
            "Count": count,
        }
        for col_name, found in zip(doi_columns, found_list):
            row[col_name] = int(found)  # True/False -> 1/0

        rows.append(row)
        time.sleep(SLEEP_BETWEEN_QUERIES)

    fieldnames = ["Query_label", "Count"] + doi_columns

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nTotal across all queries: {total}")
    print(f"Counts written to {OUTPUT_CSV}")
    publish_update(
        docs_dir=str(REPO_ROOT / "docs"),
        date=date.today().isoformat(),
        slug=f"wos-search-{datetime.now().strftime('%H%M')}",
        title="Web of Science search update",
        fieldnames=fieldnames,
        rows=rows,
    )
    update_search_terms_section(
        index_path=str(REPO_ROOT / "docs" / "index.md"),
        term_groups=TERM_GROUPS,
    )
    auto_push(repo_dir=str(REPO_ROOT))


if __name__ == "__main__":
    main()