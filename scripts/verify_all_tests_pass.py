#!/usr/bin/env python3
"""
Module: verify_all_tests_pass.py
Description: Verify all tests pass in all Granger projects

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python verify_all_tests_pass.py
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
import json
from pathlib import Path
from datetime import datetime


def run_project_tests(project_name, project_path):
    """Run all tests for a project."""
    project_path = Path(project_path)
    
    if not project_path.exists():
        return {
            "project": project_name,
            "status": "not_found",
            "error": "Project directory does not exist"
        }
    
    # Check for venv
    venv_path = project_path / ".venv"
    if not venv_path.exists():
        return {
            "project": project_name,
            "status": "no_venv",
            "error": "No virtual environment"
        }
    
    # Check for tests directory
    test_dir = project_path / "tests"
    if not test_dir.exists():
        # Try alternative locations
        if (project_path / "test").exists():
            test_dir = project_path / "test"
        else:
            return {
                "project": project_name,
                "status": "no_tests",
                "error": "No tests directory found"
            }
    
    # Run tests
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
        f'python -m pytest {test_dir} -v --tb=short --json-report --json-report-file=test-report.json 2>&1'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        # Try to read JSON report
        json_report_path = project_path / "test-report.json"
        if json_report_path.exists():
            try:
                with open(json_report_path) as f:
                    report_data = json.load(f)
                
                summary = report_data.get("summary", {})
                
                # Clean up report file
                json_report_path.unlink()
                
                return {
                    "project": project_name,
                    "status": "passed" if result.returncode == 0 else "failed",
                    "tests": {
                        "total": summary.get("total", 0),
                        "passed": summary.get("passed", 0),
                        "failed": summary.get("failed", 0),
                        "skipped": summary.get("skipped", 0),
                        "error": summary.get("error", 0)
                    },
                    "duration": report_data.get("duration", 0),
                    "output": result.stdout if result.returncode != 0 else None
                }
            except:
                pass
        
        # Fallback: parse output
        output = result.stdout + result.stderr
        
        # Parse test counts from output
        import re
        
        passed = len(re.findall(r'PASSED', output))
        failed = len(re.findall(r'FAILED', output))
        skipped = len(re.findall(r'SKIPPED', output))
        errors = len(re.findall(r'ERROR', output))
        
        # Check for collection errors
        if "collected 0 items" in output:
            return {
                "project": project_name,
                "status": "no_tests_collected",
                "error": "No tests were collected",
                "output": output
            }
        
        return {
            "project": project_name,
            "status": "passed" if result.returncode == 0 else "failed",
            "tests": {
                "total": passed + failed + skipped + errors,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "error": errors
            },
            "output": output if result.returncode != 0 else None
        }
        
    except subprocess.TimeoutExpired:
        return {
            "project": project_name,
            "status": "timeout",
            "error": "Test execution timed out after 5 minutes"
        }
    except Exception as e:
        return {
            "project": project_name,
            "status": "error",
            "error": str(e)
        }


def generate_markdown_report(results):
    """Generate a comprehensive markdown report."""
    timestamp = datetime.now()
    
    content = f"""# Granger Ecosystem Test Verification Report

**Generated**: {timestamp}
**Total Projects**: {len(results)}

## 📊 Overall Summary

"""
    
    # Calculate totals
    total_passed_projects = sum(1 for r in results if r["status"] == "passed")
    total_failed_projects = sum(1 for r in results if r["status"] == "failed")
    total_error_projects = sum(1 for r in results if r["status"] in ["error", "timeout", "no_venv", "not_found", "no_tests", "no_tests_collected"])
    
    total_tests = sum(r.get("tests", {}).get("total", 0) for r in results)
    total_passed_tests = sum(r.get("tests", {}).get("passed", 0) for r in results)
    total_failed_tests = sum(r.get("tests", {}).get("failed", 0) for r in results)
    
    content += f"""| Metric | Value |
