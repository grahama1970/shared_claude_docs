#!/usr/bin/env python3
"""Final fix for universal_report_generator.py"""

from pathlib import Path

def fix_file():
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    # Read the entire file
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the generate method
    in_template = False
    template_start = None
    
    for i, line in enumerate(lines):
        if 'return """<!DOCTYPE html>' in line:
            in_template = True
            template_start = i
            # Change back to f-string but escape percentages properly
            lines[i] = '        return f"""<!DOCTYPE html>\n'
        
        # Fix percentage issues in CSS by escaping them
        if in_template and '95%' in line:
            lines[i] = line.replace('95%', '95' + chr(37))  # chr(37) is %
        if in_template and '100%' in line:
            lines[i] = line.replace('100%', '100' + chr(37))
        if in_template and '90%' in line:
            lines[i] = line.replace('90%', '90' + chr(37))
        if in_template and '80%' in line:
            lines[i] = line.replace('80%', '80' + chr(37))
        if in_template and '50%' in line:
            lines[i] = line.replace('50%', '50' + chr(37))
            
        # Remove the .format() call we added
        if '</body></html>""".format(' in line:
            lines[i] = '</body></html>"""\n'
            # Remove the format lines
            j = i + 1
            while j < len(lines) and ')' not in lines[j]:
                lines[j] = ''
                j += 1
            if j < len(lines):
                lines[j] = ''
    
    # Write back
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Fixed {file_path}")

if __name__ == "__main__":
    fix_file()