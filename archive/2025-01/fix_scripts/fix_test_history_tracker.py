#!/usr/bin/env python3
"""Fix test_history_tracker.py percentage issues in f-strings"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from pathlib import Path

def fix_tracker():
    """Fix the test_history_tracker.py file"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/tracking/test_history_tracker.py")
    
    # Read the file
    content = file_path.read_text()
    
    # In f-strings, % needs to be escaped as %%
    # Replace percentage literals in f-strings
    replacements = [
        ('.flaky-table {{ width: 100%;', '.flaky-table {{ width: 100%%;'),
        ('.svg-chart {{ width: 100%;', '.svg-chart {{ width: 100%%;'),
        ('>100%<', '>100%%<'),
        ('>75%<', '>75%%<'),
        ('>50%<', '>50%%<'),
        ('>25%<', '>25%%<'),
        ('>0%<', '>0%%<'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Write back
    file_path.write_text(content)
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

if __name__ == "__main__":
    fix_tracker()