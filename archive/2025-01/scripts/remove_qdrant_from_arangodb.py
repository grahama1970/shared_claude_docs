#!/usr/bin/env python3
"""Remove unused qdrant-client from arangodb dependencies."""

import subprocess
import sys
from pathlib import Path

def main():
    """Remove qdrant-client from arangodb's dependencies."""
    arangodb_path = Path("/home/graham/workspace/experiments/arangodb")
    
    if not arangodb_path.exists():
        print(f"❌ ArangoDB path not found: {arangodb_path}")
        return 1
    
    pyproject_path = arangodb_path / "pyproject.toml"
    
    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found in {arangodb_path}")
        return 1
    
    # Read current content
    content = pyproject_path.read_text()
    
    # Remove qdrant-client line
    lines = content.split('\n')
    new_lines = []
    removed = False
    
    for line in lines:
        if 'qdrant-client' in line:
            print(f"✅ Removing line: {line.strip()}")
            removed = True
            continue
        new_lines.append(line)
    
    if not removed:
        print("ℹ️  qdrant-client not found in dependencies")
        return 0
    
    # Write updated content
    new_content = '\n'.join(new_lines)
    pyproject_path.write_text(new_content)
    print("✅ Removed qdrant-client from pyproject.toml")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        # Change to arangodb directory for git operations
        original_dir = Path.cwd()
        import os
        os.chdir(arangodb_path)
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        commit_message = """fix: remove unused qdrant-client dependency

- qdrant-client is not used in the codebase
- Was causing numpy version conflicts
- Simplifies dependency resolution for the ecosystem"""
        
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("✅ Changes committed")
        
        # Push to GitHub
        print("\n📤 Pushing to GitHub...")
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub!")
        else:
            print(f"⚠️  Push failed: {result.stderr}")
            print("You can push manually later with: git push")
        
        os.chdir(original_dir)
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git operation failed: {e}")
        print("The file has been updated, but you'll need to commit and push manually")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())