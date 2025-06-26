#!/usr/bin/env python3
"""
Module: test_real_module_bugs.py
Description: Test real Granger module interactions to find actual bugs

This test uses the actual module handlers to find:
- Real integration issues
- Actual data format problems
- True performance bottlenecks
- Genuine error handling failures

External Dependencies:
- Real Granger modules via proper imports

Example Usage:
>>> python test_real_module_bugs.py
"""

import sys
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the actual module paths
sys.path.insert(0, '/home/graham/workspace/experiments')
sys.path.insert(0, '/home/graham/workspace/mcp-servers')

# Import real modules directly
try:
    # SPARTA handlers
    from sparta.src.sparta.sparta_mcp_server import (
        search_cves_by_keyword,
        get_cve_details,
        search_mitre_attack_techniques
    )
    SPARTA_AVAILABLE = True
except ImportError as e:
    print(f"SPARTA import failed: {e}")
    SPARTA_AVAILABLE = False

try:
    # YouTube handlers  
    from youtube_transcripts.src.youtube_transcripts.youtube_mcp_server import (
        download_youtube_transcript,
        extract_video_metadata,
        search_youtube_videos
    )
    YOUTUBE_AVAILABLE = True
except ImportError as e:
    print(f"YouTube import failed: {e}")
    YOUTUBE_AVAILABLE = False

try:
    # ArangoDB handlers
    from arangodb.src.arangodb.arangodb_mcp_server import (
        create_document,
        search_documents,
        create_graph_edge,
        query_graph
    )
    ARANGODB_AVAILABLE = True
except ImportError as e:
    print(f"ArangoDB import failed: {e}")
    ARANGODB_AVAILABLE = False

# Try to import what we can test
from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler


