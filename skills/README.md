# Skills

Reusable, named recipes — expert instructions written once, invoked with one command (e.g. `/summarize-paper`). Each folder here is a self-contained skill.

- Most are adapted from or inspired by Scott Cunningham's [Claude Code blog](https://causalinf.substack.com/s/claude-code) — see each skill's `origin` field.
- These are *my* skills. They are a menu, not a standard — copy the ones you want and adapt them to how you work.

## Install

- **Claude Code:** copy a skill folder into `~/.claude/skills/` (e.g. `cp -R deck ~/.claude/skills/`). Invoke with `/<skill-name>`.
- **OpenCode:** copy into `~/.config/opencode/commands/`.
- Some skills ship helper scripts (e.g. `council/`) or knowledge files (e.g. `deck/rhetoric.md`) alongside `SKILL.md` — copy the whole folder, not just `SKILL.md`.

## The skills

| Skill | Command | What it does |
|---|---|---|
| [summarize-paper](summarize-paper/) | `/summarize-paper` | Deep whole-paper read (one Opus subagent, no chunking); structured extract of data, identification strategy, results. Zotero-aware. |
| [referee2](referee2/) | `/referee2` | Full empirical-research audit + cross-language R↔Python replication. Five audits, a formal referee report, and a Beamer deck. |
| [blindspot](blindspot/) | `/blindspot` | Peripheral-vision audit of empirical output — surfaces problems you can't see in your own results, and opportunities you're missing. |
| [econ-write](econ-write/) | `/econ-write` | Economics-paper writing assistant synthesizing 50+ top writing guides (Cochrane, McCloskey, Shapiro, …). All sections, all paper types. |
| [germancheck](germancheck/) | `/germancheck` | Hunts translation tells in German prose — anglicism calques, false friends, English-mirroring structure. |
| [revise](revise/) | `/revise` | Respond to referee/reviewer comments interactively — one at a time, classified and drafted with your approval at each step. |
| [deck](deck/) | `/deck` | Build or edit a Beamer deck following evidence-based rhetoric principles. Includes [rhetoric.md](deck/rhetoric.md), a knowledge base on what makes slides work. |
| [tikz](tikz/) | `/tikz` | Visual-collision check for figures (TikZ source or rendered PNG/PDF) — label collisions, whitespace, edge-running. |
| [council](council/) | `/council` | Multi-model "council": several model families answer, peer-rank each other anonymously, and a chair synthesizes. Needs adapting to your own model CLIs. |
| [premortem](premortem/) | `/premortem` | Decision premortem — imagine the plan already failed, work backward to the most critical risks before committing. |
| [skill-update-check](skill-update-check/) | `/skill-update-check` | Check your adapted skills against their upstream GitHub sources and flag substantial updates worth adopting. |
