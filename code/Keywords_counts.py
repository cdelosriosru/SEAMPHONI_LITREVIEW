# Objective: bar plot of the number of unique papers found by each query template,
# ignoring the ocean-group part of the label (e.g. "ES_core_Ocean_generic" -> "ES_core").
# A paper found by several ocean variants of the same template is counted once.

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------------------------------
# PATHS
# --------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
INPUT_CSV = REPO_ROOT / "results" / "papers_metadata.csv"
OUTPUT_PNG = REPO_ROOT / "results" / "papers_per_query_template.png"
OUTPUT_COUNTS = REPO_ROOT / "results" / "papers_per_query_template.csv"

OCEAN_SUFFIX = re.compile(r"_Ocean_\w+$")   # removes _Ocean_generic, _Ocean_habitats, ...


def strip_ocean(label):
    return OCEAN_SUFFIX.sub("", label.strip())


def main():
    df = pd.read_csv(INPUT_CSV, usecols=["Query_labels"]).dropna()

    counts = Counter()
    for cell in df["Query_labels"]:
        templates = {strip_ocean(lbl) for lbl in cell.split(";") if lbl.strip()}
        counts.update(templates)           # each paper counts once per template

    s = pd.Series(counts).sort_values(ascending=True)
    s.rename_axis("Query_template").rename("N_papers").sort_values(ascending=False).to_csv(OUTPUT_COUNTS)

    fig, ax = plt.subplots(figsize=(9, 0.45 * len(s) + 1.5))
    bars = ax.barh(s.index, s.values, color="#2a6f97")
    ax.bar_label(bars, labels=[f"{v:,}" for v in s.values], padding=3, fontsize=9)
    ax.set_xlabel("Number of unique papers")
    ax.set_title("Papers found per query template")
    ax.set_xlim(0, s.max() * 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=200)
    print(s.sort_values(ascending=False).to_string())
    print(f"\nSaved {OUTPUT_PNG} and {OUTPUT_COUNTS}")
    plt.show()


if __name__ == "__main__":
    main()