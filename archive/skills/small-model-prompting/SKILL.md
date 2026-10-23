---
name: small-model-prompting
origin: adapted from https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5
description: "How to write a prompt for a subagent on the lowest-tier (cheapest) Claude model, currently Haiku. Load before delegating to it (model=\"haiku\"), and when such a subagent stops early, skips a check or ignores instructions."
---

# Prompting the lowest-tier model as a subagent

The cheapest Claude tier (today Haiku; at the time of writing Claude Haiku 5.5,
`claude-haiku-5-5`) is the right tool for a narrow kind of job and needs tighter prompts than
the larger tiers. A new small model is often released after the session model's training
cutoff, so do not assume you know how it behaves: read Anthropic's prompting guide for the
current version (the frontmatter links the Haiku 5.5 one) and update the specifics below.

## When the lowest tier is the right subagent

Only for extraction or lookup where **a script or exact string match checks the result
afterwards**. Its output is cheap, not authoritative. Estimation, analysis code, careful
phrasing, critique and PDF reading stay at the middle tier (Sonnet) or higher.

## Prompt rules

These held for Haiku 5.5; check them against the guide when the model changes.

- **Keep tasks small and the output one line.** Thinking is on by default and could not be
  prompted away ("answer directly" did not stop it in Anthropic's tests).
- **Effort: leave it at the default (`medium`).** `low` makes the model skip searches, stop
  early and skip checks in long prompts; going from `low` to `medium` roughly halved early
  stopping (at about twice the output tokens). Only set effort when the user asks for a level.
- **Long prompts: add this paragraph** (the model sometimes stops early and hands the task
  back):
  > Keep working until everything the user asked for is done, and only stop to ask when you
  > can't go on without the user or before a risky step. When the work is done and checked,
  > stop and report. Don't add features, docs or refactors that weren't asked for; mention
  > them at the end instead.
- **Runnable code changes: add this paragraph** (otherwise it reports "done" without a check):
  > When you change code that can be run, built or type-checked, run a real check that
  > exercises the change before reporting it done. A syntax-only check, or a check that
  > failed to start, does not count; if all that is missing is the project's declared
  > dependencies, install them with its own package manager inside the project's venv. If no
  > real check can run, say which one you did not run and why instead of reporting the
  > change as done.
- **Search or "latest" questions:** put today's date in the prompt. Small models skip
  searches they should do, most at low effort and with long prompts. Add: "Your training data
  ends well before today's date; for records, office holders, prices, versions and anything
  'latest', search before you answer. Facts that can't change need no search." Do not write
  blanket "always search" rules: Haiku 5.5 then searched on half of the prompts that needed
  none.
- **Reasoning leaks into the reply** more often at low effort. Ask for results in a fixed
  format (JSON or one line), not prose.

## Delegation pattern that works

1. Inputs from disk (a batch file), never pasted into the prompt.
2. Output to a file written with `python3 json.dumps`, one write per batch; the reply to you
   is one line.
3. A script validates every result against its source (verbatim quote present, schema,
   counts). A larger model re-judges only the disagreements or the subset that matters.
4. Ask for honest self-reports (`process_attest`-style booleans), and keep the gate that
   checks them. In a test, Haiku 5.5 reported an incomplete pagination (50 of 1,085 items)
   instead of claiming success.

## Cost facts (Haiku 5.5, measured 2026-10-08)

- A general-purpose subagent costs ~27k tokens per request in fixed context (CLAUDE.md
  files plus the core tools), whatever the task: batch many items per agent.
- The Explore agent skips CLAUDE.md (~16k per request) but also does not see your rules,
  and cannot write files. Don't use it for anything that needs the rules.
- Price: $0.10 / $0.50 per MTok up to 100k tokens in a prompt; the same text is ~30% more
  tokens than on Haiku 4.5.

Not covered (API-only): structured outputs with own tools, `temperature` errors, refusal
handling, mid-turn user messages.
