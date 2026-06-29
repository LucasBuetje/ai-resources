# Working with an AI agent

How I actually use AI coding agents (Claude Code, OpenCode) for research and teaching. This folder walks through it in the order things matter — but it's a menu, not a manual. Take what fits, adapt the rest.

- **New here?** Start with [`getting-started/`](getting-started/) — install Claude Code or OpenCode (with free GWDG models).
- An agent runs *inside a project folder*: it reads, writes, and runs commands there, and (by default) can't reach above it. That folder is its whole world.
- Think of it as a fast, capable research assistant that starts every session with **no context and no memory**. The pieces below are how you give it both, keep it safe, and check its work.

## The arc

### 1. Context — [`claude-md/`](claude-md/)
- A `CLAUDE.md` file the agent reads at the start of every session, so you stop re-explaining yourself.
- **Global** (`~/.claude/CLAUDE.md`): how *you* work — applies everywhere. See [`global-CLAUDE.md`](claude-md/global-CLAUDE.md).
- **Project** (`<project>/CLAUDE.md`): what *this* project is — data locations, build commands, conventions. See [`project-CLAUDE.md`](claude-md/project-CLAUDE.md).
- The two stack. Tip: run `/init` in a new project to have the agent draft the project file for you.

### 2. Memory — [`memory-log/`](memory-log/)
- Agents forget everything between sessions. One file, `log/current.md`, carries working memory forward.
- The agent appends what changed and what's open; the next session reads it back in (automatically, with the SessionStart hook).

### 3. Plan mode
*A habit, not a file — no folder.*
- The agent investigates and writes a **plan**, but changes nothing until you approve. The single most useful safety habit.
- Without it: it edits immediately, and you find a wrong assumption *after* 12 files changed. With it: you fix the misunderstanding first, then it touches your files.
- Use it for anything non-trivial; for small tasks, just tell it what to do.

### 4. Skills — [`skills/`](skills/)
- Reusable, named recipes invoked with one command (`/summarize-paper`, `/referee2`, …). Write the instructions once, reuse forever.
- See [`skills/README.md`](skills/README.md) for the 11 shipped here and how to install them.

### 5. Subagents
*A capability shown through the skills — no folder.*
- The agent can spawn many subagents that work in parallel, each on a slice, then report back. Saves time, not tokens (N subagents ≈ N× the quota).
- In practice: `/summarize-paper` fans out across a reading list; `/referee2` runs five specialist auditors at once; `/council` sends a question to several models that critique each other.

### 6. MCP
*Connecting the agent to other tools — setup is per-tool, no folder.*
- MCP (Model Context Protocol) is a standard plug for external tools. Each server is installed once, then the agent can call it.
- Example: a **Zotero MCP** lets the agent answer "what papers do I have on X?" and pull a PDF (with your highlights) straight from your library. Install the server per its own docs, then register it with your agent (`claude mcp add …` for Claude Code, or the OpenCode MCP config).
- **Caution:** an MCP runs code on your machine. Install only servers you trust — a malicious one has the same reach as the agent.

### 7. Hooks — [`hooks/`](hooks/)
- Small scripts the tool runs automatically at set moments (before a command, at session start, on stop). Your conventions, enforced by code instead of trust.
- The 4 shipped here back up rules from `global-CLAUDE.md` — e.g. `guard-rm.sh` blocks `rm` and points at `archive/`.

### 8. Verification — [`verification/`](verification/)
- Producing code/analyses is now cheap; *checking* them is the bottleneck. The agent is confident even when wrong.
- Have it write re-runnable verification scripts that test against a known truth — see the runnable [`example-recovery-check.R`](verification/example-recovery-check.R).

## And nothing is lost
- Every session is saved as structured text at `~/.claude/projects/<working-dir>/<session-id>.jsonl`: the original prompt, every tool call, every subagent, every error and retry. A flight recorder — the work is reproducible and auditable, not a black box.
