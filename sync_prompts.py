#!/usr/bin/env python3
"""
sync_prompts.py
───────────────
Syncs system prompts from ~/.gemini (source of truth) → ai-resources repo.
Strips YAML frontmatter from .md files before copying.

Usage:
    python sync_prompts.py          # sync all, report changes
    python sync_prompts.py --dry    # preview only, no copies
    python sync_prompts.py --push   # sync + git commit & push
"""

import argparse
import re
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────
GEMINI_DIR = Path.home() / ".gemini"
REPO_DIR = Path.home() / "code_macbook" / "ai-resources"

# ── File Mapping ─────────────────────────────────────────────────────
# Each tuple: (source relative to GEMINI_DIR, dest relative to REPO_DIR)
# To add a new prompt, just append a tuple.
MAPPINGS = [
    # Antigravity system prompt
    ("GEMINI.md", "Antigravity/antigravity_general_instructions.md"),

    # Antigravity skills
    ("antigravity/skills/r-development/SKILL.md", "Antigravity/r-development/r-development.md"),
    ("antigravity/skills/r-development/examples/safe_merge.R", "Antigravity/r-development/examples/safe_merge.R"),
    ("antigravity/skills/r-code-auditing/SKILL.md", "Antigravity/r-code-auditing/r-code-auditing.md"),
    ("antigravity/skills/r-code-formatter/SKILL.md", "Antigravity/r-code-formatter/r-code-formatter.md"),
    ("antigravity/skills/latex-drafting/SKILL.md", "Antigravity/latex-drafting/latex-drafting.md"),
    ("antigravity/skills/latex-auditing/SKILL.md", "Antigravity/latex-auditing/latex-auditing.md"),
]

# ── Colours ──────────────────────────────────────────────────────────
RED = "\033[0;31m"
GRN = "\033[0;32m"
YLW = "\033[0;33m"
CYN = "\033[0;36m"
RST = "\033[0m"


# Regex: matches opening --- through closing --- (with optional trailing newline)
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n?", re.DOTALL)


def _strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter from markdown content."""
    return _FRONTMATTER_RE.sub("", text, count=1)


def _read_content(path: Path) -> str:
    """Read file, stripping YAML frontmatter for .md files."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        text = _strip_frontmatter(text)
    return text


def sync(dry: bool = False, push: bool = False) -> None:
    changed, skipped, errors = 0, 0, 0

    print(f"\n{CYN}═══ Prompt Sync: ~/.gemini → ai-resources ═══{RST}\n")

    for src_rel, dst_rel in MAPPINGS:
        src = GEMINI_DIR / src_rel
        dst = REPO_DIR / dst_rel

        # Source missing
        if not src.is_file():
            print(f"  {RED}✗ MISSING{RST}  {src_rel}")
            errors += 1
            continue

        # Prepare content (frontmatter stripped for .md)
        content = _read_content(src)

        # Already identical
        if dst.is_file() and dst.read_text(encoding="utf-8") == content:
            print(f"  {GRN}✓ current{RST}  {dst_rel}")
            skipped += 1
            continue

        # Copy or preview
        if dry:
            print(f"  {YLW}⟳ would update{RST}  {dst_rel}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding="utf-8")
            print(f"  {YLW}⟳ updated{RST}   {dst_rel}")
        changed += 1

    # Summary
    print(f"\n{CYN}───────────────────────────────────────────────{RST}")
    label = "Dry run" if dry else "Synced"
    verb = "would change" if dry else "updated"
    print(f"  {label}: {YLW}{changed}{RST} {verb}, {GRN}{skipped}{RST} current, {RED}{errors}{RST} missing\n")

    # Optional git push
    if push and not dry and changed > 0:
        print(f"{CYN}Committing and pushing to ai-resources...{RST}")
        subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"sync: update system prompts ({date.today()})"],
            cwd=REPO_DIR,
            check=True,
        )
        subprocess.run(["git", "push"], cwd=REPO_DIR, check=True)
        print(f"{GRN}Done.{RST}")
    elif push and changed == 0:
        print(f"{GRN}Nothing changed, skipping push.{RST}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync prompts to ai-resources repo.")
    parser.add_argument("--dry", action="store_true", help="Preview only, no copies")
    parser.add_argument("--push", action="store_true", help="Git commit & push after sync")
    args = parser.parse_args()
    sync(dry=args.dry, push=args.push)
