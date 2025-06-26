#!/usr/bin/env python3
"""
Test Task 60: Real-time Collaboration Engine

Verifies the collaboration engine implementation with comprehensive tests.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


def run_command(cmd: List[str], cwd: Path = None) -> Tuple[int, str, str]:
    """Run a command and return exit code, stdout, and stderr"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out after 60 seconds"
    except Exception as e:
        return 1, "", str(e)


def test_implementation() -> Dict[str, any]:
    """Test the collaboration engine implementation"""
    results = {
        "tests": [],
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0
        }
    }
    
    project_dir = Path("collaboration-engine")
    
    # Test 1: Check directory structure
    print("\n1. Checking directory structure...")
    test_result = {
        "name": "Directory Structure",
        "description": "Verify correct directory layout",
        "status": "Pass",
        "error": None
    }
    
    required_files = [
        "collaboration_engine_interaction.py",
        "__init__.py",
        "tests/__init__.py",
        "tests/test_document_sync.py",
        "tests/test_conflict_resolution.py",
        "tests/test_presence_tracking.py"
    ]
    
    for file in required_files:
        if not (project_dir / file).exists():
            test_result["status"] = "Fail"
            test_result["error"] = f"Missing file: {file}"
            results["success"] = False
            break
    
    results["tests"].append(test_result)
    
    # Test 2: Run the main validation
    print("\n2. Running main module validation...")
    test_result = {
        "name": "Main Module Validation",
        "description": "Test collaboration engine core functionality",
        "status": "Pass",
        "error": None
    }
    
    exit_code, stdout, stderr = run_command(
        [sys.executable, "collaboration_engine_interaction.py"],
        cwd=project_dir
    )
    
    if exit_code != 0:
        test_result["status"] = "Fail"
        test_result["error"] = f"Exit code: {exit_code}\nStderr: {stderr}"
        results["success"] = False
    elif "Collaboration Engine validation passed" not in stdout:
        test_result["status"] = "Fail"
        test_result["error"] = "Validation message not found in output"
        results["success"] = False
    
    results["tests"].append(test_result)
    
    # Test 3: Run pytest tests
    print("\n3. Running pytest tests...")
    test_files = [
        "tests/test_document_sync.py",
        "tests/test_conflict_resolution.py",
        "tests/test_presence_tracking.py"
    ]
    
    for test_file in test_files:
        test_name = Path(test_file).stem.replace("test_", "").replace("_", " ").title()
        test_result = {
            "name": f"Pytest: {test_name}",
            "description": f"Run {test_file}",
            "status": "Pass",
            "error": None
        }
        
        exit_code, stdout, stderr = run_command(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            cwd=project_dir
        )
        
        if exit_code != 0:
            test_result["status"] = "Fail"
            test_result["error"] = f"Exit code: {exit_code}"
            results["success"] = False
            
            # Extract failure details
            if "FAILED" in stdout:
                lines = stdout.split("\n")
                for line in lines:
                    if "FAILED" in line and "::" in line:
                        test_result["error"] += f"\n  - {line.strip()}"
        
        results["tests"].append(test_result)
    
    # Test 4: Check implementation features
    print("\n4. Checking implementation features...")
    test_result = {
        "name": "Feature Implementation",
        "description": "Verify all required features are implemented",
        "status": "Pass",
        "error": None
    }
    
    # Read the main module
    main_file = project_dir / "collaboration_engine_interaction.py"
    content = main_file.read_text()
    
    required_features = [
        ("WebSocket communication mentioned", "websocket" in content.lower()),
        ("Operational transformation", "OperationalTransform" in content),
        ("Presence tracking", "track_presence" in content),
        ("Cursor tracking", "update_cursor" in content),
        ("Selection tracking", "update_selection" in content),
        ("Conflict resolution", "resolve_conflicts" in content),
        ("Document synchronization", "handle_document_sync" in content),
        ("Offline sync", "sync_offline_operations" in content),
        ("Version history", "get_document_history" in content),
        ("Comments/annotations", "add_comment" in content),
        ("Locking mechanism", "acquire_lock" in content),
        ("User permissions", "permissions" in content)
    ]
    
    missing_features = []
    for feature_name, is_present in required_features:
        if not is_present:
            missing_features.append(feature_name)
    
    if missing_features:
        test_result["status"] = "Fail"
        test_result["error"] = f"Missing features: {', '.join(missing_features)}"
        results["success"] = False
    
    results["tests"].append(test_result)
    
    # Test 5: Performance test
    print("\n5. Running performance test...")
    test_result = {
        "name": "Performance Test",
        "description": "Test collaboration engine performance",
        "status": "Pass",
        "error": None,
        "performance_metrics": {}
    }
    
    # Create a performance test script
    perf_test = '''
import asyncio
import time
from collaboration_engine_interaction import CollaborationEngine, Operation, OperationType

async def performance_test():
    engine = CollaborationEngine()
    session = await engine.create_session("perf_doc", "user1", "PerfTest")
    
    # Test rapid operations
    start_time = time.time()
    operation_count = 50
    
    for i in range(operation_count):
        op = Operation(
            id=f"perf_{i}",
            type=OperationType.INSERT,
            user_id="user1",
            timestamp=time.time(),
            version=i,
            data={"position": 0, "text": f"{i}"}
        )
        await engine.apply_operation(session.id, op)
    
    duration = time.time() - start_time
    ops_per_sec = operation_count / duration
    
    print(f"Operations per second: {ops_per_sec:.1f}")
    print(f"Average latency: {(duration/operation_count)*1000:.1f}ms")
    
    return ops_per_sec > 10  # Should handle at least 10 ops/sec

result = asyncio.run(performance_test())
exit(0 if result else 1)
'''
    
    perf_file = project_dir / "perf_test.py"
    perf_file.write_text(perf_test)
    
    exit_code, stdout, stderr = run_command(
        [sys.executable, "perf_test.py"],
        cwd=project_dir
    )
    
    # Clean up
    perf_file.unlink()
    
    if exit_code != 0:
        test_result["status"] = "Fail"
        test_result["error"] = "Performance test failed"
        results["success"] = False
    else:
        # Extract metrics from output
        if "Operations per second:" in stdout:
            for line in stdout.split("\n"):
                if "Operations per second:" in line:
                    ops_sec = line.split(":")[1].strip()
                    test_result["performance_metrics"]["ops_per_second"] = ops_sec
                elif "Average latency:" in line:
                    latency = line.split(":")[1].strip()
                    test_result["performance_metrics"]["avg_latency"] = latency
    
    results["tests"].append(test_result)
    
    # Calculate summary
    results["summary"]["total"] = len(results["tests"])
    results["summary"]["passed"] = sum(1 for t in results["tests"] if t["status"] == "Pass")
    results["summary"]["failed"] = results["summary"]["total"] - results["summary"]["passed"]
    
    return results


