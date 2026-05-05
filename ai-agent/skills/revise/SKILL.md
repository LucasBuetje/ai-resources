---
name: revise
description: Structure a response to referee or reviewer comments interactively, one comment at a time. Classifies each point, drafts responses, and waits for user approval before proceeding. Use when responding to referee2 reports, journal referee reports, or co-author feedback.
argument-hint: "[referee-report file path] [paper/project path (optional)]"
---

# Revise

Work through referee or reviewer comments interactively — one at a time, with your approval at every step.

**Input:** `$ARGUMENTS` — path to the report file, optionally followed by the paper or project path.

---

## Step 1: Read Inputs

1. Read the referee report from `$ARGUMENTS`
2. If a paper or project path is provided, read the relevant files (`.tex`, `.R`, `.py`) to understand what currently exists
3. If no paper path is provided, ask the user before proceeding

---

## Step 2: Present Classification Overview

Extract all distinct comments from the report. Present a numbered list with your proposed classification for each:

```
Here are the N comments I found. Proposed classifications:

1. [Short description of comment] → CLARIFICATION
2. [Short description of comment] → NEW ANALYSIS
3. [Short description of comment] → DISAGREE
4. [Short description of comment] → MINOR
...

Do these classifications look right? Adjust any before we proceed.
```

**Classification key:**

| Class | Meaning |
|---|---|
| **NEW ANALYSIS** | Requires new code, data, or results not currently in the project |
| **CLARIFICATION** | The analysis is fine; the writing or explanation needs improvement |
| **REWRITE** | A section needs structural revision, not just clarification |
| **DISAGREE** | The comment is incorrect, unfair, or based on a misreading |
| **MINOR** | Typo, formatting, small wording fix |

Wait for the user to confirm or adjust before continuing.

---

## Step 3: Work Through Comments One by One

After classifications are confirmed, go through each comment sequentially. For each one:

**Present the comment:**
```
--- Comment 2 of N [CLARIFICATION] ---

"[Exact quote from the report]"
```

**Draft a response** based on the classification (see protocols below).

**Present the draft and wait:**
```
Draft response:

[Your draft]

→ Happy with this? Type 'next' to move on, or tell me how to adjust it.
```

Do not move to the next comment until the user approves or gives feedback. If the user requests changes, revise and present again. Repeat until they are satisfied.

---

## Response Protocols by Class

**CLARIFICATION / REWRITE:**
Draft revised text addressing the concern. Reference the exact location (section, page, equation) where the change would go.

**MINOR:**
Draft the fix directly and concisely.

**NEW ANALYSIS:**
Do not attempt to draft results. Instead:
```
This requires new analysis: [describe what would be needed].
Placeholder response: "We thank the referee for this suggestion. We have [conducted / plan to conduct] [brief description]. Results are reported in [Section X / Table Y]."
Mark as TBD — fill in once the analysis is done.
```
Flag clearly and confirm the user wants to proceed before moving on.

**DISAGREE:**
Follow the diplomatic disagreement protocol:
1. Open by acknowledging the legitimate concern behind the comment
2. Provide evidence for why the critique does not apply, or where it is already addressed
3. Offer a partial concession if honest (a clarifying sentence, footnote, or caveat)
4. Never say "the referee is wrong" or "we disagree" directly

Present the draft, then add:
```
⚠ DISAGREE — please review this response carefully before it goes anywhere.
```
Wait for explicit approval.

---

## Step 4: Compile Outputs

After all comments are approved, compile:

**1. Tracking document** (`revise_tracker.md`):
```markdown
# Referee Response Tracker
**Report:** [filename]
**Date:** [YYYY-MM-DD]

## Summary
- NEW ANALYSIS: N
- CLARIFICATION: N
- REWRITE: N
- DISAGREE: N
- MINOR: N

## Action Items
[Grouped by priority, with approved responses]
```

**2. Response letter** (`revise_response_[date].md`):
```markdown
# Response to Referee Report

We thank the referee for their careful reading and constructive comments.
We have addressed each point below.

---

## Major Changes
[2–3 sentence summary of the most important revisions]

---

## Point-by-Point Response

**Comment 1:** "[Exact quote]"
**Response:** [Approved response]
**Location of change:** [Section/page/equation]

[Repeat for each comment]
```

Save both files to the project directory (or current directory if no project path given). Report the paths to the user.

---

## Principles

- **One comment at a time.** Never move forward without the user's explicit approval.
- **The response letter is your voice.** Match the user's tone throughout.
- **Never fabricate results.** NEW ANALYSIS items are always TBD.
- **Flag all DISAGREE items.** These require explicit user approval before going anywhere.
- **Every comment gets a response.** Nothing is ignored.
