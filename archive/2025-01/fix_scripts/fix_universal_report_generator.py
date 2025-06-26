#!/usr/bin/env python3
"""Fix the universal report generator CSS f-string issues for Python 3.12"""

from pathlib import Path

def fix_generator():
    """Fix the universal report generator by replacing problematic f-string CSS"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find the start of the problematic f-string
    start_marker = '# Using string template to avoid f-string issues with CSS\n        return f"""<!DOCTYPE html>'
    
    if start_marker not in content:
        print("Start marker not found!")
        return
    
    # Split the content at the marker
    before_fstring = content[:content.index(start_marker)]
    after_marker = content[content.index(start_marker):]
    
    # Find the end of the f-string (it ends with </html>""")
    end_marker = '</html>"""'
    if end_marker not in after_marker:
        print("End marker not found!")
        return
    
    end_idx = after_marker.index(end_marker) + len(end_marker)
    fstring_content = after_marker[:end_idx]
    after_fstring = after_marker[end_idx:]
    
    # Replace the f-string with a regular string and .format()
    # First, replace all {{ and }} with { and } for proper formatting
    new_content = fstring_content.replace('return f"""', 'return """')
    new_content = new_content.replace('{{', '{')
    new_content = new_content.replace('}}', '}')
    
    # Now we need to handle the dynamic values
    # Find all {self.something} and {variable} patterns
    import re
    
    # Extract all the format variables
    format_vars = []
    
    # Common patterns in the HTML
    patterns_to_replace = [
        (r'{self.theme_color}', 'theme_color'),
        (r'{self.logo}', 'logo'),
        (r'{self.title}', 'title'),
        (r'{summary_cards_html}', 'summary_cards_html'),
        (r'{group_summary_html}', 'group_summary_html'),
        (r'{column_headers_html}', 'column_headers_html'),
        (r'{table_rows_html}', 'table_rows_html'),
        (r'{len\(data\)}', 'data_length'),
        (r'{json\.dumps\(columns\)}', 'columns_json'),
        (r'{datetime\.now\(\)\.strftime\("%B %d, %Y at %I:%M %p"\)}', 'datetime_str'),
        (r'{self\.title\.replace\(" ", "_"\)\.lower\(\)}', 'title_snake'),
    ]
    
    # Replace patterns with placeholders
    for pattern, placeholder in patterns_to_replace:
        new_content = re.sub(pattern, '{' + placeholder + '}', new_content)
    
    # Add .format() call
    format_args = """
            theme_color=self.theme_color,
            logo=self.logo,
            title=self.title,
            summary_cards_html=summary_cards_html,
            group_summary_html=group_summary_html,
            column_headers_html=column_headers_html,
            table_rows_html=table_rows_html,
            data_length=len(data),
            columns_json=json.dumps(columns),
            datetime_str=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
            title_snake=self.title.replace(" ", "_").lower()
        )"""
    
    # Find where the triple quotes end
    new_content = new_content.replace('</html>"""', '</html>""".format(' + format_args)
    
    # Reassemble the file
    final_content = before_fstring + new_content + after_fstring
    
    # Write back
    file_path.write_text(final_content)
    print(f"Fixed {file_path}")
    
    # Verify the fix
    import subprocess
    result = subprocess.run(
        ['python', '-m', 'py_compile', str(file_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ File compiles successfully!")
    else:
        print(f"❌ Still has errors:\n{result.stderr}")

if __name__ == "__main__":
    fix_generator()