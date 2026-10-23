---
name: summarize-paper
origin: adapted from https://github.com/scunning1975/MixtapeTools
targets: [claude]
description: "Summarize an academic paper (journal article, working paper, preprint), located via Zotero if needed. The read goes to a Claude Sonnet subagent by default, or to an Opus subagent on request (\"with Opus\"), so no PDF page image reaches the main thread; a Haiku subagent then fact-checks the extract. Auto-invoke for a whole-paper summary, and for a reading deck (HTML slides to understand a paper)."
allowed-tools: Agent, SendMessage, Bash(cd*), Bash(python*), Bash(pip*), Bash(mkdir*), Bash(ls*), Bash(cat*), Read, Write, Edit, mcp__zotero__zotero_search_items, mcp__zotero__zotero_search_by_citation_key, mcp__zotero__zotero_get_item_children, mcp__zotero__zotero_get_attachment_path
argument-hint: "[pdf-path | paper title | DOI | citation key] [— focus: what to extract] [— reader: opus] [— no-check] [— deck]"
---

# Summarize-Paper: Locate and Deep-Read a Paper in One Pass

This skill produces a deep, structured read of an **academic research paper** — journal
articles, working papers, preprints — where **one reader holds the whole paper at once**.

**One whole-paper read, not a chunk pipeline.** A single reader that holds every page at
once integrates cross-section facts (a figure on page 5 against a table on page 40),
describes figures from the actual pixels, and does not confabulate the way a reader of an
isolated 4-page chunk does. No split, no consolidate; afterwards one cheap Haiku
fact-check that a script gates (Step 4D).

**Where the read happens.**

- **Sonnet reader (default)** — the read goes to **one Claude subagent on `model: sonnet`** (Step 4A).
  Sonnet's 1M-token context holds a whole paper at once. The page images land in the
  subagent's context, which is discarded when it returns: **no PDF page image ever enters the
  main thread** (the PDF Reading rule). Claude extracts the text layer (no images), writes the
  reader prompt, spawns the subagent, and then reads the markdown extract it wrote. Everything
  else — Zotero lookup, the extraction spec, the cache, the presentation — stays in the main
  thread.
- **Opus reader (opt-in)** — when the user asks for Opus (`— reader: opus`,
  "with Opus"), the same subagent runs on `model: opus` (Step 4A). Use it when the paper is
  figure- or table-dense, when a Sonnet extract came back thin, or simply when the user
  prefers it.

## When This Skill Is Invoked

The user explicitly wants the agent to read, review, or summarize a **research paper**. The
input is either a file path to a local PDF, or a paper title, DOI, or citation key. You
cannot search for a paper you don't know exists — if invoked with no argument, ask what to
read; do not guess.

## Extraction spec: default vs focused

What gets extracted is customizable; the read mechanism is identical either way. Only the
*list of extraction targets* changes. Decide the spec once, here, before the cache check and
the read — both depend on which output file it writes.

**You — the main agent — build the extraction spec.** Interpreting the user's focus goal
into the numbered target list is a judgement call and stays in the main thread. The reader
receives the finished target list verbatim (Step 4). If the user's goal is ambiguous,
clarify it *before* the read starts.

- **Default (no focus given).** Use the standard **8 dimensions** (listed in Step 4). Output
  file: `pdf_reads/<basename>/<basename>_text.md`. This is the canonical, reusable extract.
- **Focused (the user gives a reading goal).** Translate the goal into a short numbered list
  of concrete extraction targets (typically 3–8). That list **replaces** the 8 dimensions.
  Pick a short kebab-case `<focus-slug>`; output file
  `pdf_reads/<basename>/<basename>__<focus-slug>.md`, with the extract's first line
  `> Focus: <the goal>`. A focused read **never** overwrites the default `<basename>_text.md`.
  If the user wants both, run the default first, then the focused read.

