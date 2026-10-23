#!/usr/bin/env bash
# guard-pip-venv.sh — Claude Code PreToolUse hook (matcher: Bash).
#
# Enforces the Python Virtual Environments rule: never `pip install` outside a venv,
# and never `pip install --user` / `sudo pip install`.
#
# In this harness shell state does NOT persist between Bash calls, so a venv must be
# activated in the SAME command as the install (e.g. `source .venv/bin/activate && pip
# install ...`) or the install must target a venv pip directly (`.venv/bin/pip ...`).
# The hook therefore inspects the single command string for an in-line venv signal.
#
# Contract: exit 2 blocks and shows stderr to Claude. Parse problems fail OPEN.

input=$(cat)
command -v jq >/dev/null 2>&1 || exit 0

cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
[ -n "$cmd" ] || exit 0

# Only care about pip installs (pip / pip3 / python -m pip).
printf '%s' "$cmd" | grep -Eq '(^|[;&|[:space:]])(pip3?|python3?[[:space:]]+-m[[:space:]]+pip)[[:space:]]+install' || exit 0

# Always wrong, regardless of venv:
if printf '%s' "$cmd" | grep -Eq 'sudo[[:space:]]+(-[A-Za-z]+[[:space:]]+)*pip'; then
  echo "Blocked (Rule: Python venvs): never use 'sudo pip install'. Create/activate a venv and install there." >&2
  exit 2
fi
if printf '%s' "$cmd" | grep -Eq 'pip3?[[:space:]]+install[^|;&]*--user'; then
  echo "Blocked (Rule: Python venvs): never use 'pip install --user'. Create/activate a venv and install there." >&2
  exit 2
fi

# A venv signal present in the same command (or the hook's own env) is sufficient.
if [ -n "$VIRTUAL_ENV" ]; then exit 0; fi
if printf '%s' "$cmd" | grep -Eq 'activate|\.venv/bin/pip|venv/bin/pip|VIRTUAL_ENV=|uv[[:space:]]+(pip|add)|poetry[[:space:]]+(add|install)|conda[[:space:]]+install|pipx[[:space:]]+install'; then
  exit 0
fi

cat >&2 <<EOF
Blocked by the Python Virtual Environments rule: \`pip install\` with no active venv.
Homebrew Python rejects/pollutes global installs, and shell state does not persist
between commands here — so activate the venv in the SAME command:

    python3 -m venv .venv && source .venv/bin/activate && pip install <pkg>
    # or, if .venv already exists:
    source .venv/bin/activate && pip install <pkg>

Command was:
    $cmd
EOF
exit 2
