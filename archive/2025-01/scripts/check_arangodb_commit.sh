#!/bin/bash

echo "=== Checking arangodb commit status ==="

cd /home/graham/workspace/experiments/arangodb

# Show the last commit
echo "Last commit:"
git log --oneline -1

# Check if it's the pyproject.toml fix
if git log -1 --pretty=%s | grep -q "pyproject.toml"; then
    echo "✅ pyproject.toml fix is committed"
    
    # Show what changed
    echo ""
    echo "Changes in last commit:"
    git show --name-only HEAD
    
    # Try to push just this commit
    echo ""
    echo "Attempting to push ONLY the pyproject.toml fix..."
    
    # First, stash all the uncommitted changes
    echo "Stashing uncommitted changes..."
    git stash -u
    
    # Now push
    echo "Pushing..."
    git push origin main
    
    # Restore the stashed changes
    echo "Restoring stashed changes..."
    git stash pop
else
    echo "❌ Last commit is not the pyproject.toml fix"
fi

cd /home/graham/workspace/shared_claude_docs