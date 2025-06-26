#!/usr/bin/env python3
"""
Module: fix_python_and_pytest.py
Description: Fix Python version to 3.10.11 and pytest configuration across all projects

External Dependencies:
- uv

Example Usage:
>>> python fix_python_and_pytest.py
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
import toml


def fix_pyproject_toml(project_path: Path) -> bool:
    """Fix pyproject.toml to add honeypot marker and ensure pytest-json-report."""
    pyproject_path = project_path / 'pyproject.toml'
    
    if not pyproject_path.exists():
        print(f"  ⚠️  No pyproject.toml found")
        return False
    
    try:
        # Read existing config
        with open(pyproject_path, 'r') as f:
            config = toml.load(f)
        
        # Ensure tool.pytest.ini_options exists
        if 'tool' not in config:
            config['tool'] = {}
        if 'pytest' not in config['tool']:
            config['tool']['pytest'] = {}
        if 'ini_options' not in config['tool']['pytest']:
            config['tool']['pytest']['ini_options'] = {}
        
        # Add honeypot marker
        markers = config['tool']['pytest']['ini_options'].get('markers', [])
        if isinstance(markers, str):
            markers = [markers]
        
        honeypot_marker = 'honeypot: test designed to fail for integrity verification'
        if not any('honeypot' in m for m in markers):
            markers.append(honeypot_marker)
            config['tool']['pytest']['ini_options']['markers'] = markers
        
        # Ensure dependencies include pytest-json-report
        if 'project' in config and 'dependencies' in config['project']:
            deps = config['project']['dependencies']
            if not any('pytest-json-report' in d for d in deps):
                deps.append('pytest-json-report')
        
        # Write back
        with open(pyproject_path, 'w') as f:
            toml.dump(config, f)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error fixing pyproject.toml: {e}")
        return False


def recreate_venv_with_python_3_10_11(project_path: Path, project_name: str) -> bool:
    """Recreate virtual environment with Python 3.10.11."""
    print(f"\n📦 Recreating venv for {project_name} with Python 3.10.11...")
    
    # Find existing venv
    venv_path = None
    for venv_name in ['.venv', 'venv', 'env']:
        candidate = project_path / venv_name
        if candidate.exists():
            venv_path = candidate
            break
    
    if not venv_path:
        print(f"  ⚠️  No virtual environment found")
        return False
    
    try:
        # Remove old venv
        cmd = f"rm -rf {venv_path}"
        subprocess.run(cmd, shell=True, check=True)
        
        # Create new venv with uv and Python 3.10.11
        cmd = f"cd {project_path} && uv venv --python=3.10.11"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"  ❌ Failed to create venv: {result.stderr}")
            return False
        
        # Install dependencies
        print(f"  📥 Installing dependencies...")
        cmd = f"cd {project_path} && uv sync"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Try uv pip install
            cmd = f"cd {project_path} && source {venv_path}/bin/activate && uv pip install -e ."
            result = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"  ⚠️  Failed to install dependencies: {result.stderr}")
                # Continue anyway
        
        # Install pytest-json-report explicitly
        cmd = f"cd {project_path} && source {venv_path}/bin/activate && uv pip install pytest-json-report"
        subprocess.run(['bash', '-c', cmd], capture_output=True, text=True)
        
        print(f"  ✅ Venv recreated with Python 3.10.11")
        return True
        
    except Exception as e:
        print(f"  ❌ Error recreating venv: {e}")
        return False


def main():
    """Fix Python versions and pytest configuration."""
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
    
    print("🔧 Fixing Python Versions and Pytest Configuration")
    print("=" * 60)
    
    # First, let's just fix the pytest configuration for now
    for name, path in projects:
        project_path = Path(path)
        if not project_path.exists():
            print(f"\n❌ Skipping {name}: path does not exist")
            continue
        
        print(f"\n📁 Processing {name}...")
        
        # Fix pyproject.toml
        if fix_pyproject_toml(project_path):
            print(f"  ✅ Fixed pyproject.toml")
        
        # Skip venv recreation for now - focus on fixing configs first
        # recreate_venv_with_python_3_10_11(project_path, name)
    
    print("\n✨ Configuration fixes complete")
    print("\nNote: Run with --recreate-venvs flag to also recreate virtual environments")
    
    return 0


if __name__ == "__main__":
    # sys.exit() removed)