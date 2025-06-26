#!/usr/bin/env python3
"""Fix f-string syntax issues in universal_report_generator.py"""

import re
from pathlib import Path

def fix_fstring_syntax():
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    content = file_path.read_text()
    
    # Fix the specific line with the issue
    # Change {percentage_val:.1f} to use format() instead
    content = content.replace(
        '<span class="group-percent">{percentage_val:.1f}%</span>',
        '<span class="group-percent">{:.1f}%</span>'.format('{percentage_val}')
    )
    
    # Actually, let's use a simpler approach - convert to string formatting
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if i == 176 and 'percentage_val:.1f' in line:
            # Replace with proper formatting
            fixed_lines.append('                        <span class="group-percent">{0:.1f}%</span>".format(percentage_val)')
        elif i == 179 and 'style="width: {percentage_val}' in line:
            # Fix this line too
            fixed_lines.append('                        <div class="group-bar-fill" style="width: {0}%;"></div>".format(percentage_val)')
        else:
            fixed_lines.append(line)
    
    # Write back
    file_path.write_text('\n'.join(fixed_lines))
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_fstring_syntax()