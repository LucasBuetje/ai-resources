# Current Session

2026-06-29 — Major restructure on branch `restructure-resources` (not main). Reorganized
the repo around the agent-workflow concept arc (context → memory → plan mode → skills →
subagents → MCP → hooks → verification), as a standalone resource (no talk-handout framing).

What changed:
- New `presentations/` folder; added this talk (PDF + tex + image) under
  `ai-agents-research-teaching/`.
- `ai-agent/` reorganized: folders only where there's a real artifact —
  `getting-started/`, `claude-md/`, `memory-log/`, `skills/`, `hooks/`, `verification/`.
  Plan mode / subagents / MCP are sections in `ai-agent/README.md`, not empty folders.
- Skills: now ships 11 (summarize-paper, referee2, blindspot, germancheck, econ-write,
  revise, deck, tikz, council, premortem, skill-update-check), copied from live config + sanitized.
  Retired critic/scholar/devils-advocate/empirical-paper-summarizer → archive/retired-skills/.
- Hooks: ships 3 (guard-rm, warn-pdf-mainthread, session-start-current-log). (stop-log-reminder removed at Lucas's request → archive/.)
- New `claude-md/global-CLAUDE.md` (expanded, sanitized) + `project-CLAUDE.md` example.
- `memory-log/current.md` template; `verification/example-recovery-check.R` (runs, PASS).
- Root + ai-agent READMEs rewritten as bullet skeletons (Lucas writes the prose).
- .gitignore += .Rhistory; untracked the empty archived .Rhistory.

Verified: no leaked personal data (only the public email; "Konstanz" is just the deck
palette name), all local markdown links resolve, `bash -n` passes on all 4 hooks,
verification R script PASSes.

Open / decisions for Lucas:
- READMEs are bullet skeletons by request — prose still to be written by Lucas.
- Older talks (AI_Exchange, "KI in der Lehre ADILT") not imported into presentations/ yet —
  awaiting go-ahead.
- Branch is uncommitted — Lucas commits.

2026-06-29 (later) — Refocused on agentic AI per Lucas. Dissolved `ai-agent/`: its concept
folders (claude-md, memory-log, skills, hooks, verification, getting-started) promoted to
repo ROOT. Root README is now the agentic walkthrough itself (the spine). Claude Code vs
OpenCode comparison moved OFF the landing page into `getting-started/README.md`. `ai-chat/`
renamed to `non-agentic/` (now holds AI-chat prompts + CRISPE + other tools), linked as a
footnote on the main page. Old `ai-agent/README.md` → `archive/ai-agent-README-superseded.md`.
All links re-checked (pass). Landing page is intentionally lean now.

2026-06-29 (later 2) — (1) Split the landing toolkit table into "The basics" (Context,
Memory, Plan mode) and "More specialized" (Skills, Subagents, MCP, Hooks, Verification).
(2) Gave plan-mode/, subagents/, mcp/ their own READMEs (content from the talk slides) and
linked the table rows to them; removed the inline note block. (3) claude-md/ is now just a
README explainer (global vs project, example code blocks) — archived the standalone
global-CLAUDE.md/project-CLAUDE.md to archive/claude-md-examples/, repointed 3 links.
(4) skills/README.md table now has a Source column crediting each author (Scott Cunningham,
Andrej Karpathy, hanlulong, olelehmann1337, or "original").
