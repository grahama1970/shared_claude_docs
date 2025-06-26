#!/usr/bin/env python3
"""
Module: test_02_arxiv_paper_search.py
Description: Test basic ArXiv paper search functionality
Level: 0
Modules: ArXiv
Expected Bugs: API errors, data format issues, missing fields
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path
import sys

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

class ArxivPaperSearchTest:
    """Level 0: Test basic ArXiv paper search functionality"""
    
    def __init__(self):
        self.test_name = "ArXiv Paper Search"
        self.level = 0
        self.bugs_found = []
        
    def test_basic_paper_search(self):
        """Test basic paper search with various queries"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"{'='*60}\n")
        
        # Import ArXiv handler
        try:
            from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler
            self.arxiv = ArxivSearchHandler()
        except ImportError as e:
            self.bugs_found.append({
                "bug": "ArXiv module import failure",
                "error": str(e),
                "severity": "CRITICAL",
                "impact": "Cannot use ArXiv functionality"
            })
            print(f"❌ Import failed: {e}")
            return
        
        # Test cases
        test_queries = [
            ("Normal query", "machine learning"),
            ("Empty query", ""),
            ("Special characters", "AI/ML & deep-learning"),
            ("Author search", "author:Hinton"),
            ("Title search", "title:transformer"),
            ("Very long query", "neural " * 50),
            ("Unicode", "量子计算 🔬"),
            ("Quotes", '"exact phrase search"'),
            ("Boolean", "quantum AND computing NOT cryptography"),
            ("Year filter", "machine learning 2024"),
        ]
        
        for name, query in test_queries:
            print(f"\nTesting {name}: '{query[:50]}{'...' if len(query) > 50 else ''}'")
            
            try:
                start_time = time.time()
                result = self.arxiv.handle({
                    "query": query,
                    "max_results": 3,
                    "sort_by": "relevance"
                })
                duration = time.time() - start_time
                
                if "error" not in result:
                    papers = result.get("papers", [])
                    print(f"✅ Found {len(papers)} papers in {duration:.2f}s")
                    
                    # Check data quality
                    for i, paper in enumerate(papers):
                        # Bug: None values
                        none_fields = [k for k, v in paper.items() if v is None]
                        if none_fields:
                            self.bugs_found.append({
                                "bug": "None values in paper data",
                                "fields": none_fields,
                                "query": name,
                                "severity": "HIGH",
                                "impact": "JSON serialization will fail"
                            })
                        
                        # Bug: Missing required fields
                        required = ["title", "summary", "authors", "id", "pdf_url"]
                        missing = [f for f in required if not paper.get(f)]
                        if missing:
                            self.bugs_found.append({
                                "bug": "Missing required fields",
                                "fields": missing,
                                "paper_title": paper.get("title", "Unknown")[:50],
                                "severity": "HIGH"
                            })
                        
                        # Bug: Empty authors list
                        if paper.get("authors") == []:
                            self.bugs_found.append({
                                "bug": "Empty authors list",
                                "paper_id": paper.get("id"),
                                "severity": "MEDIUM"
                            })
                    
                    # Performance check
                    if duration > 5:
                        self.bugs_found.append({
                            "bug": "Slow search performance",
                            "query": name,
                            "duration": f"{duration:.2f}s",
                            "severity": "MEDIUM"
                        })
                    
                    # Empty query should not return results
                    if query == "" and papers:
                        self.bugs_found.append({
                            "bug": "Empty query returns results",
                            "result_count": len(papers),
                            "severity": "MEDIUM"
                        })
                        
                else:
                    error = result.get("error", "Unknown")
                    print(f"❌ Search failed: {error[:100]}")
                    
                    # Check error quality
                    if query == "" and "query" not in error.lower():
                        self.bugs_found.append({
                            "bug": "Poor error message for empty query",
                            "error": error,
                            "severity": "LOW"
                        })
                        
            except Exception as e:
                self.bugs_found.append({
                    "bug": f"Exception during {name}",
                    "error": str(e),
                    "query": query[:50],
                    "severity": "HIGH"
                })
                print(f"💥 Exception: {e}")
    
    def test_sort_and_filter_options(self):
        """Test different sort and filter options"""
        print("\n\nTesting Sort and Filter Options...")
        
        base_query = "machine learning"
        
        # Test sort options
        sort_options = ["relevance", "submitted_date", "last_updated", "invalid_sort"]
        
        for sort_by in sort_options:
            print(f"\nTesting sort_by: {sort_by}")
            
            try:
                result = self.arxiv.handle({
                    "query": base_query,
                    "max_results": 2,
                    "sort_by": sort_by
                })
                
                if "error" not in result:
                    if sort_by == "invalid_sort":
                        self.bugs_found.append({
                            "bug": "Invalid sort option accepted",
                            "sort_by": sort_by,
                            "severity": "MEDIUM"
                        })
                    print(f"✅ Sort worked: {result.get('paper_count')} results")
                else:
                    if sort_by != "invalid_sort":
                        self.bugs_found.append({
                            "bug": f"Valid sort option failed",
                            "sort_by": sort_by,
                            "error": result["error"],
                            "severity": "HIGH"
                        })
                        
            except Exception as e:
                self.bugs_found.append({
                    "bug": "Exception during sort test",
                    "sort_by": sort_by,
                    "error": str(e),
                    "severity": "MEDIUM"
                })
    
    def test_edge_cases(self):
        """Test edge cases and limits"""
        print("\n\nTesting Edge Cases...")
        
        edge_cases = [
            {"name": "Negative max_results", "params": {"query": "AI", "max_results": -1}},
            {"name": "Zero max_results", "params": {"query": "AI", "max_results": 0}},
            {"name": "Huge max_results", "params": {"query": "AI", "max_results": 10000}},
            {"name": "Invalid query type", "params": {"query": 12345, "max_results": 1}},
            {"name": "Missing query", "params": {"max_results": 1}},
            {"name": "Null query", "params": {"query": None, "max_results": 1}},
        ]
        
        for case in edge_cases:
            print(f"\nTesting: {case['name']}")
            
            try:
                result = self.arxiv.handle(case["params"])
                
                if "error" not in result:
                    # These should all fail
                    self.bugs_found.append({
                        "bug": f"Edge case accepted: {case['name']}",
                        "params": case["params"],
                        "severity": "HIGH",
                        "impact": "Invalid input not validated"
                    })
                    print(f"❌ Should have failed but didn't!")
                else:
                    print(f"✅ Properly rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"✅ Exception (expected): {str(e)[:50]}")
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"{'='*60}")
        
        if not self.bugs_found:
            print("\n✅ No bugs found!")
            return
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            bugs = [b for b in self.bugs_found if b.get("severity") == severity]
            if bugs:
                print(f"\n{severity} ({len(bugs)} bugs):")
                for bug in bugs:
                    print(f"  - {bug['bug']}")
                    if "impact" in bug:
                        print(f"    Impact: {bug['impact']}")
        
        # Save detailed report
        report_path = Path(f"bug_reports/level0_{self.test_name.lower().replace(' ', '_')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report: {report_path}")
        
        return self.bugs_found


def main():
    """Run the test"""
    tester = ArxivPaperSearchTest()
    tester.test_basic_paper_search()
    tester.test_sort_and_filter_options()
    tester.test_edge_cases()
    return tester.generate_report()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)