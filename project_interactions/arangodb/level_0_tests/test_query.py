"""
Module: test_query.py
Purpose: Test AQL query execution capabilities in ArangoDB

External Dependencies:
- python-arango: https://python-arango.readthedocs.io/
- loguru: https://github.com/Delgan/loguru

Example Usage:
>>> from test_query import TestArangoDBQuery
>>> test = TestArangoDBQuery()
>>> result = test.test_basic_query()
>>> print(f"Query executed in {result.duration:.2f}s")
"""

import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from templates.interaction_framework import (
    Level0Interaction,
    InteractionResult,
    InteractionLevel
)

# Import ArangoDB dependencies
try:
    from arango import ArangoClient
    from arango.exceptions import AQLQueryExecuteError, ServerConnectionError
    HAS_ARANGO = True
except ImportError:
    HAS_ARANGO = False
    print("⚠️  python-arango not installed. Install with: pip install python-arango")


class TestArangoDBQuery(Level0Interaction):
    """Test AQL query execution in ArangoDB."""
    
    def __init__(self):
        super().__init__(
            module_name="arangodb",
            interaction_name="test_query"
        )
        
        # ArangoDB connection settings
        self.arango_host = os.getenv("ARANGO_HOST", "http://localhost:8529")
        self.arango_user = os.getenv("ARANGO_USER", "root")
        self.arango_password = os.getenv("ARANGO_PASSWORD", "")
        self.arango_db = os.getenv("ARANGO_DB_NAME", "knowledge_graph")
        
        self.client = None
        self.db = None
        
    def connect(self) -> bool:
        """Connect to ArangoDB."""
        if not HAS_ARANGO:
            return False
            
        try:
            self.client = ArangoClient(hosts=self.arango_host)
            self.db = self.client.db(
                self.arango_db,
                username=self.arango_user,
                password=self.arango_password
            )
            # Test connection
            self.db.ping()
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_basic_query(self) -> InteractionResult:
        """Test basic AQL query execution."""
        start_time = time.time()
        
        if not self.connect():
            return InteractionResult(
                interaction_name="test_basic_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error="Failed to connect to ArangoDB"
            )
        
        try:
            # Simple query to get system collections
            query = """
            FOR collection IN 1..1
            RETURN {
                name: COLLECTIONS()[0],
                type: "system"
            }
            LIMIT 5
            """
            
            cursor = self.db.aql.execute(query)
            results = list(cursor)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="test_basic_query",
                level=InteractionLevel.LEVEL_0,
                success=True,
                duration=duration,
                input_data={"query": query},
                output_data={
                    "result_count": len(results),
                    "execution_time_ms": duration * 1000,
                    "sample_results": results[:3] if results else [],
                    "timestamp": datetime.now().isoformat()
                },
                error=None
            )
            
        except AQLQueryExecuteError as e:
            return InteractionResult(
                interaction_name="test_basic_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"query": query},
                output_data={},
                error=f"AQL query failed: {str(e)}"
            )
        except Exception as e:
            return InteractionResult(
                interaction_name="test_basic_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def test_parameterized_query(self) -> InteractionResult:
        """Test parameterized AQL query with bind variables."""
        start_time = time.time()
        
        if not self.connect():
            return InteractionResult(
                interaction_name="test_parameterized_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error="Failed to connect to ArangoDB"
            )
        
        try:
            # Ensure test collection exists
            if not self.db.has_collection("test_documents"):
                self.db.create_collection("test_documents")
            
            collection = self.db.collection("test_documents")
            
            # Insert test documents
            test_docs = [
                {"name": "Document A", "value": 100, "category": "alpha"},
                {"name": "Document B", "value": 200, "category": "beta"},
                {"name": "Document C", "value": 300, "category": "alpha"},
                {"name": "Document D", "value": 150, "category": "beta"}
            ]
            
            collection.truncate()  # Clear existing data
            collection.insert_many(test_docs)
            
            # Parameterized query
            query = """
            FOR doc IN test_documents
            FILTER doc.category == @category AND doc.value >= @min_value
            SORT doc.value DESC
            RETURN {
                name: doc.name,
                value: doc.value,
                category: doc.category
            }
            """
            
            bind_vars = {
                "category": "alpha",
                "min_value": 100
            }
            
            cursor = self.db.aql.execute(query, bind_vars=bind_vars)
            results = list(cursor)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="test_parameterized_query",
                level=InteractionLevel.LEVEL_0,
                success=len(results) == 2,  # Should find 2 alpha documents
                duration=duration,
                input_data={
                    "query": query,
                    "bind_vars": bind_vars
                },
                output_data={
                    "result_count": len(results),
                    "results": results,
                    "execution_time_ms": duration * 1000,
                    "timestamp": datetime.now().isoformat()
                },
                error=None if len(results) == 2 else f"Expected 2 results, got {len(results)}"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="test_parameterized_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def test_aggregation_query(self) -> InteractionResult:
        """Test complex aggregation query."""
        start_time = time.time()
        
        if not self.connect():
            return InteractionResult(
                interaction_name="test_aggregation_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error="Failed to connect to ArangoDB"
            )
        
        try:
            # Complex aggregation query
            query = """
            FOR doc IN test_documents
            COLLECT category = doc.category
            AGGREGATE
                total = SUM(doc.value),
                avg = AVG(doc.value),
                count = COUNT(doc.value),
                min = MIN(doc.value),
                max = MAX(doc.value)
            RETURN {
                category: category,
                statistics: {
                    total: total,
                    average: avg,
                    count: count,
                    min: min,
                    max: max
                }
            }
            """
            
            cursor = self.db.aql.execute(query)
            results = list(cursor)
            
            duration = time.time() - start_time
            
            # Verify aggregation results
            expected_categories = {"alpha", "beta"}
            actual_categories = {r["category"] for r in results}
            
            return InteractionResult(
                interaction_name="test_aggregation_query",
                level=InteractionLevel.LEVEL_0,
                success=actual_categories == expected_categories,
                duration=duration,
                input_data={"query": query},
                output_data={
                    "aggregations": results,
                    "category_count": len(results),
                    "execution_time_ms": duration * 1000,
                    "timestamp": datetime.now().isoformat()
                },
                error=None if actual_categories == expected_categories else "Aggregation mismatch"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="test_aggregation_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={},
                output_data={},
                error=str(e)
            )
    
    def execute(self, **kwargs) -> InteractionResult:
        """Execute all query tests."""
        start_time = time.time()
        
        results = []
        
        # Test 1: Basic query
        basic_result = self.test_basic_query()
        results.append(("Basic Query", basic_result))
        
        # Test 2: Parameterized query
        param_result = self.test_parameterized_query()
        results.append(("Parameterized Query", param_result))
        
        # Test 3: Aggregation query
        agg_result = self.test_aggregation_query()
        results.append(("Aggregation Query", agg_result))
        
        # Compile summary
        total_tests = len(results)
        passed_tests = sum(1 for _, r in results if r.success)
        
        return InteractionResult(
            interaction_name="arangodb_query_tests",
            level=InteractionLevel.LEVEL_0,
            success=passed_tests == total_tests,
            duration=time.time() - start_time,
            input_data=kwargs,
            output_data={
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": total_tests - passed_tests
                },
                "tests": [
                    {
                        "name": name,
                        "success": result.success,
                        "duration": result.duration,
                        "error": result.error
                    }
                    for name, result in results
                ],
                "timestamp": datetime.now().isoformat()
            },
            error=None if passed_tests == total_tests else f"{total_tests - passed_tests} tests failed"
        )


