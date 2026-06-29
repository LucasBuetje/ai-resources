# Hooks

Small scripts the agent tool runs automatically at set moments — *before* a command, *before* a read, at session start, when it tries to stop. Your conventions, enforced by code instead of trust.

- These are Claude Code hooks. Each reads a JSON event on stdin and signals back via exit code / stdout.
- They're a menu — take the ones that fit your workflow and adapt the rest.
- All four are written to **fail open**: any parse problem or missing dependency just lets the session proceed, so a hook can never wedge you.

## The hooks

- **`guard-rm.sh`** — *PreToolUse (Bash).* Blocks `rm` on project files and tells the agent to `mv <file> archive/` instead. Allows genuinely disposable targets (temp dirs, caches, build output, `git rm`). A footgun-catcher, not a security boundary.
- **`warn-pdf-mainthread.sh`** — *PreToolUse (Read).* Non-blocking warning when reading a `.pdf`: page images loaded in the main thread accumulate and can make a session unrecoverable. Suggests a subagent / `/summarize-paper` for research papers; lets slides and notes through.
- **`session-start-current-log.sh`** — *SessionStart.* Reads `log/current.md` and injects it into context, so the agent always opens with the working memory from last session. (Pairs with the memory-log pattern — see [`../memory-log/`](../memory-log/).)
- **`stop-log-reminder.sh`** — *Stop.* If the session edited files but never touched `log/current.md`, nudges once before the turn ends. Fires at most once per session.

## Dependency note

- `stop-log-reminder.sh` figures out what was edited this session by reading `log/ai-edits.jsonl` — a file written by a **separate** `log-ai-edit.sh` PostToolUse hook that is *not* shipped here. Without that hook, `ai-edits.jsonl` never exists and `stop-log-reminder.sh` simply does nothing (it exits early). If you want the stop reminder to actually fire, you need an edit-logging hook that appends edited file paths (with a `session` field) to `log/ai-edits.jsonl`.

## Wiring (`~/.claude/settings.json`)

Copy the scripts to `~/.claude/hooks/` (`chmod +x` them), then register:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "~/.claude/hooks/session-start-current-log.sh", "timeout": 10 } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "~/.claude/hooks/guard-rm.sh", "timeout": 10 } ] },
      { "matcher": "Read", "hooks": [ { "type": "command", "command": "~/.claude/hooks/warn-pdf-mainthread.sh", "timeout": 10 } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "~/.claude/hooks/stop-log-reminder.sh", "timeout": 10 } ] }
    ]
  }
}
```

- `guard-rm.sh` enforces the same "move to `archive/`, never delete" rule shipped in [`../claude-md/global-CLAUDE.md`](../claude-md/global-CLAUDE.md) — the hook backs the instruction with code.
