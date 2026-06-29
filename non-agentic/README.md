# Non-agentic AI

The rest of my AI toolkit — plain chat tools and assistants that *don't* act on your computer. Useful, but secondary to the [agents](../README.md) this repo is mostly about.

## AI Chat vs Agentic AI

- **AI Chat** — you type, it replies with text. No access to your files or computer; it may produce files you download, but it can't act. *(Gemini, Claude.ai, ChatGPT, Perplexity.)*
- **Agentic AI** — reads/writes files, runs commands, completes multi-step tasks on its own. That's the [main repo](../README.md).

## Custom prompts for AI Chat

- Prompts for any chat tool (Gemini, Claude.ai, ChatGPT), structured with the **CRISPE** framework.
- **Store them somewhere reusable** (Gemini Gems, Claude Projects, …) — don't paste them into every new chat.

### The CRISPE framework

Credit: Alexis Castellanos (University of Michigan, [PDHP Workshop](https://psc.isr.umich.edu/events/ai-2/)).

| Letter | Meaning | Example |
|---|---|---|
| **C** — Capacity | Define the persona | "Expert Applied Microeconomics Research Assistant" |
| **R** — Role | Specific task | "Extract and audit causal identification strategies" |
| **I** — Insight | Constraints/protocols | "NEVER use conversational filler" |
| **S** — Style | Tone and formatting | "Telegraphic, strict LaTeX for math" |
| **P** — Process | Step-by-step execution | Scan → Classify → Audit → Sanitize → Output |
| **E** — Example | A perfect input/output pair | Shows the model exactly what you want |

### The prompts

| Custom AI | What it does |
|---|---|
| [Empirical Paper Summarizer](empirical_paper_summarizer.md) | Structured summary: data, identification strategy, main results |
| [Review Paper Summarizer](review_paper_summarizer.md) | Summary of literature reviews and survey papers |
| [Custom AI Creator](custom_ai_creator.md) | Meta-tool: drafts CRISPE prompts for new custom agents |
| [Paper Podcast Prompter](notebooklm_paper_podcast_prompter.md) | NotebookLM instructions for podcast scripts from papers |
| [Google Scholar Labs Prompter](google_scholar_labs_prompter.md) | Natural-language queries for Google Scholar Labs |

- **Chat history:** Gemini doesn't save history without enabling data training. I use [SaveChat for Gemini](https://chromewebstore.google.com/detail/savechat-%E2%80%93-for-gemini-ai/blndbnmpkgfoopgmcejnhdnepfejgipe) to export and [this script](move_gemini_chats.sh) to file them.

## Other tools

- **[NotebookLM](https://notebooklm.google.com):** upload documents for summaries, Q&A, or audio overviews — I turn a paper into a podcast for train rides.
- **[Perplexity](https://perplexity.ai):** AI chat with web search and source-type toggles.
- **Literature search:** [Google Scholar Labs](https://scholar.google.com/scholar_labs), [Elicit](https://elicit.com), [R Discovery](https://discovery.researcher.life/).
