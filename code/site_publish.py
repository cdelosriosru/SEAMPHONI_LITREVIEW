"""
publish.py

Turns a list of result rows into a markdown table and writes/updates the
corresponding page under docs/updates/, without touching any commentary
you've already written there.

How it works:
- Each update page has a table region marked by:
      <!-- TABLE:START -->
      ...
      <!-- TABLE:END -->
  On every run, only the content between those markers is replaced.
  Everything else in the file (your comments, figures, notes) is left alone.
- If the page doesn't exist yet, it's created from a template.
- docs/index.md gets a link added automatically if it's not already there.
"""

import os
import re
from datetime import date as _date

TABLE_START = "<!-- TABLE:START -->"
TABLE_END = "<!-- TABLE:END -->"


def render_table(fieldnames, rows):
    lines = []
    lines.append("| " + " | ".join(fieldnames) + " |")
    lines.append("|" + "|".join(["---"] * len(fieldnames)) + "|")
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
    table_block = f"{TABLE_START}\n\n{table_md}\n\n{TABLE_END}"

    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(_template(title, date, table_md))
        return "created"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        re.escape(TABLE_START) + r".*?" + re.escape(TABLE_END), re.DOTALL
    )
    if pattern.search(content):
        new_content = pattern.sub(table_block, content)
    else:
        new_content = content.rstrip() + f"\n\n## Results\n\n{table_block}\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    return "updated"


def ensure_index_link(index_path, date, slug, title):
    """Add a bullet linking to this update from docs/index.md, if not already present."""
    link_target = f"updates/{date}-{slug}.md"
    bullet = f"- [{date} — {title}]({link_target})"

    if not os.path.exists(index_path):
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    if link_target in content:
        return

    marker = "<!-- Add a new bullet above this line each time you publish a new update -->"
    if marker in content:
        content = content.replace(marker, f"{bullet}\n{marker}")
    else:
        content = content.rstrip() + f"\n\n## Updates\n\n{bullet}\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def auto_push(repo_dir=".", commit_message=None, remote="origin", branch=None):
    """Stages all changes, commits, and pushes. Skips cleanly if nothing changed."""
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


def publish_update(docs_dir, date, slug, title, fieldnames, rows):
    """Main entry point: renders the table, writes/updates the page, links it from index."""
    if date is None:
        date = _date.today().isoformat()

    table_md = render_table(fieldnames, rows)
    page_path = os.path.join(docs_dir, "updates", f"{date}-{slug}.md")

    status = upsert_update_page(page_path, title, date, table_md)
    ensure_index_link(os.path.join(docs_dir, "index.md"), date, slug, title)

    print(f"[publish] {status}: {page_path}")
    return page_path