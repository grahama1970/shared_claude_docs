#!/usr/bin/env python3
"""
Module: run_tests_exclude_honeypots.py
Description: Run tests excluding honeypot tests which are designed to fail

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python run_tests_exclude_honeypots.py
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
    """Run tests for a project excluding honeypot tests."""
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
    
    # Run tests excluding honeypot
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
        f'python -m pytest -v --tb=short -m "not honeypot" --json-report --json-report-file=test-report.json 2>&1'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # Try to read JSON report
        json_report_path = project_path / "test-report.json"
        if json_report_path.exists():
            try:
                with open(json_report_path) as f:
                    report_data = json.load(f)
                
                summary = report_data.get("summary", {})
                
                # Clean up
                json_report_path.unlink()
                
                # Count collection errors
                errors = 0
                if "collectors" in report_data:
                    for collector in report_data["collectors"]:
                        if collector.get("outcome") == "error":
                            errors += 1
                
                return {
                    "project": project_name,
                    "status": "passed" if result.returncode == 0 and errors == 0 else "failed",
                    "tests": {
                        "total": summary.get("collected", 0) - summary.get("deselected", 0),
                        "passed": summary.get("passed", 0),
                        "failed": summary.get("failed", 0),
                        "skipped": summary.get("skipped", 0),
                        "error": summary.get("error", 0),
                        "deselected": summary.get("deselected", 0),
                        "collection_errors": errors
                    },
                    "duration": report_data.get("duration", 0),
                    "output": result.stdout if result.returncode != 0 or errors > 0 else None
                }
            except Exception as e:
                print(f"Error reading JSON report for {project_name}: {e}")
        
        # Fallback parsing
        output = result.stdout + result.stderr
        
        # Check for collection errors
        if "error during collection" in output.lower() or "errors during collection" in output.lower():
            import re
            error_count = len(re.findall(r'ERROR\s+tests/', output))
            
            return {
                "project": project_name,
                "status": "collection_error",
                "error": f"{error_count} collection errors",
                "output": output
            }
        
        return {
            "project": project_name,
            "status": "passed" if result.returncode == 0 else "failed",
            "output": output
        }
        
    except subprocess.TimeoutExpired:
        return {
            "project": project_name,
            "status": "timeout",
            "error": "Test execution timed out"
        }
    except Exception as e:
        return {
            "project": project_name,
            "status": "error",
            "error": str(e)
        }


def main():
    """Run tests for all projects excluding honeypots."""
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
    
    print("🧪 Running Tests (Excluding Honeypots)")
    print("=" * 60)
    print("Honeypot tests are designed to fail and will be skipped.\n")
    
    all_pass = True
    results = []
    
    for project_name, project_path in projects:
        print(f"📦 {project_name}...", end="", flush=True)
        result = run_project_tests(project_name, project_path)
        results.append(result)
        
        status = result["status"]
        if status == "passed":
            tests = result.get("tests", {})
            print(f" ✅ ({tests.get('passed', 0)} tests)")
        elif status == "collection_error":
            print(f" ❌ (collection errors)")
            all_pass = False
        elif status == "no_venv":
            print(f" 📦 (no venv)")
        elif status == "not_found":
            print(f" ❓ (not found)")
        else:
            print(f" ❌ ({status})")
            all_pass = False
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/TEST_RESULTS_{timestamp}.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Report saved to: {report_path}")
    
    # Summary
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] in ["failed", "collection_error"])
    other = len(results) - passed - failed
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  📦 Other: {other}")
    print(f"{'='*60}")
    
    if all_pass:
        print("\n✅ All tests passing! Ready for level 0-4 interaction testing.")
    else:
        print("\n❌ Some tests are still failing. Fix these before proceeding.")
    
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())