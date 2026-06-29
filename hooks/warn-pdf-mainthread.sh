#!/usr/bin/env bash
# warn-pdf-mainthread.sh — Claude Code PreToolUse hook (matcher: Read).
#
# Soft guard for the PDF Reading rule (Rule #21): reading a PDF with the Read tool in
# the main thread renders page images that accumulate permanently and can make a
# session unrecoverable. A hook can't tell a research paper (must go via /summarize-paper
# or a subagent) from a syllabus/slides/notes (fine to read directly) — so this WARNS
# rather than blocks, and lets the read proceed.
#
# Contract: non-blocking. Emit hookSpecificOutput.additionalContext (reaches Claude),
# exit 0 so the Read still runs. Any parse problem → silent allow.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')
[ -n "$path" ] || exit 0

# Only PDFs.
case "$path" in
  *.pdf|*.PDF) : ;;
  *) exit 0 ;;
esac

jq -n '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    additionalContext: "PDF Reading rule (Rule #21): reading a PDF in the main thread loads page images that persist for the whole session. If this is a RESEARCH PAPER, stop and use /summarize-paper (whole-paper summary) or a Sonnet/Opus subagent for a targeted read — never read a paper PDF in the main thread. If it is slides, a syllabus, lecture notes, or a report, reading directly here is fine; proceed."
  }
}'
exit 0
