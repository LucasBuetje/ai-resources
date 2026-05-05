---
name: deck
description: Create or edit a Beamer slide deck. Use when the user asks to build, write, or edit a presentation or slide deck.
---

# Deck

Build or edit a Beamer presentation following the Rhetoric of Decks principles.

---

## Step 1: Read the Knowledge Base

Read `~/.claude/skills/deck/rhetoric.md` before doing anything else. It contains the rhetoric principles, slide architecture standards, and LaTeX style template that govern all decks. Use it as your benchmark throughout.

---

## Step 2: Triage

Answer these three questions before touching any file:

**Q1: New deck or editing existing?**
- If editing: read the `.tex` file(s) first. Understand the existing palette, structure, and style before changing anything.
- If new: proceed to Q2.

**Q2: Who is the audience?**

| Audience | Implications |
|---|---|
| **Academic seminar** | Maximum sparsity. One idea per slide, no exceptions. Titles carry the full argument. Appendix heavy. |
| **Teaching lecture** | Clarity over compression. Repetition is welcome. Progressive revelation — build up formally step by step. Check prerequisite chain. |
| **Co-authors / working deck** | More detail is acceptable. Document choices explicitly. Preserve uncertainty where it exists. |
| **External / non-academic** | Storytelling and visual impact over technical precision. Minimal jargon. Lead with the human stakes. |

If unclear, ask the user before proceeding.

**Q3: What is the tone?**
- Default: use the HSV palette and Metropolis theme from `rhetoric.md`
- If a different palette is needed, establish it before starting

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

The compile loop and `open` command use whatever filename is chosen — never hardcode `deck.tex`.

---

## Step 3: Build or Edit

Follow the rhetoric principles in `rhetoric.md` throughout. Key constraints that are non-negotiable:

- One idea per slide
- Titles are assertions, not labels — read titles in sequence: does the argument come through?
- Lead with conclusions, support with evidence (Pyramid Principle)
- No bullets unless items are genuinely parallel
- Figures readable from the back of the room
- Consider whether a Devil's Advocate slide is appropriate (see `rhetoric.md`)

---

## Step 4: Compile Loop

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

If the deck uses TikZ: before finalising, verify that no labels collide with arrows or box edges, and that all Bézier curves have labels offset from the computed curve position (not guessed).

---

## Step 5: Figures

When the deck needs data visualisations:

1. Write an R script (`generate_figures.R`) using ggplot2, or a Python script using matplotlib
2. Use the same colour palette as the LaTeX deck
3. Save figures as PDF to a `figures/` subdirectory
4. Every figure: one message, direct labels, title states the finding
5. **Always save the script** — never generate a figure without preserving the code that created it

---

## Step 6: Open and Review

```bash
open <filename>.pdf
```

Read all titles in sequence. Do they tell the argument? If not, fix the titles before anything else.
