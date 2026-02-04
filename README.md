# AI Resources

A curated collection of custom AI prompts and tools for research and writing. This repository contains system prompts optimized using the CRISPE framework to help you get better, more consistent results from AI tools.

> **Note:** These resources were presented at the Internal Exchange on AI in Research (February 11, 2026) by Lucas Bütje, University of Konstanz.

## Table of Contents

- [Introduction](#introduction)
- [Creating Custom AIs: The CRISPE Framework](#creating-custom-ais-the-crispe-framework)
- [Available Custom AI Prompts](#available-custom-ai-prompts)
  - [Gemini Custom AIs](#gemini-custom-ais)
  - [Antigravity Custom AIs](#antigravity-custom-ais)
- [AI Tools Overview](#ai-tools-overview)
- [Getting Started](#getting-started)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Introduction

Same LLM, very different results! The quality of AI outputs heavily depends on how you interact with them. This repository provides structured prompts and workflows to create custom AIs that deliver consistent, high-quality results for specific tasks.

**What you'll find here:**
- Structured system prompts using the CRISPE framework
- Custom AIs for research tasks (paper summarization, code review, LaTeX editing, etc.)
- Documentation on helpful AI tools for research and writing

**What this repository doesn't cover:**
- AI in teaching
- Data privacy & security
- Authorship & citation guidelines
- Legal issues
- Climate impact of AI

## Creating Custom AIs: The CRISPE Framework

The **CRISPE framework** provides a structured approach to crafting effective AI prompts. Follow these three steps:

### 1. Prompt Foundation: CRISPE Structure

- **C**apacity: Define the AI's expertise level
- **R**ole: Specify what the AI should do
- **I**nsight: Provide constraints, protocols, and key considerations
- **S**tyle: Define the output format and tone
- **P**rocess: Outline step-by-step workflow
- **E**xample: Provide sample input/output

### 2. Knowledge Files (Optional)

Upload reference documents for the AI to use when responding.

### 3. Instruction Tuning

Iterate on your prompt through trial and error until you get the desired output.

## Available Custom AI Prompts

### Gemini Custom AIs

Located in `prompts/gemini/`:

1. **Paper Summarizer - Empirical** (`paper-summarizer-empirical.md`)
   - Extracts and formalizes causal identification strategies
   - Structured output with research questions, methodology, and key findings
   - Uses telegraphic style with LaTeX notation for precision

2. **Paper Summarizer - Literature Review** (`paper-summarizer-litreview.md`)
   - Optimized for literature review papers
   - Provides structured summaries of theoretical contributions

3. **Custom AI Creator** (`custom-ai-creator.md`)
   - Generates first drafts of new custom AIs using the CRISPE framework
   - Meta-prompt for creating other prompts

4. **Paper Podcast Prompter** (`paper-podcast-prompter.md`)
   - Creates instructions for NotebookLM to generate podcast scripts
   - Useful for consuming papers during travel

5. **Google Scholar Labs Prompter** (`google-scholar-labs-prompter.md`)
   - Optimizes queries for Google Scholar Labs paper search
   - Helps find relevant academic literature

6. **NEPS Codebook and Code** (`neps-codebook-code.md`)
   - Project-specific AI that knows codebooks and existing code
   - Answers questions about the NEPS project via NotebookLM integration

### Antigravity Custom AIs

Located in `prompts/antigravity/`:

1. **General Instructions** (`general-instructions.md`)
   - Base instructions for all Antigravity agents
   - Sets standards and expectations across all coding tasks

2. **R Code Reviewer** (`r-code-reviewer.md`)
   - Reviews R code in small chunks
   - Checks for syntax errors, logic errors, and comment-code mismatches

3. **R Code Formatter** (`r-code-formatter.md`)
   - Formats R code to a consistent style
   - Ensures code readability and maintainability

4. **LaTeX Reviewer** (`latex-reviewer.md`)
   - Reviews LaTeX documents section by section
   - Suggests improvements for clarity and formatting

## AI Tools Overview

### General Purpose AI

**Gemini** (Primary tool)
- Flash and Pro models for different complexity levels
- Integrates with NotebookLM notebooks
- Note: No chat history unless data sharing is enabled

**Alternatives:** ChatGPT, Claude (recommended for privacy), Perplexity

### Coding and LaTeX

**Antigravity** (Agent-first IDE)
- AI agents can answer questions, rewrite, and debug code
- Works with entire projects, not just single files
- Provides diff view for accepting/rejecting changes
- In-line suggestions while typing

**Free Alternative:** VSCode + GitHub Copilot (free for university members)

### Other Useful Tools

- **NotebookLM** (Google): Upload documents, ask questions, create podcasts
- **Google Scholar Labs, elicit, R Discovery**: Find papers using natural language
- **Perplexity**: Multi-model AI chat with search engine integration

## Getting Started

1. **Choose a custom AI prompt** from the `prompts/` directory
2. **Copy the prompt** to your AI tool of choice (e.g., Gemini, ChatGPT, Claude)
3. **Customize if needed** to match your specific use case
4. **Test and iterate** until you get the desired output

### Example: Using the Paper Summarizer

1. Open Gemini and create a new custom AI
2. Copy the content from `prompts/gemini/paper-summarizer-empirical.md`
3. Paste it as the system prompt
4. Upload a paper PDF
5. Simply hit enter - the AI will automatically summarize it

## Folder Structure

```
ai-resources/
├── prompts/
│   ├── gemini/
│   │   ├── paper-summarizer-empirical.md
│   │   ├── paper-summarizer-litreview.md
│   │   ├── custom-ai-creator.md
│   │   ├── paper-podcast-prompter.md
│   │   ├── google-scholar-labs-prompter.md
│   │   └── neps-codebook-code.md
│   └── antigravity/
│       ├── general-instructions.md
│       ├── r-code-reviewer.md
│       ├── r-code-formatter.md
│       └── latex-reviewer.md
├── examples/
│   └── (Sample outputs from custom AIs)
├── LICENSE
└── README.md
```

## Contributing

Feel free to:
- Submit your own custom AI prompts
- Suggest improvements to existing prompts
- Report issues or bugs
- Share your experiences and use cases

Please open an issue or pull request to contribute!

## Acknowledgments

**Credit for the CRISPE framework and custom AI methodology:**
- Alexis Castellanos (University of Michigan)
  - https://www.si.umich.edu/people/alexis-castellanos
  - https://psc.isr.umich.edu/events/ai-2/

---

**Questions or feedback?** Feel free to reach out or open an issue!

