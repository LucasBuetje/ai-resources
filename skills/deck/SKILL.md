---
name: deck
origin: adapted from https://github.com/scunning1975/MixtapeTools
targets: [claude, opencode, antigravity, vibe]
description: Create or edit a Beamer slide deck. Use when the user asks to build, write, or edit a presentation or slide deck. For a PowerPoint (.pptx), use office-files; for HTML slides that help the user understand one paper, use summarize-paper.
---

# Deck

Build or edit a Beamer presentation following the Rhetoric of Decks principles.

---

## Step 1: Read the Knowledge Base

Open and read the `rhetoric.md` file co-located with this skill (same folder as this SKILL.md) before doing anything else. It contains the rhetoric principles, the Aristotelian triad, slide architecture standards, and the LaTeX style template that govern all decks. Use it as your benchmark throughout.

---

## Step 2: Triage

Answer these six questions before touching any file. If the user hasn't supplied an answer, ask — don't guess.

**Q1: New deck, or editing an existing one — and what is the source content?**
- If editing: read the `.tex` file(s) first. Understand the existing palette, structure, and style before changing anything.
- If new: what is the deck built from — a paper draft (`.tex`/`.pdf`/`.md`), lecture notes, an existing deck to restructure, or a description you generate from? If the source is a paper the user is reading, run `/summarize-paper` first and work from the summary rather than the PDF.

**Q2: Who is the audience?**

Pick ONE and commit — the audience sets the rhetorical balance (see the Aristotelian triad in `rhetoric.md`).

| Audience | Logos | Ethos | Pathos | Implications |
|---|---|---|---|---|
| **Academic seminar** (research talk) | 50% | 40% | 10% | Maximum sparsity. One idea per slide, no exceptions. Identification strategy early — skeptics want the source of variation before the results. Titles carry the full argument. Devil's Advocate slide. Appendix heavy. |
| **Conference presentation** (20 min) | 50% | 35% | 15% | Fast punch, headline result by slide 2, no literature review, ~15 slides. |
| **Teaching lecture** | 45% | 20% | 35% | Clarity over compression. Repetition welcome. Progressive revelation — build up formally step by step. Worked examples are content, not decoration. Check the prerequisite chain. |
| **Co-authors / working deck** | 60% | 30% | 10% | More detail is acceptable. Document choices explicitly. Preserve uncertainty. Rigor over polish. |
| **External / non-academic** | 30% | 25% | 45% | Storytelling and visual impact over technical precision. Minimal jargon. Lead with the human stakes. |

If unclear, ask before proceeding.

**Q3: What is the tone?**
- Default: the **Hamburg / Konstanz** palette (Konstanz Seeblau + Hamburg red) and Metropolis theme from `rhetoric.md`
- If a different palette is explicitly requested, establish it before starting

**Q4: Which language generates the figures and tables?**
R (ggplot2 + kable/xtable), Python (matplotlib/seaborn), or Stata (`graph export` + `esttab`). Pick ONE for the whole deck.

**Q5: Output format?**
**Beamer is the default** — richest control over typography, TikZ and math, and it compiles to a PDF that projects anywhere. Switch only on explicit request (Quarto/reveal.js, Typst, R Markdown, Marp). Whichever format is chosen, everything in this skill still applies — one idea per slide, assertion titles, the arc, code-first figures, both audits. Only the compile commands and preamble syntax change.

**Q6: What is the ONE sentence the audience should remember?**
It goes on the closing slide and frames the whole arc. If the user can't state it in one sentence, help them find it before any slide is written.

---

## File Naming

New decks get a descriptive, lowercase filename — no spaces, no generic names like `deck.tex` or `slides.tex`.

**Format:** `topic_audience.tex`

| Example | Why it works |
|---|---|
| `did_estimation_seminar.tex` | Topic + audience in the name |
| `macro_intro_lecture_03.tex` | Course lecture with sequence number |
| `chapter1_coauthor.tex` | Working deck tied to a paper chapter |
| `labor_supply_defense.tex` | Defense/job talk clearly marked |

