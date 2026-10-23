# Haiku fact-check prompt (Step 4D)

Copy the block below into `pdf_reads/<basename>/<basename>_factcheck_prompt.txt`, fill the
four paths and the PRIORITY CLAIMS list (`none` when there is no question to rank by), and pass the file's contents as the `Agent` prompt (`model: haiku`). Written to
the `haiku-prompting` skill's rules: inputs from disk, JSON out via `json.dumps`, a one-line
reply, an honest attest block, and the keep-working paragraph for a long prompt.

```
Fact-check a summary of an academic paper against the paper itself. You check; you do not
rewrite the summary.

Extract (the summary to check): <absolute path to the extract .md>
Text layer of the paper:         <absolute path to <basename>.txt>
Paper PDF:                       <absolute source PDF path>
Output JSON:                     <absolute path to <extract stem>_factcheck.json>

PRIORITY CLAIMS (the claims the user's question rests on; check these FIRST):
<P1: claim as the extract states it, with its section>
<P2: …>   — or the single word: none

TOOLS: Read (the three files above), and Bash only to run python3 for writing the output
JSON. No search, no web, no edits to any existing file.

STEPS
0. If PRIORITY CLAIMS are listed, check each of them first, by steps 4-5 below, and list
   each in the output with its own id ("P1", "P2", …) and "priority": true. Every one must
   appear, even if you cannot settle it (then verdict "not_found" and say why in `note`).
1. Read the extract in full.
2. Read the text layer in full. It is the paper's own wording.
3. List every CHECKABLE claim in the extract (priority claims keep their P ids; give the
   rest ids c1, c2, …): each number (coefficient, standard error,
   sample size, share, year range), each named data source, institution, country or
   program, each stated access route or replication archive, each "not reported" / "not
   shown" claim, and each description of what a figure or table shows. Skip pure framing
   ("the paper contributes to…").
   A claim that something is ABSENT (no code archive, no access route stated, a result
   "not reported") gets source "absence" and quote null: you cannot quote a gap, so write
   in `note` the search terms you looked for in the text layer, e.g. "searched: replication,
   github, dataverse, available on request". If you find the thing the extract calls
   absent, verdict "contradicted", and put the passage in `quote`.
4. For a claim the text layer can settle (source "text" or "table"): find the passage that
   supports it and copy it into `quote` WORD FOR WORD, 5 to 40 words, exactly as the text
   layer has it. If no passage supports it, set quote to null and verdict "not_found". If a
   passage says something different, quote that passage and set verdict "contradicted".
5. For a claim about what a figure shows (source "figure"): open that page of the PDF with
   Read's `pages` parameter (only the pages you need, at most 20 per call) and look at the
   figure itself. Verdict "supported" if the picture matches the description, "contradicted"
   if it does not (say what you see in `note`). A number the extract gives for a figure
   must be printed on the figure or in its caption or the text; if you only see it on an
   axis, verdict "contradicted", note "read off an axis". Put a caption quote in `quote`
   if one helps, else null.
6. Write the output JSON with python3 (json.dumps, ensure_ascii=False), one write:
   {"attest": {"read_extract_fully": true|false,
               "read_text_layer_fully": true|false,
               "pdf_pages_opened": [page numbers you opened],
               "claims_skipped": <number of checkable claims you did not check>},
    "claims": [{"id": "c1", "section": "<extract heading>", "claim": "<the claim, short>",
                "source": "text"|"table"|"figure"|"absence", "page": <PDF page as Read's `pages` counts it, 1 = first page of the file; not the journal's printed page number; or null>,
                "quote": "<verbatim>"|null,
                "verdict": "supported"|"contradicted"|"not_found",
                "note": "<one short sentence, or empty>",
                "priority": true only on P claims, else omit}]}
   Report the attest fields truthfully: an honest false is useful, a false true is not.

Keep working until everything the user asked for is done, and only stop to ask when you
can't go on without the user or before a risky step. When the work is done and checked,
stop and report. Don't add features, docs or refactors that weren't asked for; mention them
at the end instead.

Your final reply is ONE line only:
MODEL <your model ID as your system prompt states it> · CLAIMS <n> · WROTE <output path>
```
