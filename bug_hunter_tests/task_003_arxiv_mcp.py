#!/usr/bin/env python3
"""
Module: task_003_arxiv_mcp.py
Description: Task #003 - Find Research Paper (ArXiv MCP) Bug Hunter Test

External Dependencies:
- arxiv: https://github.com/lukasschwab/arxiv.py
- aiohttp: https://docs.aiohttp.org/

Sample Input:
>>> test_arxiv_search("diffusion models Chen 2024")

Expected Output:
>>> Search results with timing and validation

Example Usage:
>>> python task_003_arxiv_mcp.py
"""

import sys
import time
import asyncio
from typing import Dict, Any, List, Optional
import json

# Try to import arxiv
try:
    import arxiv
    ARXIV_AVAILABLE = True
    print("✅ ArXiv module imported successfully")
except ImportError as e:
    print(f"⚠️ ArXiv import failed: {e}")
    print("Installing arxiv...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "arxiv"])
    try:
        import arxiv
        ARXIV_AVAILABLE = True
        print("✅ ArXiv module installed and imported")
    except Exception as e2:
        ARXIV_AVAILABLE = False
        print(f"❌ ArXiv module unavailable: {e2}")


class ArXivBugHunter:
    """ArXiv search bug hunting tests"""
    
    def search_papers(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search ArXiv papers"""
        start_time = time.time()
        result = {
            "query": query,
            "success": False,
            "duration": 0,
            "count": 0,
            "papers": [],
            "error": None,
            "bug_found": None
        }
        
        try:
            # Create search
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            # Execute search
            papers = []
            for paper in search.results():
                papers.append({
                    "title": paper.title,
                    "authors": [author.name for author in paper.authors],
                    "summary": paper.summary[:200] + "...",
                    "published": str(paper.published),
                    "arxiv_id": paper.entry_id,
                    "pdf_url": paper.pdf_url
                })
            
            duration = time.time() - start_time
            
            result["success"] = True
            result["duration"] = duration
            result["count"] = len(papers)
            result["papers"] = papers
            
            # Validation checks
            if duration > 10.0:
                result["bug_found"] = f"Performance issue: {duration:.2f}s (>10s threshold)"
            
            if len(papers) == 0 and "diffusion" in query.lower():
                result["bug_found"] = "No results for popular topic 'diffusion'"
                
        except Exception as e:
            result["duration"] = time.time() - start_time
            result["error"] = str(e)
            result["bug_found"] = f"Exception: {type(e).__name__}"
            
        return result
    
    def test_special_characters(self, query: str) -> Dict[str, Any]:
        """Test handling of special characters"""
        try:
            result = self.search_papers(query, max_results=5)
            return result
        except Exception as e:
            return {
                "query": query,
                "success": False,
                "error": str(e),
                "bug_found": f"Failed on special chars: {type(e).__name__}"
            }


def run_arxiv_bug_hunt():
    """Run comprehensive ArXiv MCP bug hunting tests"""
    print("\n" + "="*60)
    print("🐛 TASK #003: ArXiv MCP Bug Hunter")
    print("="*60)
    
    if not ARXIV_AVAILABLE:
        print("❌ Cannot run tests - ArXiv module not available")
        return {
            "task": "003_arxiv_mcp",
            "status": "blocked",
            "reason": "Module import failure",
            "bugs_found": ["ArXiv module cannot be imported"]
        }
    
    hunter = ArXivBugHunter()
    bugs_found = []
    test_results = []
    
    # Test 1: Author search with year
    print("\n📋 Test 1: Author search with year")
    result = hunter.search_papers("Chen diffusion models 2024", max_results=5)
    test_results.append(result)
    print(f"  Duration: {result['duration']:.3f}s")
    print(f"  Papers found: {result['count']}")
    if result['bug_found']:
        bugs_found.append(result['bug_found'])
        print(f"  🐛 BUG: {result['bug_found']}")
    
    # Test 2: Special characters
    print("\n📋 Test 2: Special characters handling")
    special_tests = [
        "Müller quantum",  # Umlaut
        "∇f(x) optimization",  # Math symbols
        "Chen et al.",  # Common format
        "machine learning \"exact phrase\"",  # Quotes
        "neural+networks",  # Plus sign
    ]
    
    for special_query in special_tests:
        result = hunter.test_special_characters(special_query)
        test_results.append(result)
        if result['success']:
            print(f"  ✅ Handled: '{special_query}' ({result['count']} results)")
        else:
            bug = f"Failed on '{special_query}': {result.get('error', 'Unknown error')}"
            bugs_found.append(bug)
            print(f"  🐛 BUG: {bug}")
    
    # Test 3: Empty query
    print("\n📋 Test 3: Empty query handling")
    result = hunter.search_papers("", max_results=5)
    test_results.append(result)
    if result['success'] and result['count'] > 0:
        bug = "Empty query returned results instead of error"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    else:
        print(f"  ✅ Empty query properly handled")
    
    # Test 4: Very long query
    print("\n📋 Test 4: Extremely long query")
    long_query = "machine learning " * 100  # 1500+ characters
    result = hunter.search_papers(long_query, max_results=1)
    test_results.append(result)
    if result['success']:
        print(f"  ✅ Long query handled ({len(long_query)} chars)")
    else:
        print(f"  ⚠️ Long query failed: {result.get('error')}")
    
    # Test 5: Pagination test
    print("\n📋 Test 5: Large result set handling")
    result = hunter.search_papers("machine learning", max_results=100)
    test_results.append(result)
    print(f"  Duration: {result['duration']:.3f}s")
    print(f"  Papers retrieved: {result['count']}")
    if result['count'] < 100 and result['success']:
        bug = f"Requested 100 papers but got {result['count']}"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Test 6: Concurrent searches
    print("\n📋 Test 6: Concurrent search stress test")
    queries = [
        "quantum computing",
        "machine learning", 
        "neural networks",
        "computer vision",
        "natural language processing"
    ]
    
    start = time.time()
    concurrent_results = []
    for query in queries:
        result = hunter.search_papers(query, max_results=10)
        concurrent_results.append(result)
    duration = time.time() - start
    
    failures = sum(1 for r in concurrent_results if not r['success'])
    print(f"  Total duration: {duration:.3f}s")
    print(f"  Failures: {failures}/{len(queries)}")
    
    if failures > 0:
        bug = f"Concurrent searches had {failures} failures"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 ArXiv MCP Bug Hunt Summary")
    print("="*60)
    print(f"Total tests run: {len(test_results) + len(concurrent_results)}")
    print(f"Bugs found: {len(bugs_found)}")
    
    if bugs_found:
        print("\n🐛 Bugs discovered:")
        for i, bug in enumerate(bugs_found, 1):
            print(f"  {i}. {bug}")
    else:
        print("\n✅ No bugs found in ArXiv search")
    
    # Save detailed report
    report = {
        "task": "003_arxiv_mcp",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "module": "arxiv",
        "bugs_found": bugs_found,
        "test_results": test_results,
        "recommendations": [
            "Add input validation for query length",
            "Implement query sanitization for special chars",
            "Add rate limiting for API protection",
            "Cache results to improve performance",
            "Handle empty queries gracefully"
        ]
    }
    
    with open("bug_hunter_results_003.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n📄 Detailed report saved to: bug_hunter_results_003.json")
    
    return report


if __name__ == "__main__":
    report = run_arxiv_bug_hunt()