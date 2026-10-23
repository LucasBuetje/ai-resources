---
name: walkthrough
origin: self
description: Pick an AI-authored commit worth understanding, have the user explain its key hunks in their own words first, teach the gaps via explain-diff, quiz in chat, record the pass in log/understood.jsonl. Use when the user asks for "a walkthrough" or to be quizzed on an AI-authored commit or change — the user explains first. When they only want a change explained to them, use explain-diff.
argument-hint: [commit hash or subject — defaults to showing candidate commits and picking one]
---

# `/walkthrough`: understand an AI-authored commit

A quiz-backed way to actually understand a chosen AI-authored change: the user picks a
commit they deem worth the time, and a pass is only recorded once they've answered
questions on it. Not every commit needs this — it's for the ones the user chooses to run
it on. (Teach-then-quiz pattern after Scott Cunningham's `/quiz`.)

**Predict first.** The user reads the change cold and explains it in their own words
*before* any teaching. The attempt is the learning step (trying first beats being told), and
its gaps decide what the deck teaches.

**Hard rules**

- **Data source is the git trailer only.** AI-authored commits are those whose message
  contains `Co-Authored-By: Claude`.
- **Scope:** projects where the AI commits its own code. No trailered commits → say so and
  stop.
- **Grading is honest** — record the score the answers earned; a sign-off exists only on a
  pass. The answer key is written before the user answers, never adjusted after.
- The ledger `log/understood.jsonl` is machine-written and append-only, committed alongside
  the other log files.
- **No commit hashes in front of the user.** Not in the candidate table, the pick options,
  the quiz questions or answers, the grading, or the report. Name a commit by its subject
  (and date, when two subjects are close). Hashes stay internal — the `git` calls and the
  ledger. If the user asks which commit it is, give the hash then.

## Step 1 — List candidate commits

```bash
git log --grep='Co-Authored-By: Claude' --format='%H|%h|%ad|%s' --date=short
```

Read `log/understood.jsonl` (absent → empty ledger). Candidates = trailered commits with no
ledger row matching their full hash, restricted to result-bearing types: `feat`, `fix`,
`data`, `refactor` (`test`, `docs`, `chore` never appear here).

Done when the candidate list is computed and each entry has hash, date, type, subject, and
age.

## Step 2 — Present the list and pick

Show the candidates as a compact table (date, type, subject, age — no hash column), ranked `feat`/`fix`, then `data`, then `refactor`,
oldest first within a tier — this is a picking aid, not a queue to clear.

If the user passed a hash or named a commit, that is the target. Otherwise ask (Claude Code:
`AskUserQuestion`; elsewhere plain chat): recommend the top-ranked commit, offer the next
two, and always offer "just show the list — no session today".

## Step 3 — Write the key, pick the hunks

Do `explain-diff`'s Step 2 legwork on the commit, then, before showing the user anything:

- **The key:** 3–5 key points, one sentence each — what the change does, why, and what it
  protects or breaks. A point restating the commit subject doesn't count; the user has
  already read the subject. Keep the key internal.
- **The hunks:** the 2–4 hunks (contiguous blocks of changed lines) that carry those
  points. Boilerplate, renames, and the repeated instances of one pattern stay out.

Done when the key is written down and every key point is visible in at least one chosen
hunk.

## Step 4 — The user explains it cold

Show the chosen hunks in chat: per hunk a `file:line` header, one line on what that file is
for in the project (its role, never what the change does to it), and the hunk as a `diff`
code block. No commit message body, no explanation of the change.

Then ask, in plain chat, and end the turn:

> In your own words: what does this change do, and why? (If you like: what would go wrong
> if it were wrong?)

Any angle the user takes counts — behaviour, motivation, a number it moves, a risk. "No
idea" is a valid answer; it grades as all-missed.

## Step 5 — Grade the attempt

Mark each key point **hit**, **missed**, or **misread** (the answer states something the
code doesn't do). Show the user a short table: key point as a topic (not the answer),
status, and for a misread their own phrase quoted. Leave the explanations to the deck.

Prediction score = hits / key points.

Done when every key point has a status.

## Step 6 — Teach the gaps

**All points hit** → skip the deck, say so, go to Step 7.

Otherwise invoke **`explain-diff`** on the commit with the **gap brief**: every key point with
its status, and the user's quoted phrase for each misread. Its "Invoked by `/walkthrough`"
section says how the deck uses it. Hand over the deck link, then wait: *"Tell me when
you've read it."* The quiz starts on that signal.

## Step 7 — Quiz, one question at a time

One question per key point (so 3–5), covering the **whole key**, hits included — a quiz
limited to the gaps only re-tests what the deck just taught. Author the questions fresh
from your own reading of the diff, under explain-diff's Step 5 design rules (behaviour over
recall, distractors encoding real misunderstandings, levelled options), plus two rules of
this skill's own:

- At least one question takes the form *"if X in this change were wrong, what would happen
  to the results?"*
- **Pre-commit each question's correct-answer position before asking it** — explain-diff's
  shuffle rule assumes a finished set to inspect at once, which this one-per-call format
  never has. Draw the position at random (not a fixed rotation) before drafting the options,
  so authoring order can't leak the answer.

A misread point's question gets the user's own misreading as one distractor.

One question per `AskUserQuestion` call (plain chat elsewhere) — put the answer text itself
in each option's `label`, not a letter ("A", "B", …) or "Option 1"; the tool already numbers
choices for selection, so a letter prefix only adds visual clutter. After each answer, say
whether it was right and why in a short paragraph; on a miss, add one follow-up probe at
the misconception the chosen distractor encodes — it aids learning and leaves the score
untouched.

Done when every question is asked, answered, and graded.

## Step 8 — Grade and sign off

Pass: all correct at 3 questions; at most one miss at 4 or 5.

**On pass**, append one row to `log/understood.jsonl` (`page` is `null` when the deck was
skipped):

```json
{"commit": "<full hash>", "short": "<short hash>", "subject": "<commit subject>", "quizzed": "YYYY-MM-DD", "predicted": "2/4", "score": "4/4", "page": "explanations/<file>.html"}
```

**On fail:** no row. Name the mental model that was weak, leave the commit as a candidate,
and offer a later re-run with freshly authored questions.

## Step 9 — Report

Close with one line: prediction score, quiz score, pass/fail.

---

## What the two scores certify

The **prediction score** measures how well the user reads AI code cold — the skill this
loop trains; across ledger rows it should rise. A **pass** certifies the user understands
the change *as the key describes it*. Key, deck and quiz come from the same reading of the
diff, so neither score says whether the code is correct — that is `/code-audit`'s job:
understood ≠ verified.
