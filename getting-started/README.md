# Getting started

Pick a tool, install it, point it at a project folder. Then come back to the [main README](../README.md) for how I actually use it.

## Which tool?

- **[Claude Code](https://claude.ai/code)** — what I mainly use. Frontier Claude models, paid (subscription or API).
- **[OpenCode](https://opencode.ai) + GWDG** — free, open-source; point it at any model API. I use the models from the GWDG (German Academic Cloud). Open-weight models, less capable but very good and improving.

| | [Claude Code](https://claude.ai/code) | [OpenCode](https://opencode.ai) + GWDG |
|---|---|---|
| Cost | Subscription or API usage | Free for GWDG/Academic Cloud users |
| Models | Claude (Anthropic) — frontier models | open-weight models — less capable, still very good |
| Data handling | Anthropic's privacy policy | Processed on GWDG servers in Germany |
| Open source | No | Yes (MIT) |
| Global instruction file | `~/.claude/CLAUDE.md` | `~/.config/opencode/AGENTS.md` |
| Project instruction file | `CLAUDE.md` | `CLAUDE.md` (both tools read it) |
| Skills | `~/.claude/skills/` | `~/.config/opencode/commands/` |

## Setup guides

- **OpenCode + GWDG** (Mac & Windows, credentials, model choice, common issues): [`gwdg-opencode-setup.md`](gwdg-opencode-setup.md)
- **Claude Code:** install per [the official docs](https://claude.ai/code), then drop an [example `CLAUDE.md`](../claude-md/) into `~/.claude/`, copy the [skills](../skills/) you want into `~/.claude/skills/`, and wire any [hooks](../hooks/) you want in `~/.claude/settings.json`.
