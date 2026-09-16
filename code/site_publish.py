"""
site_publish.py

Writes/updates the public-facing docs/ pages from a search run, without
touching any commentary that's already been written by hand.

How it works:
- Two sections are "protected" by HTML comment markers:
      <!-- TABLE:START --> ... <!-- TABLE:END -->      (results table, per update page)
      <!-- TERMS:START --> ... <!-- TERMS:END -->       (search-terms table, index.md)
  On every run, only the content between a pair of markers is replaced —
  everything else in the file (comments, figures, notes) is left alone.
- A brand-new update page is created from a template if it doesn't exist yet.
- docs/index.md gets a link added automatically if it's not already there.

Usage from the search script:

    from site_publish import publish_update, update_search_terms_section, auto_push

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
"""

import os
import re
from datetime import date as _date

TABLE_START = "<!-- TABLE:START -->"
TABLE_END = "<!-- TABLE:END -->"

TERMS_START = "<!-- TERMS:START -->"
TERMS_END = "<!-- TERMS:END -->"


# --------------------------------------------------------------------------
# SHARED: marker-based "replace only this section" helper
# --------------------------------------------------------------------------

def replace_marked_section(path, start_marker, end_marker, new_content_md):
    """
    Replace everything between start_marker and end_marker in the file at
    `path` with new_content_md, leaving the rest of the file untouched.
    Returns True if the replacement happened, False if the file or the
    markers weren't found.
    """
    if not os.path.exists(path):
        print(f"[warn] {path} does not exist — nothing to update")
        return False

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    block = f"{start_marker}\n\n{new_content_md}\n\n{end_marker}"
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL
    )

    if not pattern.search(content):
        print(f"[warn] markers {start_marker} / {end_marker} not found in {path}")
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(pattern.sub(block, content))
    return True


# --------------------------------------------------------------------------
# RESULTS TABLE (per-update page under docs/updates/)
# --------------------------------------------------------------------------

def render_table(fieldnames, rows):
    lines = ["| " + " | ".join(fieldnames) + " |", "|" + "|".join(["---"] * len(fieldnames)) + "|"]
    for row in rows:
        cells = [str(row.get(col, "")) for col in fieldnames]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _template(title, date, table_md):
    return f"""---
title: {title}
date: {date}
---

[← Back to all updates](../index.md)

# {date} — {title}

## Results

{TABLE_START}

{table_md}

{TABLE_END}

## Comments

<!-- Write your interpretation here. This section is never overwritten by re-runs. -->
"""


def upsert_update_page(path, title, date, table_md):
    """Create the page if missing; otherwise replace only the table region."""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(_template(title, date, table_md))
        return "created"

    if replace_marked_section(path, TABLE_START, TABLE_END, table_md):
        return "updated"

    # Markers missing (e.g. hand-edited file) — append a Results section instead
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    block = f"{TABLE_START}\n\n{table_md}\n\n{TABLE_END}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.rstrip() + f"\n\n## Results\n\n{block}\n")
    return "updated"


def ensure_index_link(index_path, date, slug, title):
    """Add a bullet linking to this update from docs/index.md, if not already present."""
    link_target = f"updates/{date}-{slug}.md"
    bullet = f"- [{date} — {title}]({link_target})"

    if not os.path.exists(index_path):
        return  # let the user set up index.md manually first

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    if link_target in content:
        return  # already linked

    marker = "<!-- Add a new bullet above this line each time you publish a new update -->"
    if marker in content:
        content = content.replace(marker, f"{bullet}\n{marker}")
    else:
        content = content.rstrip() + f"\n\n## Updates\n\n{bullet}\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def publish_update(docs_dir, date, slug, title, fieldnames, rows):
    """
    Main entry point for a search run: renders the results table, writes/
    updates the update page, and links it from index.md.
    """
    if date is None:
        date = _date.today().isoformat()

    table_md = render_table(fieldnames, rows)
    page_path = os.path.join(docs_dir, "updates", f"{date}-{slug}.md")

    status = upsert_update_page(page_path, title, date, table_md)
    ensure_index_link(os.path.join(docs_dir, "index.md"), date, slug, title)

    print(f"[publish] {status}: {page_path}")
    return page_path


# --------------------------------------------------------------------------
# SEARCH TERMS TABLE (docs/index.md)
# --------------------------------------------------------------------------

def render_terms_table(term_groups):
    lines = ["| Term group | Terms |", "|---|---|"]
    for group, terms in term_groups.items():
        clean_terms = [t.strip('"') for t in terms]
        lines.append(f"| **{group}** | {', '.join(clean_terms)} |")
    return "\n".join(lines)


def update_search_terms_section(index_path, term_groups):
    """Replaces only the table between TERMS:START/END markers in index.md."""
    table_md = render_terms_table(term_groups)
    ok = replace_marked_section(index_path, TERMS_START, TERMS_END, table_md)
    if ok:
        print("[terms] index.md search-terms table synced")
    return ok


# --------------------------------------------------------------------------
# GIT: stage, commit, push
# --------------------------------------------------------------------------

def auto_push(repo_dir=".", commit_message=None, remote="origin", branch=None):
    """
    Stages all changes, commits, and pushes. Requires that:
      - `repo_dir` is inside a git repo that's already been cloned locally
      - git is configured with working credentials (SSH key via ssh-agent,
        or a cached HTTPS token) — this function does NOT set up auth, it
        just runs the commands as you would from the terminal.

    Safe to call every run: if there's nothing to commit, it skips the
    commit/push step instead of erroring.
    """
    import subprocess
    from datetime import datetime

    if commit_message is None:
        commit_message = f"Update results — {datetime.now().isoformat(timespec='minutes')}"

    def run(cmd):
        return subprocess.run(
            cmd, cwd=repo_dir, capture_output=True, text=True, check=False
        )

    add_result = run(["git", "add", "-A"])
    if add_result.returncode != 0:
        print("[auto_push] git add failed:", add_result.stderr.strip())
        return False

    status = run(["git", "status", "--porcelain"])
    if not status.stdout.strip():
        print("[auto_push] nothing to commit")
        return True

    commit_result = run(["git", "commit", "-m", commit_message])
    if commit_result.returncode != 0:
        print("[auto_push] git commit failed:", commit_result.stderr.strip())
        return False

    push_cmd = ["git", "push", remote]
    if branch:
        push_cmd.append(branch)
    push_result = run(push_cmd)
    if push_result.returncode != 0:
        print("[auto_push] git push failed:", push_result.stderr.strip())
        print("[auto_push] (often means auth isn't set up yet — see SSH key setup)")
        return False

    print(f"[auto_push] pushed: {commit_message}")
    return True