#!/usr/bin/env python3
"""
Module: test_23_knowledge_graph_builder.py
Description: Test building knowledge graphs from multiple sources
Level: 2
Modules: GitGet, ArXiv MCP Server, ArangoDB, World Model
Expected Bugs: Graph consistency issues, relationship inference errors, scalability
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time

class KnowledgeGraphBuilderTest(BaseInteractionTest):
    """Level 2: Test knowledge graph building from multiple sources"""
    
    def __init__(self):
        super().__init__(
            test_name="Knowledge Graph Builder",
            level=2,
            modules=["GitGet", "ArXiv MCP Server", "ArangoDB", "World Model"]
        )
    
    def test_multi_source_graph_building(self):
        """Test building comprehensive knowledge graph"""
        self.print_header()
        
        # Import modules
        try:
            from gitget import analyze_repository, extract_dependencies
            from arxiv_mcp_server import ArXivServer
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            from world_model import WorldModel
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot build knowledge graph"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            arxiv = ArXivServer()
            arango = ArangoDocumentHandler()
            world_model = WorldModel()
            self.record_test("components_init", True, {})
        except Exception as e:
            self.add_bug(
                "Component initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("components_init", False, {"error": str(e)})
            return
        
        graph_start = time.time()
        graph_metrics = {
            "nodes_created": 0,
            "edges_created": 0,
            "sources_integrated": 0,
            "inference_relationships": 0
        }
        
        try:
            # Create graph collections
            print("\n🌐 Setting up knowledge graph structure...")
            
            collections = ["kg_nodes", "kg_edges", "kg_metadata"]
            for collection in collections:
                arango.handle({
                    "operation": "create_collection",
                    "collection": collection,
                    "type": "edge" if "edges" in collection else "document"
                })
            
            # Step 1: Add research papers as nodes
            print("\n📚 Adding research papers to graph...")
            
            papers = arxiv.search("knowledge graph construction", max_results=3)
            
            for paper in papers:
                node = {
                    "_key": f"paper_{paper['id'].replace('/', '_')}",
                    "type": "research_paper",
                    "title": paper["title"],
                    "authors": paper.get("authors", []),
                    "abstract": paper["abstract"],
                    "published": paper.get("published_date"),
                    "categories": paper.get("categories", [])
                }
                
                result = arango.handle({
                    "operation": "create",
                    "collection": "kg_nodes",
                    "data": node
                })
                
                if result and "error" not in result:
                    graph_metrics["nodes_created"] += 1
                    
                    # Update world model
                    world_model.update_state({
                        "module": "knowledge_graph",
                        "action": "add_node",
                        "node_type": "research_paper",
                        "node_id": node["_key"]
                    })
            
            # Step 2: Add code repositories as nodes
            print("\n💻 Adding code repositories to graph...")
            
            repo_urls = [
                "https://github.com/networkx/networkx",
                "https://github.com/neo4j/neo4j"
            ]
            
            for url in repo_urls:
                try:
                    repo_info = analyze_repository(url)
                    
                    if repo_info:
                        node = {
                            "_key": f"repo_{url.split('/')[-1]}",
                            "type": "code_repository",
                            "url": url,
                            "name": repo_info.get("name"),
                            "languages": repo_info.get("languages", []),
                            "stars": repo_info.get("stars", 0),
                            "topics": repo_info.get("topics", [])
                        }
                        
                        result = arango.handle({
                            "operation": "create",
                            "collection": "kg_nodes",
                            "data": node
                        })
                        
                        if result and "error" not in result:
                            graph_metrics["nodes_created"] += 1
                            
                except Exception as e:
                    print(f"  ❌ Failed to add repo {url}: {str(e)[:50]}")
            
            graph_metrics["sources_integrated"] = 2  # Papers + Repos
            
            # Step 3: Create relationships between nodes
            print("\n🔗 Creating relationships...")
            
            # Get all nodes to find relationships
            nodes_result = arango.handle({
                "operation": "search",
                "collection": "kg_nodes",
                "query": {},
                "limit": 100
            })
            
            if nodes_result and "documents" in nodes_result:
                nodes = nodes_result["documents"]
                
                # Find relationships
                for i, node1 in enumerate(nodes):
                    for node2 in nodes[i+1:]:
                        relationship = self.infer_relationship(node1, node2)
                        
                        if relationship:
                            edge = {
                                "_from": f"kg_nodes/{node1['_key']}",
                                "_to": f"kg_nodes/{node2['_key']}",
                                "type": relationship["type"],
                                "strength": relationship["strength"],
                                "reason": relationship["reason"],
                                "created_at": time.time()
                            }
                            
                            edge_result = arango.handle({
                                "operation": "create",
                                "collection": "kg_edges",
                                "data": edge
                            })
                            
                            if edge_result and "error" not in edge_result:
                                graph_metrics["edges_created"] += 1
                                
                                if relationship.get("inferred", False):
                                    graph_metrics["inference_relationships"] += 1
            
            # Step 4: Analyze graph structure
            print("\n📊 Analyzing graph structure...")
            
            # Get graph statistics
            stats = {
                "total_nodes": graph_metrics["nodes_created"],
                "total_edges": graph_metrics["edges_created"],
                "node_types": {},
                "avg_connections": 0
            }
            
            # Count node types
            if nodes_result and "documents" in nodes_result:
                for node in nodes_result["documents"]:
                    node_type = node.get("type", "unknown")
                    stats["node_types"][node_type] = stats["node_types"].get(node_type, 0) + 1
                
                # Calculate average connections
                if stats["total_nodes"] > 0:
                    stats["avg_connections"] = (stats["total_edges"] * 2) / stats["total_nodes"]
            
            print(f"\n✅ Knowledge graph built:")
            print(f"   Nodes: {stats['total_nodes']}")
            print(f"   Edges: {stats['total_edges']}")
            print(f"   Node types: {stats['node_types']}")
            print(f"   Avg connections: {stats['avg_connections']:.2f}")
            
            graph_duration = time.time() - graph_start
            
            self.record_test("knowledge_graph_building", True, {
                **graph_metrics,
                "graph_stats": stats,
                "build_duration": graph_duration
            })
            
            # Quality checks
            if stats["avg_connections"] < 1:
                self.add_bug(
                    "Sparse knowledge graph",
                    "HIGH",
                    avg_connections=stats["avg_connections"],
                    nodes=stats["total_nodes"],
                    edges=stats["total_edges"]
                )
            
            if graph_metrics["inference_relationships"] == 0:
                self.add_bug(
                    "No inferred relationships",
                    "MEDIUM",
                    total_edges=graph_metrics["edges_created"]
                )
            
            if graph_duration > 60:
                self.add_bug(
                    "Slow graph construction",
                    "MEDIUM",
                    duration_seconds=graph_duration,
                    nodes=stats["total_nodes"]
                )
                
        except Exception as e:
            self.add_bug(
                "Knowledge graph building failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("knowledge_graph_building", False, {"error": str(e)})
    
    def infer_relationship(self, node1, node2):
        """Infer relationship between two nodes"""
        relationship = None
        
        # Same type relationships
        if node1.get("type") == node2.get("type"):
            if node1["type"] == "research_paper":
                # Check for common authors
                authors1 = set(node1.get("authors", []))
                authors2 = set(node2.get("authors", []))
                if authors1 & authors2:
                    relationship = {
                        "type": "shares_authors",
                        "strength": len(authors1 & authors2) / max(len(authors1), len(authors2)),
                        "reason": "Common authors found",
                        "inferred": True
                    }
                # Check for similar topics
                elif any(cat in node2.get("categories", []) for cat in node1.get("categories", [])):
                    relationship = {
                        "type": "related_topic",
                        "strength": 0.5,
                        "reason": "Similar categories",
                        "inferred": True
                    }
            
            elif node1["type"] == "code_repository":
                # Check for common languages
                langs1 = set(node1.get("languages", []))
                langs2 = set(node2.get("languages", []))
                if langs1 & langs2:
                    relationship = {
                        "type": "similar_technology",
                        "strength": len(langs1 & langs2) / max(len(langs1), len(langs2)),
                        "reason": "Common programming languages",
                        "inferred": True
                    }
        
        # Cross-type relationships
        else:
            if (node1["type"] == "research_paper" and node2["type"] == "code_repository") or \
               (node2["type"] == "research_paper" and node1["type"] == "code_repository"):
                # Check if paper mentions repo
                paper = node1 if node1["type"] == "research_paper" else node2
                repo = node2 if node2["type"] == "code_repository" else node1
                
                if repo.get("name", "").lower() in paper.get("abstract", "").lower():
                    relationship = {
                        "type": "implements",
                        "strength": 0.8,
                        "reason": "Repository mentioned in paper",
                        "inferred": True
                    }
        
        return relationship
    
    def run_tests(self):
        """Run all tests"""
        self.test_multi_source_graph_building()
        return self.generate_report()


def main():
    """Run the test"""
    tester = KnowledgeGraphBuilderTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)