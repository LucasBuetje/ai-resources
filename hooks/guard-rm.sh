#!/usr/bin/env bash
# guard-rm.sh — Claude Code PreToolUse hook (matcher: Bash).
#
# Enforces the File Preservation rule: "Never rm a file — mv to archive is the only
# permitted removal." Blocks Bash commands that invoke `rm` on project files, telling
# Claude to `mv` to archive/ instead.
#
# Heuristic, not a security boundary — it catches the common "rm myfile.tex" footgun
# while letting genuinely disposable targets through (temp dirs, caches, build output,
# dependency trees). `git rm` is allowed (VCS-tracked, recoverable from history).
#
# Contract: exit 2 blocks the tool call and shows stderr to Claude. Any parse problem
# fails OPEN (exit 0, allow) so the guard never wedges the session.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
[ -n "$cmd" ] || exit 0

# Detect `rm` at a COMMAND position only: line start, or right after a shell
# operator/separator (; & | ( {), optionally with whitespace, optionally via sudo.
# Also catch `xargs ... rm`. This deliberately does NOT match rm in ARGUMENT position
# — `grep rm file` (rm is a search string) or `git rm` (git is the command, and git rm
# is recoverable from history) — to avoid false positives.
is_rm=false
printf '%s' "$cmd" | grep -Eq '(^|[;&|({])[[:space:]]*(sudo[[:space:]]+)?rm([[:space:]]|$)' && is_rm=true
printf '%s' "$cmd" | grep -Eq 'xargs([[:space:]]+-[^[:space:]]+)*[[:space:]]+rm([[:space:]]|$)' && is_rm=true
[ "$is_rm" = true ] || exit 0

# Allowlist: if the command references a clearly disposable target, let it through.
# (Crude — a command mixing disposable and real targets would slip; that's acceptable
# for a preservation nudge, not a hard security control.)
disposable='/tmp/|/private/tmp/|/var/folders/|node_modules|__pycache__|\.venv|/\.git/|\.pyc|\.DS_Store|\.pytest_cache|\.mypy_cache|\.ipynb_checkpoints|/build/|/dist/|\.cache|\.aux|\.log|\.out|\.toc|\.synctex'
printf '%s' "$cmd" | grep -Eq "$disposable" && exit 0

# Otherwise: block.
cat >&2 <<EOF
Blocked by File Preservation rule (Rule #1): this command uses \`rm\`.
Never delete project files — move them to an archive/ subfolder instead:

    mv <file> archive/

Command was:
    $cmd

If the target is genuinely disposable (a temp file, cache, build artifact, or
dependency tree), it likely matched the allowlist already — if it didn't, rephrase
to point at a /tmp path, or tell the user why a real deletion is needed.
EOF
exit 2
