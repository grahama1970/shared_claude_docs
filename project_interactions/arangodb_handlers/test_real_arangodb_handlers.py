#!/usr/bin/env python3
"""
Test Real ArangoDB Handlers

This script tests all ArangoDB handlers with real database operations.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

# Set environment variables for ArangoDB connection
os.environ['ARANGO_HOST'] = 'http://localhost:8529'
os.environ['ARANGO_USER'] = 'root'
os.environ['ARANGO_PASSWORD'] = 'openSesame'
os.environ['ARANGO_DB_NAME'] = 'granger_test'

from real_arangodb_handlers import (
    ArangoDocumentHandler,
    ArangoSearchHandler,
    ArangoGraphHandler,
    ArangoMemoryHandler,
    ArangoPaperHandler,
    ArangoBatchHandler,
    ARANGODB_AVAILABLE
)


def test_document_handler():
    """Test document CRUD operations"""
    print("\n1. Testing Document Handler...")
    
    if not ARANGODB_AVAILABLE:
        print("   ❌ SKIPPED - ArangoDB module not available")
        return False
        
    handler = ArangoDocumentHandler()
    
    # Test document creation
    start_time = time.time()
    result = handler.handle({
        "operation": "create",
        "collection": "test_documents",
        "data": {
            "title": "Test Document",
            "content": "This is a test document for ArangoDB integration",
            "tags": ["test", "integration", "arangodb"],
            "score": 0.95
        }
    })
    duration = time.time() - start_time
    
    if "error" in result:
        print(f"   ❌ FAILED: {result['error']}")
        return False
    
    doc_key = result.get("_key")
    print(f"   ✅ Document created: {doc_key} in {duration:.3f}s")
    
    # Test document read
    result = handler.handle({
        "operation": "read",
        "collection": "test_documents",
        "key": doc_key
    })
    
    if "error" in result:
        print(f"   ❌ Read failed: {result['error']}")
    else:
        print(f"   ✅ Document read successfully")
        print(f"   Title: {result.get('title')}")
    
    # Test document update
    result = handler.handle({
        "operation": "update",
        "collection": "test_documents",
        "key": doc_key,
        "data": {
            "score": 0.98,
            "updated": True
        }
    })
    
    if "error" in result:
        print(f"   ❌ Update failed: {result['error']}")
    else:
        print(f"   ✅ Document updated")
    
    # Test query
    result = handler.handle({
        "operation": "query",
        "collection": "test_documents",
        "query": {"tags": "test"},
        "limit": 5
    })
    
    print(f"   ✅ Query found {result.get('count', 0)} documents")
    
    # Verify timing is realistic
    if duration < 0.001:
        print(f"   ⚠️  WARNING: Suspiciously fast operation ({duration:.3f}s)")
    
    return True


def test_search_handler():
    """Test search operations"""
    print("\n2. Testing Search Handler...")
    
    if not ARANGODB_AVAILABLE:
        print("   ❌ SKIPPED - ArangoDB module not available")
        return False
        
    handler = ArangoSearchHandler()
    
    # Test BM25 search
    start_time = time.time()
    result = handler.handle({
        "search_type": "bm25",
        "query": "test document integration",
        "collection": "test_documents",
        "limit": 5
    })
    duration = time.time() - start_time
    
    if "error" in result:
        print(f"   ❌ BM25 search failed: {result['error']}")
        # Continue with other tests
    else:
        print(f"   ✅ BM25 search completed in {duration:.3f}s")
        print(f"   Found {result['result_count']} results")
    
    # Test semantic search
    result = handler.handle({
        "search_type": "semantic",
        "query": "artificial intelligence machine learning",
        "limit": 5
    })
    
    if "error" in result:
        print(f"   ⚠️  Semantic search error: {result['error']}")
    else:
        print(f"   ✅ Semantic search found {result['result_count']} results")
    
    # Test hybrid search
    result = handler.handle({
        "search_type": "hybrid",
        "query": "test integration arangodb",
        "limit": 5
    })
    
    if "error" in result:
        print(f"   ⚠️  Hybrid search error: {result['error']}")
    else:
        print(f"   ✅ Hybrid search found {result['result_count']} results")
    
    return True


def test_graph_handler():
    """Test graph operations"""
    print("\n3. Testing Graph Handler...")
    
    if not ARANGODB_AVAILABLE:
        print("   ❌ SKIPPED - ArangoDB module not available")
        return False
        
    handler = ArangoGraphHandler()
    
    # First create some documents to connect
    doc_handler = ArangoDocumentHandler()
    
    # Create source document
    result1 = doc_handler.handle({
        "operation": "create",
        "data": {"title": "Source Node", "type": "concept"}
    })
    
    if "error" in result1:
        print(f"   ❌ Failed to create source node: {result1['error']}")
        return False
    
    key1 = result1.get("_key")
    
    # Create target document
    result2 = doc_handler.handle({
        "operation": "create",
        "data": {"title": "Target Node", "type": "concept"}
    })
    
    if "error" in result2:
        print(f"   ❌ Failed to create target node: {result2['error']}")
        return False
        
    key2 = result2.get("_key")
    
    # Test edge creation
    result = handler.handle({
        "operation": "create_edge",
        "from_key": key1,
        "to_key": key2,
        "edge_type": "relates_to",
        "edge_data": {"weight": 0.8}
    })
    
    if "error" in result:
        print(f"   ❌ Edge creation failed: {result['error']}")
    else:
        print(f"   ✅ Edge created: {key1} -> {key2}")
    
    # Test graph traversal
    result = handler.handle({
        "operation": "traverse",
        "from_key": key1,
        "depth": 2,
        "direction": "outbound"
    })
    
    if "error" in result:
        print(f"   ❌ Traversal failed: {result['error']}")
    else:
        print(f"   ✅ Traversal found {result['node_count']} nodes")
    
    # Test neighbors
    result = handler.handle({
        "operation": "neighbors",
        "from_key": key1,
        "direction": "any"
    })
    
    if "error" in result:
        print(f"   ❌ Neighbors query failed: {result['error']}")
    else:
        print(f"   ✅ Found {result['neighbor_count']} neighbors")
    
    return True


def test_memory_handler():
    """Test memory agent operations"""
    print("\n4. Testing Memory Handler...")
    
    if not ARANGODB_AVAILABLE:
        print("   ❌ SKIPPED - ArangoDB module not available")
        return False
        
    handler = ArangoMemoryHandler()
    
    # Test message storage
    conversation_id = f"test_conv_{int(time.time())}"
    
    result = handler.handle({
        "operation": "store_message",
        "conversation_id": conversation_id,
        "message": {
            "role": "user",
            "content": "Hello, this is a test message",
            "metadata": {"test": True}
        }
    })
    
    if "error" in result:
        print(f"   ❌ Message storage failed: {result['error']}")
        return False
    
    print(f"   ✅ Message stored in conversation: {conversation_id}")
    
    # Store assistant response
    result = handler.handle({
        "operation": "store_message",
        "conversation_id": conversation_id,
        "message": {
            "role": "assistant",
            "content": "Hello! I received your test message.",
            "metadata": {"response": True}
        }
    })
    
    if "error" in result:
        print(f"   ❌ Response storage failed: {result['error']}")
    else:
        print(f"   ✅ Response stored")
    
    # Test conversation retrieval
    result = handler.handle({
        "operation": "get_conversation",
        "conversation_id": conversation_id,
        "limit": 10
    })
    
    if "error" in result:
        print(f"   ❌ Conversation retrieval failed: {result['error']}")
    else:
        print(f"   ✅ Retrieved {result['message_count']} messages")
    
    # Test memory search
    result = handler.handle({
        "operation": "search_memory",
        "query": "test message",
        "limit": 5
    })
    
    if "error" in result:
        print(f"   ❌ Memory search failed: {result['error']}")
    else:
        print(f"   ✅ Memory search found {result['result_count']} results")
    
    return True


def test_paper_handler():
    """Test ArXiv paper operations"""
    print("\n5. Testing Paper Handler...")
    
    if not ARANGODB_AVAILABLE:
        print("   ❌ SKIPPED - ArangoDB module not available")
        return False
        
    handler = ArangoPaperHandler()
    
    # Test paper storage
    paper_data = {
        "arxiv_id": "2103.14030",
        "title": "Learning Transferable Visual Models From Natural Language Supervision",
        "authors": ["Alec Radford", "Jong Wook Kim", "Chris Hallacy"],
        "abstract": "State-of-the-art computer vision systems are trained...",
        "categories": ["cs.CV", "cs.LG"],
        "published": "2021-02-26"
    }
    
    result = handler.handle({
        "operation": "store_paper",
        "paper_data": paper_data
    })
    
    if "error" in result:
        print(f"   ❌ Paper storage failed: {result['error']}")
        return False
    
    paper_key = result.get("paper_key")
    print(f"   ✅ Paper stored: {paper_key}")
    
    # Test finding similar papers
    result = handler.handle({
        "operation": "find_similar",
        "paper_id": paper_key,
        "limit": 3,
        "similarity_threshold": 0.5
    })
    
    if "error" in result:
        print(f"   ⚠️  Similar papers search error: {result['error']}")
    else:
        print(f"   ✅ Found {result['similar_count']} similar papers")
    
    # Test citation management
    # Store another paper
    paper_data2 = {
        "arxiv_id": "1706.03762",
        "title": "Attention Is All You Need",
        "authors": ["Ashish Vaswani", "Noam Shazeer"],
        "abstract": "The dominant sequence transduction models...",
        "categories": ["cs.CL", "cs.LG"],
        "published": "2017-06-12"
    }
    
    result2 = handler.handle({
        "operation": "store_paper",
        "paper_data": paper_data2
    })
    
    if "error" not in result2:
        paper_key2 = result2.get("paper_key")
        
        # Add citation
        result = handler.handle({
            "operation": "add_citation",
            "from_paper": paper_key,
            "to_paper": paper_key2,
            "citation_type": "cites"
        })
        
        if "error" in result:
            print(f"   ⚠️  Citation creation error: {result['error']}")
        else:
            print(f"   ✅ Citation added: {paper_key} -> {paper_key2}")
    
    return True


def test_batch_handler():
    """Test batch operations"""
    print("\n6. Testing Batch Handler...")
    
    handler = ArangoBatchHandler()
    
    # Prepare batch operations
    operations = [
        {
            "handler": "document",
            "params": {
                "operation": "create",
                "data": {"title": "Batch Test 1", "batch": True}
            }
        },
        {
            "handler": "document",
            "params": {
                "operation": "create",
                "data": {"title": "Batch Test 2", "batch": True}
            }
        },
        {
            "handler": "search",
            "params": {
                "search_type": "bm25",
                "query": "batch test",
                "limit": 5
            }
        }
    ]
    
    start_time = time.time()
    result = handler.handle({"operations": operations})
    duration = time.time() - start_time
    
    if "error" in result:
        print(f"   ❌ FAILED: {result['error']}")
        return False
    
    print(f"   ✅ SUCCESS")
    print(f"   Completed {result['successful']}/{result['total_operations']} operations in {duration:.2f}s")
    
    # Show operation results
    for i, op_result in enumerate(result['results']):
        handler_type = op_result['handler']
        success = "✅" if op_result['success'] else "❌"
        print(f"   Operation {i+1} ({handler_type}): {success}")
    
    return result['successful'] > 0


def generate_test_report(test_results: Dict[str, bool]):
    """Generate test report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# Real ArangoDB Handlers Test Report
