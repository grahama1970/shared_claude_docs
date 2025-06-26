#!/usr/bin/env python3
"""Comprehensive fix for multi_project_dashboard.py percentage issues"""

from pathlib import Path

def fix_dashboard():
    """Replace the entire problematic method with a working version"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/multi_project_dashboard.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find line 197 and replace the problematic f-string
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        # Fix line 197: <span class="metric-value">{results.get('success_rate', 0):.1f}{'%'}</span>
        if i == 196 and "{'%'}" in line:  # Line 197 is index 196
            # Replace with a simpler version
            lines[i] = '                        <span class="metric-value">{0:.1f}%</span>'.format(results.get('success_rate', 0))
            print(f"Fixed line {i+1}")
        
        # Fix line 203: style="width: {results.get('passed', 0) / max(results.get('total', 1), 1) * 100}{'%'}"
        elif "{'%'}\"" in line and "width:" in line:
            # Extract the calculation part
            if "passed" in line:
                calc = "results.get('passed', 0) / max(results.get('total', 1), 1) * 100"
                lines[i] = f'                        <div class="progress-fill passed" style="width: {{{calc}:.1f}}%"></div>'
            elif "failed" in line:
                calc = "results.get('failed', 0) / max(results.get('total', 1), 1) * 100"
                lines[i] = f'                        <div class="progress-fill failed" style="width: {{{calc}:.1f}}%"></div>'
            elif "skipped" in line:
                calc = "results.get('skipped', 0) / max(results.get('total', 1), 1) * 100"
                lines[i] = f'                        <div class="progress-fill skipped" style="width: {{{calc}:.1f}}%"></div>'
            print(f"Fixed line {i+1}")
        
        # Fix line 227: {aggregate['overall_success_rate']:.1f}{'%'}
        elif i == 226 and "{'%'}" in line and "overall_success_rate" in line:
            lines[i] = '            <div class="summary-value" style="color: #10b981">{0:.1f}%</div>'.format(aggregate['overall_success_rate'])
            print(f"Fixed line {i+1}")
    
    # Actually, let's just replace the whole _generate_html method
    # Find the method start
    method_start = -1
    for i, line in enumerate(lines):
        if "def _generate_html(self, aggregate: Dict[str, Any]) -> str:" in line:
            method_start = i
            break
    
    if method_start == -1:
        print("Could not find _generate_html method")
        return
    
    # Replace problematic f-strings with regular string formatting
    # We'll convert the f-string to use % formatting for the percentages
    new_lines = []
    in_fstring = False
    fstring_content = []
    
    for i, line in enumerate(lines):
        if i < method_start:
            new_lines.append(line)
            continue
            
        # Check if we're starting an f-string
        if 'f"""' in line:
            in_fstring = True
            # Replace f""" with just """
            line = line.replace('f"""', '"""')
        
        # If we're in an f-string and see {'%'}, replace it
        if in_fstring and "{'%'}" in line:
            # Replace {'%'} with just %
            line = line.replace("{'%'}", "%")
        
        # Check if we're ending the f-string
        if in_fstring and '"""' in line and not line.strip().startswith('"""'):
            in_fstring = False
        
        new_lines.append(line)
    
    # Write back
    new_content = '\n'.join(new_lines)
    file_path.write_text(new_content)
    print(f"\nUpdated {file_path}")
    
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

if __name__ == "__main__":
    fix_dashboard()