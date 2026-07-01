# Skills

Reusable, named recipes — expert instructions written once, invoked with one command (e.g. `/summarize-paper`). Each folder here is a self-contained skill.

- Most are adapted from others' work — the **Source** column credits each and links upstream (it's also in each skill's `origin` field). Many come from Scott Cunningham's [MixtapeTools](https://github.com/scunning1975/MixtapeTools) and [Claude Code blog](https://causalinf.substack.com/s/claude-code).
- These are *my* adaptations. They are a menu, not a standard — copy the ones you want and adapt them to how you work.

## Install

- **Easiest — just ask the agent.** Point your agent at this repo and say *"install the `deck` and `referee2` skills"* — it copies the right folders into place for you.
- **Manual (Claude Code):** copy a skill folder into `~/.claude/skills/` (e.g. `cp -R deck ~/.claude/skills/`). Invoke with `/<skill-name>`.
- **Manual (OpenCode):** copy into `~/.config/opencode/commands/`.
- Some skills ship helper scripts (e.g. `council/`) or knowledge files (e.g. `deck/rhetoric.md`) alongside `SKILL.md` — copy the whole folder, not just `SKILL.md`.

## The skills

| Skill | Command | What it does | Source |
|---|---|---|---|
| [summarize-paper](summarize-paper/) | `/summarize-paper` | Deep whole-paper read (one Opus subagent, no chunking); structured extract of data, identification strategy, results. Zotero-aware. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [referee2](referee2/) | `/referee2` | Full empirical-research audit + cross-language R↔Python replication. Five audits, a formal referee report, and a Beamer deck. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [blindspot](blindspot/) | `/blindspot` | Peripheral-vision audit of empirical output — surfaces problems you can't see in your own results, and opportunities you're missing. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [econ-write](econ-write/) | `/econ-write` | Economics-paper writing assistant synthesizing 50+ top writing guides (Cochrane, McCloskey, Shapiro, …). All sections, all paper types. | [hanlulong](https://github.com/hanlulong/econ-writing-skill) |
| [revise](revise/) | `/revise` | Respond to referee/reviewer comments interactively — one at a time, classified and drafted with your approval at each step. | original |
| [deck](deck/) | `/deck` | Build or edit a Beamer deck following evidence-based rhetoric principles. Includes [rhetoric.md](deck/rhetoric.md), a knowledge base on what makes slides work. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [tikz](tikz/) | `/tikz` | Visual-collision check for figures (TikZ source or rendered PNG/PDF) — label collisions, whitespace, edge-running. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [council](council/) | `/council` | Multi-model "council": several model families answer, peer-rank each other anonymously, and a chair synthesizes. Adapt it to the models you have available. | [Andrej Karpathy](https://github.com/karpathy/llm-council) |
| [premortem](premortem/) | `/premortem` | Decision premortem — imagine the plan already failed, work backward to the most critical risks before committing. | [olelehmann1337](https://github.com/olelehmann1337/openclaw-share) |
| [skill-update-check](skill-update-check/) | `/skill-update-check` | Check your adapted skills against their upstream GitHub sources and flag substantial updates worth adopting. | original |
