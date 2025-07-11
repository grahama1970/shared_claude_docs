
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: knowledge_graph_merger_interaction.py
Purpose: Orchestrates merging of multiple knowledge graphs while resolving conflicts and maintaining consistency

External Dependencies:
- networkx: https://networkx.org/documentation/stable/
- rdflib: https://rdflib.readthedocs.io/
- json-ld: https://pyld.digitalbazaar.com/

Example Usage:
>>> from knowledge_graph_merger_interaction import KnowledgeGraphMerger
>>> merger = KnowledgeGraphMerger()
>>> merged_graph = merger.merge_graphs([graph1, graph2], strategy='confidence-based')
>>> print(f"Merged {len(merged_graph.nodes)} nodes with {len(merged_graph.edges)} edges")
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional, Set
from enum import Enum
from dataclasses import dataclass, field
import hashlib
from collections import defaultdict

import networkx as nx
from rdflib import Graph as RDFGraph, URIRef, Literal, Namespace, RDF, RDFS


class ConflictStrategy(Enum):
    """Strategies for resolving conflicts when merging graphs"""
    LATEST_WINS = "latest-wins"
    CONFIDENCE_BASED = "confidence-based"
    CONSENSUS = "consensus"
    MANUAL = "manual"


@dataclass
class EntityProvenance:
    """Tracks the origin and confidence of entities"""
    source_graph: str
    timestamp: datetime
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MergeConflict:
    """Represents a conflict during graph merging"""
    entity_id: str
    attribute: str
    values: List[Tuple[Any, EntityProvenance]]
    resolution: Optional[Any] = None
    resolution_strategy: Optional[str] = None


