#!/usr/bin/env bash
# stop-log-reminder.sh — Claude Code Stop hook.
#
# Safety net for the Progress Log rule (Rule #4): if this session edited project files
# but never touched log/current.md, nudge once before the turn ends so the working
# memory doesn't silently fall behind. The model still writes the entry — this only
# reminds.
#
# Session state comes for free from log/ai-edits.jsonl (written by the AI-edit log
# hook): rows tagged with this session_id tell us what was edited. If none of them is
# log/current.md, we block the stop once with a reminder.
#
# Loop protection (critical for Stop hooks): fire at most once per session via a marker
# file, and bail immediately if this stop is itself a continuation of a prior stop hook.
# Contract: {"decision":"block","reason":...} keeps the turn going. Any problem → allow.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

# Don't re-trigger on a stop that the hook itself caused.
active=$(printf '%s' "$input" | jq -r '.stop_hook_active // false')
[ "$active" = "true" ] && exit 0

cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
session=$(printf '%s' "$input" | jq -r '.session_id // empty')
[ -n "$cwd" ] && [ -n "$session" ] || exit 0

root=$(cd "$cwd" 2>/dev/null && pwd -P) || exit 0
[ -f "$root/CLAUDE.md" ] || [ -d "$root/log" ] || exit 0

logfile="$root/log/ai-edits.jsonl"
[ -f "$logfile" ] || exit 0

# Fire at most once per session.
marker="${TMPDIR:-/tmp}/claude-logcheck-${session}"
[ -e "$marker" ] && exit 0

# Edits made by THIS session.
edits=$(jq -r --arg s "$session" 'select(.session==$s) | .file' "$logfile" 2>/dev/null)
[ -n "$edits" ] || exit 0   # nothing edited this session → nothing to log

# If log/current.md was among them, the log was updated → fine.
printf '%s\n' "$edits" | grep -qx 'log/current.md' && exit 0

# Otherwise: nudge once.
: > "$marker" 2>/dev/null

files=$(printf '%s\n' "$edits" | grep -vx 'log/ai-edits.jsonl' | sort -u | head -8 | paste -sd ', ' -)
jq -n --arg files "$files" '{
  decision: "block",
  reason: ("Progress Log rule (Rule #4): this session edited files (" + $files + ") but did not update log/current.md. Append a brief entry now (what changed, why, any open questions). If the changes were trivial or the log is already current via a manual edit, say so in one line and stop — this reminder fires only once per session.")
}'
exit 0
