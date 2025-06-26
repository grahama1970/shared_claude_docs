#!/usr/bin/env python3
"""
Module: test_13_marker_to_arangodb_pipeline.py
Description: Test Marker → ArangoDB document storage pipeline
Level: 1
Modules: Marker, ArangoDB, Test Reporter
Expected Bugs: Document structure mismatches, storage failures, query performance
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import hashlib

class MarkerToArangoDBPipelineTest(BaseInteractionTest):
    """Level 1: Test Marker to ArangoDB pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="Marker to ArangoDB Pipeline",
            level=1,
            modules=["Marker", "ArangoDB", "Test Reporter"]
        )
    
    def test_pdf_to_knowledge_base(self):
        """Test converting PDFs and storing in knowledge base"""
        self.print_header()
        
        # Import modules
        try:
            from marker.src.marker import convert_pdf_to_markdown
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
        
        # Test PDFs for knowledge base
        test_pdfs = [
            {
                "name": "Research paper",
                "url": "https://arxiv.org/pdf/2301.12345.pdf",
                "collection": "research_papers"
            },
            {
                "name": "Technical documentation",
                "url": "https://example.com/docs.pdf",
                "collection": "technical_docs"
            },
            {
                "name": "Large PDF",
                "url": "https://arxiv.org/pdf/2301.98765.pdf",
                "collection": "research_papers"
            }
        ]
        
        stored_documents = []
        
        for test in test_pdfs:
            print(f"\nTesting: {test['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Convert PDF to Markdown
                print(f"Converting PDF: {test['url']}")
                conversion_start = time.time()
                
                result = convert_pdf_to_markdown(test["url"])
                conversion_time = time.time() - conversion_start
                
                if not result or not result.get("markdown"):
                    self.add_bug(
                        "PDF conversion failed",
                        "HIGH",
                        pdf=test["name"],
                        url=test["url"]
                    )
                    continue
                
                markdown = result["markdown"]
                metadata = result.get("metadata", {})
                
                print(f"✅ Converted: {len(markdown)} chars in {conversion_time:.2f}s")
                
                # Step 2: Prepare document for storage
                doc_id = hashlib.md5(test["url"].encode()).hexdigest()
                
                document = {
                    "_key": doc_id,
                    "title": metadata.get("title", test["name"]),
                    "source_url": test["url"],
                    "content": markdown,
                    "content_length": len(markdown),
                    "conversion_time": conversion_time,
                    "metadata": metadata,
                    "timestamp": time.time(),
                    "type": "pdf_conversion"
                }
                
                # Check document structure
                if len(markdown) > 1000000:  # 1MB limit check
                    self.add_bug(
                        "Document too large for storage",
                        "HIGH",
                        size_chars=len(markdown),
                        doc_id=doc_id
                    )
                
                # Step 3: Store in ArangoDB
                print(f"Storing in collection: {test['collection']}")
                storage_start = time.time()
                
                storage_result = arango.handle({
                    "operation": "create",
                    "collection": test["collection"],
                    "data": document
                })
                
                storage_time = time.time() - storage_start
                
                if storage_result and "error" not in storage_result:
                    print(f"✅ Stored with key: {storage_result.get('_key')}")
                    
                    stored_documents.append({
                        "key": storage_result.get("_key"),
                        "collection": test["collection"]
                    })
                    
                    self.record_test(f"pipeline_{test['name']}", True, {
                        "conversion_time": conversion_time,
                        "storage_time": storage_time,
                        "total_time": time.time() - pipeline_start,
                        "content_length": len(markdown),
                        "doc_key": storage_result.get("_key")
                    })
                    
                    # Performance checks
                    if storage_time > 5:
                        self.add_bug(
                            "Slow document storage",
                            "MEDIUM",
                            duration=f"{storage_time:.2f}s",
                            size=len(markdown)
                        )
                else:
                    error = storage_result.get("error", "Unknown error")
                    self.add_bug(
                        "Failed to store document",
                        "HIGH",
                        error=error,
                        doc_id=doc_id
                    )
                    self.record_test(f"storage_{test['name']}", False, {"error": error})
                    
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {test['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{test['name']}", False, {"error": str(e)})
        
        # Test retrieval of stored documents
        self.test_document_retrieval(arango, stored_documents)
    
    def test_document_retrieval(self, arango, stored_documents):
        """Test retrieving stored documents"""
        print("\n\nTesting Document Retrieval...")
        
        for doc_info in stored_documents:
            print(f"\nRetrieving document: {doc_info['key']}")
            
            try:
                result = arango.handle({
                    "operation": "get",
                    "collection": doc_info["collection"],
                    "key": doc_info["key"]
                })
                
                if result and "document" in result:
                    doc = result["document"]
                    print(f"✅ Retrieved document: {len(doc.get('content', ''))} chars")
                    
                    # Verify document integrity
                    required_fields = ["content", "source_url", "timestamp"]
                    missing = [f for f in required_fields if f not in doc]
                    
                    if missing:
                        self.add_bug(
                            "Retrieved document missing fields",
                            "HIGH",
                            missing_fields=missing,
                            doc_key=doc_info["key"]
                        )
                    
                    self.record_test(f"retrieval_{doc_info['key']}", True, {
                        "content_length": len(doc.get("content", ""))
                    })
                else:
                    self.add_bug(
                        "Failed to retrieve document",
                        "HIGH",
                        key=doc_info["key"],
                        collection=doc_info["collection"]
                    )
                    self.record_test(f"retrieval_{doc_info['key']}", False, {})
                    
            except Exception as e:
                self.add_bug(
                    "Exception retrieving document",
                    "HIGH",
                    error=str(e),
                    key=doc_info["key"]
                )
    
    def test_bulk_import(self):
        """Test bulk import of multiple documents"""
        print("\n\nTesting Bulk Import...")
        
        try:
            from marker.src.marker import convert_pdf_to_markdown
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            
            arango = ArangoDocumentHandler()
            
            # Prepare multiple documents
            print("Preparing 10 documents for bulk import...")
            
            documents = []
            for i in range(10):
                doc = {
                    "_key": f"bulk_doc_{i}",
                    "title": f"Bulk Document {i}",
                    "content": f"This is test content for document {i}" * 100,
                    "index": i,
                    "timestamp": time.time()
                }
                documents.append(doc)
            
            # Bulk import
            bulk_start = time.time()
            
            result = arango.handle({
                "operation": "bulk_create",
                "collection": "bulk_test",
                "documents": documents
            })
            
            bulk_time = time.time() - bulk_start
            
            if result and "created" in result:
                created_count = result.get("created", 0)
                print(f"✅ Bulk imported {created_count} documents in {bulk_time:.2f}s")
                
                self.record_test("bulk_import", True, {
                    "documents": len(documents),
                    "created": created_count,
                    "duration": bulk_time,
                    "docs_per_second": len(documents) / bulk_time
                })
                
                # Check import quality
                if created_count < len(documents):
                    self.add_bug(
                        "Incomplete bulk import",
                        "HIGH",
                        expected=len(documents),
                        created=created_count
                    )
                
                # Performance check
                docs_per_second = len(documents) / bulk_time
                if docs_per_second < 10:
                    self.add_bug(
                        "Slow bulk import",
                        "MEDIUM",
                        docs_per_second=docs_per_second
                    )
            else:
                self.add_bug(
                    "Bulk import failed",
                    "HIGH",
                    error=result.get("error", "Unknown")
                )
                self.record_test("bulk_import", False, {})
                
        except AttributeError:
            print("❌ Bulk import not implemented")
            self.record_test("bulk_import", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in bulk import",
                "HIGH",
                error=str(e)
            )
            self.record_test("bulk_import", False, {"error": str(e)})
    
    def test_search_capabilities(self):
        """Test searching stored documents"""
        print("\n\nTesting Search Capabilities...")
        
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            arango = ArangoDocumentHandler()
            
            # Test different search scenarios
            search_tests = [
                {
                    "name": "Full text search",
                    "query": "machine learning",
                    "collection": "research_papers"
                },
                {
                    "name": "Metadata search",
                    "query": {"type": "pdf_conversion"},
                    "collection": "research_papers"
                },
                {
                    "name": "Date range search",
                    "query": {
                        "timestamp": {
                            "$gte": time.time() - 3600,  # Last hour
                            "$lte": time.time()
                        }
                    },
                    "collection": "research_papers"
                }
            ]
            
            for test in search_tests:
                print(f"\nTesting: {test['name']}")
                
                search_start = time.time()
                
                result = arango.handle({
                    "operation": "search",
                    "collection": test["collection"],
                    "query": test["query"]
                })
                
                search_time = time.time() - search_start
                
                if result and "documents" in result:
                    docs = result["documents"]
                    print(f"✅ Found {len(docs)} documents in {search_time:.2f}s")
                    
                    self.record_test(f"search_{test['name']}", True, {
                        "results": len(docs),
                        "duration": search_time
                    })
                    
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
    
    def run_tests(self):
        """Run all tests"""
        self.test_pdf_to_knowledge_base()
        self.test_bulk_import()
        self.test_search_capabilities()
        return self.generate_report()


def main():
    """Run the test"""
    tester = MarkerToArangoDBPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)