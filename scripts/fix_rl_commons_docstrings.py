#!/usr/bin/env python3
"""
Module: fix_rl_commons_docstrings.py
Description: Fix all docstring issues in rl_commons project

External Dependencies:
- None

Example Usage:
>>> python fix_rl_commons_docstrings.py
"""

import re
from pathlib import Path


def fix_file_docstring(file_path: Path) -> bool:
    """Fix Module:/Description: lines outside docstring."""
    try:
        content = file_path.read_text()
        lines = content.split('\n')
        
        # Check for pattern: docstring on line 0, Module: on line 1, Description: on line 2
        if (len(lines) >= 3 and 
            lines[0].strip().startswith('"""') and
            lines[1].startswith('Module:') and 
            lines[2].startswith('Description:')):
            
            # This is the syntax error - Module/Description outside the docstring
            # We need to move the closing """ if it exists on line 0, or add newline
            
            if lines[0].strip().endswith('"""') and len(lines[0].strip()) > 6:
                # Single line docstring - expand it
                doc_content = lines[0].strip()[3:-3]
                lines[0] = '"""' + doc_content
                lines.insert(1, '')
                lines.insert(2, lines[2])  # Module line (now at index 2)
                lines.insert(3, lines[3])  # Description line (now at index 3)  
                lines.insert(4, '"""')
                # Remove the originals
                del lines[5]  # Remove old Module line
                del lines[5]  # Remove old Description line
            else:
                # Multi-line docstring but Module/Desc are outside
                # Simply comment them out for now
                lines[1] = '# ' + lines[1]
                lines[2] = '# ' + lines[2]
            
            # Write back
            file_path.write_text('\n'.join(lines))
            return True
        
        # Also check if Module: and Description: are on consecutive lines anywhere
        for i in range(len(lines) - 1):
            if (lines[i].startswith('Module:') and 
                i + 1 < len(lines) and
                lines[i + 1].startswith('Description:') and
                not lines[i].startswith('#')):
                
                # Found them - comment them out
                lines[i] = '# ' + lines[i]
                lines[i + 1] = '# ' + lines[i + 1]
                
                # Write back
                file_path.write_text('\n'.join(lines))
                return True
    
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False
    
    return False


def main():
    """Fix all rl_commons files."""
    base_path = Path('/home/graham/workspace/experiments/rl_commons')
    
    print("🔧 Fixing rl_commons docstring issues")
    print("=" * 60)
    
    # Files identified with issues
    problem_files = [
        'src/rl_commons/monitoring/tracker.py',
        'src/rl_commons/monitoring/__init__.py',
        'src/rl_commons/cli/__init__.py',
        'src/rl_commons/cli/app.py',
        'src/rl_commons/utils/__init__.py',
        'src/rl_commons/benchmarks/__init__.py',
        'src/rl_commons/__init__.py',
        'src/rl_commons/core/__init__.py',
        'src/rl_commons/safety/__init__.py',
        'src/rl_commons/algorithms/marl/__init__.py',
    ]
    
    fixed_count = 0
    
    for file_path in problem_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"Checking {file_path}...")
            if fix_file_docstring(full_path):
                print(f"  ✅ Fixed!")
                fixed_count += 1
            else:
                print(f"  ✓ No fix needed")
        else:
            print(f"  ❌ File not found: {file_path}")
    
    print(f"\n✨ Fixed {fixed_count} files")
    
    # Now let's also scan for any other files with the same issue
    print("\n🔍 Scanning for other files with similar issues...")
    
    additional_fixed = 0
    for py_file in (base_path / 'src').rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        # Skip already processed files
        relative_path = py_file.relative_to(base_path)
        if str(relative_path) in problem_files:
            continue
        
        if fix_file_docstring(py_file):
            print(f"  ✅ Fixed: {relative_path}")
            additional_fixed += 1
    
    if additional_fixed > 0:
        print(f"\n✨ Fixed {additional_fixed} additional files")
    
    print(f"\n🎯 Total files fixed: {fixed_count + additional_fixed}")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())