# Hooks

Small scripts the agent tool runs automatically at set moments — *before* a command, *before* a read, at session start. Your conventions, enforced by code instead of trust.

- These are Claude Code hooks. Each reads a JSON event on stdin and signals back via exit code / stdout.
- They're a menu — take the ones that fit your workflow and adapt the rest.
- All are written to **fail open**: any parse problem or missing dependency just lets the session proceed, so a hook can never wedge you.

## The hooks

- **`guard-rm.sh`** — *PreToolUse (Bash).* Blocks `rm` on project files and tells the agent to `mv <file> archive/` instead. Allows genuinely disposable targets (temp dirs, caches, build output, `git rm`). A footgun-catcher, not a security boundary.
- **`warn-pdf-mainthread.sh`** — *PreToolUse (Read).* Non-blocking warning when reading a `.pdf`: page images loaded in the main thread accumulate and can make a session unrecoverable. Suggests a subagent / `/summarize-paper` for research papers; lets slides and notes through.
- **`session-start-current-log.sh`** — *SessionStart.* Reads `current.md` from the project root (falling back to the older `log/current.md`) and injects it into context, so the agent always opens with the working memory from last session. (Pairs with the memory-log pattern — see [`../memory-log/`](../memory-log/).)
- **`guard-script-delete.sh`** — *PreToolUse (Edit/Write and Bash).* Blocks file-deletion calls in any language (find's delete flag, Python's tree and file removal, R's unlink, …) in new script text and in inline one-liners. Written after a test script's clean-up line ran with an empty variable and wiped every folder the session could write to — `guard-rm.sh` only ever saw `bash test.sh`.
- **`guard-pip-venv.sh`** — *PreToolUse (Bash).* Blocks `pip install` with no venv activated in the same command, and always blocks `sudo pip` / `pip --user`.
- **`stop-log-reminder.sh`** — *Stop.* If project files changed since `current.md` was last updated, asks the agent to log what it did (and only what it did). Re-arms after each log update; never nags on a turn with no new edits.
- **`econ-write-reminder.sh`** — *PreToolUse (Edit/Write) and UserPromptSubmit.* Once per session, on the first paper `.tex` edit or a prompt about paper prose, tells the agent to load [`/econ-write`](../skills/econ-write/) first.
- **`writing-great-skills-reminder.sh`** — *PreToolUse (Edit/Write).* The same pattern for the first `SKILL.md` edit of a session and [`/writing-great-skills`](../skills/writing-great-skills/).
- **`statusline.sh`** — *Status line, not a hook.* Shows the prompt cache as a countdown: warm with the time left and the last turn's cache share, or cold with what the next message will re-cache. Needs Claude Code 2.1.251+.

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
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "~/.claude/hooks/guard-script-delete.sh", "timeout": 10 } ] },
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "~/.claude/hooks/guard-pip-venv.sh", "timeout": 10 } ] },
      { "matcher": "Read", "hooks": [ { "type": "command", "command": "~/.claude/hooks/warn-pdf-mainthread.sh", "timeout": 10 } ] },
      { "matcher": "Edit|Write|MultiEdit|NotebookEdit", "hooks": [
        { "type": "command", "command": "~/.claude/hooks/guard-script-delete.sh", "timeout": 10 },
        { "type": "command", "command": "~/.claude/hooks/econ-write-reminder.sh", "timeout": 10 },
        { "type": "command", "command": "~/.claude/hooks/writing-great-skills-reminder.sh", "timeout": 10 } ] }
    ],
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "~/.claude/hooks/econ-write-reminder.sh", "timeout": 10 } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "~/.claude/hooks/stop-log-reminder.sh", "timeout": 10 } ] }
    ]
  },
  "statusLine": { "type": "command", "command": "~/.claude/hooks/statusline.sh", "refreshInterval": 30 }
}
```

- `guard-rm.sh` enforces the same "move to `archive/`, never delete" rule shown in the [`../claude-md/`](../claude-md/) example — the hook backs the instruction with code.
