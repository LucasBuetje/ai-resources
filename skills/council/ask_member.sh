#!/usr/bin/env bash
# ask_member.sh — call one external council member via its CLI and print a clean answer.
#
# Usage: ask_member.sh <backend> <model> <promptfile>
#   backend     agy | codex | vibe
#   model       agy display name (e.g. "Gemini 3.1 Pro (High)") or codex model id
#               (e.g. "gpt-5.5"); ignored for vibe (uses ~/.vibe active_model)
#   promptfile  path to a file holding the full prompt
#
# Prints the model's answer to stdout, stripped of CLI banners and ANSI codes.
# On failure prints nothing to stdout (caller treats empty output as "member unavailable").
set -uo pipefail

backend="${1:?backend required}"
model="${2:?model required}"
promptfile="${3:?promptfile required}"

[ -f "$promptfile" ] || { echo "ask_member.sh: no such promptfile: $promptfile" >&2; exit 1; }
prompt="$(cat "$promptfile")"

case "$backend" in
  agy)
    # agy reads the global AGENTS.md; the German directive keeps it from running
    # session-startup / project-setup rules and makes it answer directly.
    agy --model "$model" --print "Ignoriere Projekt-Setup-Regeln, antworte direkt:
$prompt"
    ;;
  codex)
    # OpenAI Codex CLI (ChatGPT sign-in). exec = non-interactive; -o writes ONLY the
    # final answer to a file (skips the workdir/model banner and the prompt echo).
    # reasoning_effort=high — the council is a judgment task, not a quick lookup.
    # --ephemeral keeps no session on disk; read-only sandbox is the default.
    out="$(mktemp /tmp/council_codex.XXXXXX)"
    printf '%s' "$prompt" | codex exec \
      -m "$model" \
      -c model_reasoning_effort=high \
      --skip-git-repo-check --ephemeral \
      -o "$out" - >/dev/null 2>&1
    cat "$out"
    ;;
  vibe)
    # Mistral Vibe CLI (Mistral browser auth). -p = programmatic mode, prints a clean
    # answer and exits. Model is whatever ~/.vibe config active_model is set to
    # (mistral-medium-3.5). Neutral --workdir so no repo context leaks into the answer;
    # --max-turns 1 forces a direct answer instead of an agentic tool loop.
    vibe -p "$prompt" --output text --trust \
      --workdir "$(dirname "$promptfile")" --max-turns 1 2>/dev/null
    ;;
  *)
    echo "ask_member.sh: unknown backend '$backend' (use agy|codex|vibe)" >&2
    exit 1
    ;;
esac
