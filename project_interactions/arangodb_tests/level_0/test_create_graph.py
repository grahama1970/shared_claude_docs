"""
Test ArangoDB graph creation functionality with real database operations.
Tests graph creation, edge definitions, and graph properties.
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
from typing import Dict, Any, List, Set
from arango import ArangoClient
from arango.exceptions import GraphCreateError, CollectionCreateError

# ArangoDB connection settings
ARANGO_HOST = "http://localhost:8529"
ARANGO_DB = "youtube_transcripts_test"
ARANGO_USER = "root"
ARANGO_PASS = "openSesame"

class TestArangoDBCreateGraph:
    """Test graph creation with real database"""
    
    @classmethod
    def setup_class(cls):
        """Set up test database"""
        cls.client = ArangoClient(hosts=ARANGO_HOST)
        
        # Connect to system database first
        sys_db = cls.client.db('_system', username=ARANGO_USER, password=ARANGO_PASS)
        
        # Create test database if it doesn't exist
        if not sys_db.has_database(ARANGO_DB):
            sys_db.create_database(ARANGO_DB)
        
        # Connect to test database
        cls.db = cls.client.db(ARANGO_DB, username=ARANGO_USER, password=ARANGO_PASS)
        
        # Track created graphs for cleanup
        cls.created_graphs = []
    
    def test_simple_graph_creation(self):
        """Test creating a simple graph"""
        graph_name = f"test_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        # Create graph with one edge definition
        graph = self.db.create_graph(graph_name)
        
        # Add edge definition
        graph.create_edge_definition(
            edge_collection='knows',
            from_vertex_collections=['persons'],
            to_vertex_collections=['persons']
        )
        
        duration = time.time() - start_time
        
        # Verify graph creation
        assert self.db.has_graph(graph_name)
        assert 0 < duration < 1.0, f"Graph creation took {duration}s"
        
        # Verify graph properties
        graph_info = graph.properties()
        assert graph_info['name'] == graph_name
        assert len(graph_info['edge_definitions']) == 1
        
        print(f"✅ Simple graph created in {duration:.3f}s")
    
    def test_complex_graph_creation(self):
        """Test creating a complex graph with multiple edge definitions"""
        graph_name = f"complex_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        # Create graph
        graph = self.db.create_graph(graph_name)
        
        # Add multiple edge definitions
        edge_definitions = [
            {
                'edge_collection': 'friendships',
                'from_collections': ['users'],
                'to_collections': ['users']
            },
            {
                'edge_collection': 'memberships',
                'from_collections': ['users'],
                'to_collections': ['groups']
            },
            {
                'edge_collection': 'ownerships',
                'from_collections': ['users'],
                'to_collections': ['items']
            },
            {
                'edge_collection': 'locations',
                'from_collections': ['users', 'items'],
                'to_collections': ['places']
            }
        ]
        
        for edge_def in edge_definitions:
            graph.create_edge_definition(
                edge_collection=edge_def['edge_collection'],
                from_vertex_collections=edge_def['from_collections'],
                to_vertex_collections=edge_def['to_collections']
            )
        
        duration = time.time() - start_time
        
        # Verify graph
        assert self.db.has_graph(graph_name)
        assert 0 < duration < 2.0, f"Complex graph creation took {duration}s"
        
        # Verify edge definitions
        graph_info = graph.properties()
        assert len(graph_info['edge_definitions']) == 4
        
        print(f"✅ Complex graph with 4 edge types created in {duration:.3f}s")
    
    def test_knowledge_graph_pattern(self):
        """Test creating a knowledge graph pattern"""
        graph_name = f"knowledge_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        # Create knowledge graph
        graph = self.db.create_graph(graph_name)
        
        # Knowledge graph edge definitions
        kg_edges = [
            ('has_property', ['entities'], ['properties']),
            ('relates_to', ['entities'], ['entities']),
            ('belongs_to', ['entities'], ['categories']),
            ('derived_from', ['facts'], ['sources']),
            ('contains', ['documents'], ['entities']),
            ('references', ['documents'], ['documents'])
        ]
        
        for edge_name, from_colls, to_colls in kg_edges:
            graph.create_edge_definition(
                edge_collection=edge_name,
                from_vertex_collections=from_colls,
                to_vertex_collections=to_colls
            )
        
        duration = time.time() - start_time
        
        # Verify knowledge graph
        assert self.db.has_graph(graph_name)
        graph_info = graph.properties()
        assert len(graph_info['edge_definitions']) == 6
        
        # Get all vertex collections
        vertex_collections = set()
        for edge_def in graph_info['edge_definitions']:
            vertex_collections.update(edge_def['from_vertex_collections'])
            vertex_collections.update(edge_def['to_vertex_collections'])
        
        expected_vertices = {'entities', 'properties', 'categories', 'facts', 'sources', 'documents'}
        assert vertex_collections == expected_vertices
        
        print(f"✅ Knowledge graph pattern created in {duration:.3f}s")
    
    def test_social_network_graph(self):
        """Test creating a social network graph"""
        graph_name = f"social_network_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        # Create social network graph
        graph = self.db.create_graph(graph_name)
        
        # Social network edges
        social_edges = [
            ('follows', ['users'], ['users']),
            ('likes', ['users'], ['posts', 'comments']),
            ('posted', ['users'], ['posts']),
            ('commented', ['users'], ['comments']),
            ('tagged_in', ['posts'], ['users']),
            ('reply_to', ['comments'], ['posts', 'comments'])
        ]
        
        for edge_name, from_colls, to_colls in social_edges:
            graph.create_edge_definition(
                edge_collection=edge_name,
                from_vertex_collections=from_colls,
                to_vertex_collections=to_colls
            )
        
        duration = time.time() - start_time
        
        # Verify graph
        assert self.db.has_graph(graph_name)
        graph_info = graph.properties()
        assert len(graph_info['edge_definitions']) == 6
        
        print(f"✅ Social network graph created in {duration:.3f}s")
    
    def test_graph_with_orphan_collections(self):
        """Test creating a graph with orphan vertex collections"""
        graph_name = f"graph_with_orphans_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        # Create graph with orphan collections
        graph = self.db.create_graph(
            graph_name,
            orphan_collections=['orphan_vertices', 'standalone_data']
        )
        
        # Add edge definition
        graph.create_edge_definition(
            edge_collection='connections',
            from_vertex_collections=['main_vertices'],
            to_vertex_collections=['main_vertices']
        )
        
        duration = time.time() - start_time
        
        # Verify graph
        graph_info = graph.properties()
        assert 'orphan_vertices' in graph_info['orphan_collections']
        assert 'standalone_data' in graph_info['orphan_collections']
        assert 0 < duration < 1.0, f"Graph creation took {duration}s"
        
        print(f"✅ Graph with orphan collections created in {duration:.3f}s")
    
    def test_satellite_graph_creation(self):
        """Test creating a satellite graph (if Enterprise Edition)"""
        graph_name = f"satellite_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        start_time = time.time()
        
        try:
            # Try to create satellite graph (requires Enterprise)
            graph = self.db.create_graph(
                graph_name,
                satellite=True
            )
            
            # Add edge definition
            graph.create_edge_definition(
                edge_collection='sat_edges',
                from_vertex_collections=['sat_vertices'],
                to_vertex_collections=['sat_vertices']
            )
            
            duration = time.time() - start_time
            print(f"✅ Satellite graph created in {duration:.3f}s (Enterprise Edition)")
            
        except Exception as e:
            duration = time.time() - start_time
            # Satellite graphs require Enterprise Edition
            if "satellite" in str(e).lower() or "enterprise" in str(e).lower():
                print(f"ℹ️  Satellite graph not available (Community Edition) - {duration:.3f}s")
            else:
                raise
    
    def test_graph_modification(self):
        """Test modifying an existing graph"""
        graph_name = f"modifiable_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        # Create initial graph
        graph = self.db.create_graph(graph_name)
        graph.create_edge_definition(
            edge_collection='initial_edges',
            from_vertex_collections=['vertices_a'],
            to_vertex_collections=['vertices_b']
        )
        
        start_time = time.time()
        
        # Add new edge definition
        graph.create_edge_definition(
            edge_collection='new_edges',
            from_vertex_collections=['vertices_b'],
            to_vertex_collections=['vertices_c']
        )
        
        # Add orphan collection
        graph.create_vertex_collection('orphan_collection')
        
        duration = time.time() - start_time
        
        # Verify modifications
        graph_info = graph.properties()
        assert len(graph_info['edge_definitions']) == 2
        assert 'orphan_collection' in graph_info['orphan_collections']
        assert 0 < duration < 1.0, f"Graph modification took {duration}s"
        
        print(f"✅ Graph modified successfully in {duration:.3f}s")
    
    def test_graph_performance(self):
        """Test performance of creating graphs with many edge definitions"""
        graph_name = f"performance_graph_{int(time.time())}"
        self.created_graphs.append(graph_name)
        
        num_edge_types = 10
        
        start_time = time.time()
        
        # Create graph
        graph = self.db.create_graph(graph_name)
        
        # Add many edge definitions
        for i in range(num_edge_types):
            graph.create_edge_definition(
                edge_collection=f'edge_type_{i}',
                from_vertex_collections=[f'vertex_type_{i}'],
                to_vertex_collections=[f'vertex_type_{(i+1) % num_edge_types}']
            )
        
        duration = time.time() - start_time
        
        # Verify graph
        graph_info = graph.properties()
        assert len(graph_info['edge_definitions']) == num_edge_types
        assert 0 < duration < 5.0, f"Large graph creation took {duration}s"
        
        rate = num_edge_types / duration
        print(f"✅ Created graph with {num_edge_types} edge types in {duration:.3f}s ({rate:.1f} edges/sec)")
    
    @classmethod
    def teardown_class(cls):
        """Clean up created graphs"""
        for graph_name in cls.created_graphs:
            try:
                cls.db.delete_graph(graph_name, drop_collections=True)
            except:
                pass

def create_graph_with_data(db, graph_name: str, num_vertices: int = 10, num_edges: int = 20) -> Dict[str, Any]:
    """Helper to create a graph with sample data"""
    start_time = time.time()
    
    # Create graph
    graph = db.create_graph(graph_name)
    
    # Create edge definition
    graph.create_edge_definition(
        edge_collection='test_edges',
        from_vertex_collections=['test_vertices'],
        to_vertex_collections=['test_vertices']
    )
    
    # Get collections
    vertex_collection = db.collection('test_vertices')
    edge_collection = db.collection('test_edges')
    
    # Insert vertices
    vertices = []
    for i in range(num_vertices):
        vertex = vertex_collection.insert({
            '_key': f'v{i}',
            'name': f'Vertex {i}',
            'value': i * 10
        })
        vertices.append(vertex)
    
    # Insert random edges
    import random
    edges = []
    for i in range(num_edges):
        from_idx = random.randint(0, num_vertices - 1)
        to_idx = random.randint(0, num_vertices - 1)
        
        edge = edge_collection.insert({
            '_from': f'test_vertices/v{from_idx}',
            '_to': f'test_vertices/v{to_idx}',
            'weight': random.random()
        })
        edges.append(edge)
    
    duration = time.time() - start_time
    
    return {
        'graph_name': graph_name,
        'duration': duration,
        'num_vertices': num_vertices,
        'num_edges': num_edges,
        'vertices_per_sec': num_vertices / duration,
        'edges_per_sec': num_edges / duration
    }

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])