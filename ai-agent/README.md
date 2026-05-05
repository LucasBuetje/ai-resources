# AI Agent Skills — Installation Guide

Each folder in `skills/` is a skill for Claude Code or OpenCode. To install, copy it into the appropriate skills directory and invoke it with a slash command.

## Global Instructions

The global instructions file tells the agent how to behave across every project — things like never deleting files, not touching code you weren't asked to touch, etc. You set it up once and it applies everywhere. Note: For OpenCode, you need to rename the file to AGENTS.md

| Tool | File location |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` |

A minimal starting template is in [`ai-agent/CLAUDE.md`](CLAUDE.md). Copy it to the appropriate location and edit it — remove rules that don't fit your workflow, add your own.

---

## Structure

### Claude Code

```
~/.claude/
├── CLAUDE.md               ← global instructions (applies to all projects)
└── skills/
    ├── deck/
    │   ├── SKILL.md        ← skill instructions (Claude reads this)
    │   └── rhetoric.md     ← knowledge base (referenced by SKILL.md)
    ├── devils-advocate/
    │   └── SKILL.md
    ├── revise/
    │   └── SKILL.md
    ├── referee2/
    │   ├── SKILL.md
    │   └── preflight.md
    └── empirical-paper-summarizer/
        └── SKILL.md
```

### OpenCode

```
~/.config/opencode/
├── AGENTS.md               ← global instructions (applies to all projects)
└── commands/
    ├── deck/
    │   └── SKILL.md
    ├── devils-advocate/
    │   └── SKILL.md
    ├── revise/
    │   └── SKILL.md
    ├── referee2/
    │   ├── SKILL.md
    │   └── preflight.md
    └── empirical-paper-summarizer/
        └── SKILL.md
```



## Skills

| Folder | Command | Description |
|---|---|---|
| `deck/` | `/deck` | Build or edit Beamer presentations using the Rhetoric of Decks principles |
| `devils-advocate/` | `/devils-advocate` | Challenge a slide deck with 5–7 specific pedagogical questions |
| `referee2/` | `/referee2` | Full empirical research audit + cross-language replication |
| `revise/` | `/revise [report-path]` | Respond to referee comments interactively, one at a time |
| `empirical-paper-summarizer/` | `/summarize-paper [PDF]` | Extract and audit causal identification strategies from empirical economics papers |

## Notes

- The `deck/` skill requires `pdflatex` for compilation. Install via MacTeX: `brew install --cask mactex`.
- The `referee2/` skill requires Python 3 and R to be installed for cross-language replication.
- Skills reference files by path. For Claude Code: `~/.claude/skills/<name>/...`. For OpenCode: `~/.config/opencode/commands/<name>/...`. If you move a skill, update these references.
