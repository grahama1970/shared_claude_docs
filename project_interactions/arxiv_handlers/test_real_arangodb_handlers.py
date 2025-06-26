#!/usr/bin/env python3
"""
Test Real ArangoDB Handlers

This module tests the real ArangoDB handlers to ensure they properly integrate
with the actual ArangoDB database and provide correct functionality for GRANGER.

External Dependencies:
- pytest: For test framework
- ArangoDB running locally or accessible

Example Usage:
>>> python test_real_arangodb_handlers.py
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import time
import json
from datetime import datetime
from typing import Dict, Any, List
import uuid

# Import handlers
from real_arangodb_handlers import (
    ArangoDocumentHandler,
    ArangoSearchHandler,
    ArangoGraphHandler,
    ArangoMemoryHandler,
    ArangoPaperHandler,
    ArangoBatchHandler,
    ARANGODB_AVAILABLE
)


class TestResults:
    """Track test results"""
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def add_result(self, test_name: str, description: str, 
                   result: Any, passed: bool, error: str = None):
        """Add a test result"""
        self.results.append({
            "test_name": test_name,
            "description": description,
            "result": str(result)[:200] if result else "None",
            "passed": passed,
            "error": error or "",
            "duration": time.time() - self.start_time
        })
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100):.1f}%")
        print("\nDetailed Results:")
        print("-"*80)
        
        for r in self.results:
            status = "✅ PASS" if r["passed"] else "❌ FAIL"
            print(f"{status} | {r['test_name']}: {r['description']}")
            if r["error"]:
                print(f"     Error: {r['error']}")
        
        print("="*80)
        return passed == total


def test_document_operations():
    """Test document CRUD operations"""
    print("\n🔍 Testing Document Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "document_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoDocumentHandler()
    test_collection = "test_documents"
    test_key = f"test_doc_{uuid.uuid4().hex[:8]}"
    
    # Test 1: Create document
    create_result = handler.handle({
        "action": "create",
        "collection": test_collection,
        "document": {
            "_key": test_key,
            "title": "Test Document",
            "content": "This is a test document for ArangoDB handler testing",
            "tags": ["test", "arangodb", "handler"],
            "score": 0.95
        }
    })
    
    results.add_result(
        "document_create",
        "Create a new document",
        create_result,
        create_result.get("success", False),
        create_result.get("error")
    )
    
    if create_result.get("success"):
        doc_id = create_result["data"]["document_id"]
        doc_key = create_result["data"]["document_key"]
        
        # Test 2: Read document
        read_result = handler.handle({
            "action": "read",
            "collection": test_collection,
            "document_key": doc_key
        })
        
        results.add_result(
            "document_read",
            "Read the created document",
            read_result,
            read_result.get("success", False) and 
            read_result.get("data", {}).get("document", {}).get("title") == "Test Document",
            read_result.get("error")
        )
        
        # Test 3: Update document
        update_result = handler.handle({
            "action": "update",
            "collection": test_collection,
            "document_key": doc_key,
            "updates": {
                "score": 0.98,
                "verified": True
            }
        })
        
        results.add_result(
            "document_update",
            "Update document fields",
            update_result,
            update_result.get("success", False),
            update_result.get("error")
        )
        
        # Test 4: Search documents
        search_result = handler.handle({
            "action": "search",
            "collection": test_collection,
            "query": {"tags": "test"},
            "limit": 10
        })
        
        results.add_result(
            "document_search",
            "Search documents by tag",
            search_result,
            search_result.get("success", False) and 
            len(search_result.get("data", {}).get("documents", [])) > 0,
            search_result.get("error")
        )
        
        # Test 5: Delete document
        delete_result = handler.handle({
            "action": "delete",
            "collection": test_collection,
            "document_key": doc_key
        })
        
        results.add_result(
            "document_delete",
            "Delete the test document",
            delete_result,
            delete_result.get("success", False),
            delete_result.get("error")
        )
    
    results.print_summary()
    return results


def test_search_operations():
    """Test advanced search operations"""
    print("\n🔍 Testing Search Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "search_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoSearchHandler()
    doc_handler = ArangoDocumentHandler()
    
    # Create test documents for searching
    test_docs = [
        {
            "title": "Machine Learning Fundamentals",
            "content": "Introduction to neural networks and deep learning architectures",
            "category": "AI",
            "year": 2023
        },
        {
            "title": "Quantum Computing Basics",
            "content": "Understanding quantum mechanics and quantum algorithms",
            "category": "Physics",
            "year": 2024
        },
        {
            "title": "Advanced Neural Networks",
            "content": "Deep learning with transformer architectures and attention mechanisms",
            "category": "AI",
            "year": 2024
        }
    ]
    
    # Create documents
    for doc in test_docs:
        doc_handler.handle({
            "action": "create",
            "collection": "test_search_docs",
            "document": doc
        })
    
    # Allow time for indexing
    time.sleep(1)
    
    # Test 1: BM25 search
    bm25_result = handler.handle({
        "search_type": "bm25",
        "query": "neural networks deep learning",
        "collection": "test_search_docs",
        "limit": 5
    })
    
    results.add_result(
        "search_bm25",
        "BM25 text search",
        bm25_result,
        bm25_result.get("success", False),
        bm25_result.get("error")
    )
    
    # Test 2: Semantic search
    semantic_result = handler.handle({
        "search_type": "semantic",
        "query": "artificial intelligence and machine learning",
        "collection": "test_search_docs",
        "limit": 5
    })
    
    results.add_result(
        "search_semantic",
        "Semantic vector search",
        semantic_result,
        semantic_result.get("success", False),
        semantic_result.get("error")
    )
    
    # Test 3: Hybrid search
    hybrid_result = handler.handle({
        "search_type": "hybrid",
        "query": "quantum computing algorithms",
        "collection": "test_search_docs",
        "limit": 5
    })
    
    results.add_result(
        "search_hybrid",
        "Hybrid search (BM25 + semantic)",
        hybrid_result,
        hybrid_result.get("success", False),
        hybrid_result.get("error")
    )
    
    # Test 4: Filtered search
    filtered_result = handler.handle({
        "search_type": "bm25",
        "query": "learning",
        "collection": "test_search_docs",
        "filters": {"category": "AI"},
        "limit": 5
    })
    
    results.add_result(
        "search_filtered",
        "Search with filters",
        filtered_result,
        filtered_result.get("success", False),
        filtered_result.get("error")
    )
    
    results.print_summary()
    return results


def test_graph_operations():
    """Test graph database operations"""
    print("\n🔍 Testing Graph Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "graph_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoGraphHandler()
    doc_handler = ArangoDocumentHandler()
    
    # Create test documents
    doc1_result = doc_handler.handle({
        "action": "create",
        "collection": "test_graph_docs",
        "document": {"name": "Document A", "type": "source"}
    })
    
    doc2_result = doc_handler.handle({
        "action": "create",
        "collection": "test_graph_docs",
        "document": {"name": "Document B", "type": "target"}
    })
    
    doc3_result = doc_handler.handle({
        "action": "create",
        "collection": "test_graph_docs",
        "document": {"name": "Document C", "type": "intermediate"}
    })
    
    if all(r.get("success") for r in [doc1_result, doc2_result, doc3_result]):
        doc1_id = doc1_result["data"]["document_id"]
        doc2_id = doc2_result["data"]["document_id"]
        doc3_id = doc3_result["data"]["document_id"]
        
        # Test 1: Create edges
        edge1_result = handler.handle({
            "action": "create_edge",
            "from_id": doc1_id,
            "to_id": doc3_id,
            "edge_collection": "test_edges",
            "edge_data": {"relationship": "connects_to", "weight": 0.8}
        })
        
        results.add_result(
            "graph_create_edge_1",
            "Create edge A->C",
            edge1_result,
            edge1_result.get("success", False),
            edge1_result.get("error")
        )
        
        edge2_result = handler.handle({
            "action": "create_edge",
            "from_id": doc3_id,
            "to_id": doc2_id,
            "edge_collection": "test_edges",
            "edge_data": {"relationship": "connects_to", "weight": 0.9}
        })
        
        results.add_result(
            "graph_create_edge_2",
            "Create edge C->B",
            edge2_result,
            edge2_result.get("success", False),
            edge2_result.get("error")
        )
        
        # Test 2: Traverse graph
        traverse_result = handler.handle({
            "action": "traverse",
            "start_id": doc1_id,
            "direction": "outbound",
            "max_depth": 2,
            "edge_collection": "test_edges"
        })
        
        results.add_result(
            "graph_traverse",
            "Traverse from A outbound",
            traverse_result,
            traverse_result.get("success", False) and
            len(traverse_result.get("data", {}).get("traversal_results", [])) > 0,
            traverse_result.get("error")
        )
        
        # Test 3: Find path
        path_result = handler.handle({
            "action": "find_path",
            "from_id": doc1_id,
            "to_id": doc2_id,
            "edge_collection": "test_edges"
        })
        
        results.add_result(
            "graph_find_path",
            "Find path from A to B",
            path_result,
            path_result.get("success", False),
            path_result.get("error")
        )
        
        # Test 4: Get neighbors
        neighbors_result = handler.handle({
            "action": "get_neighbors",
            "document_id": doc3_id,
            "direction": "any",
            "edge_collection": "test_edges"
        })
        
        results.add_result(
            "graph_get_neighbors",
            "Get neighbors of C",
            neighbors_result,
            neighbors_result.get("success", False) and
            neighbors_result.get("data", {}).get("count", 0) == 2,
            neighbors_result.get("error")
        )
    
    results.print_summary()
    return results


def test_memory_operations():
    """Test memory agent operations"""
    print("\n🔍 Testing Memory Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "memory_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoMemoryHandler()
    conversation_id = f"test_conv_{uuid.uuid4().hex[:8]}"
    
    # Test 1: Store message
    store_result = handler.handle({
        "action": "store",
        "conversation_id": conversation_id,
        "message": {
            "content": "Hello, I need help with machine learning",
            "metadata": {"intent": "help_request"}
        },
        "message_type": "user"
    })
    
    results.add_result(
        "memory_store",
        "Store user message",
        store_result,
        store_result.get("success", False),
        store_result.get("error")
    )
    
    # Store agent response
    store_result2 = handler.handle({
        "action": "store",
        "conversation_id": conversation_id,
        "message": {
            "content": "I'd be happy to help with machine learning. What specific topic?",
            "metadata": {"intent": "help_offer"}
        },
        "message_type": "agent"
    })
    
    results.add_result(
        "memory_store_agent",
        "Store agent message",
        store_result2,
        store_result2.get("success", False),
        store_result2.get("error")
    )
    
    # Test 2: Recall messages
    recall_result = handler.handle({
        "action": "recall",
        "conversation_id": conversation_id,
        "limit": 10
    })
    
    results.add_result(
        "memory_recall",
        "Recall conversation history",
        recall_result,
        recall_result.get("success", False) and
        len(recall_result.get("data", {}).get("messages", [])) == 2,
        recall_result.get("error")
    )
    
    # Test 3: Search memory
    search_result = handler.handle({
        "action": "search",
        "query": "machine learning help",
        "limit": 5
    })
    
    results.add_result(
        "memory_search",
        "Search across memories",
        search_result,
        search_result.get("success", False),
        search_result.get("error")
    )
    
    # Test 4: Get context
    context_result = handler.handle({
        "action": "get_context",
        "query": "machine learning",
        "conversation_id": conversation_id,
        "context_window": 3
    })
    
    results.add_result(
        "memory_context",
        "Get relevant context",
        context_result,
        context_result.get("success", False),
        context_result.get("error")
    )
    
    results.print_summary()
    return results


def test_paper_operations():
    """Test ArXiv paper-specific operations"""
    print("\n🔍 Testing Paper Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "paper_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoPaperHandler()
    
    # Test 1: Store paper
    paper_data = {
        "id": "arxiv:2401.12345",
        "title": "Advanced Transformer Architectures for NLP",
        "authors": ["John Doe", "Jane Smith"],
        "summary": "We present a novel transformer architecture that improves performance on various NLP tasks",
        "categories": ["cs.CL", "cs.AI"],
        "published": "2024-01-15T10:00:00Z"
    }
    
    store_result = handler.handle({
        "action": "store_paper",
        "paper": paper_data
    })
    
    results.add_result(
        "paper_store",
        "Store ArXiv paper",
        store_result,
        store_result.get("success", False),
        store_result.get("error")
    )
    
    if store_result.get("success"):
        paper_id = store_result["data"]["paper_id"]
        
        # Store another paper for similarity/citation tests
        paper_data2 = {
            "id": "arxiv:2401.12346",
            "title": "BERT: Pre-training of Deep Bidirectional Transformers",
            "authors": ["Alice Brown", "Bob Wilson"],
            "summary": "BERT is designed to pre-train deep bidirectional representations",
            "categories": ["cs.CL"],
            "published": "2024-01-16T10:00:00Z"
        }
        
        store_result2 = handler.handle({
            "action": "store_paper",
            "paper": paper_data2
        })
        
        if store_result2.get("success"):
            paper_id2 = store_result2["data"]["paper_id"]
            
            # Test 2: Find similar papers
            similar_result = handler.handle({
                "action": "find_similar",
                "paper_id": paper_id,
                "limit": 5
            })
            
            results.add_result(
                "paper_find_similar",
                "Find similar papers",
                similar_result,
                similar_result.get("success", False),
                similar_result.get("error")
            )
            
            # Test 3: Create citation
            citation_result = handler.handle({
                "action": "create_citation",
                "citing_paper_id": paper_id,
                "cited_paper_id": paper_id2,
                "citation_type": "references",
                "confidence": 0.95
            })
            
            results.add_result(
                "paper_create_citation",
                "Create citation relationship",
                citation_result,
                citation_result.get("success", False),
                citation_result.get("error")
            )
        
        # Test 4: Analyze topic
        topic_result = handler.handle({
            "action": "analyze_topic",
            "topic": "transformer architectures",
            "limit": 10
        })
        
        results.add_result(
            "paper_analyze_topic",
            "Analyze papers by topic",
            topic_result,
            topic_result.get("success", False) and
            topic_result.get("data", {}).get("paper_count", 0) > 0,
            topic_result.get("error")
        )
    
    results.print_summary()
    return results


def test_batch_operations():
    """Test batch processing of multiple operations"""
    print("\n🔍 Testing Batch Operations...")
    results = TestResults()
    
    if not ARANGODB_AVAILABLE:
        results.add_result(
            "batch_availability",
            "Check ArangoDB availability",
            None,
            False,
            "ArangoDB module not available"
        )
        results.print_summary()
        return results
    
    handler = ArangoBatchHandler()
    
    # Create batch operations
    batch_ops = [
        {
            "type": "document",
            "params": {
                "action": "create",
                "collection": "test_batch",
                "document": {"name": "Batch Doc 1", "value": 100}
            }
        },
        {
            "type": "document",
            "params": {
                "action": "create",
                "collection": "test_batch",
                "document": {"name": "Batch Doc 2", "value": 200}
            }
        },
        {
            "type": "search",
            "params": {
                "search_type": "bm25",
                "query": "batch",
                "collection": "test_batch",
                "limit": 5
            }
        },
        {
            "type": "paper",
            "params": {
                "action": "store_paper",
                "paper": {
                    "id": "batch:001",
                    "title": "Batch Processing in Databases",
                    "summary": "Efficient batch processing techniques"
                }
            }
        }
    ]
    
    # Execute batch
    batch_result = handler.handle({
        "operations": batch_ops
    })
    
    results.add_result(
        "batch_execute",
        "Execute batch operations",
        batch_result,
        batch_result.get("success", False) and
        batch_result.get("data", {}).get("successful", 0) >= 3,
        batch_result.get("error")
    )
    
    # Check batch results
    if batch_result.get("success"):
        data = batch_result.get("data", {})
        results.add_result(
            "batch_verify",
            "Verify batch results",
            data,
            data.get("total_operations") == 4 and
            data.get("successful") >= 3,
            None
        )
    
    results.print_summary()
    return results


def main():
    """Run all tests"""
    print("="*80)
    print("ARANGODB HANDLERS TEST SUITE")
    print("="*80)
    
    if not ARANGODB_AVAILABLE:
        print("\n⚠️  WARNING: ArangoDB module not available!")
        print("Please ensure ArangoDB module is installed at:")
        print("/home/graham/workspace/experiments/arangodb/")
        return
    
    all_results = []
    
    # Run all test suites
    test_suites = [
        ("Document Operations", test_document_operations),
        ("Search Operations", test_search_operations),
        ("Graph Operations", test_graph_operations),
        ("Memory Operations", test_memory_operations),
        ("Paper Operations", test_paper_operations),
        ("Batch Operations", test_batch_operations)
    ]
    
    total_passed = 0
    total_tests = 0
    
    for suite_name, test_func in test_suites:
        try:
            results = test_func()
            suite_passed = sum(1 for r in results.results if r["passed"])
            suite_total = len(results.results)
            total_passed += suite_passed
            total_tests += suite_total
            all_results.extend(results.results)
        except Exception as e:
            print(f"\n❌ {suite_name} suite failed: {e}")
            total_tests += 1
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL TEST SUMMARY")
    print("="*80)
    print(f"Total Test Suites: {len(test_suites)}")
    print(f"Total Tests Run: {total_tests}")
    print(f"Total Passed: {total_passed} ✅")
    print(f"Total Failed: {total_tests - total_passed} ❌")
    print(f"Overall Success Rate: {(total_passed/total_tests*100):.1f}%")
    print("="*80)
    
    # Generate test report
    generate_test_report(all_results)
    
    # Exit with appropriate code
    exit(0 if total_passed == total_tests else 1)


def generate_test_report(results: List[Dict[str, Any]]):
    """Generate markdown test report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"arangodb_handlers_test_report_{timestamp}.md"
    
    content = f"""# ArangoDB Handlers Test Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
- Total Tests: {len(results)}
- Passed: {sum(1 for r in results if r["passed"])}
- Failed: {sum(1 for r in results if not r["passed"])}

## Test Results

| Test Name | Description | Result | Status | Duration | Error |
|-----------|-------------|--------|--------|----------|-------|
"""
    
    for r in results:
        status = "✅ Pass" if r["passed"] else "❌ Fail"
        content += f"| {r['test_name']} | {r['description']} | {r['result'][:50]}... | {status} | {r['duration']:.2f}s | {r['error'] or '-'} |\n"
    
    with open(report_path, 'w') as f:
        f.write(content)
    
    print(f"\n📄 Test report saved to: {report_path}")


if __name__ == "__main__":
    main()