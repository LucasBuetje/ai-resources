---
name: summarize-paper
origin: adapted from https://github.com/scunning1975/MixtapeTools
targets: [claude]
description: Locate (via Zotero) and deeply read/summarize an academic research paper — journal article, working paper, preprint — with ONE Claude Opus subagent that reads the WHOLE PDF in a single pass (no chunking). The subagent gets the rendered pages (images) plus the extracted text layer as a grounding anchor and returns a structured extract; page images stay inside the subagent and are discarded on return, so no image tokens reach the main thread. Auto-invoke for a whole-paper summary of a research paper; other paper reads (a targeted section or table) go through a Claude subagent per the PDF Reading rule.
allowed-tools: Bash(python*), Bash(pip*), Bash(mkdir*), Bash(ls*), Read, Write, Edit, Agent, mcp__zotero__zotero_search_items, mcp__zotero__zotero_search_by_citation_key, mcp__zotero__zotero_get_item_children, mcp__zotero__zotero_get_attachment_path
argument-hint: "[pdf-path | paper title | DOI | citation key] [— focus: what to extract]"
---

# Summarize-Paper: Locate and Deep-Read a Paper with One Opus Subagent

This skill produces a deep, structured read of an **academic research paper** — journal
articles, working papers, preprints — where **one Claude Opus subagent reads the whole
paper in a single pass**.

**One whole-paper read, not a chunk pipeline.** Earlier versions split the PDF into 4-page
chunks and ran a reader per chunk, then a consolidate pass and a verify pass. Head-to-head
testing (on Bernhard 2024, Seibold 2021, Mello 2024, Fuest 2018, Houmark 2024) showed a
**single whole-paper Opus read is more accurate and far cheaper**: it integrates
cross-section facts a per-chunk reader structurally cannot (e.g. reconciling a figure on
page 5 with a table on page 40), it describes figures from the actual pixels, and it
avoids the confabulations that fragmented chunk reads introduced — errors that previously
only a whole-paper verify pass could catch. The chunk machinery cost ~6–7× more tokens to
reach the *same* answer the verify stage (itself a whole-paper read) produced. So the read
is now exactly that: one whole-paper pass, no split, no consolidate, no separate verify.

**Reader model: always Opus.** A whole-paper read holds every page at once; use **Opus**,
with its **1M-context window** for long papers (see Step 4). Never Sonnet or Haiku for the
read itself.

**CRITICAL RULE: PDF pages are never read in the main conversation.** The main thread does
NOT open the PDF — not with `Read`, not with any image-rendering tool. The page images load
only into the *Opus subagent's* context and are discarded when it returns, so only its text
extract reaches the main thread (exactly what the PDF Reading rule permits). The main thread
only extracts the text layer (text-free, no images), launches the reader subagent, and reads
the final markdown extract.

## When This Skill Is Invoked

The user explicitly wants **Claude** to read, review, or summarize a **research paper**. The
input is either a file path to a local PDF, or a paper title, DOI, or citation key. You
cannot search for a paper you don't know exists — if invoked with no argument, ask what to
read; do not guess.

## Extraction spec: default vs focused

What gets extracted is customizable; the read mechanism is identical either way. Only the
*list of extraction targets* changes. Decide the spec once, here, before the cache check and
the read — both depend on which output file it writes.

**You — the main agent — build the extraction spec.** Interpreting the user's focus goal
into the numbered target list is a judgement call and stays in the main thread. The reader
subagent (Step 4) receives the finished target list verbatim. If the user's goal is
ambiguous, clarify it *before* dispatching.

- **Default (no focus given).** Use the standard **8 dimensions** (listed in Step 4). Output
  file: `pdf_reads/<basename>/<basename>_text.md`. This is the canonical, reusable extract.
- **Focused (the user gives a reading goal).** Translate the goal into a short numbered list
  of concrete extraction targets (typically 3–8). That list **replaces** the 8 dimensions.
  Pick a short kebab-case `<focus-slug>`; output file
  `pdf_reads/<basename>/<basename>__<focus-slug>.md`, with the extract's first line
  `> Focus: <the goal>`. A focused read **never** overwrites the default `<basename>_text.md`.
  If the user wants both, run the default first, then the focused read.

Hold the chosen spec as the `EXTRACTION SPEC` injected verbatim into the reader prompt (Step 4).

## Step 1: Acquire the PDF

**If a local file path is provided:** verify it exists; use it in place.

**If a title, DOI, or citation key is provided (no path)** — follow the Finding Papers vs Zotero Library rule,
look the paper up in Zotero:
1. `zotero_search_by_citation_key` (citation key) or `zotero_search_items` (title/DOI) to
   find the item. (BetterBibTeX keys sometimes don't resolve; if so, fall back to a short
   `zotero_search_items` on author + year or title words.)
2. `zotero_get_attachment_path` (or `zotero_get_item_children` then construct
   `~/Zotero/storage/<attachmentKey>/<filename>`) to get the `application/pdf` attachment's
   on-disk path. Verify it exists (`ls`).
3. **If the storage path does not exist (stub-only folder), try your Zotero linked-file
   location.** If you store PDFs as linked files outside Zotero's own storage (e.g. a
   synced folder), check there too. Adapt this path to your own Zotero setup.

Do **not** use `zotero_get_item_fulltext` — that returns plain text only, with no tables,
figures, or layout. This skill must read the actual rendered PDF.

**If the paper is not usable from Zotero — no item match, no `application/pdf` attachment, or
neither path exists: stop.** Do not search the web, do not download anything. Tell the user
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

