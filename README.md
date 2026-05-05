# AI Resources

A collection of AI tools, setups, and prompts for academic research and writing — focused on what I actually use day-to-day. Feel free to reach out: lucas.buetje.economist@outlook.com

**Disclaimer:** All tools, scripts, and prompts are provided as-is. Use them at your own risk. I am not responsible for any data loss or other issues that may arise from their use.


## AI Chat vs Agentic AI — what's the difference?

Before diving in, a quick look at the two types of AI uses this repo covers:

### AI Chat

You type a message, the AI responds with text. It cannot access your files, run code, or take any action on your computer. It may be able to create files you can download, saving you some of the copy-pasting. But in essence, it's a capable conversation partner.

Examples: [Gemini](https://gemini.google.com), [Claude.ai](https://claude.ai), [ChatGPT](https://chat.openai.com), [Perplexity](https://perplexity.ai)

### Agentic AI (AI coding agents)

The AI can autonomously read and modify files, run terminal commands, browse the web, and execute multi-step tasks. The ability to run terminal commands means that it can, in principle, do ANYTHING AND EVERYTHING that your computer can do — with all the risks and benefits that come along. Both are hard to understate in my view.

Examples: [Claude Code](https://claude.ai/code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.sh), [Windsurf](https://windsurf.com)

### A note on agent risks

Usually, you decide which folder an AI agent can access (e.g. a project folder). It is not supposed to touch anything outside of that folder (although it may do that if you allow it to!). Even so, when an AI agent has access to your file system, it can do things that are hard to undo. Before using any agentic AI tool, please know:

- **File access is real.** The agent reads and writes actual files on your computer. It can overwrite things if you're not careful.
- **Be as careful as always when installing stuff from the internet.** Most AI agents allow you to install plugins/connectors (MCPs) to make the agent even more capable. Be very careful when installing plugins etc. from untrusted sources. With file access, an injected malicious prompt can do a lot of damage!
- **Sensitive files may be in scope.** If your project folder contains API keys, credentials, or personal data, the agent can read them. Keep anything sensitive outside the folder you are letting the AI Agent work in (unless you know what you're doing and that the data is not used for training etc.).
- **Compounding errors are possible.** An agent can make a mistake and then confidently build more work on top of it.

**Best practices:** Start in Plan/Preview mode before letting the agent execute anything. Extensively use version control (e.g. github) to be able to revert changes from the AI.


## Agentic Coding

Now that I have warned you, let's get to the fun stuff! How do I actually use AI Agents?

### My workflow

When I talk to the AI agent, I think of it as a very capable and fast research assistant - but also one that needs a some guidance and thinking to have a well-defined to do list before executing (at least for complex tasks). This is how  start in a folder that the agent has never seen before:

0. **Set up global instructions file (once)** - tells the agent how to behave anytime you interact with it. See [`ai-agent/README.md`](ai-agent/README.md) for a template.

1. **Set up a new project with `/init` (once per folder)** — this creates a `CLAUDE.md` in your project folder. The agent reads the codebase and writes down what it finds: folder structure, conventions, key files. From that point on, every new session starts with the agent reading that file, so it always has context. While working, I sometimes update this with new rules/conventions for this project (e.g. "always recompile a LaTeX document after changing it and if it fails, fix until it works").

2. **Work with the agent:**
   - **(a) Plan mode first (complex tasks)** — before the agent touches any file, it lays out exactly what it intends to do. Review the plan, push back or refine it, then let it execute.
   - **(b) Just tell it what to do** — for simpler tasks, describe what you want and watch it work.

3. **Repeat step 2 for the next task.**

- **Skills** - for specific tasks, you can create so-called "skills" that are essentially instruction manuals for the agent so you dont have to explain how to summarize a paper in the way you like it every time.

### Claude Code vs. OpenCode (with GWDG)
In my workflow, I mainly use Claude Code on the 100$ Max plan, but recently experimented with OpenCode, an OpenSource alternative that you can connect to any LLM via an API. I use the models provided by the "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen" (GWDG), but you can use any API that you get your hands on. 

| | [Claude Code](https://claude.ai/code) | [OpenCode](https://opencode.ai) + GWDG |
|---|---|---|
| Cost | Subscription or API usage | Free for GWDG/Academic Cloud users |
| Models | Claude (Anthropic) - frontier models | open-weight models - less capable, but still very good (and getting better) |
| Data handling | Anthropic's privacy policy | Processed on GWDG servers in Germany |
| Open source | No | Yes (MIT license) |
| Global instruction file | `~/.claude/CLAUDE.md` | `~/.config/opencode/AGENTS.md` |
| Project instruction file | `CLAUDE.md` | `CLAUDE.md` (same file — both tools read it) |
| Skills | `~/.claude/skills/` | `~/.config/opencode/commands/` |

OpenCode setup guide (for GWDG/Academic Cloud users): **[ai-agent/gwdg-opencode-setup.md](ai-agent/gwdg-opencode-setup.md)**

### Skills

Slash commands I've adopted into my workflow. Most of them are copied from or inspired by Scott Cunningham. Read his great blog about Claude Code here: https://causalinf.substack.com/s/claude-code. Each folder in [`ai-agent/skills/`](ai-agent/skills/) is a self-contained skill. See [`ai-agent/README.md`](ai-agent/README.md) for installation.

| Skill | Command | What it does |
|---|---|---|
| [Deck](ai-agent/skills/deck/) | `/deck` | Build or edit a Beamer slide deck following evidence-based rhetoric principles. Includes [The Rhetoric of Decks](ai-agent/skills/deck/rhetoric.md) — a knowledge base on what makes presentations actually work. |
| [Devil's Advocate](ai-agent/skills/devils-advocate/) | `/devils-advocate` | Challenge a slide deck with 5–7 specific pedagogical and rhetorical questions. Works for both teaching and research presentations. |
| [Referee 2](ai-agent/skills/referee2/) | `/referee2` | Full empirical research audit + cross-language replication (R and Python). Five structured audits with a formal referee report and Beamer presentation. For economists and quantitative researchers. |
| [Revise](ai-agent/skills/revise/) | `/revise [report]` | Respond to referee or reviewer comments interactively — one at a time, classified and drafted with your approval at every step. |
| [Empirical Paper Summarizer](ai-agent/skills/empirical-paper-summarizer/) | `/summarize-paper [PDF]` | Extract and audit causal identification strategies from empirical economics papers. Structured summary with methodology, findings, and table references. |

<details>
<summary>Older system prompts (R coding, LaTeX drafting)</summary>

The [`archive/AgenticIDE/`](archive/AgenticIDE/) folder contains system prompts I used with earlier agentic tools. They still work — paste into any tool's custom instructions or a project `CLAUDE.md` — but I no longer actively maintain them.

</details>

---

## Custom Prompts for AI Chat

These prompts work with any AI chat tool — Gemini, Claude.ai, ChatGPT, or similar. They're structured using the CRISPE framework.

### The CRISPE Framework

CRISPE helps structure system prompts for custom AI agents. Credit to Alexis Castellanos (University of Michigan, [PDHP Workshop: Generative AI for Practitioners](https://psc.isr.umich.edu/events/ai-2/)).

| Letter | Meaning | Example |
|---|---|---|
| **C** — Capacity | Define the persona | "Expert Applied Microeconomics Research Assistant" |
| **R** — Role | Specific task definition | "Extract and audit causal identification strategies" |
| **I** — Insight | Constraints and protocols | "NEVER use conversational filler" |
| **S** — Style | Tone and formatting | "Telegraphic, strict LaTeX for math" |
| **P** — Process | Step-by-step execution | Scan → Classify → Audit → Sanitize → Output |
| **E** — Example | A perfect input/output pair | Shows the model exactly what you want |

### Custom AIs

My custom AI chatbots. The feature is called a little different across AI tools (Gemini Gems, Claude Projects etc.). The important part is that you **do not** just copy paste this into every new chat, it needs to be stored and available somewhere.

| Custom AI | What it does |
|---|---|
| [Empirical Paper Summarizer](ai-chat/empirical_paper_summarizer.md) | Structured summary of empirical papers: data, identification strategy, main results |
| [Review Paper Summarizer](ai-chat/review_paper_summarizer.md) | Summary of literature reviews and survey papers |
| [Custom AI Creator](ai-chat/custom_ai_creator.md) | Meta-tool: drafts CRISPE prompts for new custom agents |
| [Paper Podcast Prompter](ai-chat/notebooklm_paper_podcast_prompter.md) | Instructions for NotebookLM to create structured podcast scripts from papers |
| [Google Scholar Labs Prompter](ai-chat/google_scholar_labs_prompter.md) | Generates natural language queries for Google Scholar Labs |

**Note on chat history:** Gemini doesn't save chat history by default without enabling data training. I use [SaveChat for Gemini](https://chromewebstore.google.com/detail/savechat-%E2%80%93-for-gemini-ai/blndbnmpkgfoopgmcejnhdnepfejgipe) to export chats and [this script](ai-chat/move_gemini_chats.sh) to file them.

---

## Other Tools

- **[NotebookLM](https://notebooklm.google.com):** Upload your own documents to generate summaries, Q&A, or audio overviews. My use case: uploading a paper to create a podcast for train rides.
- **[Perplexity](https://perplexity.ai):** AI chat with web search and source-type toggles (academic, news, web, etc.).
- **Literature search:** [Google Scholar Labs](https://scholar.google.com/scholar_labs), [Elicit](https://elicit.com), [R Discovery](https://discovery.researcher.life/) — natural language paper search across different disciplines.