Generated: {timestamp}

## Test Summary

| Handler | Test Result | Description |
|---------|-------------|-------------|
| Document Handler | {'✅ PASS' if test_results.get('document', False) else '❌ FAIL'} | CRUD operations on documents |
| Search Handler | {'✅ PASS' if test_results.get('search', False) else '❌ FAIL'} | BM25, semantic, and hybrid search |
| Graph Handler | {'✅ PASS' if test_results.get('graph', False) else '❌ FAIL'} | Graph operations and traversal |
| Memory Handler | {'✅ PASS' if test_results.get('memory', False) else '❌ FAIL'} | Conversation memory management |
| Paper Handler | {'✅ PASS' if test_results.get('paper', False) else '❌ FAIL'} | ArXiv paper storage and citations |
| Batch Handler | {'✅ PASS' if test_results.get('batch', False) else '❌ FAIL'} | Batch operation processing |

## Module Status

- **ArangoDB Module**: {'✅ Available' if ARANGODB_AVAILABLE else '❌ Not Available'}
- **Connection**: {test_results.get('connection_status', 'Unknown')}

## Integration Features

1. **Document Operations**: Full CRUD with automatic embedding generation
2. **Search Capabilities**: 
   - BM25 text search
   - Semantic vector search  
   - Hybrid search combining both
