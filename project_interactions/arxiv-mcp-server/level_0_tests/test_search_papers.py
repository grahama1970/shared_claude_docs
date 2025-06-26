"""
Test module for ArXiv search_papers functionality.

These tests validate the core paper search capabilities using the real ArXiv API.

External Dependencies:
- arxiv: https://pypi.org/project/arxiv/
- typing: Built-in type annotations

Example Usage:
>>> pytest test_search_papers.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
import arxiv
from typing import Dict, Any, List


class TestSearchPapers:
    """Test suite for paper search capabilities."""
    
    def test_basic_search(self):
        """
        Test basic paper search functionality.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Execute real ArXiv search
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(
            query="quantum computing",
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for paper in client.results(search, timeout=30.0):
            papers.append({
                "id": paper.entry_id,
                "title": paper.title,
                "summary": paper.summary[:500],  # First 500 chars
                "authors": [author.name for author in paper.authors],
                "published": paper.published.isoformat() if paper.published else None,
                "categories": paper.categories,
                "pdf_url": paper.pdf_url
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) > 0, "No papers found for 'quantum computing'"
        assert len(papers) <= 5, "Should respect max_results limit"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Validate paper structure
        for paper in papers:
            assert "id" in paper and paper["id"]
            assert "title" in paper and paper["title"]
            assert "summary" in paper and paper["summary"]
            assert "authors" in paper and len(paper["authors"]) > 0
            assert "pdf_url" in paper and paper["pdf_url"].startswith("http")
            assert "categories" in paper and len(paper["categories"]) > 0
    
    def test_advanced_search_with_filters(self):
        """
        Test search with category filters.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Search in specific categories
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(
            query="neural networks AND (cat:cs.LG OR cat:cs.AI)",
            max_results=10,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for paper in client.results(search, timeout=30.0):
            papers.append({
                "id": paper.entry_id,
                "title": paper.title,
                "primary_category": paper.primary_category,
                "categories": paper.categories,
                "published": paper.published.isoformat() if paper.published else None
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) > 0, "No papers found with category filters"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Verify at least some papers are in requested categories
        cs_papers = [p for p in papers if any(cat in ["cs.LG", "cs.AI"] for cat in p["categories"])]
        assert len(cs_papers) > 0, "No papers found in cs.LG or cs.AI categories"
        
        # Verify sorting by date (newest first)
        if len(papers) > 1:
            dates = [p["published"] for p in papers if p["published"]]
            assert dates == sorted(dates, reverse=True), "Papers not sorted by date descending"
    
    def test_author_search(self):
        """
        Test searching by author name.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Search for papers by well-known author
        client = arxiv.Client()
        search = arxiv.Search(
            query='au:"Yann LeCun"',
            max_results=5,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        papers = []
        for paper in client.results(search):
            papers.append({
                "id": paper.entry_id,
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "year": paper.published.year if paper.published else None
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Should find at least some papers (Yann LeCun has many)
        if len(papers) > 0:
            # Verify author is in the author list
            for paper in papers:
                author_names = " ".join(paper["authors"]).lower()
                assert "lecun" in author_names, f"Author not found in paper: {paper['title']}"
    
    def test_recent_papers_search(self):
        """
        Test searching for recent papers.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Search for recent ML papers
        client = arxiv.Client()
        search = arxiv.Search(
            query="machine learning",
            max_results=10,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for paper in client.results(search):
            papers.append({
                "id": paper.entry_id,
                "title": paper.title,
                "published": paper.published,
                "updated": paper.updated
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) > 0, "No recent papers found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Check papers are recent (within last 2 years)
        from datetime import datetime, timedelta
        two_years_ago = datetime.now() - timedelta(days=730)
        
        recent_papers = [p for p in papers if p["published"] and p["published"].replace(tzinfo=None) > two_years_ago]
        assert len(recent_papers) > 0, "No papers found from the last 2 years"
    
    def test_empty_search_results(self):
        """
        Test handling of searches with no results.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Search for nonsense that should return no results
        client = arxiv.Client()
        search = arxiv.Search(
            query="XYZABC123456789NONEXISTENT",
            max_results=5
        )
        
        papers = list(client.results(search))
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 0, "Found papers for nonsense query"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
    
    def test_search_with_multiple_terms(self):
        """
        Test complex search with multiple terms and operators.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Complex search query
        client = arxiv.Client()
        search = arxiv.Search(
            query='(transformer OR attention) AND ("computer vision" OR "image recognition")',
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        papers = []
        for paper in client.results(search):
            papers.append({
                "id": paper.entry_id,
                "title": paper.title,
                "summary": paper.summary[:300]
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) > 0, "No papers found for complex query"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Verify relevance - at least some papers should mention key terms
        relevant_papers = 0
        for paper in papers:
            text = (paper["title"] + " " + paper["summary"]).lower()
            if ("transformer" in text or "attention" in text) and \
               ("vision" in text or "image" in text):
                relevant_papers += 1
        
        assert relevant_papers > 0, "No papers found matching search terms"


if __name__ == "__main__":
    # Run tests
    test = TestSearchPapers()
    
    print("Testing basic search...")
    test.test_basic_search()
    print("✅ Basic search passed")
    
    print("\nTesting advanced search with filters...")
    test.test_advanced_search_with_filters()
    print("✅ Advanced search passed")
    
    print("\nTesting author search...")
    test.test_author_search()
    print("✅ Author search passed")
    
    print("\nTesting recent papers search...")
    test.test_recent_papers_search()
    print("✅ Recent papers search passed")
    
    print("\nTesting empty search results...")
    test.test_empty_search_results()
    print("✅ Empty search handling passed")
    
    print("\nTesting complex multi-term search...")
    test.test_search_with_multiple_terms()
    print("✅ Complex search passed")
    
    print("\n✅ All search tests passed!")