# Custom Google Scholar MCP Server
# Google Scholar MCP

A Model Context Protocol (MCP) server that provides AI agents with specialised tools to query Google Scholar. This server enables language models to retrieve academic metadata, citation counts, and author profiles directly within their context window.
A Model Context Protocol (MCP) server for querying Google Scholar via AI agents. This side project uses the open-source `scholarly` package to fetch citation counts, find papers, and search authors directly.

## Features

This server exposes the following tools to the connected AI client:

* **get_authors_by_title**: Finds the authors of a specific paper by searching its exact title on Google Scholar.
* **get_citation_count**: Retrieves the total citation count for a specific paper.
* **get_author_paper_count**: Finds the total number of papers published by a specific author using Google Scholar profiles.
* **get_all_papers_by_author**: Retrieves a comprehensive list of all papers written by a specific author.

## Prerequisites

* Python 3.10 or higher
* A SerpApi account and API key
* The `uv` package manager (recommended for running MCP servers)
- **Python 3.10 or higher** (Required by the official `mcp` SDK)
- `uv` or `pip`

## Installation

1. Clone this repository to your local machine:
You can install this directly or run it using `uv`:

```bash
git clone https://github.com/yourusername/custom-scholar-mcp.git
cd custom-scholar-mcp
# Clone the repository
git clone <your-repo-url>
cd google_scholar_mcp

```
# Using uv (Recommended)
uv run custom-scholar


2. Install the required dependencies. If you are using standard `pip`:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
# Using standard pip
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .

custom-scholar
```

## Available Tools

The server exposes three tools to the AI agent:
1. `search_author(name)`: Returns author's affiliation, total citations, and h-index.
2. `search_paper(title)`: Returns the paper's authors, abstract, citations, and URL.
3. `get_author_papers(name, limit)`: Returns the most cited papers by a specific author.

## Configuration
## Adding to Claude Desktop

Create a `.env` file in the root directory of the project to store your credentials. You can copy the provided example file:
To use this with Claude Desktop, add the following to your `claude_desktop_config.json`:

```bash
cp .env.example .env

```

Open the `.env` file and populate it with your specific details:

```text
# SerpApi Key (required for Google Scholar search and author profiles)
SERPAPI_API_KEY=your_serpapi_api_key_here

```

## Integration with Claude Desktop

To utilise this server within Claude Desktop, you must configure the application to initialise it upon startup.

Open your Claude Desktop configuration file, which is typically located at:

* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration, ensuring you replace the path with the absolute path to your project directory:

```json
{
  "mcpServers": {
    "custom-scholar": {
    "google-scholar": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/google_scholar_mcp",
        "run",
        "src/google_scholar_mcp/main.py"
      ],
      "cwd": "/absolute/path/to/custom-scholar-mcp",
      "env": {
        "SERPAPI_API_KEY": "your_serpapi_api_key_here"
      }
        "custom-scholar"
      ]
    }
  }
}

```

Restart Claude Desktop. The tools will now appear in the application as available functions for the AI to call.

## Project Structure

```text
custom-scholar-mcp/
├── .env                    
├── .gitignore              
├── pyproject.toml          
├── README.md               
└── src/
    └── google_scholar_mcp/
        ├── __init__.py
        ├── main.py         
        ├── config.py       
        ├── serpapi.py      
        └── tools.py        

```
*Note: Google Scholar frequently rate-limits automated requests. Since this uses `scholarly`, basic blocks are usually handled, but if you do heavy scraping, Scholar might temporarily block your IP.*

## License

This project is licensed under the MIT License

## Author
Funmi Looi-Somoye