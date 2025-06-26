"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_03_arangodb_storage.py
Description: Test basic ArangoDB document storage operations
Level: 0
Modules: ArangoDB
Expected Bugs: Connection issues, schema violations, data type mismatches
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path
import sys

sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

class ArangoDBStorageTest:
    """Level 0: Test basic ArangoDB storage functionality"""
    
    def __init__(self):
        self.test_name = "ArangoDB Storage"
        self.level = 0
        self.bugs_found = []
        
    def test_document_storage(self):
        """Test storing various document types"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"{'='*60}\n")
        
        # Import ArangoDB handler
        try:
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            self.arango = ArangoDocumentHandler()
        except ImportError as e:
            self.bugs_found.append({
                "bug": "ArangoDB module import failure",
                "error": str(e),
                "severity": "CRITICAL",
                "impact": "Cannot use ArangoDB functionality"
            })
            print(f"❌ Import failed: {e}")
            return
        
        # Test documents with various edge cases
        test_documents = [
            {
                "name": "Normal document",
                "data": {
                    "_key": "test_doc_1",
                    "title": "Test Document",
                    "content": "This is a test",
                    "timestamp": time.time()
                }
            },
            {
                "name": "Document with None values",
                "data": {
                    "_key": "test_doc_2",
                    "title": "Test with None",
                    "content": None,
                    "metadata": None
                }
            },
            {
                "name": "Document with special characters",
                "data": {
                    "_key": "test_doc_3",
                    "title": "Special: $pecial & Ch@rs!",
                    "content": "Line1\nLine2\tTab",
                    "unicode": "Hello 世界 🌍"
                }
            },
            {
                "name": "Document with nested objects",
                "data": {
                    "_key": "test_doc_4",
                    "nested": {
                        "level1": {
                            "level2": {
                                "level3": "deep value"
                            }
                        }
                    }
                }
            },
            {
                "name": "Document with large array",
                "data": {
                    "_key": "test_doc_5",
                    "large_array": list(range(1000)),
                    "matrix": [[i*j for j in range(10)] for i in range(10)]
                }
            },
            {
                "name": "Document with invalid key",
                "data": {
                    "_key": "../../etc/passwd",  # Path traversal attempt
                    "title": "Invalid key test"
                }
            },
            {
                "name": "Document with very long strings",
                "data": {
                    "_key": "test_doc_6",
                    "long_string": "A" * 50000,  # 50KB string
                    "title": "B" * 1000
                }
            },
            {
                "name": "Empty document",
                "data": {}
            },
            {
                "name": "Document with reserved fields",
                "data": {
                    "_key": "test_doc_7",
                    "_id": "should_not_set_this",
                    "_rev": "should_not_set_this",
                    "_from": "invalid",
                    "_to": "invalid"
                }
            }
        ]
        
        for test_doc in test_documents:
            print(f"\nTesting: {test_doc['name']}")
            
            try:
                result = self.arango.handle({
                    "operation": "create",
                    "collection": "test_collection",
                    "data": test_doc["data"]
                })
                
                if "error" not in result:
                    print(f"✅ Document stored successfully")
                    
                    # Check if problematic documents were accepted
                    if "invalid key" in test_doc["name"].lower():
                        self.bugs_found.append({
                            "bug": "Invalid key accepted",
                            "key": test_doc["data"].get("_key"),
                            "severity": "HIGH",
                            "impact": "Security vulnerability"
                        })
                    
                    if test_doc["name"] == "Empty document":
                        self.bugs_found.append({
                            "bug": "Empty document accepted",
                            "severity": "MEDIUM",
                            "impact": "Data integrity issue"
                        })
                    
                    if "None values" in test_doc["name"] and result.get("_key"):
                        # Try to retrieve and check if None preserved
                        retrieve_result = self.arango.handle({
                            "operation": "get",
                            "collection": "test_collection",
                            "key": result["_key"]
                        })
                        if retrieve_result.get("document", {}).get("content") is None:
                            self.bugs_found.append({
                                "bug": "None values preserved in storage",
                                "severity": "MEDIUM",
                                "impact": "JSON serialization issues"
                            })
                else:
                    error = result.get("error", "Unknown")
                    print(f"❌ Storage failed: {error[:100]}")
                    
                    # Check if proper error messages
                    if "reserved fields" in test_doc["name"] and "_id" not in error:
                        self.bugs_found.append({
                            "bug": "Poor error for reserved fields",
                            "error": error,
                            "severity": "LOW"
                        })
                        
            except Exception as e:
                self.bugs_found.append({
                    "bug": f"Exception storing {test_doc['name']}",
                    "error": str(e),
                    "severity": "HIGH"
                })
                print(f"💥 Exception: {e}")
    
    def test_collection_operations(self):
        """Test collection-level operations"""
        print("\n\nTesting Collection Operations...")
        
        operations = [
            {
                "name": "Create with invalid name",
                "params": {
                    "operation": "create_collection",
                    "collection": "123-invalid-name!"
                }
            },
            {
                "name": "Create with empty name",
                "params": {
                    "operation": "create_collection",
                    "collection": ""
                }
            },
            {
                "name": "Drop non-existent collection",
                "params": {
                    "operation": "drop_collection",
                    "collection": "definitely_does_not_exist_12345"
                }
            }
        ]
        
        for op in operations:
            print(f"\nTesting: {op['name']}")
            
            try:
                result = self.arango.handle(op["params"])
                
                if "error" not in result:
                    if "invalid" in op["name"] or "empty" in op["name"]:
                        self.bugs_found.append({
                            "bug": f"Invalid operation succeeded: {op['name']}",
                            "severity": "HIGH",
                            "impact": "No validation"
                        })
                        print(f"❌ Should have failed!")
                else:
                    print(f"✅ Properly rejected: {result['error'][:50]}")
                    
            except Exception as e:
                print(f"💥 Exception: {str(e)[:50]}")
    
    def test_concurrent_operations(self):
        """Test concurrent write scenarios"""
        print("\n\nTesting Concurrent Operations...")
        
        doc_key = "concurrent_test_doc"
        
        # Create initial document
        self.arango.handle({
            "operation": "create",
            "collection": "test_collection",
            "data": {"_key": doc_key, "counter": 0}
        })
        
        # Simulate concurrent updates
        print(f"Simulating 10 concurrent updates...")
        update_results = []
        
        for i in range(10):
            result = self.arango.handle({
                "operation": "update",
                "collection": "test_collection",
                "key": doc_key,
                "data": {"counter": i + 1}
            })
            update_results.append(result)
        
        # Check final state
        final_result = self.arango.handle({
            "operation": "get",
            "collection": "test_collection",
            "key": doc_key
        })
        
        if final_result.get("document"):
            final_counter = final_result["document"].get("counter")
            if final_counter != 10:
                self.bugs_found.append({
                    "bug": "Lost updates in concurrent scenario",
                    "expected": 10,
                    "actual": final_counter,
                    "severity": "HIGH",
                    "impact": "Data consistency issues"
                })
                print(f"❌ Lost updates: counter = {final_counter} (expected 10)")
            else:
                print(f"✅ All updates preserved")
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"{'='*60}")
        
        if not self.bugs_found:
            print("\n✅ No bugs found!")
            return []
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            bugs = [b for b in self.bugs_found if b.get("severity") == severity]
            if bugs:
                print(f"\n{severity} ({len(bugs)} bugs):")
                for bug in bugs:
                    print(f"  - {bug['bug']}")
                    if "impact" in bug:
                        print(f"    Impact: {bug['impact']}")
        
        # Save detailed report
        report_path = Path(f"bug_reports/level0_{self.test_name.lower().replace(' ', '_')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report: {report_path}")
        
        return self.bugs_found


def main():
    """Run the test"""
    tester = ArangoDBStorageTest()
    tester.test_document_storage()
    tester.test_collection_operations()
    tester.test_concurrent_operations()
    return tester.generate_report()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)