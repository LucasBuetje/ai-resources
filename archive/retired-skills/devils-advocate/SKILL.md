---
name: devils-advocate
description: Challenge a Beamer slide deck with 5-7 specific pedagogical and rhetorical questions. Checks ordering, prerequisites, cognitive load, notation, and argument flow. Use for both teaching slides and research presentations.
---

# Devil's Advocate

Critically examine a slide deck and challenge its design with 5–7 specific, pointed questions.

**Philosophy:** "We arrive at the best possible presentation through active dialogue."

---

## Setup

1. **Read `~/.claude/skills/deck/rhetoric.md`** — this is the knowledge base. It contains the rhetoric conventions, slide architecture principles, and LaTeX style standards that govern what a good deck looks like. Use it as your benchmark throughout.

2. **Read the target file** — the `.tex` file(s) for the deck being challenged. Follow `\input{}` references if the deck is split across files.

3. **If a teaching deck**: also read any adjacent lecture files (previous/next session) to check narrative continuity and prerequisite chain.

---

## Challenge Categories

Generate 5–7 challenges drawn from these categories. Always pick the ones most applicable to the specific deck — do not mechanically cover all 7.

### 1. Ordering Challenges
> "Could the audience follow this better if we showed X before Y?"

Check whether the sequence of slides matches how understanding actually builds. Look for slides that assume knowledge not yet established, or results shown before the audience has the setup to interpret them.

### 2. Prerequisite Challenges
> "Does the audience have the background for this at this point?"

For teaching decks: Does a slide introduce notation or a concept that builds on something not yet covered in this or prior lectures?
For research decks: Does the identification strategy slide assume familiarity with the institutional context before it's been explained?

### 3. Gap Challenges
> "Should there be an intuitive example or bridge slide here before this formal content?"

Identify jumps — places where the deck moves from setup to result, or from intuition to formalism, without a transition. These are where audiences get lost.

### 4. Alternative Presentation Challenges
> "Here are 1–2 other ways to present this idea — are they clearer?"

Suggest a concrete alternative for one slide or sequence. Could a table become a figure? Could a list of assumptions become a timeline? Would a numerical example before the general formula help?

### 5. Notation and Terminology Conflicts
> "This symbol or term conflicts with earlier usage."

Check that symbols are used consistently throughout. Flag any slide where a term shifts meaning, a subscript convention changes, or a variable defined in slide 3 reappears with a different meaning in slide 15.

### 6. Cognitive Load Challenges
> "This slide introduces too many new things at once — can we split it?"

Apply `deck.md`'s principle: one idea per slide. Flag slides that introduce multiple new symbols, concepts, or arguments simultaneously. Also flag slides where the title asserts one thing but the body contains content about something else.

### 7. Rhetoric and Argument Flow Challenges
> "Do the slide titles tell the argument when read in sequence?"

Apply `deck.md`'s title-as-assertion principle. Read only the slide titles in sequence — does the argument come through? Flag titles that are labels ("Results") rather than assertions ("Treatment increases distance by 61 miles"). Also check that the pyramid principle is followed: conclusion first, then evidence.

---

## Output Format

```markdown
# Devil's Advocate: [Deck Title or Filename]

## Challenges

### Challenge 1: [Category] — [Short title]
**Question:** [The specific challenge, framed as a question]
**Why it matters:** [What could go wrong for the audience]
**Suggested resolution:** [Specific, actionable fix]
**Slides affected:** [Slide numbers or titles]
**Severity:** [High / Medium / Low]

[Repeat for 5–7 challenges]

---

## Summary Verdict
**Strengths:** [2–3 things the deck does well, with reference to deck.md principles]
**Critical changes:** [0–2 changes that should happen before presenting]
**Suggested improvements:** [2–3 nice-to-have changes]
```

---

## Principles

- **Be specific**: Reference exact slide numbers, titles, or notation symbols
- **Be constructive**: Every challenge must have a suggested resolution
- **Be honest**: If the deck is strong, say so — do not invent problems
- **Prioritize**: Notation conflicts and argument flow > cognitive load > ordering > gaps
- **Use deck.md as the standard**: Ground every critique in the rhetoric principles there, not generic advice
