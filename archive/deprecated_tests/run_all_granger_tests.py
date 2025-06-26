#!/usr/bin/env python3
"""
Module: run_all_granger_tests.py
Description: Systematically run tests for all Granger projects from Level 0 to Level 4

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python run_all_granger_tests.py
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
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def get_all_granger_projects():
    """Get all Granger projects from the official registry."""
    projects = [
        # Core Infrastructure
        {"name": "granger_hub", "path": "/home/graham/workspace/experiments/granger_hub", "type": "hub"},
        {"name": "rl_commons", "path": "/home/graham/workspace/experiments/rl_commons", "type": "core"},
        {"name": "world_model", "path": "/home/graham/workspace/experiments/world_model", "type": "core"},
        {"name": "claude-test-reporter", "path": "/home/graham/workspace/experiments/claude-test-reporter", "type": "core"},
        {"name": "shared_claude_docs", "path": "/home/graham/workspace/shared_claude_docs", "type": "docs"},
        {"name": "granger-ui", "path": "/home/graham/workspace/granger-ui", "type": "ui"},
        
        # Processing Spokes
        {"name": "sparta", "path": "/home/graham/workspace/experiments/sparta", "type": "spoke"},
        {"name": "marker", "path": "/home/graham/workspace/experiments/marker", "type": "spoke"},
        {"name": "arangodb", "path": "/home/graham/workspace/experiments/arangodb", "type": "spoke"},
        {"name": "llm_call", "path": "/home/graham/workspace/experiments/llm_call", "type": "spoke"},
        {"name": "unsloth_wip", "path": "/home/graham/workspace/experiments/unsloth_wip", "type": "spoke"},
        {"name": "youtube_transcripts", "path": "/home/graham/workspace/experiments/youtube_transcripts", "type": "spoke"},
        {"name": "darpa_crawl", "path": "/home/graham/workspace/experiments/darpa_crawl", "type": "spoke"},
        {"name": "gitget", "path": "/home/graham/workspace/experiments/gitget", "type": "spoke"},
        
        # MCP Services
        {"name": "arxiv-mcp-server", "path": "/home/graham/workspace/mcp-servers/arxiv-mcp-server", "type": "mcp"},
        {"name": "mcp-screenshot", "path": "/home/graham/workspace/experiments/mcp-screenshot", "type": "mcp"},
        
        # User Interfaces
        {"name": "chat", "path": "/home/graham/workspace/experiments/chat", "type": "ui"},
        {"name": "annotator", "path": "/home/graham/workspace/experiments/annotator", "type": "ui"},
        {"name": "aider-daemon", "path": "/home/graham/workspace/experiments/aider-daemon", "type": "ui"},
        
        # Infrastructure
        {"name": "runpod_ops", "path": "/home/graham/workspace/experiments/runpod_ops", "type": "infra"},
    ]
    return projects


def check_services():
    """Check if required services are running."""
    services = {
        "ArangoDB": ("localhost", 8529),
        "GrangerHub": ("localhost", 8000),
    }
    
    results = {}
    for service, (host, port) in services.items():
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            results[service] = result == 0
        except:
            results[service] = False
    
    return results


def run_project_tests(project, level=None):
    """Run tests for a specific project and optional level."""
    project_path = Path(project["path"])
    
    if not project_path.exists():
        return {
            "project": project["name"],
            "status": "not_found",
            "error": f"Project path does not exist: {project_path}",
            "duration": 0
        }
    
    # Check for venv
    venv_path = project_path / ".venv"
    if not venv_path.exists():
        return {
            "project": project["name"],
            "status": "no_venv",
            "error": "No virtual environment found",
            "duration": 0
        }
    
    # Build test command
    test_cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
    ]
    
    if level is not None:
        # Run specific level tests
        test_patterns = []
        
        # Check for level tests in different locations
        level_dirs = [
            f"tests/level_{level}",
            f"tests/level{level}",
            f"tests/**/level_{level}",
            f"scenarios/level_{level}*.py",
            f"level_{level}_tests",
        ]
        
        for pattern in level_dirs:
            test_patterns.append(f'"{pattern}"')
        
        # Also look for test files with level in name
        test_patterns.extend([
            f'"tests/*level*{level}*.py"',
            f'"tests/**/*level*{level}*.py"',
            f'"**/test_level_{level}_*.py"',
        ])
        
        # Build pytest command with all patterns
        pytest_cmd = f'pytest -v --tb=short {" ".join(test_patterns)} 2>&1'
    else:
        # Run all tests
        pytest_cmd = 'pytest -v --tb=short 2>&1'
    
    test_cmd[2] += pytest_cmd
    
    # Run tests
    start_time = time.time()
    try:
        result = subprocess.run(
            test_cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        duration = time.time() - start_time
        
        return {
            "project": project["name"],
            "level": level,
            "status": "passed" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "duration": duration,
            "output": result.stdout + result.stderr,
            "tests_collected": extract_test_count(result.stdout)
        }
    except subprocess.TimeoutExpired:
        return {
            "project": project["name"],
            "level": level,
            "status": "timeout",
            "error": "Test execution timed out after 5 minutes",
            "duration": 300
        }
    except Exception as e:
        return {
            "project": project["name"],
            "level": level,
            "status": "error",
            "error": str(e),
            "duration": time.time() - start_time
        }


def extract_test_count(output):
    """Extract test count from pytest output."""
    import re
    
    # Look for patterns like "collected 5 items"
    match = re.search(r'collected (\d+) items?', output)
    if match:
        return int(match.group(1))
    
    # Look for "no tests ran"
    if "no tests ran" in output:
        return 0
    
    return None


def generate_report(results):
    """Generate comprehensive test report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(f"/home/graham/workspace/shared_claude_docs/docs/05_validation/test_reports/GRANGER_ALL_TESTS_{timestamp}.md")
    
    # Group results by level
    by_level = defaultdict(list)
    for result in results:
        level = result.get("level", "all")
        by_level[level].append(result)
    
    content = f"""# Granger Ecosystem Test Report

**Generated**: {datetime.now()}
**Total Projects**: {len(get_all_granger_projects())}
**Tests Run**: {len(results)}

## 📊 Summary

| Level | Total | Passed | Failed | Errors | Not Found |
|-------|-------|--------|--------|--------|-----------|
"""
    
    for level in sorted(by_level.keys()):
        level_results = by_level[level]
        passed = sum(1 for r in level_results if r.get("status") == "passed")
        failed = sum(1 for r in level_results if r.get("status") == "failed")
        errors = sum(1 for r in level_results if r.get("status") in ["error", "timeout", "no_venv"])
        not_found = sum(1 for r in level_results if r.get("status") == "not_found")
        
        level_str = f"Level {level}" if level != "all" else "All Tests"
        content += f"| {level_str} | {len(level_results)} | {passed} | {failed} | {errors} | {not_found} |\n"
    
    content += "\n## 🔍 Detailed Results\n\n"
    
    for level in sorted(by_level.keys()):
        level_str = f"Level {level}" if level != "all" else "All Tests"
        content += f"### {level_str}\n\n"
        
        for result in by_level[level]:
            status_icon = {
                "passed": "✅",
                "failed": "❌",
                "error": "🔥",
                "timeout": "⏱️",
                "not_found": "❓",
                "no_venv": "📦"
            }.get(result["status"], "❓")
            
            content += f"#### {status_icon} {result['project']}\n"
            content += f"- **Status**: {result['status']}\n"
            content += f"- **Duration**: {result.get('duration', 0):.2f}s\n"
            
            if result.get("tests_collected") is not None:
                content += f"- **Tests Collected**: {result['tests_collected']}\n"
            
            if result.get("error"):
                content += f"- **Error**: {result['error']}\n"
            
            if result.get("output") and result["status"] == "failed":
                # Show last 20 lines of output for failed tests
                lines = result["output"].strip().split('\n')
                if len(lines) > 20:
                    content += "\n<details>\n<summary>Test Output (last 20 lines)</summary>\n\n```\n"
                    content += '\n'.join(lines[-20:])
                    content += "\n```\n</details>\n"
                else:
                    content += f"\n```\n{result['output']}\n```\n"
            
            content += "\n"
    
    content += """
## 🚨 Action Items

1. **Fix failing tests** - Address all ❌ failed tests
2. **Setup missing projects** - Create venvs for 📦 projects
3. **Remove mocks** - Ensure all tests use real connections
4. **Add missing level tests** - Some projects may lack level-specific tests

## 📋 Next Steps

1. Fix all failing tests starting with Level 0
2. Ensure all projects have proper test structure
3. Implement missing level tests where needed
4. Run comprehensive verification with all levels passing
"""
    
    # Write report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content)
    
    return report_path


