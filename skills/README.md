# Skills

Reusable, named recipes — expert instructions written once, invoked with one command (e.g. `/summarize-paper`). Each folder here is a self-contained skill.

- Most are adapted from others' work — the **Source** column credits each and links upstream (it's also in each skill's `origin` field). Many come from Scott Cunningham's [MixtapeTools](https://github.com/scunning1975/MixtapeTools) and [Claude Code blog](https://causalinf.substack.com/s/claude-code).
- These are *my* adaptations. They are a menu, not a standard — copy the ones you want and adapt them to how you work.

## Install

- **Easiest — just ask the agent.** Point your agent at this repo and say *"install the `deck` and `referee2` skills"* — it copies the right folders into place for you.
- **Manual (Claude Code):** copy a skill folder into `~/.claude/skills/` (e.g. `cp -R deck ~/.claude/skills/`). Invoke with `/<skill-name>`.
- Some skills ship helper scripts (e.g. `summarize-paper/`) or knowledge files (e.g. `deck/rhetoric.md`) alongside `SKILL.md` — copy the whole folder, not just `SKILL.md`.

## The skills

Nine skills, grouped by the task they help with.

### Reading

| Skill | What it does | Source |
|---|---|---|
| [summarize-paper](summarize-paper/) | Deep whole-paper read in one pass (Sonnet subagent by default, Opus on request), then a Haiku fact-check gated by scripts; structured extract of data, identification strategy, results. Zotero-aware. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |

### Writing

| Skill | What it does | Source |
|---|---|---|
| [econ-write](econ-write/) | Economics-paper writing assistant synthesizing 50+ top writing guides (Cochrane, McCloskey, Shapiro, …). All sections, all paper types. | [hanlulong](https://github.com/hanlulong/econ-writing-skill) |
| [number-check](number-check/) | Traces every number quoted in prose (paper, deck, referee reply) back to the output that produced it and reports drift. | original |

### Code

| Skill | What it does | Source |
|---|---|---|
| [code-audit](code-audit/) | Correctness audit of one empirical script — data integrity, econometric specification, reproducibility; every serious finding is verified by running the code. | [aspi6246](https://github.com/aspi6246/Claude-Code-Skills-for-Academics) |
| [referee2](referee2/) | Full empirical-research audit + cross-language R↔Python replication. Five audits, a formal referee report, and a Beamer deck. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |
| [explain-diff](explain-diff/) | Builds an interactive HTML slide deck that teaches how a code change works. | [Geoffrey Litt](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524) |
| [walkthrough](walkthrough/) | You explain an AI-authored commit in your own words first; the agent teaches only the gaps (via explain-diff) and quizzes you. | original |

### Talks

| Skill | What it does | Source |
|---|---|---|
| [deck](deck/) | Build or edit a Beamer deck following evidence-based rhetoric principles. Includes [rhetoric.md](deck/rhetoric.md), a knowledge base on what makes slides work, and the HTML slide template the other skills build on. | [Scott Cunningham](https://github.com/scunning1975/MixtapeTools) |

### Decisions

| Skill | What it does | Source |
|---|---|---|
| [premortem](premortem/) | Imagine the plan already failed, work backward to the most critical risks before committing. | [olelehmann1337](https://github.com/olelehmann1337/openclaw-share) |
