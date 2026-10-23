#!/usr/bin/env python3
"""Gate a Haiku fact-check of a summarize-paper extract (Step 4D).

Haiku's own verdict is not trusted on its own. For every claim it listed, this script
re-checks what can be checked mechanically:

- source "text" / "table": the verbatim `quote` must occur in the paper's text layer (in order,
  in a few long pieces; see found() for the two-column allowance).
  A missing quote, or one that is not there, flags the claim.
- source "figure": no quote is required (the content is pixels). Any `quote` given (a
  caption, a printed label) must still occur in the text layer.
- source "absence" (the paper gives no code archive, does not report X): nothing can
  be quoted. With verdict "supported" and the search terms Haiku used recorded in `note`,
  it is not flagged but logged to <claims>.absence.json for audit (2026-10-23: 0 of ~17
  such flags led to a correction across 560 claims). Without search terms it is flagged,
  for the main thread to grep.
- any claim whose verdict is not "supported" is flagged, whatever its source.

Priority claims (--priority N): the main thread names the N claims the user's question
rests on, and Haiku must check each as id P1..PN with "priority": true. A missing one makes
the fact-check incomplete; every priority claim gets its own PRIORITY line, flagged or not,
so the user's question is reported apart from the rest.

It also checks the attest block: the fact-check is rejected as incomplete if Haiku says it
did not read the whole extract and text layer, or if it opened no PDF page although it
judged figure claims.

Usage:
    python3 check_claims.py --claims <basename>_factcheck.json --text <basename>.txt
                            [--priority <N>]

Prints one summary line, then one line per flagged claim. Writes the flagged rows to
<claims>.flags.json and the logged absence claims to <claims>.absence.json. Exit 0 = gate
ran (flags or not); 1 = fact-check incomplete, re-run it; 2 = malformed input.
"""
import argparse
import json
import re
import sys
import unicodedata

SOURCES = {"text", "table", "figure", "absence"}
VERDICTS = {"supported", "contradicted", "not_found"}


def norm(s):
    # Same idea as test/validate_grounding.py: survive the text layer's line wrapping
    # without fuzzy matching. NFKC first, so ligatures (ﬁ) and full-width digits become
    # plain letters; the Unicode minus becomes "-"; words hyphenated across a line break
    # are rejoined; then non-ASCII math glyphs are dropped on both sides, because they
    # round-trip inconsistently through text extraction.
    s = unicodedata.normalize("NFKC", s).replace("−", "-")
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


SKELETON_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789.%~")


def skeleton(text):
    # Letters and digits only, plus "." and "%" and a minus written as "~" when it sits
    # before a digit. Spaces go too: the text layer drops them between words
    # ("bymachines", "ofobservations"), and a hyphen kept from a line break
    # ("man-ufacturing") must not matter. Returns the skeleton and, for each of its
    # characters, its position in `text`, so a match can be mapped back to the spaced text.
    t = re.sub(r"-(?=\d)", "~", text)
    keep = [(c, i) for i, c in enumerate(t) if c in SKELETON_CHARS]
    return "".join(c for c, _ in keep), [i for _, i in keep]


def numbers(text):
    # Signed numbers in normalised (spaced) text: "-0.05", "851467" (thousands commas
    # dropped), "2002" out of "1984-2002" (a hyphen after a digit or letter is not a
    # sign), "1984" out of "with1984" (the text layer glues words to numbers).
    found = re.findall(r"((?<![\w.])-)?(?<![\d.])(\d[\d,]*(?:\.\d+)?)", text)
    return [sign + num.replace(",", "") for sign, num in found]


MIN_PIECE = 6


