"""
Run all Level 0 tests for ArXiv module and generate a comprehensive report.

This script runs all test modules and creates a detailed Markdown report
with results, timings, and test outcomes.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import time
import sys
from datetime import datetime
from pathlib import Path
import json
from typing import Dict, List, Any

# Import test modules
from test_search_papers import TestSearchPapers
from test_paper_details import TestPaperDetails
from test_download_paper import TestDownloadPaper
from test_honeypot import TestArxivHoneypot


class TestRunner:
    """Runs all tests and generates reports."""
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def run_test_method(self, test_class, method_name: str, description: str) -> Dict[str, Any]:
        """Run a single test method and capture results."""
        test_instance = test_class()
        method = getattr(test_instance, method_name)
        
        start_time = time.time()
        result = {
            "test_name": f"{test_class.__name__}.{method_name}",
            "description": description,
            "start_time": datetime.now().isoformat(),
            "status": "Pass",
            "error": None,
            "duration": 0
        }
        
        try:
            method()
            result["actual_result"] = "Test completed successfully"
        except AssertionError as e:
            result["status"] = "Fail"
            result["error"] = str(e)
            result["actual_result"] = f"Assertion failed: {str(e)}"
        except Exception as e:
            result["status"] = "Error"
            result["error"] = f"{type(e).__name__}: {str(e)}"
            result["actual_result"] = f"Unexpected error: {str(e)}"
        
        result["duration"] = round(time.time() - start_time, 3)
        return result
    
    def run_all_tests(self):
        """Run all test suites."""
        self.start_time = datetime.now()
        
        # Define all tests to run
        test_suites = [
            {
                "class": TestSearchPapers,
                "tests": [
                    ("test_basic_search", "Search for papers using basic query"),
                    ("test_advanced_search_with_filters", "Search with category filters"),
                    ("test_author_search", "Search papers by author name"),
                    ("test_recent_papers_search", "Search for recent papers"),
                    ("test_empty_search_results", "Handle searches with no results"),
                    ("test_search_with_multiple_terms", "Complex search with operators"),
                ]
            },
            {
                "class": TestPaperDetails,
                "tests": [
                    ("test_get_paper_by_id", "Retrieve paper details by ArXiv ID"),
                    ("test_get_multiple_papers", "Retrieve multiple papers by ID"),
                    ("test_paper_version_handling", "Handle paper versions (v1, v2, etc)"),
                    ("test_paper_metadata_completeness", "Check metadata completeness"),
                    ("test_invalid_paper_id", "Handle invalid paper IDs"),
                    ("test_paper_affiliations", "Extract author affiliations"),
                ]
            },
            {
                "class": TestDownloadPaper,
                "tests": [
                    ("test_get_pdf_url", "Get PDF URL for a paper"),
                    ("test_verify_pdf_accessible", "Verify PDF URL is accessible"),
                    ("test_download_pdf_content", "Download actual PDF content"),
                    ("test_save_pdf_to_file", "Save PDF to local file"),
                    ("test_download_url_generation", "Generate URLs for different formats"),
                    ("test_batch_download_urls", "Get URLs for multiple papers"),
                ]
            },
            {
                "class": TestArxivHoneypot,
                "tests": [
                    ("test_nonexistent_paper_id", "HONEYPOT: Non-existent paper"),
                    ("test_impossible_search_results", "HONEYPOT: Impossible search"),
                    ("test_future_paper_date", "HONEYPOT: Future publication dates"),
                    ("test_perfect_download_speed", "HONEYPOT: Instant downloads"),
                    ("test_identical_paper_metadata", "HONEYPOT: Duplicate metadata"),
                    ("test_author_with_thousand_papers", "HONEYPOT: Impossible author"),
                    ("test_instant_batch_results", "HONEYPOT: Instant batch results"),
                    ("test_malformed_data_acceptance", "HONEYPOT: Malformed queries"),
                ]
            }
        ]
        
        # Run each test suite
        for suite in test_suites:
            print(f"\n{'='*60}")
            print(f"Running {suite['class'].__name__} tests...")
            print('='*60)
            
            for method_name, description in suite["tests"]:
                print(f"\n▶ {method_name}: {description}")
                result = self.run_test_method(suite["class"], method_name, description)
                self.results.append(result)
                
                # Print immediate feedback
                if result["status"] == "Pass":
                    print(f"  ✅ PASSED in {result['duration']}s")
                elif result["status"] == "Fail":
                    print(f"  ❌ FAILED: {result['error']}")
                else:
                    print(f"  ⚠️  ERROR: {result['error']}")
        
        self.end_time = datetime.now()
    
    def generate_report(self) -> str:
        """Generate a comprehensive Markdown report."""
        if not self.results:
            return "No test results to report."
        
        # Calculate statistics
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "Pass"])
        failed_tests = len([r for r in self.results if r["status"] == "Fail"])
        error_tests = len([r for r in self.results if r["status"] == "Error"])
        
        # Separate honeypot tests
        honeypot_results = [r for r in self.results if "HONEYPOT" in r["description"]]
        regular_results = [r for r in self.results if "HONEYPOT" not in r["description"]]
        
        # Count honeypot successes (which are actually good - they should fail)
        honeypot_working = len([r for r in honeypot_results if r["status"] in ["Fail", "Error"]])
        
        total_duration = sum(r["duration"] for r in self.results)
        
        # Generate report
        report = f"""# ArXiv Module Level 0 Test Report