class KnowledgeGraphMerger:
    """Orchestrates merging of multiple knowledge graphs with conflict resolution"""
    
    def __init__(self):
        self.conflicts: List[MergeConflict] = []
        self.provenance_map: Dict[str, List[EntityProvenance]] = defaultdict(list)
        self.entity_map: Dict[str, str] = {}  # Maps similar entities to canonical IDs
        
    def load_graph_from_format(self, data: Any, format_type: str, source_name: str) -> nx.DiGraph:
        """Load graph from various formats"""
        if format_type == "networkx":
            return data
        elif format_type == "rdf":
            return self._convert_rdf_to_networkx(data, source_name)
        elif format_type == "json-ld":
            return self._convert_jsonld_to_networkx(data, source_name)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _convert_rdf_to_networkx(self, rdf_graph: RDFGraph, source_name: str) -> nx.DiGraph:
        """Convert RDF graph to NetworkX format"""
        g = nx.DiGraph()
        
        for subj, pred, obj in rdf_graph:
            subj_str = str(subj)
            pred_str = str(pred)
            obj_str = str(obj)
            
            # Add nodes
            if subj_str not in g:
                g.add_node(subj_str, type='entity', source=source_name)
            
            if isinstance(obj, URIRef) and obj_str not in g:
                g.add_node(obj_str, type='entity', source=source_name)
            
            # Add edge
            g.add_edge(subj_str, obj_str, predicate=pred_str, source=source_name)
            
        return g
    
    def _convert_jsonld_to_networkx(self, jsonld_data: Dict, source_name: str) -> nx.DiGraph:
        """Convert JSON-LD to NetworkX format"""
        g = nx.DiGraph()
        
        def process_entity(entity: Dict, parent_id: Optional[str] = None):
            entity_id = entity.get('@id', f"_:blank_{len(g.nodes)}")
            entity_type = entity.get('@type', 'Entity')
            
            # Add node
            g.add_node(entity_id, type=entity_type, source=source_name, **entity)
            
            # Process relationships
            for key, value in entity.items():
                if key.startswith('@'):
                    continue
                    
                if isinstance(value, dict):
                    child_id = process_entity(value, entity_id)
                    g.add_edge(entity_id, child_id, predicate=key, source=source_name)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            child_id = process_entity(item, entity_id)
                            g.add_edge(entity_id, child_id, predicate=key, source=source_name)
                        else:
                            # Add literal node
                            literal_id = f"_:literal_{len(g.nodes)}"
                            g.add_node(literal_id, value=item, type='Literal', source=source_name)
                            g.add_edge(entity_id, literal_id, predicate=key, source=source_name)
            
            return entity_id
        
        if isinstance(jsonld_data, list):
            for item in jsonld_data:
                process_entity(item)
        else:
            process_entity(jsonld_data)
            
        return g
    
    def identify_similar_entities(self, graphs: List[nx.DiGraph], threshold: float = 0.8) -> Dict[str, Set[str]]:
        """Identify potentially similar entities across graphs"""
        entity_groups = defaultdict(set)
        all_entities = []
        
        # Collect all entities with their attributes
        for i, graph in enumerate(graphs):
            for node, attrs in graph.nodes(data=True):
                all_entities.append((f"graph_{i}:{node}", attrs, node))
        
        # Compare all pairs
        matched = set()
        
        for i in range(len(all_entities)):
            if i in matched:
                continue
                
            id1, attrs1, node1 = all_entities[i]
            current_group = [id1]
            
            for j in range(i + 1, len(all_entities)):
                if j in matched:
                    continue
                    
                id2, attrs2, node2 = all_entities[j]
                similarity = self._calculate_similarity(attrs1, attrs2)
                
                # Also check for exact email match as a strong indicator
                if attrs1.get('email') and attrs1.get('email') == attrs2.get('email'):
                    similarity = max(similarity, 0.9)  # Boost similarity for same email
                
                if similarity >= threshold:
                    current_group.append(id2)
                    matched.add(j)
            
            # Create group if we found similar entities
            if len(current_group) > 1:
                group_id = current_group[0]
                for entity_id in current_group:
                    entity_groups[group_id].add(entity_id)
                    self.entity_map[entity_id] = group_id
            
            matched.add(i)
        
        return dict(entity_groups)
    
    def _calculate_similarity(self, attrs1: Dict, attrs2: Dict) -> float:
        """Calculate similarity between two entities based on attributes"""
        if not attrs1 or not attrs2:
            return 0.0
            
        # Compare common attributes
        common_keys = set(attrs1.keys()) & set(attrs2.keys())
        if not common_keys:
            return 0.0
            
        matches = sum(1 for k in common_keys if attrs1.get(k) == attrs2.get(k))
        total_keys = len(set(attrs1.keys()) | set(attrs2.keys()))
        
        return matches / total_keys if total_keys > 0 else 0.0
    
    def resolve_conflicts(self, conflicts: List[MergeConflict], strategy: ConflictStrategy) -> List[MergeConflict]:
        """Resolve conflicts using specified strategy"""
        resolved_conflicts = []
        
        for conflict in conflicts:
            if strategy == ConflictStrategy.LATEST_WINS:
                # Sort by timestamp and take the latest
                sorted_values = sorted(conflict.values, key=lambda x: x[1].timestamp, reverse=True)
                conflict.resolution = sorted_values[0][0]
                conflict.resolution_strategy = strategy.value
                
            elif strategy == ConflictStrategy.CONFIDENCE_BASED:
                # Take value with highest confidence
                sorted_values = sorted(conflict.values, key=lambda x: x[1].confidence, reverse=True)
                conflict.resolution = sorted_values[0][0]
                conflict.resolution_strategy = strategy.value
                
            elif strategy == ConflictStrategy.CONSENSUS:
                # Take most common value
                value_counts = defaultdict(int)
                for value, _ in conflict.values:
                    value_counts[str(value)] += 1
                most_common = max(value_counts.items(), key=lambda x: x[1])
                for value, prov in conflict.values:
                    if str(value) == most_common[0]:
                        conflict.resolution = value
                        break
                conflict.resolution_strategy = strategy.value
                
            resolved_conflicts.append(conflict)
            
        return resolved_conflicts
    
    def merge_graphs(self, graphs: List[Tuple[nx.DiGraph, str, datetime]], 
                    strategy: ConflictStrategy = ConflictStrategy.CONFIDENCE_BASED) -> nx.DiGraph:
        """Merge multiple graphs with conflict resolution"""
        merged = nx.DiGraph()
        self.conflicts = []
        
        # First pass: identify similar entities
        graph_list = [g[0] for g in graphs]
        entity_groups = self.identify_similar_entities(graph_list)
        
        # Second pass: merge nodes and track conflicts
        node_attributes = defaultdict(lambda: defaultdict(list))
        
        for graph, source_name, timestamp in graphs:
            for node, attrs in graph.nodes(data=True):
                # Determine canonical node ID
                graph_node_id = f"{source_name}:{node}"
                canonical_id = self.entity_map.get(graph_node_id, node)
                
                # Track provenance
                prov = EntityProvenance(
                    source_graph=source_name,
                    timestamp=timestamp,
                    confidence=attrs.get('confidence', 1.0)
                )
                self.provenance_map[canonical_id].append(prov)
                
                # Collect attributes
                for attr, value in attrs.items():
                    if attr not in ['source', 'confidence']:
                        node_attributes[canonical_id][attr].append((value, prov))
        
        # Resolve conflicts and create merged nodes
        for node_id, attributes in node_attributes.items():
            node_attrs = {}
            
            for attr, values in attributes.items():
                if len(set(v[0] for v in values)) > 1:
                    # Conflict detected
                    conflict = MergeConflict(
                        entity_id=node_id,
                        attribute=attr,
                        values=values
                    )
                    self.conflicts.append(conflict)
                    
                    # Resolve conflict
                    resolved = self.resolve_conflicts([conflict], strategy)[0]
                    node_attrs[attr] = resolved.resolution
                else:
                    # No conflict
                    node_attrs[attr] = values[0][0]
            
            # Add node with resolved attributes
            merged.add_node(node_id, **node_attrs)
        
        # Third pass: merge edges
        edge_set = set()
        for graph, source_name, timestamp in graphs:
            for u, v, attrs in graph.edges(data=True):
                # Map to canonical IDs
                u_canonical = self.entity_map.get(f"{source_name}:{u}", u)
                v_canonical = self.entity_map.get(f"{source_name}:{v}", v)
                
                edge_key = (u_canonical, v_canonical, attrs.get('predicate', 'related'))
                if edge_key not in edge_set:
                    merged.add_edge(u_canonical, v_canonical, **attrs)
                    edge_set.add(edge_key)
        
        return merged
    
    def validate_merged_graph(self, graph: nx.DiGraph) -> Dict[str, Any]:
        """Validate the merged graph for consistency"""
        validation_results = {
            'is_valid': True,
            'node_count': graph.number_of_nodes(),
            'edge_count': graph.number_of_edges(),
            'connected_components': nx.number_weakly_connected_components(graph),
            'issues': []
        }
        
        # Check for isolated nodes
        isolated = list(nx.isolates(graph))
        if isolated:
            validation_results['issues'].append({
                'type': 'isolated_nodes',
                'count': len(isolated),
                'nodes': isolated[:10]  # First 10
            })
        
        # Check for self-loops
        self_loops = list(nx.selfloop_edges(graph))
        if self_loops:
            validation_results['issues'].append({
                'type': 'self_loops',
                'count': len(self_loops),
                'edges': self_loops[:10]
            })
        
        # Check provenance coverage
        nodes_without_provenance = [
            n for n in graph.nodes() 
            if n not in self.provenance_map or not self.provenance_map[n]
        ]
        if nodes_without_provenance:
            validation_results['issues'].append({
                'type': 'missing_provenance',
                'count': len(nodes_without_provenance),
                'nodes': nodes_without_provenance[:10]
            })
        
        validation_results['is_valid'] = len(validation_results['issues']) == 0
        
        return validation_results
    
    def generate_merge_report(self, merged_graph: nx.DiGraph) -> str:
        """Generate a detailed merge report"""
        report = []
        report.append("# Knowledge Graph Merge Report")
        report.append(f"Generated: {datetime.now().isoformat()}\n")
        
        # Summary statistics
        report.append("## Summary Statistics")
        report.append(f"- Total Nodes: {merged_graph.number_of_nodes()}")
        report.append(f"- Total Edges: {merged_graph.number_of_edges()}")
        report.append(f"- Conflicts Resolved: {len(self.conflicts)}")
        report.append(f"- Entity Groups Identified: {len(set(self.entity_map.values()))}\n")
        
        # Conflict details
        if self.conflicts:
            report.append("## Conflict Resolution Details")
            report.append("| Entity | Attribute | Values | Resolution | Strategy |")
            report.append("|--------|-----------|---------|------------|----------|")
            
            for conflict in self.conflicts[:20]:  # First 20 conflicts
                values_str = f"{len(conflict.values)} values"
                report.append(
                    f"| {conflict.entity_id[:30]} | {conflict.attribute} | "
                    f"{values_str} | {str(conflict.resolution)[:30]} | "
                    f"{conflict.resolution_strategy} |"
                )
        
        # Provenance summary
        report.append("\n## Provenance Summary")
        source_counts = defaultdict(int)
        for entity, provs in self.provenance_map.items():
            for prov in provs:
                source_counts[prov.source_graph] += 1
        
        for source, count in sorted(source_counts.items()):
            report.append(f"- {source}: {count} entities")
        
        return "\n".join(report)
    
    def find_similar_entities(self, graphs: List[nx.DiGraph], threshold: float = 0.8) -> List[Tuple[str, str]]:
        """Public wrapper to find similar entities across graphs"""
        entity_groups = self.identify_similar_entities(graphs, threshold)
        
        # Convert groups to pairs
        pairs = []
        for group_id, entities in entity_groups.items():
            entity_list = list(entities)
            for i in range(len(entity_list)):
                for j in range(i + 1, len(entity_list)):
                    # Extract node ID from graph_X:node_id format
                    id1 = entity_list[i].split(":", 1)[1] if ":" in entity_list[i] else entity_list[i]
                    id2 = entity_list[j].split(":", 1)[1] if ":" in entity_list[j] else entity_list[j]
                    pairs.append((id1, id2))
        
        return pairs
    
    def get_entity_provenance(self, entity_id: str) -> List[EntityProvenance]:
        """Get provenance information for an entity"""
        return self.provenance_map.get(entity_id, [])