def found(quote, layer):
    # A two-column PDF's text layer interleaves the columns line by line, so a verbatim
    # sentence arrives cut into pieces with the other column's text between them. Accept
    # the quote when its skeleton can be laid down IN ORDER as a few long pieces (each at
    # least MIN_PIECE characters, at most one piece per 10 characters of quote) inside a
    # window of 3x its length + 200 characters. A quote of under 20 characters must occur
    # whole, since short pieces match by chance. The gaps between pieces could swallow a
    # minus sign or a digit, so every number in the quote must also stand, sign included,
    # among the numbers of the matched passage.
    skel, where, text = layer
    q, _ = skeleton(norm(quote))
    if not q:
        return False
    want = numbers(norm(quote))

    def numbers_intact(start, end):
        have = numbers(text[where[start]:where[end - 1] + 1])
        return all(n in have for n in want)

    if len(q) < 20:
        hit = skel.find(q)
        while hit != -1:
            if numbers_intact(hit, hit + len(q)):
                return True
            hit = skel.find(q, hit + 1)
        return False
    max_pieces = len(q) // 10 + 1
    start = skel.find(q[:MIN_PIECE])
    while start != -1:
        limit = start + 3 * len(q) + 200
        pos, rest, pieces = start, q, 0
        while rest and pieces < max_pieces:
            # the longest prefix of `rest` that occurs anywhere in the window
            n, hit = 0, -1
            while n < len(rest):
                nxt = skel.find(rest[:n + 1], pos, limit)
                if nxt == -1:
                    break
                n, hit = n + 1, nxt
            if n < min(MIN_PIECE, len(rest)):
                break
            pos, rest, pieces = hit + n, rest[n:], pieces + 1
        if not rest and numbers_intact(start, pos):
            return True
        start = skel.find(q[:MIN_PIECE], start + 1)
    return False


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"MALFORMED {path}: {e}")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--priority", type=int, default=0)
    args = ap.parse_args()

    data = load(args.claims)
    with open(args.text) as f:
        text = norm(f.read())
    layer = (*skeleton(text), text)

    if not isinstance(data, dict) or not isinstance(data.get("claims"), list) \
            or not isinstance(data.get("attest"), dict):
        print("MALFORMED: expected {\"attest\": {...}, \"claims\": [...]}")
        sys.exit(2)

    claims = data["claims"]
    attest = data["attest"]
    flags, absences = [], []
    for i, c in enumerate(claims):
        cid = c.get("id", f"#{i}")
        source, verdict, quote = c.get("source"), c.get("verdict"), c.get("quote")
        if source not in SOURCES or verdict not in VERDICTS:
            print(f"MALFORMED claim {cid}: source={source!r} verdict={verdict!r}")
            sys.exit(2)
        reasons = []
        if source == "absence":
            if verdict == "supported" and (c.get("note") or "").strip():
                absences.append({**c, "id": cid})
            elif not (c.get("note") or "").strip():
                reasons.append("absence claim without search terms: grep the text layer "
                               "for what is said to be missing")
        elif quote:
            if not found(quote, layer):
                reasons.append("quote not in text layer")
        elif source in ("text", "table"):
            reasons.append("no quote given")
        if verdict != "supported":
            reasons.append(f"Haiku verdict: {verdict}")
        if reasons:
            flags.append({**c, "id": cid, "reasons": reasons})

    n_fig = sum(1 for c in claims if c["source"] == "figure")
    incomplete = []
    if attest.get("read_extract_fully") is not True:
        incomplete.append("extract not read fully")
    if attest.get("read_text_layer_fully") is not True:
        incomplete.append("text layer not read fully")
    if n_fig and not attest.get("pdf_pages_opened"):
        incomplete.append(f"{n_fig} figure claims but no PDF page opened")
    if not claims:
        incomplete.append("no claims listed")
    have = {c.get("id") for c in claims}
    missing_p = [f"P{k}" for k in range(1, args.priority + 1) if f"P{k}" not in have]
    if missing_p:
        incomplete.append("priority claims not checked: " + ", ".join(missing_p))

    with open(args.claims + ".flags.json", "w") as f:
        json.dump(flags, f, indent=2, ensure_ascii=False)
    with open(args.claims + ".absence.json", "w") as f:
        json.dump(absences, f, indent=2, ensure_ascii=False)

    status = "INCOMPLETE (" + "; ".join(incomplete) + ")" if incomplete else "OK"
    print(f"{status} · {len(claims)} claims ({n_fig} figure) · {len(flags)} flagged · "
          f"{len(absences)} absence logged")
    flagged = {fl["id"] for fl in flags}
    for c in claims:
        if c.get("id", "").startswith("P") and c.get("priority"):
            print(f"PRIORITY {c['id']} {c.get('verdict')}{' FLAGGED' if c['id'] in flagged else ''}"
                  f" [{c.get('source')}, p.{c.get('page')}] :: {c.get('claim', '')[:160]}")
    for fl in flags:
        print(f"FLAG {fl['id']} [{fl['source']}, p.{fl.get('page')}] "
              f"{'; '.join(fl['reasons'])} :: {fl.get('claim', '')[:160]}")
    sys.exit(1 if incomplete else 0)


if __name__ == "__main__":
    main()
