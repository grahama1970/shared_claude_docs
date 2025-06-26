#!/usr/bin/env python3
"""Fix unsloth_wip broken submodule."""

import subprocess
import shutil
import os
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"Error: {result.stderr}")
    return result

def main():
    """Fix the broken submodule in unsloth_wip."""
    unsloth_dir = Path("/home/graham/workspace/experiments/unsloth_wip")
    
    if not unsloth_dir.exists():
        print(f"❌ Directory not found: {unsloth_dir}")
        return 1
    
    print("🔧 Fixing unsloth_wip submodule issue...")
    
    # First, check if we have uncommitted changes
    result = run_command("git status --porcelain", cwd=unsloth_dir, check=False)
    if result.stdout.strip():
        print("⚠️  Uncommitted changes detected. Committing them first...")
        run_command("git add -A", cwd=unsloth_dir)
        run_command('git commit -m "WIP: Save changes before fixing submodule"', cwd=unsloth_dir, check=False)
    
    # Option 1: Try to simply remove the submodule reference from the project
    print("\n🗑️  Removing submodule reference entirely...")
    
    # Remove .gitmodules if it exists
    gitmodules_path = unsloth_dir / ".gitmodules"
    if gitmodules_path.exists():
        gitmodules_path.unlink()
        print("✅ Removed .gitmodules")
    
    # Remove the submodule directory
    submodule_path = unsloth_dir / "repos" / "runpod_llm_ops"
    if submodule_path.exists():
        shutil.rmtree(submodule_path)
        print("✅ Removed repos/runpod_llm_ops directory")
    
    # Remove submodule from git config
    run_command("git config --file .git/config --remove-section submodule.repos/runpod_llm_ops", 
                cwd=unsloth_dir, check=False)
    
    # Remove from .git/modules
    git_modules_path = unsloth_dir / ".git" / "modules" / "repos" / "runpod_llm_ops"
    if git_modules_path.exists():
        shutil.rmtree(git_modules_path)
        print("✅ Removed .git/modules/repos/runpod_llm_ops")
    
    # Stage the removal
    run_command("git rm -rf repos/runpod_llm_ops", cwd=unsloth_dir, check=False)
    run_command("git rm -f .gitmodules", cwd=unsloth_dir, check=False)
    
    # Commit the removal
    result = run_command("git diff --staged --quiet", cwd=unsloth_dir, check=False)
    if result.returncode != 0:  # There are staged changes
        print("\n💾 Committing submodule removal...")
        run_command('''git commit -m "fix: remove broken runpod_llm_ops submodule

- Removed broken submodule that was causing 'No url found' error
- The runpod_ops functionality is available as a separate package
- This allows unsloth_wip to be installed without submodule issues"''', cwd=unsloth_dir)
        
        print("\n📤 Pushing to GitHub...")
        result = run_command("git push", cwd=unsloth_dir, check=False)
        if result.returncode == 0:
            print("✅ Successfully pushed to GitHub!")
        else:
            print("⚠️  Push failed. You may need to push manually.")
    else:
        print("✅ No changes to commit")
    
    print("\n✅ Submodule removal complete!")
    print("\n💡 Note: If runpod_ops functionality is needed, it should be added as a")
    print("   regular dependency in pyproject.toml, not as a submodule.")
    
    return 0

if __name__ == "__main__":
    exit(main())