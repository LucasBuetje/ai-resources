#!/usr/bin/env bash
# stop-log-reminder.sh — Claude Code Stop hook.
#
# Safety net for the Progress Log rule: nudge to update current.md when this
# session has edited project files that are not yet reflected in the log. It RE-ARMS after
# each log update, so a long session that logs early and keeps working still gets reminded
# about the later, still-unlogged changes — but it never nags on a turn that added no new
# edits.
#
# Session state comes from FILE MTIMES: any project file modified more recently than
# current.md is, by definition, an edit the log does not yet describe. This replaced a
# reader of log/ai-edits.jsonl (retired 2026-09-01) and is strictly better for the purpose:
# the old hook saw only Edit/Write/NotebookEdit tool calls, so in auto mode — where the
# model edits through Bash — it saw nothing at all. An mtime does not care which tool wrote
# the bytes.
#
# "Unlogged" = at least one file under the project, excluding the log itself and the usual
# machine noise, is newer than current.md.
#
# Loop protection (critical for Stop hooks):
#   - bail if this stop is itself a continuation of a prior stop hook (stop_hook_active).
#   - a marker file records the newest edit mtime seen at the last nudge; we only nudge
#     again once something newer appears. Bringing the log current makes current.md the
#     newest file, which empties the list and clears the marker, re-arming the next window.
#
# Cost: fires on every turn-end, so the scan is one `find -newer` bounded to a few dirs and
# pruned hard. Contract: {"decision":"block","reason":...} keeps the turn going. Any
# problem → allow.

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

# The log itself: root location first, pre-move log/current.md as fallback.
if [ -f "$root/current.md" ]; then
  logfile="$root/current.md"
elif [ -f "$root/log/current.md" ]; then
  logfile="$root/log/current.md"
else
  exit 0   # no progress log in this project → nothing to nudge about
fi

marker="${TMPDIR:-/tmp}/claude-logcheck-${session}"

# Per-project extra ignores: one filename glob per line in .claude/logcheck-ignore, '#'
# comments allowed. For files a TOOL rewrites as a side effect of unrelated work — the
# classic being a Better BibTeX auto-export, which Zotero rewrites on every library change,
# so adding a single reference would otherwise nudge about a .bib nobody edited. Kept
# per-project because the offending filenames are project-specific and this hook is global.
ignore_args=()
if [ -f "$root/.claude/logcheck-ignore" ]; then
  while IFS= read -r pat; do
    case "$pat" in ''|'#'*) continue ;; esac
    ignore_args+=( ! -name "$pat" )
  done < "$root/.claude/logcheck-ignore"
fi

# Files newer than the log. Prune the noise that would otherwise nudge on every turn: VCS
# internals, dependency and build trees, caches, worktrees, and the log's own siblings.
# GENERATED artifacts are excluded by extension — a pdflatex+biber run rewrites the whole
# .aux/.bcf/.log/.out/.run.xml/.synctex.gz set at once, and none of it is work to describe.
scan() {  # $1 = -print or -print0
  find "$root" \
    \( -name .git -o -name .venv -o -name venv -o -name node_modules -o -name build \
       -o -name .apply-state -o -name __pycache__ -o -name .Rproj.user -o -name renv \
       -o -name pdf_reads -o -name obsidian -o -name worktrees \) -prune -o \
    -type f -newer "$logfile" \
    ! -name '.DS_Store' ! -name '*.swp' ! -name '*.tmp' ! -name '.*.sw?' \
    ! -name '*.aux' ! -name '*.bcf' ! -name '*.blg' ! -name '*.out' ! -name '*.log' \
    ! -name '*.run.xml' ! -name '*.synctex.gz' ! -name '*.fls' ! -name '*.fdb_latexmk' \
    ! -name '*.toc' ! -name '*.nav' ! -name '*.snm' ! -name '*.vrb' \
    "${ignore_args[@]}" \
    "$1" 2>/dev/null
}

files=$(scan -print | sed "s|^$root/||" | sort -u | head -8 | paste -sd ', ' -)

# Log is current → reset the marker so the next unlogged window re-arms, then allow.
if [ -z "$files" ]; then
  rm -f "$marker" 2>/dev/null
  exit 0
fi

# sig: the newest edit mtime seen this turn (a monotonic cursor for dedup). Must use the
# SAME scan as $files — if this one saw a file the list does not, the hook would nudge about
# an empty change set and never settle.
sig=$(scan -print0 | xargs -0 stat -f %m 2>/dev/null | sort -n | tail -1)
case "$sig" in ''|*[!0-9]*) exit 0 ;; esac

# Nudge only if something has been edited since the last nudge — otherwise this is a
# no-new-work turn and we stay silent.
last=$(cat "$marker" 2>/dev/null || echo 0)
case "$last" in ''|*[!0-9]*) last=0 ;; esac
[ "$sig" -gt "$last" ] || exit 0

printf '%s' "$sig" > "$marker" 2>/dev/null

jq -n --arg files "$files" '{
  decision: "block",
  reason: ("Progress Log rule: these files changed since current.md was last updated (" + $files + "). This is an MTIME check, so it does NOT establish that you wrote them - a build, a sync, or another tool may have. Log only the work YOU actually did this turn, and if none of it is yours, say so in one line instead of inventing an entry. Otherwise append a brief entry now (what changed, why, any open questions). IMPORTANT: your previous reply was already delivered to the user — do NOT repeat, re-summarize, or rephrase any of it. After the log edit, end the turn with no new text at all (an empty reply is the expected outcome); only if the log edit itself surfaced something genuinely new may you add a single short line. If the changes were trivial or the log is already current, take no action and add nothing.")
}'
exit 0
