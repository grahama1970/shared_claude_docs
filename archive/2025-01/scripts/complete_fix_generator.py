#!/usr/bin/env python3
"""Complete fix for the universal report generator"""

from pathlib import Path

def fix_generator():
    """Fix the universal report generator by rewriting the problematic generate method"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    # Read the file
    content = file_path.read_text()
    
    # The issue is that Python 3.12 has stricter parsing for f-strings
    # Let's replace the CSS percentages with a workaround
    
    # Replace percentage values in CSS with escaped versions
    css_fixes = [
        ('max-width: 95%', 'max-width: 95%%'),  # Double percent escapes it
        ('width: 100%', 'width: 100%%'),
        ('width: 90%', 'width: 90%%'),
        ('width: 80%', 'width: 80%%'),
        ('width: 50%', 'width: 50%%'),
        ('height: 100%', 'height: 100%%'),
        ('top: 50%', 'top: 50%%'),
        ('translateY(-50%)', 'translateY(-50%%)'),
    ]
    
    # Apply fixes
    for old, new in css_fixes:
        content = content.replace(old, new)
    
    # Write back
    file_path.write_text(content)
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_generator()