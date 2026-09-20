# Google Scholar MCP

A Model Context Protocol (MCP) server for querying Google Scholar via AI agents. This server enables language models to retrieve academic metadata, citation counts, and author profiles directly within their context window using the open-source `scholarly` package (no API keys required).

## Features

This server exposes the following tools to the connected AI client:

* **search_author**: Finds an author by name and returns their affiliation, total citations, and h-index.
* **search_paper**: Finds a specific paper by title and returns its abstract, citations, authors, and URL.
* **get_author_papers**: Retrieves a list of the most cited papers by a specific author.

## Prerequisites

* **Python 3.10 or higher** (Required by the official `mcp` SDK)
* The `uv` package manager (recommended) or standard `pip`.

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/FunmiLS/google_scholar_mcp.git
cd google_scholar_mcp
```

2. Run the server using `uv` (Recommended):
```bash
uv run custom-scholar
```

Alternatively, you can install it using standard `pip`:
```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .
custom-scholar
```

## Integration with Claude Desktop

To utilise this server within Claude Desktop, add the following to your `claude_desktop_config.json` file.

* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-scholar": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/google_scholar_mcp",
        "run",
        "custom-scholar"
      ]
    }
  }
}
```

*Note: Google Scholar frequently rate-limits automated requests. Since this uses `scholarly`, basic blocks are usually handled, but if you do heavy scraping, Scholar might temporarily block your IP.*

## Project Structure

```text
google_scholar_mcp/
├── .gitignore              
├── pyproject.toml          
├── README.md               
├── LICENSE
├── tests/
│   └── test_tools.py
└── src/
    └── google_scholar_mcp/
        ├── __init__.py
        ├── main.py         
        └── tools.py        
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author
Funmi Looi-Somoye