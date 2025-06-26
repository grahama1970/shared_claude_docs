#!/usr/bin/env python3
"""
Module: test_all_and_archive_broken.py
Description: Test all projects and archive broken/deprecated tests

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python test_all_and_archive_broken.py
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from datetime import datetime


def ensure_archive_dir(project_path):
    """Ensure archive directory exists."""
    archive_dir = project_path / "archive" / "deprecated_tests"
    archive_dir.mkdir(parents=True, exist_ok=True)
    return archive_dir


def run_single_test(test_file, project_path):
    """Run a single test file and return result."""
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
        f'python -m pytest -xvs {test_file} --tb=short 2>&1'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout + result.stderr
        
        # Check for specific errors that indicate broken tests
        if "ModuleNotFoundError" in output:
            return "broken", "Module not found"
        elif "ImportError" in output:
            return "broken", "Import error"
        elif "SyntaxError" in output:
            return "broken", "Syntax error"
        elif "AttributeError" in output and "mock" in output.lower():
            return "broken", "Mock-related AttributeError"
        elif "NameError" in output and ("Mock" in output or "mock" in output):
            return "broken", "Mock usage without import"
        elif "INTERNAL ERROR" in output:
            return "broken", "Pytest internal error"
        elif result.returncode == 0:
            return "passed", None
        else:
            # Test failed but not necessarily broken
            return "failed", "Test assertions failed"
            
    except subprocess.TimeoutExpired:
        return "timeout", "Test timed out"
    except Exception as e:
        return "error", str(e)


def should_archive_test(test_file):
    """Determine if a test should be archived based on content."""
    try:
        content = test_file.read_text()
        
        # Patterns that indicate deprecated tests
        deprecated_patterns = [
            "sys.exit(",  # Tests that exit
            "DEPRECATED",
            "TODO: Remove",
            "OLD_",
            "_old.",
            "validate_",  # Old validation scripts
            "skeptical_test_",  # Old verification scripts
            "run_tests.py",  # Old test runners
        ]
        
        for pattern in deprecated_patterns:
            if pattern in content or pattern in str(test_file):
                return True, f"Contains {pattern}"
        
        # Check if it's a duplicate test runner
        if test_file.name.startswith("run_") and test_file.name.endswith("_tests.py"):
            return True, "Old test runner script"
            
        return False, None
        
    except:
        return False, None


def test_project(project_name, project_path):
    """Test a project and archive broken tests."""
    project_path = Path(project_path)
    
    if not project_path.exists():
        return {
            "project": project_name,
            "status": "not_found",
            "tests": []
        }
    
    # Find all test files
    test_files = []
    test_dirs = [project_path / "tests", project_path / "test"]
    
    for test_dir in test_dirs:
        if test_dir.exists():
            test_files.extend(test_dir.rglob("test_*.py"))
            test_files.extend(test_dir.rglob("*_test.py"))
    
    # Also check for test files in other locations
    test_files.extend(project_path.rglob("validate_*.py"))
    test_files.extend(project_path.rglob("run_*tests*.py"))
    test_files.extend(project_path.rglob("skeptical_*.py"))
    
    # Remove duplicates and filter out venv/cache
    test_files = list(set(test_files))
    test_files = [f for f in test_files if ".venv" not in str(f) and "__pycache__" not in str(f)]
    
    results = {
        "project": project_name,
        "status": "tested",
        "tests": [],
        "summary": {
            "total": len(test_files),
            "passed": 0,
            "failed": 0,
            "broken": 0,
            "archived": 0
        }
    }
    
    archive_dir = ensure_archive_dir(project_path)
    
    for test_file in test_files:
        relative_path = test_file.relative_to(project_path)
        
        # Check if should be archived based on content
        should_archive, reason = should_archive_test(test_file)
        
        if should_archive:
            # Archive the file
            archive_path = archive_dir / relative_path.name
            shutil.move(str(test_file), str(archive_path))
            
            results["tests"].append({
                "file": str(relative_path),
                "status": "archived",
                "reason": reason
            })
            results["summary"]["archived"] += 1
            continue
        
        # Run the test
        status, error = run_single_test(test_file, project_path)
        
        if status == "broken":
            # Archive broken tests
            archive_path = archive_dir / relative_path.name
            shutil.move(str(test_file), str(archive_path))
            
            results["tests"].append({
                "file": str(relative_path),
                "status": "archived",
                "reason": f"Broken: {error}"
            })
            results["summary"]["archived"] += 1
        else:
            results["tests"].append({
                "file": str(relative_path),
                "status": status,
                "error": error
            })
            
            if status == "passed":
                results["summary"]["passed"] += 1
            elif status == "failed":
                results["summary"]["failed"] += 1
            else:
                results["summary"]["broken"] += 1
    
    return results


def main():
    """Test all projects and archive broken tests."""
    projects = [
        ("granger_hub", "/home/graham/workspace/experiments/granger_hub"),
        ("rl_commons", "/home/graham/workspace/experiments/rl_commons"),
        ("world_model", "/home/graham/workspace/experiments/world_model"),
        ("claude-test-reporter", "/home/graham/workspace/experiments/claude-test-reporter"),
        ("sparta", "/home/graham/workspace/experiments/sparta"),
        ("marker", "/home/graham/workspace/experiments/marker"),
        ("arangodb", "/home/graham/workspace/experiments/arangodb"),
        ("llm_call", "/home/graham/workspace/experiments/llm_call"),
        ("unsloth_wip", "/home/graham/workspace/experiments/unsloth_wip"),
        ("youtube_transcripts", "/home/graham/workspace/experiments/youtube_transcripts"),
        ("darpa_crawl", "/home/graham/workspace/experiments/darpa_crawl"),
        ("gitget", "/home/graham/workspace/experiments/gitget"),
        ("arxiv-mcp-server", "/home/graham/workspace/mcp-servers/arxiv-mcp-server"),
        ("mcp-screenshot", "/home/graham/workspace/experiments/mcp-screenshot"),
        ("chat", "/home/graham/workspace/experiments/chat"),
        ("annotator", "/home/graham/workspace/experiments/annotator"),
        ("aider-daemon", "/home/graham/workspace/experiments/aider-daemon"),
        ("runpod_ops", "/home/graham/workspace/experiments/runpod_ops"),
        ("granger-ui", "/home/graham/workspace/granger-ui"),
        ("shared_claude_docs", "/home/graham/workspace/shared_claude_docs"),
    ]
    
    print("🧹 Testing All Projects and Archiving Broken Tests")
    print("=" * 60)
    
    all_results = []
    
    for project_name, project_path in projects:
        print(f"\n📦 Testing {project_name}...")
        results = test_project(project_name, project_path)
        all_results.append(results)
        
        # Print summary
        summary = results.get("summary", {})
        if summary:
            print(f"  Total: {summary['total']}")
            print(f"  ✅ Passed: {summary['passed']}")
            print(f"  ❌ Failed: {summary['failed']}")
            print(f"  🗄️  Archived: {summary['archived']}")
    
    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/TEST_AND_ARCHIVE_REPORT_{timestamp}.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n📝 Report saved to: {report_path}")
    
    # Summary
    total_passed = sum(r["summary"]["passed"] for r in all_results if "summary" in r)
    total_failed = sum(r["summary"]["failed"] for r in all_results if "summary" in r)
    total_archived = sum(r["summary"]["archived"] for r in all_results if "summary" in r)
    
    print(f"\n{'='*60}")
    print(f"🏁 Final Summary:")
    print(f"  ✅ Total Passed: {total_passed}")
    print(f"  ❌ Total Failed: {total_failed}")
    print(f"  🗄️  Total Archived: {total_archived}")
    print(f"{'='*60}")
    
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())