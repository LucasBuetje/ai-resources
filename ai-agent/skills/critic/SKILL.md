---
name: critic
description: >
  All-purpose reviewer. Looks up domain-specific evaluation criteria via web
  research, then delivers a critical-but-good-faith assessment of an artifact:
  scored rubric plus a short prose review. Does not edit. Use when the user
  asks for a review, critique, or assessment of writing, code, a presentation,
  documentation, or any other artifact.
argument-hint: "[file path to review] [optional: review focus or audience]"
---

# Critic: Domain-Grounded Review

**Goal:** Give the user a critical, fair, well-grounded assessment of an artifact. Look up what "good" looks like in the relevant domain, evaluate the artifact against those criteria, and report honestly — neither rubber-stamping nor nitpicking.

**Input:** `$ARGUMENTS` — path to the artifact, optionally followed by review focus (e.g., "as if for a top-5 econ journal", "from a beginner's perspective", "focus on argument flow").

**What this skill is NOT:**
- Not a rewrite tool. Never edit the artifact.
- Not a worker-critic loop. One pass, one report.
- Not a hostile teardown. The stance is "good-faith colleague who has read the literature."

---

## The Stance

Before starting, internalise the posture this skill requires:

- **Critical**: Surface real weaknesses. If a 4-star reviewer would flag it, you flag it. Do not hedge to avoid hurting feelings.
- **Good-faith**: Assume the author is competent and trying to do something specific. Look for the strongest version of what they wrote before objecting.
- **Grounded**: Every objection cites either the rubric or a domain convention. "I think it's weak" is not a valid objection.
- **Proportional**: Distinguish blockers from polish. A 2/5 on Clarity matters more than a 4/5 on Polish.
- **Honest about strengths**: A review that only finds problems is suspect. Note what works, briefly.

---

## Step 1: Read & Classify the Artifact

1. Read the artifact from `$ARGUMENTS`.
2. Detect the domain from extension + content:

| Signal | Domain |
|--------|--------|
| `.tex` with `\begin{frame}` | Beamer presentation |
| `.tex` / `.md` with substantial prose | Academic / long-form writing |
| `.py`, `.R`, `.js`, `.ts`, `.jl`, etc. | Code (specify language) |
| `.md` with YAML frontmatter or instructional structure | Documentation / skill / prompt |
| Cover letter, CV, application | Job-search writing |
| Ambiguous | Ask the user which domain to use |

3. Present:

```
Artifact: [path]
Detected domain: [domain]
Review focus: [user's instructions, or "general assessment" if none]

Confirm domain and focus, or override.
```

4. **Wait for confirmation.**

**Success criterion:** A confirmed domain label and a stated review focus.

---

## Step 2: Research the Evaluation Criteria

**Goal:** Build a Critic Rubric grounded in how the domain actually evaluates work, not generic intuition.

Launch **one Agent call** (Explore subagent, "medium" thoroughness) with this prompt — substituting `[domain]` and `[focus]`:

> You are preparing to evaluate a **[domain]** artifact. The reviewer's focus is: **[focus]**.
>
> Search the web for **how this domain evaluates quality and what its common failure modes are**. Use 2-3 targeted queries — prefer queries about evaluation, weaknesses, review checklists, and rejection reasons over generic "best practices" queries. Examples:
> - "common weaknesses in [domain]"
> - "[domain] review checklist"
> - "why [domain] gets rejected"
> - "[domain] evaluation criteria"
>
> For the 2-3 most promising results, fetch the page and extract concrete evaluation dimensions.
>
> Compile a **Critic Rubric**: a numbered list of **5-8 evaluation dimensions**. For each dimension provide:
> - **Name** — short label
> - **What 5/5 looks like** — one sentence
> - **What 1/5 looks like** — one sentence
> - **Source** — which page/convention it comes from (one short citation)
>
> Return ONLY the rubric — no preamble, no review of the artifact. Do NOT read the artifact itself.

Keep the rubric in context and proceed directly to Step 3. Do not present it for approval — the review in Step 4 will show the rubric alongside the scores.

**Success criterion:** A rubric of 5-8 dimensions with clear anchors and sources is held in context.

---

## Step 3: Review Against the Rubric

**Hard rule:** Do not edit the artifact. Do not produce a "fixed" version. Read, score, explain.

1. Re-read the artifact in full.
2. For **each dimension** in the confirmed rubric:
   - Assign a score (1-5)
   - Write a one-line **finding** with a specific location (line number, section name, function name, slide number)
   - If score ≤ 3, write a concrete **objection** explaining what is wrong and what a 4+ would look like
   - If score = 5, briefly note what makes it strong (one phrase) — do not invent praise

3. Identify **strengths** (2-4 things that genuinely work) and **blockers** (issues serious enough that the artifact is not ready until fixed).

---

## Step 4: Deliver the Assessment

Output exactly this structure:

```
## Critic Review — [artifact path]

**Domain:** [domain]  |  **Focus:** [focus]  |  **Overall: [SHIP / MINOR REVISIONS / MAJOR REVISIONS / NOT READY]**

### Assessment
[2-4 short paragraphs. Honest, good-faith reading of what the artifact is trying to do, where it succeeds, where it falls short, and what the most useful next move would be. No bullet points here — this is the human-voiced summary, and it is the most important part of the report. Lead with it.]

### Strengths
1. [What works, with location]
2. ...

### Blockers
*(Empty if none. List only issues that must be fixed before this artifact is ready.)*
1. **[Dimension] (score)** — [specific problem at location]. A 4+ would [concrete fix shape, not the fix itself].

### Scorecard

| # | Dimension | Score | Finding (location) |
|---|-----------|-------|--------------------|
| 1 | Clarity   | 4/5   | Section 2 reads cleanly; one ambiguity at L47. |
| 2 | Structure | 2/5   | Method jumps to results without bridge (L60–72). |
| ... |

### Objections (score ≤ 3)
1. **[Dimension] (score)** — [what is wrong, where, what 4+ looks like].
2. ...
```

**Verdict bands:**
- **SHIP** — all dimensions ≥ 4, no blockers
- **MINOR REVISIONS** — one or two dimensions at 3, no blockers
- **MAJOR REVISIONS** — multiple dimensions ≤ 3, or one blocker
- **NOT READY** — multiple blockers or any dimension at 1

---

## Step 5: Hand Off

After delivering the assessment, ask:

> Want me to draft fixes for specific objections, or leave it as a review only?

Do not start editing unprompted. The skill ends here.

---

## Step 6: Log

Append to `log/current.md`:

```
- Reviewed `[artifact path]` (domain: [domain]). Verdict: [band]. [1-line summary of biggest finding].
```
