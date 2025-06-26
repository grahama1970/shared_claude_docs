#!/usr/bin/env python3
"""
Module: setup_python_paths.py
Description: Properly set up Python paths for all Granger modules

External Dependencies:
- pathlib: https://docs.python.org/3/library/pathlib.html
- subprocess: https://docs.python.org/3/library/subprocess.html

Sample Input:
>>> # No input required

Expected Output:
>>> # Sets up proper Python paths and creates .pth file

Example Usage:
>>> python setup_python_paths.py
"""

import os
import sys
import site
from pathlib import Path
import subprocess

def get_site_packages():
    """Get the site-packages directory for the current Python"""
    return site.getusersitepackages() if hasattr(site, 'getusersitepackages') else site.getsitepackages()[0]

def create_pth_file():
    """Create a .pth file to add all module paths"""
    pth_content = """# Granger ecosystem module paths
/home/graham/workspace/experiments/sparta/src
/home/graham/workspace/experiments/marker/src
/home/graham/workspace/experiments/arangodb/src
/home/graham/workspace/experiments/youtube_transcripts/src
/home/graham/workspace/experiments/rl_commons/src
/home/graham/workspace/experiments/world_model/src
/home/graham/workspace/experiments/claude-test-reporter/src
/home/graham/workspace/experiments/llm_call/src
/home/graham/workspace/experiments/gitget/src
/home/graham/workspace/mcp-servers/arxiv-mcp-server/src
/home/graham/workspace/experiments/fine_tuning/src
/home/graham/workspace/experiments/darpa_crawl/src
/home/graham/workspace/experiments/chat/src
/home/graham/workspace/experiments/annotator/src
/home/graham/workspace/experiments/aider-daemon/src
/home/graham/workspace/experiments/granger_hub/src
/home/graham/workspace/experiments/claude-module-communicator/src
/home/graham/workspace/experiments/mcp-screenshot/src
/home/graham/workspace/shared_claude_docs/project_interactions
/home/graham/workspace/shared_claude_docs
"""
    
    # Write to current directory for immediate use
    pth_path = Path("granger_modules.pth")
    pth_path.write_text(pth_content)
    print(f"✅ Created {pth_path}")
    
    # Also try to write to site-packages if possible
    try:
        site_packages = get_site_packages()
        if site_packages and os.access(site_packages, os.W_OK):
            site_pth = Path(site_packages) / "granger_modules.pth"
            site_pth.write_text(pth_content)
            print(f"✅ Created {site_pth}")
    except:
        pass

def create_setup_script():
    """Create a shell script to set PYTHONPATH"""
    script_content = '''#!/bin/bash
# Set up Python paths for Granger ecosystem

export PYTHONPATH="/home/graham/workspace/experiments/sparta/src:\
/home/graham/workspace/experiments/marker/src:\
/home/graham/workspace/experiments/arangodb/src:\
/home/graham/workspace/experiments/youtube_transcripts/src:\
/home/graham/workspace/experiments/rl_commons/src:\
/home/graham/workspace/experiments/world_model/src:\
/home/graham/workspace/experiments/claude-test-reporter/src:\
/home/graham/workspace/experiments/llm_call/src:\
/home/graham/workspace/experiments/gitget/src:\
/home/graham/workspace/mcp-servers/arxiv-mcp-server/src:\
/home/graham/workspace/experiments/fine_tuning/src:\
/home/graham/workspace/experiments/darpa_crawl/src:\
/home/graham/workspace/experiments/chat/src:\
/home/graham/workspace/experiments/annotator/src:\
/home/graham/workspace/experiments/aider-daemon/src:\
/home/graham/workspace/experiments/granger_hub/src:\
/home/graham/workspace/experiments/claude-module-communicator/src:\
/home/graham/workspace/experiments/mcp-screenshot/src:\
/home/graham/workspace/shared_claude_docs/project_interactions:\
/home/graham/workspace/shared_claude_docs:$PYTHONPATH"

echo "✅ Python paths configured for Granger ecosystem"
echo "You can now run: python run_final_ecosystem_test.py"
'''
    
    script_path = Path("setup_granger_paths.sh")
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    print(f"✅ Created {script_path}")
    print("\nTo use: source ./setup_granger_paths.sh")

def update_current_pythonpath():
    """Update PYTHONPATH for current session"""
    paths = [
        "/home/graham/workspace/experiments/sparta/src",
        "/home/graham/workspace/experiments/marker/src",
        "/home/graham/workspace/experiments/arangodb/src",
        "/home/graham/workspace/experiments/youtube_transcripts/src",
        "/home/graham/workspace/experiments/rl_commons/src",
        "/home/graham/workspace/experiments/world_model/src",
        "/home/graham/workspace/experiments/claude-test-reporter/src",
        "/home/graham/workspace/experiments/llm_call/src",
        "/home/graham/workspace/experiments/gitget/src",
        "/home/graham/workspace/mcp-servers/arxiv-mcp-server/src",
        "/home/graham/workspace/experiments/fine_tuning/src",
        "/home/graham/workspace/experiments/darpa_crawl/src",
        "/home/graham/workspace/experiments/chat/src",
        "/home/graham/workspace/experiments/annotator/src",
        "/home/graham/workspace/experiments/aider-daemon/src",
        "/home/graham/workspace/experiments/granger_hub/src",
        "/home/graham/workspace/experiments/claude-module-communicator/src",
        "/home/graham/workspace/experiments/mcp-screenshot/src",
        "/home/graham/workspace/shared_claude_docs/project_interactions",
        "/home/graham/workspace/shared_claude_docs"
    ]
    
    for path in paths:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    # Update environment variable
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    new_paths = ':'.join(paths)
    os.environ['PYTHONPATH'] = f"{new_paths}:{current_pythonpath}" if current_pythonpath else new_paths

def main():
    """Set up all Python paths"""
    print("🔧 Setting up Python paths for Granger ecosystem...")
    
    update_current_pythonpath()
    create_pth_file()
    create_setup_script()
    
    print("\n✅ Python path setup complete!")
    print("\nYour modules should now be importable.")
    print("For permanent setup in new terminals, run:")
    print("  source ./setup_granger_paths.sh")

if __name__ == "__main__":
    main()