#!/usr/bin/env python3
"""
Module: fix_arangodb_auth.py
Description: Fix ArangoDB authentication in all test files

External Dependencies:
- None

Example Usage:
>>> python fix_arangodb_auth.py
"""

import re
from pathlib import Path


def fix_arangodb_auth_in_file(file_path):
    """Fix ArangoDB authentication in a test file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to find ArangoClient() calls without auth
    pattern = r'ArangoClient\(\s*hosts\s*=\s*"http://localhost:8529"\s*\)'
    replacement = 'ArangoClient(hosts="http://localhost:8529", username="root", password="")'
    
    # Also fix without hosts parameter
    pattern2 = r'ArangoClient\(\s*\)'
    replacement2 = 'ArangoClient(hosts="http://localhost:8529", username="root", password="")'
    
    modified = False
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        modified = True
    
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        modified = True
    
    if modified:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    
    return False


def main():
    """Fix ArangoDB authentication in all test files."""
    print("🔧 Fixing ArangoDB Authentication")
    print("=" * 60)
    
    # Find all Python test files in project_interactions
    test_files = Path("/home/graham/workspace/shared_claude_docs/project_interactions").rglob("test_*.py")
    
    fixed_count = 0
    for test_file in test_files:
        if fix_arangodb_auth_in_file(test_file):
            print(f"  ✓ Fixed {test_file.name}")
            fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")


if __name__ == "__main__":
    main()