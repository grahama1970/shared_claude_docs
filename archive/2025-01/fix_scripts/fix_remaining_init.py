#!/usr/bin/env python3
"""Fix remaining __init__.py files with incorrect docstring format."""

import re
from pathlib import Path

def fix_init_file(file_path):
    """Fix docstring in __init__.py that has Module: outside quotes."""
    try:
        content = file_path.read_text()
        
        # Check if Description: is outside quotes
        lines = content.split('\n')
        fixed_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Look for Module: or Description: at start of line
            if (line.strip().startswith('Module:') or 
                line.strip().startswith('Description:')) and i > 0:
                
                # Check previous line for docstring
                prev_line = lines[i-1].strip()
                if prev_line.endswith('"""'):
                    # Move Module:/Description: inside docstring
                    fixed_lines[-1] = prev_line[:-3]  # Remove """
                    fixed_lines.append("")
                    fixed_lines.append(line)
                    
                    # Look for Description: if this was Module:
                    if line.strip().startswith('Module:') and i+1 < len(lines):
                        if lines[i+1].strip().startswith('Description:'):
                            fixed_lines.append(lines[i+1])
                            i += 1
                    
                    fixed_lines.append('"""')
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
            i += 1
        
        new_content = '\n'.join(fixed_lines)
        if new_content != content:
            file_path.write_text(new_content)
            print(f"Fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# Find all __init__.py files
base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src")
init_files = list(base_path.rglob("__init__.py"))

print(f"Checking {len(init_files)} __init__.py files")

fixed_count = 0
for init_file in init_files:
    if fix_init_file(init_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} files")