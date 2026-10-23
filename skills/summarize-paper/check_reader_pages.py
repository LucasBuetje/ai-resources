#!/usr/bin/env python3
"""Check from the reader subagent's own transcript that it read the whole paper (Step 4A).

The reader's reply line is a self-report. On 2026-10-23 a dissertation-chapter reader
replied `PAGES 134` after opening pages 79-98 only; it opened the rest after being sent
back, so even a union over its whole transcript looks complete. The transcript records
every tool call in order, so this script counts only what was read BEFORE the last write
of the extract:

- PDF pages: the union of the `pages` arguments of Read calls on the PDF (no `pages` =
  the whole file), against the page count from Step 3.
- Text layer: the line numbers Read actually returned for the text-layer file (taken from
  the result, since a call can return fewer lines than it asked for), against the file's
  non-blank lines.

A Read whose result was an error counts for nothing.

Usage:
    python3 check_reader_pages.py --agent-id <id from the Agent result> --pages <n> \\
        --pdf <source PDF> --text <basename>.txt --extract <extract .md> [--transcript <path>]

The page count comes from Step 3's output, so this script needs no PDF library. The
transcript is found at ~/.claude/projects/<cwd slug>/*/subagents/agent-<id>.jsonl, falling
back to any project folder; --transcript overrides the search.

Prints `OK` or the gaps, then one line per tool other than Read/Write the reader called.
Exit 0 = every page and every text-layer line read before the extract was written;
1 = something missing, or the extract never written; 2 = transcript not found.
"""
import argparse
import glob
import json
import os
import re
import sys

LINE_NO = re.compile(r"^\s*(\d+)\t", re.M)  # Read's "  42\t<line>" result format


def find_transcript(agent_id):
    root = os.path.expanduser("~/.claude/projects")
    slug = re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())
    name = f"agent-{agent_id}.jsonl"
    hits = glob.glob(os.path.join(root, slug, "*", "subagents", name))
    if not hits:
        hits = glob.glob(os.path.join(root, "*", "*", "subagents", name))
    return max(hits, key=os.path.getmtime) if hits else None


def parse_pages(spec, n_pages):
    # "1-20", "5,11,13"; None means the whole file
    if spec is None:
        return set(range(1, n_pages + 1))
    pages = set()
    for part in str(spec).split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            pages.update(range(int(a), int(b) + 1))
        elif part:
            pages.add(int(part))
    return pages & set(range(1, n_pages + 1))


def ranges(nums):
    # {1,2,3,7,8} -> "1-3,7-8"
    out, run = [], []
    for p in sorted(nums):
        if run and p == run[-1] + 1:
            run.append(p)
            continue
        if run:
            out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
        run = [p]
    if run:
        out.append(f"{run[0]}-{run[-1]}" if len(run) > 1 else str(run[0]))
    return ",".join(out) or "none"


def runs(nums):
    # {1,2,3,7,8} -> [[1,2,3],[7,8]]
    out = []
    for p in sorted(nums):
        if out and p == out[-1][-1] + 1:
            out[-1].append(p)
        else:
            out.append([p])
    return out


def result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(x.get("text", "") for x in content
                       if isinstance(x, dict) and x.get("type") == "text")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent-id")
    ap.add_argument("--pages", type=int, required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--extract", required=True)
    ap.add_argument("--transcript")
    args = ap.parse_args()

    path = args.transcript or (args.agent_id and find_transcript(args.agent_id))
    if not path or not os.path.exists(path):
        print(f"NO TRANSCRIPT for agent {args.agent_id}")
        sys.exit(2)
    with open(args.text) as f:
        text_lines = f.read().split("\n")
    n_lines = len(text_lines)
    blank = {i for i, t in enumerate(text_lines, 1) if not t.strip()}  # nothing to miss
    pdf, txt, ext = (os.path.basename(p) for p in (args.pdf, args.text, args.extract))

    # tool calls in transcript order, and their results
    order, calls, results = [], {}, {}
    with open(path) as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            if not isinstance(content, list):
                continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("id") not in calls:
                    order.append(b.get("id"))
                    calls[b.get("id")] = (b.get("name"), b.get("input") or {})
                elif b.get("type") == "tool_result":
                    results[b.get("tool_use_id")] = (b.get("is_error"), b.get("content"))

    def base(inp):
        return os.path.basename(inp.get("file_path", ""))

    writes = [i for i, cid in enumerate(order)
              if calls[cid][0] in ("Write", "Edit") and base(calls[cid][1]) == ext
              and not results.get(cid, (True,))[0]]
    if not writes:
        print(f"EXTRACT NEVER WRITTEN {ext}")
        sys.exit(1)

    pages, lines, other = set(), set(), {}
    for cid in order[:writes[-1]]:
        name, inp = calls[cid]
        err, content = results.get(cid, (True, None))
        if err:
            continue
        if name == "Read" and base(inp) == pdf:
            pages |= parse_pages(inp.get("pages"), args.pages)
        elif name == "Read" and base(inp) == txt:
            lines |= {int(n) for n in LINE_NO.findall(result_text(content))}
        elif name not in ("Read", "Write", "Edit", "SubagentHandback"):  # the last is the harness's
            other[name] = other.get(name, 0) + 1

    miss_p = set(range(1, args.pages + 1)) - pages
    miss_l = set(range(1, n_lines + 1)) - lines - blank
    if not miss_p and not miss_l:
        print(f"OK · {args.pages}/{args.pages} pages · {n_lines}/{n_lines} text-layer lines")
    if miss_p:
        print(f"PAGES MISSING {ranges(miss_p)} · {args.pages - len(miss_p)}/{args.pages} "
              f"opened before the extract was written ({ranges(pages)})")
    if miss_l:
        # report gaps with the blank lines inside them, so a skipped stretch reads as one range
        gaps = [r for r in runs(miss_l | blank) if set(r) & miss_l]
        shown = ",".join(f"{r[0]}-{r[-1]}" if len(r) > 1 else str(r[0]) for r in gaps)
        print(f"TEXT LINES MISSING {shown} · {len(miss_l)} non-blank lines unread")
    for name, k in sorted(other.items()):
        print(f"OTHER TOOL {name} × {k}")
    sys.exit(1 if miss_p or miss_l else 0)


if __name__ == "__main__":
    main()
