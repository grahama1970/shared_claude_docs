#!/usr/bin/env python3
"""Fix incorrect docstring syntax in __init__.py files."""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import re
from pathlib import Path

def fix_init_file(file_path):
    """Fix docstring syntax in an __init__.py file."""
    try:
        content = file_path.read_text()
        
        # Check if file has the problematic pattern
        if re.search(r'^"""[^"]*"""\s*\nModule:', content, re.MULTILINE):
            # Fix the pattern
            fixed = re.sub(
                r'^("""[^"]*""")\s*\n(Module:.*?)\n(Description:.*?)$',
                r'\1\n\n\2\n\3\n"""',
                content,
                flags=re.MULTILINE
            )
            
            # Also handle case where Module: is on same line as opening docstring
            fixed = re.sub(
                r'^"""([^"]*?)"""\s*Module:',
                r'"""\n\1\n\nModule:',
                fixed,
                flags=re.MULTILINE
            )
            
            file_path.write_text(fixed)
            print(f"Fixed: {file_path}")
            return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# Find all __init__.py files in claude-test-reporter src
base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src")
init_files = list(base_path.rglob("__init__.py"))

print(f"Found {len(init_files)} __init__.py files")

fixed_count = 0
for init_file in init_files:
    if fix_init_file(init_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} files")