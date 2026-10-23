#!/bin/bash
# writing-great-skills-reminder.sh — Claude Code PreToolUse hook (matcher: Edit|Write|MultiEdit).
#
# Fires on the FIRST Edit/Write to a SKILL.md file in a session and blocks that one call
# with a reminder to invoke the /writing-great-skills skill (invocation choice, description
# writing, information hierarchy, splitting) before authoring or editing skill content. All
# later SKILL.md edits in the same session pass through silently (marker file keyed by
# session id). Non-SKILL.md edits always pass through.
# Fails OPEN on any parse problem — a reminder must never wedge an edit.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')
session_id=$(printf '%s' "$input" | jq -r '.session_id // "nosession"')

case "$file_path" in
  */SKILL.md|SKILL.md) ;;
  *) exit 0 ;;
esac

marker="${TMPDIR:-/tmp}/claude-writing-great-skills-reminder-${session_id}"

[ -f "$marker" ] && exit 0
touch "$marker"

cat >&2 << 'EOF'
Skill authoring (global rule): before writing or editing a SKILL.md, invoke the
/writing-great-skills skill — invocation choice (model- vs user-invoked), how to write a
model-facing description with trigger phrasing, the steps-vs-reference information
hierarchy, progressive disclosure, and when to split a skill in two. If you have already
invoked it this session, simply retry this edit; it will pass through. This reminder fires
once per session.
EOF
exit 2
