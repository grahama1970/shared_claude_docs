#!/usr/bin/env python3
"""Fix all Module: headers in docstrings"""

import re
from pathlib import Path

def fix_module_headers():
    """Fix all Python files with incorrect Module: headers"""
    
    # Find all Python files with Module: at line start
    files_to_fix = []
    base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter")
    
    for py_file in base_path.rglob("*.py"):
        try:
            content = py_file.read_text()
            lines = content.split('\n')
            
            # Check if any line starts with "Module:" (not in docstring)
            for i, line in enumerate(lines):
                if line.startswith("Module:") and i > 0:
                    # Check if it's outside a docstring
                    if i == 0 or not (lines[i-1].strip() == '"""' or lines[i-1].strip().endswith('"""')):
                        files_to_fix.append(py_file)
                        break
        except Exception as e:
            print(f"Error reading {py_file}: {e}")
    
    print(f"Found {len(files_to_fix)} files to fix")
    
    # Fix each file
    for py_file in files_to_fix:
        try:
            content = py_file.read_text()
            lines = content.split('\n')
            
            # Find the Module: line
            module_line_idx = -1
            for i, line in enumerate(lines):
                if line.startswith("Module:"):
                    module_line_idx = i
                    break
            
            if module_line_idx == -1:
                continue
                
            # Extract the module info
            module_line = lines[module_line_idx]
            
            # Check if there's already a docstring
            has_docstring = False
            docstring_start = -1
            
            for i in range(min(module_line_idx, 5)):
                if lines[i].strip().startswith('"""'):
                    has_docstring = True
                    docstring_start = i
                    break
            
            if has_docstring and docstring_start < module_line_idx:
                # Move the Module: line inside the existing docstring
                # Find the end of the docstring
                docstring_end = -1
                in_docstring = False
                for i in range(docstring_start, len(lines)):
                    if lines[i].strip().startswith('"""'):
                        if i > docstring_start:
                            docstring_end = i
                            break
                        else:
                            in_docstring = True
                    elif lines[i].strip().endswith('"""') and in_docstring:
                        docstring_end = i
                        break
                
                if docstring_end > docstring_start:
                    # Insert Module: line after the opening """
                    lines.pop(module_line_idx)
                    if module_line_idx > docstring_start + 1:
                        module_line_idx -= 1
                    lines.insert(docstring_start + 1, module_line)
                    
                    # Also check for Description: line
                    desc_idx = -1
                    for i in range(module_line_idx + 1, min(module_line_idx + 5, len(lines))):
                        if lines[i].startswith("Description:"):
                            desc_idx = i
                            break
                    
                    if desc_idx > 0 and desc_idx > docstring_end:
                        desc_line = lines.pop(desc_idx)
                        lines.insert(docstring_start + 2, desc_line)
            else:
                # Create a new docstring
                # Check for a Description: line following Module:
                desc_line = None
                if module_line_idx + 1 < len(lines) and lines[module_line_idx + 1].startswith("Description:"):
                    desc_line = lines[module_line_idx + 1]
                    lines.pop(module_line_idx + 1)
                
                # Remove the Module: line
                lines.pop(module_line_idx)
                
                # Create new docstring at the beginning
                new_docstring = ['"""', module_line]
                if desc_line:
                    new_docstring.append(desc_line)
                new_docstring.append('"""')
                new_docstring.append('')
                
                # Insert at beginning (after shebang if present)
                insert_idx = 0
                if lines and lines[0].startswith("#!"):
                    insert_idx = 1
                
                for i, line in enumerate(new_docstring):
                    lines.insert(insert_idx + i, line)
            
            # Write back
            new_content = '\n'.join(lines)
            py_file.write_text(new_content)
            print(f"Fixed {py_file}")
            
        except Exception as e:
            print(f"Error fixing {py_file}: {e}")

if __name__ == "__main__":
    fix_module_headers()