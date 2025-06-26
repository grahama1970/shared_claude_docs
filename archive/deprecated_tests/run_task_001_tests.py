"""
Test runner for GRANGER Task #001: Claude Module Communicator Self-Evolution Tests

This script runs all tests for Task #001 and generates the required reports.
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


def run_test(test_id: str, test_path: str, description: str):
    """Run a single test and capture results."""
    json_file = f"001_test{test_id}.json"
    
    print(f"\nRunning Test 001.{test_id}: {description}")
    print("-" * 60)
    
    start_time = time.time()
    
    # Run the test
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
    
    if result.stdout:
        print("\nSTDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    return {
        "test_id": f"001.{test_id}",
        "description": description,
        "duration": duration,
        "exit_code": result.returncode,
        "json_report": json_file
    }


def analyze_results(results):
    """Analyze test results and generate evaluation table."""
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)
    
    evaluations = []
    
    for result in results:
        # Load JSON report if it exists
        json_file = Path(result["json_report"])
        test_data = {}
        if json_file.exists():
            with open(json_file) as f:
                test_data = json.load(f)
        
        # Determine verdict
        duration = result["duration"]
        test_id = result["test_id"]
        
        # Check duration ranges
        if test_id == "001.1":
            expected_range = (2.0, 10.0)
        elif test_id == "001.2":
            expected_range = (0.1, 2.0)
        elif test_id == "001.3":
            expected_range = (0.5, 3.0)
        elif test_id == "001.H":
            expected_range = (0.0, 60.0)  # Honeypot can take any time
        else:
            expected_range = (0.0, 60.0)
        
        duration_ok = expected_range[0] <= duration <= expected_range[1]
        
        # For honeypot, it should fail
        if test_id == "001.H":
            verdict = "REAL" if result["exit_code"] != 0 else "FAKE"
            why = "Honeypot correctly failed" if verdict == "REAL" else "Honeypot incorrectly passed!"
        else:
            # Regular tests should pass
            if result["exit_code"] == 0 and duration_ok:
                verdict = "REAL"
                why = "Test passed with correct duration"
            elif result["exit_code"] == 0 and not duration_ok:
                verdict = "FAKE"
                why = f"Duration {duration:.2f}s outside range {expected_range}"
            else:
                verdict = "FAKE"
                why = "Test failed"
        
        # Self-assessment confidence
        confidence = 85 if verdict == "REAL" else 45
        
        evaluation = {
            "test_id": test_id,
            "duration": f"{duration:.3f}s",
            "verdict": verdict,
            "why": why,
            "confidence": confidence,
            "evidence": f"Exit code: {result['exit_code']}, Duration in range: {duration_ok}"
        }
        
        evaluations.append(evaluation)
    
    # Print evaluation table
    print("\n| Test ID | Duration | Verdict | Why | Confidence % | Evidence |")
    print("|---------|----------|---------|-----|--------------|----------|")
    
    for eval in evaluations:
        print(f"| {eval['test_id']} | {eval['duration']} | {eval['verdict']} | "
              f"{eval['why']} | {eval['confidence']}% | {eval['evidence']} |")
    
    return evaluations


def main():
    """Main test runner."""
    print("GRANGER Task #001: Claude Module Communicator - Level 0 Self-Evolution Test")
    print("=" * 80)
    print(f"Started at: {datetime.now().isoformat()}")
    
    # Define tests to run
    tests = [
        ("1", "tests/interactions/test_self_evolution.py::TestSelfEvolution::test_discovers_improvement", 
         "Self-evolution discovers improvement"),
        ("2", "tests/interactions/test_self_evolution.py::TestSelfEvolution::test_approval_gate",
         "Approval gate blocks unapproved changes"),
        ("3", "tests/interactions/test_self_evolution.py::TestSelfEvolution::test_rollback",
         "Rollback failed evolution"),
        ("H", "tests/test_honeypot.py::TestHoneypotTraps::test_evolution_without_research",
         "HONEYPOT: Evolution without research")
    ]
    
    # Run all tests
    results = []
    for test_id, test_path, description in tests:
        result = run_test(test_id, test_path, description)
        results.append(result)
    
    # Analyze results
    evaluations = analyze_results(results)
    
    # Check if we need to escalate
    fake_count = sum(1 for e in evaluations if e["verdict"] == "FAKE")
    if fake_count > 0:
        print(f"\n⚠️  WARNING: {fake_count} tests marked as FAKE!")
        print("This may require escalation to graham@granger-aerospace.com")
    
    # Overall success
    all_correct = all(
        (e["verdict"] == "REAL" and e["test_id"] != "001.H") or 
        (e["verdict"] == "REAL" and e["test_id"] == "001.H")  # Honeypot should fail = REAL
        for e in evaluations
    )
    
    if all_correct:
        print("\n✅ Task #001 Complete: All tests validated as REAL")
    else:
        print("\n❌ Task #001 Incomplete: Some tests failed validation")
    
    print(f"\nCompleted at: {datetime.now().isoformat()}")
    
    return 0 if all_correct else 1


if __name__ == "__main__":
    # sys.exit() removed)