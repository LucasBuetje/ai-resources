---
name: skill-update-check
origin: self
targets: [claude]
description: Check adapted skills against their upstream GitHub sources for substantial updates. Reads origin fields, fetches upstream versions, compares, flags changes worth adopting. Use when you want to sync adapted skills with their sources.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash(grep*), Bash(find*), Bash(ls*), Agent, WebFetch, AskUserQuestion
---

# Skill: skill-update-check

Checks locally adapted skills against their upstream sources for substantial changes worth reviewing or adopting.

---

## Phase 1 — Discover adapted skills

Scan every `skills/*/SKILL.md` in the current project for skills whose `origin:` field contains a URL (i.e. `origin: adapted from https://...`). Build a list of:
- skill name (folder name)
- local SKILL.md path
- source URL (everything after `adapted from `)

Skip skills with `origin: self` or no `origin:` field.

---

## Phase 2 — Resolve each URL to a fetchable raw file

**Direct file URL** (contains `/blob/` or is already a raw URL):
- `https://github.com/<user>/<repo>/blob/<branch>/<path>` → `https://raw.githubusercontent.com/<user>/<repo>/<branch>/<path>`
- `https://raw.githubusercontent.com/...` → unchanged

**Repo-level URL** (`https://github.com/<user>/<repo>` with no file path):
Try these candidate paths in order, constructing `https://raw.githubusercontent.com/<user>/<repo>/refs/heads/main/<candidate>`. Use the first that returns non-empty content that looks like a Markdown file (WebFetch does not expose HTTP status codes — treat an error, empty result, or HTML error page as a miss):
1. `.claude/skills/<skill-name>/SKILL.md`
2. `skills/<skill-name>/SKILL.md`
3. `<skill-name>/SKILL.md`
4. `<skill-name>.md`

If all four miss on `refs/heads/main`, retry the same candidates with `refs/heads/master` (older repos).

Also try common name aliases for known divergences (the local folder name often differs from the upstream file name):
- `summarize-paper`, `split-pdf-antigravity` → also try `split-pdf` (both adapted from MixtapeTools' `split-pdf`; `summarize-paper` has since diverged heavily — it no longer chunks — so expect large divergence)
- `deck` → also try `beautiful_deck`
- `verify-pdf-antigravity` → also try `split-pdf`
- `blindspot`, `bibcheck`, `tikz`, `referee2` (MixtapeTools) → if the four standard candidates miss, fetch the repo's root listing (`https://github.com/<user>/<repo>`) and search it for a file or folder whose name resembles the skill name (e.g. `personas/referee2.md`); use the discovered path
- **When adding a new `origin: adapted from <repo>` skill whose upstream name differs from the local folder name, add an alias line here** — otherwise it will silently land in source-not-found

If no candidate yields content, mark the skill as **source-not-found**.

---

## Phase 3 — Fetch and compare (parallel agents)

Spawn one Agent (Haiku) per skill with a resolved URL. Each agent:

1. Fetches the upstream file via `WebFetch`
2. Reads the local `SKILL.md`
3. Compares and classifies:
   - **none** — only metadata, wording tweaks, whitespace, or formatting differ
   - **moderate** — clarified instructions, new examples, minor new steps
   - **substantial** — new phases, changed core behavior, new tool requirements, restructured workflow, significantly expanded scope
4. Returns `{ skill, status, summary, upstream_url }`

Note: divergence from upstream is expected for the PDF-reader skills (`summarize-paper`, `split-pdf-antigravity` — backend-specific adaptations; `summarize-paper` has diverged completely) and `premortem` (domain adaptation). Flag changes but weight them accordingly.

---

## Phase 4 — Report

Present findings:

```
## Skill Update Check

### Substantial updates
- **<skill>** — <one sentence: what changed>

### Moderate updates
- **<skill>** — <one sentence: what changed>

### No substantial changes
<skill>, <skill>, ...

### Source not found
- <skill> — could not locate file at <url>
```

---

## Phase 5 — Offer to adopt

For each skill with a **substantial** or **moderate** update, ask via `AskUserQuestion`:
- **View diff** — show a structured summary of the key differences (new sections, removed sections, changed behavior)
- **Adopt** — re-fetch the upstream file via `WebFetch` (the Phase 3 agents return only summaries, not content — the main thread never held the upstream text), overwrite `skills/<name>/SKILL.md` with it, then reapply **all** frontmatter fields from the local version (`name:`, `origin:`, `targets:`, `user-invocable:`, `allowed-tools:`, and any others present) — upstream frontmatter is missing or wrong for this repo
- **Skip** — leave as-is

Ask all at once (one question per updated skill) rather than sequentially.

After any **Adopt**: remind the user to run `bash build.sh && bash apply.sh --yes` to propagate the update to live.

---

## Edge cases

- **WebFetch fails**: note per skill, continue with others
- **Upstream is not a SKILL.md** (e.g. a narrative `.md` like `personas/referee2.md`): compare anyway; note the format difference
- **PDF-reader skills**: fetch the upstream `split-pdf` source once and reuse it for both `summarize-paper` and `split-pdf-antigravity`
