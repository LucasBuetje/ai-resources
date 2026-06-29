---
name: council
description: Convene a multi-model "council" to answer a hard question — four different model families answer in parallel, anonymously peer-rank each other, and a Claude Opus chairman synthesizes the final answer. Adaptation of karpathy/llm-council for local CLIs (agy, codex, vibe) plus Claude subagents. Can judge attached material: point it at project files (R scripts, .tex/.md drafts, data dictionaries) or paste content inline, and every member sees it (PDFs are extracted to text by a subagent first). Use when the user wants cross-model consensus, a second/third opinion, or maximum-confidence judgment on open-ended, high-stakes, or contested questions — invoke on "/council", "ask the council", "convene the council", "council on …". Not for quick factual lookups (the fan-out costs ~9 model calls).
targets: [claude]
origin: adapted from https://github.com/karpathy/llm-council
---

# Council

A "council of LLMs": one question goes to several different model families; each
answers independently; each then ranks the others' answers **anonymously**; a
chairman model reads everything and writes the final synthesis. The anonymity in
stage 2 is the whole point — it strips self-preference bias, so a model can't
just vote for its own style.

This is a Claude Code only skill: it orchestrates Bash CLIs (`agy`, `codex`,
`vibe`) for the non-Claude members and native Claude subagents for the Claude
roles.

> **Adapt this to your own setup.** `agy`, `codex`, and `vibe` are *my* local
> command-line aliases for Gemini, GPT, and Mistral CLIs. They will not exist on
> your machine. To reuse this skill, install whatever model CLIs you have access
> to and edit `ask_member.sh` / `dispatch.sh` and the table below to match their
> command names, auth, and flags. The structure (parallel answers → anonymous
> peer-ranking → chairman synthesis) is the reusable part; the exact binaries are not.

## The council (4 members + chairman)

Four families, no overlap except Anthropic (one member + the chairman).

| # | Member | How it's called | Family |
|---|---|---|---|
| 1 | Gemini 3.1 Pro | Bash: `agy` | Google |
| 2 | GPT-5.5 | Bash: `codex` (ChatGPT sign-in, reasoning high) | OpenAI |
| 3 | Mistral Medium 3.5 | Bash: `vibe` (Mistral auth, thinking high) | Mistral |
| 4 | Claude Sonnet 4.6 | native subagent (`model: sonnet`) | Anthropic |
| — | **Chairman:** Claude Opus 4.8 | native subagent (`model: opus`) | Anthropic |

Exact backend strings (verified working):

- Gemini → `bash <skilldir>/ask_member.sh agy "Gemini 3.1 Pro (High)" <promptfile>`
- GPT-5.5 → `bash <skilldir>/ask_member.sh codex "gpt-5.5" <promptfile>`
- Mistral → `bash <skilldir>/ask_member.sh vibe "mistral-medium-3.5" <promptfile>`

`<skilldir>` is this skill's directory (`~/.claude/skills/council`). The helper
prepends the "answer directly" directive for agy; for `codex` it captures only
the final message via `-o` (skipping the banner), and `vibe` already prints clean
text. The `vibe` model is set in `~/.vibe/config.toml` (`active_model`), not via a
CLI flag, so the model string above is documentation only. The `agy` binary lives
in `/opt/homebrew/bin`; `codex`/`vibe` in `~/.local/bin`.

## Invocation

- `/council <question>` — run the council on `<question>`.
- `/council` with no question — ask the user for the question first, then run.
- **With context:** the user may point the council at material to judge — files
  in the project, or content pasted inline. Two equivalent ways:
  - `/council [context: path/a.R, notes/b.md] <question>`
  - just name the paths in the question, or paste the content inline.
  Whatever is referenced gets assembled into a context packet (Stage 0) that every
  member sees. This is the skill's main lever: the council can only judge what it
  is given.

Auto-invoke is **off**: the fan-out is ~9 model calls, so only run when the user
clearly asks for a council / multi-model opinion.

## Procedure

Set up a scratch dir once: `mkdir -p /tmp/council`.

### Stage 0 — Readiness check, then assemble context

**Part A — readiness check (always, before any dispatch).** The fan-out costs
~9 model calls, so first pause and reason about whether the council has what it
needs. Given the question, ask: *what material would materially change the
quality of the answer, and is it actually here?* Think about the obvious
candidates for this kind of question — the artifact under discussion (script,
draft, deck outline), the goal/spec/constraints, reference sources, a data
dictionary (never raw data, Rule #3), relevant prior work.

- If something important is plausibly **missing or would clearly help**, tell the
  user in one short list what you'd add and why, name where it likely lives (a
  project file? a Zotero paper? paste inline?), and **wait** for them to attach
  it, point you at it, or say "go without it."