class RealModuleBugFinder:
    """Find real bugs in actual Granger module interactions"""
    
    def __init__(self):
        self.arxiv = ArxivSearchHandler()
        self.bugs = []
        self.test_results = []
    
    async def test_sparta_to_arxiv_pipeline(self):
        """Test SPARTA CVE → ArXiv paper search"""
        print("\n🔍 REAL TEST 1: SPARTA → ArXiv Pipeline")
        print("-" * 50)
        
        if not SPARTA_AVAILABLE:
            print("❌ SPARTA not available for testing")
            return
        
        try:
            # Search for real CVEs
            print("Searching for buffer overflow CVEs...")
            cves = await search_cves_by_keyword("buffer overflow", limit=5)
            
            if cves:
                print(f"✅ Found {len(cves)} CVEs")
                
                # For each CVE, search ArXiv
                for cve in cves[:2]:  # Test first 2
                    cve_id = cve.get("id", "Unknown")
                    description = cve.get("description", "")
                    
                    print(f"\nProcessing {cve_id}...")
                    
                    # Build ArXiv query from CVE
                    if description:
                        # Extract keywords
                        keywords = description.split()[:5]  # First 5 words
                        arxiv_query = " ".join(keywords)
                        
                        # Search ArXiv
                        arxiv_result = self.arxiv.handle({
                            "query": arxiv_query,
                            "max_results": 2
                        })
                        
                        if "error" in arxiv_result:
                            self.bugs.append({
                                "bug": "ArXiv search failed for CVE description",
                                "cve_id": cve_id,
                                "query": arxiv_query[:50],
                                "error": arxiv_result["error"],
                                "severity": "HIGH"
                            })
                            print(f"   ❌ ArXiv error: {arxiv_result['error'][:50]}")
                        else:
                            papers = arxiv_result.get("papers", [])
                            print(f"   ✅ Found {len(papers)} papers")
                    else:
                        self.bugs.append({
                            "bug": "CVE has no description",
                            "cve_id": cve_id,
                            "impact": "Cannot search for papers",
                            "severity": "MEDIUM"
                        })
                        print(f"   ⚠️ CVE has no description")
            else:
                print("❌ No CVEs found")
                
        except Exception as e:
            self.bugs.append({
                "bug": "SPARTA integration exception",
                "error": str(e),
                "severity": "CRITICAL"
            })
            print(f"💥 Exception: {e}")
    
    async def test_youtube_to_arangodb_flow(self):
        """Test YouTube → ArangoDB storage"""
        print("\n\n🔍 REAL TEST 2: YouTube → ArangoDB Flow")
        print("-" * 50)
        
        if not YOUTUBE_AVAILABLE:
            print("❌ YouTube module not available")
            return
            
        if not ARANGODB_AVAILABLE:
            print("❌ ArangoDB module not available")
            return
        
        try:
            # Get video metadata
            test_video_id = "dQw4w9WgXcQ"  # Well-known video
            print(f"Extracting metadata for video {test_video_id}...")
            
            metadata = await extract_video_metadata(test_video_id)
            
            if metadata:
                print(f"✅ Got metadata: {metadata.get('title', 'Unknown')[:40]}...")
                
                # Try to store in ArangoDB
                print("Storing in ArangoDB...")
                
                doc_result = await create_document(
                    collection="youtube_videos",
                    document=metadata
                )
                
                if "error" in doc_result:
                    self.bugs.append({
                        "bug": "YouTube metadata incompatible with ArangoDB",
                        "error": doc_result["error"],
                        "severity": "HIGH"
                    })
                    print(f"   ❌ Storage failed: {doc_result['error'][:50]}")
                else:
                    print(f"   ✅ Stored with key: {doc_result.get('_key')}")
                    
                    # Try to search for it
                    search_result = await search_documents(
                        collection="youtube_videos",
                        query=metadata.get("title", "")[:20]
                    )
                    
                    if not search_result or len(search_result) == 0:
                        self.bugs.append({
                            "bug": "Stored video not searchable",
                            "impact": "Data loss",
                            "severity": "HIGH"
                        })
                        print("   ❌ Cannot find stored video!")
                    else:
                        print(f"   ✅ Video searchable")
            else:
                print("❌ Failed to get video metadata")
                
        except Exception as e:
            self.bugs.append({
                "bug": "YouTube-ArangoDB integration exception",
                "error": str(e),
                "severity": "CRITICAL"
            })
            print(f"💥 Exception: {e}")
    
    async def test_cross_module_data_formats(self):
        """Test data format compatibility across modules"""
        print("\n\n🔍 REAL TEST 3: Cross-Module Data Formats")
        print("-" * 50)
        
        # Test ArXiv paper format
        print("Getting ArXiv paper...")
        arxiv_result = self.arxiv.handle({
            "query": "machine learning",
            "max_results": 1
        })
        
        if "error" not in arxiv_result and arxiv_result.get("papers"):
            paper = arxiv_result["papers"][0]
            print(f"✅ Got paper: {paper['title'][:40]}...")
            
            # Check required fields for different modules
            required_fields = {
                "ArangoDB": ["title", "authors", "id"],
                "Marker": ["pdf_url"],
                "YouTube": ["title", "summary"],  # For search
                "SPARTA": ["title", "categories"]  # For classification
            }
            
            for module, fields in required_fields.items():
                missing = [f for f in fields if f not in paper or not paper[f]]
                if missing:
                    self.bugs.append({
                        "bug": f"ArXiv data missing fields for {module}",
                        "missing_fields": missing,
                        "impact": f"{module} integration will fail",
                        "severity": "MEDIUM"
                    })
                    print(f"   ❌ Missing for {module}: {missing}")
                else:
                    print(f"   ✅ Compatible with {module}")
    
    async def test_error_propagation(self):
        """Test how errors propagate through modules"""
        print("\n\n🔍 REAL TEST 4: Error Propagation")
        print("-" * 50)
        
        # Test with invalid inputs
        test_cases = [
            {
                "module": "ArXiv",
                "method": lambda: self.arxiv.handle({"query": "", "max_results": 5}),
                "expected_error": "query"
            },
            {
                "module": "ArXiv", 
                "method": lambda: self.arxiv.handle({"query": "test", "max_results": -1}),
                "expected_error": "max_results"
            }
        ]
        
        if ARANGODB_AVAILABLE:
            test_cases.append({
                "module": "ArangoDB",
                "method": lambda: create_document("", {}),
                "expected_error": "collection"
            })
        
        for test in test_cases:
            print(f"\nTesting {test['module']} error handling...")
            try:
                if asyncio.iscoroutinefunction(test["method"]):
                    result = await test["method"]()
                else:
                    result = test["method"]()
                
                if isinstance(result, dict) and "error" in result:
                    error_msg = result["error"].lower()
                    if test["expected_error"] not in error_msg:
                        self.bugs.append({
                            "bug": "Poor error message",
                            "module": test["module"],
                            "expected": test["expected_error"],
                            "actual": result["error"][:50],
                            "severity": "LOW"
                        })
                        print(f"   ⚠️ Error doesn't mention '{test['expected_error']}'")
                    else:
                        print(f"   ✅ Good error message")
                else:
                    self.bugs.append({
                        "bug": "No error for invalid input",
                        "module": test["module"],
                        "severity": "HIGH"
                    })
                    print(f"   ❌ No error returned!")
                    
            except Exception as e:
                print(f"   💥 Exception: {str(e)[:50]}")
    
    def generate_real_bug_report(self):
        """Generate report of real bugs found"""
        print("\n\n" + "="*60)
        print("🐛 REAL BUG REPORT: Granger Module Integration")
        print("="*60)
        
        print(f"\nModules tested:")
        print(f"   SPARTA: {'✅ Available' if SPARTA_AVAILABLE else '❌ Not Available'}")
        print(f"   YouTube: {'✅ Available' if YOUTUBE_AVAILABLE else '❌ Not Available'}")
        print(f"   ArangoDB: {'✅ Available' if ARANGODB_AVAILABLE else '❌ Not Available'}")
        print(f"   ArXiv: ✅ Available")
        
        if not self.bugs:
            print("\n✅ No bugs found!")
            return
        
        print(f"\n🐛 Found {len(self.bugs)} real bugs:\n")
        
        # Group by severity
        critical = [b for b in self.bugs if b.get("severity") == "CRITICAL"]
        high = [b for b in self.bugs if b.get("severity") == "HIGH"]
        medium = [b for b in self.bugs if b.get("severity") == "MEDIUM"]
        low = [b for b in self.bugs if b.get("severity") == "LOW"]
        
        if critical:
            print(f"🔴 CRITICAL ({len(critical)} bugs):")
            for bug in critical:
                print(f"   - {bug['bug']}")
                if "error" in bug:
                    print(f"     Error: {bug['error'][:100]}")
                print()
        
        if high:
            print(f"🟠 HIGH ({len(high)} bugs):")
            for bug in high:
                print(f"   - {bug['bug']}")
                if "impact" in bug:
                    print(f"     Impact: {bug['impact']}")
                print()
        
        if medium:
            print(f"🟡 MEDIUM ({len(medium)} bugs):")
            for bug in medium:
                print(f"   - {bug['bug']}")
                print()
        
        # Save report
        report_path = Path("real_granger_bugs.json")
        report_path.write_text(json.dumps(self.bugs, indent=2))
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        print("\n🔧 FIXES NEEDED:")
        print("1. Ensure all modules are properly installed in pyproject.toml")
        print("2. Standardize data formats across all modules")
        print("3. Add proper error context to all handlers")
        print("4. Validate inputs before processing")
        print("5. Handle missing fields gracefully")


async def main():
    print("🔍 Starting REAL Granger Module Bug Hunt...")
    print("Testing with actual module imports!\n")
    
    finder = RealModuleBugFinder()
    
    # Run all tests
    await finder.test_sparta_to_arxiv_pipeline()
    await finder.test_youtube_to_arangodb_flow()
    await finder.test_cross_module_data_formats()
    await finder.test_error_propagation()
    
    # Generate report
    finder.generate_real_bug_report()
    
    print("\n✅ Real bug testing complete!")


if __name__ == "__main__":
    asyncio.run(main())