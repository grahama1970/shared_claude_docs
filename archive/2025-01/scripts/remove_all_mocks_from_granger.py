#!/usr/bin/env python3
"""
Module: remove_all_mocks_from_granger.py
Description: Remove all mock usage from Granger projects to comply with NO MOCKS policy

External Dependencies:
- pathlib: https://docs.python.org/3/library/pathlib.html

Sample Input:
>>> # Run from shared_claude_docs directory
>>> python remove_all_mocks_from_granger.py

Expected Output:
>>> Removing mocks from granger_hub...
>>> Fixed: tests/test_hub.py - removed 5 mock imports
>>> ... (more fixes)
>>> ✅ All mocks removed successfully

Example Usage:
>>> python remove_all_mocks_from_granger.py
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# Projects known to have mocks from audit
MOCK_PROJECTS = {
    "granger_hub": "/home/graham/workspace/experiments/granger_hub",
    "rl_commons": "/home/graham/workspace/experiments/rl_commons",
    "arangodb": "/home/graham/workspace/experiments/arangodb",
    "marker": "/home/graham/workspace/experiments/marker",
    "sparta": "/home/graham/workspace/experiments/sparta",
}

# Additional projects to check
OTHER_PROJECTS = {
    "world_model": "/home/graham/workspace/experiments/world_model",
    "claude-test-reporter": "/home/graham/workspace/experiments/claude-test-reporter",
    "youtube_transcripts": "/home/graham/workspace/experiments/youtube_transcripts",
    "unsloth_wip": "/home/graham/workspace/experiments/unsloth_wip",
    "chat": "/home/graham/workspace/experiments/chat",
    "annotator": "/home/graham/workspace/experiments/annotator",
    "aider-daemon": "/home/graham/workspace/experiments/aider-daemon",
    "arxiv-mcp-server": "/home/graham/workspace/mcp-servers/arxiv-mcp-server",
    "mcp-screenshot": "/home/graham/workspace/experiments/mcp-screenshot",
    "gitget": "/home/graham/workspace/experiments/gitget",
    "darpa_crawl": "/home/graham/workspace/experiments/darpa_crawl",
}

# Patterns to find and remove
MOCK_PATTERNS = [
    # Import statements
    (r'^from unittest\.mock import.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^from unittest import mock.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^import unittest\.mock.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^from mock import.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^import mock.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    
    # Pytest mock imports
    (r'^from pytest_mock import.*$', '# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    
    # Common mock usage patterns - comment out instead of removing
    (r'^(\s*)@patch\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)@mock\.patch\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*Mock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*MagicMock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*AsyncMock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*mock\.Mock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*mock\.MagicMock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)(\w+)\s*=\s*mock\.AsyncMock\(.*\)$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    
    # patch.object usage
    (r'^(\s*)with patch\.object\(.*\):$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
    (r'^(\s*)with mock\.patch\.object\(.*\):$', '\\1# REMOVED BY NO-MOCK POLICY: \\g<0>'),
]


def remove_mocks_from_file(file_path: Path) -> Tuple[bool, int]:
    """Remove mock usage from a single Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # Apply each pattern
        for pattern, replacement in MOCK_PATTERNS:
            content, n = re.subn(pattern, replacement, content, flags=re.MULTILINE)
            changes += n
        
        # Only write if changes were made
        if content != original_content:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.mock_backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, changes
        
        return False, 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False, 0


def remove_mocks_from_project(project_name: str, project_path: str) -> List[str]:
    """Remove mocks from all Python files in a project"""
    results = []
    project_dir = Path(project_path)
    
    if not project_dir.exists():
        return [f"❌ {project_name}: Directory not found"]
    
    # Find all Python test files
    test_files = []
    for pattern in ['tests/**/*.py', 'test/**/*.py', '**/test_*.py', '**/*_test.py']:
        test_files.extend(project_dir.glob(pattern))
    
    # Also check src files that might have mocks
    src_files = list(project_dir.glob('src/**/*.py'))
    
    all_files = set(test_files + src_files)
    
    # Skip .venv and other directories
    skip_dirs = {'.venv', 'venv', '__pycache__', '.git', 'repos', 'build', 'dist'}
    all_files = [f for f in all_files if not any(skip in f.parts for skip in skip_dirs)]
    
    total_changes = 0
    files_changed = 0
    
    for file_path in all_files:
        changed, changes = remove_mocks_from_file(file_path)
        if changed:
            files_changed += 1
            total_changes += changes
            relative_path = file_path.relative_to(project_dir)
            results.append(f"  Fixed: {relative_path} - {changes} mock patterns removed")
    
    if files_changed > 0:
        results.insert(0, f"✅ {project_name}: Fixed {files_changed} files, removed {total_changes} mock patterns")
    else:
        results.append(f"✓ {project_name}: No mocks found in project files")
    
    return results


def main():
    """Remove mocks from all Granger projects"""
    print("🧹 Removing Mocks from Granger Projects")
    print("=" * 50)
    
    all_results = []
    
    # Process known mock projects first
    print("\n📦 Processing Projects with Known Mocks")
    print("-" * 40)
    
    for project_name, project_path in MOCK_PROJECTS.items():
        print(f"\nProcessing {project_name}...")
        results = remove_mocks_from_project(project_name, project_path)
        all_results.extend(results)
        for result in results:
            print(result)
    
    # Process other projects
    print("\n📦 Checking Other Projects")
    print("-" * 40)
    
    for project_name, project_path in OTHER_PROJECTS.items():
        print(f"\nProcessing {project_name}...")
        results = remove_mocks_from_project(project_name, project_path)
        all_results.extend(results)
        for result in results:
            print(result)
    
    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    
    fixed_projects = sum(1 for r in all_results if "✅" in r)
    clean_projects = sum(1 for r in all_results if "✓" in r)
    errors = sum(1 for r in all_results if "❌" in r)
    
    print(f"✅ Fixed: {fixed_projects} projects")
    print(f"✓ Already clean: {clean_projects} projects")
    print(f"❌ Errors: {errors}")
    
    print("\n🎯 Next Steps:")
    print("1. Review the .mock_backup files to understand what was removed")
    print("2. Fix any broken tests by implementing real test scenarios")
    print("3. Run tests for each project to identify what needs fixing")
    print("4. Delete .mock_backup files once tests are passing")
    
    print("\n📝 Note: Mock usage has been commented out, not deleted.")
    print("This allows you to see what was being mocked and implement real alternatives.")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())