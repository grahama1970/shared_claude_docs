"""
Test module for ArXiv download_paper functionality.

These tests validate paper download capabilities using the real ArXiv API.

External Dependencies:
- arxiv: https://pypi.org/project/arxiv/
- httpx: For downloading PDFs
- typing: Built-in type annotations

Example Usage:
>>> pytest test_download_paper.py -v
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
import httpx
from typing import Dict, Any
from pathlib import Path
import tempfile
import os


class TestDownloadPaper:
    """Test suite for paper download capabilities."""
    
    def test_get_pdf_url(self):
        """
        Test retrieving PDF URL for a paper.
        Expected duration: 0.1s-1.0s
        """
        start_time = time.time()
        
        # Use a known paper
        paper_id = "1706.03762"
        
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search))
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(papers) == 1, "Paper not found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        paper = papers[0]
        pdf_url = paper.pdf_url
        
        # Validate PDF URL
        assert pdf_url is not None, "PDF URL is None"
        assert pdf_url.startswith("http"), f"Invalid URL format: {pdf_url}"
        assert "pdf" in pdf_url, f"URL doesn't contain 'pdf': {pdf_url}"
        assert paper_id in pdf_url, f"Paper ID not in URL: {pdf_url}"
    
    def test_verify_pdf_accessible(self):
        """
        Test that PDF URL is actually accessible.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Get paper
        paper_id = "2103.14030"  # LoRA paper
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search))
        
        assert len(papers) == 1, "Paper not found"
        pdf_url = papers[0].pdf_url
        
        # Check if URL is accessible
        response = httpx.head(pdf_url, follow_redirects=True)
        
        duration = time.time() - start_time
        
        # Assertions
        assert response.status_code == 200, f"PDF not accessible: {response.status_code}"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Check content type
        content_type = response.headers.get("content-type", "")
        assert "pdf" in content_type.lower(), f"Not a PDF: {content_type}"
    
    def test_download_pdf_content(self):
        """
        Test downloading actual PDF content.
        Expected duration: 1.0s-5.0s
        """
        start_time = time.time()
        
        # Get paper
        paper_id = "1409.0473"  # Smaller paper for faster download
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search))
        
        assert len(papers) == 1, "Paper not found"
        pdf_url = papers[0].pdf_url
        
        # Download PDF content
        with httpx.Client() as client:
            response = client.get(pdf_url, follow_redirects=True, timeout=30.0)
        
        duration = time.time() - start_time
        
        # Assertions
        assert response.status_code == 200, f"Download failed: {response.status_code}"
        assert 0.1 <= duration <= 15.0, f"Duration {duration}s outside expected range"
        
        # Verify PDF content
        content = response.content
        assert len(content) > 1000, "PDF too small to be valid"
        assert content.startswith(b"%PDF"), "Not a valid PDF file"
        
        # Check PDF header
        pdf_header = content[:10].decode('latin-1')
        assert pdf_header.startswith("%PDF-"), f"Invalid PDF header: {pdf_header}"
    
    def test_save_pdf_to_file(self):
        """
        Test saving downloaded PDF to file.
        Expected duration: 1.0s-5.0s
        """
        start_time = time.time()
        
        # Get paper
        paper_id = "1409.0473"
        client = arxiv.Client()
        search = arxiv.Search(id_list=[paper_id])
        papers = list(client.results(search))
        
        assert len(papers) == 1, "Paper not found"
        paper = papers[0]
        pdf_url = paper.pdf_url
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download and save PDF
            pdf_path = Path(temp_dir) / f"{paper_id.replace('/', '_')}.pdf"
            
            with httpx.Client() as client:
                response = client.get(pdf_url, follow_redirects=True, timeout=30.0)
            
            # Save to file
            pdf_path.write_bytes(response.content)
            
            duration = time.time() - start_time
            
            # Assertions
            assert pdf_path.exists(), "PDF file not created"
            assert pdf_path.stat().st_size > 1000, "PDF file too small"
            assert 0.1 <= duration <= 15.0, f"Duration {duration}s outside expected range"
            
            # Verify file is valid PDF
            with open(pdf_path, 'rb') as f:
                header = f.read(10)
                assert header.startswith(b"%PDF"), "Saved file is not a valid PDF"
    
    def test_download_url_generation(self):
        """
        Test PDF URL generation for different paper formats.
        Expected duration: 0.5s-2.0s
        """
        start_time = time.time()
        
        # Test different paper ID formats
        paper_ids = [
            "2103.14030",      # Standard format
            "cs/0301012",      # Old format with category
            "math.AG/0601001", # Old format with subcategory
        ]
        
        pdf_urls = []
        for paper_id in paper_ids:
            try:
                client = arxiv.Client(
                    page_size=100,
                    delay_seconds=0.34,  # 3 requests per second
                    num_retries=3
                )
                search = arxiv.Search(id_list=[paper_id])
                papers = list(client.results(search, timeout=30.0))
                if papers:
                    pdf_urls.append({
                        "id": paper_id,
                        "url": papers[0].pdf_url,
                        "found": True
                    })
                else:
                    pdf_urls.append({
                        "id": paper_id,
                        "url": None,
                        "found": False
                    })
            except Exception as e:
                pdf_urls.append({
                    "id": paper_id,
                    "url": None,
                    "found": False,
                    "error": str(e)
                })
        
        duration = time.time() - start_time
        
        # Assertions
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # At least some papers should be found
        found_papers = [p for p in pdf_urls if p["found"]]
        assert len(found_papers) > 0, "No papers found"
        
        # Check URL format for found papers
        for paper_info in found_papers:
            if paper_info["url"]:
                assert paper_info["url"].startswith("http"), f"Invalid URL: {paper_info['url']}"
                assert ".pdf" in paper_info["url"], f"Not a PDF URL: {paper_info['url']}"
    
    def test_batch_download_urls(self):
        """
        Test getting download URLs for multiple papers.
        Expected duration: 0.5s-3.0s
        """
        start_time = time.time()
        
        # Multiple papers
        paper_ids = ["1706.03762", "1810.04805", "2005.14165"]
        
        search = arxiv.Search(id_list=paper_ids)
        papers = list(search.results())
        
        pdf_urls = []
        for paper in papers:
            pdf_urls.append({
                "id": paper.entry_id.split("/")[-1],
                "title": paper.title[:50],
                "pdf_url": paper.pdf_url,
                "size_estimate": "1-10 MB"  # ArXiv doesn't provide size beforehand
            })
        
        duration = time.time() - start_time
        
        # Assertions
        assert len(pdf_urls) == len(paper_ids), "Not all papers found"
        assert 0.1 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        
        # Verify all URLs are valid
        for pdf_info in pdf_urls:
            assert pdf_info["pdf_url"], f"Missing URL for {pdf_info['id']}"
            assert pdf_info["pdf_url"].startswith("http"), f"Invalid URL for {pdf_info['id']}"


if __name__ == "__main__":
    # Run tests
    test = TestDownloadPaper()
    
    print("Testing get PDF URL...")
    test.test_get_pdf_url()
    print("✅ Get PDF URL passed")
    
    print("\nTesting PDF accessibility...")
    test.test_verify_pdf_accessible()
    print("✅ PDF accessibility passed")
    
    print("\nTesting PDF content download...")
    test.test_download_pdf_content()
    print("✅ PDF content download passed")
    
    print("\nTesting save PDF to file...")
    test.test_save_pdf_to_file()
    print("✅ Save PDF to file passed")
    
    print("\nTesting URL generation for different formats...")
    test.test_download_url_generation()
    print("✅ URL generation passed")
    
    print("\nTesting batch download URLs...")
    test.test_batch_download_urls()
    print("✅ Batch download URLs passed")
    
    print("\n✅ All download tests passed!")