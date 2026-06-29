---
name: tikz
origin: adapted from https://github.com/scunning1975/MixtapeTools
targets: [claude, opencode, antigravity]
description: Quick visual-collision check for figures — TikZ inside .tex files OR rendered .png/.jpg/.pdf figures from R/Python. Three checks only. (1) Bezier-curve label collisions via gap math. (2) Label-to-object whitespace. (3) Labels touching or running off the figure edge. These are the visual errors that compile cleanly — pdflatex never warns about them, ggsave never refuses to write them, so the agent that produced them does not know they are wrong. Use after generating any figure where visual correctness matters and you cannot eyeball it yourself.
allowed-tools: Bash(grep*), Bash(ls*), Bash(file*), Bash(wc*), Read
argument-hint: [path/to/file.tex | path/to/figure.png | path/to/figure.pdf]
---

# `/tikz`: narrow visual-collision check

A small, fast collision check for figures. Three checks. Catches the class of error that produces no warning, no error, no exit code — only a wrong-looking figure that the producing agent cannot see.

This skill replaced an earlier six-pass version that ran an entire-file re-audit after every fix. That version timed out on real decks. This version does **three checks, one pass, exits**. If you want more, run it again.

---

## Step 1: Identify the input

Routing depends on file type:

| Extension | Mode | What gets checked |
|---|---|---|
| `.tex` | **Math mode** | TikZ source — gap calculations, coordinate distances |
| `.png`, `.jpg`, `.jpeg` | **Visual mode** | Rendered raster — read the image, look |
| `.pdf` (single-figure) | **Visual mode** | Same: read and look |
| `.pdf` (multi-page deck) | **Refuse** | Out of scope. Run `/tikz` on the figure file or the standalone .tex. |

If the user did not specify a file, ask. Do not guess.

---

## The three checks (both modes apply them, just differently)

### Check 1 — Bezier curve label collisions

A curved arrow has an arc that bows away from the chord between its endpoints. If a label sits in that arc, it gets crossed by the line.

### Check 2 — Label-to-object whitespace

Every text label needs at least 0.4 cm (or visible whitespace, in raster terms) between its bounding box and any drawn shape — node, axis, marker, bar.

### Check 3 — Labels touching or running off the figure edge

Every label has to be entirely inside the figure bounds, with at least 0.5 cm clearance from the edge. Labels at the right margin, top margin, or rotated y-axis labels are the typical offenders.

---

## Math mode (for `.tex` files)

For each `\begin{tikzpicture}` block:

### Check 1: Bezier curves

```bash
grep -n "bend" [file].tex
```

For each curved arrow with `bend left=N` or `bend right=N`: extract the two anchor
coordinates from the `to`/`edge` command — either raw `(x,y)` pairs directly, or by
looking up the named nodes' coordinates earlier in the same `tikzpicture` block. Then:

```
chord_length = distance between the two endpoints (cm)
max_depth    = (chord_length / 2) × tan(N / 2)
safe_zone    = max_depth + 0.5 cm
```

| Bend angle | tan(angle/2) |
|---|---|
| 20° | 0.176 |
| 30° | 0.268 |
| 45° | 0.414 |
| 60° | 0.577 |

If any label coordinate is within `safe_zone` of the chord baseline (in the direction the curve bends): flag and propose a position outside the safe zone.

### Check 2: Whitespace

For each `\node` containing label text and each adjacent `\draw` shape (rectangle, circle, line):

- Compute label center
- Compute shape boundary
- Required clearance: 0.4 cm

If a label coordinate lands within 0.4 cm of a boundary: flag and propose moving it 0.4 cm outside.

### Check 3: Edge clipping

For each `\node`, `\draw`, `\fill`:

- Note extreme x/y coordinates
- Compare against `\useasboundingbox` if declared; if absent, estimate the canvas bounds as the min/max of all coordinates in the block plus 0.1 cm padding
- If any element is within 0.5 cm of the figure edge: flag.

---

## Visual mode (for `.png` / `.jpg` / single-figure `.pdf`)

Read the image file and inspect it visually (requires a multimodal session — if the current tool cannot view images, fall back to the `.tex` source in math mode, or say so and stop). Apply the same three checks, scored by visible whitespace rather than measured distance:

### Check 1: Curve label collisions

Any text that visibly intersects a curved line, arrow shaft, or smoothed regression line.

### Check 2: Label-object overlap

Any text that touches or overlaps a marker, bar, axis line, gridline, or other plot element. Includes legend boxes that overlap the plot area.

### Check 3: Edge clipping

Any label partially cut off by the image boundary, or running into the figure margin. Includes y-axis titles too close to the left edge, x-axis titles too close to the bottom, rotated tick labels overflowing.

### Honest limitation

Visual-mode detection is less reliable than math mode. Reliable: clipping, large overlaps. Less reliable: subtle whitespace violations under a few pixels. When the figure is high-stakes, also run `/tikz` on the source code (.R, .py, or .tex) that generated it — the source has signals the rendering does not.

### Typical fixes by toolchain

**ggplot2 (R)**:
- Move legend: `theme(legend.position = "top")`
- Crowded labels: `ggrepel::geom_text_repel()`
- Edge clipping: `theme(plot.margin = margin(t=10, r=20, b=10, l=20))`
- Long y-axis title: `theme(axis.title.y = element_text(margin = margin(r=10)))`

**matplotlib (Python)**:
- Auto-padding: `plt.tight_layout()`
- Save with bounds: `plt.savefig(..., bbox_inches='tight')`
- Move legend: `ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')`

**TikZ (LaTeX)**:
- Add `\useasboundingbox` to declare canvas explicitly
- Use `node[anchor=...]` to control label placement relative to coordinate
- For curves, place label as a separate `\node at (midpoint)` outside the arc, not as inline edge label

---

## Output

Report findings as a structured list. Do not enter a repair loop.

```
[file] — quick check complete

Bezier collisions:    N
Whitespace collisions: M
Edge clipping:        K

Findings:
  - <location>: <description>. Fix: <proposed change>.
  - ...
```

Then **stop**. The user reviews and edits. If they want a deeper look at a specific element, they invoke `/tikz` again on that scope.

---

## What this skill does NOT do

- It does not iterate. One pass, one report, exit.
- It does not re-audit the whole file after a fix. That's the quadratic blowup that killed the previous version.
- It does not run `pdflatex` in a loop.
- It does not eyeball multi-page PDFs. PDF mode is single-figure only; for decks, point it at the source `.tex` instead.
- It does not perform cross-slide consistency checks, autosized-node detection, scale-factor compensation, or the four other passes the previous version did. If you want those, the prior behavior is in git history before this commit.

---

## Why narrow

Visual errors that don't produce compile errors are the class Claude Code fundamentally cannot detect during normal work. The agent compiles, sees no warnings, declares done — and the figure has a label sitting on a curve. Three checks, focused on the three errors that compile cleanly, finishing in under five minutes per figure. That is the entire value proposition.