def main():
    """Run all Granger tests systematically."""
    print("🧪 Granger Ecosystem Comprehensive Test Runner")
    print("=" * 60)
    
    # Check services
    print("\n📡 Checking Required Services...")
    services = check_services()
    for service, running in services.items():
        status = "✅ Running" if running else "❌ Not Running"
        print(f"  {service}: {status}")
    
    if not all(services.values()):
        print("\n⚠️  WARNING: Some required services are not running!")
        print("Tests may fail without proper services.")
    
    # Get all projects
    projects = get_all_granger_projects()
    print(f"\n📦 Found {len(projects)} Granger projects")
    
    # Test strategy: Run tests for each level
    levels = [0, 1, 2, 3, 4]
    all_results = []
    
    print("\n🔄 Running tests by level...")
    
    for level in levels:
        print(f"\n{'='*60}")
        print(f"Testing Level {level}")
        print(f"{'='*60}")
        
        level_results = []
        for project in projects:
            print(f"\n📁 {project['name']} (Level {level})...")
            result = run_project_tests(project, level=level)
            level_results.append(result)
            
            # Quick summary
            if result["status"] == "passed":
                print(f"  ✅ Passed ({result.get('tests_collected', '?')} tests)")
            elif result["status"] == "failed":
                print(f"  ❌ Failed")
            else:
                print(f"  🔥 {result['status']}: {result.get('error', 'Unknown error')}")
        
        all_results.extend(level_results)
        
        # Level summary
        passed = sum(1 for r in level_results if r["status"] == "passed")
        total = len(level_results)
        print(f"\n📊 Level {level} Summary: {passed}/{total} projects passed")
    
    # Also run all tests for each project (not level-specific)
    print(f"\n{'='*60}")
    print("Running All Tests (not level-specific)")
    print(f"{'='*60}")
    
    for project in projects:
        print(f"\n📁 {project['name']} (All tests)...")
        result = run_project_tests(project, level=None)
        all_results.append(result)
        
        if result["status"] == "passed":
            print(f"  ✅ Passed ({result.get('tests_collected', '?')} tests)")
        elif result["status"] == "failed":
            print(f"  ❌ Failed")
        else:
            print(f"  🔥 {result['status']}: {result.get('error', 'Unknown error')}")
    
    # Generate report
    print("\n📝 Generating comprehensive report...")
    report_path = generate_report(all_results)
    print(f"✅ Report saved to: {report_path}")
    
    # Final summary
    total_passed = sum(1 for r in all_results if r["status"] == "passed")
    total_tests = len(all_results)
    
    print(f"\n{'='*60}")
    print(f"🏁 Final Summary: {total_passed}/{total_tests} test runs passed")
    print(f"{'='*60}")
    
    return 0 if total_passed == total_tests else 1


if __name__ == "__main__":
    # sys.exit() removed)