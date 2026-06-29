<div align="center">

# AI Resources

**How I use AI _agents_ for academic research and teaching** — the setups, conventions, and skills I actually rely on, day-to-day.

`Claude Code` · `OpenCode` · `Research` · `Teaching`

</div>

> [!NOTE]
> **This is a menu, not a template.** Don't clone it and expect it to "work" — it's here to inspire and be picked from. Take what fits how you work, adapt it, ignore the rest.
> **Agentic AI is the focus:** tools that act on your computer. Plain chat and other tools are a footnote → [`non-agentic/`](non-agentic/).

New here? Install a tool first → [`getting-started/`](getting-started/) · _Provided as-is; use at your own risk._ · Reach out: lucas.buetje.economist@outlook.com

---

## What an AI agent is

- It runs **inside a project folder**: reads, writes, and runs commands there, and by default can't reach above it. That folder is its **whole world**.
- Think of it as a fast, capable **research assistant** that starts every session with **no context and no memory** — the toolkit below is how you give it both, keep it safe, and check its work.
- Because it can run any terminal command, it can in principle do **anything your computer can**.

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

## How I use an agent well

The toolkit, in the order it matters. Each row links to its folder, or to a note below.

| | Step | What it does | Where |
|:--:|---|---|:--:|
| 📋 | **Context** | A `CLAUDE.md` the agent reads every session — how *you* work, what *this* project is. | [`claude-md/`](claude-md/) |
| 🧠 | **Memory** | A running `log/current.md` that carries working memory across sessions. | [`memory-log/`](memory-log/) |
| 📝 | **Plan mode** | The agent plans; you approve; *then* it edits. | _note ↓_ |
| ⚡ | **Skills** | Reusable one-command recipes — `/summarize-paper`, `/referee2`, … (11 of them). | [`skills/`](skills/) |
| 👥 | **Subagents** | A team working in parallel, each on a slice, then reporting back. | _note ↓_ |
| 🔌 | **MCP** | Plug the agent into external tools (e.g. a Zotero library). | _note ↓_ |
| 🪝 | **Hooks** | Your conventions enforced by code, not trust. | [`hooks/`](hooks/) |
| ✅ | **Verification** | Re-runnable checks against a known truth — the new bottleneck. | [`verification/`](verification/) |

> [!TIP]
> **Plan mode** is the single most useful safety habit. Without it, you find a wrong assumption *after* 12 files changed; with it, you fix the misunderstanding first.
>
> **Subagents** save time, not tokens (N subagents ≈ N× the quota): `/summarize-paper` fans out across a reading list, `/referee2` runs five specialist auditors at once.

> [!CAUTION]
> **MCP** servers run code on your machine. They're powerful — a Zotero MCP can pull a paper (with your highlights) straight into the chat — but install only servers you trust.

## Nothing is lost

- Every session is **saved as structured text** at `~/.claude/projects/<dir>/<session-id>.jsonl`: the original prompt, every tool call, subagent, script, error, and retry.
- The quiet fear is that AI work is a **black box**. It isn't — the full record sits on your machine, **reproducible and auditable**, ready to hand to a co-author or another agent.

---

<div align="center">

📊 [**Slides**](presentations/) from talks on this material  ·  💬 [**Non-agentic AI**](non-agentic/): chat prompts &amp; other tools

</div>
