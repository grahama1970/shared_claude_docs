#!/usr/bin/env python3
"""
Module: fix_arangodb_tests_no_auth.py
Description: Update ArangoDB tests to work without authentication

External Dependencies:
- None

Example Usage:
>>> python fix_arangodb_tests_no_auth.py
"""

import re
from pathlib import Path


def fix_arangodb_no_auth(file_path):
    """Update test file to work without authentication."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Remove username and password from db connections
    content = re.sub(
        r'\.db\([^)]+,\s*username=[^,)]+,\s*password=[^)]+\)',
        '.db(\\1)',
        content
    )
    
    # Simpler pattern for system db
    content = re.sub(
        r"sys_db\.has_database",
        "cls.client.db('_system').has_database",
        content
    )
    
    content = re.sub(
        r"sys_db\.create_database",
        "cls.client.db('_system').create_database",
        content
    )
    
    # Fix the db connection pattern
    content = re.sub(
        r"cls\.db = cls\.client\.db\(ARANGO_DB, username=ARANGO_USER, password=ARANGO_PASS\)",
        "cls.db = cls.client.db(ARANGO_DB)",
        content
    )
    
    content = re.sub(
        r"cls\.client\.db\('_system', username=ARANGO_USER, password=ARANGO_PASS\)",
        "cls.client.db('_system')",
        content
    )
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    
    return False


def main():
    """Fix all ArangoDB test files."""
    print("🔧 Fixing ArangoDB Tests for No Authentication")
    print("=" * 60)
    
    # Find all test files related to ArangoDB
    test_dirs = [
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arangodb_tests"),
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arangodb"),
    ]
    
    fixed_count = 0
    
    for test_dir in test_dirs:
        if not test_dir.exists():
            continue
            
        for test_file in test_dir.rglob("test_*.py"):
            if fix_arangodb_no_auth(test_file):
                print(f"  ✓ Fixed {test_file.name}")
                fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")


if __name__ == "__main__":
    main()