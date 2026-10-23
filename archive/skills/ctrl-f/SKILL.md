---
name: ctrl-f
origin: self
description: For each claim in a passage of draft, name the Zotero source that backs it and give a verbatim string to Ctrl-F for inside that source.
user-invocable: true
allowed-tools: Read, Grep, Bash(pdftotext*), Bash(grep*), ToolSearch, mcp__zotero__zotero_semantic_search, mcp__zotero__zotero_search_items, mcp__zotero__zotero_search_by_citation_key, mcp__zotero__zotero_get_item_metadata, mcp__zotero__zotero_get_item_fulltext, mcp__zotero__zotero_get_item_children, mcp__zotero__zotero_get_attachment_path, mcp__zotero__zotero_read_pdf_pages
argument-hint: '[passage | file.tex | file.tex:120-160]'
---

# ctrl-f

Hand back, per claim in the passage, the source that backs it and a **verbatim** string the
user can Ctrl-F for in that source's PDF. Read-only — never edit the draft.

## Input

`$ARGUMENTS` is the passage itself, a file path, or `file.tex:120-160`. With nothing given,
ask which passage — don't pick one.

## 1. Split into claims

A claim is one assertion a referee could demand a citation for. A sentence carrying two
claims becomes two rows. Setup, transitions, and statements about the paper's own contribution
are not claims. Done when every sentence in the passage is either a numbered claim or named
explicitly as carrying none.

## 2. Find the source

The normal case is a bare claim with nothing attached: search the library for it —
`zotero_semantic_search`, then `zotero_search_items` on the claim's terms.

If the claim does carry a pointer — any `\cite`/`\textcite`/`\parencite` variant, a
`[@key]`, or plain prose like "Smith (2020) shows" — treat it as a hypothesis, not the answer:
step 3 either confirms it or moves the claim to Unsupported. Never let a pointer skip the
lookup.

Retrieval goes through the Zotero MCP; load its schemas with `ToolSearch` before the first call.

## 3. Locate the string

Pull the source's text with `zotero_get_item_fulltext` and search it for the claim's terms.
Fall back to `pdftotext` on the attachment path when the full text is unavailable.

Copy the hit out of the retrieved text: 4–10 words, unique in the document, no ellipsis, no
rewrapping. A string that was typed from memory or paraphrased is worthless — it is precisely
the thing Ctrl-F will not find. Prefer a span with no hyphenated line break and no `fi`/`fl`
ligature; those are what a PDF viewer's search misses. Note the page or section it sits in.

## 4. Report

A table: Claim | Source (Author Year) | Page/section | Ctrl-F string. Below it, one line per
distinct source giving the PDF's **local file path** as a markdown link — `zotero_get_attachment_path`
returns it, and the path is what the user can actually click. A `zotero://` link is dead in the
Claude desktop app, so don't emit one here; never show a bare item key either.

Then an **Unsupported** list: claims where no source was found, and cited claims whose source
turned out not to say it — the second kind named as such, since it is a live citation error in
the draft. Say a claim is unsupported rather than filling its row with a plausible string.