**Use extract** → read it, skip to Step 5. **Re-read** → continue. A default extract does not
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
the Python venv rule). A scanned, image-only PDF yields little/no text — note that and tell
the reader (Step 4) to rely on the page images, since there is no anchor.

## Step 4: Launch the Opus reader (one subagent, whole PDF)

Launch **one** Claude subagent (`subagent_type: general-purpose`, **`model: opus`**) and hand
it the **source PDF path**, the **text-layer path** from Step 3, and the EXTRACTION SPEC. It
reads the whole paper and returns the extract as text. The main thread does not open the PDF.

**Long papers / context.** Opus's default context holds a ~70-page paper as images
comfortably (verified). For very long PDFs (≳100 pages of dense scans), launch the subagent
with the **1M-context window**. If a paper is so large even that won't hold all page images
at once, have the subagent read the text layer in full plus the figure/table pages as images
(it can identify those from the text), or read in two halves and stitch — but this is a rare
edge case; the default is one subagent, whole PDF.

Write the returned extract to the output file (`<basename>_text.md`, or the focused file with
its `> Focus:` first line). Reader prompt:

```
Read this ENTIRE academic paper and extract the targets listed below. Do it in one pass.

Whole PDF (images):  <source PDF path>
Text layer:          <pdf_reads/<basename>/<basename>.txt>   ← AUTHORITATIVE for wording/numbers

HOW TO READ:
1. Read the text-layer file first. It is the authoritative source for all wording, names,
   and numbers — quote coefficients, sample sizes, and identifiers from it verbatim.
2. Then Read the whole PDF (it loads as page images). Use the images for tables, figures,
   equations, and layout. For every FIGURE, describe what it actually SHOWS — the shape and
   slope of curves, pre-trends, magnitudes, distributions, confidence bands — not just its
   caption. The figure's visual content is information the text does not carry; do not skip
   a figure because its numbers happen to appear in the caption.
3. If the text layer is empty/near-empty (a scanned PDF), say so and rely on the images.

HARD RULES:
- Extract ONLY what THIS paper contains. Do NOT use prior knowledge of the topic, of related
  studies, or of this paper from any other source. If you would name a study, setting,
  dataset, author, or number that is not in this paper, do not.
- If the paper cites OTHER studies, report them as "the paper cites X" — attribute only what
  the page says about them.
- Be thorough and specific: exact coefficient estimates, standard errors / confidence
  intervals, sample sizes, identification details, equation references, data sources, URLs.

Your returned text IS the deliverable — do not address me, do not narrate. Output only the
extraction, starting directly with the first target heading. (For a focused read, keep the
`> Focus: <goal>` first line intact.)

EXTRACTION SPEC: <injected verbatim — see below>
```

**Failure.** If the subagent errors or returns nothing, retry once; if it still fails, STOP
and report it — never fake or thin the output.

**EXTRACTION SPEC injected into the reader.** Whichever list it is, demand concrete specifics
— data sources, variable names, equation references, sample sizes, coefficients, standard
errors — not a vague summary.

```
DEFAULT (8 dimensions) — what a researcher would need to build on or replicate the work:
1. Research question — what is asked, why it matters
2. Audience — which sub-community cares
3. Method — how the question is answered; identification strategy
4. Data — sources, unit of observation, sample size, time period; where the data came from
5. Statistical methods — econometric techniques, key specifications
6. Findings — main results, key coefficient estimates and standard errors; what the figures show
7. Contributions — what is now known that wasn't
8. Replication feasibility — public data? replication archive? data appendix? URLs?

FOCUSED — replace the 8 dimensions with the user's numbered target list; the instructions
above apply unchanged to those targets.
```

**On verification.** This is a single whole-paper read, so there is no separate verify pass.
The text-layer anchor plus the no-prior-knowledge rule are the safeguards, and a whole-paper
Opus read reliably grounds in the real pages (the confabulation failure mode came from blind
per-chunk reads, which no longer exist). If a paper is unusually high-stakes and the user
wants extra assurance, offer to re-run the read or spot-check specific claims against the
text layer — but do not do this by default.

## Step 5: Present the result

**If the subagent failed:** tell the user the read couldn't be completed and offer to retry.

Otherwise, read the extract file (plain markdown — cheap) and present it. Tell them:

> "Extract saved to `pdf_reads/<basename>/<file>`. Future requests on this paper can reuse it
> without re-reading."

## Triage mode

To quickly decide whether a paper is relevant, launch one Opus subagent on **only the first
few pages** (abstract + introduction — pass a small PDF of pages 1–4, or tell it to read only
those) reporting relevance. No `_text.md` written.

## Quick Reference

| Step | Action |
|------|--------|
| **Acquire** | Local path used in place; title/DOI/citation key → Zotero lookup; not in Zotero → stop, ask user to add it |
| **Spec** | No focus → default 8 dimensions → `<basename>_text.md`. Focus given → user's target list → `<basename>__<focus-slug>.md` |
| **Check** | Output → project-local `pdf_reads/<basename>/`; reuse existing extract (matching the current mode) if present |
| **Anchor** | Main thread extracts the whole text layer → `<basename>.txt` (grounding anchor; no image tokens) |
| **Read** | ONE Opus subagent reads the whole PDF (images) + text anchor; grounds in the text, describes figures visually, forbids prior knowledge → returns the extract |
| **Persist** | Extract written to `pdf_reads/<basename>/<basename>_text.md` (or the focused file) |
| **Present** | Main thread reads the markdown extract and reports |
