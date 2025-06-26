#!/usr/bin/env python3
"""Fix mcp-screenshot packaging to include core module."""

import subprocess
import sys
from pathlib import Path

def main():
    """Fix the package configuration."""
    mcp_path = Path("/home/graham/workspace/experiments/mcp-screenshot")
    
    if not mcp_path.exists():
        print(f"❌ mcp-screenshot path not found: {mcp_path}")
        return 1
    
    pyproject_path = mcp_path / "pyproject.toml"
    
    # Read current content
    content = pyproject_path.read_text()
    
    # Update package configuration to use find_packages
    new_content = content.replace(
        'packages = ["mcp_screenshot"]',
        'packages = ["mcp_screenshot", "mcp_screenshot.core", "mcp_screenshot.cli", "mcp_screenshot.integrations", "mcp_screenshot.mcp"]'
    )
    
    if new_content == content:
        # Try alternative approach
        new_content = content.replace(
            '[tool.setuptools]\npackages = ["mcp_screenshot"]\npackage-dir = {"" = "src"}',
            '[tool.setuptools]\npackage-dir = {"" = "src"}\n\n[tool.setuptools.packages.find]\nwhere = ["src"]\ninclude = ["mcp_screenshot*"]'
        )
    
    pyproject_path.write_text(new_content)
    print(f"✅ Updated pyproject.toml to include all subpackages")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(mcp_path)
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        
        commit_message = """fix: update packaging to include core module

- Changed from explicit package list to setuptools.packages.find
- This ensures core/ and other submodules are included in the package
- Fixes ModuleNotFoundError: No module named 'mcp_screenshot.core'"""
        
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