---
name: premortem
origin: adapted from https://github.com/olelehmann1337/openclaw-share
targets: [claude, opencode, antigravity]
description: Decision premortem — imagine the plan has already failed, then work backward to find out why. Use before committing to high-stakes, still-reversible decisions (job market strategy, dissertation chapter direction, research design, grant framing). Generates failure scenarios and investigates the most significant ones in depth (parallel subagents in Claude Code; sequential inline in OpenCode/Antigravity), then synthesizes the three most critical risks with concrete revisions.
argument-hint: '[description of the decision or plan being premortemed]'
---

# Premortem

Gary Klein's technique, endorsed by Kahneman as his single most valuable decision-making tool. The key shift: instead of asking "what could go wrong?" — which produces hedged, cautious lists — you ask "it already failed; explain why." That framing activates narrative reasoning and produces specific, honest failure scenarios that traditional risk assessment misses.

---

## When to Invoke

**Good targets:** Job market application strategy, dissertation chapter commitment, research design before data collection, grant framing before writing, major career decisions before they become irreversible, partnership or collaboration decisions.

**Poor targets:** Vague preliminary ideas ("I'm thinking about maybe pivoting..."), factual questions, creative feedback, decisions already made and irreversible.

The trigger is: **a concrete plan exists and there is still time to revise it.**

---

## Process

### Step 1 — Context

Before generating failure scenarios, establish:
- **The plan**: what exactly is being decided or committed to?
- **Success definition**: what does it look like if this works?
- **Time horizon**: when would failure become apparent?
- **Key stakeholders**: who is affected, who has to cooperate?

If the user provided a description as an argument, extract these from it. If any are genuinely unclear, ask — but keep it to one focused question, not a checklist.

---

### Step 2 — Frame Setting

Establish the narrative explicitly before generating scenarios:

> "It is [time horizon] from now. The plan has failed. Not partially — it has clearly, undeniably failed. You are explaining to a colleague what went wrong."

This framing is the mechanism. Do not skip it or soften it ("partially failed", "didn't go as well as hoped"). The failure must be complete and already past.

---

### Step 3 — Raw Failure Generation

Generate 8–12 specific failure reasons. Each must be:
- **Specific to this plan** — not generic risk ("execution problems", "bad luck")
- **Narrative** — a story about what happened, not a category label
- **Honest** — include failures the planner might not want to hear

Organize by failure type:
- **Assumption failures** — something believed to be true wasn't
- **Execution failures** — something went wrong in carrying the plan out
- **External failures** — the environment changed in a way not anticipated
- **Hidden dependency failures** — something the plan relied on that wasn't visible

---

### Step 4 — Parallel Investigation

For the **4–5 most significant failure reasons**, investigate each one deeply and independently.

- **In Claude Code:** spawn one subagent per scenario, in parallel. Use **Sonnet** for each (likelihood assessment, causal analysis, and mitigation planning are multi-step reasoning — a deliberate override of the Subagent Model Default rule).
- **In OpenCode / Antigravity (no subagent capability):** work through the scenarios sequentially in the main thread, one at a time, using the same per-scenario structure below. Do not pretend to spawn agents and do not skip scenarios.

Each investigation receives:
- The plan description
- The specific failure scenario
- The instruction: "Investigate this failure path. How likely is it? What are the early warning signs? What would prevent it or limit the damage?"

Each investigation returns:
- Likelihood assessment (low / medium / high)
- Early warning signs (observable before failure is complete)
- Prevention or mitigation actions

---

### Step 5 — Synthesis

Across all failure scenarios and deep investigations, identify:

1. **Most likely failure** — the one with the highest probability given what you know about the plan and context
2. **Most dangerous failure** — the one with the worst consequences if it occurs, regardless of probability
3. **Hidden assumption** — the thing the plan is betting on that hasn't been stated explicitly and hasn't been tested

For each: state it plainly, then give one concrete revision to the plan that would reduce that risk.

---

## Output Format

Print the synthesis to chat. Don't write separate files unless the user asks for one.

```
## Premortem: [Plan Name]

### Frame
[One sentence: what was premortemed and over what time horizon]

---

### Failure Scenarios
[Numbered list of 8–12 specific failure stories, organized by type]

---

### Deep Investigation Results
[For each of the 4–5 investigated scenarios: likelihood, early warning signs, prevention]

---

### Synthesis

**Most likely failure:**
[What it is and why]
→ Revision: [one concrete change to the plan]

**Most dangerous failure:**
[What it is and why]
→ Revision: [one concrete change to the plan]

**Hidden assumption:**
[What the plan is silently betting on]
→ Revision: [how to test or hedge this assumption before committing]

---

### Verdict
[ ] PROCEED — risks identified and manageable; revisions noted
[ ] PROCEED WITH CONDITION — one specific thing must be resolved first
[ ] RECONSIDER — fundamental assumption is untested and failure is high-consequence
```

Tick exactly one verdict, decided from the synthesis: **RECONSIDER** if the hidden assumption is untested and its failure would be high-consequence; **PROCEED WITH CONDITION** if exactly one finding meets the "high consequence + unmitigated" bar and a concrete condition would remove it (name the condition); otherwise **PROCEED**.

---

## Principles

- **Narrative beats lists.** A failure scenario that reads like a story ("The committee chair who informally told you the job was yours retired in January, and her replacement had a different candidate") is more useful than a category ("key personnel changes").
- **Honesty over comfort.** The most important failures are often the ones the planner is least willing to say aloud. Name them.
- **Specific over generic.** "Poor execution" is not a failure scenario. "You underestimated how long the data cleaning would take and ran out of time before the conference deadline" is.
- **Revisions, not reassurance.** The output is actionable. Each of the three synthesis findings must come with a concrete change, not a note to "be careful about" something.
