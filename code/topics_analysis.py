
import ast
import json
import re
from collections import Counter
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# ---------------- settings ----------------


SCRIPT_DIR = Path(__file__).resolve().parent   # .../SEAMPHONI_LITREVIEW/code
REPO_ROOT = SCRIPT_DIR.parent                  # .../SEAMPHONI_LITREVIEW
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(REPO_ROOT))



CSV_PATH = REPO_ROOT / "results" / "papers_metadata.csv"  # <- your file
KEYWORD_COL = "Topics_subfields"                  # <- column name (e.g. "keywords.display_name")
OUTPUT_PNG = REPO_ROOT / "results" / "Topics_subfields_wordcloud.png"
EXCLUDE = set()                           # e.g. {"Computer science", "Biology"} to drop generic terms
MAX_WORDS = 150
# ------------------------------------------


def parse_keywords(cell):
    """Return a list of keyword strings from one cell, whatever format OpenAlex used."""
    if pd.isna(cell) or str(cell).strip() == "":
        return []
    text = str(cell).strip()

    # Case 1: JSON / Python list, e.g. [{"display_name": "Ocean acidification", "score": 0.6}, ...]
    if text.startswith("["):
        data = None
        for loader in (json.loads, ast.literal_eval):
            try:
                data = loader(text)
                break
            except Exception:
                pass
        if isinstance(data, list):
            out = []
            for item in data:
                if isinstance(item, dict):
                    name = item.get("display_name") or item.get("keyword")
                    if name:
                        out.append(name)
                elif isinstance(item, str):
                    out.append(item)
            return out

    # Case 2: delimited string, e.g. "Ocean acidification|Phytoplankton" or "a; b; c"
    return [k for k in re.split(r"\s*[|;]\s*", text) if k]


df = pd.read_csv(CSV_PATH)
if KEYWORD_COL not in df.columns:
    raise KeyError(f"Column '{KEYWORD_COL}' not found. Available columns: {list(df.columns)}")

# Count each keyword once per paper, keeping multi-word keywords as one term
counts = Counter()
for cell in df[KEYWORD_COL]:
    kws = {k.strip().lower() for k in parse_keywords(cell)}
    counts.update(k for k in kws if k and k not in {e.lower() for e in EXCLUDE})

print(f"{len(df)} records, {len(counts)} unique keywords")
print("Top 20:")
for kw, n in counts.most_common(20):
    print(f"  {n:4d}  {kw}")

wc = WordCloud(
    width=1600,
    height=900,
    background_color="white",
    colormap="Reds",
    max_words=MAX_WORDS,
    prefer_horizontal=0.9,
    collocations=False,
).generate_from_frequencies(counts)

plt.figure(figsize=(16, 9))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.tight_layout()
plt.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
plt.show()
print(f"Saved {OUTPUT_PNG}")