# Reading deck: the standard (Step 6)

A reading deck lets the user understand a paper **without having read it**: a smart economist,
outside the paper's subfield, reading alone at a screen. Each slide must be clear to that
reader cold. The previous decks failed here, not on looks: they were faithful to the paper
and still impossible to follow, because they used the paper's order, the paper's vocabulary
and the paper's internal references ("the Table 2 pattern", "Sample C", "the three
devices") without first saying what problem each piece solves.

The writer is an **Opus** subagent. It works from the fact-checked extract and **looks
things up** in the paper only where the extract is missing something or unclear: a step of
the identification argument, a figure it wants to redraw, a number it needs. It searches
the text layer for the passage and opens only the PDF pages it needs; it does not read the
paper through. The block at the end of this file is its prompt.

## The arc

Acts, in this order; each slide carries its act in `data-act`, which draws the argument map
at the top of every slide. Skip an act the paper does not have (a theory paper has no
Identification); never rename one.

| Act | Slides | What it must leave in the reader's head |
|---|---|---|
| Question | 2 | The question in everyday words, and why anyone should care (stakes, a number). |
| Setting | 1–2 | Who, where, when, how many, which data: one picture, not a list. |
| Facts | 1–3 | What the raw data show before any method; the puzzle the paper answers. |
| Method | 1–3 | The approach as a picture: who chooses what, what is compared with what. Equations only after the picture, and in a More box unless the reader needs them. |
| Identification | 4–7 | The ladder below. The act the earlier decks lost readers in. |
| Results | 3–6 | One result per slide, the number large, its specification beside it. |
| Limits | 1–2 | What could make the result wrong, and what the paper cannot say. |
| Use | 0–1 | Only with a reading focus: what this paper means for the user's question. |

Slide 2 is always **"The paper in one picture"**: a left-to-right chain drawn as boxes,
question → data → method → key assumption → main result → so what, each box one short line.
Every later slide is one box of that chain opened up, so the reader always knows where a
slide sits.

Total: 15–22 main slides, then detail slides (sample construction, full parameter tables,
the glossary). The closing slide is the one sentence to remember.

## The identification ladder

Identification is taught as a ladder, one rung per slide, in this order. Mark each rung
slide with `data-rung`. The checker fails a deck with an Identification act that misses a
rung.

