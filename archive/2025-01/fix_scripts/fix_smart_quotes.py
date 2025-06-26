#!/usr/bin/env python3
"""Fix smart quotes in Python files"""

from pathlib import Path

def fix_file(filepath):
    """Fix smart quotes in a file"""
    content = filepath.read_bytes()
    
    # Replace smart quotes with regular quotes
    replacements = [
        (b'\xe2\x80\x99', b"'"),  # Right single quotation mark
        (b'\xe2\x80\x98', b"'"),  # Left single quotation mark
        (b'\xe2\x80\x9c', b'"'),  # Left double quotation mark
        (b'\xe2\x80\x9d', b'"'),  # Right double quotation mark
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    filepath.write_bytes(content)
    print(f"Fixed {filepath}")

if __name__ == "__main__":
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/test_result_verifier.py")
    fix_file(file_path)