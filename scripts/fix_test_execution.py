#!/usr/bin/env python3
"""
Module: fix_test_execution.py
Description: Fix test execution infrastructure across all Granger projects

External Dependencies:
- None (uses subprocess)

Sample Input:
>>> project_path = "/home/graham/workspace/experiments/granger_hub"

Expected Output:
>>> Running pytest with proper output logging...
>>> Test output saved to: pytest_output.log
>>> 15 tests passed, 0 failed

Example Usage:
>>> python fix_test_execution.py
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import subprocess
import sys
from pathlib import Path
import time
import json


def find_venv(project_path: Path) -> Path:
    """Find virtual environment in project."""
    for venv_name in ['.venv', 'venv', 'env']:
        venv_path = project_path / venv_name
        if venv_path.exists() and (venv_path / 'bin' / 'activate').exists():
            return venv_path
    return None


def run_tests_with_output(project_path: Path, project_name: str) -> dict:
    """Run tests and capture output properly."""
    print(f"\n{'='*60}")
    print(f"Testing: {project_name}")
    print(f"Path: {project_path}")
    print('='*60)
    
    result = {
        'project': project_name,
        'path': str(project_path),
        'status': 'pending',
        'total': 0,
        'passed': 0,
        'failed': 0,
        'output': '',
        'error': None,
        'duration': 0
    }
    
    if not project_path.exists():
        result['status'] = 'error'
        result['error'] = 'Project path does not exist'
        return result
    
    tests_dir = project_path / 'tests'
    if not tests_dir.exists():
        result['status'] = 'no_tests'
        result['error'] = 'No tests directory found'
        return result
    
    # Find virtual environment
    venv = find_venv(project_path)
    if not venv:
        result['status'] = 'error'
        result['error'] = 'No virtual environment found'
        return result
    
    # Create log directory
    log_dir = Path('/home/graham/workspace/shared_claude_docs/granger_verification_reports/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Run pytest with proper output
    pytest_log = log_dir / f'pytest_{project_name}.log'
    pytest_json = project_path / 'test_report.json'
    
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source {venv}/bin/activate && '
        f'pytest tests/ -v --tb=short --no-header --durations=0 '
        f'--json-report --json-report-file={pytest_json} '
        f'2>&1 | tee {pytest_log}'
    ]
    
    print(f"Running pytest in {project_path}...")
    start_time = time.time()
    
    try:
        # Run with real-time output
        process = subprocess.run(cmd, text=True, capture_output=True)
        duration = time.time() - start_time
        
        result['duration'] = duration
        result['output'] = process.stdout
        
        # Also print output to console
        print("\n--- Test Output ---")
        print(process.stdout)
        if process.stderr:
            print("\n--- Errors ---")
            print(process.stderr)
        print("--- End Output ---\n")
        
        # Save output to log file
        with open(pytest_log, 'w') as f:
            f.write(f"Project: {project_name}\n")
            f.write(f"Path: {project_path}\n")
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Duration: {duration:.2f}s\n")
            f.write(f"Exit Code: {process.returncode}\n")
            f.write("\n--- STDOUT ---\n")
            f.write(process.stdout)
            if process.stderr:
                f.write("\n--- STDERR ---\n")
                f.write(process.stderr)
        
        # Parse JSON report if available
        if pytest_json.exists():
            try:
                with open(pytest_json) as f:
                    test_data = json.load(f)
                result['total'] = test_data['summary'].get('total', 0)
                result['passed'] = test_data['summary'].get('passed', 0)
                result['failed'] = test_data['summary'].get('failed', 0)
                result['status'] = 'passed' if result['failed'] == 0 else 'failed'
            except Exception as e:
                print(f"Error parsing test report: {e}")
                result['status'] = 'error'
                result['error'] = f'Failed to parse test report: {e}'
        else:
            # Try to parse from output
            if 'passed' in process.stdout or 'failed' in process.stdout:
                result['status'] = 'completed'
            else:
                result['status'] = 'no_output'
                result['error'] = 'No test output found'
        
        return result
        
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        return result


def main():
    """Test all Granger projects."""
    projects = [
        ('granger_hub', '/home/graham/workspace/experiments/granger_hub'),
        ('rl_commons', '/home/graham/workspace/experiments/rl_commons'),
        ('claude-test-reporter', '/home/graham/workspace/experiments/claude-test-reporter'),
        ('world_model', '/home/graham/workspace/experiments/world_model'),
        ('sparta', '/home/graham/workspace/experiments/sparta'),
        ('marker', '/home/graham/workspace/experiments/marker'),
        ('arangodb', '/home/graham/workspace/experiments/arangodb'),
        ('llm_call', '/home/graham/workspace/experiments/llm_call'),
        ('unsloth_wip', '/home/graham/workspace/experiments/unsloth_wip'),
    ]
    
    results = []
    
    print("🔧 Fixing Test Execution Infrastructure")
    print("This will run pytest for each project and save proper logs")
    
    for name, path in projects[:3]:  # Start with first 3 projects
        result = run_tests_with_output(Path(path), name)
        results.append(result)
        
        print(f"\nSummary for {name}:")
        print(f"  Status: {result['status']}")
        print(f"  Tests: {result['passed']}/{result['total']} passed")
        if result['error']:
            print(f"  Error: {result['error']}")
    
    # Save summary
    summary_path = Path('/home/graham/workspace/shared_claude_docs/granger_verification_reports/test_execution_fix_summary.json')
    with open(summary_path, 'w') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': results
        }, f, indent=2)
    
    print(f"\n📊 Summary saved to: {summary_path}")
    
    # Count issues
    no_output = sum(1 for r in results if r['status'] == 'no_output')
    errors = sum(1 for r in results if r['status'] == 'error')
    passed = sum(1 for r in results if r['status'] == 'passed')
    
    print(f"\n🎯 Overall Results:")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ No output: {no_output}")
    print(f"  ⚠️  Errors: {errors}")
    
    return 0 if no_output == 0 and errors == 0 else 1


if __name__ == "__main__":
    # sys.exit() removed)