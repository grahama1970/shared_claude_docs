#!/usr/bin/env python3
"""Fix mcp-screenshot missing core module."""

import subprocess
import sys
from pathlib import Path

def main():
    """Create the missing core module in mcp-screenshot."""
    mcp_path = Path("/home/graham/workspace/experiments/mcp-screenshot")
    
    if not mcp_path.exists():
        print(f"❌ mcp-screenshot path not found: {mcp_path}")
        return 1
    
    # Create the core module directory
    core_path = mcp_path / "src" / "mcp_screenshot" / "core"
    core_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {core_path}")
    
    # Create __init__.py with the expected exports
    init_file = core_path / "__init__.py"
    init_content = '''"""Core functionality for MCP Screenshot tool."""

from typing import Any, Dict, List, Optional, Tuple, Union
import base64
import io
from pathlib import Path

# Try to import screenshot libraries
try:
    from PIL import ImageGrab, Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


class ScreenshotTool:
    """Tool for capturing screenshots."""
    
    def __init__(self, backend: str = "auto"):
        """Initialize screenshot tool.
        
        Args:
            backend: Screenshot backend to use ("pil", "pyautogui", or "auto")
        """
        self.backend = self._select_backend(backend)
        
    def _select_backend(self, backend: str) -> str:
        """Select the screenshot backend."""
        if backend == "auto":
            if HAS_PIL:
                return "pil"
            elif HAS_PYAUTOGUI:
                return "pyautogui"
            else:
                raise ImportError("No screenshot backend available. Install pillow or pyautogui.")
        elif backend == "pil" and not HAS_PIL:
            raise ImportError("PIL not available. Install pillow.")
        elif backend == "pyautogui" and not HAS_PYAUTOGUI:
            raise ImportError("pyautogui not available. Install pyautogui.")
        return backend
    
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None) -> bytes:
        """Capture a screenshot.
        
        Args:
            region: Optional (x, y, width, height) tuple for region capture
            
        Returns:
            Screenshot as PNG bytes
        """
        if self.backend == "pil":
            img = ImageGrab.grab(bbox=region)
        else:  # pyautogui
            if region:
                img = pyautogui.screenshot(region=region)
            else:
                img = pyautogui.screenshot()
        
        # Convert to PNG bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()
    
    def capture_base64(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Capture a screenshot and return as base64 string."""
        png_bytes = self.capture(region)
        return base64.b64encode(png_bytes).decode('utf-8')


class ScreenshotProcessor:
    """Process and analyze screenshots."""
    
    def __init__(self):
        """Initialize processor."""
        self.tool = ScreenshotTool()
    
    def capture_and_save(self, filepath: Union[str, Path], 
                        region: Optional[Tuple[int, int, int, int]] = None) -> Path:
        """Capture screenshot and save to file."""
        filepath = Path(filepath)
        png_bytes = self.tool.capture(region)
        filepath.write_bytes(png_bytes)
        return filepath
    
    def get_screen_info(self) -> Dict[str, Any]:
        """Get information about the screen."""
        info = {
            "backend": self.tool.backend,
            "has_pil": HAS_PIL,
            "has_pyautogui": HAS_PYAUTOGUI
        }
        
        if HAS_PYAUTOGUI:
            size = pyautogui.size()
            info["screen_width"] = size.width
            info["screen_height"] = size.height
        
        return info


# For backward compatibility
screenshot_tool = ScreenshotTool()
capture_screenshot = screenshot_tool.capture
capture_screenshot_base64 = screenshot_tool.capture_base64

__all__ = [
    "ScreenshotTool",
    "ScreenshotProcessor", 
    "screenshot_tool",
    "capture_screenshot",
    "capture_screenshot_base64",
]
'''
    
    init_file.write_text(init_content)
    print(f"✅ Created: {init_file}")
    
    # Also update the main __init__.py to import from core correctly
    main_init = mcp_path / "src" / "mcp_screenshot" / "__init__.py"
    if main_init.exists():
        # Read current content
        current_content = main_init.read_text()
        
        # Replace the problematic import
        new_content = current_content.replace(
            "from mcp_screenshot.core import (",
            "from .core import ("
        )
        
        # If that didn't work, try another approach
        if new_content == current_content:
            # Just rewrite it completely
            new_content = '''"""MCP Screenshot - Model Context Protocol screenshot tool."""

from .core import (
    ScreenshotTool,
    ScreenshotProcessor,
    screenshot_tool,
    capture_screenshot,
    capture_screenshot_base64,
)

__version__ = "0.1.0"

__all__ = [
    "ScreenshotTool",
    "ScreenshotProcessor", 
    "screenshot_tool",
    "capture_screenshot",
    "capture_screenshot_base64",
]
'''
        
        main_init.write_text(new_content)
        print(f"✅ Updated: {main_init}")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(mcp_path)
        
        # Add and commit
        subprocess.run(["git", "add", "src/mcp_screenshot/"], check=True)
        
        commit_message = """fix: add missing core module

- Created core/__init__.py with screenshot functionality
- Fixed import error "No module named 'mcp_screenshot.core'"
- Provides ScreenshotTool and ScreenshotProcessor classes"""
        
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
        print("The file has been created, but you'll need to commit and push manually")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())