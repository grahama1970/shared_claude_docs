#!/usr/bin/env python3
"""
Run all project tests with claude-test-reporter
A simpler, more robust approach focused on test execution and reporting
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
from typing import Dict, List, Any, Tuple
import shutil

class TestRunner:
    """Run tests across all projects with claude-test-reporter"""
    
    def __init__(self, config_file='cleanup_config_localhost.json'):
        # Load configuration
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_dir = Path(__file__).parent / 'test_reports' / self.timestamp
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        self.results = []
        
    def run_command(self, cmd: str, cwd: Path, timeout: int = 300) -> Tuple[str, str, int]:
        """Run a command and return output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=str(cwd),
                timeout=timeout
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return '', f'Command timed out after {timeout}s', -1
        except Exception as e:
            return '', str(e), -1
    
    def check_project_setup(self, project_path: Path) -> Dict[str, Any]:
        """Check if project is set up correctly for testing"""
        checks = {
            'exists': project_path.exists(),
            'has_tests': (project_path / 'tests').exists(),
            'has_venv': (project_path / '.venv').exists() or (project_path / 'venv').exists(),
            'has_pyproject': (project_path / 'pyproject.toml').exists(),
            'test_files': []
        }
        
        if checks['has_tests']:
            # Find test files
            test_dir = project_path / 'tests'
            checks['test_files'] = list(test_dir.glob('test_*.py')) + list(test_dir.glob('*_test.py'))
        
        return checks
    
    def setup_venv_if_needed(self, project_path: Path) -> str:
        """Ensure virtual environment exists and return python path"""
        venv_path = project_path / '.venv'
        
        if not venv_path.exists():
            print(f"  Creating virtual environment...")
            stdout, stderr, returncode = self.run_command(
                'python -m venv .venv',
                project_path
            )
            if returncode != 0:
                print(f"  ❌ Failed to create venv: {stderr}")
                return 'python'
        
        # Return platform-specific python path
        if sys.platform == 'win32':
            python_path = venv_path / 'Scripts' / 'python.exe'
        else:
            python_path = venv_path / 'bin' / 'python'
        
        return str(python_path) if python_path.exists() else 'python'
    
    def install_test_dependencies(self, project_path: Path, python_cmd: str) -> bool:
        """Install test dependencies including claude-test-reporter"""
        print(f"  Installing test dependencies...")
        
        # Basic test requirements
        basic_deps = [
            'pytest>=8.0.0',
            'pytest-asyncio>=0.23.0',
            'pytest-cov>=4.1.0',
            'pytest-json-report>=1.5.0'
        ]
        
        # Install basic deps
        for dep in basic_deps:
            stdout, stderr, returncode = self.run_command(
                f'{python_cmd} -m pip install "{dep}"',
                project_path,
                timeout=120
            )
            if returncode != 0 and 'already satisfied' not in stderr:
                print(f"    ⚠️  Failed to install {dep}")
        
        # Install claude-test-reporter
        print(f"  Installing claude-test-reporter...")
        reporter_cmd = f'{python_cmd} -m pip install git+https://github.com/grahama1970/claude-test-reporter.git@main'
        stdout, stderr, returncode = self.run_command(reporter_cmd, project_path, timeout=180)
        
        if returncode == 0 or 'already satisfied' in stdout:
            print(f"  ✅ Test dependencies ready")
            return True
        else:
            print(f"  ❌ Failed to install claude-test-reporter")
            return False
    
    def run_tests(self, project_path: Path, project_name: str) -> Dict[str, Any]:
        """Run tests for a single project"""
        print(f"\n{'='*60}")
        print(f"Testing: {project_name}")
        print(f"Path: {project_path}")
        print(f"{'='*60}")
        
        result = {
            'project': project_name,
            'path': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'coverage': None,
            'errors': []
        }
        
        # Check project setup
        checks = self.check_project_setup(project_path)
        
        if not checks['exists']:
            result['status'] = 'not_found'
            result['errors'].append('Project directory not found')
            print(f"❌ Project not found")
            return result
        
        if not checks['has_tests']:
            result['status'] = 'no_tests'
            result['errors'].append('No tests directory found')
            print(f"⚠️  No tests directory")
            return result
        
        if not checks['test_files']:
            result['status'] = 'no_test_files'
            result['errors'].append('No test files found in tests directory')
            print(f"⚠️  No test files found")
            return result
        
        print(f"✅ Found {len(checks['test_files'])} test files")
        
        # Setup virtual environment
        python_cmd = self.setup_venv_if_needed(project_path)
        
        # Install dependencies
        if not self.install_test_dependencies(project_path, python_cmd):
            result['status'] = 'setup_failed'
            result['errors'].append('Failed to install test dependencies')
            return result
        
        # Run pytest with JSON report
        report_file = self.report_dir / f"{project_name}_test_report.json"
        coverage_file = self.report_dir / f"{project_name}_coverage.xml"
        
        pytest_cmd = (
            f'{python_cmd} -m pytest '
            f'--json-report --json-report-file={report_file} '
            f'--cov=. --cov-report=xml:{coverage_file} '
            f'--tb=short -v'
        )
        
        print(f"\n🧪 Running tests...")
        stdout, stderr, returncode = self.run_command(
            pytest_cmd,
            project_path,
            timeout=600  # 10 minutes
        )
        
        # Parse results
        if report_file.exists():
            try:
                with open(report_file, 'r') as f:
                    test_data = json.load(f)
                
                result['tests_run'] = test_data.get('summary', {}).get('total', 0)
                result['tests_passed'] = test_data.get('summary', {}).get('passed', 0)
                result['tests_failed'] = test_data.get('summary', {}).get('failed', 0)
                result['duration'] = test_data.get('duration', 0)
                
                if result['tests_failed'] == 0 and result['tests_run'] > 0:
                    result['status'] = 'passed'
                elif result['tests_run'] > 0:
                    result['status'] = 'failed'
                else:
                    result['status'] = 'no_tests_run'
                
                # Extract failed test details
                if result['tests_failed'] > 0:
                    failed_tests = []
                    for test in test_data.get('tests', []):
                        if test.get('outcome') == 'failed':
                            failed_tests.append({
                                'name': test.get('nodeid', 'unknown'),
                                'error': test.get('call', {}).get('longrepr', 'No details')
                            })
                    result['failed_tests'] = failed_tests[:5]  # First 5 failures
                
            except Exception as e:
                result['errors'].append(f'Failed to parse test report: {e}')
                result['status'] = 'parse_error'
        else:
            # Fallback: parse stdout
            if 'passed' in stdout or 'PASSED' in stdout:
                result['status'] = 'passed'
                # Try to extract counts
                import re
                match = re.search(r'(\d+) passed', stdout)
                if match:
                    result['tests_passed'] = int(match.group(1))
                    result['tests_run'] = result['tests_passed']
            elif 'failed' in stdout or 'FAILED' in stdout:
                result['status'] = 'failed'
            elif returncode == 0:
                result['status'] = 'passed'
            else:
                result['status'] = 'error'
                result['errors'].append('Test execution failed')
        
        # Save full output
        output_file = self.report_dir / f"{project_name}_output.txt"
        with open(output_file, 'w') as f:
            f.write(f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}\n")
        
        # Print summary
        if result['status'] == 'passed':
            print(f"\n✅ All tests passed! ({result['tests_passed']} tests)")
        elif result['status'] == 'failed':
            print(f"\n❌ Tests failed: {result['tests_failed']} failed, {result['tests_passed']} passed")
        else:
            print(f"\n⚠️  Test status: {result['status']}")
        
        return result
    
    def run_all_projects(self) -> List[Dict[str, Any]]:
        """Run tests for all configured projects"""
        print(f"🚀 Running tests for {len(self.config['projects'])} projects")
        print(f"📁 Reports will be saved to: {self.report_dir}")
        print("")
        
        for project_path in self.config['projects']:
            project_path = Path(project_path)
            project_name = project_path.name
            
            try:
                result = self.run_tests(project_path, project_name)
                self.results.append(result)
            except Exception as e:
                print(f"\n❌ Unexpected error testing {project_name}: {e}")
                self.results.append({
                    'project': project_name,
                    'path': str(project_path),
                    'status': 'error',
                    'errors': [str(e)]
                })
        
        return self.results
    
    def generate_summary_report(self):
        """Generate a summary report of all test results"""
        print(f"\n\n{'='*80}")
        print("📊 TEST SUMMARY REPORT")
        print(f"{'='*80}")
        
        # Count statuses
        status_counts = {}
        for result in self.results:
            status = result['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Overall stats
        total_projects = len(self.results)
        total_tests = sum(r.get('tests_run', 0) for r in self.results)
        total_passed = sum(r.get('tests_passed', 0) for r in self.results)
        total_failed = sum(r.get('tests_failed', 0) for r in self.results)
        
        print(f"\nProjects tested: {total_projects}")
        print(f"Total tests run: {total_tests}")
        print(f"Total passed: {total_passed}")
        print(f"Total failed: {total_failed}")
        
        if total_tests > 0:
            print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
        
        print(f"\n📈 Status breakdown:")
        for status, count in sorted(status_counts.items()):
            emoji = {
                'passed': '✅',
                'failed': '❌',
                'no_tests': '⚠️',
                'no_test_files': '📭',
                'not_found': '🚫',
                'error': '💥'
            }.get(status, '❓')
            print(f"  {emoji} {status}: {count}")
        
        # Detailed results table
        print(f"\n📋 Detailed Results:")
        print(f"{'Project':<30} {'Status':<12} {'Tests':<10} {'Passed':<10} {'Failed':<10}")
        print(f"{'-'*30} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")
        
        for result in sorted(self.results, key=lambda x: x['project']):
            print(f"{result['project']:<30} "
                  f"{result['status']:<12} "
                  f"{result.get('tests_run', '-'):<10} "
                  f"{result.get('tests_passed', '-'):<10} "
                  f"{result.get('tests_failed', '-'):<10}")
        
        # Failed tests details
        failed_projects = [r for r in self.results if r['status'] == 'failed']
        if failed_projects:
            print(f"\n❌ Failed Test Details:")
            for project in failed_projects:
                print(f"\n  {project['project']}:")
                for test in project.get('failed_tests', [])[:3]:
                    print(f"    - {test['name']}")
        
        # Save JSON summary
        summary_file = self.report_dir / 'test_summary.json'
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'total_projects': total_projects,
                'total_tests': total_tests,
                'total_passed': total_passed,
                'total_failed': total_failed,
                'status_counts': status_counts,
                'results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Full report saved to: {summary_file}")
        
        # Create markdown report
        self.generate_markdown_report()
    
    def generate_markdown_report(self):
        """Generate a nice markdown report"""
        md_file = self.report_dir / 'test_report.md'
        
        with open(md_file, 'w') as f:
            f.write(f"# Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Summary
            total_tests = sum(r.get('tests_run', 0) for r in self.results)
            total_passed = sum(r.get('tests_passed', 0) for r in self.results)
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Projects**: {len(self.results)}\n")
            f.write(f"- **Total Tests**: {total_tests}\n")
            f.write(f"- **Tests Passed**: {total_passed}\n")
            f.write(f"- **Success Rate**: {(total_passed/total_tests)*100:.1f}%\n\n" if total_tests > 0 else "")
            
            # Results table
            f.write("## Results by Project\n\n")
            f.write("| Project | Status | Tests | Passed | Failed | Coverage |\n")
            f.write("|---------|--------|-------|--------|--------|----------|\n")
            
            for result in sorted(self.results, key=lambda x: x['project']):
                status_emoji = {
                    'passed': '✅',
                    'failed': '❌',
                    'no_tests': '⚠️',
                    'error': '💥'
                }.get(result['status'], '❓')
                
                f.write(f"| {result['project']} | {status_emoji} {result['status']} | "
                       f"{result.get('tests_run', '-')} | "
                       f"{result.get('tests_passed', '-')} | "
                       f"{result.get('tests_failed', '-')} | "
                       f"{result.get('coverage', '-')} |\n")
            
            # Failed tests
            failed = [r for r in self.results if r['status'] == 'failed']
            if failed:
                f.write("\n## Failed Tests\n\n")
                for project in failed:
                    f.write(f"### {project['project']}\n\n")
                    for test in project.get('failed_tests', []):
                        f.write(f"- `{test['name']}`\n")
                    f.write("\n")
        
        print(f"📄 Markdown report saved to: {md_file}")

def main():
    """Run all tests with claude-test-reporter"""
    runner = TestRunner()
    
    try:
        # Run all tests
        results = runner.run_all_projects()
        
        # Generate summary
        runner.generate_summary_report()
        
        # Exit with appropriate code
        failed_count = sum(1 for r in results if r['status'] == 'failed')
        # sys.exit() removed
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test run interrupted by user")
        # sys.exit() removed
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        # sys.exit() removed

if __name__ == '__main__':
    main()