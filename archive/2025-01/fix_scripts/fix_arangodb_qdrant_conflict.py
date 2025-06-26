#!/usr/bin/env python3
"""Fix arangodb qdrant-client conflict by pinning to an older version."""

import subprocess
import sys
from pathlib import Path

def main():
    """Update arangodb's qdrant-client requirement."""
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
    
    # Update qdrant-client requirement to a version that works with numpy 1.26.4
    if '"qdrant-client>=1.14.2"' in content:
        # Pin to an older version that doesn't have the numpy 2.x requirement
        new_content = content.replace('"qdrant-client>=1.14.2"', '"qdrant-client==1.10.0"')
        pyproject_path.write_text(new_content)
        print("✅ Updated qdrant-client requirement from >=1.14.2 to ==1.10.0")
    else:
        print("ℹ️  qdrant-client requirement not found or already modified")
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
        
        commit_message = """fix: pin qdrant-client to older version for numpy compatibility

- Changed from qdrant-client>=1.14.2 to qdrant-client==1.10.0
- Newer versions of qdrant-client require numpy>=2.1.0 on Python 3.13+
- This ensures compatibility with numpy==1.26.4 across all Python versions
- Part of ecosystem-wide numpy compatibility fix"""
        
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