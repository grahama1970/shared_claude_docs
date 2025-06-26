#!/usr/bin/env python3
"""Fix incorrect docstring syntax in all Python files."""

import re
from pathlib import Path

def fix_docstring(file_path):
    """Fix docstring syntax in a Python file."""
    try:
        content = file_path.read_text()
        original = content
        
        # Pattern 1: Module: on line after docstring
        pattern1 = r'("""[^"]*""")\s*\n(Module:.*?)\n(Description:.*?)(?=\n)'
        if re.search(pattern1, content):
            content = re.sub(
                pattern1,
                r'"""\n\1\n\n\2\n\3\n"""',
                content,
                flags=re.MULTILINE
            )
        
        # Pattern 2: Module: without proper docstring enclosure
        lines = content.split('\n')
        new_lines = []
        in_docstring = False
        docstring_start = -1
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Track docstring state
            if '"""' in line:
                count = line.count('"""')
                if count == 1:
                    in_docstring = not in_docstring
                    if in_docstring:
                        docstring_start = i
                elif count == 2:
                    # Single line docstring
                    pass
            
            # Check for Module: pattern outside docstring
            if not in_docstring and line.strip().startswith('Module:') and i > 0:
                # This Module: line should be inside the previous docstring
                if docstring_start >= 0 and i - docstring_start < 5:
                    # Find the closing """ and move it after Description
                    j = i
                    while j < len(lines) and not lines[j].strip().startswith('Description:'):
                        j += 1
                    if j < len(lines):
                        # Insert closing """ after Description line
                        lines[j] = lines[j] + '\n"""'
                        in_docstring = False
            
            i += 1
        
        # If content changed, write it back
        if content != original:
            file_path.write_text(content)
            print(f"Fixed: {file_path}")
            return True
            
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# More robust fix
def fix_docstring_v2(file_path):
    """More robust docstring fix."""
    try:
        content = file_path.read_text()
        
        # Check if file has Module: and Description: that should be in docstring
        if 'Module:' in content and 'Description:' in content:
            lines = content.split('\n')
            new_lines = []
            i = 0
            
            while i < len(lines):
                line = lines[i].rstrip()
                
                # Look for docstring start followed by Module:
                if i < len(lines) - 2 and '"""' in line and 'Module:' in lines[i+1]:
                    # Check if Module: line is not inside the docstring
                    if line.endswith('"""') and not line.startswith('"""'):
                        # Opening and closing on same line, Module: is outside
                        new_lines.append(line[:-3])  # Remove closing """
                        new_lines.append("")
                        new_lines.append(lines[i+1])  # Module: line
                        i += 2
                        # Look for Description: line
                        if i < len(lines) and 'Description:' in lines[i]:
                            new_lines.append(lines[i])
                            new_lines.append('"""')
                            i += 1
                        continue
                
                # Look for standalone Module: line
                if line.strip().startswith('Module:') and i > 0:
                    # Check if previous line has """
                    prev = lines[i-1].rstrip()
                    if prev.endswith('"""'):
                        # Need to move Module: inside docstring
                        new_lines[-1] = prev[:-3]  # Remove """ from previous line
                        new_lines.append("")
                        new_lines.append(line)
                        # Look for Description:
                        if i + 1 < len(lines) and 'Description:' in lines[i+1]:
                            new_lines.append(lines[i+1])
                            new_lines.append('"""')
                            i += 2
                            continue
                
                new_lines.append(line)
                i += 1
            
            new_content = '\n'.join(new_lines)
            if new_content != content:
                file_path.write_text(new_content)
                print(f"Fixed: {file_path}")
                return True
                
    except Exception as e:
        print(f"Error in v2 fix for {file_path}: {e}")
    return False

# Find all Python files
base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src")
py_files = list(base_path.rglob("*.py"))

print(f"Found {len(py_files)} Python files")

fixed_count = 0
for py_file in py_files:
    if fix_docstring_v2(py_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} files")