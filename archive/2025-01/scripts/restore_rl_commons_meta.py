#!/usr/bin/env python3
"""Restore rl_commons meta module to use actual implementations."""

import subprocess
import sys
from pathlib import Path

def main():
    """Restore the meta module to use actual implementations."""
    rl_commons_path = Path("/home/graham/workspace/experiments/rl_commons")
    
    if not rl_commons_path.exists():
        print(f"❌ rl_commons path not found: {rl_commons_path}")
        return 1
    
    # Restore meta/__init__.py to import from actual modules
    meta_init = rl_commons_path / "src" / "rl_commons" / "algorithms" / "meta" / "__init__.py"
    
    content = '''"""Meta-learning algorithms for reinforcement learning.

This module provides implementations of various meta-learning algorithms
that can quickly adapt to new tasks.
"""

from .maml import MAML, MAMLAgent
from .reptile import Reptile, ReptileAgent
from .task_distribution import TaskDistribution, TaskSampler

__all__ = [
    "MAML",
    "MAMLAgent", 
    "Reptile",
    "ReptileAgent",
    "TaskDistribution",
    "TaskSampler",
]
'''
    
    meta_init.write_text(content)
    print(f"✅ Restored meta/__init__.py to use actual implementations")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(rl_commons_path)
        
        # Add and commit
        subprocess.run(["git", "add", "src/rl_commons/algorithms/meta/__init__.py"], check=True)
        
        commit_message = """fix: restore meta module to use actual implementations

- Import from actual implementation modules (maml.py, reptile.py, etc.)
- Remove placeholder implementations  
- Use the real meta-learning algorithms that already exist"""
        
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