#!/usr/bin/env python3
"""
Module: test_specific_projects.py
Description: Test specific projects and show detailed errors

External Dependencies:
- pytest: https://docs.pytest.org/

Example Usage:
>>> python test_specific_projects.py
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


def run_project_tests(project_name, project_path):
    """Run tests for a specific project with detailed output."""
    project_path = Path(project_path)
    
    print(f"\n{'='*60}")
    print(f"Testing {project_name}")
    print(f"{'='*60}")
    
    # Check if project exists
    if not project_path.exists():
        print(f"❌ Project does not exist: {project_path}")
        return False
    
    # Check for venv
    venv_path = project_path / ".venv"
    if not venv_path.exists():
        print(f"❌ No virtual environment found")
        return False
    
    # Run tests
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
        f'python -m pytest -xvs --tb=short --no-header 2>&1 | head -100'
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Test specific projects that are critical."""
    # Start with core projects
    projects = [
        ("world_model", "/home/graham/workspace/experiments/world_model"),
        ("rl_commons", "/home/graham/workspace/experiments/rl_commons"),
        ("granger_hub", "/home/graham/workspace/experiments/granger_hub"),
    ]
    
    results = []
    
    for project_name, project_path in projects:
        success = run_project_tests(project_name, project_path)
        results.append((project_name, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    
    for project_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{project_name}: {status}")
    
    return 0 if all(r[1] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())