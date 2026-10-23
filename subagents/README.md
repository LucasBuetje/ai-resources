# Subagents

The agent can spawn **many subagents** that work in parallel — each on a slice of the task — then report back. One assistant becomes a team.

Useful for (at least) two things
- **Parallelization** (get the same thing faster)
- **Different roles** (specialist subagent)

## Example use-cases

- **Reading list:** ask the agent to run [`/summarize-paper`](../skills/summarize-paper/) on a folder of papers — it spawns one subagent per paper, so a whole stack is summarized in about the time it takes to read one.
- **Paper audit:** [`/referee2`](../skills/referee2/) runs five specialists simultaneously: code, replication, econometrics, structure, prose.

## Custom agent types

A subagent can be given a fixed role and a fixed tool list in a small file under `~/.claude/agents/`. A tool list holds where a prompt doesn't: an agent told "don't use Bash" may still use it, an agent without Bash can't.

- [`pdf-reader.md`](pdf-reader.md) — the reader `/summarize-paper` spawns: Sonnet, only Read and Write, so it reads the paper and writes one extract file and can do nothing else. Copy it to `~/.claude/agents/`; without it the skill falls back to a general-purpose subagent.

## Saves time, not tokens

- Running N subagents costs roughly **N× the quota** — they all think in parallel.

## You don't set this up

- No manual wiring — just ask: "use one subagent per paper", "fan this out", "run these checks in parallel".
