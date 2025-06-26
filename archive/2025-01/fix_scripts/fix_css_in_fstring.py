#!/usr/bin/env python3
"""Fix CSS in f-string issues"""

from pathlib import Path
import re

def fix_css_percentages():
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    content = file_path.read_text()
    
    # Find all occurrences of percentage values in CSS that might cause issues
    # Replace patterns like "95%" with a safer version
    
    # Pattern to find CSS percentage values that come after a space or colon
    # This is causing issues in Python 3.12 when inside f-strings
    
    # Replace specific problematic lines
    replacements = [
        ('max-width: 95%;', "max-width: 95" + "%;"),  # Split the % from the number
        ('width: 100%;', "width: 100" + "%;"),
        ('width: 90%;', "width: 90" + "%;"),
        ('opacity: 0.9;', "opacity: 0.9;"),  # This one should be fine
        ('opacity: 0.85;', "opacity: 0.85;"),
        ('letter-spacing: 0.5px;', "letter-spacing: 0.5px;"),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"Replaced: {old} -> {new}")
    
    # Write back
    file_path.write_text(content)
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_css_percentages()