# Test functions for validation
def test_basic_merge():
    """Test basic graph merging functionality"""
    print("\n🧪 Testing Basic Graph Merge...")
    start_time = time.time()
    
    # Create test graphs
    g1 = nx.DiGraph()
    g1.add_node("person_1", name="John Doe", age=30, occupation="Engineer")
    g1.add_node("company_1", name="TechCorp", industry="Technology")
    g1.add_edge("person_1", "company_1", predicate="works_for")
    
    g2 = nx.DiGraph()
    g2.add_node("person_1", name="John Doe", age=31, city="New York")  # Age conflict
    g2.add_node("company_1", name="TechCorp", employees=1000)
    g2.add_edge("person_1", "company_1", predicate="works_for")
    
    # Merge graphs
    merger = KnowledgeGraphMerger()
    graphs = [
        (g1, "source1", datetime.now()),
        (g2, "source2", datetime.now())
    ]
    
    merged = merger.merge_graphs(graphs, ConflictStrategy.LATEST_WINS)
    
    # Validate results
    assert merged.number_of_nodes() == 2, f"Expected 2 nodes, got {merged.number_of_nodes()}"
    assert merged.nodes['person_1']['age'] == 31, "Latest wins strategy should select age=31"
    assert len(merger.conflicts) == 1, f"Expected 1 conflict, got {len(merger.conflicts)}"
    
    duration = time.time() - start_time
    print(f"✅ Basic merge test passed in {duration:.2f}s")
    return True, duration


