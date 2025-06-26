#!/usr/bin/env python3
"""
Module: fix_module_imports.py
Description: Fix Python module imports to follow CLAUDE.md standards

External Dependencies:
- pathlib: https://docs.python.org/3/library/pathlib.html

Sample Input:
>>> # No input required

Expected Output:
>>> # Creates proper module structure and fixes imports

Example Usage:
>>> python fix_module_imports.py
"""

import os
import sys
from pathlib import Path

def ensure_pythonpath():
    """Ensure modules can be imported by adding them to Python path"""
    base_experiments = Path("/home/graham/workspace/experiments")
    base_mcp = Path("/home/graham/workspace/mcp-servers")
    
    modules = {
        # Core Infrastructure
        "granger_hub": base_experiments / "granger_hub/src",
        "rl_commons": base_experiments / "rl_commons/src", 
        "world_model": base_experiments / "world_model/src",
        "claude_test_reporter": base_experiments / "claude-test-reporter/src",
        
        # Processing Spokes
        "sparta": base_experiments / "sparta/src",
        "marker": base_experiments / "marker/src",
        "arangodb": base_experiments / "arangodb/src",
        "youtube_transcripts": base_experiments / "youtube_transcripts/src",
        "llm_call": base_experiments / "llm_call/src",
        "unsloth": base_experiments / "unsloth_wip/src",
        "darpa_crawl": base_experiments / "darpa_crawl/src",
        
        # MCP Services
        "arxiv_mcp_server": base_mcp / "arxiv-mcp-server/src",
        "mcp_screenshot": base_experiments / "mcp-screenshot/src",
        "gitget": base_experiments / "gitget/src",
        
        # UI Modules
        "chat": base_experiments / "chat/src",
        "annotator": base_experiments / "annotator/src",
        "aider_daemon": base_experiments / "aider-daemon/src",
        
        # Module Communicator
        "claude_module_communicator": base_experiments / "claude-module-communicator/src",
        "claude_max_proxy": base_experiments / "claude-max-proxy/src"
    }
    
    # Add all module paths to sys.path
    for module_name, module_path in modules.items():
        if module_path.exists():
            str_path = str(module_path)
            if str_path not in sys.path:
                sys.path.insert(0, str_path)
                print(f"✅ Added {module_name} to Python path: {module_path}")
        else:
            print(f"❌ Module path not found: {module_name} at {module_path}")

def create_env_files():
    """Create .env files with PYTHONPATH for each module"""
    base_experiments = Path("/home/graham/workspace/experiments")
    base_mcp = Path("/home/graham/workspace/mcp-servers")
    
    modules = [
        base_experiments / "sparta",
        base_experiments / "marker", 
        base_experiments / "arangodb",
        base_experiments / "youtube_transcripts",
        base_experiments / "rl_commons",
        base_experiments / "world_model",
        base_experiments / "claude-test-reporter",
        base_experiments / "llm_call",
        base_experiments / "gitget",
        base_mcp / "arxiv-mcp-server",
        base_experiments / "chat",
        base_experiments / "annotator",
        base_experiments / "aider-daemon"
    ]
    
    env_template = """PYTHONPATH=./src

# Module configuration
MODULE_NAME={module_name}
MODULE_VERSION=1.0.0

# Granger ecosystem URLs
GRANGER_HUB_URL=http://localhost:8000
ARANGODB_URL=http://localhost:8529
LLM_CALL_URL=http://localhost:8001
TEST_REPORTER_URL=http://localhost:8002

# API Keys (replace with actual values)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
"""
    
    for module_path in modules:
        if module_path.exists():
            env_file = module_path / ".env.example"
            if not env_file.exists():
                module_name = module_path.name.replace("-", "_")
                content = env_template.format(module_name=module_name)
                env_file.write_text(content)
                print(f"✅ Created .env.example for {module_path.name}")

def fix_module_imports():
    """Fix specific module import issues"""
    
    # Fix sparta to export what tests expect
    sparta_init = Path("/home/graham/workspace/experiments/sparta/src/sparta/__init__.py")
    if sparta_init.exists():
        content = sparta_init.read_text()
        if "from sparta.integrations.sparta_module import SPARTAModule" not in content:
            new_content = '''"""
Module: __init__.py
Description: SPARTA - Space-Based Cybersecurity module exports

External Dependencies:
- None (package initialization)

Sample Input:
>>> from sparta import SPARTAModule

Expected Output:
>>> # Imports SPARTA functionality

Example Usage:
>>> module = SPARTAModule()
"""

# Core exports
from sparta.config import settings
from sparta.integrations.sparta_module import SPARTAModule

# MCP server if needed
try:
    from sparta.mcp.server import server
except ImportError:
    server = None

__version__ = "0.2.0"
__all__ = ["SPARTAModule", "settings", "server"]
'''
            sparta_init.write_text(new_content)
            print("✅ Fixed sparta/__init__.py exports")
    
    # Create sparta_handlers module for compatibility
    sparta_handlers_dir = Path("/home/graham/workspace/shared_claude_docs/project_interactions/sparta_handlers")
    sparta_handlers_dir.mkdir(exist_ok=True)
    
    sparta_handlers_init = sparta_handlers_dir / "__init__.py"
    sparta_handlers_init.write_text('''"""SPARTA handlers compatibility module"""
# Re-export from actual location
try:
    from sparta.integrations.sparta_module import SPARTAModule as SPARTAHandler
except ImportError:
    # Fallback to real handlers if available
    try:
        from .real_sparta_handlers import SPARTAHandler
    except ImportError:
        SPARTAHandler = None

__all__ = ["SPARTAHandler"]
''')
    print("✅ Created sparta_handlers compatibility module")

def main():
    """Run all fixes"""
    print("🔧 Fixing Python module imports...")
    
    ensure_pythonpath()
    create_env_files()
    fix_module_imports()
    
    print("\n✅ Module import fixes complete!")
    print("\nTo use:")
    print("1. Source the virtual environment: source .venv/bin/activate")
    print("2. Run the ecosystem test: python run_final_ecosystem_test_simple.py")

if __name__ == "__main__":
    main()