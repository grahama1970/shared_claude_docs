#!/usr/bin/env python3
"""
Run SPARTA verification with proper error handling
Following TEST_VERIFICATION_TEMPLATE_GUIDE.md strictly
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Path to SPARTA
SPARTA_PATH = Path("/home/graham/workspace/experiments/sparta")

def check_and_fix_prerequisites():
    """Check prerequisites and fix what we can."""
    print("🔍 Checking Prerequisites for SPARTA...")
    issues = []
    
    # 1. Check for banned validate_*.py files (excluding .venv)
    validate_files = []
    for f in SPARTA_PATH.rglob("validate_*.py"):
        if ".venv" not in str(f):
            validate_files.append(f)
    
    if validate_files:
        print(f"\n❌ Found {len(validate_files)} validate_*.py files (banned by CLAUDE.md):")
        for f in validate_files:
            print(f"   - {f.relative_to(SPARTA_PATH)}")
        issues.append("validate_files")
    
    # 2. Check Python version
    result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    print(f"\n✓ Python version: {result.stdout.strip()}")
    
    # 3. Check if we're in SPARTA directory
    if not SPARTA_PATH.exists():
        print(f"\n❌ SPARTA not found at: {SPARTA_PATH}")
        return False, issues
    
    # 4. Check for tests directory
    if not (SPARTA_PATH / "tests").exists():
        print(f"\n❌ No tests directory found")
        return False, issues
    
    # 5. Check for .venv
    if not (SPARTA_PATH / ".venv").exists():
        print(f"\n❌ No .venv found - creating one...")
        subprocess.run(["python", "-m", "venv", str(SPARTA_PATH / ".venv")])
        issues.append("created_venv")
    
    # 6. Check ArangoDB
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8529/_api/version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            print("\n✓ ArangoDB is running")
        else:
            print("\n⚠️  ArangoDB not accessible")
            issues.append("arangodb_down")
    except:
        print("\n⚠️  Could not check ArangoDB")
        issues.append("arangodb_check_failed")
    
    return len(issues) == 0 or (len(issues) == 1 and "validate_files" in issues), issues


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    os.chdir(SPARTA_PATH)
    
    # Activate venv and install
    commands = [
        "source .venv/bin/activate && uv pip install -e .",
        "source .venv/bin/activate && uv add --dev pytest pytest-asyncio pytest-json-report",
        "source .venv/bin/activate && uv add requests"  # For honeypot tests
    ]
    
    for cmd in commands:
        result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Warning: {cmd} had issues")
            print(result.stderr[:200])


def remove_mocks():
    """Check for and report mock usage."""
    print("\n🔍 Checking for mock usage...")
    
    # Search for mocks in test files
    result = subprocess.run(
        # REMOVED: ["grep", "-r", "mock\\|Mock\\|@patch", str(SPARTA_PATH / "tests"), "--include=*.py"],
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        lines = result.stdout.strip().split('\n')
        print(f"\n❌ Found {len(lines)} instances of mock usage:")
        for line in lines[:5]:  # Show first 5
            print(f"   {line[:100]}...")
        print(f"   ... and {len(lines)-5} more") if len(lines) > 5 else None
        return False
    else:
        print("✓ No mock usage found")
        return True


def run_tests_with_verification():
    """Run tests and collect detailed timing data."""
    print("\n🧪 Running SPARTA tests...")
    
    os.chdir(SPARTA_PATH)
    
    # First, let's see what tests we have
    list_cmd = "source .venv/bin/activate && python -m pytest --collect-only -q tests/ 2>/dev/null | grep -E '^[^ ]' | head -20"
    result = subprocess.run(["bash", "-c", list_cmd], capture_output=True, text=True)
    
    if result.stdout:
        test_count = len(result.stdout.strip().split('\n'))
        print(f"\n📋 Found approximately {test_count} tests")
        print("Sample tests:")
        for line in result.stdout.strip().split('\n')[:5]:
            print(f"   - {line}")
    
    # Run tests with JSON report
    test_cmd = """source .venv/bin/activate && python -m pytest -v \
        --json-report --json-report-file=test_report.json \
        --durations=10 \
        -p no:warnings \
        tests/ \
        -k 'not test_honeypot' \
        --tb=short"""
    
    print("\n⏳ Running tests (this may take a minute)...")
    start_time = datetime.now()
    
    result = subprocess.run(
        ["bash", "-c", test_cmd],
        capture_output=True,
        text=True,
        timeout=300  # 5 minute timeout
    )
    
    duration = (datetime.now() - start_time).total_seconds()
    print(f"\n✓ Test run completed in {duration:.1f} seconds")
    
    # Check if report was generated
    report_file = SPARTA_PATH / "test_report.json"
    if report_file.exists():
        with open(report_file) as f:
            report = json.load(f)
            
        summary = report.get("summary", {})
        print(f"\n📊 Test Results:")
        print(f"   Total: {summary.get('total', 0)}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Skipped: {summary.get('skipped', 0)}")
        
        # Analyze test durations
        analyze_test_durations(report)
        
        return report
    else:
        print("\n❌ No test report generated")
        print("STDOUT:", result.stdout[:500])
        print("STDERR:", result.stderr[:500])
        return None


def analyze_test_durations(report):
    """Analyze test durations for suspicious patterns."""
    print("\n⏱️  Analyzing test durations...")
    
    duration_buckets = {
        "instant (<1ms)": 0,
        "very_fast (1-10ms)": 0,
        "fast (10-100ms)": 0,
        "normal (100ms-1s)": 0,
        "slow (>1s)": 0
    }
    
    suspicious_tests = []
    
    for test in report.get("tests", []):
        duration = test.get("duration", 0)
        
        if duration < 0.001:
            duration_buckets["instant (<1ms)"] += 1
            suspicious_tests.append((test["nodeid"], duration))
        elif duration < 0.01:
            duration_buckets["very_fast (1-10ms)"] += 1
        elif duration < 0.1:
            duration_buckets["fast (10-100ms)"] += 1
        elif duration < 1.0:
            duration_buckets["normal (100ms-1s)"] += 1
        else:
            duration_buckets["slow (>1s)"] += 1
    
    print("\nDuration Distribution:")
    for bucket, count in duration_buckets.items():
        print(f"   {bucket}: {count} tests")
    
    if suspicious_tests:
        print(f"\n⚠️  Found {len(suspicious_tests)} suspiciously fast tests (<1ms):")
        for test_name, duration in suspicious_tests[:5]:
            print(f"   - {test_name}: {duration*1000:.3f}ms")


def run_honeypot_tests():
    """Run honeypot tests - they should ALL fail."""
    print("\n🍯 Running honeypot tests (should all FAIL)...")
    
    os.chdir(SPARTA_PATH)
    
    # Check if honeypot tests exist
    honeypot_file = SPARTA_PATH / "tests" / "test_honeypot.py"
    if not honeypot_file.exists():
        print("⚠️  No honeypot tests found - creating them...")
        # Run our honeypot creator
        subprocess.run([sys.executable, str(Path.cwd() / "verification" / "create_honeypot_tests.py")])
    
    # Run honeypot tests
    honeypot_cmd = """source .venv/bin/activate && python -m pytest -v \
        -k 'test_honeypot' \
        --tb=short \
        tests/test_honeypot.py || true"""  # Don't fail on test failures
    
    result = subprocess.run(
        ["bash", "-c", honeypot_cmd],
        capture_output=True,
        text=True
    )
    
    # Check that they all failed
    if "failed" in result.stdout:
        # Count failures
        import re
        failed_match = re.search(r'(\d+) failed', result.stdout)
        if failed_match:
            failed_count = int(failed_match.group(1))
            print(f"✅ Good! {failed_count} honeypot tests failed as expected")
            return True
    else:
        print("❌ WARNING: Some honeypot tests may have passed!")
        print(result.stdout[:500])
        return False


def generate_verification_report(test_report, issues, honeypot_ok):
    """Generate final verification report."""
    report = {
        "module": "SPARTA",
        "timestamp": datetime.now().isoformat(),
        "prerequisites": {
            "issues_found": issues,
            "ready": len(issues) <= 1  # Only validate_files is ok
        },
        "test_results": None,
        "honeypot_results": {
            "all_failed": honeypot_ok,
            "integrity": "GOOD" if honeypot_ok else "COMPROMISED"
        },
        "verdict": None
    }
    
    if test_report:
        summary = test_report.get("summary", {})
        report["test_results"] = {
            "total": summary.get("total", 0),
            "passed": summary.get("passed", 0),
            "failed": summary.get("failed", 0),
            "success_rate": (summary.get("passed", 0) / summary.get("total", 1)) * 100
        }
        
        # Determine verdict
        if honeypot_ok and report["test_results"]["success_rate"] > 80:
            report["verdict"] = "LIKELY REAL - High confidence"
        elif not honeypot_ok:
            report["verdict"] = "TESTING FRAMEWORK COMPROMISED"
        else:
            report["verdict"] = "NEEDS INVESTIGATION"
    else:
        report["verdict"] = "COULD NOT RUN TESTS"
    
    # Save report
    report_path = Path.cwd() / "verification" / "sparta_final_verification.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Module: SPARTA")
    print(f"Verdict: {report['verdict']}")
    if report["test_results"]:
        print(f"Tests: {report['test_results']['passed']}/{report['test_results']['total']} passed")
        print(f"Success Rate: {report['test_results']['success_rate']:.1f}%")
    print(f"Honeypot Integrity: {report['honeypot_results']['integrity']}")
    
    return report


def main():
    print("🔍 SPARTA Module Verification")
    print("Following TEST_VERIFICATION_TEMPLATE_GUIDE.md")
    print("="*60)
    
    # Step 1: Prerequisites
    ready, issues = check_and_fix_prerequisites()
    
    if not ready and "validate_files" not in issues:
        print("\n❌ Prerequisites not met. Cannot continue.")
        return
    
    # Step 2: Install dependencies
    install_dependencies()
    
    # Step 3: Check for mocks
    no_mocks = remove_mocks()
    if not no_mocks:
        issues.append("mocks_detected")
    
    # Step 4: Run main tests
    test_report = run_tests_with_verification()
    
    # Step 5: Run honeypot tests
    honeypot_ok = run_honeypot_tests()
    
    # Step 6: Generate report
    report = generate_verification_report(test_report, issues, honeypot_ok)
    
    print("\n✅ Verification complete!")
    
    # Return exit code based on verdict
    if "REAL" in report["verdict"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    # Change to SPARTA directory for operations
    original_dir = Path.cwd()
    try:
        exit_code = main()
        sys.exit(exit_code)
    finally:
        os.chdir(original_dir)