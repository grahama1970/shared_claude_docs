#!/usr/bin/env python3
"""
Module: run_real_granger_tests.py
Description: Execute Granger scenarios with REAL module interactions from actual installations

This script properly sets up paths to use the real Granger modules from
/home/graham/workspace/experiments/ and runs interaction tests.

External Dependencies:
- All Granger modules installed in experiments directory

Sample Input:
>>> runner = RealGrangerTestRunner()
>>> runner.test_sparta_module()

Expected Output:
>>> {
>>>     "module": "sparta",
>>>     "status": "connected",
>>>     "bugs_found": ["list of real bugs"]
>>> }
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add all module paths to Python path
MODULES_PATH = Path("/home/graham/workspace/experiments")
MODULE_DIRS = [
    "sparta", "arxiv-mcp-server", "arangodb", "youtube_transcripts",
    "marker", "llm_call", "gitget", "world_model", "rl_commons",
    "claude-test-reporter", "granger_hub"
]

for module_dir in MODULE_DIRS:
    module_path = MODULES_PATH / module_dir / "src"
    if module_path.exists():
        sys.path.insert(0, str(module_path))
    # Also try without src
    module_path = MODULES_PATH / module_dir
    if module_path.exists():
        sys.path.insert(0, str(module_path))

class RealGrangerTestRunner:
    """Run real module interaction tests"""
    
    def __init__(self):
        self.results = []
        self.bugs_found = []
        
    def test_sparta_module(self) -> Dict[str, Any]:
        """Test real SPARTA module functionality"""
        print("\n" + "="*80)
        print("Testing SPARTA Module (Real)")
        print("="*80)
        
        result = {
            "module": "sparta",
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        try:
            # Try to import from installed location
            sys.path.insert(0, str(MODULES_PATH / "sparta" / "src"))
            from sparta.handlers import CVESearchHandler
            
            print("✅ Successfully imported SPARTA module")
            
            # Test 1: Basic CVE search
            print("\nTest 1: Basic CVE search...")
            handler = CVESearchHandler()
            
            test_keywords = [
                "buffer overflow",
                "sql injection",
                "cross site scripting"
            ]
            
            for keyword in test_keywords:
                try:
                    start = time.time()
                    response = handler.handle({
                        "action": "search",
                        "keyword": keyword,
                        "limit": 5
                    })
                    duration = time.time() - start
                    
                    test_result = {
                        "test": f"CVE search: {keyword}",
                        "duration": duration,
                        "status": "success" if response.get("success") else "failed",
                        "vulnerabilities_found": len(response.get("vulnerabilities", []))
                    }
                    
                    # Check for bugs
                    if duration < 0.01:
                        test_result["bug"] = "Response too fast - possible mock"
                        self.bugs_found.append(f"SPARTA: Instant response for '{keyword}'")
                    
                    if response.get("success") and not response.get("vulnerabilities"):
                        test_result["bug"] = "Success but no data returned"
                        self.bugs_found.append(f"SPARTA: Empty results for '{keyword}'")
                    
                    result["tests"].append(test_result)
                    print(f"  - {keyword}: {test_result['status']} ({duration:.3f}s)")
                    
                except Exception as e:
                    test_result = {
                        "test": f"CVE search: {keyword}",
                        "status": "error",
                        "error": str(e)
                    }
                    result["tests"].append(test_result)
                    self.bugs_found.append(f"SPARTA: Exception on '{keyword}' - {str(e)}")
                    print(f"  - {keyword}: ERROR - {e}")
            
        except ImportError as e:
            result["status"] = "import_failed"
            result["error"] = str(e)
            self.bugs_found.append(f"SPARTA: Import failed - {e}")
            print(f"❌ Failed to import SPARTA: {e}")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.bugs_found.append(f"SPARTA: Unexpected error - {e}")
            print(f"❌ Unexpected error: {e}")
        
        self.results.append(result)
        return result
    
    def test_arangodb_module(self) -> Dict[str, Any]:
        """Test real ArangoDB module functionality"""
        print("\n" + "="*80)
        print("Testing ArangoDB Module (Real)")
        print("="*80)
        
        result = {
            "module": "arangodb",
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        try:
            # Try direct import from experiments
            sys.path.insert(0, str(MODULES_PATH / "arangodb" / "src"))
            from arangodb.handlers import ArangoDBHandler
            
            print("✅ Successfully imported ArangoDB module")
            
            # Test 1: Connection test
            print("\nTest 1: Database connection...")
            handler = ArangoDBHandler()
            
            try:
                start = time.time()
                # Try to connect
                connection_result = handler.handle({
                    "action": "connect",
                    "host": "http://localhost:8529"
                })
                duration = time.time() - start
                
                test_result = {
                    "test": "Database connection",
                    "duration": duration,
                    "status": "connected" if connection_result.get("success") else "failed"
                }
                
                if duration < 0.01:
                    test_result["bug"] = "Connection too fast"
                    self.bugs_found.append("ArangoDB: Instant connection suspicious")
                
                result["tests"].append(test_result)
                print(f"  - Connection: {test_result['status']} ({duration:.3f}s)")
                
            except Exception as e:
                test_result = {
                    "test": "Database connection",
                    "status": "error",
                    "error": str(e)
                }
                result["tests"].append(test_result)
                self.bugs_found.append(f"ArangoDB: Connection error - {e}")
                print(f"  - Connection: ERROR - {e}")
            
            # Test 2: Document operations
            print("\nTest 2: Document operations...")
            test_docs = [
                {"name": "test1", "type": "bug_test"},
                {"name": "test2", "data": {"nested": "value"}}
            ]
            
            for doc in test_docs:
                try:
                    start = time.time()
                    insert_result = handler.handle({
                        "action": "insert",
                        "collection": "test_collection",
                        "document": doc
                    })
                    duration = time.time() - start
                    
                    test_result = {
                        "test": f"Insert document: {doc.get('name')}",
                        "duration": duration,
                        "status": "success" if insert_result.get("success") else "failed"
                    }
                    
                    if duration < 0.05:
                        test_result["bug"] = "Insert too fast for network operation"
                        self.bugs_found.append(f"ArangoDB: Suspiciously fast insert")
                    
                    result["tests"].append(test_result)
                    print(f"  - Insert {doc.get('name')}: {test_result['status']} ({duration:.3f}s)")
                    
                except Exception as e:
                    test_result = {
                        "test": f"Insert document: {doc.get('name')}",
                        "status": "error",
                        "error": str(e)
                    }
                    result["tests"].append(test_result)
                    self.bugs_found.append(f"ArangoDB: Insert error - {e}")
                    
        except ImportError as e:
            result["status"] = "import_failed"
            result["error"] = str(e)
            self.bugs_found.append(f"ArangoDB: Import failed - {e}")
            print(f"❌ Failed to import ArangoDB: {e}")
            
        except Exception as e:
            result["status"] = "error"  
            result["error"] = str(e)
            self.bugs_found.append(f"ArangoDB: Unexpected error - {e}")
            print(f"❌ Unexpected error: {e}")
        
        self.results.append(result)
        return result
    
    def test_module_interaction(self) -> Dict[str, Any]:
        """Test real module-to-module interaction"""
        print("\n" + "="*80)
        print("Testing Module Interactions (Real)")
        print("="*80)
        
        result = {
            "interaction": "sparta_to_arangodb",
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
        
        try:
            # Import both modules
            sys.path.insert(0, str(MODULES_PATH / "sparta" / "src"))
            sys.path.insert(0, str(MODULES_PATH / "arangodb" / "src"))
            
            from sparta.handlers import CVESearchHandler
            from arangodb.handlers import ArangoDBHandler
            
            print("✅ Successfully imported both modules")
            
            # Test: Search CVE and store in ArangoDB
            print("\nTest: CVE search → ArangoDB storage pipeline...")
            
            sparta = CVESearchHandler()
            arango = ArangoDBHandler()
            
            # Step 1: Search for CVEs
            start = time.time()
            cve_result = sparta.handle({
                "action": "search",
                "keyword": "buffer overflow",
                "limit": 3
            })
            search_duration = time.time() - start
            
            test_result = {
                "test": "CVE search",
                "duration": search_duration,
                "status": "success" if cve_result.get("success") else "failed",
                "cves_found": len(cve_result.get("vulnerabilities", []))
            }
            result["tests"].append(test_result)
            print(f"  - CVE search: {test_result['status']} ({search_duration:.3f}s)")
            
            # Step 2: Store each CVE in ArangoDB
            if cve_result.get("vulnerabilities"):
                for cve in cve_result["vulnerabilities"][:2]:  # Just first 2
                    start = time.time()
                    store_result = arango.handle({
                        "action": "insert",
                        "collection": "cve_data",
                        "document": cve
                    })
                    store_duration = time.time() - start
                    
                    test_result = {
                        "test": f"Store CVE {cve.get('cve', {}).get('id', 'unknown')}",
                        "duration": store_duration,
                        "status": "success" if store_result.get("success") else "failed"
                    }
                    
                    if search_duration + store_duration < 0.1:
                        test_result["bug"] = "Pipeline too fast for real network operations"
                        self.bugs_found.append("Module interaction: Unrealistic speed")
                    
                    result["tests"].append(test_result)
                    print(f"  - Store CVE: {test_result['status']} ({store_duration:.3f}s)")
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            self.bugs_found.append(f"Module interaction: {e}")
            print(f"❌ Interaction test failed: {e}")
        
        self.results.append(result)
        return result
    
    def generate_verification_report(self) -> Dict[str, Any]:
        """Generate skeptical verification report"""
        print("\n" + "="*80)
        print("VERIFICATION REPORT")
        print("="*80)
        
        total_tests = sum(len(r.get("tests", [])) for r in self.results)
        successful_tests = sum(
            1 for r in self.results 
            for t in r.get("tests", []) 
            if t.get("status") in ["success", "connected"]
        )
        
        # Calculate suspicion indicators
        instant_responses = sum(
            1 for r in self.results
            for t in r.get("tests", [])
            if t.get("duration", 1) < 0.01
        )
        
        import_failures = sum(
            1 for r in self.results
            if r.get("status") == "import_failed"
        )
        
        verification_result = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "successful": successful_tests,
                "failed": total_tests - successful_tests,
                "bugs_found": len(self.bugs_found),
                "import_failures": import_failures,
                "instant_responses": instant_responses
            },
            "bugs": self.bugs_found,
            "verdict": "REAL" if instant_responses == 0 and import_failures < 2 else "SUSPICIOUS",
            "confidence": 1.0 - (instant_responses / max(total_tests, 1)) - (import_failures * 0.2)
        }
        
        # Print summary
        print(f"\nTotal Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {total_tests - successful_tests}")
        print(f"Bugs Found: {len(self.bugs_found)}")
        print(f"Import Failures: {import_failures}")
        print(f"Instant Responses: {instant_responses}")
        print(f"\nVerdict: {verification_result['verdict']}")
        print(f"Confidence: {verification_result['confidence']:.2f}")
        
        if self.bugs_found:
            print("\nBugs Found:")
            for bug in self.bugs_found:
                print(f"  - {bug}")
        
        # Save detailed report
        report_path = Path("verification_reports") / f"real_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps({
            "verification": verification_result,
            "detailed_results": self.results
        }, indent=2))
        
        print(f"\n📄 Detailed report: {report_path}")
        
        return verification_result


def main():
    """Run real Granger module tests"""
    print("🔍 Starting Real Granger Module Testing")
    print("📋 NO MOCKS - Testing actual module installations")
    print("🐛 Bug hunting mode enabled")
    
    runner = RealGrangerTestRunner()
    
    # Run individual module tests
    runner.test_sparta_module()
    runner.test_arangodb_module()
    
    # Run interaction test
    runner.test_module_interaction()
    
    # Generate report
    report = runner.generate_verification_report()
    
    # Return appropriate exit code
    if report["verdict"] == "REAL" and report["summary"]["bugs_found"] == 0:
        print("\n✅ All tests passed with real modules")
        return 0
    else:
        print(f"\n⚠️ Issues detected - {len(runner.bugs_found)} bugs found")
        return 1


if __name__ == "__main__":
    exit(main())