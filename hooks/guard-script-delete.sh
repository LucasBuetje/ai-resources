#!/usr/bin/env bash
# guard-script-delete.sh — Claude Code PreToolUse hook
# (matchers: Edit|Write|MultiEdit|NotebookEdit, and Bash).
#
# Why: on 2026-10-15 a test script Claude wrote ran its clean-up line with an empty
# variable — the delete-everything-under-a-folder line expanded to the whole disk — and
# wiped every folder the sandbox could write to. guard-rm.sh could not see it: a hook
# only sees `bash some_test.sh`, never what the script does. The user's decision: Claude
# never writes a deletion into a file. Removal is `mv <file> archive/`; a real deletion
# is a command Claude hands the user to run.
#
# What it checks:
#   - Edit/Write/MultiEdit/NotebookEdit on a script file: the NEW text only (an Edit's
#     new_string, a Write's content), so existing scripts can still be edited elsewhere.
#   - Bash: inline code that deletes without the shell's own delete command (find's delete flag,
#     python/R/perl one-liners). That command itself stays guard-rm.sh's job.
#
# Patterns are kept as character classes ([r]m, [u]nlink, …) so this file never matches
# itself. Contract: exit 2 blocks and shows stderr to Claude; any parse problem fails
# OPEN (exit 0) so the guard never wedges a session.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

tool=$(printf '%s' "$input" | jq -r '.tool_name // empty')

# Deletion calls in any language. Word-ish boundaries keep "form", "confirm", "alarm" out.
pat_lang='(^|[^[:alnum:]_.$-])[r]m(dir)?[[:space:]]|-[d]elete([[:space:]]|$)|[r]mtree|(^|[^[:alnum:]_])[u]nlink[[:space:]]*\(|(^|[^[:alnum:]_])[u]nlink[[:space:]]|os\.[r]emove|os\.[r]emovedirs|\.[u]nlink\(|file\.[r]emove|file_[d]elete|dir_[d]elete|[R]emove-Item|(^|[[:space:]])[e]rase[[:space:]]'

block() {
  cat >&2 <<EOF
Blocked: Claude does not write file deletions — not into scripts, not as inline code.
($1)

Instead:
  - retire a file with:   mv <file> archive/
  - leave temporary files in \$TMPDIR; the OS clears it
  - if something really must be deleted, give the user the exact command to run
    themselves, and say what it deletes.
EOF
  exit 2
}

case "$tool" in
  Bash)
    cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
    [ -n "$cmd" ] || exit 0
    # The shell's own delete command is guard-rm.sh's job; here only the other forms.
    pat_inline='-[d]elete([[:space:]]|$)|[r]mtree|[u]nlink[[:space:]]*\(|os\.[r]emove|\.[u]nlink\(|file\.[r]emove|file_[d]elete|dir_[d]elete|[R]emove-Item'
    printf '%s' "$cmd" | grep -Eq -- "$pat_inline" && block "inline deletion in a Bash command"
    exit 0
    ;;
  Edit|Write|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')
[ -n "$path" ] || exit 0

text=$(printf '%s' "$input" | jq -r '
  [ .tool_input.content, .tool_input.new_string, .tool_input.new_source,
    (.tool_input.edits // [] | .[].new_string) ] | map(select(. != null)) | join("\n")')
[ -n "$text" ] || exit 0

# Script files: by extension, or any file whose new text starts with a shebang.
base=$(basename "$path")
is_script=false
case "$base" in
  *.sh|*.bash|*.zsh|*.py|*.R|*.r|*.Rmd|*.qmd|*.do|*.ado|*.jl|*.js|*.mjs|*.ts|*.pl|*.rb|*.ipynb|Makefile|makefile|*.mk)
    is_script=true ;;
esac
printf '%s' "$text" | head -1 | grep -q '^#!' && is_script=true
[ "$is_script" = true ] || exit 0

hit=$(printf '%s\n' "$text" | grep -En -- "$pat_lang" | head -3)
[ -n "$hit" ] && block "in $base: $(printf '%s' "$hit" | tr '\n' ' ' | cut -c1-200)"
exit 0
