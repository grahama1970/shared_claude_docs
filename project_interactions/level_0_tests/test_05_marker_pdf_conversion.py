#!/usr/bin/env python3
"""
Module: test_05_marker_pdf_conversion.py
Description: Test Marker PDF to Markdown conversion with test reporter verification
Level: 0
Modules: Marker, Claude Test Reporter
Expected Bugs: PDF parsing errors, table extraction issues, format preservation
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path
import sys

sys.path.insert(0, '/home/graham/workspace/experiments')

# Import the test reporter for skeptical verification
try:
    from claude_test_reporter import GrangerTestReporter
    TEST_REPORTER_AVAILABLE = True
except ImportError:
    TEST_REPORTER_AVAILABLE = False
    print("Warning: Test Reporter not available for verification")

class MarkerPDFConversionTest:
    """Level 0: Test Marker PDF conversion with skeptical verification"""
    
    def __init__(self):
        self.test_name = "Marker PDF Conversion"
        self.level = 0
        self.bugs_found = []
        self.test_results = []
        
        # Initialize test reporter
        if TEST_REPORTER_AVAILABLE:
            self.reporter = GrangerTestReporter(
                module_name="marker_pdf_conversion",
                test_suite="level_0_tests"
            )
        else:
            self.reporter = None
    
    def _record_test(self, test_name: str, passed: bool, details: Dict[str, Any]):
        """Record test result for reporter verification"""
        result = {
            "test": test_name,
            "passed": passed,
            "timestamp": time.time(),
            "details": details
        }
        self.test_results.append(result)
        
        # Also report to test reporter
        if self.reporter:
            self.reporter.add_test_result(
                test_name=test_name,
                status="PASS" if passed else "FAIL",
                duration=details.get("duration", 0),
                error=details.get("error") if not passed else None
            )
    
    def test_pdf_conversion(self):
        """Test converting various PDF types to Markdown"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"{'='*60}\n")
        
        # Import Marker
        try:
            from marker.src.marker import convert_pdf_to_markdown
            from marker.src.marker.settings import Settings
        except ImportError as e:
            self.bugs_found.append({
                "bug": "Marker module import failure",
                "error": str(e),
                "severity": "CRITICAL",
                "impact": "Cannot use Marker functionality"
            })
            self._record_test("marker_import", False, {"error": str(e)})
            print(f"❌ Import failed: {e}")
            return
        
        self._record_test("marker_import", True, {})
        
        # Test PDFs with different characteristics
        test_pdfs = [
            {
                "name": "Simple text PDF",
                "url": "https://arxiv.org/pdf/2301.12345.pdf",
                "expected_features": ["text", "paragraphs"]
            },
            {
                "name": "PDF with tables",
                "url": "https://arxiv.org/pdf/2301.12345.pdf",
                "expected_features": ["tables", "columns"]
            },
            {
                "name": "PDF with images",
                "url": "https://arxiv.org/pdf/2301.12345.pdf",
                "expected_features": ["figures", "captions"]
            },
            {
                "name": "PDF with equations",
                "url": "https://arxiv.org/pdf/2301.12345.pdf",
                "expected_features": ["math", "latex"]
            },
            {
                "name": "Invalid PDF URL",
                "url": "https://notareal.site/fake.pdf",
                "expected_features": []
            },
            {
                "name": "Empty URL",
                "url": "",
                "expected_features": []
            }
        ]
        
        for test_pdf in test_pdfs:
            print(f"\nTesting: {test_pdf['name']}")
            test_start = time.time()
            
            try:
                # Configure settings
                settings = Settings()
                settings.enable_table_extraction = True
                settings.enable_figure_extraction = True
                
                # Convert PDF
                result = convert_pdf_to_markdown(
                    pdf_url=test_pdf["url"],
                    settings=settings
                )
                
                duration = time.time() - test_start
                
                if result and isinstance(result, dict):
                    markdown = result.get("markdown", "")
                    metadata = result.get("metadata", {})
                    
                    print(f"✅ Converted: {len(markdown)} chars in {duration:.2f}s")
                    
                    # Verify expected features
                    missing_features = []
                    for feature in test_pdf["expected_features"]:
                        if feature == "tables" and "|" not in markdown:
                            missing_features.append(feature)
                        elif feature == "math" and "$" not in markdown:
                            missing_features.append(feature)
                    
                    if missing_features:
                        self.bugs_found.append({
                            "bug": f"Missing expected features",
                            "pdf": test_pdf["name"],
                            "missing": missing_features,
                            "severity": "HIGH"
                        })
                        self._record_test(f"pdf_features_{test_pdf['name']}", False, {
                            "missing_features": missing_features
                        })
                    else:
                        self._record_test(f"pdf_features_{test_pdf['name']}", True, {
                            "markdown_length": len(markdown)
                        })
                    
                    # Check for quality issues
                    if len(markdown) < 100 and test_pdf["name"] != "Invalid PDF URL":
                        self.bugs_found.append({
                            "bug": "Suspiciously short conversion",
                            "pdf": test_pdf["name"],
                            "length": len(markdown),
                            "severity": "HIGH"
                        })
                    
                    # Performance check
                    if duration > 30:
                        self.bugs_found.append({
                            "bug": "Slow PDF conversion",
                            "pdf": test_pdf["name"],
                            "duration": f"{duration:.2f}s",
                            "severity": "MEDIUM"
                        })
                else:
                    if test_pdf["name"] not in ["Invalid PDF URL", "Empty URL"]:
                        self.bugs_found.append({
                            "bug": "Conversion returned no result",
                            "pdf": test_pdf["name"],
                            "severity": "HIGH"
                        })
                    self._record_test(f"pdf_conversion_{test_pdf['name']}", False, {
                        "error": "No result returned"
                    })
                    print(f"❌ Conversion failed")
                    
            except Exception as e:
                error_msg = str(e)
                print(f"💥 Exception: {error_msg[:100]}")
                
                self._record_test(f"pdf_conversion_{test_pdf['name']}", False, {
                    "error": error_msg
                })
                
                # Check error quality
                if test_pdf["name"] == "Empty URL" and "url" not in error_msg.lower():
                    self.bugs_found.append({
                        "bug": "Poor error message for empty URL",
                        "error": error_msg,
                        "severity": "LOW"
                    })
    
    def test_table_extraction(self):
        """Test table extraction capabilities"""
        print("\n\nTesting Table Extraction...")
        
        # Create a test case for table extraction
        table_test = {
            "name": "table_extraction",
            "passed": False,
            "details": {}
        }
        
        try:
            from marker.src.marker.tables import extract_tables
            
            # Test with a known PDF containing tables
            test_pdf = "https://arxiv.org/pdf/2301.12345.pdf"
            
            print(f"Extracting tables from: {test_pdf}")
            tables = extract_tables(test_pdf)
            
            if tables and len(tables) > 0:
                print(f"✅ Found {len(tables)} tables")
                table_test["passed"] = True
                table_test["details"]["table_count"] = len(tables)
                
                # Check table quality
                for i, table in enumerate(tables):
                    if not table.get("headers") or not table.get("rows"):
                        self.bugs_found.append({
                            "bug": f"Table {i} missing headers or rows",
                            "severity": "MEDIUM"
                        })
            else:
                print(f"❌ No tables found")
                self.bugs_found.append({
                    "bug": "Table extraction returned empty",
                    "severity": "HIGH"
                })
                
        except ImportError:
            print("❌ Table extraction not available")
            table_test["details"]["error"] = "Module not available"
        except Exception as e:
            self.bugs_found.append({
                "bug": "Exception in table extraction",
                "error": str(e),
                "severity": "HIGH"
            })
            table_test["details"]["error"] = str(e)
        
        self._record_test("table_extraction", table_test["passed"], table_test["details"])
    
    def verify_with_test_reporter(self):
        """Use test reporter to skeptically verify results"""
        print("\n\n🔍 Skeptical Verification with Test Reporter...")
        
        if not self.reporter:
            print("❌ Test Reporter not available for verification")
            return
        
        # Generate skeptical report
        report = self.reporter.generate_report(
            include_skeptical_analysis=True,
            detect_lies=True
        )
        
        # Check for suspicious patterns
        suspicious_patterns = []
        
        # Pattern 1: All tests passing (unlikely)
        pass_rate = sum(1 for r in self.test_results if r["passed"]) / len(self.test_results)
        if pass_rate == 1.0:
            suspicious_patterns.append("100% pass rate is suspicious")
        
        # Pattern 2: Very fast test execution
        fast_tests = [r for r in self.test_results if r["details"].get("duration", 0) < 0.1]
        if len(fast_tests) > len(self.test_results) * 0.5:
            suspicious_patterns.append("Many tests completed suspiciously fast")
        
        # Pattern 3: Identical error messages
        errors = [r["details"].get("error") for r in self.test_results if not r["passed"]]
        if len(set(errors)) < len(errors) * 0.5:
            suspicious_patterns.append("Many identical error messages")
        
        if suspicious_patterns:
            print("\n⚠️ Suspicious patterns detected:")
            for pattern in suspicious_patterns:
                print(f"  - {pattern}")
            
            self.bugs_found.append({
                "bug": "Test results may be unreliable",
                "patterns": suspicious_patterns,
                "severity": "HIGH"
            })
        else:
            print("✅ Test results appear legitimate")
        
        # Save reporter output
        report_path = Path(f"test_reports/{self.test_name.lower().replace(' ', '_')}_verified.html")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        print(f"\n📊 Verification report: {report_path}")
    
    def generate_report(self):
        """Generate test report with verification"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"{'='*60}")
        
        # First verify results
        self.verify_with_test_reporter()
        
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
        
        # Save detailed report
        report_path = Path(f"bug_reports/level0_{self.test_name.lower().replace(' ', '_')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report: {report_path}")
        
        return self.bugs_found


def main():
    """Run the test"""
    tester = MarkerPDFConversionTest()
    tester.test_pdf_conversion()
    tester.test_table_extraction()
    return tester.generate_report()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)