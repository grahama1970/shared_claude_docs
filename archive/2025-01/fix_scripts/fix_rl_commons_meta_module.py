#!/usr/bin/env python3
"""Fix rl_commons missing algorithms.meta module."""

import subprocess
import sys
from pathlib import Path

def main():
    """Create the missing meta module in rl_commons."""
    rl_commons_path = Path("/home/graham/workspace/experiments/rl_commons")
    
    if not rl_commons_path.exists():
        print(f"❌ rl_commons path not found: {rl_commons_path}")
        return 1
    
    # Create the meta module directory
    meta_path = rl_commons_path / "src" / "rl_commons" / "algorithms" / "meta"
    meta_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {meta_path}")
    
    # Create __init__.py
    init_file = meta_path / "__init__.py"
    init_content = '''"""Meta-learning algorithms for RL Commons."""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np

class MAML:
    """Model-Agnostic Meta-Learning placeholder implementation."""
    
    def __init__(self, model: Any, alpha: float = 0.01, beta: float = 0.001):
        """Initialize MAML.
        
        Args:
            model: The model to be meta-trained
            alpha: Inner loop learning rate
            beta: Outer loop learning rate
        """
        self.model = model
        self.alpha = alpha
        self.beta = beta
    
    def inner_update(self, support_data: Tuple[np.ndarray, np.ndarray]) -> Any:
        """Perform inner loop update on support data."""
        # Placeholder implementation
        return self.model
    
    def outer_update(self, tasks: List[Tuple[np.ndarray, np.ndarray]]) -> None:
        """Perform outer loop update across tasks."""
        # Placeholder implementation
        pass


class MAMLAgent:
    """MAML-based agent placeholder implementation."""
    
    def __init__(self, state_dim: int, action_dim: int, **kwargs):
        """Initialize MAML agent.
        
        Args:
            state_dim: Dimension of state space
            action_dim: Dimension of action space
            **kwargs: Additional configuration
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.config = kwargs
    
    def act(self, state: np.ndarray) -> int:
        """Select action given state."""
        # Placeholder: random action
        return np.random.randint(0, self.action_dim)
    
    def update(self, experience: Dict[str, Any]) -> None:
        """Update agent with experience."""
        # Placeholder implementation
        pass


__all__ = ["MAML", "MAMLAgent"]
'''
    
    init_file.write_text(init_content)
    print(f"✅ Created: {init_file}")
    
    # Git operations
    print("\n📦 Committing changes...")
    try:
        original_dir = Path.cwd()
        import os
        os.chdir(rl_commons_path)
        
        # Add and commit
        subprocess.run(["git", "add", "src/rl_commons/algorithms/meta/"], check=True)
        
        commit_message = """fix: add missing algorithms.meta module

- Created algorithms/meta/__init__.py with MAML and MAMLAgent placeholders
- Fixes ModuleNotFoundError when importing rl_commons
- Provides basic structure for meta-learning algorithms"""
        
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