If the project only has one deck, a short topic name is enough (`parental_jobloss.tex`). Add the audience suffix when there are multiple decks or when the audience materially changes the content.

The compile loop uses whatever filename is chosen — never hardcode `deck.tex`.

---

## Step 3: Design the Narrative Arc

Before writing any slides, write a one-page outline to `<deck_name>_outline.md` and show it to the user. Fixing the arc here is dramatically cheaper than fixing it after every slide exists.

### Intuition first, technical last

Every section moves in this order, never the reverse:

**Narrative → Application → Picture → Codeblock → Technical**

| Stage | What it looks like | Why it comes here |
|---|---|---|
| **1. Narrative** | A concrete scene: a named place, a real policy, a person facing a decision. "In 2003 the Hartz reforms cut the benefit duration for workers over 45…" | Anchors the audience in something specific before anything abstract arrives. Builds curiosity, not resistance. |
| **2. Application** | One example the audience can hold. "Suppose you are a 46-year-old deciding whether to accept an offer this month or search another two." | Makes the abstraction physical — they can picture the decision, not just parse symbols. |
| **3. Picture** | The figure showing the pattern. One message, direct labels. | Pictures carry intuition faster than words or equations. They see the relationship before they name it. |
| **4. Codeblock** | A short readable snippet showing how the quantity is computed, matching the deck palette, also saved as a standalone script. | A middle layer: more precise than a picture, more approachable than a theorem. |
| **5. Technical** | The equation, the identifying assumption in formal notation, the estimator. | Arrives *after* the audience already understands what it says, so the formalism reads as a compact summary rather than a wall to climb. |

The anti-pattern is the lecture that opens with definitions, derives the estimator, then offers an example at the end "for intuition" — it treats the technical as primary and the intuition as decorative. If you catch yourself showing an equation before the figure that motivates it, swap them.

**Exceptions:** a load-bearing definition may come early, but state the plain-English meaning first and the formal definition on the *next* slide; roadmap slides in long teaching decks may precede the narrative; title slides and section dividers are exempt.

### The arc

Three acts; proportions depend on the audience (Q2).

**Act I — Tension.** 2–4 slides. Title; opening hook (a provocative question, a surprising number, a concrete problem they recognise — **not** an agenda, **not** "Today I'll talk about…"); the stakes; optional roadmap for long teaching decks.

**Act II — Investigation.** 60–75% of the deck. Identification strategy early for academic audiences. One idea per slide, Pyramid Principle within each section. Alternate dense technical slides with lighter figure or summary slides so the deck breathes. Devil's Advocate slide near the end for academic or external decks.

**Act III — Resolution.** 2–4 slides. The headline result as a claim in the title with one figure or one equation supporting it; implications — what should the audience believe or do differently; the closing slide carrying the Q6 sentence, centred on a full-bleed dark background. **Not** "Questions?", **not** "Thank you".

### Titles as assertions

| Weak (label) | Strong (assertion) |
|---|---|
| Results | Benefit extension raised nonemployment duration by 4.2 weeks |
| Identification | We exploit the age-45 discontinuity in benefit duration |
| Methodology | Effects are estimated with Callaway–Sant'Anna, not two-way FE |
| Literature | Prior work confounds duration effects with selection into UI |
| Implications | A shorter extension would have produced the same reemployment wage |

Write out just the titles in sequence. If they don't tell the argument on their own, the arc is broken — fix it before writing slides.

### The outline checkpoint

```
# <Deck name> — Outline

## Audience and rhetoric
<Q1–Q6 answers>

## Theme
<palette, frame-title style, aesthetic choices>

## The arc
### Act I (slides 1–4)
  1. Title
  2. Opening: <hook>
  3. Stakes: <why this matters>
### Act II (slides 5–N)
  5. <assertion title>
  ...
### Act III (slides N+1 to end)
  K. Closing: <the one sentence>

## Figures and tables (code-first)
  - Figure 1: <what it shows, which script generates it>
  - Table 1: <what it contains, which script generates it>
```

**Show the outline and wait for approval before writing slides.**

---

## Step 4: Figures and Tables — Code First, Then Embed

