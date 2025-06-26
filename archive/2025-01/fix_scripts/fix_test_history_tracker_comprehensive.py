#!/usr/bin/env python3
"""Comprehensive fix for test_history_tracker.py f-string issues"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from pathlib import Path

def fix_tracker():
    """Replace the problematic method with a working version"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/tracking/test_history_tracker.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find the line with the return f""" statement
    lines = content.split('\n')
    
    # Find the start of the problematic f-string (around line 288)
    for i, line in enumerate(lines):
        if 'return f"""<!DOCTYPE html>' in line:
            # Found it, now we need to replace the f-string with regular string formatting
            # Replace f""" with """ and add .format() at the end
            lines[i] = '        return """<!DOCTYPE html>'
            
            # Find the closing """ and add .format()
            for j in range(i+1, len(lines)):
                if lines[j].strip() == '"""':
                    # Add format arguments
                    format_args = []
                    format_args.append("project_name=project_name")
                    format_args.append("flaky_tests_html=flaky_tests_html")
                    format_args.append("summary_pass_rate=summary['pass_rate']")
                    format_args.append("summary_total_runs=summary['total_runs']")
                    format_args.append("summary_flaky_count=summary['flaky_count']")
                    format_args.append("chart_svg=chart_svg")
                    format_args.append("datetime=datetime")
                    
                    lines[j] = '        """.format(' + ', '.join(format_args) + ')'
                    break
            break
    
    # Replace all {variable} with {variable} format placeholders
    # But we need to be careful about CSS double braces
    new_content = '\n'.join(lines)
    
    # Write back
    file_path.write_text(new_content)
    print(f"Updated {file_path}")
    
    # Test compilation
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
        print("\nTrying alternative approach...")
        
        # Alternative: Replace the entire generate_history_report method
        content = file_path.read_text()
        
        # Find where the method starts
        method_start = content.find("def generate_history_report(")
        if method_start == -1:
            print("Could not find generate_history_report method")
            return
            
        # Find the end of the method (next def or class)
        method_end = content.find("\n    def ", method_start + 1)
        if method_end == -1:
            method_end = content.find("\nclass ", method_start + 1)
        if method_end == -1:
            method_end = len(content)
        
        # Extract the method
        method_content = content[method_start:method_end]
        
        # Replace the CSS numeric values that are causing issues
        # In CSS, we don't need to worry about f-string formatting
        replacements = [
            ('max-width: 1200px', 'max-width: 1200' + 'px'),
            ('font-size: 2.5em', 'font-size: 2.5' + 'em'),
            ('font-size: 1.8em', 'font-size: 1.8' + 'em'),
            ('font-size: 0.9em', 'font-size: 0.9' + 'em'),
            ('font-size: 2em', 'font-size: 2' + 'em'),
            ('line-height: 1.6', 'line-height: 1.6'),
            ('stroke-width="3"', 'stroke-width="3"'),
            ('letter-spacing: 0.1em', 'letter-spacing: 0.1' + 'em'),
            ('letter-spacing: 0.05em', 'letter-spacing: 0.05' + 'em'),
        ]
        
        for old, new in replacements:
            method_content = method_content.replace(old, new)
        
        # Reconstruct the file
        new_content = content[:method_start] + method_content + content[method_end:]
        file_path.write_text(new_content)
        
        # Test again
        result = subprocess.run(
            ['python', '-m', 'py_compile', str(file_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Alternative approach worked! File compiles successfully!")
        else:
            print(f"❌ Still has errors with alternative approach:\n{result.stderr}")

if __name__ == "__main__":
    fix_tracker()