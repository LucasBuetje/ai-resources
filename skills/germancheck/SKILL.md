---
name: germancheck
origin: self
targets: [claude, opencode, antigravity]
description: Scan generated German text for translation tells — anglicism calques, false friends, untranslated English words, and English-mirroring sentence structure that mark a passage as machine-translated rather than natively written. Runs a fresh review pass (Sonnet subagent in Claude Code/OpenCode; inline in Antigravity) over the prose of a .tex, .md, or .txt file and reports a reviewable findings table with suggested German replacements. Read-only by default; offers to apply fixes surgically. Use as a final pass over any important German deliverable — slides, exercise sheets (Übungsblätter), letters, emails.
allowed-tools: Read, Bash(grep*), Bash(ls*), Bash(file*), Bash(wc*), Agent, Edit
argument-hint: '[path/to/file.tex | path/to/file.md | path/to/file.txt]'
---

# `/germancheck`: hunt for translation tells in German text

A narrow, fast review pass over German prose. It looks for one class of problem: words and
constructions that are technically German but that a native expert would never use, because
they were reached for as the cognate of an English term. These compile fine, read fine to the
author, and are invisible to the model that wrote them — exactly because the same model
produced them. A separate pass with fresh eyes catches what self-review in the generating
context misses.

This is **not** a grammar checker, a style editor, or a proofreader. Four checks only.

---

## When to invoke

- After generating an important German deliverable: slides, Übungsblätter, lecture material,
  letters, emails, reports.
- On explicit request: "germancheck", "prüf das Deutsch", "klingt das übersetzt?", `/germancheck <file>`.

Do **not** auto-invoke on every German snippet — it is a final pass, run on demand.

---

## The four checks

1. **Lexical calques** — a German word standing in for an English cognate where the field uses
   a different term. *Quantum* (→ Menge), *Recap* (→ Wiederholung), *Setup* (→ Aufbau),
   *der Markt klärt* (→ der Markt räumt sich / Markträumung).
2. **Verb/preposition calques** — an English verb or government bolted onto German. *für X
   kontrollieren* (→ um X bereinigen), *adressieren* a problem (→ behandeln), *realisieren* =
   understand (→ erkennen), *macht Sinn* (→ ergibt Sinn), *basiert auf* overused.
3. **False friends** — English meaning smuggled into a German look-alike. *eventuell* (=
   possibly, NOT eventually), *aktuell* (= current, NOT actual), *sensibel*, *Kontrolle*,
   *konsequent*, *brillant*.
4. **Untranslated / English-mirroring** — English words left in where a German term exists
   (*mandate*, *deadweight loss* in running prose), or sentence structure that tracks the
   English original too literally (word order, "es gibt …" for "there is", nominal style).

**Plus, für `.tex` unter babel ngerman:** gerades ASCII-`"` als schließendes Anführungszeichen
flaggen — es wird nicht gesetzt (öffnendes „ rendert, schließendes fehlt). Fix: „ … " oder
`\glqq … \grqq{}`.

---

## Process

### Step 1 — Resolve the target

- If a path was given as an argument, use it. If the user just generated or discussed a file,
  use that. Otherwise ask for the path — one question, no checklist.
- Accept `.tex`, `.md`, `.txt`, and plain pasted text. For other formats, ask the user to point
  at the text.

### Step 2 — Isolate the prose

The check is on **running German prose**, not on markup or math.

- For `.tex`: ignore preamble, commands (`\command{…}`), math (`$…$`, `\[…\]`, `align`
  environments), labels, and TikZ coordinates. Review the human-readable text inside frames,
  `\textbf{}`, item text, block bodies, captions.
- For `.md` / `.txt`: review the body; skip code fences, URLs, and YAML frontmatter.
- Reading these text files directly is fine (they are documents, not raw data).

### Step 3 — Fresh review pass

Dispatch a **fresh reviewer** so the eyes are not the eyes that wrote the text:

- **Claude Code / OpenCode:** spawn one **Sonnet** subagent (nuanced German language
  judgment — Haiku is not enough; this overrides the Haiku subagent default). Pass it the
  isolated prose and the four checks above.
- **Antigravity** (no subagents): run the review inline yourself, but explicitly re-read the
  prose fresh against the four checks rather than relying on recollection of having written it.

Reviewer instructions:
- Go phrase by phrase. For each suspected tell, capture: the **exact phrase**, **where** it is
  (frame title / section / line), **which of the four checks** it trips, **why** it reads as a
  translation, and a **suggested German replacement**.
- Hunt beyond the seed examples — the lists above are a starting point, not the whole problem.
  A novel calque not named above still counts.
- Be calibrated, not trigger-happy. Established loanwords that German academia genuinely uses
  (e.g. *Paper*, *Working Paper*) are not tells. Flag only what a native expert would change.
  If a passage is clean, say so — don't manufacture findings to fill a quota.

### Step 4 — Report

Present a single table, most-confident first:

| Phrase | Ort | Check | Warum | Besser |
|---|---|---|---|---|

- If nothing is found, say so plainly: the German reads natively, no translation tells.
- Then ask whether to apply the changes. **Do not edit unprompted.**

### Step 5 — Apply (only if asked)

- Apply surgically: change only the flagged phrase, touch nothing adjacent (Surgical Editing
  rule). Each edit must trace to a finding in the table.
- Where a fix has more than one valid rendering, present the options rather than silently
  picking one.

---

## Scope discipline

- ❌ Don't drift into grammar, spelling, punctuation, or style preferences — those are out of
  scope. If a glaring grammar error sits next to a flagged calque, note it in one line, but
  don't turn this into a full proofread.
- ❌ Don't rewrite whole sentences for elegance. The deliverable is a list of translation
  tells, not a rewrite.
- ✅ Keep it to the four checks. Like a collision check for figures: one narrow class of error,
  caught reliably.
