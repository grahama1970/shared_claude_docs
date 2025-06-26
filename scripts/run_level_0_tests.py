#!/usr/bin/env python3
"""
Module: run_level_0_tests.py
Description: Run all Level 0 tests across the Granger ecosystem

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python run_level_0_tests.py
"""

import subprocess
from pathlib import Path
import sys
import json
from datetime import datetime


def run_level_0_tests():
    """Run all Level 0 tests."""
    print("🚀 Running Level 0 Tests")
    print("=" * 60)
    
    # Find all Level 0 test directories
    project_interactions = Path("/home/graham/workspace/shared_claude_docs/project_interactions")
    
    level_0_dirs = [
        project_interactions / "arangodb_tests/level_0",
        project_interactions / "arxiv-mcp-server/level_0",
        project_interactions / "arxiv-mcp-server/level_0_tests",
        project_interactions / "arangodb/level_0_tests",
    ]
    
    results = []
    passed_count = 0
    failed_count = 0
    
    for test_dir in level_0_dirs:
        if not test_dir.exists():
            print(f"\n❌ Level 0 test directory not found: {test_dir}")
            continue
            
        print(f"\n📦 Testing {test_dir.name} in {test_dir.parent.name}")
        print("-" * 40)
        
        # Run pytest on the directory
        cmd = [
            "python", "-m", "pytest",
            str(test_dir),
            "-v",
            "--tb=short",
            "--json-report",
            "--json-report-file=/tmp/test_results.json"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Check results
        if result.returncode == 0:
            print("  ✅ All tests passed")
            passed_count += 1
        else:
            print("  ❌ Tests failed")
            failed_count += 1
            if result.stdout:
                print("\nSTDOUT:")
                print(result.stdout[-2000:])  # Last 2000 chars
            if result.stderr:
                print("\nSTDERR:")
                print(result.stderr[-2000:])  # Last 2000 chars
        
        # Try to load test results
        try:
            with open("/tmp/test_results.json", "r") as f:
                test_data = json.load(f)
                results.append({
                    "directory": str(test_dir),
                    "passed": test_data.get("summary", {}).get("passed", 0),
                    "failed": test_data.get("summary", {}).get("failed", 0),
                    "errors": test_data.get("summary", {}).get("error", 0),
                    "skipped": test_data.get("summary", {}).get("skipped", 0),
                })
        except:
            results.append({
                "directory": str(test_dir),
                "error": "Could not load test results"
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 LEVEL 0 TEST SUMMARY")
    print("=" * 60)
    print(f"Directories tested: {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    
    # Generate report
    report_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/LEVEL_0_TEST_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report_content = f"""# Level 0 Test Report

Generated: {datetime.now()}

## Summary

- **Directories Tested**: {len(results)}
- **Passed**: {passed_count}
- **Failed**: {failed_count}

## Detailed Results

"""
    
    for result in results:
        report_content += f"### {result['directory']}\n\n"
        if "error" in result:
            report_content += f"Error: {result['error']}\n\n"
        else:
            report_content += f"- Passed: {result.get('passed', 0)}\n"
            report_content += f"- Failed: {result.get('failed', 0)}\n"
            report_content += f"- Errors: {result.get('errors', 0)}\n"
            report_content += f"- Skipped: {result.get('skipped', 0)}\n\n"
    
    report_path.write_text(report_content)
    print(f"\n📄 Report generated: {report_path}")
    
    return failed_count == 0


if __name__ == "__main__":
    success = run_level_0_tests()
    sys.exit(0 if success else 1)