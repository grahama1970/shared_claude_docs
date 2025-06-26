#!/usr/bin/env python3
"""Fix marker's surya-ocr requirement to be compatible with granger-hub."""

import subprocess
import sys
from pathlib import Path

def main():
    """Update marker's surya-ocr requirement."""
    marker_path = Path("/home/graham/workspace/experiments/marker")
    
    if not marker_path.exists():
        print(f"❌ Marker path not found: {marker_path}")
        return 1
    
    pyproject_path = marker_path / "pyproject.toml"
    
    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found in {marker_path}")
        return 1
    
    # Read current content
    content = pyproject_path.read_text()
    
    # Update surya-ocr requirement
    if '"surya-ocr~=0.13.1"' in content:
        new_content = content.replace('"surya-ocr~=0.13.1"', '"surya-ocr>=0.14.5,<0.15.0"')
        pyproject_path.write_text(new_content)
        print("✅ Updated surya-ocr requirement from ~=0.13.1 to >=0.14.5,<0.15.0")
    else:
        print("ℹ️  surya-ocr requirement not found or already modified")
        # Let's check what surya-ocr requirements exist
        print("\nCurrent surya-ocr requirements in file:")
        for line in content.split('\n'):
            if 'surya-ocr' in line or 'surya_ocr' in line:
                print(f"  {line.strip()}")
        return 0
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        # Change to marker directory for git operations
        original_dir = Path.cwd()
        import os
        os.chdir(marker_path)
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        commit_message = """fix: update surya-ocr requirement for granger-hub compatibility

- Changed from surya-ocr>=0.13.1,<0.14.dev0 to surya-ocr>=0.14.5,<0.15.0
- This matches granger-hub's marker-pdf requirement
- Ensures compatibility across the Granger ecosystem"""
        
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