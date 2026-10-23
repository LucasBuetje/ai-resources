<div align="center">

# AI Resources

**How I use AI _agents_ for academic research and teaching** — the setups, conventions, and skills I actually use.


</div>

> [!NOTE]
> - **Treat this as a menu, not a template.** Don't clone it and expect it to "work" — it's here to inspire and be picked from. Take what fits how you work, adapt it, ignore the rest.
> - **Agentic AI is the focus:** Plain chat and other tools have been demoted to a footnote (just as they have been in my workflow) → [`non-agentic/`](non-agentic/).
> - **Written from a Claude Code perspective** — that's what I use, so the paths and commands here are Claude's.

_**Provided as-is; use at your own risk.**_ · Reach out: lucas.buetje.economist@outlook.com

---

## What an AI agent is

- An LLM that can actually **_do real work_** - by running commands on your computer.
- It runs **inside a (project) folder**: reads, writes, and runs commands there, and by default can't reach above it. That folder is its **whole world**.
- Think of it as a fast, capable **research assistant** that starts every session with **no context and no memory** — the toolkit below is how you give it both, keep it safe, and check its work.
- Because it can run any terminal command, it can in principle do **anything your computer can**.

## Get an agent

Don't have one installed yet? This repo is built around Claude Code:

| Provider | Agent | Install |
|---|---|---|
| Anthropic | Claude Code | [claude.com/product/claude-code](https://claude.com/product/claude-code) |

## Risks and safeguards

> [!CAUTION]
> **Risks to know**
> - **File access is real** — files can be overwritten or deleted
> - **Untrusted plugins (MCPs)** can run malicious code on your machine
> - **Sensitive files** in the working folder (keys, credentials, data) are readable
> - **Errors compound** — a wrong assumption gets confidently built upon

> [!TIP]
> **Built-in safeguards**
> - **Permission prompt** before each action
> - **Plan / read-only mode** before anything runs
> - **Confined** to the working folder
> - **Visible diffs** before changes apply

> [!WARNING]
> **Stay alert anyway.** Safeguards can fail, the tools keep changing, and permission pop-ups get clicked away. Use plan mode, keep backups / version control, and install only what you trust.

## How to use an agent well, in my experience

You _can_ just put an agent in a folder and start talking to it. But I don't think you _should_ (most of the time). 

Here's a list of the tools I use to make my agent better.

**None of it is manual** — you just ask the agent to set it up (examples below ↓).

**The basics** — I set these up for every project:

| | Feature | What it does | Details |
|:--:|---|---|:--:|
| 📋 | **Context** | A `CLAUDE.md` the agent reads every session — how *you* work, what *this* project is. | [`claude-md/`](claude-md/) |
| 🧠 | **Memory** | A running `current.md` in the project root that carries working memory across sessions. | [`memory-log/`](memory-log/) |
| 📝 | **Plan mode** | The agent plans; you approve; *then* it edits. | [`plan-mode/`](plan-mode/) |

**More specialized** — reach for these as the task calls for it:

| | Feature | What it does | Details |
|:--:|---|---|:--:|
| ⚡ | **Skills** | Reusable one-command recipes — `/summarize-paper`, `/referee2`, … (9 of them). | [`skills/`](skills/) |
| 👥 | **Subagents** | A team working in parallel, each on a subtask, then reporting back. | [`subagents/`](subagents/) |
| 🔌 | **MCP** | Plug the agent into external tools (e.g. a Zotero library). | [`mcp/`](mcp/) |
| 🪝 | **Hooks** | Your conventions enforced by code, not trust. | [`hooks/`](hooks/) |

> [!TIP]
> **You don't have to set any of this up by hand.** Just ask the agent and it does it for you — for example:
> - *"Set up a `CLAUDE.md` for this project."*
> - *"Turn this GitHub repo into a skill, adapted to my workflow."*
> - *"Use one subagent per paper."*
>
> The folders above are examples to point it at, not chores for you.

## What's in the box

**Skills** (each runs with `/<name>`; details in [`skills/`](skills/)):

- **Reading** — [`/summarize-paper`](skills/summarize-paper/): a whole paper read in one pass, then fact-checked.
- **Writing** — [`/econ-write`](skills/econ-write/): writing guidance for economics papers · [`/number-check`](skills/number-check/): every number in the prose traced back to its source.
- **Code** — [`/code-audit`](skills/code-audit/): is this script right? · [`/referee2`](skills/referee2/): a full project audit with replication · [`/explain-diff`](skills/explain-diff/): a code change explained as slides · [`/walkthrough`](skills/walkthrough/): you explain an AI's commit first, then learn the gaps.
- **Talks** — [`/deck`](skills/deck/): Beamer decks built on rhetoric principles.
- **Decisions** — [`/premortem`](skills/premortem/): find how a plan fails before you commit to it.

**Hooks** (they run automatically; details in [`hooks/`](hooks/)):

- `guard-rm` and `guard-script-delete` — the agent moves files to `archive/` instead of deleting them, in commands and in scripts it writes.
- `session-start-current-log` and `stop-log-reminder` — working memory is loaded at the start of each session and kept up to date at the end of each turn.
- `warn-pdf-mainthread` — a warning before a PDF is read in a way that bloats the session.

## Claude's Automatic Documentation: Nothing is lost

- Every session is **saved as structured text** at `~/.claude/projects/<dir>/<session-id>.jsonl`: the original prompt, every tool call, subagent, script, error, and retry.
- The quiet fear is that AI work is a **black box**. It isn't — the full record sits on your machine, **reproducible and auditable**, ready to hand to a co-author or another agent.
- Still, this is not exactly very readable, so I think the logging in .md files still deserves its place.

---

<div align="center">

💬 [**Non-agentic AI**](non-agentic/): chat prompts &amp; other tools

</div>
