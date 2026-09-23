
# Objective: This script searches Open Alex and returns the count
# of papers found by query string and whether or not specific DOIs are present
# in the search.

# Objective: This script searches Open Alex and returns the count
# of papers found by query string and whether or not specific DOIs are present
# in the search.

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
API_KEY = os.getenv("API_KEY_OPENALEX")
MAILTO = os.getenv("MAILTO_OPENALEX")
SLEEP_BETWEEN_QUERIES = 0.5
BASE_URL = "https://api.openalex.org/works"
OUTPUT_CSV = REPO_ROOT / "results" / "query_counts.csv"

# --------------------------------------------------------------------------
# BUILDING QUERIES
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
            ("methods_es_ocean",      ["ES_core", ocean_name, "Ecosystem_data_methods"]),

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
# DEFINING HELPER FUNCTIONS TO RUN  SEARCH IN OPENALEX
# --------------------------------------------------------------------------

def get_count_for_filter(filter_str, mailto=MAILTO, api_key=API_KEY,
                          debug=False, max_retries=5):
    """Generic: return meta.count for an arbitrary OpenAlex filter string."""
    params = {
        "filter": filter_str,
        "per-page": 1,
    }
    if mailto:
        params["mailto"] = mailto
    if api_key:
        params["api_key"] = api_key

    for attempt in range(1, max_retries + 1):
        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code == 429:
            try:
                wait_s = response.json().get("retryAfter", 30)
            except ValueError:
                wait_s = 30
            wait_s = wait_s + 3
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
        return data.get("meta", {}).get("count", 0)

    raise RuntimeError(f"Still rate-limited after {max_retries} retries: {filter_str}")


def get_count(query, mailto=MAILTO, api_key=API_KEY, debug=False, max_retries=5):
    """Wrapper: count of works matching the search query alone."""
    filter_str = f"title_and_abstract.search:{query}"
    return get_count_for_filter(filter_str, mailto, api_key, debug, max_retries)

def check_target_dois(query, dois=TARGET_DOIS):
    """
    For a given search query, check which of the target DOIs are matched
    by that same search string (title_and_abstract.search AND doi:<doi>).
    Returns (found_count, found_list) where found_list has one bool per DOI.
    """
    found_list = []
    for doi in dois:
        clean_doi = doi.replace("https://doi.org/", "").strip()
        filter_str = f"title_and_abstract.search:{query},doi:{clean_doi}"
        try:
            count = get_count_for_filter(filter_str)
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
        slug=f"search-{datetime.now().strftime('%H%M')}",
        title="OpenAlex search update",
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


