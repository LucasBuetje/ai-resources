# Subagents

The agent can spawn **many subagents** that work in parallel — each on a slice of the task — then report back. One assistant becomes a team.

## What it's good for

- **Reading list:** ask the agent to run [`/summarize-paper`](../skills/summarize-paper/) on a folder of papers — it spawns one subagent per paper, so a whole stack is summarized in about the time it takes to read one.
- **Paper audit:** [`/referee2`](../skills/referee2/) runs five specialists simultaneously: code, replication, econometrics, structure, prose.
- **LLM council:** [`/council`](../skills/council/) sends a question to several models; they critique each other and a chair synthesizes.

> [!TIP]
> **Example:** 30 papers on peer effects summarized and synthesized in a coffee break.

## Saves time, not tokens

- Running N subagents costs roughly **N× the quota** — they all think in parallel.
- So the win is *wall-clock time*, not cost. Reach for them when the work splits cleanly into independent slices, not to save money.

## You don't set this up

- No manual wiring — just ask: "use one subagent per paper", "fan this out", "run these checks in parallel".
