import asyncio
from mcp.server.fastmcp import FastMCP
from scholarly import scholarly

# Create the MCP server
mcp = FastMCP("Google Scholar")

@mcp.tool()
async def search_author(name: str) -> str:
    """
    Description:
        Searches for a Google Scholar author by name and returns their citation information.
        
    Parameters:
        name (str): The full or partial name of the author to search for.
        
    Returns:
        str: A formatted string containing the author's details, including affiliation and citation indices, or an error message if unrecognised.
    """
    try:
        # Run blocking scholarly code in a thread
        def _search():
            search_query = scholarly.search_author(name)
            author = next(search_query, None)
            if not author:
                return f"No author found for '{name}'"
            # Fill the author to get citation counts
            return scholarly.fill(author, sections=['basics', 'indices', 'counts'])
        
        author = await asyncio.to_thread(_search)
        if isinstance(author, str):
            return author

        # Format output
        info = [
            f"Name: {author.get('name')}",
            f"Affiliation: {author.get('affiliation', 'N/A')}",
            f"Cited By: {author.get('citedby', 0)}",
            f"h-index: {author.get('hindex', 0)}",
            f"i10-index: {author.get('i10index', 0)}",
            f"Interests: {', '.join(author.get('interests', []))}"
        ]
        return "\n".join(info)

    except StopIteration:
        return f"No author found for '{name}'."
    except Exception as e:
        return f"Error searching author: {e}"

@mcp.tool()
async def search_paper(title: str) -> str:
    """
    Description:
        Searches for a paper by its title on Google Scholar and returns its details.
        
    Parameters:
        title (str): The title of the publication to search for.
        
    Returns:
        str: A formatted string summarising the paper's details, including its abstract and citations, or an error message if unrecognised.
    """
    try:
        def _search():
            search_query = scholarly.search_pubs(title)
            return next(search_query, None)

        paper = await asyncio.to_thread(_search)
        
        if not paper:
            return f"No paper found for '{title}'."

        bib = paper.get('bib', {})
        info = [
            f"Title: {bib.get('title', 'N/A')}",
            f"Author(s): {', '.join(bib.get('author', [])) if isinstance(bib.get('author'), list) else bib.get('author', 'N/A')}",
            f"Venue: {bib.get('venue', 'N/A')} ({bib.get('pub_year', 'N/A')})",
            f"Citations: {paper.get('num_citations', 0)}",
            f"Abstract: {bib.get('abstract', 'N/A')}",
            f"URL: {paper.get('eprint_url', paper.get('pub_url', 'N/A'))}"
        ]
        return "\n".join(info)
    
    except StopIteration:
        return f"No paper found for '{title}'."
    except Exception as e:
        return f"Error searching paper: {e}"

@mcp.tool()
async def get_author_papers(name: str, limit: int = 5) -> str:
    """
    Description:
        Retrieves the most cited papers for a specific author.
        
    Parameters:
        name (str): The full or partial name of the author.
        limit (int): The maximum number of publications to return. Defaults to 5.
        
    Returns:
        str: A formatted list of the author's top papers and their citation counts, or an error message if unrecognised.
    """
    try:
        def _search():
            search_query = scholarly.search_author(name)
            author = next(search_query, None)
            if not author:
                return None
            return scholarly.fill(author, sections=['publications'])

        author = await asyncio.to_thread(_search)
        
        if not author:
            return f"No author found for '{name}'."

        pubs = author.get('publications', [])[:limit]
        if not pubs:
            return f"No publications found for {author.get('name')}."

        results = [f"Top {len(pubs)} papers for {author.get('name')}:"]
        for i, pub in enumerate(pubs, 1):
            bib = pub.get('bib', {})
            results.append(f"{i}. {bib.get('title', 'N/A')} ({bib.get('pub_year', 'N/A')}) - Citations: {pub.get('num_citations', 0)}")
            
        return "\n".join(results)

    except Exception as e:
        return f"Error fetching author papers: {e}"

def run():
    """
    Description:
        Entry point for the custom-scholar-mcp package. Initialises and starts the server.
        
    Parameters:
        None
        
    Returns:
        None
    """
    mcp.run()

if __name__ == "__main__":
    run()

