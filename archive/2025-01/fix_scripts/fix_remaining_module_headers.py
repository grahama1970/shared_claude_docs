#!/usr/bin/env python3
"""Fix remaining module header issues"""

from pathlib import Path
import re

def fix_file(file_path):
    """Fix a single file's module header"""
    content = file_path.read_text()
    lines = content.split('\n')
    
    # Find patterns like:
    # """some docstring"""
    # Module: filename.py
    # Description: ...
    # import ...
    
    fixed = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a docstring followed by Module:
        if (line.strip().startswith('"""') and line.strip().endswith('"""') and 
            i + 1 < len(lines) and lines[i + 1].startswith('Module:')):
            
            # Extract the original docstring content
            orig_docstring = line.strip()[3:-3].strip()
            
            # Get Module and Description lines
            module_line = lines[i + 1]
            desc_line = None
            skip_lines = 2
            
            if i + 2 < len(lines) and lines[i + 2].startswith('Description:'):
                desc_line = lines[i + 2]
                skip_lines = 3
            
            # Create new docstring
            new_lines.append('"""')
            new_lines.append(module_line)
            if desc_line:
                new_lines.append(desc_line)
            new_lines.append('')
            if orig_docstring:
                new_lines.append(orig_docstring)
            new_lines.append('"""')
            
            i += skip_lines
            fixed = True
            
        else:
            new_lines.append(line)
            i += 1
    
    if fixed:
        file_path.write_text('\n'.join(new_lines))
        print(f"Fixed {file_path}")
        return True
    return False

def main():
    """Fix all remaining module header issues"""
    base_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter")
    
    files_to_check = [
        "cli/validate.py",
        "cli/slash_mcp_mixin.py",
        "cli/code_review.py",
        "monitoring/hallucination_monitor.py",
        "analyzers/claim_verifier.py",
        "analyzers/mock_detector.py",
        "analyzers/integration_tester.py",
        "analyzers/llm_test_analyzer.py",
        "analyzers/pattern_analyzer.py",
        "analyzers/implementation_verifier.py",
        "analyzers/comprehensive_analyzer.py",
        "analyzers/realtime_monitor.py",
        "analyzers/honeypot_enforcer.py",
    ]
    
    fixed_count = 0
    for file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            if fix_file(full_path):
                fixed_count += 1
                
    print(f"\nFixed {fixed_count} files")

if __name__ == "__main__":
    main()