#!/usr/bin/env python3
"""borda.py — aggregate council peer-rankings into a Borda leaderboard.

Reads a JSON object on stdin:

    {
      "members": ["Gemini 3.1 Pro", "GPT-5.5", ...],   # index 0..N-1 == response number 1..N
      "rankings": [                                          # one per reviewing member
        [3, 1, 4, 2, 5],   # best-first list of response NUMBERS (1-based)
        [1, 3, 5, 2, 4],
        ...
      ]
    }

With N responses, a rank-1 vote scores N-1 points down to 0 for last place.
Reviewers rank blindly (responses are anonymised), so self-votes are expected
and counted — that is intended.

Prints the leaderboard (highest score first) as plain text, then a JSON line
`SCORES_JSON: {...}` mapping member name -> score for downstream use.
Malformed or partial rankings are skipped with a note to stderr; valid ones
still count.
"""
import json
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"borda.py: invalid JSON on stdin: {e}", file=sys.stderr)
        return 1

    members = data.get("members") or []
    rankings = data.get("rankings") or []
    n = len(members)
    if n == 0:
        print("borda.py: no members", file=sys.stderr)
        return 1

    scores = {i: 0 for i in range(n)}  # 0-based response index -> points
    counted = 0
    for k, ranking in enumerate(rankings):
        # Validate: must be a permutation-ish list of 1..n response numbers.
        nums = [r for r in ranking if isinstance(r, int) and 1 <= r <= n]
        seen = set(nums)
        if len(seen) < 2:
            print(f"borda.py: ranking {k} unusable, skipped", file=sys.stderr)
            continue
        for pos, r in enumerate(nums):
            if r in seen:
                scores[r - 1] += (n - 1 - pos)
                seen.discard(r)  # ignore later duplicates of the same response
        counted += 1

    board = sorted(range(n), key=lambda i: scores[i], reverse=True)
    print(f"Borda leaderboard ({counted}/{len(rankings)} rankings counted):")
    for rank, i in enumerate(board, 1):
        print(f"  {rank}. {members[i]} — {scores[i]} pts")

    named = {members[i]: scores[i] for i in range(n)}
    print("SCORES_JSON: " + json.dumps(named, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
