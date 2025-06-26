#!/usr/bin/env python3
"""Fix f-string issues in universal_report_generator.py"""

from pathlib import Path

def fix_file():
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    content = file_path.read_text()
    
    # Find and replace the problematic multi-line f-string
    # Look for the specific pattern and replace with a working version
    old_pattern = '''                group_summary_html += f"""
                <div class="group-item">
                    <div class="group-name">{self._format_value(group_name_str)}</div>
                    <div class="group-stats">
                        <span class="group-count">{len(items_list)} items</span>
                        <span class="group-percent">{percentage_val:.1f}%</span>
                    </div>
                    <div class="group-bar">
                        <div class="group-bar-fill" style="width: {percentage_val}%;"></div>
                    </div>
                </div>
                """'''
    
    # Use a simpler approach - concatenate strings
    new_pattern = '''                group_summary_html += (
                    f'<div class="group-item">'
                    f'<div class="group-name">{self._format_value(group_name_str)}</div>'
                    f'<div class="group-stats">'
                    f'<span class="group-count">{len(items_list)} items</span>'
                    f'<span class="group-percent">{percentage_val:.1f}%</span>'
                    f'</div>'
                    f'<div class="group-bar">'
                    f'<div class="group-bar-fill" style="width: {percentage_val}%;"></div>'
                    f'</div>'
                    f'</div>'
                )'''
    
    # Replace
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        file_path.write_text(content)
        print(f"✅ Fixed {file_path}")
    else:
        print("Pattern not found, trying alternative fix...")
        
        # Alternative: Fix line by line
        lines = content.split('\n')
        for i in range(len(lines)):
            if 'group_summary_html += f"""' in lines[i]:
                # Find the end of this f-string
                j = i + 1
                while j < len(lines) and '"""' not in lines[j]:
                    j += 1
                
                # Replace this section with concatenated f-strings
                indent = '                '
                new_lines = [
                    f"{indent}group_summary_html += (",
                    f"{indent}    f'<div class=\"group-item\">'"
                    f"{indent}    f'<div class=\"group-name\">" + "{self._format_value(group_name_str)}</div>'",
                    f"{indent}    f'<div class=\"group-stats\">'"
                    f"{indent}    f'<span class=\"group-count\">" + "{len(items_list)} items</span>'",
                    f"{indent}    f'<span class=\"group-percent\">" + "{percentage_val:.1f}%</span>'",
                    f"{indent}    f'</div>'"
                    f"{indent}    f'<div class=\"group-bar\">'"
                    f"{indent}    f'<div class=\"group-bar-fill\" style=\"width: " + "{percentage_val}%;\"></div>'",
                    f"{indent}    f'</div>'"
                    f"{indent}    f'</div>'"
                    f"{indent})"
                ]
                
                # Replace the lines
                lines[i:j+1] = new_lines
                break
        
        content = '\n'.join(lines)
        file_path.write_text(content)
        print(f"✅ Applied alternative fix to {file_path}")

if __name__ == "__main__":
    fix_file()