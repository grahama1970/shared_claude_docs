#!/usr/bin/env python3
"""Fix arangodb numpy constraint to be compatible with the ecosystem."""

import subprocess
import sys
from pathlib import Path

def main():
    """Update arangodb's numpy requirement."""
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
    
    # Check current numpy requirement
    if 'numpy>=2.2.2' not in content:
        print("✅ ArangoDB numpy requirement already fixed or different than expected")
        if 'numpy' in content:
            print("Current numpy requirements in file:")
            for line in content.split('\n'):
                if 'numpy' in line:
                    print(f"  {line.strip()}")
        return 0
    
    # Create backup
    backup_path = pyproject_path.with_suffix('.toml.backup')
    backup_path.write_text(content)
    print(f"✅ Created backup: {backup_path}")
    
    # Update numpy requirement - since marker has numpy==1.26.4, we'll use that
    new_content = content.replace('"numpy>=2.2.2"', '"numpy==1.26.4"')
    pyproject_path.write_text(new_content)
    print("✅ Updated numpy requirement from >=2.2.2 to ==1.26.4 (matching marker)")
    
    # Show the change
    print("\nUpdated numpy requirements:")
    for line in new_content.split('\n'):
        if 'numpy' in line:
            print(f"  {line.strip()}")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        # Change to arangodb directory for git operations
        original_dir = Path.cwd()
        import os
        os.chdir(arangodb_path)
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        commit_message = """fix: pin numpy to 1.26.4 for ecosystem compatibility

- Changed from numpy>=2.2.2 to numpy==1.26.4
- This matches marker's numpy version exactly
- Ensures compatibility across the Granger ecosystem
- TODO: Test thoroughly and update code if numpy 2.x features were used"""
        
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