**Mark every quotation, whatever the spec.** Wording lifted verbatim from the paper goes in
quotation marks with its page or section; everything else is reworded in the reader's own
indirect speech. An unmarked passage in the extract is indistinguishable from paraphrase
downstream, and the extract feeds notes and drafts — that is how a source's sentences end
up in your own writing unattributed. Keep marked quotes short and few; the extract is a
summary, not a transcript.

Hold the chosen spec as the `EXTRACTION SPEC` used verbatim by the reader (Step 4).

**Reader choice.** A Sonnet subagent (Step 4A) unless the user asked for
Opus (Step 4A on `model: opus`). Don't switch readers on your own; if the
requested reader fails twice, offer the Sonnet subagent (or, if Sonnet failed, Opus) as the
fallback instead of stopping silently. The choice does not change the output filename: the
provenance stamp on the extract's first line records which model read it.

## Step 1: Acquire the PDF

**If a local file path is provided:** verify it exists; use it in place.

**If a title, DOI, or citation key is provided (no path)** — look the paper up in Zotero:
1. `zotero_search_by_citation_key` (citation key) or `zotero_search_items` (title/DOI) to
   find the item. (BetterBibTeX keys sometimes don't resolve; if so, fall back to a short
   `zotero_search_items` on author + year or title words.)
2. `zotero_get_attachment_path` (or `zotero_get_item_children` then construct
   `~/Zotero/storage/<attachmentKey>/<filename>`) to get the `application/pdf` attachment's
   on-disk path. Verify it exists (`ls`). If your PDFs are linked files rather than stored
   attachments, the path points into your own linked-file folder instead.

Do **not** use `zotero_get_item_fulltext` — that returns plain text only, with no tables,
figures, or layout. This skill must read the actual rendered PDF.

**If the paper is not usable from Zotero — no item match, no `application/pdf` attachment, or
the path does not exist: stop.** Do not search the web, do not download anything. Tell the user
the paper isn't in their Zotero library and ask them to add it (or give a file path). The
skill never downloads PDFs itself.

**Always preserve the original PDF.** Never delete, move, or overwrite the source. If a
Zotero call fails with a connection error, run `open -a Zotero && sleep 6` and retry once.
If a search returns nothing unexpectedly, the MCP may be on the wrong library — check
`zotero_list_libraries` and switch to the user library if needed.

## Step 2: Locate the output folder and check the cache

All output goes in a project-local `pdf_reads/` folder, one subfolder per paper:
`pdf_reads/<basename>/`. Create it if missing. The source PDF is never touched.

Look for the extract file matching the requested mode — `<basename>_text.md` (default) or
`<basename>__<focus-slug>.md` (focused). If found, ask:

> "An extract from a previous deep-read exists (`pdf_reads/<basename>/<file>`). Use it, or
> re-read the PDF from scratch?"

Name the model from the extract's stamp in the question, so the user can decide whether e.g.
a Sonnet extract is good enough when they asked for Opus. **Use extract** → read it, run Step 4D if no `<extract stem>_factcheck.json` sits beside it,
then Step 5. **Re-read** → continue. A default extract does not
satisfy a focused request (and vice versa).

## Step 3: Extract the text-layer anchor

