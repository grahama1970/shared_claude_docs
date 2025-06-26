#!/usr/bin/env python3
"""Fix multi_project_dashboard.py percentage issues"""

from pathlib import Path
import re

def fix_dashboard():
    """Fix the multi_project_dashboard.py file"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/multi_project_dashboard.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find all f-strings that contain percentage values and convert them
    # Strategy: Convert problematic f-strings to use .format() instead
    
    # First, let's find the specific problematic line
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Check if this line contains the problematic pattern
        if ':.1f}%' in line and '<span' in line:
            # This is likely inside an f-string with percentage
            # Replace the % with %% for proper escaping
            line = line.replace(':.1f}%<', ':.1f}%%<')
            line = line.replace(':.0f}%<', ':.0f}%%<')
        elif 'style="width:' in line and '}%"' in line:
            # This is a width style with percentage
            # We need to handle this differently - extract the calculation
            # and format it separately
            if 'f"""' in content[:content.find(line)]:
                # We're in an f-string, need to escape the %
                line = line.replace('}%"', '}%%"')
        
        fixed_lines.append(line)
    
    # Write back
    new_content = '\n'.join(fixed_lines)
    file_path.write_text(new_content)
    print(f"Fixed {file_path}")
    
    # Verify it compiles
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
        # If it still has errors, we might need a more drastic approach
        print("\nAttempting more comprehensive fix...")
        
        # Read again
        content = file_path.read_text()
        
        # Find the specific f-string blocks and replace them
        # Look for the pattern: project_cards_html += f"""
        pattern = r'(project_cards_html \+= f"""[^"]*?""")'
        
        def fix_fstring_block(match):
            block = match.group(1)
            # Replace f""" with """ and add .format() at the end
            # First, replace all {var} with placeholders
            fixed = block.replace('f"""', '"""')
            
            # Extract all the variables used
            import re
            var_pattern = r'\{([^}:]+)(?::[^}]*)?\}'
            variables = re.findall(var_pattern, block)
            
            # Create format mapping
            format_args = []
            for var in variables:
                if '(' in var:  # It's a function call
                    format_args.append(f"{var}={var}")
                else:
                    format_args.append(f"{var}={var}")
            
            # Add .format() call
            if format_args:
                fixed = fixed.replace('"""', '""".format(' + ', '.join(set(format_args)) + ')')
            
            return fixed
        
        # Apply the fix
        # Actually, let's just fix the specific percentages
        content = content.replace('{results.get(\'success_rate\', 0):.1f}%', '{results.get(\'success_rate\', 0):.1f}%%')
        content = content.replace('{aggregate[\'overall_success_rate\']:.1f}%', '{aggregate[\'overall_success_rate\']:.1f}%%')
        
        # Fix width percentages
        content = re.sub(r'(\* 100\})%"', r'\1%%"', content)
        
        file_path.write_text(content)
        
        # Test again
        result = subprocess.run(
            ['python', '-m', 'py_compile', str(file_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ File now compiles successfully!")
        else:
            print(f"❌ Still has errors after comprehensive fix:\n{result.stderr}")

if __name__ == "__main__":
    fix_dashboard()