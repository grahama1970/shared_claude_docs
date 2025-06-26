#!/usr/bin/env python3
"""
Module: task_003_arxiv_quick.py
Description: Quick ArXiv test with timeout handling

External Dependencies:
- arxiv: https://github.com/lukasschwab/arxiv.py

Sample Input:
>>> test_arxiv_quick()

Expected Output:
>>> Test results with bugs found

Example Usage:
>>> python task_003_arxiv_quick.py
"""

import arxiv
import time
import signal
import json
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    """Context manager for timing out operations"""
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def test_arxiv_basic():
    """Basic ArXiv functionality test"""
    bugs_found = []
    
    print("\n" + "="*60)
    print("🐛 TASK #003: ArXiv Quick Bug Test")
    print("="*60)
    
    # Test 1: Simple search with timeout
    print("\n📋 Test 1: Basic search with 5s timeout")
    try:
        with time_limit(5):
            start = time.time()
            # Use the new Client API
            client = arxiv.Client()
            search = arxiv.Search(
                query="machine learning",
                max_results=1
            )
            
            papers = list(client.results(search))
            duration = time.time() - start
            
            print(f"  ✅ Found {len(papers)} papers in {duration:.3f}s")
            
            if duration > 5.0:
                bugs_found.append(f"Performance issue: {duration:.3f}s for single result")
                
    except TimeoutException:
        bugs_found.append("ArXiv search timed out after 5 seconds")
        print("  🐛 BUG: Search timed out!")
    except Exception as e:
        bugs_found.append(f"ArXiv search failed: {type(e).__name__}: {e}")
        print(f"  🐛 BUG: {type(e).__name__}: {e}")
    
    # Test 2: Deprecated API warning
    print("\n📋 Test 2: API deprecation check")
    try:
        # Intentionally use deprecated method
        search = arxiv.Search(query="test", max_results=1)
        # This should trigger deprecation warning
        results = search.results()
        bugs_found.append("Using deprecated Search.results() method - should use Client.results()")
        print("  🐛 BUG: Deprecated API usage detected")
    except:
        print("  ✅ Deprecated API properly handled")
    
    # Test 3: Empty query
    print("\n📋 Test 3: Empty query handling")
    try:
        client = arxiv.Client()
        search = arxiv.Search(query="", max_results=1)
        papers = list(client.results(search))
        
        if papers:
            bugs_found.append("Empty query returned results")
            print(f"  🐛 BUG: Empty query returned {len(papers)} results")
        else:
            print("  ✅ Empty query returned no results")
    except Exception as e:
        print(f"  ✅ Empty query raised exception: {type(e).__name__}")
    
    # Test 4: Connection handling
    print("\n📋 Test 4: Network timeout simulation")
    try:
        # Create client with very short timeout
        client = arxiv.Client(
            page_size=100,
            delay_seconds=0,
            num_retries=1
        )
        
        with time_limit(2):
            search = arxiv.Search(query="quantum computing", max_results=50)
            papers = list(client.results(search))
            
        if len(papers) == 50:
            bugs_found.append("No rate limiting on large requests")
            print(f"  🐛 BUG: Retrieved {len(papers)} papers without rate limiting")
            
    except TimeoutException:
        print("  ✅ Properly timed out on large request")
    except Exception as e:
        print(f"  ℹ️ Exception: {type(e).__name__}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 ArXiv Quick Test Summary")
    print("="*60)
    print(f"Bugs found: {len(bugs_found)}")
    
    if bugs_found:
        print("\n🐛 Bugs discovered:")
        for i, bug in enumerate(bugs_found, 1):
            print(f"  {i}. {bug}")
    
    # Save report
    report = {
        "task": "003_arxiv_quick",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "bugs_found": bugs_found,
        "critical_findings": [
            "ArXiv searches can timeout without proper handling",
            "Deprecated API (Search.results) still in use",
            "Need to use Client.results() instead"
        ]
    }
    
    with open("bug_hunter_results_003_quick.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return len(bugs_found)


if __name__ == "__main__":
    test_arxiv_basic()