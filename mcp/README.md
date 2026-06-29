# MCP — connecting the agent to other tools

**MCP** (Model Context Protocol) is a standard plug for external tools. Each server is installed once, then the agent can call it — Zotero, a database, a browser, an issue tracker, whatever speaks MCP.

## Example: the Zotero MCP

With the Zotero MCP, I can:

- 🔍 Ask "what papers do I have on X?" and have the agent search my library.
- 📄 Let the agent pull a PDF straight from Zotero — including my own highlights and notes.

That turns the agent from something that works *only* on files in the folder into something that reaches into the tools I already use.

> [!CAUTION]
> An MCP **runs code on your machine**, with the same reach as the agent. A malicious or careless server can do real damage. Install only servers you trust.

## How to add one

- Install the MCP server per its own docs.
- Point the agent to an MCP you would like to install and it will guide you through it.
- Then just ask the agent to use it — it discovers the available tools on its own.
