# Dispute prompt for the reader (Step 4E)

The block below goes back to the reader that wrote the extract: as a `SendMessage` to the
Claude reader subagent, or as the prompt of a fresh Claude subagent when that one is gone.
Fill the paths and paste the disputes file's contents where marked.

For a **fresh Claude** reader, put this in front of the block:

```
Use only two tools: Read (on the three files below) and Write (for the output file named at
the end). No Bash, no search, no web. Read the text layer in full, then only the PDF pages
the disputes name.
```

```
A fact-checker disagrees with some claims in the extract you wrote about this paper. Settle
each dispute from the paper itself.

Extract:     <absolute path to the extract .md>
Text layer:  <absolute path to <basename>.txt>
Whole PDF:   <absolute source PDF path>

For each dispute below:
1. Open the named page again (Read with `pages`, or the text layer for a text claim) and
   look at it as if for the first time. Your extract is not evidence; the page is.
2. Write down what the page actually prints or shows, quoting printed values word for word.
3. Then decide:
   - "haiku_right": the extract is wrong. Give `old`, an exact passage copied from the
     extract (long enough to occur only once), and `new`, the corrected passage in the
     paper's own terms. Fix every sentence the error reaches inside that passage, e.g. a
     result attributed to the wrong group.
   - "extract_right": the extract stands; `evidence` says why the fact-checker misread.
   - "unclear": the page does not settle it; say what is missing.
   The fact-checker is a smaller model and is often wrong; you are also capable of having
   been wrong the first time. Decide on the page alone.

DISPUTES:
<contents of <extract stem>_disputes.json>

Write your answer as a JSON list with the Write tool to <absolute path to
<extract stem>_decisions.json>, one object per dispute:
[{"id": "<dispute id>", "decision": "haiku_right"|"extract_right"|"unclear",
  "evidence": "<what the page shows, printed values quoted>",
  "old": "<exact extract passage, haiku_right only>", "new": "<replacement, haiku_right only>"}]
Your final reply to me is ONE line: `DECIDED <n> · WROTE <path>`.
```
