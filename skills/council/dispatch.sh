#!/usr/bin/env bash
# dispatch.sh — fan one prompt out to all three external council members IN PARALLEL.
#
# Usage: dispatch.sh <promptfile> <outdir>
#
# Runs the three CLI members concurrently (background + wait) so parallelism does
# NOT depend on the orchestrator batching tool calls, and costs a single
# permission prompt instead of three. Writes one answer file per member:
#   <outdir>/{gemini,openai,mistral}.txt
# An empty file means that member's CLI failed → treat it as unavailable.
# The Claude Sonnet member is NOT here — it runs as a native subagent in parallel
# with this script (spawn it in the same orchestrator message).
set -uo pipefail

promptfile="${1:?usage: dispatch.sh <promptfile> <outdir>}"
outdir="${2:?usage: dispatch.sh <promptfile> <outdir>}"
mkdir -p "$outdir"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Per-member wall-clock cap (seconds). Members run in parallel, so the slowest
# sets the floor — vibe (mistral, thinking=high) is the long pole, observed
# anywhere from ~20s to >110s. A CLI that exceeds the cap is killed and leaves an
# empty file → treated as unavailable (graceful degradation). perl provides the
# timeout since macOS has no `timeout`; the alarm survives the exec into bash.
TIMEOUT="${COUNCIL_TIMEOUT:-180}"
run() {
  perl -e 'alarm shift; exec @ARGV' "$TIMEOUT" \
    bash "$here/ask_member.sh" "$1" "$2" "$promptfile" > "$outdir/$3.txt" 2>/dev/null
}

run agy   "Gemini 3.1 Pro (High)"  gemini  &
run codex "gpt-5.5"                 openai  &
run vibe  "mistral-medium-3.5"      mistral &
wait

for k in gemini openai mistral; do
  if [ -s "$outdir/$k.txt" ]; then echo "OK    $k"; else echo "EMPTY $k (unavailable)"; fi
done
