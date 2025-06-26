#!/usr/bin/env python3
"""Fix all broken docstrings in Python files."""

from pathlib import Path

def fix_broken_docstring(file_path):
    """Fix files where docstring opening quotes are missing."""
    try:
        content = file_path.read_text()
        
        # Check if file starts with Module: without opening quotes
        lines = content.split('\n')
        if len(lines) > 3 and lines[0] == '' and lines[1] == '' and lines[2].startswith('Module:'):
            # Add opening quotes
            lines[1] = '"""'
            new_content = '\n'.join(lines)
            
            file_path.write_text(new_content)
            print(f"Fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# Find all Python files that might have this issue
base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src")
py_files = list(base_path.rglob("*.py"))

print(f"Checking {len(py_files)} Python files")

fixed_count = 0
for py_file in py_files:
    if fix_broken_docstring(py_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} files")