#!/usr/bin/env python3
"""
Module: test_01_sparta_cve_search.py
Description: Test basic SPARTA CVE search functionality
Level: 0
Modules: SPARTA
Expected Bugs: Missing CVE data, malformed responses, rate limiting
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path

class SPARTACVESearchTest:
    """Level 0: Test basic SPARTA CVE search functionality"""
    
    def __init__(self):
        self.test_name = "SPARTA CVE Search"
        self.level = 0
        self.bugs_found = []
        
    def test_basic_cve_search(self):
        """Test basic CVE search with common terms"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"{'='*60}\n")
        
        # Import SPARTA handler
        try:
            from sparta.real_sparta_handlers_fixed import SPARTACVESearchHandler
            self.sparta = SPARTACVESearchHandler()
        except ImportError as e:
            self.bugs_found.append({
                "bug": "SPARTA module import failure",
                "error": str(e),
                "severity": "CRITICAL",
                "impact": "Cannot use SPARTA functionality"
            })
            print(f"❌ Import failed: {e}")
            return
        
        # Test cases
        test_keywords = [
            "buffer overflow",
            "sql injection", 
            "cross site scripting",
            "",  # Empty query
            "CVE-2024-",  # Partial CVE ID
            "😈💉🔥",  # Unicode
            "a" * 1000,  # Very long query
        ]
        
        for keyword in test_keywords:
            print(f"\nTesting keyword: '{keyword[:50]}{'...' if len(keyword) > 50 else ''}'")
            
            try:
                start_time = time.time()
                result = self.sparta.handle({
                    "keyword": keyword,
                    "limit": 5
                })
                duration = time.time() - start_time
                
                if result.get("success"):
                    cves = result.get("vulnerabilities", [])
                    print(f"✅ Found {len(cves)} CVEs in {duration:.2f}s")
                    
                    # Check for data quality issues
                    for cve in cves:
                        cve_data = cve.get("cve", {})
                        
                        # Bug: Missing CVE ID
                        if not cve_data.get("id"):
                            self.bugs_found.append({
                                "bug": "CVE missing ID",
                                "keyword": keyword,
                                "severity": "HIGH"
                            })
                            
                        # Bug: No description
                        desc = cve_data.get("description", {}).get("description_data", [])
                        if not desc or not desc[0].get("value"):
                            self.bugs_found.append({
                                "bug": "CVE missing description",
                                "cve_id": cve_data.get("id", "Unknown"),
                                "severity": "MEDIUM"
                            })
                    
                    # Performance issue
                    if duration > 5:
                        self.bugs_found.append({
                            "bug": "Slow CVE search",
                            "keyword": keyword,
                            "duration": f"{duration:.2f}s",
                            "severity": "MEDIUM"
                        })
                        
                else:
                    error = result.get("error", "Unknown error")
                    print(f"❌ Search failed: {error}")
                    
                    # Check if proper error for empty query
                    if keyword == "" and "keyword" not in error.lower():
                        self.bugs_found.append({
                            "bug": "Poor error message for empty query",
                            "error": error,
                            "severity": "LOW"
                        })
                        
            except Exception as e:
                self.bugs_found.append({
                    "bug": "Exception during CVE search",
                    "keyword": keyword[:50],
                    "error": str(e),
                    "severity": "HIGH"
                })
                print(f"💥 Exception: {e}")
    
    def test_cve_details_retrieval(self):
        """Test retrieving specific CVE details"""
        print("\n\nTesting CVE Details Retrieval...")
        
        test_cve_ids = [
            "CVE-2024-12345",  # Recent CVE
            "CVE-1999-0001",   # Old CVE
            "CVE-INVALID",     # Invalid format
            "",                # Empty
            None,              # None type
        ]
        
        for cve_id in test_cve_ids:
            if cve_id is None:
                continue
                
            print(f"\nTesting CVE ID: '{cve_id}'")
            
            try:
                # Assuming there's a get_cve_details method
                result = self.sparta.handle({
                    "action": "get_details",
                    "cve_id": cve_id
                })
                
                if "error" in result:
                    if cve_id == "" and "cve_id" not in result["error"].lower():
                        self.bugs_found.append({
                            "bug": "Unclear error for empty CVE ID",
                            "error": result["error"],
                            "severity": "LOW"
                        })
                        
            except AttributeError:
                print("   ℹ️ CVE details method not available")
                break
            except Exception as e:
                self.bugs_found.append({
                    "bug": "Exception getting CVE details",
                    "cve_id": cve_id,
                    "error": str(e),
                    "severity": "MEDIUM"
                })
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"{'='*60}")
        
        if not self.bugs_found:
            print("\n✅ No bugs found!")
            return
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            bugs = [b for b in self.bugs_found if b.get("severity") == severity]
            if bugs:
                print(f"\n{severity} ({len(bugs)} bugs):")
                for bug in bugs:
                    print(f"  - {bug['bug']}")
                    if "error" in bug:
                        print(f"    Error: {bug['error'][:50]}...")
        
        # Save detailed report
        report_path = Path(f"bug_reports/level0_{self.test_name.lower().replace(' ', '_')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report: {report_path}")
        
        return self.bugs_found


def main():
    """Run the test"""
    tester = SPARTACVESearchTest()
    tester.test_basic_cve_search()
    tester.test_cve_details_retrieval()
    return tester.generate_report()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)