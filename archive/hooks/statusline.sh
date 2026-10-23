#!/bin/bash
# Status line: prompt-cache countdown for the main conversation.
#
# Reads the status-line JSON on stdin and prints one segment built from its
# `prompt_cache` object (Claude Code >= 2.1.251; `last_miss_cause` >= 2.1.260):
#   warm  → green  "cache ● 1h ████░░ 38m left · last turn 91% from cache · misses 0"
#           yellow once less than 20% of the TTL is left
#   cold  → red    "cache ○ cold · next message re-caches 82k tokens · cause ttl_expired_5m"
# The cache share is the last API call's (`context_window.current_usage`), not the
# session-wide `prompt_cache.hit_ratio`, which barely moves after a miss.
# Prints nothing until `prompt_cache` appears, and skips any field that is absent
# or null. `refreshInterval` in settings re-runs it so the countdown moves while idle.
# Field reference: https://code.claude.com/docs/en/statusline (Prompt cache fields).
# STATUSLINE_NOW (epoch seconds) overrides the clock, for scripts/test/test_statusline.sh.

input=$(cat)
now=${STATUSLINE_NOW:-$(date +%s)}

echo "$input" | jq -r --argjson now "$now" '
  (.context_window.current_usage // {}) as $u
  | (($u.input_tokens // 0) + ($u.cache_creation_input_tokens // 0) + ($u.cache_read_input_tokens // 0)) as $in
  | .prompt_cache // empty
  | . as $c
  | ({"5m": 300, "1h": 3600}[$c.ttl // ""]) as $ttl_s
  | (if $c.expires_at then $c.expires_at - $now else null end) as $left
  | ($c.warm == true and ($left == null or $left > 0)) as $warm

  # Optional trailing parts, each dropped when its field is absent.
  | ([ (if $in > 0 then "last turn \((($u.cache_read_input_tokens // 0) / $in * 100) | round)% from cache" else empty end),
       (if $c.misses    != null then "misses \($c.misses)"                 else empty end) ]) as $stats

  | if $warm then
      (if $ttl_s and $left then ([0, ([1, $left / $ttl_s] | min)] | max) else null end) as $frac
      | (if $frac != null and $frac < 0.2 then "\u001b[33m" else "\u001b[32m" end) as $col
      | (if $frac != null then ($frac * 6 | round) as $n
           | ([range(0; $n)] | map("█") | join("")) + ([range($n; 6)] | map("░") | join(""))
         else null end) as $bar
      | (if $left == null then null
         elif $left >= 3600 then "\($left / 3600 | floor)h \(($left % 3600) / 60 | floor)m left"
         elif $left >= 60   then "\($left / 60 | floor)m left"
         else "\($left | floor)s left" end) as $time
      | $col + ([ "cache ●", $c.ttl, $bar, $time ] | map(select(. != null)) | join(" "))
        + ($stats | map(" · " + .) | join("")) + "\u001b[0m"
    else
      (if $c.recache_tokens_if_cold != null
         then " · next message re-caches \(($c.recache_tokens_if_cold / 1000) | round)k tokens"
         else "" end) as $recache
      | ($c.last_miss_cause.causes // [] | join(", ")) as $cause
      | "\u001b[31mcache ○ cold" + $recache
        + (if $cause != "" then " · cause \($cause)" else "" end) + "\u001b[0m"
    end
'
