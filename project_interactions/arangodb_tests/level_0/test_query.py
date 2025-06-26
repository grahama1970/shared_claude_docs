"""
Test ArangoDB query functionality with real database operations.
Tests execute actual AQL queries and verify response times.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
import json
from typing import Dict, Any, List
from arango import ArangoClient
from arango.exceptions import AQLQueryExecuteError, CollectionCreateError

# ArangoDB connection settings
ARANGO_HOST = "http://localhost:8529"
ARANGO_DB = "youtube_transcripts_test"
ARANGO_USER = "root"
ARANGO_PASS = "openSesame"  # Often empty for local dev

class TestArangoDBQuery:
    """Test AQL query execution with real database"""
    
    @classmethod
    def setup_class(cls):
        """Set up test database and collections"""
        cls.client = ArangoClient(hosts=ARANGO_HOST)
        
        # Connect to system database first
        sys_db = cls.client.db('_system', username=ARANGO_USER, password=ARANGO_PASS)
        
        # Create test database if it doesn't exist
        if not sys_db.has_database(ARANGO_DB):
            sys_db.create_database(ARANGO_DB)
        
        # Connect to test database
        cls.db = cls.client.db(ARANGO_DB, username=ARANGO_USER, password=ARANGO_PASS)
        
        # Create test collection if it doesn't exist
        if not cls.db.has_collection('test_documents'):
            cls.collection = cls.db.create_collection('test_documents')
        else:
            cls.collection = cls.db.collection('test_documents')
            
        # Insert test data
        cls._insert_test_data()
    
    @classmethod
    def _insert_test_data(cls):
        """Insert test documents"""
        test_docs = [
            {"_key": "doc1", "name": "Test Document 1", "category": "A", "value": 100},
            {"_key": "doc2", "name": "Test Document 2", "category": "B", "value": 200},
            {"_key": "doc3", "name": "Test Document 3", "category": "A", "value": 300},
            {"_key": "doc4", "name": "Test Document 4", "category": "C", "value": 150},
            {"_key": "doc5", "name": "Test Document 5", "category": "B", "value": 250}
        ]
        
        for doc in test_docs:
            try:
                cls.collection.insert(doc)
            except:
                # Document might already exist
                pass
    
    def test_simple_query(self):
        """Test simple FOR...RETURN query"""
        start_time = time.time()
        
        query = """
        FOR doc IN test_documents
        RETURN doc
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) >= 5, f"Expected at least 5 documents, got {len(results)}"
        assert 0 < duration < 1.0, f"Query took {duration}s, expected 0.01-1.0s"
        
        # Verify data structure
        for doc in results:
            assert '_key' in doc
            assert 'name' in doc
            assert 'category' in doc
            assert 'value' in doc
        
        print(f"✅ Simple query returned {len(results)} documents in {duration:.3f}s")
    
    def test_filtered_query(self):
        """Test query with FILTER clause"""
        start_time = time.time()
        
        query = """
        FOR doc IN test_documents
        FILTER doc.category == @category
        RETURN doc
        """
        
        bind_vars = {'category': 'A'}
        cursor = self.db.aql.execute(query, bind_vars=bind_vars)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) >= 2, f"Expected at least 2 category A documents"
        assert all(doc['category'] == 'A' for doc in results)
        assert 0 < duration < 0.5, f"Query took {duration}s"
        
        print(f"✅ Filtered query returned {len(results)} documents in {duration:.3f}s")
    
    def test_aggregation_query(self):
        """Test query with aggregation functions"""
        start_time = time.time()
        
        query = """
        FOR doc IN test_documents
        COLLECT category = doc.category
        AGGREGATE 
            count = COUNT(1),
            total = SUM(doc.value),
            avg = AVG(doc.value)
        RETURN {
            category: category,
            count: count,
            total: total,
            average: avg
        }
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) >= 3, f"Expected at least 3 categories"
        assert 0 < duration < 0.5, f"Query took {duration}s"
        
        # Verify aggregation structure
        for result in results:
            assert 'category' in result
            assert 'count' in result
            assert 'total' in result
            assert 'average' in result
            assert result['count'] > 0
            assert result['total'] > 0
            assert result['average'] > 0
        
        print(f"✅ Aggregation query completed in {duration:.3f}s")
    
    def test_sort_limit_query(self):
        """Test query with SORT and LIMIT"""
        start_time = time.time()
        
        query = """
        FOR doc IN test_documents
        SORT doc.value DESC
        LIMIT 3
        RETURN {
            name: doc.name,
            value: doc.value
        }
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) == 3, f"Expected exactly 3 documents"
        assert 0 < duration < 0.5, f"Query took {duration}s"
        
        # Verify sorting
        values = [r['value'] for r in results]
        assert values == sorted(values, reverse=True), "Results not properly sorted"
        
        print(f"✅ Sort/limit query returned top 3 documents in {duration:.3f}s")
    
    def test_join_query(self):
        """Test query with JOIN-like operation"""
        # Create a second collection for joining
        if not self.db.has_collection('test_categories'):
            cat_collection = self.db.create_collection('test_categories')
        else:
            cat_collection = self.db.collection('test_categories')
        
        # Insert category data
        categories = [
            {"_key": "A", "description": "Category Alpha", "priority": 1},
            {"_key": "B", "description": "Category Beta", "priority": 2},
            {"_key": "C", "description": "Category Charlie", "priority": 3}
        ]
        
        for cat in categories:
            try:
                cat_collection.insert(cat)
            except:
                pass
        
        start_time = time.time()
        
        query = """
        FOR doc IN test_documents
        FOR cat IN test_categories
        FILTER doc.category == cat._key
        RETURN {
            document: doc.name,
            value: doc.value,
            category_desc: cat.description,
            priority: cat.priority
        }
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) >= 5, f"Expected at least 5 joined results"
        assert 0 < duration < 1.0, f"Query took {duration}s"
        
        # Verify join worked
        for result in results:
            assert 'document' in result
            assert 'category_desc' in result
            assert 'priority' in result
            assert result['priority'] in [1, 2, 3]
        
        print(f"✅ Join query completed in {duration:.3f}s with {len(results)} results")
    
    def test_complex_query(self):
        """Test complex query with multiple operations"""
        start_time = time.time()
        
        query = """
        LET total_value = (
            FOR d IN test_documents
            RETURN d.value
        )
        
        LET avg_value = AVG(total_value)
        
        FOR doc IN test_documents
        FILTER doc.value > avg_value
        SORT doc.value DESC
        RETURN {
            name: doc.name,
            value: doc.value,
            above_average_by: doc.value - avg_value,
            category: doc.category
        }
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) > 0, "Expected some above-average documents"
        assert 0 < duration < 1.0, f"Query took {duration}s"
        
        # Verify all results are above average
        for result in results:
            assert result['above_average_by'] > 0
        
        print(f"✅ Complex query found {len(results)} above-average documents in {duration:.3f}s")
    
    @classmethod
    def teardown_class(cls):
        """Clean up test data"""
        # We keep the test data for other tests
        pass

def measure_query_performance(db, query: str, bind_vars: Dict = None) -> Dict[str, Any]:
    """Helper to measure query performance"""
    start_time = time.time()
    
    try:
        cursor = db.aql.execute(query, bind_vars=bind_vars)
        results = list(cursor)
        success = True
        error = None
    except Exception as e:
        results = []
        success = False
        error = str(e)
    
    duration = time.time() - start_time
    
    return {
        'duration': duration,
        'result_count': len(results),
        'success': success,
        'error': error,
        'results': results[:5]  # First 5 for preview
    }

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])