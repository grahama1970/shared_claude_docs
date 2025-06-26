#!/usr/bin/env python3
"""Fix all module header syntax errors in ArXiv MCP server."""

import os
import re
from pathlib import Path

def fix_module_header(file_path):
    """Fix module header syntax in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Skip binary files or files with encoding issues
        return False
    
    # Pattern to match incomplete module headers
    pattern = r'("""[^"]*"""\n)(Module:\s*[^\n]+\n)(Description:\s*[^\n]+)(?!\n""")'
    
    def replacer(match):
        docstring = match.group(1)
        module_line = match.group(2)
        desc_line = match.group(3)
        # Move module and description inside the docstring
        return f'{docstring[:-4]}\n{module_line}{desc_line}\n"""\n'
    
    # Apply the fix
    fixed_content = re.sub(pattern, replacer, content)
    
    # Also fix standalone Module: lines outside docstrings
    if 'Module:' in fixed_content and '"""' in fixed_content:
        lines = fixed_content.split('\n')
        fixed_lines = []
        in_docstring = False
        
        for i, line in enumerate(lines):
            if '"""' in line:
                in_docstring = not in_docstring
            
            # If we find Module: outside a docstring, it's an error
            if not in_docstring and line.strip().startswith('Module:'):
                # This line should be inside the previous docstring
                # Find the last docstring and insert it there
                for j in range(len(fixed_lines) - 1, -1, -1):
                    if '"""' in fixed_lines[j] and fixed_lines[j].strip().endswith('"""'):
                        # Insert before the closing """
                        fixed_lines[j] = fixed_lines[j][:-3] + f"\n{line}\n" + '"""'
                        continue
            else:
                fixed_lines.append(line)
        
        fixed_content = '\n'.join(fixed_lines)
    
    if fixed_content != content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    return False

def main():
    """Fix all Python files in ArXiv MCP server."""
    arxiv_path = Path("/home/graham/workspace/mcp-servers/arxiv-mcp-server")
    
    if not arxiv_path.exists():
        print(f"ArXiv MCP server not found at {arxiv_path}")
        return
    
    fixed_count = 0
    for py_file in arxiv_path.rglob("*.py"):
        if fix_module_header(py_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()