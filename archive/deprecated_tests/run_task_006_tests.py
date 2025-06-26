"""
Test runner for GRANGER Task #006: Marker AI-Enhanced Accuracy Tests

This script runs all tests for Task #006 and generates the required reports.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import subprocess
import sys
import json
import time
from pathlib import Path
from datetime import datetime


def run_test(test_id: str, test_path: str, description: str, expected_duration: tuple):
    """Run a single test and capture results."""
    json_file = f"006_test{test_id}.json"
    
    print(f"\nRunning Test 006.{test_id}: {description}")
    print("-" * 60)
    
    start_time = time.time()
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--json-report",
        f"--json-report-file={json_file}",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start_time
    
    print(f"Exit code: {result.returncode}")
    print(f"Duration: {duration:.2f}s")
    print(f"Expected: {expected_duration[0]}s-{expected_duration[1]}s")
    
    return {
        "test_id": f"006.{test_id}",
        "description": description,
        "duration": duration,
        "expected_duration": expected_duration,
        "exit_code": result.returncode,
        "json_report": json_file
    }


def main():
    """Main test runner."""
    print("GRANGER Task #006: Marker - AI-Enhanced Accuracy Improvements")
    print("=" * 80)
    print(f"Started at: {datetime.now().isoformat()}")
    
    tests = [
        ("1", "tests/test_ai_enhancement.py::TestAIEnhancement::test_accuracy_improvement", 
         "AI improves extraction accuracy", (10.0, 30.0)),
        ("2", "tests/test_ai_enhancement.py::TestAIEnhancement::test_complex_tables",
         "Complex table extraction", (5.0, 20.0)),
        ("3", "tests/test_ai_enhancement.py::TestAIEnhancement::test_telemetry_processing",
         "Live hardware data processing", (5.0, 15.0)),
        ("H", "tests/test_ai_enhancement.py::TestHoneypot::test_corrupted_pdf",
         "HONEYPOT: Extract from corrupted PDF", (0.0, 10.0))
    ]
    
    results = []
    for test_id, test_path, description, expected_duration in tests:
        result = run_test(test_id, test_path, description, expected_duration)
        results.append(result)
    
    # Analyze results
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS - TASK #006")
    print("=" * 80)
    
    all_passed = True
    for result in results:
        if result["test_id"] == "006.H":
            # Honeypot should fail
            if result["exit_code"] == 0:
                all_passed = False
                print(f"❌ {result['test_id']}: HONEYPOT PASSED (should fail)")
        else:
            # Regular tests should pass
            if result["exit_code"] != 0:
                all_passed = False
                print(f"❌ {result['test_id']}: FAILED")
            else:
                print(f"✅ {result['test_id']}: PASSED")
    
    if all_passed:
        print("\n✅ Task #006 Complete: All tests validated")
    else:
        print("\n❌ Task #006 Incomplete: Some tests failed")
    
    print(f"\nCompleted at: {datetime.now().isoformat()}")
    return 0 if all_passed else 1


if __name__ == "__main__":
    # sys.exit() removed)