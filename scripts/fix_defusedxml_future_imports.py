#!/usr/bin/env python3
"""
Module: fix_defusedxml_future_imports.py
Description: Fix __future__ imports in defusedxml package

External Dependencies:
- None

Example Usage:
>>> python fix_defusedxml_future_imports.py
"""

import os
from pathlib import Path


def fix_future_imports(file_path):
    """Fix __future__ imports to be at the beginning of the file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if "from __future__" not in content:
            return False
        
        lines = content.split('\n')
        future_imports = []
        other_lines = []
        in_initial_comments = True
        shebang = None
        
        for i, line in enumerate(lines):
            # Keep shebang at the very top
            if i == 0 and line.startswith('#!'):
                shebang = line
                continue
            
            # Keep encoding declaration near top
            if i < 3 and '# -*- coding:' in line:
                if shebang:
                    other_lines.insert(0, line)
                else:
                    shebang = line
                continue
            
            # Collect __future__ imports
            if line.strip().startswith('from __future__'):
                future_imports.append(line)
            else:
                other_lines.append(line)
        
        if future_imports:
            # Reconstruct file with proper order
            new_lines = []
            
            # Shebang/encoding first
            if shebang:
                new_lines.append(shebang)
            
            # Then __future__ imports
            new_lines.extend(future_imports)
            
            # Then everything else
            new_lines.extend(other_lines)
            
            new_content = '\n'.join(new_lines)
            
            # Write back
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix all defusedxml files in marker."""
    defusedxml_dir = Path("/home/graham/workspace/experiments/marker/.venv/lib/python3.10/site-packages/defusedxml")
    
    if not defusedxml_dir.exists():
        print("defusedxml directory not found")
        return
    
    print("🔧 Fixing defusedxml __future__ imports")
    print("=" * 60)
    
    fixed = 0
    for py_file in defusedxml_dir.glob("*.py"):
        if fix_future_imports(py_file):
            print(f"✓ Fixed {py_file.name}")
            fixed += 1
    
    print(f"\n✅ Fixed {fixed} files")


if __name__ == "__main__":
    main()