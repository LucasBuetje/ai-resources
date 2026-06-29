# Hooks

Small scripts the agent tool runs automatically at set moments — *before* a command, *before* a read, at session start. Your conventions, enforced by code instead of trust.

- These are Claude Code hooks. Each reads a JSON event on stdin and signals back via exit code / stdout.
- They're a menu — take the ones that fit your workflow and adapt the rest.
- All are written to **fail open**: any parse problem or missing dependency just lets the session proceed, so a hook can never wedge you.

## The hooks

- **`guard-rm.sh`** — *PreToolUse (Bash).* Blocks `rm` on project files and tells the agent to `mv <file> archive/` instead. Allows genuinely disposable targets (temp dirs, caches, build output, `git rm`). A footgun-catcher, not a security boundary.
- **`warn-pdf-mainthread.sh`** — *PreToolUse (Read).* Non-blocking warning when reading a `.pdf`: page images loaded in the main thread accumulate and can make a session unrecoverable. Suggests a subagent / `/summarize-paper` for research papers; lets slides and notes through.
- **`session-start-current-log.sh`** — *SessionStart.* Reads `log/current.md` and injects it into context, so the agent always opens with the working memory from last session. (Pairs with the memory-log pattern — see [`../memory-log/`](../memory-log/).)

## Wiring (`~/.claude/settings.json`)

- **Easiest — just ask the agent.** Point it at this repo and say *"install the `guard-rm` and `session-start` hooks and wire them into my settings.json"* — it copies the scripts, makes them executable, and adds the config.
- **Manual:** copy the scripts to `~/.claude/hooks/` (`chmod +x` them), then register:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command", "command": "~/.claude/hooks/session-start-current-log.sh", "timeout": 10 } ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "~/.claude/hooks/guard-rm.sh", "timeout": 10 } ] },
      { "matcher": "Read", "hooks": [ { "type": "command", "command": "~/.claude/hooks/warn-pdf-mainthread.sh", "timeout": 10 } ] }
    ]
  }
}
```

- `guard-rm.sh` enforces the same "move to `archive/`, never delete" rule shown in the [`../claude-md/`](../claude-md/) example — the hook backs the instruction with code.