def test_rdf_conversion():
    """Test RDF to NetworkX conversion"""
    print("\n🧪 Testing RDF Conversion...")
    start_time = time.time()
    
    # Create RDF graph
    rdf = RDFGraph()
    EX = Namespace("http://example.org/")
    
    rdf.add((EX.Alice, RDF.type, EX.Person))
    rdf.add((EX.Alice, EX.name, Literal("Alice")))
    rdf.add((EX.Alice, EX.knows, EX.Bob))
    rdf.add((EX.Bob, RDF.type, EX.Person))
    rdf.add((EX.Bob, EX.name, Literal("Bob")))
    
    # Convert and validate
    merger = KnowledgeGraphMerger()
    nx_graph = merger.load_graph_from_format(rdf, "rdf", "test_source")
    
    assert nx_graph.number_of_nodes() >= 4, f"Expected at least 4 nodes, got {nx_graph.number_of_nodes()}"
    assert nx_graph.has_edge(str(EX.Alice), str(EX.Bob)), "Missing edge Alice->Bob"
    
    duration = time.time() - start_time
    print(f"✅ RDF conversion test passed in {duration:.2f}s")
    return True, duration


def test_entity_resolution():
    """Test entity resolution across graphs"""
    print("\n🧪 Testing Entity Resolution...")
    start_time = time.time()
    
    # Create graphs with similar entities
    g1 = nx.DiGraph()
    g1.add_node("john_doe", name="John Doe", email="john@example.com")
    g1.add_node("acme_corp", name="ACME Corporation", type="company")
    
    g2 = nx.DiGraph()
    g2.add_node("j_doe", name="John Doe", email="john@example.com", phone="555-1234")
    g2.add_node("acme", name="ACME Corporation", type="company", founded=1990)
    
    # Test entity resolution
    merger = KnowledgeGraphMerger()
    entity_groups = merger.identify_similar_entities([g1, g2], threshold=0.6)
    
    assert len(entity_groups) >= 2, f"Expected at least 2 entity groups, got {len(entity_groups)}"
    
    # Verify John Doe entities are grouped
    john_group = None
    for group_id, entities in entity_groups.items():
        if any("john" in e.lower() for e in entities):
            john_group = entities
            break
    
    assert john_group is not None, "John Doe entities not grouped"
    assert len(john_group) == 2, f"Expected 2 John Doe entities, got {len(john_group)}"
    
    duration = time.time() - start_time
    print(f"✅ Entity resolution test passed in {duration:.2f}s")
    return True, duration


