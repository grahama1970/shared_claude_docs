#!/usr/bin/env python3
"""
Module: test_practical_module_bugs.py
Description: Practical test to find bugs in module interactions using available code

This test explores real bugs by:
1. Testing data format mismatches between ArXiv and expected formats
2. Finding edge cases in module handlers
3. Exposing integration issues
4. Testing error handling weaknesses

External Dependencies:
- arxiv: Real API
- Local handler code

Example Usage:
>>> python test_practical_module_bugs.py
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, List, Any
import sys

# Use what's available
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from arxiv_handlers.real_arxiv_handlers import (
    ArxivSearchHandler,
    ArxivDownloadHandler,
    ArxivEvidenceHandler,
    ArxivCitationHandler,
    ArxivBatchHandler
)


class PracticalModuleBugFinder:
    """Find practical bugs in module interactions"""
    
    def __init__(self):
        self.arxiv_search = ArxivSearchHandler()
        self.arxiv_download = ArxivDownloadHandler()
        self.arxiv_evidence = ArxivEvidenceHandler()
        self.arxiv_citation = ArxivCitationHandler()
        self.arxiv_batch = ArxivBatchHandler()
        self.bugs = []
    
    def test_arxiv_data_format_bugs(self):
        """Find bugs in ArXiv data formats that break downstream modules"""
        print("\n🐛 BUG HUNT 1: ArXiv Data Format Issues")
        print("-" * 50)
        
        # Get a paper with all fields
        result = self.arxiv_search.handle({
            "query": "transformer architecture attention",
            "max_results": 3
        })
        
        if "error" not in result and result.get("papers"):
            papers = result["papers"]
            print(f"Testing {len(papers)} papers for format issues...\n")
            
            for i, paper in enumerate(papers):
                print(f"Paper {i+1}: {paper['title'][:40]}...")
                
                # Bug 1: Check for None values that break JSON
                none_fields = [k for k, v in paper.items() if v is None]
                if none_fields:
                    self.bugs.append({
                        "bug": "None values in paper data",
                        "fields": none_fields,
                        "impact": "JSON serialization fails",
                        "paper_id": paper.get("id"),
                        "fix": "Replace None with empty string or omit field"
                    })
                    print(f"   ❌ Found None values in: {none_fields}")
                
                # Bug 2: Check for inconsistent author formats
                authors = paper.get("authors", [])
                if authors and isinstance(authors[0], dict):
                    self.bugs.append({
                        "bug": "Authors as dict instead of string list",
                        "format": type(authors[0]).__name__,
                        "impact": "Breaks ArangoDB storage",
                        "fix": "Normalize to string list"
                    })
                    print(f"   ❌ Authors are dicts, not strings!")
                
                # Bug 3: Check ID format consistency
                paper_id = paper.get("id", "")
                if paper_id and not paper_id.startswith("http"):
                    self.bugs.append({
                        "bug": "Inconsistent paper ID format",
                        "id": paper_id,
                        "impact": "Citation lookup fails",
                        "fix": "Standardize to full URL format"
                    })
                    print(f"   ❌ Non-URL ID format: {paper_id}")
                
                # Bug 4: Check for extremely long fields
                for field, value in paper.items():
                    if isinstance(value, str) and len(value) > 10000:
                        self.bugs.append({
                            "bug": f"Extremely long {field}",
                            "length": len(value),
                            "impact": "Database storage issues",
                            "fix": "Truncate or chunk long text"
                        })
                        print(f"   ❌ {field} is {len(value)} chars!")
                
                # Bug 5: Missing critical fields
                critical_fields = ["title", "summary", "authors", "pdf_url"]
                missing = [f for f in critical_fields if not paper.get(f)]
                if missing:
                    self.bugs.append({
                        "bug": "Missing critical fields",
                        "fields": missing,
                        "impact": "Downstream modules fail",
                        "paper_id": paper.get("id")
                    })
                    print(f"   ❌ Missing fields: {missing}")
    
    def test_arxiv_search_edge_cases(self):
        """Test edge cases that break ArXiv search"""
        print("\n\n🐛 BUG HUNT 2: ArXiv Search Edge Cases")
        print("-" * 50)
        
        edge_cases = [
            ("Empty query", ""),
            ("Only spaces", "   "),
            ("Special chars", "!@#$%^&*()"),
            ("Very long query", "quantum " * 100),
            ("Newlines", "quantum\ncomputing\nresearch"),
            ("Unicode", "量子计算 🔬"),
            ("SQL injection", "'; DROP TABLE papers; --"),
            ("Unmatched quotes", '"quantum computing'),
            ("Zero results query", "xyzqwerty12345notarealterm"),
        ]
        
        for name, query in edge_cases:
            print(f"\nTesting: {name}")
            print(f"Query: {repr(query[:50])}...")
            
            try:
                start = time.time()
                result = self.arxiv_search.handle({
                    "query": query,
                    "max_results": 1
                })
                duration = time.time() - start
                
                if "error" in result:
                    print(f"   ✅ Properly handled: {result['error'][:50]}")
                else:
                    papers = result.get("papers", [])
                    if query == "" and papers:
                        self.bugs.append({
                            "bug": "Empty query returns results",
                            "result_count": len(papers),
                            "impact": "Unexpected behavior"
                        })
                        print(f"   ❌ Empty query returned {len(papers)} results!")
                    elif duration > 5:
                        self.bugs.append({
                            "bug": f"Slow query processing",
                            "query_type": name,
                            "duration": f"{duration:.2f}s",
                            "impact": "Performance degradation"
                        })
                        print(f"   ⚠️ Took {duration:.2f}s")
                    else:
                        print(f"   ✅ Handled correctly ({len(papers)} results)")
                        
            except Exception as e:
                self.bugs.append({
                    "bug": f"Exception on {name}",
                    "error": str(e),
                    "query": query[:50],
                    "impact": "Crashes pipeline"
                })
                print(f"   💥 Exception: {str(e)[:50]}")
    
    def test_download_handler_bugs(self):
        """Test bugs in PDF download handler"""
        print("\n\n🐛 BUG HUNT 3: PDF Download Issues")
        print("-" * 50)
        
        # First get some papers
        result = self.arxiv_search.handle({
            "query": "machine learning",
            "max_results": 2
        })
        
        if "error" not in result and result.get("papers"):
            papers = result["papers"]
            
            # Test various ID formats
            test_ids = []
            for paper in papers:
                pdf_url = paper.get("pdf_url", "")
                paper_id = paper.get("id", "")
                
                # Extract ID in different ways
                if pdf_url:
                    # Method 1: From PDF URL
                    id1 = pdf_url.split("/")[-1].replace(".pdf", "")
                    test_ids.append(("PDF URL extraction", id1))
                    
                    # Method 2: From paper ID
                    if paper_id:
                        id2 = paper_id.split("/")[-1]
                        test_ids.append(("Paper ID extraction", id2))
                    
                    # Method 3: Full URL
                    test_ids.append(("Full PDF URL", pdf_url))
            
            # Add edge cases
            test_ids.extend([
                ("Invalid format", "not-a-valid-id"),
                ("Old format", "cs/0301012"),
                ("With version", "2301.12345v3"),
                ("Empty string", ""),
                ("None type", None),
            ])
            
            print(f"Testing {len(test_ids)} ID formats...\n")
            
            for name, test_id in test_ids:
                if test_id is None:
                    continue
                    
                print(f"Testing: {name} = '{test_id}'")
                
                try:
                    result = self.arxiv_download.handle({
                        "paper_ids": [test_id] if test_id else [],
                        "output_dir": "/tmp/arxiv_bug_test"
                    })
                    
                    if "error" in result:
                        print(f"   ❌ Error: {result['error'][:50]}")
                    else:
                        downloaded = result.get("downloaded", 0)
                        if downloaded == 0:
                            files = result.get("files", [])
                            if files and "error" in files[0]:
                                error = files[0]["error"]
                                if "404" not in error and "Not Found" not in error:
                                    self.bugs.append({
                                        "bug": "Poor error handling",
                                        "id_format": name,
                                        "error": error[:50],
                                        "impact": "Confusing error messages"
                                    })
                                    print(f"   ❌ Unclear error: {error[:50]}")
                                else:
                                    print(f"   ✅ Clear 404 error")
                        else:
                            print(f"   ✅ Downloaded successfully")
                            
                except Exception as e:
                    self.bugs.append({
                        "bug": f"Exception on {name}",
                        "error": str(e),
                        "impact": "Download crashes"
                    })
                    print(f"   💥 Exception: {str(e)[:50]}")
    
    def test_evidence_handler_bugs(self):
        """Test bugs in evidence finding"""
        print("\n\n🐛 BUG HUNT 4: Evidence Handler Issues")
        print("-" * 50)
        
        test_claims = [
            ("Normal claim", "neural networks improve accuracy"),
            ("Empty claim", ""),
            ("Very long claim", "a" * 1000),
            ("Special characters", "AI/ML & deep learning => better results!"),
            ("Question format", "Do neural networks improve accuracy?"),
            ("Negation", "neural networks do not improve accuracy"),
        ]
        
        for name, claim in test_claims:
            print(f"\nTesting: {name}")
            print(f"Claim: '{claim[:50]}...'")
            
            for evidence_type in ["supporting", "contradicting", "invalid_type"]:
                try:
                    result = self.arxiv_evidence.handle({
                        "claim": claim,
                        "evidence_type": evidence_type,
                        "max_results": 1
                    })
                    
                    if "error" in result:
                        if evidence_type == "invalid_type" and "evidence_type" not in result["error"]:
                            self.bugs.append({
                                "bug": "Invalid type not validated",
                                "type": evidence_type,
                                "impact": "Accepts invalid input"
                            })
                            print(f"   ❌ Invalid type not caught!")
                        else:
                            print(f"   ✅ Error: {result['error'][:30]}")
                    else:
                        evidence = result.get("evidence", [])
                        if claim == "" and evidence:
                            self.bugs.append({
                                "bug": "Empty claim returns evidence",
                                "count": len(evidence),
                                "impact": "Invalid results"
                            })
                            print(f"   ❌ Empty claim got {len(evidence)} results!")
                        elif evidence_type == "invalid_type":
                            self.bugs.append({
                                "bug": "Invalid evidence type accepted",
                                "impact": "No input validation"
                            })
                            print(f"   ❌ Invalid type accepted!")
                            
                except Exception as e:
                    if name != "Very long claim":  # Expected to fail
                        self.bugs.append({
                            "bug": f"Exception on {name}",
                            "error": str(e)[:50],
                            "impact": "Evidence search crashes"
                        })
                    print(f"   💥 Exception: {str(e)[:30]}")
    
    def test_batch_handler_bugs(self):
        """Test batch processing bugs"""
        print("\n\n🐛 BUG HUNT 5: Batch Processing Issues")
        print("-" * 50)
        
        # Test various batch scenarios
        test_batches = [
            {
                "name": "Empty batch",
                "operations": []
            },
            {
                "name": "Invalid operation type",
                "operations": [
                    {"type": "invalid_op", "params": {}}
                ]
            },
            {
                "name": "Missing params",
                "operations": [
                    {"type": "search"}  # No params
                ]
            },
            {
                "name": "Mixed valid/invalid",
                "operations": [
                    {"type": "search", "params": {"query": "test", "max_results": 1}},
                    {"type": "invalid", "params": {}},
                    {"type": "download", "params": {"paper_ids": ["2301.12345"]}}
                ]
            },
            {
                "name": "Duplicate operations",
                "operations": [
                    {"type": "search", "params": {"query": "AI", "max_results": 1}},
                    {"type": "search", "params": {"query": "AI", "max_results": 1}},
                    {"type": "search", "params": {"query": "AI", "max_results": 1}}
                ]
            }
        ]
        
        for batch in test_batches:
            print(f"\nTesting: {batch['name']}")
            print(f"Operations: {len(batch['operations'])}")
            
            try:
                result = self.arxiv_batch.handle(batch)
                
                if "error" in result:
                    print(f"   ✅ Error handled: {result['error'][:50]}")
                else:
                    successful = result.get("successful", 0)
                    failed = result.get("failed", 0)
                    total = result.get("total_operations", 0)
                    
                    if batch["name"] == "Empty batch" and total > 0:
                        self.bugs.append({
                            "bug": "Empty batch processed",
                            "impact": "Wasted resources"
                        })
                        print(f"   ❌ Empty batch returned results!")
                    elif batch["name"] == "Invalid operation type" and successful > 0:
                        self.bugs.append({
                            "bug": "Invalid operations succeed",
                            "impact": "No operation validation"
                        })
                        print(f"   ❌ Invalid operations succeeded!")
                    else:
                        print(f"   ✅ Results: {successful} success, {failed} failed")
                        
            except Exception as e:
                self.bugs.append({
                    "bug": f"Batch exception: {batch['name']}",
                    "error": str(e)[:50],
                    "impact": "Batch processing fails"
                })
                print(f"   💥 Exception: {str(e)[:50]}")
    
    def generate_bug_report(self):
        """Generate comprehensive bug report"""
        print("\n\n" + "="*60)
        print("🐛 PRACTICAL BUG REPORT: Module Interactions")
        print("="*60)
        
        if not self.bugs:
            print("\n✅ No bugs found! (This is suspicious...)")
            return
        
        print(f"\nFound {len(self.bugs)} bugs:\n")
        
        # Group by impact
        for bug in self.bugs:
            print(f"🔴 {bug['bug']}")
            if "impact" in bug:
                print(f"   Impact: {bug['impact']}")
            if "fix" in bug:
                print(f"   Fix: {bug['fix']}")
            print()
        
        # Save detailed report
        report_path = Path("practical_module_bugs.json")
        report_path.write_text(json.dumps(self.bugs, indent=2, default=str))
        print(f"📄 Detailed report saved to: {report_path}")
        
        # Statistics
        print(f"\n📊 Bug Statistics:")
        print(f"   Data format issues: {sum(1 for b in self.bugs if 'format' in str(b))}")
        print(f"   Validation failures: {sum(1 for b in self.bugs if 'validation' in str(b).lower())}")
        print(f"   Exception bugs: {sum(1 for b in self.bugs if 'Exception' in b.get('bug', ''))}")
        print(f"   Performance issues: {sum(1 for b in self.bugs if 'slow' in str(b).lower())}")
        
        print("\n🔧 TOP RECOMMENDATIONS:")
        print("1. Add input validation for all handlers")
        print("2. Standardize data formats (especially IDs)")
        print("3. Handle None values before JSON serialization")
        print("4. Add proper error messages for edge cases")
        print("5. Implement request throttling")
        print("6. Validate operation types in batch handler")


if __name__ == "__main__":
    print("🔍 Starting Practical Module Bug Hunt...")
    print("Testing with real ArXiv API calls!\n")
    
    finder = PracticalModuleBugFinder()
    
    # Run all bug hunts
    finder.test_arxiv_data_format_bugs()
    finder.test_arxiv_search_edge_cases()
    finder.test_download_handler_bugs()
    finder.test_evidence_handler_bugs()
    finder.test_batch_handler_bugs()
    
    # Generate report
    finder.generate_bug_report()
    
    print("\n✅ Practical bug hunting complete!")