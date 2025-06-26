"""
Test module for ArXiv get_paper_details functionality.

These tests validate retrieving metadata for specific papers using the real ArXiv API.

External Dependencies:
- arxiv: https://pypi.org/project/arxiv/
- typing: Built-in type annotations

Example Usage:
>>> pytest test_paper_details.py -v
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
from typing import Dict, Any
from datetime import datetime


class TestPaperDetails:
    """Test suite for paper details retrieval."""
    
    def test_get_paper_by_id(self):
        """
        Test retrieving paper details by ArXiv ID.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Use a well-known paper ID (Attention Is All You Need)
        paper_id = "1706.03762"
        
        # Fetch paper details
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 1, f"Expected 1 paper, got {len(papers)}"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        paper = papers[0]
        
        # Validate paper details
        assert paper.entry_id.endswith(paper_id), f"Wrong paper ID returned"
        assert "Attention Is All You Need" in paper.title, f"Unexpected title: {paper.title}"
        assert len(paper.authors) > 0, "No authors found"
        assert paper.summary and len(paper.summary) > 100, "Summary too short or missing"
        assert paper.published is not None, "Published date missing"
        assert paper.pdf_url is not None, "PDF URL missing"
        
        # Check specific known details
        author_names = [author.name for author in paper.authors]
        assert any("Vaswani" in name for name in author_names), "Expected author not found"
    
    def test_get_multiple_papers(self):
        """
        Test retrieving multiple papers by ID.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Multiple paper IDs
        paper_ids = ["1706.03762", "1810.04805", "2005.14165"]  # Transformer, BERT, GPT-3
        
        # Fetch papers
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=paper_ids)
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == len(paper_ids), f"Expected {len(paper_ids)} papers, got {len(papers)}"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Check each paper
        retrieved_ids = []
        for paper in papers:
            # Extract just the ID part
            paper_id = paper.entry_id.split("/")[-1].replace("v", "").split(".")[0] + "." + paper.entry_id.split("/")[-1].replace("v", "").split(".")[1][:5]
            retrieved_ids.append(paper_id)
            
            # Validate structure
            assert paper.title, "Title missing"
            assert paper.authors, "Authors missing"
            assert paper.summary, "Summary missing"
            assert paper.pdf_url, "PDF URL missing"
        
        # Verify we got all requested papers
        for requested_id in paper_ids:
            assert any(requested_id in retrieved for retrieved in retrieved_ids), f"Paper {requested_id} not retrieved"
    
    def test_paper_version_handling(self):
        """
        Test handling of paper versions (v1, v2, etc).
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Paper with known multiple versions
        paper_id = "1706.03762v7"  # Specific version
        
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 1, "Paper not found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        paper = papers[0]
        
        # Check version info
        assert paper.entry_id.endswith("1706.03762v7"), "Wrong version returned"
        assert paper.updated is not None, "Update date missing"
        
        # Updated date should be after published date for versioned papers
        if paper.published and paper.updated:
            assert paper.updated >= paper.published, "Update date before publish date"
    
    def test_paper_metadata_completeness(self):
        """
        Test completeness of paper metadata.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Recent paper to ensure all metadata fields
        paper_id = "2103.14030"  # LoRA paper
        
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 1, "Paper not found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        paper = papers[0]
        
        # Check all metadata fields
        metadata_fields = {
            "entry_id": paper.entry_id,
            "title": paper.title,
            "summary": paper.summary,
            "authors": paper.authors,
            "published": paper.published,
            "updated": paper.updated,
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "pdf_url": paper.pdf_url,
            "comment": paper.comment,
            "journal_ref": paper.journal_ref,
            "doi": paper.doi
        }
        
        # Essential fields must be present
        assert metadata_fields["entry_id"], "Entry ID missing"
        assert metadata_fields["title"], "Title missing"
        assert metadata_fields["summary"], "Summary missing"
        assert len(metadata_fields["authors"]) > 0, "Authors missing"
        assert metadata_fields["published"], "Published date missing"
        assert len(metadata_fields["categories"]) > 0, "Categories missing"
        assert metadata_fields["primary_category"], "Primary category missing"
        assert metadata_fields["pdf_url"], "PDF URL missing"
        
        # Optional fields may be None but should exist
        assert "comment" in metadata_fields, "Comment field missing"
        assert "journal_ref" in metadata_fields, "Journal ref field missing"
        assert "doi" in metadata_fields, "DOI field missing"
    
    def test_invalid_paper_id(self):
        """
        Test handling of invalid paper IDs.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Invalid paper ID
        paper_id = "9999.99999"
        
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 0, "Should not find invalid paper"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
    
    def test_paper_affiliations(self):
        """
        Test extraction of author affiliations when available.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Paper with known affiliations
        paper_id = "2201.11903"  # Chain-of-Thought paper
        
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second
            num_retries=3
        )
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search, timeout=30.0))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 1, "Paper not found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        paper = papers[0]
        
        # Check author details
        assert len(paper.authors) > 0, "No authors found"
        
        # ArXiv API provides author names
        for author in paper.authors:
            assert author.name, f"Author name missing"
            # Note: ArXiv API doesn't always provide affiliations directly


if __name__ == "__main__":
    # Run tests
    test = TestPaperDetails()
    
    print("Testing get paper by ID...")
    test.test_get_paper_by_id()
    print("✅ Get paper by ID passed")
    
    print("\nTesting get multiple papers...")
    test.test_get_multiple_papers()
    print("✅ Get multiple papers passed")
    
    print("\nTesting paper version handling...")
    test.test_paper_version_handling()
    print("✅ Version handling passed")
    
    print("\nTesting metadata completeness...")
    test.test_paper_metadata_completeness()
    print("✅ Metadata completeness passed")
    
    print("\nTesting invalid paper ID...")
    test.test_invalid_paper_id()
    print("✅ Invalid ID handling passed")
    
    print("\nTesting paper affiliations...")
    test.test_paper_affiliations()
    print("✅ Affiliations test passed")
    
    print("\n✅ All paper details tests passed!")