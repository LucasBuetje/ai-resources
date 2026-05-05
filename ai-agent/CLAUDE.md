# Global Claude Instructions

These rules apply to every project. Project-specific rules go in the project's local `CLAUDE.md`.

---

## File Safety

Never delete files — move them to an `archive/` subfolder instead:

```bash
mv file.md archive/
```

Never use `rm` on project files. If something needs to be cleared out, `mv` it to `archive/` first.

---

## Scope Boundary

Never navigate above the current project's root folder. If external files are needed, ask the user to copy them in.

---

## Surgical Editing

When editing existing code, LaTeX, or prose:

- Don't improve or refactor things that weren't part of the request
- Don't clean up adjacent code, comments, or formatting
- Match the existing style, even if you'd do it differently
- Every changed line should trace directly to what was asked

When a task has multiple valid interpretations, present them — don't pick silently.

---

## Capture Conventions

When the user establishes a new rule or preference during a session, write it to the local `CLAUDE.md` immediately — not at the end of the session.

---

## Auto Mode Scope

Auto mode grants file-editing permissions, not decision-making authority.

- Run commands and edit files without asking at each step
- When a decision has multiple valid outcomes, surface the options and wait for explicit approval — even in auto mode

---

## Clean Working Files

Don't pre-fill files with instructional scaffolding the user then has to delete:

- No `# TODO: fill in X` comments
- No "example" placeholder blocks
- Leave new files empty, or with only the minimum real content that belongs there

