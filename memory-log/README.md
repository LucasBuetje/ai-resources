# Memory: a running log across sessions

Models forget everything between sessions. One working-memory file, maintained by the agent, fixes that. (A habit adopted from Scott Cunningham.)

- Keep one file per project: `log/current.md`.
- **As the agent works:** it appends short entries — what changed, why, what's still open.
- **At the next session start:** the file is read back in (a [SessionStart hook](../hooks/) makes this automatic), so it resumes where you stopped instead of starting cold.
- **Say "log":** archive `current.md` to a timestamped file (`log/YYYY-MM-DD_HHMM.md`) and start a fresh one — so the working memory stays short and the history is preserved.

- [`current.md`](current.md) in this folder is a starter template — drop it into your project's `log/` folder.
- This pairs with the global rule of the same name in [`../claude-md/global-CLAUDE.md`](../claude-md/global-CLAUDE.md).
