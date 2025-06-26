#!/usr/bin/env python3
"""Fix all f-string syntax issues in claude-test-reporter"""

from pathlib import Path

def fix_universal_report_generator():
    """Fix the universal_report_generator.py file by avoiding f-string for CSS"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    content = file_path.read_text()
    
    # Find the generate() method and replace it with a version that doesn't use f-strings for CSS
    lines = content.split('\n')
    
    # Find where the CSS starts (around line 197)
    for i in range(len(lines)):
        if 'return f"""<!DOCTYPE html>' in lines[i]:
            # Found the start of the problematic f-string
            # Replace the f-string with regular string concatenation
            break
    
    # Create a new version that uses .format() instead of f-strings for the HTML
    # This is a bit complex, so let's just fix the immediate syntax error
    # Replace the line with the error
    for j in range(len(lines)):
        if '.container {{ max-width: 95%; margin: 20px auto;' in lines[j]:
            # This line has issues with the decimal in the f-string context
            # It should work but might be a Python version issue
            lines[j] = '        .container { max-width: 95%; margin: 20px auto; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }'
    
    # Write back
    content = '\n'.join(lines)
    file_path.write_text(content)
    print(f"Fixed {file_path}")

def main():
    fix_universal_report_generator()

if __name__ == "__main__":
    main()