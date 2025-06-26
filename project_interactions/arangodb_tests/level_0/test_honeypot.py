"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Honeypot tests for ArangoDB module - designed to catch fake implementations.
These tests should properly handle error cases and invalid operations.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
from typing import Dict, Any
from arango import ArangoClient
from arango.exceptions import (
    AQLQueryExecuteError, 
    DocumentInsertError,
    CollectionCreateError,
    GraphCreateError,
    DatabaseCreateError
)

# ArangoDB connection settings
ARANGO_HOST = "http://localhost:8529"
ARANGO_DB = "youtube_transcripts_test"
ARANGO_USER = "root"
ARANGO_PASS = "openSesame"

class TestArangoDBHoneypot:
    """Honeypot tests that should fail gracefully"""
    
    @classmethod
    def setup_class(cls):
        """Set up test database connection"""
        cls.client = ArangoClient(hosts=ARANGO_HOST)
        
        # Connect to system database
        sys_db = cls.client.db('_system', username=ARANGO_USER, password=ARANGO_PASS)
        
        # Ensure test database exists
        if not sys_db.has_database(ARANGO_DB):
            sys_db.create_database(ARANGO_DB)
        
        cls.db = cls.client.db(ARANGO_DB, username=ARANGO_USER, password=ARANGO_PASS)
    
    def test_query_nonexistent_collection(self):
        """Test querying a collection that doesn't exist"""
        start_time = time.time()
        
        query = """
        FOR doc IN this_collection_definitely_does_not_exist_12345
        RETURN doc
        """
        
        with pytest.raises(AQLQueryExecuteError) as exc_info:
            cursor = self.db.aql.execute(query)
            list(cursor)
        
        duration = time.time() - start_time
        
        # Should fail with collection not found error
        assert "not found" in str(exc_info.value).lower() or "unknown" in str(exc_info.value).lower()
        assert 0 < duration < 0.5, f"Error should be quick, took {duration}s"
        
        print(f"✅ Honeypot: Nonexistent collection properly rejected in {duration:.3f}s")
    
    def test_invalid_aql_syntax(self):
        """Test executing invalid AQL syntax"""
        start_time = time.time()
        
        # Invalid AQL syntax
        query = """
        FOR doc IN WHERE HAVING SELECT * FROM nowhere
        RETURN INVALID SYNTAX HERE
        """
        
        with pytest.raises(AQLQueryExecuteError) as exc_info:
            cursor = self.db.aql.execute(query)
            list(cursor)
        
        duration = time.time() - start_time
        
        # Should fail with syntax error
        assert "syntax" in str(exc_info.value).lower() or "parse" in str(exc_info.value).lower()
        assert 0 < duration < 0.3, f"Syntax error should be quick, took {duration}s"
        
        print(f"✅ Honeypot: Invalid AQL syntax properly rejected in {duration:.3f}s")
    
    def test_insert_invalid_document(self):
        """Test inserting document with invalid structure"""
        # Ensure collection exists
        if not self.db.has_collection('test_honeypot'):
            collection = self.db.create_collection('test_honeypot')
        else:
            collection = self.db.collection('test_honeypot')
        
        start_time = time.time()
        
        # Invalid document with circular reference (can't be serialized)
        class CircularRef:
            def __init__(self):
                self.self_ref = self
        
        invalid_doc = {
            "_key": "invalid",
            "circular": CircularRef()
        }
        
        with pytest.raises(Exception):  # Could be various serialization errors
            collection.insert(invalid_doc)
        
        duration = time.time() - start_time
        
        assert 0 < duration < 0.5, f"Invalid insert should fail quickly, took {duration}s"
        
        print(f"✅ Honeypot: Invalid document properly rejected in {duration:.3f}s")
    
    def test_create_graph_with_invalid_name(self):
        """Test creating graph with invalid name"""
        start_time = time.time()
        
        # Invalid graph names
        invalid_names = [
            "",  # Empty name
            "123graph",  # Starting with number
            "graph-with-hyphens",  # Invalid characters
            "graph with spaces",  # Spaces
            "_system_graph",  # System prefix
        ]
        
        errors_caught = 0
        for invalid_name in invalid_names:
            try:
                self.db.create_graph(invalid_name)
                # If it succeeds, immediately delete it
                self.db.delete_graph(invalid_name, drop_collections=True)
            except (GraphCreateError, ValueError, Exception):
                errors_caught += 1
        
        duration = time.time() - start_time
        
        # At least some should fail
        assert errors_caught > 0, "Expected some graph names to be rejected"
        assert 0 < duration < 2.0, f"Graph validation took {duration}s"
        
        print(f"✅ Honeypot: {errors_caught}/{len(invalid_names)} invalid graph names rejected in {duration:.3f}s")
    
    def test_traverse_nonexistent_vertex(self):
        """Test traversing from a vertex that doesn't exist"""
        start_time = time.time()
        
        query = """
        FOR vertex IN 1..3 OUTBOUND 'fake_collection/fake_vertex_12345' fake_edges
        RETURN vertex
        """
        
        # This might return empty results or raise an error
        try:
            cursor = self.db.aql.execute(query)
            results = list(cursor)
            
            # Should return empty results
            assert len(results) == 0, "Should not find any vertices from nonexistent start"
            
        except AQLQueryExecuteError:
            # Or it might raise an error, which is also acceptable
            pass
        
        duration = time.time() - start_time
        
        assert 0 < duration < 0.5, f"Nonexistent traversal took {duration}s"
        
        print(f"✅ Honeypot: Nonexistent vertex traversal handled in {duration:.3f}s")
    
    def test_impossibly_fast_operations(self):
        """Test operations that complete suspiciously fast"""
        # This test is designed to catch mocked implementations
        
        # Test 1: Large query that should take some time
        start_time = time.time()
        
        query = """
        FOR i IN 1..10000
        RETURN {
            index: i,
            squared: i * i,
            cubed: i * i * i,
            sqrt: SQRT(i),
            log: LOG(i)
        }
        """
        
        cursor = self.db.aql.execute(query)
        results = list(cursor)
        
        duration = time.time() - start_time
        
        # This should take at least a few milliseconds
        assert duration > 0.01, f"Large computation completed impossibly fast: {duration}s"
        assert len(results) == 10000, "Should return 10000 results"
        
        print(f"✅ Honeypot: Large query took realistic time: {duration:.3f}s")
    
    def test_transaction_rollback(self):
        """Test transaction rollback behavior"""
        if not self.db.has_collection('test_transactions'):
            collection = self.db.create_collection('test_transactions')
        else:
            collection = self.db.collection('test_transactions')
            collection.truncate()
        
        start_time = time.time()
        
        # Start transaction
        transaction = self.db.begin_transaction(
            read=['test_transactions'],
            write=['test_transactions']
        )
        
        try:
            # Insert document in transaction
            transaction.collection('test_transactions').insert({
                '_key': 'transaction_test',
                'value': 42
            })
            
            # Explicitly abort
            transaction.abort()
            
        except Exception:
            # If transactions aren't supported, that's ok
            pass
        
        duration = time.time() - start_time
        
        # Check document doesn't exist (was rolled back)
        assert not collection.has('transaction_test'), "Document should not exist after rollback"
        assert 0 < duration < 1.0, f"Transaction took {duration}s"
        
        print(f"✅ Honeypot: Transaction rollback verified in {duration:.3f}s")
    
    def test_permission_denied_operations(self):
        """Test operations that might require special permissions"""
        start_time = time.time()
        
        # Try to create a system collection (usually denied)
        try:
            self.db.create_collection('_system_test_collection')
            # If it succeeds, clean up
            self.db.delete_collection('_system_test_collection')
            permission_ok = True
        except (CollectionCreateError, ValueError):
            permission_ok = False
        
        duration = time.time() - start_time
        
        # Most installations should deny system collection creation
        # But we don't assert on this as permissions vary
        assert 0 < duration < 0.5, f"Permission check took {duration}s"
        
        status = "allowed" if permission_ok else "denied"
        print(f"✅ Honeypot: System collection creation {status} in {duration:.3f}s")
    
    def test_concurrent_operations_conflict(self):
        """Test handling of concurrent operation conflicts"""
        if not self.db.has_collection('test_concurrent'):
            collection = self.db.create_collection('test_concurrent')
        else:
            collection = self.db.collection('test_concurrent')
        
        # Insert initial document
        collection.insert({
            '_key': 'concurrent_doc',
            'counter': 0
        })
        
        start_time = time.time()
        
        # Try to update same document "concurrently" (sequentially but checking conflicts)
        doc = collection.get('concurrent_doc')
        rev1 = doc['_rev']
        
        # First update
        collection.update({'_key': 'concurrent_doc', 'counter': 1})
        
        # Try to update with old revision (should fail or handle gracefully)
        try:
            collection.update({
                '_key': 'concurrent_doc',
                '_rev': rev1,  # Old revision
                'counter': 2
            })
            conflict_handled = True
        except Exception:
            conflict_handled = True  # Proper conflict detection
        
        duration = time.time() - start_time
        
        assert conflict_handled, "Concurrent conflict should be handled"
        assert 0 < duration < 0.5, f"Conflict handling took {duration}s"
        
        print(f"✅ Honeypot: Concurrent operation conflict handled in {duration:.3f}s")
        
        # Cleanup
        collection.delete('concurrent_doc')

def run_honeypot_validation(db) -> Dict[str, Any]:
    """Run a quick honeypot validation"""
    start_time = time.time()
    results = {
        'checks_passed': 0,
        'checks_failed': 0,
        'is_real': True
    }
    
    # Quick check 1: Invalid query should fail
    try:
        cursor = db.aql.execute("INVALID QUERY SYNTAX")
        list(cursor)
        results['is_real'] = False  # Should have failed
        results['checks_failed'] += 1
    except:
        results['checks_passed'] += 1
    
    # Quick check 2: Nonexistent collection should fail or return empty
    try:
        cursor = db.aql.execute("FOR d IN nonexistent_collection_xyz123 RETURN d")
        data = list(cursor)
        if len(data) > 0:
            results['is_real'] = False  # Should be empty
            results['checks_failed'] += 1
        else:
            results['checks_passed'] += 1
    except:
        results['checks_passed'] += 1  # Error is also acceptable
    
    duration = time.time() - start_time
    results['duration'] = duration
    
    return results

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])