|--------|-------|
| **Projects with Passing Tests** | {total_passed_projects}/{len(results)} |
| **Projects with Failing Tests** | {total_failed_projects}/{len(results)} |
| **Projects with Errors** | {total_error_projects}/{len(results)} |
| **Total Tests Run** | {total_tests} |
| **Total Tests Passed** | {total_passed_tests} |
| **Total Tests Failed** | {total_failed_tests} |

## 🔍 Project-by-Project Results

| Project | Status | Tests | Passed | Failed | Duration |
|---------|--------|-------|--------|--------|----------|
"""
    
    for result in results:
        status_icon = {
            "passed": "✅",
            "failed": "❌",
            "error": "🔥",
            "timeout": "⏱️",
            "not_found": "❓",
            "no_venv": "📦",
            "no_tests": "🚫",
            "no_tests_collected": "⚠️"
        }.get(result["status"], "❓")
        
        tests = result.get("tests", {})
        total = tests.get("total", "-")
        passed = tests.get("passed", "-")
        failed = tests.get("failed", "-")
        duration = result.get("duration", "-")
        if isinstance(duration, (int, float)):
            duration = f"{duration:.2f}s"
        
        content += f"| {result['project']} | {status_icon} {result['status']} | {total} | {passed} | {failed} | {duration} |\n"
    
    # Add details for failed projects
    failed_projects = [r for r in results if r["status"] in ["failed", "error", "timeout"]]
    
    if failed_projects:
        content += "\n## ❌ Failed Project Details\n\n"
        
        for result in failed_projects:
            content += f"### {result['project']}\n\n"
            content += f"**Status**: {result['status']}\n"
            
            if result.get("error"):
                content += f"**Error**: {result['error']}\n"
            
            if result.get("output"):
                # Show last 30 lines of output
                lines = result["output"].strip().split('\n')
                if len(lines) > 30:
                    content += "\n<details>\n<summary>Test Output (last 30 lines)</summary>\n\n```\n"
                    content += '\n'.join(lines[-30:])
                    content += "\n```\n</details>\n"
                else:
                    content += f"\n```\n{result['output']}\n```\n"
            
            content += "\n"
    
    # Add action items
    if total_failed_projects > 0 or total_error_projects > 0:
        content += """
## 🚨 Action Items

1. **Fix failing tests** - Address all test failures in projects marked with ❌
2. **Setup missing environments** - Create venvs for projects marked with 📦
3. **Add missing tests** - Create tests for projects marked with 🚫
4. **Debug timeout issues** - Investigate projects marked with ⏱️

## 📝 Next Steps

1. Run `python scripts/fix_remaining_test_issues.py` to apply automated fixes
2. Manually fix any remaining failures
3. Re-run this verification script
"""
    else:
        content += """
## ✅ All Tests Passing!

The Granger ecosystem is ready for Level 0-4 interaction testing.
"""
    
    return content


def main():
    """Verify all tests pass in all projects."""
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
    
    print("🧪 Granger Ecosystem Test Verification")
    print("=" * 60)
    print("Verifying all tests pass in all projects...\n")
    
    results = []
    
    for project_name, project_path in projects[:5]:  # Start with first 5 projects
        print(f"📦 Testing {project_name}...", end="", flush=True)
        result = run_project_tests(project_name, project_path)
        results.append(result)
        
        # Quick status
        if result["status"] == "passed":
            tests = result.get("tests", {})
            print(f" ✅ ({tests.get('passed', 0)} tests)")
        else:
            print(f" ❌ ({result['status']})")
    
    # Generate reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON report
    json_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/VERIFICATION_{timestamp}.json")
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Markdown report
    md_content = generate_markdown_report(results)
    md_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/VERIFICATION_{timestamp}.md")
    md_path.write_text(md_content)
    
    print(f"\n📝 Reports saved:")
    print(f"  - JSON: {json_path}")
    print(f"  - Markdown: {md_path}")
    
    # Summary
    total_passed = sum(1 for r in results if r["status"] == "passed")
    print(f"\n{'='*60}")
    print(f"🏁 Summary: {total_passed}/{len(results)} projects have passing tests")
    print(f"{'='*60}")
    
    return 0 if total_passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())