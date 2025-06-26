#!/usr/bin/env python3
"""
Module: run_all_granger_tests.py
Description: Run tests for all Granger projects with proper error handling

External Dependencies:
- pytest: https://docs.pytest.org/
- loguru: https://loguru.readthedocs.io/

Example Usage:
>>> python run_all_granger_tests.py
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import os

from loguru import logger


class GrangerTestRunner:
    """Run tests for all Granger projects."""
    
    def __init__(self):
        self.projects = [
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
        
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def check_services(self):
        """Check if required services are running."""
        print("\n🔍 Checking Required Services")
        print("=" * 60)
        
        services = {
            "ArangoDB": ("http://localhost:8529", "curl -s http://localhost:8529/_api/version"),
            "GrangerHub": ("http://localhost:8000", "curl -s http://localhost:8000/health"),
        }
        
        all_running = True
        for service, (url, check_cmd) in services.items():
            result = subprocess.run(check_cmd, shell=True, capture_output=True)
            if result.returncode == 0:
                print(f"✅ {service} is running at {url}")
            else:
                print(f"❌ {service} is NOT running at {url}")
                all_running = False
        
        if not all_running:
            print("\n⚠️  Start missing services with:")
            print("  bash scripts/start_granger_services.sh")
        
        return all_running

    def fix_common_issues(self, project_path: Path):
        """Fix common issues before running tests."""
        fixes = []
        
        # 1. Fix __future__ imports in site-packages
        venv_path = project_path / ".venv"
        if venv_path.exists():
            # Fix PIL/packaging issues
            problem_files = [
                venv_path / "lib/python3.10/site-packages/PIL/ExifTags.py",
                venv_path / "lib/python3.10/site-packages/packaging/version.py",
                venv_path / "lib/python3.10/site-packages/pytest/__init__.py",
                venv_path / "lib/python3.10/site-packages/allure_pytest/plugin.py",
            ]
            
            for pf in problem_files:
                if pf.exists():
                    try:
                        content = pf.read_text()
                        if "from __future__" in content and not content.strip().startswith("from __future__"):
                            # Move __future__ imports to the top
                            lines = content.split('\n')
                            future_imports = []
                            other_lines = []
                            
                            for line in lines:
                                if line.strip().startswith('from __future__'):
                                    future_imports.append(line)
                                else:
                                    other_lines.append(line)
                            
                            if future_imports:
                                new_content = '\n'.join(future_imports) + '\n' + '\n'.join(other_lines)
                                pf.write_text(new_content)
                                fixes.append(f"Fixed __future__ import in {pf.name}")
                    except Exception as e:
                        logger.debug(f"Could not fix {pf}: {e}")
        
        # 2. Ensure pytest.ini exists with honeypot marker
        pytest_ini = project_path / "pytest.ini"
        if not pytest_ini.exists():
            pytest_ini.write_text("""[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    honeypot: Tests designed to detect mocking (should fail if mocks are used)
    integration: Integration tests requiring real services
    unit: Unit tests
""")
            fixes.append("Created pytest.ini with markers")
        
        return fixes

    def run_project_tests(self, project_name: str, project_path: str) -> Dict:
        """Run tests for a single project."""
        project_path = Path(project_path)
        
        if not project_path.exists():
            return {
                "project": project_name,
                "status": "missing",
                "error": "Project directory not found"
            }
        
        print(f"\n📦 Testing {project_name}")
        print("-" * 40)
        
        # Fix common issues first
        fixes = self.fix_common_issues(project_path)
        if fixes:
            for fix in fixes:
                print(f"  🔧 {fix}")
        
        # Run tests
        cmd = [
            'bash', '-c',
            f'cd {project_path} && source .venv/bin/activate && '
            f'python -m pytest -xvs --tb=short -m "not honeypot" --json-report --json-report-file=test_report.json 2>&1'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Parse results
            test_report_path = project_path / "test_report.json"
            if test_report_path.exists():
                with open(test_report_path) as f:
                    report = json.load(f)
                
                summary = report.get('summary', {})
                
                return {
                    "project": project_name,
                    "status": "passed" if summary.get('failed', 0) == 0 and summary.get('error', 0) == 0 else "failed",
                    "passed": summary.get('passed', 0),
                    "failed": summary.get('failed', 0),
                    "errors": summary.get('error', 0),
                    "total": summary.get('total', 0),
                    "duration": report.get('duration', 0),
                    "output": result.stdout[-1000:] if result.stdout else result.stderr[-1000:]
                }
            else:
                # No JSON report, parse output
                output = result.stdout + result.stderr
                
                if "collected 0 items" in output:
                    return {
                        "project": project_name,
                        "status": "no_tests",
                        "total": 0,
                        "output": output[-1000:]
                    }
                
                # Try to extract test counts from output
                import re
                passed_match = re.search(r'(\d+) passed', output)
                failed_match = re.search(r'(\d+) failed', output)
                error_match = re.search(r'(\d+) error', output)
                
                passed = int(passed_match.group(1)) if passed_match else 0
                failed = int(failed_match.group(1)) if failed_match else 0
                errors = int(error_match.group(1)) if error_match else 0
                
                return {
                    "project": project_name,
                    "status": "passed" if failed == 0 and errors == 0 and passed > 0 else "failed",
                    "passed": passed,
                    "failed": failed,
                    "errors": errors,
                    "total": passed + failed,
                    "output": output[-1000:]
                }
                
        except subprocess.TimeoutExpired:
            return {
                "project": project_name,
                "status": "timeout",
                "error": "Tests timed out after 60 seconds"
            }
        except Exception as e:
            return {
                "project": project_name,
                "status": "error",
                "error": str(e)
            }

    def generate_report(self):
        """Generate a comprehensive test report."""
        report_path = Path(f"docs/05_validation/test_reports/GRANGER_TEST_REPORT_{self.timestamp}.md")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Count results
        passed_projects = [r for r in self.results if r.get('status') == 'passed']
        failed_projects = [r for r in self.results if r.get('status') == 'failed']
        no_test_projects = [r for r in self.results if r.get('status') == 'no_tests']
        error_projects = [r for r in self.results if r.get('status') in ['error', 'timeout', 'missing']]
        
        content = f"""# Granger Ecosystem Test Report
Generated: {datetime.now().isoformat()}

## Summary

- **Total Projects**: {len(self.results)}
- **Passed**: {len(passed_projects)} ✅
- **Failed**: {len(failed_projects)} ❌
- **No Tests**: {len(no_test_projects)} ⚠️
- **Errors**: {len(error_projects)} 🚨

## Detailed Results

| Project | Status | Tests | Passed | Failed | Errors | Duration |
|---------|--------|-------|--------|--------|--------|----------|
"""
        
        for result in self.results:
            status_icon = {
                'passed': '✅',
                'failed': '❌',
                'no_tests': '⚠️',
                'error': '🚨',
                'timeout': '⏱️',
                'missing': '❓'
            }.get(result.get('status', 'unknown'), '❓')
            
            total = result.get('total', 0)
            passed = result.get('passed', 0)
            failed = result.get('failed', 0)
            errors = result.get('errors', 0)
            duration = result.get('duration', 0)
            
            content += f"| {result['project']} | {status_icon} {result.get('status', 'unknown')} | "
            content += f"{total} | {passed} | {failed} | {errors} | {duration:.2f}s |\n"
        
        # Add critical issues section
        content += "\n## Critical Issues\n\n"
        
        for result in error_projects + failed_projects:
            content += f"### {result['project']}\n\n"
            if 'error' in result:
                content += f"**Error**: {result['error']}\n\n"
            if 'output' in result:
                content += "**Output**:\n```\n"
                content += result['output'][-500:]  # Last 500 chars
                content += "\n```\n\n"
        
        # Add recommendations
        content += "\n## Recommendations\n\n"
        
        if len(passed_projects) < 10:
            content += "1. **Critical**: Less than half of projects have passing tests\n"
            content += "2. Fix syntax errors and import issues in failing projects\n"
            content += "3. Ensure all required services are running\n"
            content += "4. Install missing dependencies\n\n"
        
        if no_test_projects:
            content += f"- {len(no_test_projects)} projects have no tests - add basic tests\n"
        
        content += "\n## Next Steps\n\n"
        
        if len(passed_projects) == len(self.results):
            content += "✅ All projects passing! Ready for Level 0-4 interaction testing.\n"
        else:
            content += "❌ Fix failing tests before proceeding to interaction testing.\n"
        
        report_path.write_text(content)
        
        # Also save JSON report
        json_path = report_path.with_suffix('.json')
        with open(json_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return report_path

    def run_all_tests(self):
        """Run tests for all projects."""
        print("🚀 Granger Ecosystem Test Runner")
        print("=" * 60)
        
        # Check services
        services_ok = self.check_services()
        if not services_ok:
            print("\n⚠️  Warning: Some services are not running. Tests may fail.")
        
        # Run tests for each project
        for project_name, project_path in self.projects:
            result = self.run_project_tests(project_name, project_path)
            self.results.append(result)
            
            # Quick summary
            if result['status'] == 'passed':
                print(f"  ✅ {result['passed']} tests passed")
            elif result['status'] == 'failed':
                print(f"  ❌ {result['failed']} failed, {result['errors']} errors")
            elif result['status'] == 'no_tests':
                print(f"  ⚠️  No tests found")
            else:
                print(f"  🚨 {result.get('error', 'Unknown error')}")
        
        # Generate report
        report_path = self.generate_report()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 FINAL SUMMARY")
        print("=" * 60)
        
        passed_projects = [r for r in self.results if r.get('status') == 'passed']
        print(f"Passed: {len(passed_projects)}/{len(self.results)} projects")
        
        if len(passed_projects) < len(self.results):
            print("\n❌ Not all projects are passing. Fix issues before Level 0-4 testing.")
            return 1
        else:
            print("\n✅ All projects passing! Ready for Level 0-4 interaction testing.")
            return 0


def main():
    """Run all Granger tests."""
    runner = GrangerTestRunner()
    return runner.run_all_tests()


if __name__ == "__main__":
    sys.exit(main())