def generate_report(results: Dict[str, any]) -> None:
    """Generate a markdown report of the test results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"test_report_task_60_{timestamp}.md"
    
    content = f"""# Task 60 Test Report: Real-time Collaboration Engine

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Total Tests**: {results['summary']['total']}
- **Passed**: {results['summary']['passed']}
- **Failed**: {results['summary']['failed']}
- **Success**: {'✅ Yes' if results['success'] else '❌ No'}

## Test Results

| Test Name | Description | Status | Error |
|-----------|-------------|--------|-------|
"""
    
    for test in results["tests"]:
        status = "✅ Pass" if test["status"] == "Pass" else "❌ Fail"
        error = test["error"] or "None"
        error = error.replace("\n", "<br>") if len(error) > 50 else error
        
        content += f"| {test['name']} | {test['description']} | {status} | {error} |\n"
    
    # Add performance metrics if available
    perf_test = next((t for t in results["tests"] if "performance_metrics" in t), None)
    if perf_test and perf_test["performance_metrics"]:
        content += "\n## Performance Metrics\n\n"
        for metric, value in perf_test["performance_metrics"].items():
            content += f"- **{metric.replace('_', ' ').title()}**: {value}\n"
    
    content += f"\n## Implementation Details\n\n"
    content += "- **Architecture**: Level 2 - Parallel Processing\n"
    content += "- **Key Features**: Real-time sync, Operational transformation, Presence tracking\n"
    content += "- **Use Cases**: Collaborative editing, Shared workspaces, Multi-user documents\n"
    
    with open(report_path, "w") as f:
        f.write(content)
    
    print(f"\n📄 Report generated: {report_path}")


def main():
    """Main test execution"""
    print("=" * 60)
    print("Task 60: Real-time Collaboration Engine - Test Suite")
    print("=" * 60)
    
    # Change to project_interactions directory
    orig_dir = Path.cwd()
    try:
        import os
        os.chdir("project_interactions")
        
        # Check if the directory exists and rename if needed
        if Path("collaboration-engine").exists() and not Path("collaboration_engine").exists():
            print("\n📁 Renaming directory to Python convention...")
            Path("collaboration-engine").rename("collaboration_engine")
        
        # Now work with the correct directory name
        if Path("collaboration_engine").exists():
            os.chdir(orig_dir)
            os.chdir("project_interactions")
            project_dir = "collaboration_engine"
        else:
            project_dir = "collaboration-engine"
        
        # Run tests
        results = test_implementation()
        
        # Generate report
        generate_report(results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(f"Total Tests: {results['summary']['total']}")
        print(f"Passed: {results['summary']['passed']}")
        print(f"Failed: {results['summary']['failed']}")
        
        if results['success']:
            print("\n✅ All tests passed! Collaboration engine is working correctly.")
            return 0
        else:
            print("\n❌ Some tests failed. Please check the report for details.")
            return 1
            
    finally:
        os.chdir(orig_dir)


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)