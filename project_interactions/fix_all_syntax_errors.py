#!/usr/bin/env python3
"""
Module: fix_all_syntax_errors.py
Description: Find and fix all syntax errors in Granger modules

External Dependencies:
- None (uses only built-in modules)

Sample Input:
>>> fixer = SyntaxErrorFixer()
>>> fixer.fix_all_modules()

Expected Output:
>>> Fixed 5 syntax errors in 3 files
"""

import os
import re
from pathlib import Path

class SyntaxErrorFixer:
    def __init__(self):
        self.fixed_count = 0
        self.errors_found = []
        
    def fix_module_docstring(self, file_path: Path) -> bool:
        """Fix module docstring placement in a file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if file has misplaced Module: docstring
            if 'Module:' in content and not content.strip().startswith('"""'):
                lines = content.split('\n')
                
                # Find the Module: line
                module_line_idx = None
                for i, line in enumerate(lines):
                    if 'Module:' in line and not line.strip().startswith('#'):
                        module_line_idx = i
                        break
                
                if module_line_idx is not None and module_line_idx > 5:
                    # Extract module docstring lines
                    docstring_lines = []
                    
                    # Look for docstring start before Module:
                    start_idx = module_line_idx - 1
                    while start_idx >= 0 and not lines[start_idx].strip().startswith('"""'):
                        start_idx -= 1
                    
                    if start_idx >= 0:
                        # Found docstring start, extract it
                        end_idx = module_line_idx
                        while end_idx < len(lines) and '"""' not in lines[end_idx]:
                            end_idx += 1
                        
                        # Extract the docstring
                        docstring_lines = lines[start_idx:end_idx+1]
                        
                        # Remove old docstring location
                        for i in range(end_idx, start_idx-1, -1):
                            del lines[i]
                        
                        # Insert at beginning
                        for i, line in enumerate(docstring_lines):
                            lines.insert(i, line)
                        
                        # Write back
                        with open(file_path, 'w') as f:
                            f.write('\n'.join(lines))
                        
                        self.fixed_count += 1
                        return True
                        
        except Exception as e:
            self.errors_found.append({
                "file": str(file_path),
                "error": str(e)
            })
        
        return False
    
    def fix_all_modules(self):
        """Fix syntax errors in all Granger modules"""
        print("🔧 Fixing syntax errors in Granger modules...")
        
        modules_base = Path("/home/graham/workspace/experiments")
        modules = [
            "sparta", "arangodb", "marker", "youtube_transcripts",
            "llm_call", "gitget", "world_model", "rl_commons",
            "claude-test-reporter", "granger_hub"
        ]
        
        for module_name in modules:
            module_path = modules_base / module_name
            if module_path.exists():
                print(f"\nChecking {module_name}...")
                
                # Find all Python files
                py_files = list(module_path.rglob("*.py"))
                
                for py_file in py_files:
                    # Skip test files and __pycache__
                    if "__pycache__" in str(py_file) or ".venv" in str(py_file):
                        continue
                        
                    if self.fix_module_docstring(py_file):
                        print(f"  ✅ Fixed: {py_file.relative_to(module_path)}")
        
        print(f"\n📊 Summary:")
        print(f"  Fixed {self.fixed_count} syntax errors")
        print(f"  Encountered {len(self.errors_found)} errors")
        
        if self.errors_found:
            print("\n❌ Errors encountered:")
            for err in self.errors_found[:5]:  # Show first 5
                print(f"  - {err['file']}: {err['error']}")

if __name__ == "__main__":
    fixer = SyntaxErrorFixer()
    fixer.fix_all_modules()