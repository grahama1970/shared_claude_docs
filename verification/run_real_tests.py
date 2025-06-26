#!/usr/bin/env python3
"""
Run real tests and generate verified results using claude-test-reporter
"""

import subprocess
import json
import sys
from pathlib import Path
from datetime import datetime

# Add claude-test-reporter to path
sys.path.insert(0, '/home/graham/workspace/experiments/claude-test-reporter/src')

try:
    from claude_test_reporter.core.test_result_verifier import TestResultVerifier
    from claude_test_reporter.analyzers.llm_test_analyzer import LLMTestAnalyzer
    from claude_test_reporter.monitoring.hallucination_monitor import HallucinationMonitor
except ImportError as e:
    print(f"Error importing claude-test-reporter: {e}")
    print("Make sure claude-test-reporter is properly installed")
    sys.exit(1)


def run_module_tests(module_path: str, module_name: str):
    """Run tests for a specific module and verify results."""
    
    print(f"\n{'='*60}")
    print(f"Testing Module: {module_name}")
    print(f"Path: {module_path}")
    print(f"{'='*60}\n")
    
    # Change to module directory
    original_dir = Path.cwd()
    module_dir = Path(module_path)
    
    if not module_dir.exists():
        print(f"❌ Module directory not found: {module_path}")
        return None
    
    try:
        os.chdir(module_dir)
        
        # Step 1: Check if tests exist
        test_dir = module_dir / "tests"
        if not test_dir.exists():
            print(f"❌ No tests directory found")
            return None
            
        # Count test files
        test_files = list(test_dir.glob("**/test_*.py"))
        print(f"Found {len(test_files)} test files")
        
        # Step 2: Try to collect tests first
        print("\n📋 Collecting tests...")
        collect_cmd = [
            sys.executable, "-m", "pytest", 
            "--collect-only", "--quiet",
            "-p", "no:warnings"
        ]
        
        collect_result = subprocess.run(
            collect_cmd, 
            capture_output=True, 
            text=True
        )
        
        if collect_result.returncode != 0:
            print(f"❌ Test collection failed:")
            print(collect_result.stderr[:500])
            
            # Try to fix common issues
            print("\n🔧 Attempting to fix dependencies...")
            
            # Install test dependencies
            if (module_dir / "pyproject.toml").exists():
                subprocess.run(["uv", "pip", "install", "-e", "."], capture_output=True)
                subprocess.run(["uv", "add", "--dev", "pytest", "pytest-asyncio"], capture_output=True)
        
        # Step 3: Run actual tests
        print("\n🧪 Running tests...")
        
        # Create results directory
        results_dir = module_dir / "test_results"
        results_dir.mkdir(exist_ok=True)
        
        # Run pytest with JSON report
        test_cmd = [
            sys.executable, "-m", "pytest",
            "-v",
            "--tb=short",
            "--json-report",
            f"--json-report-file={results_dir}/results.json",
            "--durations=10",
            "-p", "no:warnings",
            "tests/"
        ]
        
        start_time = datetime.now()
        test_result = subprocess.run(
            test_cmd,
            capture_output=True,
            text=True
        )
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"\nTest execution completed in {duration:.2f}s")
        print(f"Exit code: {test_result.returncode}")
        
        # Parse results
        results_file = results_dir / "results.json"
        if results_file.exists():
            with open(results_file) as f:
                test_data = json.load(f)
                
            # Extract key metrics
            summary = test_data.get("summary", {})
            total = summary.get("total", 0)
            passed = summary.get("passed", 0)
            failed = summary.get("failed", 0)
            
            print(f"\n📊 Test Results:")
            print(f"   Total: {total}")
            print(f"   Passed: {passed}")
            print(f"   Failed: {failed}")
            print(f"   Success Rate: {(passed/total*100) if total > 0 else 0:.1f}%")
            
            # Step 4: Create verified results
            print("\n🔐 Creating verified results...")
            verifier = TestResultVerifier()
            
            # Create test results in expected format
            test_results = {
                "total": total,
                "passed": passed,
                "failed": failed,
                "skipped": summary.get("skipped", 0),
                "success_rate": (passed/total*100) if total > 0 else 0,
                "duration": duration,
                "tests": []
            }
            
            # Add individual test details
            for test in test_data.get("tests", []):
                test_results["tests"].append({
                    "nodeid": test.get("nodeid"),
                    "outcome": test.get("outcome"),
                    "duration": test.get("duration", 0),
                    "error": test.get("call", {}).get("longrepr", "") if test.get("outcome") == "failed" else None
                })
            
            # Create immutable record
            verified_record = verifier.create_immutable_test_record(test_results)
            
            # Save verified results
            verified_file = results_dir / "verified_results.json"
            with open(verified_file, "w") as f:
                json.dump(verified_record, f, indent=2)
                
            print(f"   Hash: {verified_record['verification']['hash'][:32]}...")
            print(f"   Deployment: {'BLOCKED' if failed > 0 else 'ALLOWED'}")
            
            # Step 5: Check for hallucination indicators
            print("\n🔍 Checking for test authenticity...")
            
            # Check for suspiciously fast tests
            fast_tests = [t for t in test_results["tests"] if t["duration"] < 0.001]
            if fast_tests:
                print(f"   ⚠️  {len(fast_tests)} tests completed in <1ms (suspicious)")
                
            # Check for mock usage
            if test_result.stdout:
                # REMOVED: mock_indicators = ["Mock", "patch", "monkeypatch", "MagicMock"]
                mock_found = any(indicator in test_result.stdout for indicator in mock_indicators)
                if mock_found:
                    # REMOVED: print(f"   ❌ Mock usage detected in test output")
            
            return verified_record
            
        else:
            print(f"❌ No test results file generated")
            return None
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        os.chdir(original_dir)


def main():
    """Run tests for key Granger modules."""
    
    # Start with modules that are likely to have real tests
    modules_to_test = [
        ("/home/graham/workspace/experiments/claude-test-reporter", "claude-test-reporter"),
        ("/home/graham/workspace/experiments/sparta", "sparta"),
        ("/home/graham/workspace/experiments/marker", "marker"),
        ("/home/graham/workspace/experiments/arangodb", "arangodb"),
    ]
    
    all_results = {}
    
    for module_path, module_name in modules_to_test:
        result = run_module_tests(module_path, module_name)
        if result:
            all_results[module_name] = result
    
    # Save combined results
    output_file = Path("/home/graham/workspace/shared_claude_docs/verification/all_module_results.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n✅ All results saved to: {output_file}")
    
    # Summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    for module, result in all_results.items():
        facts = result["immutable_facts"]
        print(f"\n{module}:")
        print(f"  Total: {facts['total_tests']}")
        print(f"  Failed: {facts['failed_count']}")
        print(f"  Success Rate: {facts['exact_success_rate']}%")
        print(f"  Deployment: {facts['deployment_status']}")


if __name__ == "__main__":
    import os
    main()