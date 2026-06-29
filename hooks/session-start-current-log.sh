#!/usr/bin/env bash
# session-start-current-log.sh — Claude Code SessionStart hook.
#
# Guarantees the Session Startup rule: at the start of every session, inject the
# project's log/current.md into context so the working memory is always present,
# instead of relying on the model to remember to read it. The model still does the
# summarising — this just makes the file unconditionally available.
#
# Fires on SessionStart. Reads <cwd>/log/current.md (if the cwd is a set-up project)
# and emits its contents as plain text on stdout, which Claude Code adds to the
# session context. Always exits 0; never blocks a session.

input=$(cat)

command -v jq >/dev/null 2>&1 || exit 0

cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
[ -n "$cwd" ] || exit 0

root=$(cd "$cwd" 2>/dev/null && pwd -P) || exit 0

# Only act in folders set up as projects (same gate as the AI-edit log hook).
[ -f "$root/CLAUDE.md" ] || [ -d "$root/log" ] || exit 0

log="$root/log/current.md"
[ -f "$log" ] || exit 0

# Skip if effectively empty (whitespace only).
[ -s "$log" ] || exit 0
grep -q '[^[:space:]]' "$log" || exit 0

printf '%s\n' "=== Project working memory — log/current.md (injected by SessionStart hook) ==="
printf '%s\n' "Summarise to the user what was in progress, then proceed with their request."
printf '%s\n' "---"
cat "$log"

exit 0