Generated: {self.end_time.isoformat()}

## Summary

- **Total Tests**: {total_tests}
- **Passed**: {passed_tests}
- **Failed**: {failed_tests}
- **Errors**: {error_tests}
- **Success Rate**: {(passed_tests / total_tests * 100):.1f}%
- **Total Duration**: {total_duration:.2f}s
- **Test Duration**: {(self.end_time - self.start_time).total_seconds():.2f}s

## Honeypot Tests

**{honeypot_working}/{len(honeypot_results)} honeypot tests working correctly** (they failed as expected)

## Test Results

| Test Name | Description | Result | Status | Duration | Error |
|-----------|-------------|--------|--------|----------|-------|
"""
        
        # Add regular test results
        for result in regular_results:
            status_icon = "✅" if result["status"] == "Pass" else "❌" if result["status"] == "Fail" else "⚠️"
            error_msg = result["error"] or ""
            if len(error_msg) > 50:
                error_msg = error_msg[:50] + "..."
            
            report += f"| {result['test_name']} | {result['description']} | {result['actual_result'][:40]}... | {status_icon} | {result['duration']}s | {error_msg} |\n"
        
        # Add honeypot section
        report += "\n## Honeypot Test Results\n\n"
        report += "| Test Name | Description | Status | Expected | Result |\n"
        report += "|-----------|-------------|--------|----------|--------|\n"
        
        for result in honeypot_results:
            # For honeypots, failing is good
            is_working = result["status"] in ["Fail", "Error"]
            status_icon = "✅" if is_working else "❌"
            expected = "Should Fail"
            actual = "Failed (Good)" if is_working else "Passed (Bad!)"
            
            report += f"| {result['test_name']} | {result['description'][:30]}... | {status_icon} | {expected} | {actual} |\n"
        
        # Add detailed results for failures
        failures = [r for r in self.results if r["status"] != "Pass"]
        if failures:
            report += "\n## Failed Test Details\n\n"
            for failure in failures:
                report += f"### {failure['test_name']}\n\n"
                report += f"**Description**: {failure['description']}\n\n"
                report += f"**Error**: {failure['error']}\n\n"
                report += f"**Duration**: {failure['duration']}s\n\n"
                report += "---\n\n"
        
        # Add performance analysis
        report += "## Performance Analysis\n\n"
        report += "| Test Category | Avg Duration | Min | Max |\n"
        report += "|---------------|--------------|-----|-----|\n"
        
        # Group by test class
        for class_name in ["TestSearchPapers", "TestPaperDetails", "TestDownloadPaper"]:
            class_results = [r for r in regular_results if class_name in r["test_name"]]
            if class_results:
                durations = [r["duration"] for r in class_results]
                avg_duration = sum(durations) / len(durations)
                min_duration = min(durations)
                max_duration = max(durations)
                report += f"| {class_name} | {avg_duration:.2f}s | {min_duration:.2f}s | {max_duration:.2f}s |\n"
        
        return report
    
    def save_report(self, filepath: Path):
        """Save the report to a file."""
        report = self.generate_report()
        filepath.write_text(report)
        print(f"\n📄 Report saved to: {filepath}")
    
    def save_json_results(self, filepath: Path):
        """Save raw results as JSON."""
        json_data = {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "total_duration": (self.end_time - self.start_time).total_seconds(),
            "results": self.results
        }
        
        with open(filepath, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"📊 JSON results saved to: {filepath}")


def main():
    """Run all tests and generate reports."""
    print("🚀 Starting ArXiv Module Level 0 Tests")
    print("=" * 60)
    
    runner = TestRunner()
    
    try:
        # Run all tests
        runner.run_all_tests()
        
        # Generate timestamp for report files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create reports directory
        reports_dir = Path("../../../docs/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Save reports
        report_path = reports_dir / f"arxiv_test_report_{timestamp}.md"
        json_path = reports_dir / f"arxiv_test_results_{timestamp}.json"
        
        runner.save_report(report_path)
        runner.save_json_results(json_path)
        
        # Print summary
        total = len(runner.results)
        passed = len([r for r in runner.results if r["status"] == "Pass"])
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed / total * 100):.1f}%")
        
        # Check honeypot tests
        honeypot_results = [r for r in runner.results if "HONEYPOT" in r["description"]]
        honeypot_working = len([r for r in honeypot_results if r["status"] in ["Fail", "Error"]])
        
        print(f"\nHoneypot Tests: {honeypot_working}/{len(honeypot_results)} working correctly")
        
        if honeypot_working < len(honeypot_results):
            print("⚠️  WARNING: Some honeypot tests passed! This may indicate fake test data.")
        
        # Exit code based on results
        if passed == total:
            print("\n✅ All tests passed!")
            # sys.exit() removed
        else:
            print(f"\n❌ {total - passed} tests failed!")
            # sys.exit() removed
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        # sys.exit() removed
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        # sys.exit() removed


if __name__ == "__main__":
    main()