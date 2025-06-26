#!/usr/bin/env python3
"""
Module: fix_all_indentation_errors.py
Description: Fix all indentation errors in test files across Granger projects

External Dependencies:
- ast: https://docs.python.org/3/library/ast.html

Example Usage:
>>> python fix_all_indentation_errors.py
"""

import ast
import os
import re
from pathlib import Path
from typing import List, Tuple


def fix_indentation_error(file_path: Path) -> bool:
    """Fix indentation errors in a Python file."""
    try:
        content = file_path.read_text()
        
        # Try to parse the file
        try:
            ast.parse(content)
            return False  # No syntax errors
        except IndentationError as e:
            lines = content.split('\n')
            line_num = e.lineno - 1
            
            if 0 <= line_num < len(lines):
                # Get the problematic line and previous line
                current_line = lines[line_num]
                
                # Find the previous non-empty line
                prev_line_num = line_num - 1
                while prev_line_num >= 0 and not lines[prev_line_num].strip():
                    prev_line_num -= 1
                
                if prev_line_num >= 0:
                    prev_line = lines[prev_line_num]
                    
                    # If previous line ends with colon, indent properly
                    if prev_line.strip().endswith(':'):
                        # Calculate proper indentation
                        prev_indent = len(prev_line) - len(prev_line.lstrip())
                        new_indent = prev_indent + 4
                        
                        # Fix the current line
                        lines[line_num] = ' ' * new_indent + current_line.lstrip()
                        
                        # Write back
                        file_path.write_text('\n'.join(lines))
                        return True
                    
                    # If it's an unexpected unindent, check if we need to dedent
                    elif "unexpected unindent" in str(e):
                        # Find the matching indentation level
                        target_indent = None
                        for i in range(prev_line_num, -1, -1):
                            if lines[i].strip() and not lines[i].strip().startswith('#'):
                                line_indent = len(lines[i]) - len(lines[i].lstrip())
                                if line_indent < len(prev_line) - len(prev_line.lstrip()):
                                    target_indent = line_indent
                                    break
                        
                        if target_indent is not None:
                            lines[line_num] = ' ' * target_indent + current_line.lstrip()
                            file_path.write_text('\n'.join(lines))
                            return True
                
        except SyntaxError as e:
            # Handle other syntax errors
            if "for module in # REMOVED:" in content:
                # Fix the broken mock removal
                content = re.sub(r'for module in # REMOVED:.*', 'pass  # Mock loop removed', content)
                file_path.write_text(content)
                return True
                
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return False


def fix_project_indentation(project_path: Path) -> List[str]:
    """Fix all indentation errors in a project."""
    fixes = []
    
    # Find all Python test files
    for py_file in project_path.rglob("test_*.py"):
        if ".venv" in str(py_file) or "archive" in str(py_file):
            continue
        
        # Try to fix indentation errors
        max_attempts = 5
        for attempt in range(max_attempts):
            if fix_indentation_error(py_file):
                if attempt == 0:
                    fixes.append(f"Fixed indentation in {py_file.name}")
                break
            else:
                # No more errors
                break
    
    return fixes


def main():
    """Fix indentation errors in all Granger projects."""
    projects = [
        ("granger_hub", "/home/graham/workspace/experiments/granger_hub"),
        ("sparta", "/home/graham/workspace/experiments/sparta"),
        ("marker", "/home/graham/workspace/experiments/marker"),
        ("arangodb", "/home/graham/workspace/experiments/arangodb"),
        ("unsloth_wip", "/home/graham/workspace/experiments/unsloth_wip"),
        ("youtube_transcripts", "/home/graham/workspace/experiments/youtube_transcripts"),
        ("arxiv-mcp-server", "/home/graham/workspace/mcp-servers/arxiv-mcp-server"),
        ("gitget", "/home/graham/workspace/experiments/gitget"),
        ("runpod_ops", "/home/graham/workspace/experiments/runpod_ops"),
        ("aider-daemon", "/home/graham/workspace/experiments/aider-daemon"),
    ]
    
    print("🔧 Fixing Indentation Errors in All Projects")
    print("=" * 60)
    
    for project_name, project_path in projects:
        project_path = Path(project_path)
        if not project_path.exists():
            continue
        
        print(f"\n📦 {project_name}")
        fixes = fix_project_indentation(project_path)
        
        if fixes:
            for fix in fixes:
                print(f"  ✓ {fix}")
        else:
            print("  ℹ️  No indentation errors found")
    
    print("\n✅ Indentation fix complete!")


if __name__ == "__main__":
    main()