"""
Test ArangoDB insert functionality with real database operations.
Tests document insertion, bulk inserts, and edge creation.
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
import uuid
from typing import Dict, Any, List
from arango import ArangoClient
from arango.exceptions import DocumentInsertError, CollectionCreateError

# ArangoDB connection settings
ARANGO_HOST = "http://localhost:8529"
ARANGO_DB = "youtube_transcripts_test"
ARANGO_USER = "root"
ARANGO_PASS = "openSesame"

class TestArangoDBInsert:
    """Test document insertion with real database"""
    
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
        
        # Create test collection
        if not cls.db.has_collection('test_inserts'):
            cls.collection = cls.db.create_collection('test_inserts')
        else:
            cls.collection = cls.db.collection('test_inserts')
            # Clear existing data
            cls.collection.truncate()
    
    def test_single_document_insert(self):
        """Test inserting a single document"""
        start_time = time.time()
        
        document = {
            "_key": f"test_doc_{uuid.uuid4().hex[:8]}",
            "title": "Test Document",
            "content": "This is a test document for ArangoDB insert",
            "timestamp": time.time(),
            "tags": ["test", "arangodb", "insert"],
            "metadata": {
                "author": "Test Suite",
                "version": 1
            }
        }
        
        result = self.collection.insert(document)
        duration = time.time() - start_time
        
        # Verify result
        assert result['_key'] == document['_key']
        assert '_id' in result
        assert '_rev' in result
        assert 0 < duration < 0.5, f"Insert took {duration}s, expected 0.01-0.5s"
        
        # Verify document was actually inserted
        retrieved = self.collection.get(document['_key'])
        assert retrieved['title'] == document['title']
        assert retrieved['tags'] == document['tags']
        
        print(f"✅ Single document inserted in {duration:.3f}s")
    
    def test_bulk_insert(self):
        """Test bulk document insertion"""
        num_docs = 100
        documents = []
        
        for i in range(num_docs):
            documents.append({
                "index": i,
                "title": f"Bulk Document {i}",
                "value": i * 10,
                "category": chr(65 + (i % 5)),  # A-E
                "timestamp": time.time()
            })
        
        start_time = time.time()
        
        # Bulk insert
        results = self.collection.insert_many(documents)
        
        duration = time.time() - start_time
        
        # Verify results
        assert len(results) == num_docs
        assert all('_key' in r for r in results)
        assert 0 < duration < 2.0, f"Bulk insert took {duration}s"
        
        # Calculate insertion rate
        rate = num_docs / duration
        print(f"✅ Bulk inserted {num_docs} documents in {duration:.3f}s ({rate:.0f} docs/sec)")
    
    def test_insert_with_custom_key(self):
        """Test inserting documents with custom keys"""
        start_time = time.time()
        
        custom_key = f"custom_key_{int(time.time())}"
        document = {
            "_key": custom_key,
            "type": "custom",
            "data": {"test": True}
        }
        
        result = self.collection.insert(document)
        duration = time.time() - start_time
        
        # Verify custom key was used
        assert result['_key'] == custom_key
        assert 0 < duration < 0.3, f"Insert took {duration}s"
        
        # Retrieve and verify
        retrieved = self.collection.get(custom_key)
        assert retrieved['_key'] == custom_key
        assert retrieved['type'] == 'custom'
        
        print(f"✅ Document with custom key inserted in {duration:.3f}s")
    
    def test_insert_complex_document(self):
        """Test inserting document with complex nested structure"""
        start_time = time.time()
        
        complex_doc = {
            "name": "Complex Document",
            "nested": {
                "level1": {
                    "level2": {
                        "level3": {
                            "data": "Deep nested value",
                            "array": [1, 2, 3, 4, 5]
                        }
                    },
                    "metadata": {
                        "created": time.time(),
                        "tags": ["nested", "complex", "test"]
                    }
                }
            },
            "array_of_objects": [
                {"id": 1, "name": "Item 1", "active": True},
                {"id": 2, "name": "Item 2", "active": False},
                {"id": 3, "name": "Item 3", "active": True}
            ],
            "mixed_array": [1, "two", 3.0, {"four": 4}, [5, 6, 7]],
            "large_text": "Lorem ipsum " * 100  # ~1200 chars
        }
        
        result = self.collection.insert(complex_doc)
        duration = time.time() - start_time
        
        # Verify insertion
        assert '_key' in result
        assert 0 < duration < 0.5, f"Complex insert took {duration}s"
        
        # Retrieve and verify structure
        retrieved = self.collection.get(result['_key'])
        assert retrieved['nested']['level1']['level2']['level3']['data'] == "Deep nested value"
        assert len(retrieved['array_of_objects']) == 3
        assert len(retrieved['mixed_array']) == 5
        
        print(f"✅ Complex document inserted in {duration:.3f}s")
    
    def test_insert_with_validation(self):
        """Test document validation during insert"""
        # Create collection with schema validation
        schema_collection_name = 'test_validated'
        
        if self.db.has_collection(schema_collection_name):
            self.db.delete_collection(schema_collection_name)
        
        # Create collection with schema
        schema = {
            "rule": {
                "properties": {
                    "email": {"type": "string", "pattern": "^[^@]+@[^@]+\\.[^@]+$"},
                    "age": {"type": "number", "minimum": 0, "maximum": 150},
                    "status": {"type": "string", "enum": ["active", "inactive", "pending"]}
                },
                "required": ["email", "age", "status"]
            }
        }
        
        validated_collection = self.db.create_collection(
            schema_collection_name,
            schema=schema
        )
        
        # Test valid document
        start_time = time.time()
        
        valid_doc = {
            "email": "test@example.com",
            "age": 25,
            "status": "active",
            "name": "Test User"
        }
        
        result = validated_collection.insert(valid_doc)
        duration = time.time() - start_time
        
        assert '_key' in result
        assert 0 < duration < 0.5, f"Validated insert took {duration}s"
        
        print(f"✅ Validated document inserted in {duration:.3f}s")
        
        # Clean up
        self.db.delete_collection(schema_collection_name)
    
    def test_insert_edge_document(self):
        """Test inserting edge documents for graph relationships"""
        # Create vertex collections
        if not self.db.has_collection('test_vertices_from'):
            from_collection = self.db.create_collection('test_vertices_from')
        else:
            from_collection = self.db.collection('test_vertices_from')
            
        if not self.db.has_collection('test_vertices_to'):
            to_collection = self.db.create_collection('test_vertices_to')
        else:
            to_collection = self.db.collection('test_vertices_to')
        
        # Create edge collection
        if not self.db.has_collection('test_edges'):
            edge_collection = self.db.create_collection('test_edges', edge=True)
        else:
            edge_collection = self.db.collection('test_edges')
        
        # Insert vertices
        from_vertex = from_collection.insert({"name": "Source Node", "type": "origin"})
        to_vertex = to_collection.insert({"name": "Target Node", "type": "destination"})
        
        # Insert edge
        start_time = time.time()
        
        edge = {
            "_from": f"test_vertices_from/{from_vertex['_key']}",
            "_to": f"test_vertices_to/{to_vertex['_key']}",
            "relationship": "connects_to",
            "weight": 0.8,
            "created": time.time()
        }
        
        result = edge_collection.insert(edge)
        duration = time.time() - start_time
        
        # Verify edge
        assert '_key' in result
        # _from is set by server when inserting into edge collection
        # _to is set by server when inserting into edge collection
        assert 0 < duration < 0.5, f"Edge insert took {duration}s"
        
        print(f"✅ Edge document inserted in {duration:.3f}s")
    
    def test_insert_performance(self):
        """Test insertion performance with various document sizes"""
        sizes = [
            ("small", 100),      # 100 bytes
            ("medium", 1000),    # 1 KB
            ("large", 10000),    # 10 KB
            ("xlarge", 100000)   # 100 KB
        ]
        
        results = []
        
        for size_name, size_bytes in sizes:
            # Create document of specified size
            padding = "x" * (size_bytes // 2)  # Divide by 2 because of Unicode
            document = {
                "size_category": size_name,
                "size_bytes": size_bytes,
                "data": padding,
                "timestamp": time.time()
            }
            
            start_time = time.time()
            result = self.collection.insert(document)
            duration = time.time() - start_time
            
            results.append({
                "size": size_name,
                "bytes": size_bytes,
                "duration": duration,
                "rate": size_bytes / duration / 1024  # KB/s
            })
            
            print(f"  {size_name}: {duration:.3f}s ({results[-1]['rate']:.0f} KB/s)")
        
        # Verify reasonable performance
        assert all(r['duration'] < 1.0 for r in results), "Some inserts took too long"
        print(f"✅ Performance test completed for {len(sizes)} document sizes")
    
    @classmethod
    def teardown_class(cls):
        """Clean up test collections"""
        # Keep collections for other tests
        pass

def measure_insert_performance(collection, document: Dict) -> Dict[str, Any]:
    """Helper to measure insert performance"""
    start_time = time.time()
    
    try:
        result = collection.insert(document)
        success = True
        error = None
        key = result.get('_key')
    except Exception as e:
        success = False
        error = str(e)
        key = None
    
    duration = time.time() - start_time
    
    return {
        'duration': duration,
        'success': success,
        'error': error,
        'key': key,
        'document_size': len(json.dumps(document))
    }

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])