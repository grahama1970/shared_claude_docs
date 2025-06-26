#!/usr/bin/env python3
"""Fix files where External Dependencies is outside the docstring."""

from pathlib import Path

def fix_external_deps(file_path):
    """Move External Dependencies inside docstring."""
    try:
        content = file_path.read_text()
        
        # Check if External Dependencies is outside the docstring
        if '"""\n\nExternal Dependencies:' in content:
            # Move it inside
            content = content.replace('"""\n\nExternal Dependencies:', '\nExternal Dependencies:')
            # Find the next """ and add it after
            lines = content.split('\n')
            new_lines = []
            in_docstring = False
            found_external_deps = False
            
            for i, line in enumerate(lines):
                if '"""' in line and not in_docstring:
                    in_docstring = True
                    new_lines.append(line)
                elif 'External Dependencies:' in line and not found_external_deps:
                    found_external_deps = True
                    new_lines.append(line)
                elif found_external_deps and not in_docstring and line.strip() == '':
                    # Add closing quotes before empty line
                    new_lines.append('"""')
                    new_lines.append(line)
                    found_external_deps = False
                else:
                    new_lines.append(line)
            
            new_content = '\n'.join(new_lines)
            if new_content != content:
                file_path.write_text(new_content)
                print(f"Fixed: {file_path}")
                return True
                
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

# Find Python files with this issue
base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src")
py_files = list(base_path.rglob("*.py"))

print(f"Checking {len(py_files)} Python files")

fixed_count = 0
for py_file in py_files:
    if fix_external_deps(py_file):
        fixed_count += 1

print(f"\nFixed {fixed_count} files")