- If the question is **self-contained**, skip the prompt — say in one line what
  context (if any) you'll use, and proceed.
- Don't over-ask: a handful of targeted suggestions, not a generic checklist.
  One round of suggestions, then run the council.

**Part B — assemble the packet.** For material that is actually available or the
user confirmed, build a context packet at `/tmp/council/context.md`, one block
per item:

- **Text-ish files** (`.md` `.txt` `.R` `.tex` `.csv`/dictionaries, source code):
  read with the Read tool and embed verbatim under a header `### File: <path>`.
- **PDFs:** never read a PDF in the main thread (Rule #21). Spawn a Sonnet
  subagent (`model: sonnet`; Opus for dense tables/math) that reads it and returns
  the **text faithfully (not a summary)**; embed that text under `### File: <path>`.
  Page images stay in the subagent. If the user already has an `.md` of the paper,
  use that directly and skip the subagent.
- **Inline content:** already in the question — leave it there.

**Size guard:** the packet goes to 4 members × 2 stages. If it is large (very
roughly >6k words), tell the user the rough cost before proceeding, or offer to
trim to the relevant excerpt. Keep raw data out of it (Rule #3: a data dictionary
is fine, a data file is not).

Keep the path→content map; both stage prompts reference the same `context.md`.

### Stage 1 — Dispatch (parallel)

1. Write the dispatch prompt to `/tmp/council/q1.txt`. Prepend the context packet
   when Stage 0 produced one:

   ```
   [CONTEXT — material the council must base its answer on]
   <contents of /tmp/council/context.md, omit this whole block if none>

   You are one member of an expert council answering a user's question.
   Give your best, complete, standalone answer grounded in the context above
   (if any). Be substantive, specific, and honest about uncertainty. Answer in
   the same language as the question. Do not mention that you are part of a council.

   QUESTION:
   <the user's question, verbatim>
   ```

2. In **one orchestrator message**, do both of these so the slow CLIs and the
   subagent all run concurrently:
   - **One** Bash call to the fan-out driver — it backgrounds all three external
     members with `&`/`wait`, so true parallelism does NOT depend on the model
     batching tool calls, and it costs a single permission prompt instead of three:
     `bash ~/.claude/skills/council/dispatch.sh /tmp/council/q1.txt /tmp/council/s1`
   - **One** Agent call (`subagent_type: claude`, `model: sonnet`) whose prompt is
     the contents of `q1.txt`. Tell it to return only its answer, no preamble.

   Do NOT issue the three external members as three separate Bash calls — that is
   what regressed to sequential dispatch. Always go through `dispatch.sh`.

3. Read the three answer files `/tmp/council/s1/{gemini,openai,mistral}.txt`
   plus the Sonnet subagent's result → `R1…R4`. The driver prints `OK`/`EMPTY`
   per member; an **empty file means that CLI failed** — mark it unavailable and
   drop it (graceful degradation). Proceed as long as **≥2 members answered**;
   note any drop-outs in the final output. Don't echo the answer files — see
   "Progress narration during the run" for what to print here.

### Stage 2 — Anonymized peer review (parallel)

1. Shuffle the answers and relabel them `Response 1…Response N` with **no model
   names** (so label order ≠ member order; no member can identify its own).
   Keep a private map of label → member for your own bookkeeping.

2. Write the review prompt to `/tmp/council/q2.txt`. If Stage 0 built a context
   packet, prepend it here too — reviewers need the source to judge which answer
   used it accurately:

   ```
   [CONTEXT — the material the answers were supposed to use]
   <contents of /tmp/council/context.md, omit this whole block if none>

   Below are anonymized answers from a council of AI models to this question.

   QUESTION:
   <question>

   Response 1:
   <…>

   Response 2:
   <…>

   …(all N responses)…

   Evaluate the responses for accuracy, depth, and usefulness. Then output
   EXACTLY in this format, nothing before it:

   RANKING: <comma-separated response numbers, best first>
   (example: RANKING: 3, 1, 4, 2)

   Then one line per response:
   Response <n>: <one sentence — its main strength or the error that sank it>
   ```

3. Fire the **same** `q2.txt` at all available members again, the same way as
   stage 1: one `dispatch.sh` call (into a fresh dir `/tmp/council/s2`) plus the
   Sonnet subagent, in one message. Collect each member's `RANKING:` line and
   critique from `/tmp/council/s2/*.txt` and the subagent result. Keep the
   label→member map private (see "Progress narration during the run").

4. Aggregate with the helper. Build a JSON object and pipe it to `borda.py`:

   ```bash
   echo '{"members":["Gemini 3.1 Pro","GPT-5.5","Mistral Medium 3.5","Claude Sonnet 4.6"],
          "rankings":[[…],[…],[…],[…],[…]]}' \
     | python3 ~/.claude/skills/council/borda.py
   ```

   `members` must be in **response-number order** (member behind Response 1 first,
   etc. — i.e. un-shuffle back to a fixed order before scoring). Each `rankings`
   entry is one reviewer's best-first list of response numbers. `borda.py` prints
   the leaderboard and a `SCORES_JSON:` line. Drop any member that didn't answer.

### Stage 3 — Chairman synthesis

Spawn one **Agent** (`subagent_type: claude`, `model: opus`). Give it:
- the original question,
- all member answers (now de-anonymized, labeled by model),
- each member's ranking + critique,
- the Borda leaderboard from `borda.py`.

Chairman prompt:

```
You are the chairman of an AI council. Below is a question, each member's full
answer, each member's anonymous ranking and critique of the others, and the
aggregate Borda leaderboard.

Write the single best answer to the question. Synthesize — merge the strongest
material across members and correct any error the reviews surfaced; do not just
pick one member's answer. Answer in the question's language, and use that
language for any headings you write.

Structure it exactly so, for skimmability:
- Open with a one-line **verdict in bold** — the answer in a single sentence.
- Then the rationale: the 2–3 load-bearing reasons, each a short paragraph or
  tight bullet. Carry only what is decision-relevant — not every angle raised.
- If there was real disagreement, end with a short "Dissent" note: the minority
  view and why you did or didn't follow it.

Be brief: a tight verdict + rationale beats an exhaustive essay. A genuinely
high-stakes call may run longer, but still lead with the verdict and keep each
section short. Do NOT write a "Council notes" or leaderboard section — that is
appended separately by the orchestrator.

QUESTION: …
MEMBER ANSWERS: …
REVIEWS + RANKINGS: …
BORDA LEADERBOARD: …
```

## Progress narration during the run

The dispatch takes ~1–2 min; keep the user oriented without the play-by-play
noise. **Emit at most one brief status line per stage**, plain prose — e.g.:

- on convening: `Convening the council on <short topic>. Dispatching 4 members in parallel…`
- after Stage 1 collect: `Answers in — N/5 responded[, dropped: X]. Running anonymized peer review…`
- after Stage 2 / Borda: `Peer review done. Synthesizing…`

Do **not**:
- echo raw tool output — no pasting `cat`/file contents, no per-member word counts,
  no "X's answer is in" beats;
- print the private label→member map (e.g. "R1=Mistral…") — it is internal
  bookkeeping, and surfacing it defeats the anonymity Stage 2 exists for.

The only substantive prose the user reads is the final synthesis block below.

## Output to the user

The chairman (Opus) produces only the **Answer** block (verdict + rationale +
dissent). The orchestrator wraps it and appends Council notes and the raw block.
Headings follow the **question's language** — `## Answer` / `## Council notes`
for an English question, `## Antwort` / `## Council-Notizen` for a German one:

```
## Answer            (## Antwort)
<chairman synthesis: bold verdict line, rationale, dissent>

## Council notes     (## Council-Notizen)
- Leaderboard (Borda): <paste borda.py's ranked lines verbatim>
- Dissent: <one line, or "largely aligned" / "weitgehend einig">
- (if any) Unavailable: <dropped members>

<details><summary>Raw answers + rankings</summary>
<the N de-anonymized member answers, plus each reviewer's RANKING line>
</details>
```

The leaderboard lives **only** in Council notes — paste `borda.py`'s output
verbatim; the synthesis must not restate it. Embed the **actual** member answers
in the `<details>` block (you hold `R1…R4`) — not a `/tmp/council/...` pointer —
so the reasoning is auditable without dominating the reply.

## Notes & robustness

- **Parallelism:** the three external members MUST go through `dispatch.sh` (shell
  `&`/`wait`) — never as four separate Bash tool calls, which the orchestrator
  tends to run sequentially. Spawn the Sonnet subagent in the same message so it
  overlaps the driver. Each external call takes ~15–90 s; serial would be painful.
- **Long prompts go in files** (`q1.txt`, `q2.txt`) — never inline a multi-line
  question/bundle as a shell argument (quoting breaks).
- **Empty output = unavailable.** `ask_member.sh` prints nothing on CLI failure;
  treat that member as absent for this run and say so.
- **Cost:** 4 members × 2 stages + 1 chairman ≈ 9 model calls. Opt-in only.
- **Roster changes:** edit the table above and the `members` array passed to
  `borda.py` together — they must stay in the same order.
