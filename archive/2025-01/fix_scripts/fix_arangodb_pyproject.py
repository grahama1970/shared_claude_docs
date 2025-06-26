#!/usr/bin/env python3
"""Fix the arangodb pyproject.toml syntax error."""

import os
import sys

# Path to arangodb pyproject.toml
arangodb_path = "/home/graham/workspace/experiments/arangodb/pyproject.toml"

if not os.path.exists(arangodb_path):
    print(f"Error: {arangodb_path} not found")
    sys.exit(1)

# Read the file
with open(arangodb_path, 'r') as f:
    lines = f.readlines()

# Check line 70 for the issue
print(f"Line 70 currently: {repr(lines[69])}")

# Check if there's a stray quote
if lines[69].strip().endswith('"]'):
    print("Found issue: extra quote at end of line 70")
    lines[69] = lines[69].replace('"]', ']')
    
    # Write back
    with open(arangodb_path, 'w') as f:
        f.writelines(lines)
    print("Fixed!")
elif '[project.scripts]"' in ''.join(lines):
    # Search for the problematic line
    for i, line in enumerate(lines):
        if '[project.scripts]"' in line:
            print(f"Found issue at line {i+1}: {repr(line)}")
            lines[i] = line.replace('[project.scripts]"', '[project.scripts]')
            
            # Write back
            with open(arangodb_path, 'w') as f:
                f.writelines(lines)
            print("Fixed!")
            break
else:
    print("Checking for other potential issues...")
    
    # Look for any lines with [project.scripts]
    for i, line in enumerate(lines):
        if 'project.scripts' in line:
            print(f"Line {i+1}: {repr(line)}")
    
    # Also check if the file has proper TOML syntax
    try:
        import toml
        with open(arangodb_path, 'r') as f:
            toml.load(f)
        print("TOML syntax appears to be valid")
    except Exception as e:
        print(f"TOML parsing error: {e}")
        print("This might be the actual issue")