def test_conflict_strategies():
    """Test different conflict resolution strategies"""
    print("\n🧪 Testing Conflict Resolution Strategies...")
    start_time = time.time()
    
    # Create conflicting data
    base_time = datetime.now()
    
    g1 = nx.DiGraph()
    g1.add_node("product_1", name="Laptop", price=1000, confidence=0.8)
    
    g2 = nx.DiGraph()
    g2.add_node("product_1", name="Laptop", price=1200, confidence=0.9)
    
    g3 = nx.DiGraph()
    g3.add_node("product_1", name="Laptop", price=1200, confidence=0.7)
    
    graphs = [
        (g1, "store1", base_time),
        (g2, "store2", base_time),
        (g3, "store3", base_time)
    ]
    
    # Test confidence-based strategy
    merger = KnowledgeGraphMerger()
    merged = merger.merge_graphs(graphs, ConflictStrategy.CONFIDENCE_BASED)
    assert merged.nodes['product_1']['price'] == 1200, "Confidence-based should select price from g2"
    
    # Test consensus strategy
    merger2 = KnowledgeGraphMerger()
    merged2 = merger2.merge_graphs(graphs, ConflictStrategy.CONSENSUS)
    assert merged2.nodes['product_1']['price'] == 1200, "Consensus should select most common price"
    
    duration = time.time() - start_time
    print(f"✅ Conflict strategies test passed in {duration:.2f}s")
    return True, duration


def test_graph_validation():
    """Test merged graph validation"""
    print("\n🧪 Testing Graph Validation...")
    start_time = time.time()
    
    # Create graph with issues
    g = nx.DiGraph()
    g.add_node("node1", type="entity")
    g.add_node("node2", type="entity")
    g.add_node("isolated_node", type="entity")  # No edges
    g.add_edge("node1", "node2", predicate="related")
    g.add_edge("node1", "node1", predicate="self_ref")  # Self-loop
    
    merger = KnowledgeGraphMerger()
    validation = merger.validate_merged_graph(g)
    
    assert not validation['is_valid'], "Graph with issues should not be valid"
    assert len(validation['issues']) >= 2, f"Expected at least 2 issues, got {len(validation['issues'])}"
    
    issue_types = [issue['type'] for issue in validation['issues']]
    assert 'isolated_nodes' in issue_types, "Should detect isolated nodes"
    assert 'self_loops' in issue_types, "Should detect self-loops"
    
    duration = time.time() - start_time
    print(f"✅ Graph validation test passed in {duration:.2f}s")
    return True, duration


