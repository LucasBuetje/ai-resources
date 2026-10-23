#!/usr/bin/env python3
"""Check a reading deck against the standard in reading-deck.md (summarize-paper Step 6).

The writer runs it until it exits 0; the main thread runs it once more before handing the
deck over. It checks what can be checked mechanically:

FAIL (exit 1)
  - the deck is not the template (no SLIDES START/END markers) or has no provenance line
  - a line of the template's CSS or script is missing (the writer may add CSS and must
    replace the QUIZ array, nothing else)
  - a main slide without an assertion title (h2), an act (data-act) or a takeaway (p.so)
  - an Identification act missing one of the five ladder rungs (data-rung)
  - a dfn without data-def; raw LaTeX in the text
  - a reference to the paper's tables, figures, sections or samples in a main slide's
    visible text (allowed in More boxes, the p.src footer, detail slides)
  - a number that is in neither the extract nor the text layer (rounding allowed, a share
    may appear as a percentage). Exempt: integers up to 20, years, and anything inside an element
    with class "own" (the writer's arithmetic) or "tick" (axis labels).
WARN
  - more than 80 visible words on a main slide; a figure without a howto line before it
  - an acronym whose first appearance is not a dfn; no glossary slide; no quiz in the
    Identification act; fewer than 15 or more than 22 main slides

Usage:
    python3 check_deck.py --deck <deck.html> --extract <extract.md> --text <basename>.txt
                          [--template <internal-slides.html>]
"""
import argparse
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_claims import norm, numbers  # noqa: E402  (same folder, live and in the repo)

ACTS = ["Question", "Setting", "Facts", "Method", "Identification", "Results", "Limits", "Use"]
RUNGS = ["question", "naive", "fix", "assumption", "payoff"]
SPECIAL = {"title", "section", "closing", "detail", "quiz"}
VOID = {"br", "img", "meta", "input", "hr", "link", "source", "wbr", "col", "area"}
PAPER_REF = re.compile(r"\b(Table|Tables|Figure|Fig\.|Appendix|Section|Sample [A-Z]\b|"
                       r"[Ee]q\.|[Ee]quation \(?\d|footnote|fn\.? ?\d)")
LATEX = re.compile(r"\\(frac|beta|alpha|gamma|sigma|mathrm|text|sum|hat|bar)\b|"
                   r"\$[^$\n]{0,80}[\\^_][^$\n]{0,80}\$")   # "$49 … $36" is money, not math
ACRONYM = re.compile(r"\b[A-Z][A-Z0-9]{1,6}s?\b")
ACRONYM_OK = {"US", "UK", "EU", "I", "A", "B", "C", "D", "OK", "PDF", "HTML"}


def plain(text):
    # Dashes, dots and signs between numbers ("pp. 7–16", "0.1795·12", "≈ 0.6") become
    # spaces before norm() drops non-ASCII, or the two numbers would be glued into one.
    text = text.replace("\u2212", "-")
    return norm(re.sub(r"[\u2010-\u2015\u00b7\u00d7\u2026\u2248\u2264\u2265\u2192]", " ", text))


class Slide:
    def __init__(self, attrs):
        self.cls = set((attrs.get("class") or "").split())
        self.act = attrs.get("data-act")
        self.rung = attrs.get("data-rung")
        self.glossary = "data-glossary" in attrs
        self.h2 = ""
        self.has_so = False
        self.visible = []      # main text: not in More, svg, footer
        self.all_text = []     # (text, exempt_numbers)
        self.paper_refs = []
        self.figures_without_howto = 0
        self.seen_howto = False

    @property
    def main(self):
        return "slide" in self.cls and not (self.cls & SPECIAL)


class DeckParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.slides = []
        self.cur = None
        self.dfn_missing = 0
        self.first_acronym = {}   # acronym -> True if its first appearance was in a dfn
        self.text_all = []

    def flags(self):
        f = {"skip": False, "more": False, "svg": False, "src": False, "exempt": False,
             "dfn": False, "h2": False}
        for tag, attrs in self.stack:
            cls = set((attrs.get("class") or "").split())
            if tag in ("script", "style", "title", "head"):
                f["skip"] = True
            if tag == "details":
                f["more"] = True
            if tag in ("svg", "figure", "img"):
                f["svg"] = True
            if "src" in cls:
                f["src"] = True
            if cls & {"own", "tick"}:
                f["exempt"] = True
            if tag == "dfn":
                f["dfn"] = True
            if tag == "h2":
                f["h2"] = True
        return f

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = set((attrs.get("class") or "").split())
        if tag == "section" and "slide" in cls:
            self.cur = Slide(attrs)
            self.slides.append(self.cur)
        if self.cur is not None:
            if tag == "p" and "so" in cls:
                self.cur.has_so = True
            if tag == "p" and "howto" in cls:
                self.cur.seen_howto = True
            if tag in ("svg", "img") and not self.flags()["svg"] and not self.flags()["more"]:
                if not self.cur.seen_howto:
                    self.cur.figures_without_howto += 1
                self.cur.seen_howto = False
        if tag == "dfn" and not attrs.get("data-def"):
            self.dfn_missing += 1
        if tag not in VOID:
            self.stack.append((tag, attrs))

    def handle_startendtag(self, tag, attrs):
        if tag in ("svg", "img"):
            self.handle_starttag(tag, attrs)
            if tag not in VOID:
                self.stack.pop()

    def handle_endtag(self, tag):
        for k in range(len(self.stack) - 1, -1, -1):
            if self.stack[k][0] == tag:
                del self.stack[k:]
                break
        if tag == "section":
            self.cur = None

    def handle_data(self, data):
        f = self.flags()
        if f["skip"] or not data.strip():
            return
        self.text_all.append(data)
        for m in ACRONYM.finditer(data):
            a = m.group(0).rstrip("s") if m.group(0).endswith("s") and len(m.group(0)) > 2 else m.group(0)
            if (a not in ACRONYM_OK and a not in self.first_acronym
                    and not re.fullmatch(r"[IVXL]+", a)):      # roman numerals
                self.first_acronym[a] = f["dfn"]
        s = self.cur
        if s is None:
            return
        s.all_text.append((data, f["exempt"]))
        if f["h2"]:
            s.h2 += data
        if not (f["more"] or f["svg"] or f["src"]):
            s.visible.append(data)
            if s.main:
                s.paper_refs += PAPER_REF.findall(data)


