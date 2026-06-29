# Plan mode

The agent investigates and writes a **plan**, but changes *nothing* until you say go. The single most useful safety habit — and it needs no setup, it's built into the tool.

## Why it matters

| Without plan mode | With plan mode |
|---|---|
| It starts editing immediately | You read the plan first, fix the misunderstanding |
| You discover a wrong assumption *after* 12 files changed | Only then does it touch your files |

- The cost of a wrong assumption is paid *before* any file changes, not after.

## When to use it

- Anything non-trivial or multi-step — refactors, a new analysis, touching many files.
- For small, well-defined tasks, skip it: just tell the agent what to do.

## How

- In Claude Code, enter plan mode before describing the task; the agent explores read-only, proposes a plan, and waits.
- Read it, push back, refine — then approve. Treat the plan as the place to catch misunderstandings cheaply.
