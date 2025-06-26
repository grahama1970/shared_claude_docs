#!/usr/bin/env python3
"""
Module: verify_project_readiness.py
Description: Verifies UI projects are ready for Level 0-4 interaction testing

External Dependencies:
- None (uses only standard library)

Sample Input:
>>> # Run from command line
>>> python verify_project_readiness.py

Expected Output:
>>> Checking project readiness...
>>> ✅ aider-daemon: Ready for testing
>>> ❌ annotator: Missing dependencies
>>> ...

Example Usage:
>>> python verify_project_readiness.py
"""

import sys
import os
import importlib.util
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

# Project configurations
PROJECTS = {
    'aider-daemon': {
        'path': '/home/graham/workspace/experiments/aider-daemon',
        'type': 'python',
        'modules': ['aider_daemon.cli.app', 'aider_daemon.core.daemon'],
        'entry_point': 'src/aider_daemon/cli/app.py',
        'critical': True
    },
    'annotator': {
        'path': '/home/graham/workspace/experiments/annotator',
        'type': 'python',
        'modules': ['annotator.core', 'annotator.api.app'],
        'entry_point': 'src/annotator/api/app.py',
        'critical': True
    },
    'chat-backend': {
        'path': '/home/graham/workspace/experiments/chat',
        'type': 'python',
        'modules': ['backend.api.main', 'backend.api.websocket_manager'],
        'entry_point': 'backend/api/main.py',
        'critical': True
    },
    'chat-frontend': {
        'path': '/home/graham/workspace/experiments/chat/frontend',
        'type': 'javascript',
        'files': ['package.json', 'src/App.jsx'],
        'critical': False
    },
    'granger-ui': {
        'path': '/home/graham/workspace/granger-ui',
        'type': 'javascript',
        'files': ['package.json', 'packages/ui-core/src/index.ts'],
        'critical': False
    }
}

def check_python_project(name: str, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Check if a Python project is ready"""
    issues = []
    project_path = Path(config['path'])
    
    # Check if project exists
    if not project_path.exists():
        issues.append(f"Project directory not found: {config['path']}")
        return False, issues
    
    # Add to Python path
    src_path = project_path / 'src'
    if src_path.exists():
        sys.path.insert(0, str(src_path))
    else:
        sys.path.insert(0, str(project_path))
    
    # Check entry point
    entry_point = project_path / config['entry_point']
    if not entry_point.exists():
        issues.append(f"Entry point not found: {config['entry_point']}")
    
    # Try importing modules
    for module in config.get('modules', []):
        try:
            # Use importlib to check if module can be imported
            spec = importlib.util.find_spec(module)
            if spec is None:
                issues.append(f"Cannot import module: {module}")
        except Exception as e:
            issues.append(f"Import error for {module}: {str(e)}")
    
    # Check for pyproject.toml
    pyproject = project_path / 'pyproject.toml'
    if not pyproject.exists():
        issues.append("No pyproject.toml found")
    
    # Check for test directory
    test_dirs = ['tests', 'test']
    has_tests = any((project_path / td).exists() for td in test_dirs)
    if not has_tests:
        issues.append("No test directory found")
    
    return len(issues) == 0, issues

def check_javascript_project(name: str, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Check if a JavaScript project is ready"""
    issues = []
    project_path = Path(config['path'])
    
    # Check if project exists
    if not project_path.exists():
        issues.append(f"Project directory not found: {config['path']}")
        return False, issues
    
    # Check required files
    for file in config.get('files', []):
        file_path = project_path / file
        if not file_path.exists():
            issues.append(f"Required file not found: {file}")
    
    # Check package.json
    package_json = project_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                package_data = json.load(f)
                
            # Check for test script
            scripts = package_data.get('scripts', {})
            if 'test' not in scripts:
                issues.append("No test script in package.json")
                
        except Exception as e:
            issues.append(f"Cannot read package.json: {str(e)}")
    else:
        issues.append("No package.json found")
    
    # Check for node_modules
    node_modules = project_path / 'node_modules'
    if not node_modules.exists():
        issues.append("Dependencies not installed (no node_modules)")
    
    return len(issues) == 0, issues

def check_project_interactions_ready() -> bool:
    """Check if project_interactions directory has necessary structure"""
    interactions_path = Path('/home/graham/workspace/shared_claude_docs/project_interactions')
    
    required_dirs = [
        'arangodb/level_0_tests',
        'arxiv-mcp-server/level_0_tests',
        'level_2_tests',
        'level_3_tests'
    ]
    
    print(f"\n{BLUE}Checking project_interactions structure...{NC}")
    all_exist = True
    
    for dir_path in required_dirs:
        full_path = interactions_path / dir_path
        if full_path.exists():
            print(f"{GREEN}✅ {dir_path}{NC}")
        else:
            print(f"{RED}❌ {dir_path} missing{NC}")
            all_exist = False
    
    return all_exist

def main():
    """Main verification function"""
    print(f"{BLUE}🔍 Verifying Project Readiness for Level 0-4 Testing{NC}")
    print("=" * 60)
    
    ready_projects = []
    critical_failures = []
    
    # Check each project
    for name, config in PROJECTS.items():
        print(f"\n{YELLOW}Checking {name}...{NC}")
        
        if config['type'] == 'python':
            is_ready, issues = check_python_project(name, config)
        elif config['type'] == 'javascript':
            is_ready, issues = check_javascript_project(name, config)
        else:
            is_ready, issues = False, ["Unknown project type"]
        
        if is_ready:
            print(f"{GREEN}✅ {name}: Ready for testing{NC}")
            ready_projects.append(name)
        else:
            print(f"{RED}❌ {name}: Not ready{NC}")
            for issue in issues:
                print(f"   - {issue}")
            
            if config.get('critical', False):
                critical_failures.append(name)
    
    # Check project interactions
    interactions_ready = check_project_interactions_ready()
    
    # Summary
    print(f"\n{BLUE}{'=' * 60}{NC}")
    print(f"{BLUE}Summary:{NC}")
    print(f"Ready projects: {len(ready_projects)}/{len(PROJECTS)}")
    print(f"Critical failures: {len(critical_failures)}")
    print(f"Project interactions ready: {'Yes' if interactions_ready else 'No'}")
    
    if critical_failures:
        print(f"\n{RED}Critical projects not ready:{NC}")
        for project in critical_failures:
            print(f"  - {project}")
    
    # Overall readiness
    overall_ready = len(critical_failures) == 0 and interactions_ready
    
    print(f"\n{BLUE}Overall Status:{NC}")
    if overall_ready:
        print(f"{GREEN}✅ Ready for Level 0-4 interaction testing!{NC}")
        return 0
    else:
        print(f"{RED}❌ Not ready for testing. Fix issues above.{NC}")
        print(f"\n{YELLOW}Run ./fix_ui_projects.sh to install dependencies{NC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())