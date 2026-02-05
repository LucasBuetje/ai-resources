# AI Resources
A collection of AI tips, tools and prompts that I find helpful - maybe you do too. Feel free to reach out if you have any questions or feedback (email: lucas.buetje@uni-konstanz.de)

## Customize your AI!
### Why customize?
Most LLMs allow you to create custom agents (Gemini Gems, CustomGPTs, etc.). By creating different agents with different system prompts, you can control both how the AI approaches a task and what you want the output to look like. I find this very uselful for tasks I regularly use AI for, such as summarizing papers. You can find all the prompts for my custom AIs below. But first, I would like to introduce the CRISPE framework that I use for all my custom AIs. Feel free to use and adapt them for your own needs!

### The CRISPE Framework
The CRISPE framework below helps to structure the system prompt. Shoutout to Alexis Castellanos from the University of Michigan for introducing this framework in the PDHP Workshop: Generative AI for Practitioners (Pt 2) (link: https://psc.isr.umich.edu/events/ai-2/).

*   **C -- Capacity:** Define the persona (e.g., "Expert Applied Microeconomics Research Assistant").
*   **R -- Role:** Specific task definition (e.g., "Extract and audit causal identification strategies").
*   **I -- Insight:** Constraints and protocols (e.g., "Negative Constraints: NEVER use conversational filler").
*   **S -- Style:** Tone and formatting (e.g., "Telegraphic, strict LaTeX for math").
*   **P -- Process:** Step-by-step execution instructions (Scan -> Classify -> Audit -> Sanitize -> Output).
*   **E -- Example:** Providing a perfect input/output pair to guide the model.


## Tools I use and my custom AIs for them

### Google Gemini (Chat)
My go-to general purpose AI. I started using it because I got a free year of the Pro version, but it performs very well in LLM comparisons. It offers both Flash (fast) and Pro (complex) models. A nice feature is the ability to use notebooks from NotebookLM as context.
*Note: The lack of chat history without enabling data training is a big downside.*

**My Custom Gems:**
*   **Paper Summarizer:** Two versions - one for [empirical papers](Gemini/empirical_paper_summarizer.md) and one for [literature reviews](Gemini/review_paper_summarizer.md).
*   **[Custom AI Creator](Gemini/custom_ai_creator.md):** A meta-tool to draft the initial CRISPE prompt for new custom agents.
*   **[Paper Podcast Prompter](Gemini/notebooklm_paper_podcast_prompter.md):** Instructions for NotebookLM to create structured podcast scripts from papers.
*   **[Google Scholar Labs Prompter](Gemini/google_scholar_labs_prompter.md):** Helps generate natural language queries for finding papers.
*   **NEPS Codebook and Code:** An agent that "knows" the codebooks and my specific project code to answer data questions.

### Antigravity (Agentic IDE)
An "Agent-first" IDE (think RStudio but for all languages with integrated AI). The agents can view the entire project/subfolders, answer questions, and autonomously debug or rewrite code. You get a "diff" view to accept/reject changes. There are several similar tools out there (e.g. Cursor, Claude Code, Codex by openAI). For everyone with an academic affiliation, VSCode + GitHub Copilot is a great free alternative. 

**[Custom General Instructions](Antigravity/antigravity_general_instructions.md)**

**Custom "Workflows":**
*   **[R Code Developer](Antigravity/r-development/r-development.md):** Helps writing code.
*   **[R Code Reviewer](Antigravity/r-code-auditing/r-code-auditing.md):** Reviews code chunks for syntax and logic errors (checks if code matches comments).
*   **[R Code Formatter](Antigravity/r-code-formatter/r-code-formatter.md):** Enforces consistent styling without altering logic.
*   **[LaTeX Drafter](Antigravity/latex-drafting/latex-drafting.md):** Help drafting documents.
*   **[LaTeX Reviewer](Antigravity/latex-auditing/latex-auditing.md):** Reviews documents section-by-section for formatting and improvements.


### Other Tools
*   **NotebookLM:** Upload your own documents to ask questions or create media from it. Many students love it for studying with flashcards etc. My use case: Uploading a paper to create a podcast for train rides.
*   **Perplexity:** All-purpose AI Chat with search engine and some nice features, e.g. toggles for which sources to use (academic, web, etc.).
*   **Literature Search Tools:** Google Scholar Labs, Elicit, R Discovery - for finding papers using natural language.