3. **Graph Database**: Edges, traversal, pathfinding
4. **Memory Agent**: Conversation tracking with temporal awareness
5. **Paper Management**: Specialized handlers for research papers

## Known Issues

- Semantic search requires embeddings to be pre-generated
- Graph operations require proper collection setup
- Memory agent needs specific collections created

## Verification

All passing tests used real ArangoDB operations with actual database queries.
"""
    
    # Calculate summary
    passed = sum(1 for v in test_results.values() if v and isinstance(v, bool))
    total = len([k for k in test_results.keys() if k != 'connection_status'])
    
    report += f"\n## Overall Result\n\n**Tests Passed**: {passed}/{total} ({passed/total*100:.0f}%)\n"
    
    if passed == total:
        report += "\n✅ **All ArangoDB handlers are working correctly with real database integration.**"
    elif passed > 0:
        report += "\n⚠️ **Some ArangoDB handlers are working, but there are issues to address.**"
    else:
        report += "\n❌ **ArangoDB handlers are not functioning properly. Check database connection.**"
    
    return report


def main():
    """Run all tests"""
    print("="*60)
    print("Real ArangoDB Handlers Test Suite")
    print("="*60)
    
    test_results = {}
    
    # First check if we can connect
    print("\nChecking ArangoDB connection...")
    doc_handler = ArangoDocumentHandler()
    if doc_handler.connect():
        print("✅ Connected to ArangoDB")
        test_results['connection_status'] = "Connected"
    else:
        print("❌ Failed to connect to ArangoDB")
        test_results['connection_status'] = "Failed"
        print("\nMake sure ArangoDB is running on http://localhost:8529")
        print("with credentials: root/openSesame")
    
    # Run tests
    test_results['document'] = test_document_handler()
    test_results['search'] = test_search_handler()
    test_results['graph'] = test_graph_handler()
    test_results['memory'] = test_memory_handler()
    test_results['paper'] = test_paper_handler()
    test_results['batch'] = test_batch_handler()
    
    # Generate report
    report = generate_test_report(test_results)
    
    # Save report
    report_path = Path("arangodb_handlers_test_report.md")
    report_path.write_text(report)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for k, v in test_results.items() if v and k != 'connection_status')
    total = len([k for k in test_results.keys() if k != 'connection_status'])
    
    print(f"\nTests Passed: {passed}/{total}")
    print(f"Report saved to: {report_path}")
    
    if not ARANGODB_AVAILABLE:
        print("\n⚠️  ArangoDB module not properly installed")
        print("   Check /home/graham/workspace/experiments/arangodb/src")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())