The order is non-negotiable:

1. Write standalone scripts in `scripts/`
2. Run them, generating figures into `figures/` and table fragments into `tables/`
3. **Only then** write the `\includegraphics{}` and `\input{}` calls in the deck

The reverse order — writing `\includegraphics{fig2.pdf}` first and generating the figure to match — is the main cause of mismatched labels, stale numbers, and broken compiles.

**Scripts are standalone.** Each one runs on its own: libraries and data loading at the top (relative paths from the project, never hardcoded absolute ones), export at the bottom, no shared state between scripts. Someone should be able to open `scripts/figure_3.R`, run it, and reproduce `figures/figure_3.pdf` exactly. **Always save the script** — never generate a figure without preserving the code that made it (the Verification Is Code rule).

**Figures.** One message each; the title states the finding, not the chart type ("Reemployment wages fell only above the cutoff", not "Wages by age"). Direct labels at line endpoints rather than legends. Use the deck palette via the **one-accent-with-tints** rule in `rhetoric.md`: white background, series separated by the Seeblau tint ladder (not multiple hues), textures only beyond four series, Hamburg red reserved for semantic emphasis. Save as PDF (vector) for line charts and schematics; PNG only for dense rasters. Figure background matches the slide background.

**Tables.** `booktabs` only — top, mid, bottom rule, nothing else. Highlight the coefficient of interest. Strip anything that doesn't advance the argument (SEs in parentheses, stars, R² and N at the bottom; no F-stat unless the argument needs it). Export `.tex` fragments and `\input{}` them, so a re-run of the script never touches the deck source.

**Code blocks in teaching decks.** Show code in a `listings` environment styled to the palette, under ~12 lines; longer code becomes a skeleton on the slide with the full version in `scripts/`. Every code block shown in the deck corresponds to a real script file the students can be handed.

---

## Step 5: Build or Edit

Follow the rhetoric principles in `rhetoric.md` throughout. Key constraints that are non-negotiable:

- One idea per slide
- Titles are assertions, not labels — read titles in sequence: does the argument come through?
- Lead with conclusions, support with evidence (Pyramid Principle)
- No bullets unless items are genuinely parallel
- Figures readable from the back of the room
- Consider whether a Devil's Advocate slide is appropriate (see `rhetoric.md`)

### TikZ: write it safe from the start

These defaults exist because `/tikz` (invoked in Step 6) is a repair tool, not a safety net — it catches remaining collisions but can't reliably fix a diagram that was never built with measurement in mind.

- Always set explicit `minimum width`/`minimum height` on every `\node` — never let TikZ autosize a box.
- Every edge label needs a directional keyword (`above`, `below`, `left`, `right`, `sloped`, `pos=`, `midway`) — a label with none of these renders on top of the line.
- Write a coordinate-map comment before every `tikzpicture` (node name, coordinates, dimensions) — forces spatial planning before drawing.
- Start standard diagrams (DAG, flow chart, RDD threshold plot) from a canonical skeleton rather than from scratch.
- Never use `scale` on a complex diagram — it shrinks coordinates but not text, creating collisions that look fine in the source.
- Never define parameterized TikZ styles (`\tikzset{...#1...}`) inside a Beamer frame — `#` is consumed by the frame's argument parser first, causing "Illegal parameter number" errors that resist `##1`/`[fragile]`/`\catcode` workarounds. Define parameterized styles in the preamble; only *use* them inside frames.

### MB/MC equivalence — the rhythm check

After drafting the full deck, walk through it and rate each slide's marginal benefit (MB) and marginal cost (MC) on a 1–5 scale. The optimal deck holds MB/MC roughly constant across slides:

- **Overloaded (MB/MC too low):** footer text, competing ideas, a chart with too many series — split or simplify.
- **Underloaded (MB/MC too high):** a single word where a sentence would reinforce, wasted real estate — add or merge.

Exception: a deliberate "jump scare" — one dense table or provocative claim for rhetorical effect — is fine, intentionally, once or twice per deck.

---

## Step 6: Compile Loop

After every edit, run:

