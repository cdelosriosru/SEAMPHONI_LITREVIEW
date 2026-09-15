"""
Merge systematic-literature-search exports from three sources:
  - Web of Science  (folder of .xls/.xlsx/.csv/.txt exports)
  - Scopus          (folder of .csv exports)
  - OpenAlex API    (folder of .csv exports pulled from the API)

into a single clean CSV with columns: DOI, Title, Abstract, Year, Journal.
Duplicate records (matched on normalized DOI) are removed, keeping the most
complete version of each record.

USAGE
-----
1. Edit the three folder paths in the CONFIG section below to match your
   local folders.
2. Run:  python3 merge_literature.py
3. Output is written to OUTPUT_PATH (default: merged_literature.csv in the
   current folder).

Each source folder can contain multiple files (e.g. WoS/Scopus exports are
often split into batches of 500/2000 records) - every matching file in the
folder (and its subfolders) is read and combined automatically.
"""

import json
import re
from pathlib import Path

import pandas as pd


# =========================================================================
# 1. CONFIG - EDIT THESE PATHS
# =========================================================================
WOS_FOLDER = "LiteratureReview_SEAMPHONI/WOS"
SCOPUS_FOLDER = "LiteratureReview_SEAMPHONI/SCOPUS"
OPENALEX_FOLDER = "LiteratureReview_SEAMPHONI/Openalex/API"

OUTPUT_PATH = "LiteratureReview_SEAMPHONI/merged_literature.csv"

# Web of Science column names -> standard field names
WOS_COLUMNS = {
    "doi": "DOI",
    "title": "Article Title",
    "abstract": "Abstract",
    "year": "Publication Year",
    "journal": "Source Title",
}

# Scopus column names -> standard field names
SCOPUS_COLUMNS = {
    "doi": "DOI",
    "title": "Title",
    "abstract": "Abstract",
    "year": "Year",
    "journal": "Source title",
}

OPENALEX_COLUMN_CANDIDATES = {
    "doi": "doi",
    "title": "title",
    "abstract": "abstract",
    "year": "year",
    "journal": "source",
}


# =========================================================================
# 2. HELPERS
# =========================================================================
def normalize_doi(doi):
    """Lowercase, strip whitespace, and remove URL/prefix so DOIs from
    different databases match each other, e.g. 'https://doi.org/10.X',
    '10.X', and 'doi:10.X' all become '10.x'."""
    if doi is None or (isinstance(doi, float) and pd.isna(doi)):
        return None
    doi = str(doi).strip().lower()
    if not doi or doi == "nan":
        return None
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    doi = doi.strip().strip("/")
    return doi if doi else None