def test_large_scale_merge():
    """Test merging large graphs"""
    print("\n🧪 Testing Large Scale Merge...")
    start_time = time.time()
    
    # Create larger graphs with different edge patterns
    graphs = []
    for i in range(3):
        g = nx.DiGraph()
        # Add 1000 nodes
        for j in range(1000):
            g.add_node(f"entity_{j}", 
                      type="entity",
                      value=f"value_{i}_{j}",
                      source_specific=f"source_{i}")
        
        # Add edges with source-specific patterns to avoid complete overlap
        for j in range(800):
            u = f"entity_{j}"
            v = f"entity_{(j + 1) % 1000}"
            g.add_edge(u, v, predicate=f"rel_{j % 10}")
        
        # Add some unique edges per source
        for j in range(200):
            u = f"entity_{(i * 200 + j) % 1000}"
            v = f"entity_{(i * 200 + j + 100) % 1000}"
            g.add_edge(u, v, predicate=f"source_{i}_rel")
        
        graphs.append((g, f"source_{i}", datetime.now()))
    
    # Merge graphs
    merger = KnowledgeGraphMerger()
    merged = merger.merge_graphs(graphs, ConflictStrategy.LATEST_WINS)
    
    assert merged.number_of_nodes() == 1000, f"Expected 1000 nodes, got {merged.number_of_nodes()}"
    assert merged.number_of_edges() >= 1000, f"Expected at least 1000 edges, got {merged.number_of_edges()}"
    
    # Generate report
    report = merger.generate_merge_report(merged)
    assert "Knowledge Graph Merge Report" in report
    assert "1000" in report  # Should mention node count
    
    duration = time.time() - start_time
    print(f"✅ Large scale merge test passed in {duration:.2f}s")
    return True, duration


if __name__ == "__main__":
    print("=" * 60)
    print("Knowledge Graph Merger Validation")
    print("=" * 60)
    
    tests = [
        ("Basic Merge", test_basic_merge),
        ("RDF Conversion", test_rdf_conversion),
        ("Entity Resolution", test_entity_resolution),
        ("Conflict Strategies", test_conflict_strategies),
        ("Graph Validation", test_graph_validation),
        ("Large Scale Merge", test_large_scale_merge)
    ]
    
    results = []
    total_tests = len(tests)
    passed_tests = 0
    
    for test_name, test_func in tests:
        try:
            success, duration = test_func()
            if success:
                passed_tests += 1
                results.append((test_name, "✅ PASS", duration, None))
            else:
                results.append((test_name, "❌ FAIL", duration, "Test returned False"))
        except Exception as e:
            results.append((test_name, "❌ FAIL", 0, str(e)))
            print(f"❌ {test_name} failed with error: {e}")
    
    # Summary report
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print("\nDetailed Results:")
    print("-" * 60)
    
    for test_name, status, duration, error in results:
        print(f"{test_name:<25} {status:<10} {duration:>6.2f}s", end="")
        if error:
            print(f"  Error: {error[:50]}")
        else:
            print()
    
    # Generate markdown report
    report_content = f"""# Knowledge Graph Merger Test Report
Generated: {datetime.now().isoformat()}

## Summary
- Total Tests: {total_tests}
- Passed: {passed_tests}
- Failed: {total_tests - passed_tests}

## Test Results

| Test Name | Status | Duration | Error |
|-----------|--------|----------|-------|
"""
    
    for test_name, status, duration, error in results:
        error_msg = error[:50] + "..." if error and len(error) > 50 else (error or "")
        report_content += f"| {test_name} | {status} | {duration:.2f}s | {error_msg} |\n"
    
    # Save report
    report_path = f"/tmp/kg_merger_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"\n📄 Report saved to: {report_path}")
    
    # Exit with appropriate code
    exit_code = 0 if passed_tests == total_tests else 1
    print(f"\n{'✅ All tests passed!' if exit_code == 0 else '❌ Some tests failed!'}")
    exit(exit_code)