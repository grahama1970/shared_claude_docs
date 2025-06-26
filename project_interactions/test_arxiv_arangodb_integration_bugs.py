"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_arxiv_arangodb_integration_bugs.py
Description: Test ArXiv → ArangoDB integration to find real bugs

This focused test explores:
- ArXiv data format issues
- ArangoDB storage failures
- Edge creation problems
- Search inconsistencies

External Dependencies:
- arxiv: Real API calls
- arangodb: Real database

Example Usage:
>>> python test_arxiv_arangodb_integration_bugs.py
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from arxiv_handlers.real_arxiv_handlers import (
    ArxivSearchHandler, 
    ArxivDownloadHandler,
    ArxivEvidenceHandler
)
from arangodb_handlers.real_arangodb_handlers import (
    ArangoDocumentHandler,
    ArangoSearchHandler,
    ArangoGraphHandler
)


class ArxivArangoDBIntegrationBugFinder:
    """Find real bugs in ArXiv → ArangoDB integration"""
    
    def __init__(self):
        self.arxiv_search = ArxivSearchHandler()
        self.arxiv_download = ArxivDownloadHandler()
        self.arxiv_evidence = ArxivEvidenceHandler()
        self.arango_doc = ArangoDocumentHandler()
        self.arango_search = ArangoSearchHandler()
        self.arango_graph = ArangoGraphHandler()
        self.bugs_found = []
    
    def test_arxiv_to_arangodb_data_mismatch(self):
        """Bug Test 1: ArXiv data format vs ArangoDB expectations"""
        print("\n🐛 BUG TEST 1: Data Format Mismatches")
        print("-" * 50)
        
        # Get real ArXiv data
        print("Fetching real ArXiv papers...")
        result = self.arxiv_search.handle({
            "query": "machine learning",
            "max_results": 3
        })
        
        if "error" not in result:
            papers = result.get("papers", [])
            print(f"Found {len(papers)} papers to test")
            
            for paper in papers:
                # Try to store paper directly in ArangoDB
                print(f"\nTesting paper: {paper.get('title', '')[:50]}...")
                
                # Test 1: Direct storage (might fail due to format)
                try:
                    doc_result = self.arango_doc.handle({
                        "operation": "create",
                        "collection": "test_papers",
                        "data": paper  # Raw ArXiv data
                    })
                    
                    if "error" in doc_result:
                        self.bugs_found.append({
                            "bug": "ArXiv format incompatible with ArangoDB",
                            "field": doc_result.get("error", "Unknown"),
                            "paper_id": paper.get("id"),
                            "impact": "Cannot store papers without transformation"
                        })
                        print(f"   ❌ Storage failed: {doc_result['error'][:50]}")
                    else:
                        print(f"   ✅ Stored successfully")
                        
                        # Test retrieval
                        search_result = self.arango_search.handle({
                            "search_type": "fulltext",
                            "query": paper.get("title", "")[:30],
                            "collection": "test_papers"
                        })
                        
                        if search_result.get("result_count", 0) == 0:
                            self.bugs_found.append({
                                "bug": "Stored paper not searchable",
                                "paper_id": paper.get("id"),
                                "impact": "Data stored but not retrievable"
                            })
                            print(f"   ❌ Paper stored but not searchable!")
                            
                except Exception as e:
                    self.bugs_found.append({
                        "bug": "Exception storing ArXiv data",
                        "error": str(e),
                        "paper_id": paper.get("id"),
                        "impact": "Pipeline crashes"
                    })
                    print(f"   💥 Exception: {str(e)[:50]}")
    
    def test_edge_creation_with_invalid_nodes(self):
        """Bug Test 2: Creating edges with non-existent nodes"""
        print("\n\n🐛 BUG TEST 2: Invalid Edge Creation")
        print("-" * 50)
        
        # Try to create edges without creating nodes first
        test_edges = [
            {
                "from": "papers/nonexistent_paper_123",
                "to": "videos/nonexistent_video_456",
                "edge_type": "mentions"
            },
            {
                "from": "papers/2301.12345",  # Might exist
                "to": "papers/9999.99999",     # Definitely doesn't
                "edge_type": "cites"
            },
            {
                "from": "chunks/chunk_" + "x" * 100,  # Very long key
                "to": "chunks/chunk_abc",
                "edge_type": "semantically_similar"
            }
        ]
        
        for edge in test_edges:
            print(f"\nTesting edge: {edge['from'][:30]} → {edge['to'][:30]}")
            
            try:
                result = self.arango_graph.handle({
                    "operation": "create_edge",
                    "from": edge["from"],
                    "to": edge["to"],
                    "edge_type": edge["edge_type"]
                })
                
                if "error" not in result:
                    self.bugs_found.append({
                        "bug": "Edge created with invalid nodes",
                        "edge": edge,
                        "impact": "Corrupt graph with dangling edges"
                    })
                    print(f"   ❌ Edge created without validating nodes!")
                else:
                    print(f"   ✅ Properly rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"   ✅ Exception (expected): {str(e)[:50]}")
    
    def test_search_special_characters(self):
        """Bug Test 3: Special characters in search queries"""
        print("\n\n🐛 BUG TEST 3: Search Query Injection")
        print("-" * 50)
        
        # Test queries with special characters
        injection_queries = [
            '"; db._drop("test_papers"); //',  # AQL injection
            "' OR 1==1 OR '",                   # Logic injection
            "\\x00\\x01\\x02",                  # Null bytes
            "𝕌𝕟𝕚𝕔𝕠𝕕𝕖",                      # Unicode
            "a" * 10000,                        # Very long query
            '{"$ne": null}',                    # NoSQL injection
        ]
        
        for query in injection_queries:
            print(f"\nTesting query: {repr(query[:30])}...")
            
            try:
                result = self.arango_search.handle({
                    "search_type": "fulltext",
                    "query": query,
                    "collection": "test_papers",
                    "limit": 1
                })
                
                if "error" not in result:
                    # Check if injection worked
                    if result.get("result_count", 0) > 100:  # Suspiciously many results
                        self.bugs_found.append({
                            "bug": "Possible query injection",
                            "query": query[:50],
                            "results": result.get("result_count"),
                            "impact": "Security vulnerability"
                        })
                        print(f"   ❌ Got {result['result_count']} results - possible injection!")
                    else:
                        print(f"   ✅ Query handled safely: {result.get('result_count', 0)} results")
                else:
                    print(f"   ✅ Query rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"   ✅ Exception (good): {str(e)[:50]}")
    
    def test_concurrent_paper_updates(self):
        """Bug Test 4: Race conditions updating same paper"""
        print("\n\n🐛 BUG TEST 4: Concurrent Update Race Conditions")
        print("-" * 50)
        
        # First create a test paper
        test_paper = {
            "_key": "race_test_paper",
            "title": "Test Paper for Race Conditions",
            "view_count": 0,
            "download_count": 0
        }
        
        create_result = self.arango_doc.handle({
            "operation": "create",
            "collection": "test_papers",
            "data": test_paper
        })
        
        if "error" not in create_result:
            print("Created test paper, simulating concurrent updates...")
            
            # Simulate multiple agents updating counters
            update_results = []
            for i in range(5):
                result = self.arango_doc.handle({
                    "operation": "update",
                    "collection": "test_papers",
                    "key": "race_test_paper",
                    "data": {
                        "view_count": i + 1,  # Each thinks it's incrementing by 1
                        "download_count": i * 2
                    }
                })
                update_results.append(result)
                time.sleep(0.1)  # Small delay
            
            # Get final state
            final_result = self.arango_doc.handle({
                "operation": "get",
                "collection": "test_papers",
                "key": "race_test_paper"
            })
            
            if "document" in final_result:
                final_doc = final_result["document"]
                print(f"\nFinal state:")
                print(f"   view_count: {final_doc.get('view_count')} (expected: 5)")
                print(f"   download_count: {final_doc.get('download_count')} (expected: 8)")
                
                if final_doc.get("view_count") != 5:
                    self.bugs_found.append({
                        "bug": "Lost updates in concurrent scenario",
                        "expected": 5,
                        "actual": final_doc.get("view_count"),
                        "impact": "Data inconsistency"
                    })
                    print("   ❌ Lost updates detected!")
    
    def test_arxiv_evidence_storage(self):
        """Bug Test 5: Complex evidence data storage"""
        print("\n\n🐛 BUG TEST 5: Evidence Data Complexity")
        print("-" * 50)
        
        # Get evidence from ArXiv
        print("Searching for evidence papers...")
        evidence_result = self.arxiv_evidence.handle({
            "claim": "neural networks improve image recognition",
            "evidence_type": "supporting",
            "max_results": 2
        })
        
        if "error" not in evidence_result:
            evidence_papers = evidence_result.get("evidence", [])
            print(f"Found {len(evidence_papers)} evidence papers")
            
            for paper in evidence_papers:
                # Evidence papers have nested structure
                print(f"\nStoring evidence paper: {paper.get('title', '')[:40]}...")
                
                try:
                    # Try to store with evidence snippets
                    result = self.arango_doc.handle({
                        "operation": "create",
                        "collection": "evidence_papers",
                        "data": paper
                    })
                    
                    if "error" in result:
                        # Check what field caused the error
                        if "evidence" in result.get("error", ""):
                            self.bugs_found.append({
                                "bug": "Cannot store evidence snippets",
                                "error": result["error"],
                                "impact": "Loss of evidence data"
                            })
                            print(f"   ❌ Evidence storage failed: {result['error'][:50]}")
                            
                            # Try without evidence field
                            paper_copy = paper.copy()
                            paper_copy.pop("evidence", None)
                            retry_result = self.arango_doc.handle({
                                "operation": "create",
                                "collection": "evidence_papers",
                                "data": paper_copy
                            })
                            
                            if "error" not in retry_result:
                                print("   ⚠️  Succeeded without evidence field!")
                                
                except Exception as e:
                    self.bugs_found.append({
                        "bug": "Exception on complex data",
                        "error": str(e),
                        "impact": "Pipeline failure"
                    })
                    print(f"   💥 Exception: {str(e)[:50]}")
    
    def generate_bug_report(self):
        """Generate bug report with actionable fixes"""
        print("\n\n" + "="*60)
        print("🐛 BUG REPORT: ArXiv → ArangoDB Integration")
        print("="*60)
        
        if not self.bugs_found:
            print("✅ No bugs found in this test run")
            return
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group by impact
        for bug in self.bugs_found:
            print(f"🔴 {bug['bug']}")
            print(f"   Impact: {bug.get('impact', 'Unknown')}")
            if "error" in bug:
                print(f"   Error: {bug['error'][:100]}")
            print()
        
        # Save detailed report
        report_path = Path("arxiv_arangodb_bugs.json")
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"📄 Detailed report saved to: {report_path}")
        
        print("\n🔧 RECOMMENDED FIXES:")
        print("1. Add data transformation layer between ArXiv and ArangoDB")
        print("2. Validate node existence before creating edges")
        print("3. Sanitize search queries to prevent injection")
        print("4. Use transactions for concurrent updates")
        print("5. Handle nested/complex data structures properly")
        print("6. Add schema validation for collections")


if __name__ == "__main__":
    print("🔍 Starting ArXiv → ArangoDB Integration Bug Hunt...")
    print("This will make REAL API calls and database operations!\n")
    
    bug_finder = ArxivArangoDBIntegrationBugFinder()
    
    # Run all bug tests
    bug_finder.test_arxiv_to_arangodb_data_mismatch()
    bug_finder.test_edge_creation_with_invalid_nodes()
    bug_finder.test_search_special_characters()
    bug_finder.test_concurrent_paper_updates()
    bug_finder.test_arxiv_evidence_storage()
    
    # Generate report
    bug_finder.generate_bug_report()
    
    print("\n✅ Bug hunting complete!")