Extract the whole file's text layer to `pdf_reads/<basename>/<basename>.txt`. This is
mechanical — run it in the main thread; it costs no image tokens. The text layer is the
**grounding anchor** the reader treats as authoritative for exact wording, names, and
numbers (image OCR can misread a digit in a coefficient table; the text layer doesn't). It
also stops the model reconstructing claims from prior knowledge instead of from the page.

```python
from pypdf import PdfReader
import os
pdf_path = "<source PDF>"
out_dir  = "pdf_reads/<basename>"
os.makedirs(out_dir, exist_ok=True)
reader = PdfReader(pdf_path)
text = "\n\n".join((p.extract_text() or "") for p in reader.pages)
basename = os.path.splitext(os.path.basename(pdf_path))[0]
with open(os.path.join(out_dir, f"{basename}.txt"), "w") as f:
    f.write(text)
print(f"{len(reader.pages)} pages, {len(text.split())} words extracted")
```

If `pypdf` is not installed: `pip install pypdf` (inside the project venv if one exists, per
the Python venv rule). `pdftotext -layout <pdf> pdf_reads/<basename>/<basename>.txt` is an
equivalent one-liner if it is already on the machine. A scanned, image-only PDF yields little/no text — note that and tell
the reader (Step 4) to rely on the page images, since there is no anchor.

## Step 4: Write the reader prompt

The reader gets one prompt: the source PDF, the text layer from Step 3, the EXTRACTION
SPEC, and the rules below. Two paragraphs — which tools it may use, and where its output
goes — are filled in by Step 4A.

**Write the prompt to a file first** — `pdf_reads/<basename>/<basename>_prompt.txt` — rather
than inlining it. It keeps the quoting sane, and the read is re-runnable by hand from the same
two files.

**Prompt file contents:**

```
Read this ENTIRE academic paper and extract the targets listed below. Do it in one pass.

Whole PDF:   <absolute source PDF path>
Text layer:  <absolute pdf_reads/<basename>/<basename>.txt>   ← AUTHORITATIVE for wording/numbers

<TOOLS PARAGRAPH — Step 4A>

HOW TO READ:
1. Read the text-layer file first. It is the authoritative source for all wording, names,
   and numbers — quote coefficients, sample sizes, and identifiers from it verbatim.
2. Then open the whole PDF. Use it for tables, figures, equations, and layout. For every
   FIGURE, describe what it actually SHOWS — the SHAPE of the picture: where the mass sits,
   which way a series moves, whether it is flat or trending before a threshold, whether two
   series separate or overlap, whether confidence bands include zero, whether a spike has a
   trough beside it. Not just the caption. The figure's visual content is information the text
   does not carry; do not skip a figure because its numbers happen to appear in the caption.
   **Describe figures in words, never in quantities of your own.** A number may leave a figure
   only if it is PRINTED — a data label, an annotated estimate, a value in the caption or note
   — or stated in the running text. Everything else about a figure is described without
   numbers at all.
   Specifically forbidden, because these are read off an axis rather than printed: the height
   of a bar or spike, the level of a line at a point, the value where a series starts or ends,
   the range a cloud of points occupies, an average of plotted points. Phrasings like
   "reaching approximately 40,000", "sits around 2,000–3,000", "stable around 61", "exceeding
   1,000,000", "mostly between 15 and 25", "averaging around 0.4 to 0.6", "hovering around
   0.05" are all violations — the hedge does not rescue them. Also never compute a gap,
   difference, ratio, slope, growth rate, or effect size between plotted series or points.
   Say it qualitatively instead: "the spike at the ERA is by far the tallest in the
   distribution, several times the height of the surrounding months, and the series is
   otherwise smooth" carries the finding; "reaching approximately 40,000 exits" does not, and
   is not checkable. Where the paper does not state a quantity, say the magnitude is not
   reported. This binds everywhere in the extract, not only in the figure descriptions, and
   appendix / supplementary / Extended Data figures count as figures.
3. READ THE FOOTNOTES AND TABLE NOTES. They are where a paper states the caveat it does not
   put in the body: the threat to identification the authors concede, why a variable was
   constructed one way and not another, which robustness check is "not reported", who pointed
   out a problem. A caveat the authors raise about their OWN headline result belongs in the
   extract next to that result, not dropped. Same for a stated limitation.
4. If the text layer is empty/near-empty (a scanned PDF), say so and rely on the pages.

HARD RULES:
- Extract ONLY what THIS paper contains. Do NOT use prior knowledge of the topic, of related
  studies, or of this paper from any other source. If you would name a study, setting,
  dataset, author, or number that is not in this paper, do not.
- If the paper cites OTHER studies, report them as "the paper cites X" — attribute only what
  the page says about them.
- Report exact coefficient estimates, standard errors / confidence intervals, sample
  sizes, identification details, equation references, data sources, URLs.
- Wording lifted verbatim from the paper goes in quotation marks with its page or section;
  everything else is reworded in your own indirect speech.
- NO NUMBER INFERRED FROM A FIGURE. If a quantity is neither printed on the figure nor stated
  in the text, it does not enter the extract in any form — not as an approximation, not hedged
  with "roughly" / "about" / "~", not as a range. Saying the paper does not report it is the
  correct answer.
- NO ARITHMETIC ON THE PAPER'S NUMBERS EITHER. Do not divide, subtract, rescale, convert to a
  percentage, or otherwise compute a new figure from values in a table or the text. Report the
  paper's own numbers and the paper's own characterisation of them. If the paper writes
  "slightly less than 10% of the original variance remains", that phrase is the finding —
  do NOT replace it with a ratio you worked out from the table.
- If the paper does not contain something the spec asks for (no results table, no replication
  archive, no data-availability statement), say that plainly. Do not substitute the nearest
  available thing without saying so. **Absence is a finding and is reported as absence** — the
  correct sentence is "the paper gives no access route for the data", never a plausible access
  route supplied from your own knowledge of how such data usually works.
- **Do not append the explanation either.** Having correctly reported an absence, do not follow
  it with a parenthetical saying why, or how access to that kind of source normally works, or
  what such records are typically governed by. "The paper gives no access route" followed by
  "(records of this kind are protected under federal privacy law and require an approved
  research agreement)" is the same violation wearing brackets: the second clause is not in the
  paper. The sentence ends at the absence.

<OUTPUT PARAGRAPH — Step 4A>

EXTRACTION SPEC: <injected verbatim — see below>
```

**EXTRACTION SPEC written into the prompt file.** Whichever list it is, demand concrete
specifics — data sources, variable names, equation references, sample sizes, coefficients,
standard errors — not a vague summary.

```
DEFAULT (8 dimensions) — what a researcher would need to build on or replicate the work:
1. Research question — what is asked, why it matters
2. Audience — which sub-community cares
3. Method — how the question is answered; identification strategy
4. Data — sources, unit of observation, sample size, time period; where the data came from
5. Statistical methods — econometric techniques, key specifications
6. Findings — main results, key coefficient estimates and standard errors; what the figures show
7. Contributions — what is now known that wasn't
8. Replication feasibility — what a replicator would actually be blocked by. Data: named
   source, and the access route AS STATED IN THE PAPER (if none is stated, say so — do not
   supply one). Code/replication archive: URL if given, otherwise say none is given. What the
   tables do and do not report (e.g. t-statistics only, no standard errors). Which results are
   described as "not reported" / "not shown" and therefore cannot be checked. Any data
   appendix, and what is in it.

FOCUSED — replace the 8 dimensions with the user's numbered target list; the instructions
above apply unchanged to those targets.
```

**Two spot-checks after every read**, whichever model produced the extract — both are cheap,
and both errors were caught in the run this recipe was built from (they are a class, not a
model quirk). First, **§8 and any other absence claim**: if the extract explains
*why* data are unavailable (privacy law, an agency's access procedure, a permit authority)
check that the paper actually says so — supplying a plausible-sounding access story is the
characteristic prior-knowledge slip. Second, **hedged quantities** — the residue of the figure
rule that prompting does not fully remove, and the one failure that survives on figure-dense
papers:

```bash
grep -nE "around [0-9]|approximately [0-9]|roughly [0-9]|exceeding [0-9]|~[0-9]" <extract>
```

**Expect nearly all hits to be legitimate** — papers hedge their own numbers, and a year read
off a time axis ("peaks around 1990") is a date, not a magnitude. For each hit, `grep` the text
layer for the number; if it is there, keep it. Only if it is absent did it come off an axis, and
only then cut it or replace it with the paper's own wording.

**`grep` the whole text layer, not a filtered subset, and remember it wraps mid-sentence** —
"jumps ⏎ by approximately 0.40 units" will not match a search for `jumps by approximately`.
Search the bare number. A false accusation here costs more than the error it hunts: it
provokes edits to a prompt that was working.

Both checks exist because these are quiet errors — the extract reads perfectly either way —
and because the reader prompt has been tuned to the point of diminishing returns on both. Two
greps in the main thread are cheaper and more reliable than more instruction text.

## Step 4A: Claude Code — Claude subagent reader (default: Sonnet)

Spawn **one** `Agent` call with `subagent_type: pdf-reader` and `model: sonnet` — or
`model: opus` when the user asked for Opus. `pdf-reader` is a custom agent
(`~/.claude/agents/pdf-reader.md`) with only Read and Write: two of three readers in the
2026-10-23 run used Bash although the prompt forbade it, and a tool list cannot be talked
around. If the type is missing (the `Agent` call names an unknown type), fall back to
`general-purpose` and say so. Sonnet's 1M-token context holds a whole paper's
page images plus appendix, so the one-reader-holds-everything design needs no chunking. The
page images land in the subagent's context, which is discarded when it returns; the main
thread only ever reads the markdown extract.

Fill the two per-reader slots of the Step 4 prompt file with:

- **TOOLS PARAGRAPH:**
  ```
  Use only two tools: Read (on the two files above) and Write (for the output file below).
  No Bash, no search, no web. Read the text layer first, in full: if Read says the file is
  too large, read it with `offset`/`limit` in consecutive pieces until its last line. Then
  read the WHOLE PDF
  with Read's `pages` parameter in consecutive ranges of at most 20 pages (1-20, 21-40, …)
  until the last page, so you hold every page at once before writing — do not skip the
  appendix.
  ```
- **OUTPUT PARAGRAPH:**
  ```
  Write the extraction with the Write tool to: <absolute output path>
  Start the file directly with the first target heading (for a focused read, the
  `> Focus: <goal>` line first). One `## ` heading per numbered target, its text taken from
  the spec below; nested structure under it as needed.
  Write the file only once you have read every page. Your final reply to me is ONE line
  only: `MODEL <your model ID as your system prompt states it> · RANGES <the page ranges you
  opened, e.g. 1-20,21-40,41-51> · WROTE <path>`. Do not repeat the extraction in the reply.
  ```

Then pass the prompt file's contents as the `Agent` prompt. The PDF never enters the main
thread; the subagent's one-line reply is all that comes back. Keep the agent ID the `Agent`
result gives: Step 4E sends the fact-check disputes back to this reader.

**Verify from the transcript, not the reply.** The reply is a self-report: on 2026-10-23
two of three dissertation-chapter readers wrote their extract after opening 20 of 134 and
55 of 113 pages, and one replied `PAGES 134`. Run

```bash
python3 ~/.claude/skills/summarize-paper/check_reader_pages.py --agent-id <agent ID> \
  --pages <page count from Step 3> --pdf <source PDF> --text <basename>.txt --extract <extract>
```

It reads the reader's own transcript and counts the PDF pages and text-layer lines it
read before it last wrote the extract. Exit 1 (`PAGES MISSING`, `TEXT LINES MISSING`,
`EXTRACT NEVER WRITTEN`) → `SendMessage` the reader the missing ranges, tell it to read
them and rewrite the extract, and run the check again; still failing → report it. Exit 2
(no transcript) → fall back to checking that the `RANGES` line covers 1 to the page count,
and say the check was the reply's. `OTHER TOOL` lines mean the `pdf-reader` type was not
used; mention them.

**Stamp** the extract's first line (second, below `> Focus:`) with
`*Extract produced by <model ID from the MODEL line> (Claude subagent) · <YYYY-MM-DD>*`. If the
reply carries no MODEL line, write `claude <sonnet|opus> (model ID not reported)` with the
tier you passed.

Run the Step 4 spot-checks, then Step 4D.

## Step 4D: Claude Code — Haiku fact-check (every read)

After the spot-checks, one **Haiku** subagent checks the extract claim by claim against the
paper. It costs a few cents and about five minutes (a 15-page paper, 2026-10-08: 134
claims, ~210k Haiku tokens), and it reaches what the two greps cannot: every number, name and
source in the extract, and every figure description against the figure's own pixels. Runs
after every read, and on a cached extract that has no fact-check yet. Skip
it in triage mode and when the user says `— no-check`.

Haiku **finds evidence; the script and you sort it; only the reader corrects**. Neither
Haiku's verdict nor your own reading ever edits the extract: every change to it, and to any
note made from it, comes through `apply_corrections.py` from a reader's decision. That holds
even when your grep of the text layer seems to settle a flag in favour of Haiku — you drop
a flag (the extract stands) or dispute it; you never correct it yourself.

1. **Prompt.** Copy the block in [`factcheck-prompt.md`](factcheck-prompt.md) into
   `pdf_reads/<basename>/<basename>_factcheck_prompt.txt`, fill its four paths (output:
   `<extract stem>_factcheck.json` beside the extract) and its PRIORITY CLAIMS. **Priority
   claims:** when the user asked a question of the paper (a focused read, or a question
   that sent you here), name the 3–8 claims in the extract your answer will rest on, as
   the extract states them; otherwise write `none`. On 2026-10-23 Haiku checked 560 claims
   evenly and none of its corrections touched the claims the question rested on. Then
   spawn one `Agent` call with `subagent_type: general-purpose`, `model: haiku`, that
   file's contents as the prompt.
   Page images it opens stay in its context, which is discarded on return.
2. **Gate.** Run
   `python3 ~/.claude/skills/summarize-paper/check_claims.py --claims <factcheck.json> --text <basename>.txt --priority <N>`
   (N = the number of priority claims, 0 for none). It prints a `PRIORITY` line for each.
   Its logged absence claims (`<factcheck.json>.absence.json`) need no triage; glance at
   their search terms only if an absence claim matters to the user's question.
   Exit 1 (`INCOMPLETE`: an attest field false, figure claims with no page opened) or 2
   (malformed JSON) → re-run step 1 once, then report the check as not completed.
3. **Triage each `FLAG` line** — every one, none sampled. You only sort; the reader who
   wrote the extract settles what survives (Step 4E).
   - *priority claim* (`P` id), whatever its verdict or grep → **always** a dispute: the
     user's answer rests on it.
   - *Haiku verdict `contradicted` or `not_found`* → **always** a dispute, whatever the
     grep finds: a number that occurs somewhere in the paper does not show the claim is
     right (2026-10-22: 75 such flags dropped on a grep hit, 61 of them real errors). Still
     run the grep below and record its result in `triage`, as a lead for the reader.
   The two rules below drop flags only when Haiku's verdict is `supported` (flagged for
   another reason, e.g. its quote missing from the text layer):
   - *text / table flag*: `grep` the whole text layer for the bare number or name (the
     Step 4 wrapping caveat applies). Found → drop the flag. On an old two-column scan the
     text layer scrambles word order inside lines, so most flags end here; the script
     already allows for interleaved columns and dropped spaces. Absent → dispute.
   - *absence flag*: only reaches you when Haiku recorded no search terms (a supported
     absence claim with terms is logged to `<factcheck.json>.absence.json` instead, not
     flagged: across 560 claims on 2026-10-23, 0 of ~17 such flags led to a correction).
     `grep` for what is said to be missing (`replication`, `available`, `github`,
     `dataverse`, the data provider). No hit → drop. A hit → dispute, with the hit.
   - *figure flag*, whatever its verdict → dispute.
     A figure flag is **always** a dispute: it needs the page image, which only a reader
     sees. Never drop one, never settle one from Haiku's description.

   Write the disputes to `<extract stem>_disputes.json` and the dropped flags to
   `<extract stem>_dropped.json`: each a list of the flagged rows as the gate wrote them
   (`<factcheck.json>.flags.json`), each with a `triage` field saying what your grep found.
   Both files are written, an empty list if nothing went there.

**Completion criterion:** the gate printed `OK`, and every `FLAG` line is in exactly one of
the two files. Step 4E runs even with no disputes, for its closure check.

## Step 4E: Claude Code — the reader settles the disputes

The model that wrote the extract looks again at each disputed page and decides who is right;
a correction comes from it, never from Haiku or from you.

This step is never skipped and never done by the main thread in the reader's place, not
even "to save a subagent". With several papers, each paper gets its own reader; papers run
in parallel.

1. **Send the disputes back** (no disputes → write `[]` to the decisions file and go to
   step 2). Fill the block in [`disputes-prompt.md`](disputes-prompt.md):
   - *Claude reader from this run*: load `SendMessage` (ToolSearch `select:SendMessage`)
     and send the block to the reader's agent ID. It still holds every page.
   - *Otherwise* (a cached extract, or `SendMessage` fails): a fresh `Agent`,
     `subagent_type: pdf-reader`, `model: sonnet` (`opus` if the extract's stamp names Opus). It opens the disputed
     pages as images itself.
2. **Apply.** Run
   `python3 ~/.claude/skills/summarize-paper/apply_corrections.py --extract <extract> --decisions <extract stem>_decisions.json --disputes <extract stem>_disputes.json --flags <factcheck.json>.flags.json --dropped <extract stem>_dropped.json`.
   It first checks closure (every flag disputed or dropped, no figure or `contradicted` /
   `not_found` flag dropped), then applies each `haiku_right` correction whose `old` passage occurs exactly once, after
   copying the extract to `<extract stem>.pre-factcheck.md`. Exit 1 → `UNACCOUNTED` /
   `FIGURE DROPPED` / `VERDICT DROPPED`: move those flags into the disputes and send them to the reader;
   `UNANSWERED` / `NOT APPLIED`: send the reader those ids once more, then report the rest
   as open. Exit 2 → a file is malformed: fix it, or ask the reader to rewrite the
   decisions once.

**Completion criterion:** `apply_corrections.py` with `--flags` and `--dropped` exited 0, or
its remaining problems are reported as open. Only then is the extract fact-checked: no note,
summary or deck built from it is called final, and none is written to your notes, before
that. Any correction to a note already written comes from the corrected extract.

Append to the stamp line: ` · Fact-check: <model ID from Haiku's MODEL line> · <n> claims,
<k> corrected by the reader, <u> unclear`, and ` · <o> open` if problems remain.

## Step 5: Present the result

**If the read failed** (the subagent wrote no file or stopped short, or the PDF would not
open): tell the user it couldn't be
completed and offer to retry.

Otherwise, read the extract file (plain markdown — cheap) and present it, opening with who
wrote what: `Extract: <model from the stamp> · Fact-check: <Haiku model> · Summary: <your
model>`. A cached extract from before stamping has no line: say `extract model not recorded`
rather than assuming a model. Then one line on the fact-check — claims checked, corrections
the reader made (each in a few words) — and each `unclear` or open dispute with its page.
If there were priority claims, report them first and separately: each with its verdict
and, if disputed, the reader's decision.
Never report a correction you did not get from the reader's decisions. Tell
them:

> "Extract saved to `pdf_reads/<basename>/<file>`. Future requests on this paper can reuse it
> without re-reading."

If the summary is also written to a file (a note, say), the same two-model line goes
under its title.

## Step 6: Reading deck (on request)

Only when the user asks for slides to read (`— deck`, "reading deck", "make me slides of
this paper"). It runs after Step 4E, on the corrected extract; for a cached extract, run
the missing fact-check steps first. The deck must let the user follow the paper **without
having read it**; the standard, the identification ladder and the writer's prompt are in
[`reading-deck.md`](reading-deck.md). Quality outranks cost here.

1. **Write.** Fill the writer prompt at the end of `reading-deck.md` and spawn one `Agent`
   with `subagent_type: general-purpose`, `model: opus`. Output:
   `pdf_reads/<basename>/<basename>_deck.html`, unless the project's `CLAUDE.md` names
   another place for decks. The writer looks up in the text layer and the PDF only what
   the extract lacks; any page images stay in its context. Keep its agent ID.
2. **Gate.** Run
   `python3 ~/.claude/skills/summarize-paper/check_deck.py --deck <deck> --extract <extract> --text <basename>.txt`.
   A `FAIL` line → `SendMessage` the lines to the writer once; still failing → report them.
3. **Look at it.** Serve the folder (`python3 -m http.server <port>` in the background),
   open the deck in the browser pane, and run this probe. It lists every element that is
   clipped or runs off its slide, as the reader first sees it (More boxes closed):
   ```js
   [...document.querySelectorAll('.slide')].flatMap((s, i) => {
     if (s.classList.contains('detail')) return [];
     const was = s.classList.contains('on'); s.classList.add('on');
     const bottom = s.getBoundingClientRect().bottom, out = [];
     s.querySelectorAll('.body, .body *').forEach(e => {
       const st = getComputedStyle(e), r = e.getBoundingClientRect();
       if (/hidden|clip/.test(st.overflow + st.overflowY) && e.scrollHeight > e.clientHeight + 2)
         out.push((i + 1) + ': clipped ' + (e.className || e.tagName));
       else if (r.height && r.bottom > bottom + 1 && !e.closest('details:not([open])'))
         out.push((i + 1) + ': off-slide ' + (e.className || e.tagName));
     });
     if (!was) s.classList.remove('on');
     return [...new Set(out)];
   })
   ```
   Then take a screenshot of the "paper in one picture" slide, every Identification slide
   and every Results slide, and read them as the cold reader: is each rung clear from the
   slides before it, is every headline number one a reader can feel, does the main element
   fill the slide? Send everything you find to the writer in one message, naming slide and
   problem; repeat once after its revision.

**Completion criterion:** the checker exits 0, the probe returns `[]`, and every
Identification rung reads clearly on its own. Hand the deck over as a link, with the
checker's WARN lines if any remain.

## Triage mode

To quickly decide whether a paper is relevant, read **only the first few pages** (abstract +
introduction — pages 1–4) and report relevance. That is the same Sonnet subagent as
Step 4A (Opus if the user asked for it) with a one-line spec ("is this paper about X? report the question, setting and data,
and whether it is relevant") and the reader told to read only pages 1–4. No `_text.md` written, no prompt file — inline the short
prompt — and no fact-check.

## Quick Reference

| Step | Action |
|------|--------|
| **Acquire** | Local path used in place; title/DOI/citation key → Zotero lookup; not in Zotero → stop, ask user to add it |
| **Spec** | No focus → default 8 dimensions → `<basename>_text.md`. Focus given → user's target list → `<basename>__<focus-slug>.md` |
| **Check** | Output → project-local `pdf_reads/<basename>/`; reuse existing extract (matching the current mode) if present |
| **Anchor** | Main thread extracts the whole text layer → `<basename>.txt` (grounding anchor; no image tokens) |
| **Read** | ONE reader takes the whole PDF + text anchor; grounds in the text, describes figures visually but never infers numbers from them, forbids prior knowledge. A Sonnet subagent (Opus on request) reads in 20-page ranges and writes the file (page images stay in the subagent) |
| **Fact-check** | A Haiku subagent quotes the text layer for each claim and opens figure pages; `check_claims.py` gates the quotes; main thread greps every flag (figure flags and `contradicted` / `not_found` verdicts always go on); surviving disputes go back to the reader (fresh Sonnet if it is gone), who corrects the extract via `apply_corrections.py`, which also refuses a flag that vanished. The main thread never corrects. `— no-check` skips it |
| **Deck** | On request (`— deck`): an Opus subagent builds a reading deck from the corrected extract, looking up in the paper only what it lacks, to the `reading-deck.md` standard (identification ladder, cold-reader rules); `check_deck.py` gates it, the main thread checks overflow and reads the identification slides |
| **Persist** | Extract written to `pdf_reads/<basename>/<basename>_text.md` (or the focused file) |
| **Present** | Main thread reads the markdown extract and reports |
