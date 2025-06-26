#!/usr/bin/env python3
"""
Module: test_15_gitget_to_arangodb_pipeline.py
Description: Test GitGet → ArangoDB code analysis storage pipeline
Level: 1
Modules: GitGet, ArangoDB, Test Reporter
Expected Bugs: Large repo handling, code parsing errors, storage limits
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import hashlib

class GitGetToArangoDBPipelineTest(BaseInteractionTest):
    """Level 1: Test GitGet to ArangoDB pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="GitGet to ArangoDB Pipeline",
            level=1,
            modules=["GitGet", "ArangoDB", "Test Reporter"]
        )
    
    def test_repo_analysis_storage(self):
        """Test analyzing repos and storing results"""
        self.print_header()
        
        # Import modules
        try:
            from gitget import analyze_repository, extract_code_insights
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run pipeline"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize ArangoDB
        try:
            arango = ArangoDocumentHandler()
            self.record_test("arangodb_init", True, {})
        except Exception as e:
            self.add_bug(
                "ArangoDB initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("arangodb_init", False, {"error": str(e)})
            return
        
        # Test repositories
        test_repos = [
            {
                "name": "Small utility library",
                "url": "https://github.com/requests/requests",
                "expected_size": "small"
            },
            {
                "name": "Medium-sized project",
                "url": "https://github.com/pallets/flask",
                "expected_size": "medium"
            },
            {
                "name": "Large framework",
                "url": "https://github.com/django/django",
                "expected_size": "large"
            }
        ]
        
        for repo in test_repos:
            print(f"\nTesting: {repo['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Analyze repository
                print(f"Analyzing repository: {repo['url']}")
                analysis_start = time.time()
                
                analysis = analyze_repository(repo["url"])
                analysis_time = time.time() - analysis_start
                
                if not analysis:
                    self.add_bug(
                        "Repository analysis failed",
                        "HIGH",
                        repo=repo["name"],
                        url=repo["url"]
                    )
                    continue
                
                print(f"✅ Analysis complete in {analysis_time:.2f}s")
                print(f"   Files: {analysis.get('total_files', 0)}")
                print(f"   Languages: {', '.join(analysis.get('languages', [])[:3])}")
                
                # Step 2: Extract code insights
                print("Extracting code insights...")
                insights_start = time.time()
                
                insights = extract_code_insights(repo["url"])
                insights_time = time.time() - insights_start
                
                # Step 3: Prepare document for storage
                repo_id = hashlib.md5(repo["url"].encode()).hexdigest()
                
                document = {
                    "_key": f"repo_{repo_id}",
                    "url": repo["url"],
                    "name": repo["name"],
                    "analysis": analysis,
                    "insights": insights or {},
                    "analyzed_at": time.time(),
                    "analysis_duration": analysis_time + insights_time,
                    "metadata": {
                        "stars": analysis.get("stars", 0),
                        "forks": analysis.get("forks", 0),
                        "size_mb": analysis.get("size_mb", 0),
                        "primary_language": analysis.get("languages", ["Unknown"])[0]
                    }
                }
                
                # Check document size
                doc_size = len(str(document))
                if doc_size > 1000000:  # 1MB limit
                    self.add_bug(
                        "Document too large for storage",
                        "HIGH",
                        repo=repo["name"],
                        size_bytes=doc_size
                    )
                    
                    # Try to reduce size
                    if "file_contents" in document["analysis"]:
                        del document["analysis"]["file_contents"]
                    if "detailed_metrics" in document["insights"]:
                        document["insights"]["summary"] = document["insights"].get("summary", {})
                        del document["insights"]["detailed_metrics"]
                
                # Step 4: Store in ArangoDB
                print("Storing analysis in ArangoDB...")
                storage_start = time.time()
                
                result = arango.handle({
                    "operation": "create",
                    "collection": "code_repositories",
                    "data": document
                })
                
                storage_time = time.time() - storage_start
                
                if result and "error" not in result:
                    print(f"✅ Stored with key: {result.get('_key')}")
                    
                    self.record_test(f"pipeline_{repo['name']}", True, {
                        "analysis_time": analysis_time,
                        "insights_time": insights_time,
                        "storage_time": storage_time,
                        "total_time": time.time() - pipeline_start,
                        "doc_size": doc_size,
                        "files_analyzed": analysis.get("total_files", 0)
                    })
                    
                    # Performance checks
                    total_time = time.time() - pipeline_start
                    if repo["expected_size"] == "small" and total_time > 30:
                        self.add_bug(
                            "Slow small repo processing",
                            "MEDIUM",
                            repo=repo["name"],
                            duration=f"{total_time:.2f}s"
                        )
                    elif repo["expected_size"] == "large" and total_time > 300:
                        self.add_bug(
                            "Very slow large repo processing",
                            "HIGH",
                            repo=repo["name"],
                            duration=f"{total_time:.2f}s"
                        )
                else:
                    self.add_bug(
                        "Failed to store analysis",
                        "HIGH",
                        repo=repo["name"],
                        error=result.get("error", "Unknown")
                    )
                    self.record_test(f"storage_{repo['name']}", False, {
                        "error": result.get("error")
                    })
                    
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {repo['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{repo['name']}", False, {"error": str(e)})
    
    def test_code_search_capabilities(self):
        """Test searching stored code analysis"""
        print("\n\nTesting Code Search Capabilities...")
        
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            arango = ArangoDocumentHandler()
            
            # Test different search scenarios
            search_tests = [
                {
                    "name": "Search by language",
                    "query": {"metadata.primary_language": "Python"}
                },
                {
                    "name": "Search by size",
                    "query": {"metadata.size_mb": {"$gte": 10, "$lte": 100}}
                },
                {
                    "name": "Search by popularity",
                    "query": {"metadata.stars": {"$gte": 1000}}
                },
                {
                    "name": "Search by insights",
                    "query": {"insights.has_tests": True}
                }
            ]
            
            for test in search_tests:
                print(f"\nTesting: {test['name']}")
                
                search_start = time.time()
                
                result = arango.handle({
                    "operation": "search",
                    "collection": "code_repositories",
                    "query": test["query"]
                })
                
                search_time = time.time() - search_start
                
                if result and "documents" in result:
                    docs = result["documents"]
                    print(f"✅ Found {len(docs)} repositories in {search_time:.2f}s")
                    
                    self.record_test(f"search_{test['name']}", True, {
                        "results": len(docs),
                        "duration": search_time
                    })
                    
                    # Validate search results
                    if docs and test["name"] == "Search by language":
                        # Check if results match criteria
                        for doc in docs[:5]:
                            lang = doc.get("metadata", {}).get("primary_language")
                            if lang != "Python":
                                self.add_bug(
                                    "Search returned incorrect results",
                                    "HIGH",
                                    query=test["query"],
                                    expected="Python",
                                    got=lang
                                )
                    
                    # Performance check
                    if search_time > 2:
                        self.add_bug(
                            "Slow search performance",
                            "MEDIUM",
                            query_type=test["name"],
                            duration=f"{search_time:.2f}s"
                        )
                else:
                    self.add_bug(
                        "Search failed",
                        "HIGH",
                        test=test["name"],
                        error=result.get("error", "Unknown")
                    )
                    self.record_test(f"search_{test['name']}", False, {})
                    
        except Exception as e:
            self.add_bug(
                "Exception in search test",
                "HIGH",
                error=str(e)
            )
            self.record_test("search_test", False, {"error": str(e)})
    
    def test_dependency_graph_storage(self):
        """Test storing repository dependency graphs"""
        print("\n\nTesting Dependency Graph Storage...")
        
        try:
            from gitget import analyze_dependencies
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            
            arango = ArangoDocumentHandler()
            
            # Test repository
            repo_url = "https://github.com/pallets/flask"
            
            print(f"Analyzing dependencies for: {repo_url}")
            
            # Get dependency graph
            dependencies = analyze_dependencies(repo_url)
            
            if dependencies:
                print(f"✅ Found {len(dependencies.get('direct', []))} direct dependencies")
                
                # Create graph structure for ArangoDB
                nodes = []
                edges = []
                
                # Add main repo as node
                main_node = {
                    "_key": "flask",
                    "type": "repository",
                    "url": repo_url,
                    "name": "flask"
                }
                nodes.append(main_node)
                
                # Add dependencies as nodes and edges
                for dep in dependencies.get("direct", []):
                    dep_node = {
                        "_key": dep["name"].replace("/", "_"),
                        "type": "dependency",
                        "name": dep["name"],
                        "version": dep.get("version", "latest")
                    }
                    nodes.append(dep_node)
                    
                    edge = {
                        "_from": f"dependencies/{main_node['_key']}",
                        "_to": f"dependencies/{dep_node['_key']}",
                        "type": "depends_on",
                        "version_constraint": dep.get("version", "*")
                    }
                    edges.append(edge)
                
                # Store graph in ArangoDB
                print(f"Storing dependency graph: {len(nodes)} nodes, {len(edges)} edges")
                
                # Create collections if needed
                arango.handle({
                    "operation": "create_collection",
                    "collection": "dependencies",
                    "type": "document"
                })
                
                arango.handle({
                    "operation": "create_collection",
                    "collection": "dependency_edges",
                    "type": "edge"
                })
                
                # Bulk insert nodes
                nodes_result = arango.handle({
                    "operation": "bulk_create",
                    "collection": "dependencies",
                    "documents": nodes
                })
                
                # Bulk insert edges
                edges_result = arango.handle({
                    "operation": "bulk_create",
                    "collection": "dependency_edges",
                    "documents": edges
                })
                
                if nodes_result and edges_result:
                    print("✅ Dependency graph stored successfully")
                    
                    self.record_test("dependency_graph_storage", True, {
                        "nodes": len(nodes),
                        "edges": len(edges)
                    })
                else:
                    self.add_bug(
                        "Failed to store dependency graph",
                        "HIGH",
                        nodes_error=nodes_result.get("error"),
                        edges_error=edges_result.get("error")
                    )
            else:
                self.add_bug(
                    "Failed to analyze dependencies",
                    "HIGH",
                    repo=repo_url
                )
                
        except AttributeError:
            print("❌ Dependency analysis not implemented")
            self.record_test("dependency_analysis", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in dependency graph test",
                "HIGH",
                error=str(e)
            )
            self.record_test("dependency_graph", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_repo_analysis_storage()
        self.test_code_search_capabilities()
        self.test_dependency_graph_storage()
        return self.generate_report()


def main():
    """Run the test"""
    tester = GitGetToArangoDBPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)