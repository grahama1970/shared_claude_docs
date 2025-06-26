#!/usr/bin/env python3
"""
Test script to verify ArXiv API fixes.

This script tests the new arxiv.Client API with proper rate limiting
and timeout handling.
"""

import arxiv
import time
from datetime import datetime


def test_new_api():
    """Test the new ArXiv API with Client."""
    print("Testing new ArXiv API...")
    
    # Create client with rate limiting
    client = arxiv.Client(
        page_size=100,
        delay_seconds=0.34,  # 3 requests per second
        num_retries=3
    )
    
    # Test 1: Basic search
    print("\n1. Testing basic search...")
    search = arxiv.Search(
        query="quantum computing",
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    start_time = time.time()
    try:
        papers = list(client.results(search, timeout=30.0))
        duration = time.time() - start_time
        
        print(f"   Found {len(papers)} papers in {duration:.2f}s")
        for i, paper in enumerate(papers):
            print(f"   {i+1}. {paper.title[:60]}...")
            
    except arxiv.ArxivError as e:
        print(f"   ArXiv API error: {e}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Search by ID
    print("\n2. Testing search by ID...")
    search = arxiv.Search(id_list=["1706.03762"])  # Attention Is All You Need
    
    start_time = time.time()
    try:
        papers = list(client.results(search, timeout=30.0))
        duration = time.time() - start_time
        
        if papers:
            paper = papers[0]
            print(f"   Found paper in {duration:.2f}s")
            print(f"   Title: {paper.title}")
            print(f"   Authors: {', '.join([a.name for a in paper.authors[:3]])}...")
            print(f"   Published: {paper.published}")
        else:
            print("   No paper found")
            
    except arxiv.ArxivError as e:
        print(f"   ArXiv API error: {e}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Rate limiting
    print("\n3. Testing rate limiting (3 requests)...")
    start_time = time.time()
    
    for i in range(3):
        search = arxiv.Search(query=f"test {i}", max_results=1)
        try:
            papers = list(client.results(search, timeout=30.0))
            print(f"   Request {i+1}: Found {len(papers)} papers")
        except Exception as e:
            print(f"   Request {i+1} failed: {e}")
    
    total_duration = time.time() - start_time
    print(f"   Total time for 3 requests: {total_duration:.2f}s")
    print(f"   Average time per request: {total_duration/3:.2f}s")
    
    if total_duration < 1.0:
        print("   WARNING: Requests completed too quickly. Rate limiting may not be working.")
    else:
        print("   Rate limiting appears to be working correctly.")
    
    print("\n✅ All tests completed!")


def test_deprecated_api():
    """Show what happens with the deprecated API (for comparison)."""
    print("\nTesting deprecated API (for comparison)...")
    print("This would fail in future versions:")
    print("  search = arxiv.Search(query='test')")
    print("  for paper in search.results():  # DEPRECATED!")
    print("      print(paper.title)")
    print("\nThe deprecated API will be removed in arxiv package v2.0.0")


if __name__ == "__main__":
    print("ArXiv API Fix Verification")
    print("=" * 50)
    
    test_new_api()
    test_deprecated_api()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("- Use arxiv.Client() instead of direct Search.results()")
    print("- Always specify timeout (30s recommended)")
    print("- Rate limiting: 3 requests/second (0.34s delay)")
    print("- Handle arxiv.ArxivError exceptions")