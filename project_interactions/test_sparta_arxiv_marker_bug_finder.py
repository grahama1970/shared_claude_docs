"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_sparta_arxiv_marker_bug_finder.py
Description: Test real interactions between SPARTA → ArXiv → Marker to find bugs

This test will expose:
- Data format mismatches between modules
- Missing error handling
- Unexpected data types
- Performance bottlenecks
- Edge cases that break the pipeline

External Dependencies:
- sparta: Real CVE/vulnerability data
- arxiv: Real paper search
- marker: PDF processing

Example Usage:
>>> python test_sparta_arxiv_marker_bug_finder.py
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Add paths
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments')

from sparta.real_sparta_handlers_fixed import SPARTACVESearchHandler
from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler, ArxivDownloadHandler
from loguru import logger

class SPARTAArxivMarkerBugFinder:
    """Find bugs in SPARTA → ArXiv → Marker interaction"""
    
    def __init__(self):
        self.sparta = SPARTACVESearchHandler()
        self.arxiv_search = ArxivSearchHandler()
        self.arxiv_download = ArxivDownloadHandler()
        self.bugs_found = []
        
    def test_empty_cve_descriptions(self):
        """Bug Test 1: What happens when CVE has no description?"""
        print("\n🐛 TEST 1: Empty CVE Descriptions")
        print("-" * 50)
        
        try:
            # Search for generic term that might return CVEs with missing data
            result = self.sparta.handle({
                "keyword": "unknown",
                "limit": 10
            })
            
            if result.get("success"):
                for cve in result.get("vulnerabilities", []):
                    desc = cve.get("cve", {}).get("description", {}).get("description_data", [])
                    if not desc or not desc[0].get("value"):
                        self.bugs_found.append({
                            "bug": "CVE with missing description",
                            "cve_id": cve.get("cve", {}).get("id", "Unknown"),
                            "impact": "ArXiv search will fail with empty query"
                        })
                        print(f"❌ Found CVE with no description: {cve.get('cve', {}).get('id')}")
                        
                        # Try to search ArXiv with empty description
                        arxiv_result = self.arxiv_search.handle({
                            "query": "",  # Empty query
                            "max_results": 1
                        })
                        print(f"   ArXiv response to empty query: {arxiv_result.get('error', 'No error?!')}")
                        
        except Exception as e:
            self.bugs_found.append({
                "bug": "Exception on empty descriptions",
                "error": str(e),
                "impact": "Pipeline crashes"
            })
            print(f"💥 Exception: {e}")
    
    def test_special_characters_in_cve(self):
        """Bug Test 2: Special characters breaking ArXiv queries"""
        print("\n\n🐛 TEST 2: Special Characters in CVE → ArXiv")
        print("-" * 50)
        
        # Test CVE descriptions with special characters
        test_queries = [
            "SQL injection'; DROP TABLE--",
            "XSS <script>alert('xss')</script>",
            "Path traversal ../../../etc/passwd",
            "Command injection && rm -rf /",
            "Unicode: 🔥💉🐛"
        ]
        
        for query in test_queries:
            try:
                # Simulate CVE with malicious description
                print(f"\nTesting query: {query[:50]}...")
                
                arxiv_result = self.arxiv_search.handle({
                    "query": query,
                    "max_results": 1
                })
                
                if "error" in arxiv_result:
                    self.bugs_found.append({
                        "bug": "Special characters cause ArXiv error",
                        "query": query,
                        "error": arxiv_result["error"],
                        "impact": "Cannot search papers for certain CVEs"
                    })
                    print(f"   ❌ ArXiv failed: {arxiv_result['error']}")
                else:
                    print(f"   ✅ ArXiv handled it: {arxiv_result.get('paper_count')} results")
                    
            except Exception as e:
                self.bugs_found.append({
                    "bug": "Exception on special characters",
                    "query": query,
                    "error": str(e),
                    "impact": "Pipeline crashes on malicious CVE descriptions"
                })
                print(f"   💥 Exception: {e}")
    
    def test_arxiv_pdf_url_formats(self):
        """Bug Test 3: ArXiv PDF URLs breaking download"""
        print("\n\n🐛 TEST 3: ArXiv PDF URL Format Issues")
        print("-" * 50)
        
        # Search for real papers
        result = self.arxiv_search.handle({
            "query": "buffer overflow",
            "max_results": 5
        })
        
        if "error" not in result:
            for paper in result.get("papers", []):
                pdf_url = paper.get("pdf_url", "")
                paper_id = paper.get("id", "")
                
                print(f"\nTesting PDF URL: {pdf_url}")
                
                # Test different ID extraction methods
                test_ids = [
                    pdf_url.split("/")[-1].replace(".pdf", ""),  # Current method
                    paper_id.split("/")[-1],  # From paper ID
                    pdf_url,  # Full URL
                    "invalid_id_12345"  # Invalid ID
                ]
                
                for test_id in test_ids:
                    try:
                        download_result = self.arxiv_download.handle({
                            "paper_ids": [test_id],
                            "output_dir": "/tmp/arxiv_test"
                        })
                        
                        if download_result.get("downloaded") == 0:
                            self.bugs_found.append({
                                "bug": "PDF download failed",
                                "paper_id": test_id,
                                "pdf_url": pdf_url,
                                "error": download_result.get("files", [{}])[0].get("error", "Unknown"),
                                "impact": "Cannot process papers with Marker"
                            })
                            print(f"   ❌ Failed to download with ID: {test_id}")
                        else:
                            print(f"   ✅ Downloaded with ID: {test_id}")
                            break
                            
                    except Exception as e:
                        self.bugs_found.append({
                            "bug": "Exception during download",
                            "paper_id": test_id,
                            "error": str(e),
                            "impact": "Download crashes"
                        })
                        print(f"   💥 Exception: {e}")
    
    def test_rate_limiting_cascade(self):
        """Bug Test 4: Rate limiting cascading through modules"""
        print("\n\n🐛 TEST 4: Rate Limiting Cascade")
        print("-" * 50)
        
        # Hammer APIs to trigger rate limits
        print("Sending rapid requests to trigger rate limits...")
        
        start_time = time.time()
        request_count = 0
        
        for i in range(20):  # Rapid fire requests
            try:
                # SPARTA request
                sparta_result = self.sparta.handle({
                    "keyword": f"test{i}",
                    "limit": 1
                })
                request_count += 1
                
                # Immediate ArXiv request
                arxiv_result = self.arxiv_search.handle({
                    "query": f"security test {i}",
                    "max_results": 1
                })
                request_count += 1
                
                # Check for rate limit errors
                if "rate" in str(sparta_result.get("error", "")).lower():
                    self.bugs_found.append({
                        "bug": "SPARTA rate limit hit",
                        "after_requests": request_count,
                        "time_elapsed": time.time() - start_time,
                        "impact": "Pipeline stalls"
                    })
                    print(f"   ❌ SPARTA rate limited after {request_count} requests")
                    
                if "rate" in str(arxiv_result.get("error", "")).lower():
                    self.bugs_found.append({
                        "bug": "ArXiv rate limit hit",
                        "after_requests": request_count,
                        "time_elapsed": time.time() - start_time,
                        "impact": "Cannot fetch papers"
                    })
                    print(f"   ❌ ArXiv rate limited after {request_count} requests")
                    
            except Exception as e:
                if "429" in str(e) or "rate" in str(e).lower():
                    print(f"   ❌ Rate limit exception: {e}")
                    
        print(f"Completed {request_count} requests in {time.time() - start_time:.2f}s")
    
    def test_data_size_limits(self):
        """Bug Test 5: Large data breaking module boundaries"""
        print("\n\n🐛 TEST 5: Data Size Limits")
        print("-" * 50)
        
        # Search for maximum CVEs
        print("Requesting maximum CVEs from SPARTA...")
        result = self.sparta.handle({
            "keyword": "overflow",  # Common term
            "limit": 1000  # Large limit
        })
        
        if result.get("success"):
            cve_count = len(result.get("vulnerabilities", []))
            print(f"Got {cve_count} CVEs")
            
            # Build massive ArXiv query from all CVEs
            if cve_count > 100:
                descriptions = []
                for cve in result["vulnerabilities"][:200]:  # Take many
                    desc = cve.get("cve", {}).get("description", {}).get("description_data", [])
                    if desc and desc[0].get("value"):
                        descriptions.append(desc[0]["value"][:50])
                
                # Create huge query
                massive_query = " OR ".join(descriptions)
                query_size = len(massive_query)
                print(f"Created query with {query_size} characters")
                
                try:
                    arxiv_result = self.arxiv_search.handle({
                        "query": massive_query,
                        "max_results": 1
                    })
                    
                    if "error" in arxiv_result:
                        self.bugs_found.append({
                            "bug": "Large query breaks ArXiv",
                            "query_size": query_size,
                            "error": arxiv_result["error"],
                            "impact": "Cannot process large CVE sets"
                        })
                        print(f"   ❌ ArXiv failed with large query: {arxiv_result['error']}")
                    else:
                        print(f"   ✅ ArXiv handled {query_size} character query")
                        
                except Exception as e:
                    self.bugs_found.append({
                        "bug": "Exception on large data",
                        "query_size": query_size,
                        "error": str(e),
                        "impact": "Pipeline crashes on large datasets"
                    })
                    print(f"   💥 Exception: {e}")
    
    def test_timeout_propagation(self):
        """Bug Test 6: Timeout handling between modules"""
        print("\n\n🐛 TEST 6: Timeout Propagation")
        print("-" * 50)
        
        # Test with queries that might take long
        slow_queries = [
            "a" * 1000,  # Very long query
            "complex quantum cryptography blockchain AI ML",  # Many terms
            "\"exact phrase match\" AND \"another phrase\" AND \"third phrase\""  # Complex
        ]
        
        for query in slow_queries:
            print(f"\nTesting potentially slow query: {query[:50]}...")
            start = time.time()
            
            try:
                result = self.arxiv_search.handle({
                    "query": query,
                    "max_results": 50,  # Large result set
                    "sort_by": "relevance"
                })
                
                duration = time.time() - start
                print(f"   Query took {duration:.2f}s")
                
                if duration > 10:
                    self.bugs_found.append({
                        "bug": "Slow query not timing out",
                        "query": query[:50],
                        "duration": duration,
                        "impact": "Pipeline hangs on complex queries"
                    })
                    print(f"   ⚠️ Query took too long: {duration:.2f}s")
                    
            except Exception as e:
                if "timeout" in str(e).lower():
                    print(f"   ✅ Properly timed out: {e}")
                else:
                    self.bugs_found.append({
                        "bug": "Unexpected error instead of timeout",
                        "error": str(e),
                        "impact": "Poor error handling"
                    })
                    print(f"   ❌ Unexpected error: {e}")
    
    def generate_bug_report(self):
        """Generate comprehensive bug report"""
        print("\n\n" + "="*60)
        print("🐛 BUG REPORT: SPARTA → ArXiv → Marker Integration")
        print("="*60)
        
        if not self.bugs_found:
            print("✅ No bugs found! (This is suspicious...)")
            return
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group bugs by severity
        critical = [b for b in self.bugs_found if "crash" in b.get("impact", "").lower()]
        high = [b for b in self.bugs_found if "fail" in b.get("impact", "").lower()]
        medium = [b for b in self.bugs_found if b not in critical and b not in high]
        
        if critical:
            print(f"🔴 CRITICAL ({len(critical)} bugs that crash the pipeline):")
            for bug in critical:
                print(f"   - {bug['bug']}")
                print(f"     Impact: {bug['impact']}")
                print(f"     Details: {bug.get('error', 'N/A')}")
                print()
        
        if high:
            print(f"🟠 HIGH ({len(high)} bugs that break functionality):")
            for bug in high:
                print(f"   - {bug['bug']}")
                print(f"     Impact: {bug['impact']}")
                print()
        
        if medium:
            print(f"🟡 MEDIUM ({len(medium)} bugs that degrade performance):")
            for bug in medium:
                print(f"   - {bug['bug']}")
                print(f"     Impact: {bug.get('impact', 'N/A')}")
                print()
        
        # Save detailed report
        report_path = Path("sparta_arxiv_marker_bugs.json")
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("1. Add input validation in ArXiv handler for empty/special queries")
        print("2. Implement proper timeout handling with configurable limits")
        print("3. Add rate limiting with exponential backoff")
        print("4. Sanitize CVE descriptions before passing to ArXiv")
        print("5. Handle large datasets with pagination or chunking")
        print("6. Add circuit breakers between modules")


if __name__ == "__main__":
    print("🔍 Starting SPARTA → ArXiv → Marker Bug Hunt...")
    print("This will make REAL API calls to find REAL bugs!\n")
    
    bug_finder = SPARTAArxivMarkerBugFinder()
    
    # Run all bug tests
    bug_finder.test_empty_cve_descriptions()
    bug_finder.test_special_characters_in_cve()
    bug_finder.test_arxiv_pdf_url_formats()
    bug_finder.test_rate_limiting_cascade()
    bug_finder.test_data_size_limits()
    bug_finder.test_timeout_propagation()
    
    # Generate report
    bug_finder.generate_bug_report()
    
    print("\n✅ Bug hunting complete!")