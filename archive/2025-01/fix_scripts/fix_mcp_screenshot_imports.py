#!/usr/bin/env python3
"""Fix mcp-screenshot imports to match core module."""

import subprocess
import sys
from pathlib import Path

def main():
    """Fix the imports in __init__.py."""
    mcp_path = Path("/home/graham/workspace/experiments/mcp-screenshot")
    
    if not mcp_path.exists():
        print(f"❌ mcp-screenshot path not found: {mcp_path}")
        return 1
    
    # Fix the main __init__.py
    main_init = mcp_path / "src" / "mcp_screenshot" / "__init__.py"
    
    # Rewrite it to match what's available in core
    content = '''"""MCP Screenshot - Model Context Protocol screenshot tool."""

from .core import (
    ScreenshotTool,
    ScreenshotProcessor,
    screenshot_tool,
    capture_screenshot,
    capture_screenshot_base64,
    describe_image_content,
    analyze_screenshot,
    get_screenshot_tool,
    capture_region,
)

__version__ = "0.1.0"

# Compatibility alias
def verify_d3_visualization(screenshot_data: bytes) -> dict:
    """Verify D3 visualization (placeholder for backward compatibility)."""
    return analyze_screenshot(screenshot_data)

__all__ = [
    "ScreenshotTool",
    "ScreenshotProcessor", 
    "screenshot_tool",
    "capture_screenshot",
    "capture_screenshot_base64",
    "describe_image_content",
    "analyze_screenshot",
    "verify_d3_visualization",
    "get_screenshot_tool",
    "capture_region",
]
'''
    
    main_init.write_text(content)
    print(f"✅ Fixed imports in __init__.py")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(mcp_path)
        
        # Add and commit
        subprocess.run(["git", "add", "src/mcp_screenshot/__init__.py"], check=True)
        
        commit_message = """fix: align imports with core module exports

- Updated imports to match what core module actually exports
- Added verify_d3_visualization as compatibility alias
- Fixed ImportError issues"""
        
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