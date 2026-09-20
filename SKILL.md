---
name: google-scholar-mcp
description: >
  Use this skill whenever the user asks about academic papers, researchers,
  citation counts, h-indexes, author profiles, or anything that requires
  looking up information on Google Scholar. This skill teaches the agent
  how to call the three Google Scholar MCP tools correctly and how to
  combine them to answer research questions effectively.
---

# Google Scholar MCP Skill

You have access to a **Google Scholar MCP server** that lets you query
Google Scholar in real time — no API key required. Use it whenever the
user needs information about academic publications or researchers.

---

## Available Tools

### 1. `search_author`
Look up a researcher's profile by name.

**When to use:**
- "Who is [researcher]?"
- "What is [person]'s h-index / citation count / affiliation?"
- "What are [person]'s research interests?"

**Input:**
| Parameter | Type   | Description                          |
|-----------|--------|--------------------------------------|
| `name`    | string | Full or partial name of the author   |

**Returns:** Name, affiliation, total citations, h-index, i10-index, and research interests.

**Example call:**
```
search_author(name="Yoshua Bengio")
```

---

### 2. `search_paper`
Find a specific paper by its title.

**When to use:**
- "Find the paper '[title]'"
- "How many citations does '[title]' have?"
- "What is the abstract of '[title]'?"
- "Who wrote '[title]'?"

**Input:**
| Parameter | Type   | Description                          |
|-----------|--------|--------------------------------------|
| `title`   | string | Title (or partial title) of the paper|

**Returns:** Title, authors, venue & year, citation count, abstract, and URL.

**Example call:**
```
search_paper(title="Attention is All You Need")
```

---

### 3. `get_author_papers`
Retrieve an author's most-cited publications.

**When to use:**
- "What are [person]'s top papers?"
- "List the most cited works by [author]"
- "Give me [N] papers by [researcher]"

**Input:**
| Parameter | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| `name`    | string  | Full or partial name of the author               |
| `limit`   | integer | Max papers to return (optional, defaults to 5)   |

**Returns:** A ranked list of papers with titles, publication years, and citation counts.

**Example call:**
```
get_author_papers(name="Geoffrey Hinton", limit=10)
```

---

## How to Combine the Tools

Many research questions benefit from chaining the tools together:

| User Goal | Suggested Tool Chain |
|---|---|
| Summarise a researcher's impact | `search_author` → `get_author_papers` |
| Compare two authors' h-indexes | `search_author` × 2 |
| Find a paper, then look up its first author | `search_paper` → `search_author` |
| Build a reading list on a topic | `search_paper` × N (different titles) |

---

## Behaviour Guidelines

- **Always try the tool first** before saying you cannot access Google Scholar.
- **Partial names work** — use the most distinctive part of the name if the full name is ambiguous (e.g. `"LeCun"` instead of `"Yann LeCun"`).
- **Rate limits** — Google Scholar may occasionally throttle requests. If a tool returns an error mentioning a block or CAPTCHA, let the user know and suggest retrying after a short wait.
- **Accuracy** — results come directly from Google Scholar via `scholarly`. Treat citation counts as approximate (Scholar updates them periodically).
- **No API key needed** — this MCP uses the open-source `scholarly` library. No credentials are required from the user.

---

## Example Prompts You Can Handle

- *"What is Andrew Ng's h-index and what institution is he at?"*
- *"Find the paper 'BERT: Pre-training of Deep Bidirectional Transformers' and tell me how many times it's been cited."*
- *"List the 7 most cited papers by Demis Hassabis."*
- *"Compare the citation counts of Yann LeCun and Yoshua Bengio."*
- *"What are the research interests of Fei-Fei Li?"*

