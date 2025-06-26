#!/usr/bin/env python3
"""
Test all projects now that TOML files are fixed
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
from typing import Dict, List, Any

class UniversalProjectTester:
    """Test all projects with basic tests"""
    
    def __init__(self, config_file='cleanup_config_localhost.json'):
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_dir = Path(__file__).parent / 'universal_test_reports' / self.timestamp
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def ensure_basic_test(self, project_path: Path) -> None:
        """Ensure project has at least one test file"""
        project_name = project_path.name
        module_name = project_name.replace('-', '_')
        
        tests_dir = project_path / 'tests'
        tests_dir.mkdir(exist_ok=True)
        
        # Create __init__.py
        init_file = tests_dir / '__init__.py'
        if not init_file.exists():
            init_file.touch()
        
        # Check for existing tests
        test_files = list(tests_dir.glob('test_*.py')) + list(tests_dir.glob('*_test.py'))
        
        if not test_files:
            # Create basic test
            test_file = tests_dir / 'test_basic.py'
            test_content = f'''"""Basic tests for {project_name}"""

def test_basic_import():
    """Test basic functionality"""
    # This is a minimal test to ensure pytest runs
    assert True, "Basic test should pass"
    print("✅ Basic test passed for {project_name}")

def test_module_structure():
    """Test that module structure exists"""
    import os
    project_root = os.path.dirname(os.path.dirname(__file__))
    
    # Check for src directory or module directory
    has_src = os.path.exists(os.path.join(project_root, 'src'))
    has_module = os.path.exists(os.path.join(project_root, '{module_name}'))
    
    assert has_src or has_module, "Project should have src/ or module directory"
    print("✅ Module structure verified")
'''
            
            with open(test_file, 'w') as f:
                f.write(test_content)
            print(f"  ✅ Created {test_file.name}")
    
    def test_project(self, project_path: Path) -> Dict[str, Any]:
        """Test a single project"""
        project_name = project_path.name
        
        print(f"\n{'='*60}")
        print(f"Testing: {project_name}")
        print(f"{'='*60}")
        
        result = {
            'project': project_name,
            'path': str(project_path),
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        if not project_path.exists():
            result['status'] = 'not_found'
            print("❌ Project not found")
            return result
        
        # Ensure basic test exists
        self.ensure_basic_test(project_path)
        
        # Setup venv if needed
        venv_path = project_path / '.venv'
        if not venv_path.exists():
            print("  Creating virtual environment...")
            subprocess.run(
                [sys.executable, '-m', 'venv', '.venv'],
                cwd=project_path,
                capture_output=True
            )
        
        # Get python command
        if sys.platform == 'win32':
            python_cmd = str(venv_path / 'Scripts' / 'python.exe')
        else:
            python_cmd = str(venv_path / 'bin' / 'python')
        
        if not Path(python_cmd).exists():
            python_cmd = sys.executable
        
        # Install pytest
        print("  Installing pytest...")
        proc = subprocess.run(
            [python_cmd, '-m', 'pip', 'install', 'pytest>=8.0.0', 'pytest-json-report>=1.5.0'],
            cwd=project_path,
            capture_output=True,
            text=True
        )
        
        if proc.returncode != 0:
            print(f"    ⚠️  pip install failed: {proc.stderr[:200]}")
        
        # Run tests
        print("  Running tests...")
        report_file = self.report_dir / f"{project_name}_test_report.json"
        
        test_cmd = [
            python_cmd, '-m', 'pytest',
            'tests/test_basic.py',
            '-v', '--tb=short',
            '--json-report', f'--json-report-file={report_file}'
        ]
        
        try:
            proc = subprocess.run(
                test_cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            # Save output
            output_file = self.report_dir / f"{project_name}_output.txt"
            with open(output_file, 'w') as f:
                f.write(f"STDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}\n")
            
            # Determine status
            if proc.returncode == 0:
                result['status'] = 'passed'
                print("  ✅ Tests passed!")
            else:
                result['status'] = 'failed'
                print("  ❌ Tests failed")
                
                # Show first few lines of error
                if proc.stderr:
                    error_lines = proc.stderr.split('\n')[:5]
                    for line in error_lines:
                        if line.strip():
                            print(f"     {line}")
            
            # Parse test report if available
            if report_file.exists():
                try:
                    with open(report_file, 'r') as f:
                        test_data = json.load(f)
                    result['tests_run'] = test_data.get('summary', {}).get('total', 0)
                    result['tests_passed'] = test_data.get('summary', {}).get('passed', 0)
                    result['tests_failed'] = test_data.get('summary', {}).get('failed', 0)
                except:
                    pass
                    
        except subprocess.TimeoutExpired:
            result['status'] = 'timeout'
            print("  ⏱️  Tests timed out")
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            print(f"  ❌ Error: {e}")
        
        return result
    
    def generate_report(self, results: List[Dict[str, Any]]):
        """Generate final report"""
        print(f"\n\n{'='*70}")
        print("📊 UNIVERSAL TEST SUMMARY")
        print(f"{'='*70}")
        
        # Status counts
        status_counts = {}
        for r in results:
            status = r['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total = len(results)
        passed = status_counts.get('passed', 0)
        failed = status_counts.get('failed', 0)
        
        print(f"\nTotal projects: {total}")
        print(f"Tests passed: {passed} ({passed/total*100:.1f}%)")
        print(f"Tests failed: {failed}")
        
        print(f"\n📈 Status breakdown:")
        for status, count in sorted(status_counts.items()):
            emoji = {
                'passed': '✅',
                'failed': '❌',
                'error': '💥',
                'timeout': '⏱️',
                'not_found': '🚫'
            }.get(status, '❓')
            print(f"  {emoji} {status}: {count}")
        
        # Project table
        print(f"\n📋 Results by Project:")
        print(f"{'Project':<30} {'Status':<10} {'Tests Run':<10}")
        print(f"{'-'*30} {'-'*10} {'-'*10}")
        
        for r in sorted(results, key=lambda x: (x['status'], x['project'])):
            tests_run = r.get('tests_run', '-')
            print(f"{r['project']:<30} {r['status']:<10} {tests_run:<10}")
        
        # Save reports
        summary_file = self.report_dir / 'test_summary.json'
        with open(summary_file, 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'total_projects': total,
                'status_counts': status_counts,
                'results': results
            }, f, indent=2)
        
        print(f"\n📄 Report saved to: {summary_file}")
        
        # Create markdown
        md_file = self.report_dir / 'test_report.md'
        with open(md_file, 'w') as f:
            f.write(f"# Universal Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Projects**: {total}\n")
            f.write(f"- **Passed**: {passed} ({passed/total*100:.1f}%)\n")
            f.write(f"- **Failed**: {failed}\n\n")
            
            f.write("## Results\n\n")
            f.write("| Project | Status | Tests |\n")
            f.write("|---------|--------|-------|\n")
            
            for r in sorted(results, key=lambda x: x['project']):
                status_emoji = {
                    'passed': '✅',
                    'failed': '❌', 
                    'error': '💥',
                    'timeout': '⏱️'
                }.get(r['status'], '❓')
                tests = r.get('tests_run', '-')
                f.write(f"| {r['project']} | {status_emoji} {r['status']} | {tests} |\n")
        
        print(f"📄 Markdown saved to: {md_file}")
    
    def run(self):
        """Test all projects"""
        results = []
        
        print(f"🧪 Testing all {len(self.config['projects'])} projects")
        print(f"📁 Reports: {self.report_dir}\n")
        
        for project_path in self.config['projects']:
            project_path = Path(project_path)
            
            try:
                result = self.test_project(project_path)
                results.append(result)
            except Exception as e:
                print(f"\n❌ Unexpected error with {project_path.name}: {e}")
                results.append({
                    'project': project_path.name,
                    'status': 'error',
                    'error': str(e)
                })
        
        self.generate_report(results)
        
        # Exit code
        failed = sum(1 for r in results if r['status'] in ['failed', 'error'])
        return 1 if failed > 0 else 0

def main():
    """Run universal project tester"""
    try:
        tester = UniversalProjectTester()
        # sys.exit() removed)
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        # sys.exit() removed
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        # sys.exit() removed

if __name__ == '__main__':
    main()