1. **`question`: what we want to know, as two worlds.** The same person (firm, county) with
   and without the treatment, drawn as two boxes side by side, the unknown marked "?". Name
   the quantity the paper is after in words first ("how much one therapy session improves
   mental health"), then its symbol.
2. **`naive`: the obvious comparison, and why it lies.** Show the comparison anyone would
   make first, with the paper's own numbers where it reports them. Then the reason it
   misleads, as a story about people ("people start therapy right after something bad
   happens, so the treated look worse"), and the bias drawn as three nodes:
   treatment ← hidden cause → outcome.
3. **`fix`: what the paper compares instead, or what it borrows.** One sentence of the form
   "The paper compares A with B" or "The paper takes X from outside evidence and estimates
   only Y." Draw the comparison. For a structural model, a table with one row per key
   parameter: parameter (in words) · the feature of the data that moves it · the intuition
   ("a wider spread of effects means more people try therapy once and quit").
4. **`assumption`: why the fix works, and when it would fail.** The identifying assumption
   in plain words, then a box **"This would fail if…"** with one concrete story that breaks
   it, then what the paper does to test or relax it.
5. **`payoff`: what the fix buys.** The parameter it identifies and its estimate, with the
   specification next to it (the Results Carry Their Specification rule).

**Several strategies.** When a paper combines several devices (outside evidence for one
parameter, a fixed-effects comparison for another, shock types for selection), open the act
with a **map slide**: a table with one row per device: the problem in plain words · what
would go wrong without it · the device · its assumption. Then run rungs 3–5 per device; the
`question` and `naive` rungs are shared. Number the devices on the map and refer back to
them by number and name.

End the act with a quiz slide whose correct answer is the naive comparison's flaw, and whose
wrong answers are the two most tempting misreadings.

## Readability rules

These hold on every main slide; detail slides and More boxes are exempt.

- **Cold reader.** Never refer to the paper's tables, figures, sections, sample names or
  equation numbers in the visible text. Point to earlier slides instead ("the gap on slide
  6"). Paper locations go in the `<p class="src">` footer or a More box.
- **Every term defined where it first appears**, with `<dfn data-def="…">`: acronyms (MEPS,
  RCT, DiD), jargon (ordered logit, Emax, nested fixed point), and every symbol. A symbol
  appears only after its words: "the spread of the therapy effect (σ)". The glossary slide
  fills itself from these.
- **Titles are claims in everyday words**, at most about 12 words, a full sentence: "People
  in therapy look worse next period — because they start after a shock", not "Negative
  selection".
- **About 60 visible words per slide**, outside figures and More boxes. If it does not fit,
  it is two slides or a More box.
- **A picture wherever something can be drawn**: inline SVG, direct labels, no legend if
  avoidable, one message. Every figure has a `howto` line above it. When the paper's own
  figure makes the point better than a redraw, embed it: crop it from the page with
  `pdftoppm -png -r 150 -f <p> -l <p> -x <x> -y <y> -W <w> -H <h> <pdf> <out>`, look at
  the crop with Read to confirm it holds the whole figure and nothing else, and inline it
  as a `data:image/png;base64,` URI, at least 900 px wide on the slide. If its axis labels
  would still be smaller than body text, redraw it instead. Say in the `howto` line what to
  look at in it.
- **Every main slide ends in a takeaway** (`<p class="so">`) that says what this slide
  contributes to the argument, not a restatement of the title.
- **One running example** where it helps (a named person, a county, a firm), introduced in
  Setting and reused in Method and Identification. Keep it consistent.
- **Numbers come only from the extract, the text layer, or a value printed in the PDF**
  (a table cell, a data label). Never a value read off an axis. A number you compute yourself
  (a ratio, a sum) carries `class="own"` on its element and says how in a More box; axis
  labels you choose for a drawn chart carry `class="tick"`. Round
  for display, but never change a number's meaning.
- **Numbers a reader can feel.** A parameter in model units (utils, a latent index, the
  standard deviation of something unobserved) is never a headline. Say what it means in
  money, percent, probability or a comparison the paper itself reports ("one session costs
  more than half a year of pills"), and put the raw value, its standard error and the
  specification in a More box. The `payoff` rung above all.
- **A symbol only if a later slide uses it.** Otherwise the words alone.
- **Use the canvas.** The main element (figure, diagram, table) fills at least half the
  slide body. A slide with a small figure or two lines of text and an empty lower half is
  unfinished: enlarge the picture, draw what the text says, or merge the slide.
- **Estimates carry their specification**: the estimating equation in MathML (inline
  `<math>`, never LaTeX source or ASCII), what is reported, the estimator, the controls and
  the clustering. On the slide when short; in a More box otherwise.

## Components

The deck is built on the shared template `~/.claude/skills/deck/internal-slides.html`:
copy the **whole** file (its CSS and script line for line: the checker compares them),
replace what sits between the `SLIDES START` and `SLIDES END` markers, and replace the
example entry in `QUIZ` with your own. Its header lists the
reading aids: `data-act`, `howto`, `so`, `src`, `details.more`, `dfn data-def`, and a detail
slide with `data-glossary`. Use the template's colours and classes; add CSS only inside
the template's `<style>`, for a figure that needs it.

The title slide carries the full reference, the version read, and the provenance line
`Produced by <model> from the extract by <extract model> · <date>`.

## Writer prompt

Fill the paths and pass the block as the `Agent` prompt (`model: opus`).

```
Build a reading deck: an HTML slide deck that lets a smart economist who has NOT read this
paper understand it, reading alone. Clarity for that reader beats faithfulness to the
paper's order and vocabulary.

Standard:  <absolute path to ~/.claude/skills/summarize-paper/reading-deck.md>
Template:  <absolute path to ~/.claude/skills/deck/internal-slides.html>
Extract:   <absolute path to the extract .md>   ← your starting point
Text layer:<absolute path to <basename>.txt>     ← look up: search it, read only the passages you need
PDF:       <absolute source PDF path>            ← look up: open only the pages you need
Output:    <absolute path to <basename>_deck.html>
Reading focus (if any): <the user's focus, or "none">

1. Read the standard in full, then the template, then the extract. Do not read the
   paper through. Where the extract is missing something or unclear (above all a step of
   the identification argument), find the passage with `grep -n` in the text layer and
   read only those lines (Read with offset and limit); open a PDF page (Read with `pages`)
   only to see a figure or table you will redraw or embed.
2. Before writing any slide, write a plan (for yourself, not into the file): the "paper in
   one picture" chain; the acts and the title of every slide; for Identification, each
   rung, and the map if there are several devices; the running example; every term that
   needs a dfn.
3. Check the plan against the cold reader: for each slide, could someone who saw only the
   previous slides follow it? Fix the plan where the answer is no.
4. Write the deck: the template file with your slides between the markers. Use only
   numbers from the extract, the text layer or printed in the PDF; mark your own
   arithmetic class="own".
5. Run `python3 <absolute path to ~/.claude/skills/summarize-paper/check_deck.py>
   --deck <output> --extract <extract> --text <text layer>` and fix every FAIL line; fix
   WARN lines unless the standard allows them. Re-run until it exits 0.

Tools: Read, Write, Edit, and Bash only for grep on the text layer, the checker, pdftoppm
and base64. No web.
Your final reply is ONE line: `MODEL <your model ID> · SLIDES <n> · WROTE <path>`.
```