if __name__ == "__main__":
    # Test the query capabilities
    test = TestArangoDBQuery()
    
    print("🔍 Testing ArangoDB Query Operations...")
    
    # Test basic query
    print("\n1. Testing basic query...")
    result = test.test_basic_query()
    print(f"   {'✅' if result.success else '❌'} Duration: {result.duration:.2f}s")
    if result.success:
        print(f"   Results: {result.output_data.get('result_count', 0)} items")
    else:
        print(f"   Error: {result.error}")
    
    # Test parameterized query
    print("\n2. Testing parameterized query...")
    result = test.test_parameterized_query()
    print(f"   {'✅' if result.success else '❌'} Duration: {result.duration:.2f}s")
    if result.success:
        print(f"   Found: {result.output_data.get('result_count', 0)} documents")
    
    # Test aggregation
    print("\n3. Testing aggregation query...")
    result = test.test_aggregation_query()
    print(f"   {'✅' if result.success else '❌'} Duration: {result.duration:.2f}s")
    if result.success:
        print(f"   Categories: {result.output_data.get('category_count', 0)}")
    
    # Run all tests
    print("\n📊 Running all tests...")
    final_result = test.execute()
    
    summary = final_result.output_data.get('summary', {})
    print(f"\n✅ Passed: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} tests")
    print(f"⏱️  Total duration: {final_result.duration:.2f}s")
    
    if not final_result.success:
        print(f"❌ {final_result.error}")