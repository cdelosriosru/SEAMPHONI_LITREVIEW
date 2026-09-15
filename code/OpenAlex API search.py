
import csv
import time
import requests
import os

# --------------------------------------------------------------------------
# SETTINGS - edit these
# --------------------------------------------------------------------------


START = ['"ecosystem services"',
         '"environmental services"',
         '"nature services"'
        ]



DEMO_SITE_1 = ['iceland AND offshore',
               'icelandic AND offshore',
               '"faroe ridge"'
               ]

DEMO_SITE_2 = ['"wadden sea"',
               '"north sea"',
               'danish AND offshore',
               'denmark AND offshore'
               ]

DEMO_SITE_3 = ['ebro',
               '"spanish mediterranean sea"',
               'spanish AND mediterranean AND offshore',
               'spain AND mediterranean AND offshore',
               '"garraf coast"',
               'garraf AND mediterranean AND offshore',
               '"cetacean migratory corridor"'
               ]

DEMO_SITE_4 = ['"finikie submarine seamounts"',
               '"finikie seamounts"',
               '"finikie seamount"',
               'turkish AND mediterranean AND offshore',
               'turkey AND mediterranean AND offshore'
               ]


DEMO_SITE_5 = ['ampere AND seamount',
               'seine AND seamount',
               '"selvagens islands"',
               'madeira AND offshore'
               ]

DEMO_SITE_6 = ['"la reunion"',
               '"Mount La Pérouse"',
               '"la reunion" AND offshore'
               ]

DEMO_SITES = [
    DEMO_SITE_1,
    DEMO_SITE_2,
    DEMO_SITE_3,
    DEMO_SITE_4,
    DEMO_SITE_5,
    DEMO_SITE_6,
]


def or_join(terms):
    """Wrap each term in parentheses (safe even for simple terms, required
    for terms that already contain AND) and join with OR."""
    return " OR ".join(f"({t})" for t in terms)


def build_query(start_terms, site_terms):
    """start AND (site_1 OR site_2 OR ...) , with 'start' itself OR-joined
    if it has more than one term."""
    start_part = or_join(start_terms)
    site_part = or_join(site_terms)
    return f"({start_part}) AND ({site_part})"


# One query per demo site
QUERIES2 = [build_query(START, site) for site in DEMO_SITES]


# Max number of works to retrieve PER query (set to None for "all results")
MAX_RESULTS_PER_QUERY = None

# Number of results per API page (OpenAlex max is 200)
PER_PAGE = 200

# Politeness: OpenAlex asks for an email in the "mailto" param for faster,
# more reliable service (the "polite pool"). Put your email here.
MAILTO = "mail@mail.com"

# Be nice to the API between page requests (seconds).
# Bumped up from 0.1 -> 1.0 to avoid tripping the rate limiter.
SLEEP_BETWEEN_REQUESTS = 1.0

# Pause between separate queries (seconds)
SLEEP_BETWEEN_QUERIES = 2.0



BASE_URL = "https://api.openalex.org/works"
OUTPUT_DIR = "LiteratureReview_SEAMPHONI/Openalex/API"  # change if you want output elsewhere


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def reconstruct_abstract(inverted_index):
    """OpenAlex stores abstracts as an inverted index: {word: [positions]}.
    Rebuild the plain-text abstract from it."""
    if not inverted_index:
        return ""

    # Build position -> word map
    position_word = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            position_word[pos] = word

    # Sort by position and join
    max_pos = max(position_word.keys())
    words = [position_word.get(i, "") for i in range(max_pos + 1)]
    return " ".join(words)


def get_authors(work):
    """Return a semicolon-separated string of author display names."""
    authorships = work.get("authorships", []) or []
    names = [a["author"]["display_name"] for a in authorships if a.get("author")]
    return "; ".join(names)


def get_source(work):
    """Return the journal / venue name (host venue / primary location)."""
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    return source.get("display_name", "")


def get_doi(work):
    doi = work.get("doi")
    return doi if doi else ""


def search_openalex(query, keywords=None, max_results=None, per_page=PER_PAGE, mailto=MAILTO):
    """Page through OpenAlex results for a single boolean search query,
    searching only the title + abstract field (no relevance sorting).

    Uses cursor-based pagination (works fine here since we no longer sort
    by relevance_score, and it has no 10,000-result cap like page-number
    pagination does).

    keywords : optional list of OpenAlex keyword-taxonomy strings
        (e.g. ["climate change"]). If given, ANDed on top of the
        title_and_abstract search via filter=keywords.keyword:a|b|c.
        NOTE: this matches OpenAlex's own auto-assigned keyword tags,
        not arbitrary free text — it's a controlled vocabulary, so
        site-specific terms (place names, etc.) usually won't match here.
    """
    results = []
    cursor = "*"

    filter_str = f"title_and_abstract.search:{query}"
    if keywords:
        keyword_or = "|".join(keywords)
        filter_str += f",keywords.keyword:{keyword_or}"

    while True:
        params = {
            "filter": filter_str,
            "per-page": per_page,
            "cursor": cursor,
        }
        if mailto:
            params["mailto"] = mailto

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        page_results = data.get("results", [])
        results.extend(page_results)

        if max_results is not None and len(results) >= max_results:
            results = results[:max_results]
            break

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor or not page_results:
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    return results


def extract_row(work, query):
    return {
        "query": query,
        "doi": get_doi(work),
        "authors": get_authors(work),
        "year": work.get("publication_year", ""),
        "source": get_source(work),
        "title": work.get("display_name", ""),
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
    }


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    fieldnames = ["query", "doi", "authors", "year", "source", "title", "abstract"]
    all_rows = []

    for i, query in enumerate(QUERIES, start=1):
        print(f"[{i}/{len(QUERIES)}] Searching: {query}")
        try:
            works = search_openalex(query, max_results=MAX_RESULTS_PER_QUERY)
        except requests.HTTPError as e:
            print(f"  ERROR for query '{query}': {e}")
            continue

        rows = [extract_row(w, query) for w in works]
        all_rows.extend(rows)
        print(f"  -> {len(rows)} works retrieved")

        # Write one CSV per query
        safe_name = f"query_{i}.csv"
        out_path = f"{OUTPUT_DIR}/{safe_name}"
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    # Write combined CSV
    combined_path = f"{OUTPUT_DIR}/all_queries_combined.csv"
    with open(combined_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. {len(all_rows)} total rows written to {combined_path}")


if __name__ == "__main__":
    main()



