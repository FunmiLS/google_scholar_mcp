import pytest
from unittest.mock import MagicMock
from google_scholar_mcp.tools import search_author, search_paper, get_author_papers

@pytest.fixture
def mock_scholarly(mocker):
    """Mocks the external scholarly API to prevent actual network calls during testing."""
    return mocker.patch('google_scholar_mcp.tools.scholarly')

@pytest.mark.asyncio
async def test_search_author_found(mock_scholarly):
    # Setup mock returns
    mock_scholarly.search_author.return_value = iter([{"name": "Albert Einstein"}])
    mock_scholarly.fill.return_value = {
        "name": "Albert Einstein",
        "affiliation": "Institute for Advanced Study",
        "citedby": 99999,
        "hindex": 100,
        "i10index": 500,
        "interests": ["physics"]
    }
    
    # Execute the tool
    result = await search_author("Albert Einstein")
    
    # Assert formatting is correct
    assert "Albert Einstein" in result
    assert "Institute for Advanced Study" in result
    assert "99999" in result
    assert "physics" in result
    mock_scholarly.search_author.assert_called_once_with("Albert Einstein")

@pytest.mark.asyncio
async def test_search_author_not_found(mock_scholarly):
    # Setup empty mock return
    mock_scholarly.search_author.return_value = iter([])
    
    # Execute
    result = await search_author("Unknown Person")
    
    # Assert
    assert "No author found for 'Unknown Person'" in result

@pytest.mark.asyncio
async def test_search_paper_found(mock_scholarly):
    mock_paper = {
        "bib": {
            "title": "Relativity",
            "author": ["A Einstein"],
            "venue": "Annalen der Physik",
            "pub_year": "1905",
            "abstract": "A theory of relativity."
        },
        "num_citations": 1000,
        "pub_url": "http://example.com"
    }
    mock_scholarly.search_pubs.return_value = iter([mock_paper])
    
    result = await search_paper("Relativity")
    
    assert "Relativity" in result
    assert "A Einstein" in result
    assert "1905" in result
    assert "1000" in result
    mock_scholarly.search_pubs.assert_called_once_with("Relativity")

@pytest.mark.asyncio
async def test_get_author_papers_found(mock_scholarly):
    # Setup mock author with publications
    mock_scholarly.search_author.return_value = iter([{"name": "Albert Einstein"}])
    mock_scholarly.fill.return_value = {
        "name": "Albert Einstein",
        "publications": [
            {"bib": {"title": "Paper 1", "pub_year": "1905"}, "num_citations": 100},
            {"bib": {"title": "Paper 2", "pub_year": "1915"}, "num_citations": 200}
        ]
    }
    
    result = await get_author_papers("Albert Einstein", limit=2)
    
    assert "Top 2 papers for Albert Einstein:" in result
    assert "1. Paper 1 (1905)" in result
    assert "2. Paper 2 (1915)" in result

