---
name: scholar
description: >
  Search for NEW papers on Google Scholar and Google Scholar Labs via Chrome,
  or paste a list of papers (e.g. from claude.ai Research mode) to act on them.
  Use this skill — NOT Zotero MCP tools — whenever the user wants to discover
  or find papers from the web, or when they paste paper titles/DOIs/URLs to
  summarize, ask questions about, or add to Zotero.
  Zotero MCP is only for the user's existing personal library.
argument-hint: "<search query or natural language question>"
---

# Scholar

Search academic literature using both Google Scholar and Google Scholar Labs — run together, driven through your real Chrome browser.

**Input:** `$ARGUMENTS` — a search query, a natural language question, or a pasted list of papers.

**Requirements:** The [Claude Code Chrome extension](https://claude.ai/code) must be installed and active. This skill uses `mcp__Claude_in_Chrome__*` tools to drive a sandboxed browser tab.

---

## Step 1: Detect input type

Examine `$ARGUMENTS`:

- **Search query** — keywords or a question → run Steps 2A and 2B in sequence, then present results together
- **Pasted paper list** — the user pasted titles, DOIs, URLs, or a bibliography (e.g. from claude.ai Research mode) → go to **Step 2C**

If the input is empty, ask: "Paste a list of papers or enter a search query."

---

## Step 2A: Google Scholar — keyword search

1. URL-encode the query (replace spaces with `+`, encode special characters)
2. Navigate:
   ```
   mcp__Claude_in_Chrome__navigate → https://scholar.google.com/scholar?q=<encoded-query>
   ```
3. Read the page:
   ```
   mcp__Claude_in_Chrome__get_page_text
   ```
4. Parse and display the **top 10 results** as a markdown table:

   | # | Title | Authors | Year | Cited by | Snippet |
   |---|-------|---------|------|----------|---------|

   If the page text is hard to parse, use:
   ```
   mcp__Claude_in_Chrome__javascript_tool
   ```
   with a script that extracts `.gs_ri` result blocks (Scholar's CSS class for result entries).

5. Hold the results — present after Step 2B is also complete.

---

## Step 2B: Google Scholar Labs — natural language query

Scholar Labs provides an AI-powered natural language interface to the literature.

1. Navigate to the Labs page:
   ```
   mcp__Claude_in_Chrome__navigate → https://scholar.google.com/scholar_labs
   ```
2. Read the page to discover the current UI structure:
   ```
   mcp__Claude_in_Chrome__read_page
   ```
   Scholar Labs is experimental — do not assume a fixed layout. Find the query input field dynamically.

3. Locate the text input and submit the query. Try in order:
   - `mcp__Claude_in_Chrome__find` → search for an `<input>` or `<textarea>` element
   - `mcp__Claude_in_Chrome__javascript_tool` → focus the input, set its value, and submit the form

4. Wait for the response to load, then extract the page content:
   ```
   mcp__Claude_in_Chrome__get_page_text
   ```

5. Present:
   - The **Labs-generated summary** or response verbatim (clearly labelled as AI-generated)
   - A **list of papers cited or surfaced** by the Labs response, formatted as:

     | # | Title | Authors | Year |
     |---|-------|---------|------|

6. Now present both results together: Scholar table first, then the Labs response and its paper list.

---

## Step 2C: Paste mode — user-provided paper list

For when the user pastes results from claude.ai Research mode or any other source.

1. Parse the pasted text to extract individual papers. Look for:
   - DOIs (e.g. `10.xxxx/...`)
   - URLs (e.g. NBER, SSRN, arXiv, journal links)
   - Titles with author/year info
2. Present the parsed papers as a numbered table:

   | # | Title | Authors | Year | DOI/URL |
   |---|-------|---------|------|---------|

3. If any entries are ambiguous or unparseable, flag them and ask the user to clarify.
4. Proceed directly to **Step 3** (follow-up loop) — the user can now act on papers by number.

---

## Step 3: Follow-up loop

After presenting results, always offer:

```
Options:
  [1] Summarize paper #N
  [2] Ask a question about paper #N
  [3] Add paper #N to Zotero
  [4] Refine or new query
  [5] Done
```

Repeat the menu after each action (except Done).

---

### Option 1 — Summarize paper

Delegates to Gemini's `paper-summarizer` skill for a structured empirical audit.

1. Extract the paper's URL from the results table (Scholar result link or DOI link)
2. Navigate to the paper page in Chrome (`mcp__Claude_in_Chrome__navigate`), look for a direct PDF link
3. If PDF is accessible: download to the current project root as `paper.pdf`
4. Call Gemini:
   ```
   Ask-Gemini → "Use your paper-summarizer skill to summarize @paper.pdf.
   Do NOT read any other files in the project. Focus exclusively on the PDF content."
   ```
5. Print the Gemini summary inline to the user
6. Save the summary to `obsidian/claude-output/@[BIBKEY].md` — extract BIBKEY from the Gemini response or construct as `AuthorYear` (e.g. `Card1994`)
7. Clean up: `rm paper.pdf` (throwaway copy)
8. If no PDF is freely accessible: extract the abstract from the paper page via Chrome, present a lightweight summary, and note that the full structured audit requires PDF access

---

### Option 2 — Ask a question about a paper

1. Same PDF acquisition as Option 1 (steps 1–3)
2. Call Gemini with the user's specific question:
   ```
   Ask-Gemini → "<user's question> @paper.pdf
   Do NOT read any other files in the project. Focus exclusively on the PDF content.
   Cite exact sections, page numbers, and quote relevant sentences verbatim."
   ```
3. Print Gemini's response inline
4. Clean up: `rm paper.pdf`
5. If no PDF available: answer from abstract + Scholar Labs context already gathered

---

### Option 3 — Add paper to Zotero

1. Extract DOI or URL from the selected result
2. Call `zotero_get_collections` to list the user's existing collections
3. Infer the best-matching collection from the paper's topic/title and the collection names
4. Present the suggestion: "Adding to collection **X** — correct?" (user can override)
5. Call `zotero_add_by_doi` (if DOI available) or `zotero_add_by_url` with the chosen collection

---

### Option 4 — Refine or new query

Run Steps 2A and 2B again with the user's new or refined query.

### Option 5 — Done

Stop.

---

## Notes

- **Login state:** The skill uses the user's real browser session. If Scholar Labs requires a Google login, the user's existing session handles it.
- **Bot detection:** Because the skill drives a real browser (not a headless scraper), Google's bot detection is bypassed.
- **Scholar Labs URL:** If `https://scholar.google.com/scholar_labs` redirects or changes, read the landing page and adapt to the current structure before proceeding.
- **Failures:** If a page does not load or the expected elements are not found, report the error clearly and suggest the user check their browser tab.
