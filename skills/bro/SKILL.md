---
name: bro
origin: self
description: Restate the last message in plain human language, with no jargon.
disable-model-invocation: true
user-invocable: true
---

Restate your last message. Stop using jargon and speak coherently. State it more simply and concisely, like one human talking to another.

**With a file argument** (`/bro slides.html`, `/bro summary.md`): rewrite the prose in that file in place to the same standard. Tables, figures, code blocks, numbers and the file's structure (slides, headings, sections) stay untouched; only the running text and titles change. Empirical-micro terms are not jargon and stay; software terms (gate, invariant, guardrail, surface) are. Report which passages changed in one line each.
