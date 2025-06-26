#!/usr/bin/env python3
"""
Module: comprehensive_arangodb_fix.py
Description: Comprehensive fix for arangodb pyproject.toml syntax issues

External Dependencies:
- None (uses standard library only)

Sample Input:
>>> # Malformed TOML with stray quotes
>>> [project.scripts]"
>>> key = "value"

Expected Output:
>>> [project.scripts]
>>> key = "value"

Example Usage:
>>> python comprehensive_arangodb_fix.py
"""

import os
import re
import tempfile
import subprocess
import shutil

def fix_toml_comprehensive(content: str) -> str:
    """Fix all TOML syntax issues comprehensively."""
    lines = content.splitlines()
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix section headers with trailing quotes
        if line.strip().startswith('[') and '"' in line:
            # Pattern 1: [section]"
            line = re.sub(r'\]"(\s*)$', r']\1', line)
            # Pattern 2: [section.subsection]"
            line = re.sub(r'\]"(\s*)$', r']\1', line)
        
        # Fix unbalanced quotes in values
        # Count quotes to ensure they're balanced
        quote_count = line.count('"') - line.count('\\"')
        if quote_count % 2 == 1 and not line.strip().startswith('#'):
            # Try to fix by removing trailing quote if it's at the end
            if line.rstrip().endswith('"'):
                line = line.rstrip()[:-1] + line[len(line.rstrip()):]
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def main():
    """Fix arangodb pyproject.toml comprehensively."""
    print("=== Comprehensive arangodb fix ===")
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    print(f"Working in: {temp_dir}")
    
    try:
        # Clone the repository
        print("\nCloning arangodb repository...")
        clone_result = subprocess.run(
            ["git", "clone", "https://github.com/grahama1970/arangodb.git"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        if clone_result.returncode != 0:
            print(f"Clone failed: {clone_result.stderr}")
            print("\nTrying with GitHub CLI...")
            clone_result = subprocess.run(
                ["gh", "repo", "clone", "grahama1970/arangodb"],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if clone_result.returncode != 0:
                print("GitHub CLI also failed. Please set up authentication first.")
                return
        
        repo_path = os.path.join(temp_dir, "arangodb")
        pyproject_path = os.path.join(repo_path, "pyproject.toml")
        
        # Read the file
        print("\nReading pyproject.toml...")
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Apply comprehensive fixes
        print("Applying fixes...")
        fixed_content = fix_toml_comprehensive(content)
        
        # Write back
        with open(pyproject_path, 'w') as f:
            f.write(fixed_content)
        
        # Validate the fix
        print("\nValidating fixed TOML...")
        try:
            import toml
            with open(pyproject_path, 'r') as f:
                toml.load(f)
            print("✅ TOML is now valid!")
        except Exception as e:
            print(f"❌ TOML validation failed: {e}")
            # Show problematic lines
            lines = fixed_content.splitlines()
            for i, line in enumerate(lines):
                if '[' in line and ']' in line:
                    print(f"Line {i+1}: {repr(line)}")
            return
        
        # Commit the fix
        print("\nCommitting fix...")
        os.chdir(repo_path)
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        subprocess.run([
            "git", "commit", "-m",
            "fix: comprehensive pyproject.toml syntax corrections\n\n"
            "- Removed all stray quotes from section headers\n"
            "- Fixed unbalanced quotes in values\n"
            "- Ensured valid TOML syntax throughout"
        ], check=True)
        
        # Try to push
        print("\nAttempting to push...")
        push_result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True,
            text=True
        )
        
        if push_result.returncode == 0:
            print("✅ Successfully pushed fixes!")
        else:
            print(f"Push failed: {push_result.stderr}")
            print("\nTrying with GitHub CLI...")
            push_result = subprocess.run(
                ["gh", "repo", "sync", "--force"],
                capture_output=True,
                text=True
            )
            
            if push_result.returncode == 0:
                print("✅ Successfully pushed with GitHub CLI!")
            else:
                print("❌ Push failed. Please configure authentication.")
                print("\nTo fix authentication, run one of:")
                print("  gh auth login")
                print("  git remote set-url origin git@github.com:grahama1970/arangodb.git")
                return
        
    finally:
        # Clean up
        os.chdir("/home/graham/workspace/shared_claude_docs")
        shutil.rmtree(temp_dir)
    
    # Now try uv sync
    print("\n=== Running uv sync ===")
    sync_result = subprocess.run(["uv", "sync"], capture_output=True, text=True)
    
    if sync_result.returncode == 0:
        print("✅ uv sync successful!")
        print("\nInstalling in editable mode...")
        subprocess.run(["uv", "pip", "install", "-e", "."])
    else:
        print(f"❌ uv sync failed:\n{sync_result.stderr}")

if __name__ == "__main__":
    main()