def clean_text(value):
    """Collapse whitespace/newlines and strip; return None for empty/NaN."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    if text.lower() in ("", "nan", "none"):
        return None
    return text



def find_files(folder, extensions):
    """Recursively find all files in `folder` with any of `extensions`."""
    folder_path = Path(folder)
    if not folder_path.exists():
        print(f"  WARNING: folder not found: {folder}")
        return []
    files = [
        p for p in folder_path.rglob("*")
        if p.is_file() and p.suffix.lower() in extensions
    ]
    return sorted(files)


def read_table(path):
    """Read a .xls/.xlsx/.csv/.txt/.tsv file into a DataFrame."""
    suffix = path.suffix.lower()
    if suffix in (".xls", ".xlsx"):
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path, sep=",", encoding="utf-8-sig")
    # default: csv (utf-8-sig handles BOM, common in Scopus exports)
    return pd.read_csv(path, encoding="utf-8-sig")


def load_tabular_source(folder, column_map, source_name):
    """Load every table file in a folder using a fixed column mapping,
    returning a standardized DataFrame with columns:
    doi, title, abstract, year, journal, source."""
    files = find_files(folder, {".xls", ".xlsx", ".csv", ".tsv", ".txt"})
    print(f"[{source_name}] found {len(files)} file(s) in {folder}")

    frames = []
    for f in files:
        print(f"  reading {f}")
        try:
            df = read_table(f)
        except Exception as e:
            print(f"  ERROR reading {f}: {e}")
            continue

        out = pd.DataFrame()
        for field, src_col in column_map.items():
            if src_col in df.columns:
                out[field] = df[src_col]
            else:
                out[field] = None
        out["source"] = source_name
        out["source_file"] = str(f)
        frames.append(out)

    if not frames:
        return pd.DataFrame(columns=["doi", "title", "abstract", "year",
                                      "journal", "source", "source_file"])
    return pd.concat(frames, ignore_index=True)





# =========================================================================
# 3. LOAD ALL THREE SOURCES
# =========================================================================
wos_df = load_tabular_source(WOS_FOLDER, WOS_COLUMNS, "Web of Science")
scopus_df = load_tabular_source(SCOPUS_FOLDER, SCOPUS_COLUMNS, "Scopus")
openalex_df = load_tabular_source(OPENALEX_FOLDER, OPENALEX_COLUMN_CANDIDATES, "OpenAlex")

combined = pd.concat([wos_df, scopus_df, openalex_df], ignore_index=True)
print(f"\nTotal records loaded across all sources: {len(combined)}")
print(combined["source"].value_counts().to_string())

# =========================================================================
# 4. CLEAN FIELDS
# =========================================================================
combined["doi"] = combined["doi"].apply(normalize_doi)
for col in ["title", "abstract", "journal"]:
    combined[col] = combined[col].apply(clean_text)
combined["year"] = pd.to_numeric(combined["year"], errors="coerce").astype("Int64")

combined['Demo_site'] = combined['source_file'].astype(str).str[-5]

# =========================================================================
# 5. DEDUPLICATE BY DOI
#    Records without a DOI can't be matched this way, so they are kept as-is
#    (flagged below so you can review them manually if you want).
# =========================================================================
has_doi = combined["doi"].notna()
no_doi_count = (~has_doi).sum()
if no_doi_count:
    print(f"\nNOTE: {no_doi_count} record(s) have no DOI and cannot be "
          f"deduplicated by DOI; they are kept as-is.")

with_doi = combined[has_doi].copy()
without_doi = combined[~has_doi].copy()

before = len(with_doi)
# When the same DOI shows up more than once, keep the version with the
# fewest missing fields (i.e. the most complete record).
with_doi["_missing_count"] = with_doi[["title", "abstract", "year", "journal"]].isna().sum(axis=1)
with_doi = with_doi.sort_values("_missing_count")
with_doi = with_doi.drop_duplicates(subset=['doi','Demo_site'], keep="first")
with_doi = with_doi.drop(columns="_missing_count")
after = len(with_doi)
print(f"\nDuplicate DOIs removed: {before - after}")

final = pd.concat([with_doi, without_doi], ignore_index=True)

# =========================================================================
# 6. FINALIZE + SAVE
# =========================================================================
final = final.rename(columns={
    "doi": "DOI",
    "title": "Title",
    "abstract": "Abstract",
    "year": "Year",
    "journal": "Journal",
})

# Arrange by Demo_site then DOI(this defines the position used for the ID),
# then assign ID = "<position within Demo_site>_D<Demo_site>".
# groupby().cumcount() is a single vectorized pass over the whole frame,
# so this stays O(n log n) overall (dominated by the sort) with no
# per-row Python loops.
final = final.sort_values(by=["Demo_site", "DOI"], na_position="last").reset_index(drop=True)
position_in_site = final.groupby("Demo_site").cumcount() + 1
final["ID"] = position_in_site.astype(str) + "_D" + final["Demo_site"].astype(str)

# Put ID first for readability
cols = ["ID"] + [c for c in final.columns if c != "ID"]
final = final[cols]

final.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved {len(final)} records to {OUTPUT_PATH}")


