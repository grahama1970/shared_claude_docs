#!/usr/bin/env python3
"""
Module: fix_module_docstrings.py
Description: Fix malformed docstrings with Module: lines outside triple quotes

External Dependencies:
- None

Example Usage:
>>> python fix_module_docstrings.py
"""

import os
import re
from pathlib import Path


def fix_module_docstring(content: str) -> tuple[str, bool]:
    """Fix Module: line outside of docstring."""
    # Pattern to match Module: line followed by docstring
    pattern = r'^(Module:\s*[^\n]+)\n(""")'
    
    # Check if pattern exists
    if re.match(pattern, content, re.MULTILINE):
        # Fix by moving Module: inside the docstring
        fixed = re.sub(
            pattern,
            r'\2\n\1',
            content,
            count=1,
            flags=re.MULTILINE
        )
        return fixed, True
    
    # Also check for Description: outside docstring
    desc_pattern = r'^(Description:\s*[^\n]+)\n(""")'
    if re.match(desc_pattern, content, re.MULTILINE):
        fixed = re.sub(
            desc_pattern,
            r'\2\n\1',
            content,
            count=1,
            flags=re.MULTILINE
        )
        return fixed, True
    
    return content, False


def fix_project_files(project_path: Path) -> dict:
    """Fix all Python files in a project."""
    result = {
        'project': project_path.name,
        'files_checked': 0,
        'files_fixed': 0,
        'errors': []
    }
    
    src_dir = project_path / 'src'
    if not src_dir.exists():
        result['errors'].append('No src directory found')
        return result
    
    # Find all Python files
    for py_file in src_dir.rglob('*.py'):
        if '__pycache__' in str(py_file):
            continue
        
        result['files_checked'] += 1
        
        try:
            content = py_file.read_text()
            fixed_content, was_fixed = fix_module_docstring(content)
            
            if was_fixed:
                py_file.write_text(fixed_content)
                result['files_fixed'] += 1
                print(f"  ✅ Fixed: {py_file.relative_to(project_path)}")
        
        except Exception as e:
            result['errors'].append(f"{py_file}: {e}")
    
    return result


def main():
    """Fix docstrings in all Granger projects."""
    projects = [
        '/home/graham/workspace/experiments/granger_hub',
        '/home/graham/workspace/experiments/rl_commons',
        '/home/graham/workspace/experiments/claude-test-reporter',
        '/home/graham/workspace/experiments/world_model',
        '/home/graham/workspace/experiments/sparta',
        '/home/graham/workspace/experiments/marker',
        '/home/graham/workspace/experiments/arangodb',
        '/home/graham/workspace/experiments/llm_call',
        '/home/graham/workspace/experiments/unsloth_wip',
    ]
    
    print("🔧 Fixing Module Docstring Syntax Errors")
    print("=" * 60)
    
    total_fixed = 0
    
    for project_path in projects:
        path = Path(project_path)
        if not path.exists():
            print(f"❌ Skipping {path.name}: does not exist")
            continue
        
        print(f"\n📁 Checking {path.name}...")
        result = fix_project_files(path)
        
        if result['files_fixed'] > 0:
            print(f"  Fixed {result['files_fixed']} files")
            total_fixed += result['files_fixed']
        elif result['files_checked'] > 0:
            print(f"  ✓ No fixes needed ({result['files_checked']} files checked)")
        
        if result['errors']:
            print(f"  ⚠️  Errors: {len(result['errors'])}")
            for err in result['errors'][:3]:
                print(f"    - {err}")
    
    print(f"\n✨ Total files fixed: {total_fixed}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())