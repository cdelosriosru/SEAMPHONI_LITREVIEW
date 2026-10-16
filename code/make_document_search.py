"""
print_queries.py

Prints every search query exactly as it would be sent to OpenAlex.
Makes no API calls and doesn't run the search.
"""

from OpenAlex_search_new_counts import QUERIES

for i, q in enumerate(QUERIES, start=1):
    print(f"[{i}] {q['label']}")
    print(q["query"])
    print()