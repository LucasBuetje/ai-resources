#!/usr/bin/env python3
"""Apply the reader's answers to the fact-check disputes (summarize-paper Step 4E).

The reader that wrote the extract re-examines each dispute and answers with a decision:

- "haiku_right": the extract is wrong. `old` is an exact passage of the extract, `new` its
  replacement in the paper's own terms. Applied only if `old` occurs exactly once.
- "extract_right": the extract stands; `evidence` says what the page shows.
- "unclear": the page does not settle it; reported to the user as an open dispute.

Before the first edit, the extract is copied to <extract stem>.pre-factcheck.md so every
correction stays auditable.

With --flags (the gate's <factcheck.json>.flags.json) and --dropped (the flags the main
thread's grep dropped, each with its `triage` hit), the script also checks that the
fact-check is closed: every flag is either a dispute or dropped, and no figure flag is
dropped, because only a reader with the page image can settle a figure. Nor is a flag whose
Haiku verdict is "contradicted" or "not_found": a grep hit does not show the claim is right
(2026-10-22: 61 of 75 such dropped flags were real errors). Nor is a priority claim
("priority": true), one the user's question rests on. Run it even when
there are no disputes (empty lists), so the closure check still runs.

Usage:
    python3 apply_corrections.py --extract <extract.md> --decisions <decisions.json>
                                 --disputes <disputes.json>
                                 [--flags <flags.json> --dropped <dropped.json>]

Prints one summary line, then one line per decision. Exit 0 = every flag accounted for,
every dispute answered and every "haiku_right" applied; 1 = a flag unaccounted for, a figure
or contradicted/not_found flag dropped, a dispute unanswered or a correction not applied (fix and re-run, or report
it); 2 = malformed input.
"""
import argparse
import json
import os
import shutil
import sys

DECISIONS = {"haiku_right", "extract_right", "unclear"}


def load(path):
    # A reader may wrap the JSON in a ```json fence or add
    # a line of prose around it. If the whole file does not parse, try the text between
    # the first "[" and the last "]" once; anything else is malformed.
    try:
        with open(path) as f:
            raw = f.read()
    except OSError as e:
        print(f"MALFORMED {path}: {e}")
        sys.exit(2)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        first, last = raw.find("["), raw.rfind("]")
        if first != -1 and last > first:
            try:
                return json.loads(raw[first:last + 1])
            except json.JSONDecodeError:
                pass
        print(f"MALFORMED {path}: {e}")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", required=True)
    ap.add_argument("--decisions", required=True)
    ap.add_argument("--disputes", required=True)
    ap.add_argument("--flags")
    ap.add_argument("--dropped")
    args = ap.parse_args()
    if bool(args.flags) != bool(args.dropped):
        print("MALFORMED: --flags and --dropped go together")
        sys.exit(2)

    decisions = load(args.decisions)
    disputes = load(args.disputes)
    if not isinstance(decisions, list) or not isinstance(disputes, list):
        print("MALFORMED: decisions and disputes must both be JSON lists")
        sys.exit(2)
    for d in decisions:
        if d.get("decision") not in DECISIONS or not d.get("id"):
            print(f"MALFORMED decision: {d}")
            sys.exit(2)
        if d["decision"] == "haiku_right" and not (d.get("old") and d.get("new") is not None):
            print(f"MALFORMED decision {d['id']}: haiku_right needs `old` and `new`")
            sys.exit(2)

    with open(args.extract) as f:
        text = f.read()

    by_id = {d["id"]: d for d in decisions}
    lines, problems, applied = [], 0, 0

    # Closure: no flag may vanish between the gate and the reader.
    if args.flags:
        flags, dropped = load(args.flags), load(args.dropped)
        if not isinstance(flags, list) or not isinstance(dropped, list):
            print("MALFORMED: flags and dropped must both be JSON lists")
            sys.exit(2)
        disputed = {d["id"] for d in disputes}
        dropped_ids = {d["id"] for d in dropped}
        for fl in flags:
            if fl["id"] in disputed:
                continue
            if fl["id"] not in dropped_ids:
                lines.append(f"UNACCOUNTED {fl['id']}: flagged by the gate, neither disputed nor dropped")
                problems += 1
            elif fl.get("source") == "figure":
                lines.append(f"FIGURE DROPPED {fl['id']}: a figure flag must go to the reader")
                problems += 1
            elif fl.get("priority"):
                lines.append(f"PRIORITY DROPPED {fl['id']}: a priority claim must go to the reader")
                problems += 1
            elif fl.get("verdict") in ("contradicted", "not_found"):
                lines.append(f"VERDICT DROPPED {fl['id']}: a {fl['verdict']} flag must go to the reader")
                problems += 1
    for disp in disputes:
        d = by_id.get(disp["id"])
        if d is None:
            lines.append(f"UNANSWERED {disp['id']}")
            problems += 1
            continue
        if d["decision"] != "haiku_right":
            lines.append(f"{d['decision'].upper()} {d['id']} :: {d.get('evidence', '')[:160]}")
            continue
        count = text.count(d["old"])
        if count != 1:
            lines.append(f"NOT APPLIED {d['id']}: `old` occurs {count} times in the extract")
            problems += 1
            continue
        text = text.replace(d["old"], d["new"])
        applied += 1
        lines.append(f"CORRECTED {d['id']} :: {d.get('evidence', '')[:160]}")

    if applied:
        stem, ext = os.path.splitext(args.extract)
        backup = stem + ".pre-factcheck" + ext
        if not os.path.exists(backup):
            shutil.copy2(args.extract, backup)
        with open(args.extract, "w") as f:
            f.write(text)

    counts = {k: sum(1 for d in decisions if d["decision"] == k) for k in DECISIONS}
    print(f"{'OK' if not problems else 'PROBLEMS'} · {len(disputes)} disputes · "
          f"{applied} corrected · {counts['extract_right']} extract right · "
          f"{counts['unclear']} unclear · {problems} problems")
    print("\n".join(lines))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
