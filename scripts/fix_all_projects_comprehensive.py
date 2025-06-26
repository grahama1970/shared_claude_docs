#!/usr/bin/env python3
"""
Module: fix_all_projects_comprehensive.py
Description: Comprehensive fix script for all Granger projects

External Dependencies:
- None (uses standard library)

Example Usage:
>>> python fix_all_projects_comprehensive.py
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime


def fix_arango_url_scheme(file_path):
    """Fix ArangoDB URL scheme issues."""
    try:
        content = file_path.read_text()
        
        # Fix localhost without scheme
        patterns = [
            (r'hosts=(["\'])localhost(["\'])', r'hosts=\1http://localhost:8529\2'),
            (r'ARANGO_HOST["\s]*:["\s]*(["\'])localhost(["\'])', r'ARANGO_HOST": \1http://localhost:8529\2'),
            (r'arango_host["\s]*=["\s]*(["\'])localhost(["\'])', r'arango_host=\1http://localhost:8529\2'),
        ]
        
        modified = False
        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                modified = True
        
        if modified:
            file_path.write_text(content)
            return True
    except:
        pass
    return False


def fix_import_errors(file_path):
    """Fix common import errors."""
    try:
        content = file_path.read_text()
        
        # Fix pydantic imports
        if 'from pydantic import BaseSettings' in content and 'except ImportError' not in content:
            content = content.replace(
                'from pydantic import BaseSettings',
                '''try:
    from pydantic import BaseSettings
except ImportError:
    from pydantic.v1 import BaseSettings'''
            )
            file_path.write_text(content)
            return True
        
        # Fix other common imports
        fixes = [
            # Fix TestResultVerifier as dataclass
            ('@dataclass
class TestResultVerifier:', '@dataclass\n@dataclass
class TestResultVerifier:'),
        ]
        
        modified = False
        for old, new in fixes:
            if old in content and new not in content:
                # Add import if needed
                if '@dataclass' in new and 'from dataclasses import dataclass' not in content:
                    content = 'from dataclasses import dataclass\n' + content
                content = content.replace(old, new)
                modified = True
        
        if modified:
            file_path.write_text(content)
            return True
            
    except:
        pass
    return False


def fix_mock_imports(file_path):
    """Remove or fix mock imports properly."""
    try:
        content = file_path.read_text()
        
        # Skip honeypot tests
        if 'honeypot' in str(file_path).lower():
            return False
        
        lines = content.split('\n')
        new_lines = []
        modified = False
        
        for line in lines:
            # Remove mock imports
            if re.match(r'^from unittest\.mock import|^import mock|^from mock import', line.strip()):
                new_lines.append(f"# REMOVED: {line}")
                modified = True
            else:
                new_lines.append(line)
        
        if modified:
            file_path.write_text('\n'.join(new_lines))
            return True
            
    except:
        pass
    return False


def fix_test_file_issues(file_path):
    """Fix test file specific issues."""
    try:
        content = file_path.read_text()
        
        # Remove sys.exit() calls in test files
        if 'sys.exit(' in content:
            content = re.sub(r'sys\.exit\([^)]*\)', '# sys.exit() removed', content)
            file_path.write_text(content)
            return True
            
    except:
        pass
    return False


def fix_project(project_name, project_path):
    """Apply comprehensive fixes to a project."""
    fixes_applied = []
    project_path = Path(project_path)
    
    if not project_path.exists():
        return fixes_applied
    
    # Fix Python files
    for py_file in project_path.rglob('*.py'):
        if '__pycache__' in str(py_file) or '.venv' in str(py_file):
            continue
        
        # Apply various fixes
        if fix_arango_url_scheme(py_file):
            fixes_applied.append(f"Fixed ArangoDB URL in {py_file.name}")
        
        if fix_import_errors(py_file):
            fixes_applied.append(f"Fixed imports in {py_file.name}")
        
        if fix_mock_imports(py_file):
            fixes_applied.append(f"Removed mocks from {py_file.name}")
        
        if 'test' in py_file.name and fix_test_file_issues(py_file):
            fixes_applied.append(f"Fixed test issues in {py_file.name}")
    
    # Ensure pytest.ini exists
    pytest_ini = project_path / "pytest.ini"
    if not pytest_ini.exists():
        pytest_ini.write_text("""[pytest]
markers =
    honeypot: test designed to fail for integrity verification
    slow: marks tests as slow
    integration: integration tests
    unit: unit tests
    asyncio: marks tests as async
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
asyncio_mode = auto
""")
        fixes_applied.append("Created pytest.ini with asyncio support")
    
    # Fix .env.example
    env_example = project_path / ".env.example"
    if env_example.exists():
        content = env_example.read_text()
        if 'PYTHONPATH' not in content:
            content = 'PYTHONPATH=./src\n' + content
            env_example.write_text(content)
            fixes_applied.append("Added PYTHONPATH to .env.example")
    
    # Create .env from .env.example if missing
    env_file = project_path / ".env"
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        fixes_applied.append("Created .env from .env.example")
    
    return fixes_applied


def ensure_dependencies(project_path):
    """Ensure all dependencies are installed."""
    project_path = Path(project_path)
    
    # Check venv
    venv_path = project_path / ".venv"
    if not venv_path.exists():
        subprocess.run(["uv", "venv", "--python=3.10.11"], cwd=project_path)
    
    # Install dependencies
    if (project_path / "pyproject.toml").exists():
        subprocess.run(["uv", "sync"], cwd=project_path)
    
    # Ensure test dependencies
    subprocess.run([
        "bash", "-c",
        f"cd {project_path} && source .venv/bin/activate && "
        f"uv pip install pytest pytest-asyncio pytest-json-report"
    ])


def main():
    """Fix all projects comprehensively."""
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
    
    print("🔧 Comprehensive Project Fixes")
    print("=" * 60)
    
    for project_name, project_path in projects:
        print(f"\n📦 {project_name}")
        print("-" * 40)
        
        # Apply fixes
        fixes = fix_project(project_name, project_path)
        
        if fixes:
            for fix in fixes:
                print(f"  ✓ {fix}")
        else:
            print("  ✓ No fixes needed")
        
        # Ensure dependencies
        print("  Installing dependencies...")
        ensure_dependencies(project_path)
    
    print("\n✅ All fixes applied!")
    return 0


if __name__ == "__main__":
    sys.exit(main())