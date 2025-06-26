#!/usr/bin/env python3
"""Restore mcp-screenshot core module to use actual functionality."""

import subprocess
import sys
from pathlib import Path

def main():
    """Restore the core module to use the actual implementation files."""
    mcp_path = Path("/home/graham/workspace/experiments/mcp-screenshot")
    
    if not mcp_path.exists():
        print(f"❌ mcp-screenshot path not found: {mcp_path}")
        return 1
    
    # Restore core/__init__.py to import from actual modules
    core_init = mcp_path / "src" / "mcp_screenshot" / "core" / "__init__.py"
    
    content = '''"""Core functionality for MCP Screenshot tool."""

# Import actual implementations from the modules
from .capture import capture_screenshot, capture_screenshot_base64
from .description import describe_image_content
from .d3_verification import verify_d3_visualization
from .compare import compare_screenshots
from .history import ScreenshotHistory
from .utils import get_screenshot_tool, save_screenshot, load_screenshot
from .annotate import annotate_screenshot
from .batch import BatchScreenshotProcessor

# Re-export commonly used functions
__all__ = [
    "capture_screenshot",
    "capture_screenshot_base64", 
    "describe_image_content",
    "verify_d3_visualization",
    "compare_screenshots",
    "ScreenshotHistory",
    "get_screenshot_tool",
    "save_screenshot",
    "load_screenshot",
    "annotate_screenshot",
    "BatchScreenshotProcessor",
]
'''
    
    core_init.write_text(content)
    print(f"✅ Restored core/__init__.py to use actual modules")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(mcp_path)
        
        # Add and commit
        subprocess.run(["git", "add", "src/mcp_screenshot/core/__init__.py"], check=True)
        
        commit_message = """fix: restore core module to use actual implementations

- Import from actual implementation modules (capture, description, etc.)
- Remove placeholder implementations
- Use the real functionality that already exists in the codebase"""
        
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