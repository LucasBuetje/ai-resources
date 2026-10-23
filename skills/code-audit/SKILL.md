---
name: code-audit
origin: adapted from https://github.com/aspi6246/Claude-Code-Skills-for-Academics
description: Correctness diagnostic for an existing empirical research script — audits data integrity, econometric specification, and reproducibility; every 🔴/🟡 candidate is verified by execution before it is reported. Works on any committed file, not just the current diff. Use on explicit request — "code-audit <path>", "audit this analysis", "is this regression specified right".
allowed-tools: Read, Grep, Write, Agent, Bash(grep*), Bash(ls*), Bash(find*), Bash(file*), Bash(wc*), Bash(git*), Bash(Rscript*), Bash(python*), Bash(python3*), Bash(stata*), Bash(source*)
argument-hint: '[path/to/file | path/to/directory]'
user-invocable: true
---

# `/code-audit`: correctness diagnostic for existing empirical code

Point this at a script or module that already exists. It reads the code against the
**empirical-correctness checklist** and reports what may be *wrong* — data-integrity slips,
mis-specified econometrics, reproducibility gaps — as a severity-labelled findings list. It is a
**diagnostic: it reports, it does not fix.** The audited file is never modified.

**Static reading only produces suspects, not findings.** Before any 🔴/🟡 item reaches the report it
must be verified by execution — either a synthetic test case with a known true outcome, or the actual
script — per Step 3. A suspicion that doesn't survive execution doesn't get reported as a finding.

---

## Process

### Step 1 — Resolve the target & detect its kind

- Use the path given as an argument. Else use the file just discussed. Else ask for the path — one
  question. A directory audits each code file under it.
- Detect the language(s) and whether it is analysis / research code (R, Python/pandas/numpy/
  statsmodels, Stata, Julia). The checklist's econometrics and data-integrity sections apply to
  analysis code; for pure utility code, lean on the reproducibility section and general correctness.

### Step 2 — Static review against the shared checklist (read-only)

Read the code without executing it. Work through **all three sections** of
`references/empirical-correctness-checklist.md`:

1. **Data integrity** — duplicates, missing-value handling, merge validation, variable
   construction, filters, selection.
2. **Econometrics** — identification, estimating equation, standard errors / clustering, fixed
   effects, bad controls, DiD (parallel trends, staggered-timing estimator), IV (first stage, F),
   RCT/RD balance, winsorisation, magnitude plausibility.
3. **Reproducibility** — seeds, relative paths, dependency versions, execution order, determinism.

For each concern, record the **file, line(s), what's wrong, and why it matters** (the mechanism —
"treatment effects are biased because…", not just "this is wrong").

**Fresh eyes.** Spawn one review subagent (inheriting the session model —
the Subagent Model Default; do not pin a cheaper one — correctness calls are high-stakes). It gets
the code and the checklist.

Be calibrated. If a section is clean, say so — do not manufacture findings to fill a quota (no false
positives for thoroughness).

This step produces **candidates**, not findings. 🔴 Critical and 🟡 Warning candidates proceed to
Step 3 for verification before they may appear in the report. 🟢 Note candidates (hygiene/style —
unset seed, absolute paths, naming) are not executable claims; they skip Step 3 and go straight to
the report as static observations.

### Step 3 — Verify every 🔴/🟡 candidate before it's reported

No 🔴 or 🟡 candidate reaches the report unverified-and-unlabeled. Verify each one by execution, via
whichever path fits — try (a) first, fall back to (b):

**(a) Synthetic test with a known true outcome — default, runs automatically, no approval needed.**
Construct a minimal synthetic/toy case that isolates the specific mechanism the candidate is about
(a handful of rows of fabricated data), where the *correct* answer is known **by construction** — not
by re-reading the audited code and trusting your own reconstruction of what it should do (Verify
Against Ground Truth rule). Source or import the exact function/block directly from the audited file
into the check script — never re-type or paraphrase the code by hand — against that case, and compare actual output
to the known-true expectation. Because the data is fabricated, this carries no privacy or approval
concern and runs without asking.

Examples: a 6-row synthetic panel with two duplicate unit-period rows built in, to check whether the
merge really does inflate N by exactly the duplicated count; a synthetic DGP with a known treatment
effect, to check the estimating equation recovers it; a frame with a known number of true NAs, to
check whether `na.omit`/`dropna` silently removes more rows than that.

**(b) Run the actual script — explicit approval only.** Use this when the concern can't be isolated
synthetically (it depends on properties of the real data — actual merge cardinality, actual
coefficient magnitude, an actual missingness pattern). Do **not** run the real script or real data
without the user explicitly saying so ("go ahead and run it", "you can execute", "test it").
Subject to the Raw Data rule: report aggregates only. If data is restricted or absent, fall through
to "unverifiable" below.

When running: execute within the project venv; run on a small sample or synthetic subset first; check
what static review could only suspect — output dimensions, coefficient magnitude, merge row counts,
convergence/estimation warnings. Write separate check scripts — do not modify the audited code.

**Verification Is Code, either path:** save every check script as a named, durable file under the
project's test location (e.g. `tests/`, `code/test/`) — e.g. `audit_verify_<basename>_<n>.{R,py}` —
and name its path in the report. No throwaway one-liners, no inline `Rscript -e` / `python -c`.

**Resolve each candidate to one of three outcomes:**

- **Confirmed** — execution reproduces the mechanism → keep it, tagged ✅ *Verified* with the script
  path.
- **Refuted** — execution contradicts the suspicion → drop it. It does not appear in the report. A
  static-only suspicion that execution disproves is not a finding.
- **Unverifiable** — no synthetic case can isolate it, and the actual-script path is unavailable
  (restricted/absent data, no runtime, or the user declines to approve execution) → keep it, tagged
  ⚠️ *Unverified*, with a one-line reason why it couldn't be tested.

### Step 4 — Report

Present findings as a structured report, most-severe first, each anchored to `file:line`. Every
🔴/🟡 line carries its Step 3 outcome tag (✅ *Verified* + script path, or ⚠️ *Unverified* + reason); 🟢
lines carry no tag, since they were never put through execution:

- 🔴 **Critical** — results may be wrong; must fix before interpreting output. (Wrong clustering,
  merge inflating observations, post-treatment controls, missing fixed effects, `na.omit` silently
  dropping the sample.)
- 🟡 **Warning** — a potential issue worth investigating; may or may not affect conclusions. (No
  duplicate check, missing parallel-trends test, unjustified winsorisation cutoff.)
- 🟢 **Note** — won't change results but improves correctness hygiene or reproducibility. (Absolute
  paths, unset seed, undocumented sample restriction.)

End with a **Recommendations** section: concrete, actionable fixes ordered by severity, each
referencing the specific line(s). If the code is clean, say so plainly.

Log what was audited and headline findings in `current.md` per the Progress Log rule.

---

## Scope discipline

- ✅ **Report findings only**: Audit existing files for correctness problems ranked by severity. Never modify the audited code.
- ✅ **Execution-verified claims**: Ensure every 🔴/🟡 candidate carries its outcome tag (`✅ Verified` + script path, or `⚠️ Unverified` + reason). Drop refuted candidates entirely.
- ✅ **Nuanced evaluation**: Name multiple plausible readings when a concern is ambiguous rather than asserting one.
- ℹ️ **Tool Boundaries**: For whole-project audits with cross-language replication, use `referee2`.
