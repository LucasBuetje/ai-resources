#!/bin/bash
# econ-write-reminder.sh — Claude Code hook, two entry points.
#
#   PreToolUse (Edit|Write|MultiEdit): fires on the FIRST edit to a paper .tex file in a
#   session and blocks that one call with a reminder to invoke /econ-write. Exit 2 feeds
#   stderr back to Claude, which invokes the skill and retries the edit.
#
#   UserPromptSubmit: fires on the FIRST prompt of a session that reads as paper-prose work
#   and injects the same reminder as context. Non-blocking (exit 0 + stdout). The match is
#   three-way (strong / weak+context / negative) — see the case body for why a bare prose
#   keyword is not enough.
#
# Both are once per session (marker keyed by session id) and share one marker, so a prompt
# that already triggered it will not re-fire on the subsequent edit. Decks are excluded
# (the /deck skill owns those); preamble.tex is excluded (packages, not prose).
# Fails OPEN on any parse problem — a reminder must never wedge an edit.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

session_id=$(printf '%s' "$input" | jq -r '.session_id // "nosession"')
event=$(printf '%s' "$input" | jq -r '.hook_event_name // empty')
marker="${TMPDIR:-/tmp}/claude-econ-write-reminder-${session_id}"

reminder='Paper prose (global rule): this touches economics paper writing, so invoke the
/econ-write skill before drafting, rewriting, reviewing or restructuring the text —
it carries the synthesized guidance (Cochrane, McCloskey, Shapiro, Head, Bellemare)
and is a fixer on execution but an examiner on judgment. If the project CLAUDE.md
reserves narrative prose for the user, follow it: propose wording in chat and ask
before writing sentences into the manuscript. This reminder fires once per session.'

case "$event" in
  UserPromptSubmit)
    [ -f "$marker" ] && exit 0
    prompt=$(printf '%s' "$input" | jq -r '.prompt // empty' | tr '[:upper:]' '[:lower:]')

    # Three-way match. A bare prose word is NOT enough: "draft", "prose" and "wording" are
    # everyday vocabulary in code and config work (this repo calls its own sources drafts),
    # and matching them alone fired the reminder on prompts like "add it as drafted".
    #
    #   STRONG  — names a paper outright; fires on its own.
    #   WEAK    — prose vocabulary; fires only alongside a CONTEXT word.
    #   NEG     — tooling/config vocabulary; suppresses everything.
    strong='(the|my|our|this) paper|manuscript|literature review|job market paper|\bjmp\b|referee (report|comment)|reviewer (report|comment)|response to referees'
    weak='draft|prose|wording|phrasing|abstract|introduction|the intro|conclusion|discussion section|results section|write.?up|writeup|paragraph'
    context='paper|manuscript|chapter|thesis|dissertation|article|journal|submission|\.tex|latex|seminar|co.?author|referee|reviewer'
    neg='claude\.md|agents\.md|\bskill|\bhook|settings\.json|instruction|recipe|\bcommit|apply\.sh|build\.sh|\bregex|\brepo\b|\.sh\b|\bconfig'

    if printf '%s' "$prompt" | grep -Eq "$neg"; then
      exit 0
    fi
    if printf '%s' "$prompt" | grep -Eq "$strong" ||
       { printf '%s' "$prompt" | grep -Eq "$weak" && printf '%s' "$prompt" | grep -Eq "$context"; }; then
      touch "$marker"
      printf '%s\n' "$reminder"
    fi
    exit 0
    ;;
esac

# PreToolUse path
file_path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty')

case "$file_path" in
  */project_state_decks/*) exit 0 ;;
  */preamble.tex) exit 0 ;;
  *.tex) ;;
  *) exit 0 ;;
esac

[ -f "$marker" ] && exit 0
touch "$marker"

printf '%s\n' "$reminder" >&2
exit 2