```bash
pdflatex -interaction=nonstopmode <filename>.tex 2>&1 | grep "Overfull" | grep -v "hyperref\|beamer"
```

Then check fatal errors:

```bash
grep "^!" <filename>.log
```

**Fix all fatal errors before anything else.**

For overflow warnings, apply the thresholds from `rhetoric.md`. Zero fatal errors required before distributing.

**Circuit breaker — do not spiral.** If 3 different fixes for the same error haven't resolved it (an error persisting at the same line, or moving to a nearby line, still counts as "the same"), stop editing the `.tex` file. Quote the log line to the user, list the 3 approaches tried and why each failed, and ask how to proceed. A fourth attempt on a file already made worse by three prior edits costs more than the 2 minutes it takes to ask.

If the deck uses TikZ: it should already follow the safe-generation defaults from Step 5. Before finalising, still run the `/tikz` skill on each figure — it performs the label-collision, whitespace, and edge-clipping checks that safe generation reduces but doesn't guarantee against; don't re-derive them inline here.

---

## Step 7: Rhetoric Audit

Once the deck compiles clean, get a second opinion on it against the Rhetoric of Decks principles — the built-in blind spot is that the agent who wrote the slides is bad at spotting its own buried leads.

- **In Claude Code:** dispatch a subagent (Agent tool) with this task:
  > Audit the Beamer deck at `<filename>.tex` and its compiled `<filename>.pdf` against `rhetoric.md` (co-located with the deck skill). Check: (1) titles are assertions, not labels — read them in sequence, do they tell a coherent story; (2) one idea per slide — flag any slide with two or more competing ideas; (3) no wall of sentences — flag any slide with more than two prose sentences stacked vertically; (4) MB/MC equivalence — rate each slide's density 1–5, flag outliers; (5) narrative arc — is there a clear setup/development/resolution, does the opening hook and does the closing land; (6) intuition-first ordering — flag any section where an equation or formal definition precedes the figure or example motivating it; (7) Devil's Advocate — if the audience is academic or external, is the strongest objection addressed somewhere. Return a structured report with numbered concerns and suggested rewrites. Do NOT modify the deck — only diagnose.
- **In OpenCode / Antigravity (no subagent capability):** run through the same seven checks yourself, in the main thread, treating it as a distinct pass rather than folding it into Step 5 — the point is a second, dedicated look at the compiled output, not a mental note taken while writing.

Apply every concern raised, then go back to Step 6 and recompile.

---

## Step 8: Graphics Audit

A second, narrower pass — figures, tables, and TikZ diagrams only. This is the step most likely to get skipped, and the errors it catches don't trigger LaTeX warnings or show up in a rhetoric read: a mislabeled axis or a coefficient that doesn't match the script output looks completely fine to both.

- **In Claude Code:** dispatch a subagent (Agent tool) with this task:
  > Audit ONLY the figures, tables, and TikZ diagrams in the compiled `<filename>.pdf`. Do not evaluate rhetoric, narrative, or content. Check: (1) numerical accuracy — do the numbers shown match the underlying script's output, any mismatch is critical; (2) label positioning — do labels sit where the source code intends, nothing clipped or drifted; (3) axis and tick coherence — sensible ranges, readable tick labels; (4) color consistency — figure colors match the deck palette and are used consistently for the same variable across figures; (5) font sizing — readable from the back of the room; (6) table formatting — booktabs rules only, consistent decimal alignment; (7) captions — states what to conclude, not just what the figure is. Return a structured report tied to specific files/coordinates. Do NOT modify any files — only diagnose.
- **In OpenCode / Antigravity (no subagent capability):** run through the same seven checks yourself against the compiled PDF, as a distinct pass after the rhetoric audit — not merged into it, since the two catch different failure modes.

Apply every fix, then go back to Step 6 (recompile) and re-run `/tikz` — this is typically where the last round of silent errors gets caught.

---

## Step 9: Review and hand off

Read all titles in sequence. Do they tell the argument? If not, fix the titles before anything else.

Then link the compiled `<filename>.pdf` in the reply (the Generated Files rule: a markdown link, never `open`).
