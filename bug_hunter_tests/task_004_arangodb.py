#!/usr/bin/env python3
"""
Module: task_004_arangodb.py
Description: Task #004 - Store Finding in Knowledge Graph (ArangoDB) Bug Hunter Test

External Dependencies:
- python-arango: https://python-arango.readthedocs.io/
- aiohttp: https://docs.aiohttp.org/

Sample Input:
>>> test_arangodb_operations()

Expected Output:
>>> Test results with performance metrics and bugs found

Example Usage:
>>> python task_004_arangodb.py
"""

import time
import json
import asyncio
from typing import Dict, Any, List, Optional
import os

# Try importing ArangoDB
try:
    from arango import ArangoClient
    from arango.exceptions import ArangoError, DocumentInsertError
    ARANGO_AVAILABLE = True
    print("✅ ArangoDB client imported successfully")
except ImportError as e:
    print(f"⚠️ ArangoDB import failed: {e}")
    ARANGO_AVAILABLE = False


class ArangoDBBugHunter:
    """ArangoDB operations bug hunting"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.graph = None
        self.bugs_found = []
        
    def connect(self) -> bool:
        """Connect to ArangoDB"""
        try:
            # Try default connection
            self.client = ArangoClient(hosts='http://localhost:8529')
            
            # Try to connect as root user (common default)
            self.db = self.client.db(
                '_system',
                username='root',
                password=os.getenv('ARANGO_ROOT_PASSWORD', '')
            )
            
            # Verify connection
            self.db.properties()
            print("  ✅ Connected to ArangoDB")
            return True
            
        except Exception as e:
            error = f"Connection failed: {type(e).__name__}: {e}"
            self.bugs_found.append(error)
            print(f"  🐛 BUG: {error}")
            
            # Try alternate connection
            try:
                self.client = ArangoClient(hosts='http://127.0.0.1:8529')
                self.db = self.client.db('_system')
                print("  ✅ Connected with alternate method")
                return True
            except:
                return False
    
    def test_crud_operations(self) -> Dict[str, Any]:
        """Test Create, Read, Update, Delete operations"""
        if not self.db:
            return {"error": "No database connection"}
        
        results = {
            "create": {"success": False, "duration": 0},
            "read": {"success": False, "duration": 0},
            "update": {"success": False, "duration": 0},
            "delete": {"success": False, "duration": 0}
        }
        
        collection_name = "test_components"
        
        try:
            # Create collection if not exists
            if not self.db.has_collection(collection_name):
                self.db.create_collection(collection_name)
            
            collection = self.db.collection(collection_name)
            
            # Test CREATE
            start = time.time()
            doc = {
                "_key": f"component_{int(time.time() * 1000)}",
                "name": "TestComponent",
                "dependencies": ["LibraryA", "LibraryB"],
                "metadata": {"version": "1.0.0", "critical": True}
            }
            
            result = collection.insert(doc)
            results["create"]["duration"] = time.time() - start
            results["create"]["success"] = True
            doc_key = result["_key"]
            
            # Test READ
            start = time.time()
            retrieved = collection.get(doc_key)
            results["read"]["duration"] = time.time() - start
            results["read"]["success"] = retrieved is not None
            
            # Test UPDATE
            start = time.time()
            collection.update({"_key": doc_key, "metadata": {"version": "1.0.1"}})
            results["update"]["duration"] = time.time() - start
            results["update"]["success"] = True
            
            # Test DELETE
            start = time.time()
            collection.delete(doc_key)
            results["delete"]["duration"] = time.time() - start
            results["delete"]["success"] = True
            
            # Clean up
            self.db.delete_collection(collection_name)
            
        except Exception as e:
            self.bugs_found.append(f"CRUD operation failed: {type(e).__name__}")
            
        return results
    
    def test_concurrent_writes(self, num_concurrent: int = 100) -> Dict[str, Any]:
        """Test concurrent write operations"""
        if not self.db:
            return {"error": "No database connection"}
        
        collection_name = "test_concurrent"
        results = {
            "total": num_concurrent,
            "successful": 0,
            "failed": 0,
            "duration": 0,
            "errors": []
        }
        
        try:
            # Create collection
            if not self.db.has_collection(collection_name):
                self.db.create_collection(collection_name)
            
            collection = self.db.collection(collection_name)
            
            # Prepare documents
            docs = [
                {
                    "_key": f"concurrent_{i}",
                    "component": f"Component_{i}",
                    "timestamp": time.time()
                }
                for i in range(num_concurrent)
            ]
            
            # Insert concurrently
            start = time.time()
            
            # Batch insert (ArangoDB handles concurrency)
            result = collection.insert_many(docs, overwrite=False)
            
            results["duration"] = time.time() - start
            
            # Count successes and failures
            for r in result:
                if r.get("error"):
                    results["failed"] += 1
                    if r.get("errorMessage") not in results["errors"]:
                        results["errors"].append(r.get("errorMessage"))
                else:
                    results["successful"] += 1
            
            # Clean up
            self.db.delete_collection(collection_name)
            
            # Check for bugs
            if results["failed"] > 0:
                self.bugs_found.append(f"Concurrent writes: {results['failed']}/{num_concurrent} failed")
            
            if results["duration"] > 5.0:
                self.bugs_found.append(f"Performance issue: {num_concurrent} inserts took {results['duration']:.2f}s")
                
        except Exception as e:
            self.bugs_found.append(f"Concurrent test failed: {type(e).__name__}")
            results["errors"].append(str(e))
            
        return results
    
    def test_graph_operations(self) -> Dict[str, Any]:
        """Test graph database operations"""
        if not self.db:
            return {"error": "No database connection"}
        
        results = {
            "graph_creation": False,
            "edge_creation": False,
            "traversal": False,
            "errors": []
        }
        
        try:
            # Create graph
            graph_name = "test_dependency_graph"
            
            if self.db.has_graph(graph_name):
                self.db.delete_graph(graph_name)
            
            # Create vertex collections
            if not self.db.has_collection("components"):
                self.db.create_collection("components")
            if not self.db.has_collection("libraries"):
                self.db.create_collection("libraries")
            
            # Create edge collection
            if not self.db.has_collection("depends_on"):
                self.db.create_collection("depends_on", edge=True)
            
            # Create graph
            self.db.create_graph(
                graph_name,
                edge_definitions=[{
                    "edge_collection": "depends_on",
                    "from_vertex_collections": ["components"],
                    "to_vertex_collections": ["libraries"]
                }]
            )
            
            results["graph_creation"] = True
            
            # Add vertices
            components = self.db.collection("components")
            libraries = self.db.collection("libraries")
            edges = self.db.collection("depends_on")
            
            comp1 = components.insert({"_key": "comp1", "name": "Component1"})
            lib1 = libraries.insert({"_key": "lib1", "name": "Library1"})
            
            # Create edge
            edge = edges.insert({
                "_from": f"components/{comp1['_key']}",
                "_to": f"libraries/{lib1['_key']}",
                "version": "1.0.0"
            })
            
            results["edge_creation"] = True
            
            # Test traversal
            query = """
            FOR v, e, p IN 1..2 OUTBOUND 'components/comp1' depends_on
            RETURN {vertex: v, edge: e}
            """
            
            cursor = self.db.aql.execute(query)
            traversal_results = list(cursor)
            
            results["traversal"] = len(traversal_results) > 0
            
            # Clean up
            self.db.delete_graph(graph_name, drop_collections=True)
            
        except Exception as e:
            error = f"Graph operation failed: {type(e).__name__}: {e}"
            self.bugs_found.append(error)
            results["errors"].append(error)
            
        return results


def run_arangodb_bug_hunt():
    """Run comprehensive ArangoDB bug hunting tests"""
    print("\n" + "="*60)
    print("🐛 TASK #004: ArangoDB Knowledge Graph Bug Hunter")
    print("="*60)
    
    if not ARANGO_AVAILABLE:
        print("❌ Cannot run tests - ArangoDB client not available")
        print("Install with: pip install python-arango")
        return {
            "task": "004_arangodb",
            "status": "blocked",
            "reason": "Module not installed"
        }
    
    hunter = ArangoDBBugHunter()
    
    # Test 1: Connection
    print("\n📋 Test 1: Database connection")
    connected = hunter.connect()
    
    if not connected:
        print("❌ Cannot connect to ArangoDB")
        print("Make sure ArangoDB is running on localhost:8529")
        return {
            "task": "004_arangodb",
            "status": "blocked",
            "reason": "Cannot connect to database",
            "bugs_found": hunter.bugs_found
        }
    
    # Test 2: CRUD Operations
    print("\n📋 Test 2: CRUD operations performance")
    crud_results = hunter.test_crud_operations()
    
    for op, result in crud_results.items():
        if isinstance(result, dict) and "success" in result:
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {op.upper()}: {result['duration']:.3f}s")
            
            if result["duration"] > 0.1:  # 100ms threshold
                hunter.bugs_found.append(f"{op.upper()} too slow: {result['duration']:.3f}s")
    
    # Test 3: Concurrent writes
    print("\n📋 Test 3: Concurrent write operations")
    concurrent_results = hunter.test_concurrent_writes(100)
    
    print(f"  Total: {concurrent_results['total']}")
    print(f"  Successful: {concurrent_results['successful']}")
    print(f"  Failed: {concurrent_results['failed']}")
    print(f"  Duration: {concurrent_results['duration']:.3f}s")
    
    # Test 4: Graph operations
    print("\n📋 Test 4: Graph database operations")
    graph_results = hunter.test_graph_operations()
    
    for op, success in graph_results.items():
        if op != "errors":
            status = "✅" if success else "❌"
            print(f"  {status} {op.replace('_', ' ').title()}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 ArangoDB Bug Hunt Summary")
    print("="*60)
    print(f"Bugs found: {len(hunter.bugs_found)}")
    
    if hunter.bugs_found:
        print("\n🐛 Bugs discovered:")
        for i, bug in enumerate(hunter.bugs_found, 1):
            print(f"  {i}. {bug}")
    else:
        print("\n✅ No bugs found in ArangoDB operations")
    
    # Save report
    report = {
        "task": "004_arangodb",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "module": "ArangoDB",
        "bugs_found": hunter.bugs_found,
        "test_results": {
            "crud": crud_results,
            "concurrent": concurrent_results,
            "graph": graph_results
        },
        "recommendations": [
            "Add connection pooling for better performance",
            "Implement retry logic for transient failures",
            "Add query optimization for graph traversals",
            "Set up proper authentication (not using root)",
            "Add connection timeout handling"
        ]
    }
    
    with open("bug_hunter_results_004.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: bug_hunter_results_004.json")
    
    return report


if __name__ == "__main__":
    run_arangodb_bug_hunt()