def template_lines_missing(deck, template):
    # Every non-empty line of the template's <style> and <script> must survive in the deck,
    # except the QUIZ array, which the writer replaces with its own.
    def blocks(html, tag):
        return "\n".join(re.findall(rf"<{tag}>(.*?)</{tag}>", html, re.S))
    missing = []
    for tag in ("style", "script"):
        have = {l.strip() for l in blocks(deck, tag).splitlines()}
        body = blocks(template, tag)
        if tag == "script":
            body = re.sub(r"var QUIZ = \[.*?\n\];", "", body, flags=re.S)
        for line in body.splitlines():
            if line.strip() and not line.strip().startswith("//") and line.strip() not in have:
                missing.append(line.strip())
    return missing


def source_numbers(*paths):
    have = set()
    for p in paths:
        with open(p) as f:
            for n in numbers(plain(f.read())):
                try:
                    have.add(float(n))
                except ValueError:
                    pass
    return have


def traced(num, have):
    # A deck number is traced if some source number rounds to it at the deck's precision,
    # directly or as a share shown in percent (0.35 -> 35%).
    d = float(num)                      # signed: -9.65 must come from a negative source
    places = len(num.split(".")[1]) if "." in num else 0
    for s in have:
        for v in (s, s * 100):
            if round(v, places) == d or (places == 0 and abs(v - d) < 0.5):
                return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", required=True)
    ap.add_argument("--extract", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--template",
                    default=os.path.expanduser("~/.claude/skills/deck/internal-slides.html"))
    args = ap.parse_args()

    raw = open(args.deck).read()
    fails, warns = [], []
    if "SLIDES START" not in raw or "SLIDES END" not in raw:
        fails.append("not built on the template: SLIDES START/END markers missing")
    if "Produced by" not in raw:
        fails.append("no provenance line ('Produced by …') on the title slide")
    if os.path.exists(args.template):
        lost = template_lines_missing(raw, open(args.template).read())
        if lost:
            fails.append(f"{len(lost)} template CSS/script line(s) missing, e.g. "
                         f"{lost[0][:70]!r}: copy the template whole")

    p = DeckParser()
    p.feed(raw)
    have = source_numbers(args.extract, args.text)

    mains = [s for s in p.slides if s.main]
    for n, s in enumerate(p.slides, 1):
        label = f"slide {n} '{s.h2.strip()[:50]}'"
        if s.main:
            if not s.h2.strip():
                fails.append(f"slide {n}: no assertion title (h2)")
            if s.act not in ACTS:
                fails.append(f"{label}: data-act {s.act!r} not one of {ACTS}")
            if not s.has_so:
                fails.append(f"{label}: no takeaway (p.so)")
            if s.paper_refs:
                fails.append(f"{label}: refers to the paper's {sorted(set(s.paper_refs))} in "
                             "visible text; point to a slide, or move it to More / p.src")
            words = len(" ".join(s.visible).split())
            if words > 80:
                warns.append(f"{label}: {words} visible words (aim for about 60)")
            if s.figures_without_howto:
                warns.append(f"{label}: {s.figures_without_howto} figure(s) without a howto line")
        if "detail" not in s.cls:
            for text, exempt in s.all_text:
                if exempt:
                    continue
                for num in numbers(plain(text)):
                    bare = num.lstrip("-")
                    if "." not in bare and (int(bare) <= 20 or 1900 <= int(bare) <= 2100):
                        continue
                    if not traced(num, have):
                        fails.append(f"slide {n}: number {num} is in neither the extract nor "
                                     "the text layer (mark the writer's arithmetic class=\"own\")")

    if p.dfn_missing:
        fails.append(f"{p.dfn_missing} dfn element(s) without data-def")
    latex = LATEX.findall(" ".join(p.text_all))
    if latex:
        fails.append(f"raw LaTeX in the text ({len(latex)} hit(s)); use MathML")

    ident = [s for s in p.slides if s.act == "Identification"]
    if ident:
        missing = [r for r in RUNGS if r not in {s.rung for s in ident}]
        if missing:
            fails.append(f"Identification act misses ladder rung(s): {missing}")
        if not any("quiz" in s.cls for s in ident):
            warns.append("no quiz slide in the Identification act")
    for a, in_dfn in p.first_acronym.items():
        if not in_dfn:
            warns.append(f"acronym {a}: first appearance is not a dfn")
    if not any(s.glossary for s in p.slides):
        warns.append("no glossary slide (detail slide with data-glossary)")
    if not 15 <= len(mains) <= 22:
        warns.append(f"{len(mains)} main slides (the standard asks for 15-22)")

    print(f"{'FAIL' if fails else 'OK'} · {len(p.slides)} slides ({len(mains)} main) · "
          f"{len(fails)} fail · {len(warns)} warn")
    for f in fails:
        print("FAIL", f)
    for w in warns:
        print("WARN", w)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
