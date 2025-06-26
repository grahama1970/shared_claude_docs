#!/usr/bin/env python3
"""
Module: fix_level0_tests_credentials.py
Description: Update Level 0 tests to use test database credentials from .env

External Dependencies:
- None

Example Usage:
>>> python fix_level0_tests_credentials.py
"""

from pathlib import Path
import re


def fix_test_credentials(file_path):
    """Update test file to use test database and credentials."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    
    # Update database name to use test database
    content = re.sub(
        r'ARANGO_DB = "[^"]*"',
        'ARANGO_DB = "youtube_transcripts_test"',
        content
    )
    
    # Update password
    content = re.sub(
        r'ARANGO_PASS = ""',
        'ARANGO_PASS = "openSesame"',
        content
    )
    
    # Update host if needed
    content = re.sub(
        r'ARANGO_HOST = "http://localhost:8529"',
        'ARANGO_HOST = "http://localhost:8529"',
        content
    )
    
    # Fix any hardcoded database names
    content = re.sub(
        r'"test_granger"',
        '"youtube_transcripts_test"',
        content
    )
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    
    return False


def main():
    """Fix all Level 0 test files."""
    print("🔧 Fixing Level 0 Test Credentials")
    print("=" * 60)
    
    # Find all test files in Level 0 directories
    test_dirs = [
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arangodb_tests/level_0"),
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arxiv-mcp-server/level_0"),
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arxiv-mcp-server/level_0_tests"),
        Path("/home/graham/workspace/shared_claude_docs/project_interactions/arangodb/level_0_tests"),
    ]
    
    fixed_count = 0
    
    for test_dir in test_dirs:
        if not test_dir.exists():
            continue
            
        for test_file in test_dir.glob("test_*.py"):
            if fix_test_credentials(test_file):
                print(f"  ✓ Fixed {test_file.name}")
                fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")


if __name__ == "__main__":
    main()