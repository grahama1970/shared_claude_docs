#!/usr/bin/env python3
"""Fix arangodb pillow conflict with granger-hub."""

import subprocess
import sys
from pathlib import Path

def main():
    """Update arangodb's pillow requirement."""
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
    
    # Check and update pillow requirement
    if '"pillow>=11.2.1"' in content:
        # Downgrade to be compatible with marker-pdf's requirement
        new_content = content.replace('"pillow>=11.2.1"', '"pillow>=10.1.0,<11.0.0"')
        pyproject_path.write_text(new_content)
        print("✅ Updated pillow requirement from >=11.2.1 to >=10.1.0,<11.0.0")
    else:
        print("ℹ️  pillow requirement not found or already modified")
        # Let's check what pillow requirements exist
        print("\nCurrent pillow requirements in file:")
        for line in content.split('\n'):
            if 'pillow' in line.lower():
                print(f"  {line.strip()}")
        return 0
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        # Change to arangodb directory for git operations
        original_dir = Path.cwd()
        import os
        os.chdir(arangodb_path)
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        commit_message = """fix: downgrade pillow requirement for granger-hub compatibility

- Changed from pillow>=11.2.1 to pillow>=10.1.0,<11.0.0
- This matches marker-pdf's requirement (used by granger-hub)
- Ensures compatibility across the Granger ecosystem
- Part of ecosystem-wide dependency resolution"""
        
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