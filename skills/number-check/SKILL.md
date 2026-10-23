---
name: number-check
origin: self
description: "Trace every number quoted in prose — paper, deck, note, referee reply — back to the artifact that produced it and report drift. Use after re-running a pipeline the prose quotes, or before a draft goes to a reader. Numbers the project computed, not figures cited from papers."
allowed-tools: Read, Write, Bash(grep*), Bash(ls*), Bash(find*), Bash(wc*), Bash(stat*), Bash(Rscript*), Bash(python3*), Bash(stata*), Agent, Edit
argument-hint: '[path/to/draft.tex | path/to/deck.tex | path/to/note.md]'
---

# number-check

Prose quotes numbers. Pipelines rewrite them. Nothing links the two, so a rebuilt panel leaves
a sentence stating a figure no artifact produces any more — **drift**, invisible until a referee
finds it.

This skill re-derives the link every run rather than storing a mapping, so there is no registry
to rot. The trace script it writes is not a registry: it re-runs.

## The three states

Every number lands in exactly one:

- **matches** — an artifact reproduces it at the precision the prose states.
- **drifted** — the artifact exists and yields a different value.
- **unsourced** — no artifact reproduces it. A legitimate finding, and the one that matters most:
  it is where invented and hand-typed numbers live.

## Steps

**1. Scope.** Read the target file. Read the project's `CLAUDE.md` for reporting conventions
before reading any artifact — which aggregate is the headline, which units, which sample. A number
checked against the wrong convention is a false alarm, and a false all-clear.

Rank rendered prose above source comments, and label which is which in the report. A drifted
number in a comment reaches no reader, but it is what the author reads while drafting: a stale
working note hands the next revision a wrong number to write down.

**2. Inventory.** Extract every numeral making an empirical claim: estimates, standard errors,
interval bounds, p-values, counts, shares, sample sizes, ages, years of data collection, durations.
Exclude only cross-references (section, equation, table, figure numbers), citation years, page
numbers, grant and funder numbers, version numbers, and numerals inside file paths.

**Resolve indirection first.** A number the prose quotes need not be a numeral in the target file:
`\input{tables/main.tex}`, `\include`, and macro definitions (`\newcommand{\est}{0.117}`) put it
elsewhere. Expand those before inventorying — otherwise the completion criterion below passes a
draft whose numbers were never checked. A number that arrives from a compiled artifact is sound
only if that artifact is not stale (see step 3).

Completion criterion: every numeral in the file and in its resolved includes appears in the
inventory or in the excluded list. None is skipped for being obvious.

**3. Trace.** For each number, locate the artifact and read the value.

**Read, don't re-run — by default.** Reading a saved value out of a `.tex` table, `.csv`, `.rds`
or log is a proofreading-cost operation; re-running the script that produced it can cost the whole
pipeline. So:

- Read the saved output. Check it is **current**: the artifact's mtime is newer than the script
  and the input data that write it (`stat`, or the project's build order). A current artifact is
  the authority.
- **Stale or missing → re-run** the script that produces it, and only that script.
- Report per row which of the two happened. A value read from a stale artifact is not a match.

Each row carries: the quoted value, the artifact path, the exact slot or column read, the value
found, `read`/`re-ran`, and the state.

**Never infer an artifact.** A number whose source cannot be located is **unsourced**, and saying
so is the finding. A plausible-looking source that was guessed turns the check into
self-confirmation.

**How to run it.** In Claude Code, fan out **one Sonnet subagent per section** when the file runs
past a few hundred lines — one per section, never several; on a short file, run the trace inline. Either way the trace runs code to read artifacts and never reads raw data into
its own context.

**Write the trace as a script.** The recomputation is the deliverable, not the chat table: put it
in the project's test location as `code/test/number_check_<target>.R` (or `.py`, matching the
project), one runnable file that reads the artifacts and prints quoted-vs-found per number, and
name that path in the report. The next run re-runs it instead of re-deriving it. Ad-hoc
`Rscript -e` one-liners are for exploring; promote them before reporting.

**4. Adjudicate.** Review every row yourself before reporting. A subagent's match is a claim, not a
result: check that the slot it read is the one the project's convention designates, and that the
value matches at the stated precision rather than after rounding differently.

**5. Report.** One table, drifted and unsourced rows first, each carrying its artifact path so the
user can audit. State the count checked and the trace script's path. Then offer to fix the drifted
numbers; apply nothing without a yes.

## Rounding and sign

Match at the precision the prose states, not at some rounder precision.

- Prose `11.7\%`, artifact `0.1172` → **matches** (11.72% states as 11.7%).
- Prose `11.7\%`, artifact `0.1181` → **drifted** (11.81% states as 11.8%), even though both
  round to 12%.

Flag a number that matches only under a different rounding rule rather than passing it.

**A sign reversal is drift.** Prose `11.7\%` against artifact `-0.1172` matches only if the prose's
own words carry the direction — *reduces by*, *a decline of*, a negatively-signed table column.
Absent that, a magnitude quoted for an oppositely-signed estimate is the finding, not a formatting
detail.

## Qualitative claims count

A number often travels with a claim about it: *rules out harm larger than*, *narrowly includes
zero*, *the only estimate whose interval excludes zero*, *the largest*. Recompute those too — they
drift on their own while the number they sit beside stays correct.
