#!/bin/bash

echo "=== Setting up Git authentication and pushing ==="

cd /home/graham/workspace/experiments/arangodb

# Check current remote
echo "Current remote:"
git remote -v

# Try to push with SSH if configured
echo ""
echo "Attempting to push..."

# First check if we have an SSH remote
if git remote -v | grep -q "git@github.com"; then
    echo "Using SSH remote"
    git push origin main
else
    echo "Please configure git authentication:"
    echo ""
    echo "Option 1: Use GitHub CLI (recommended)"
    echo "  gh auth login"
    echo ""
    echo "Option 2: Use SSH key"
    echo "  git remote set-url origin git@github.com:grahama1970/arangodb.git"
    echo ""
    echo "Option 3: Use Personal Access Token"
    echo "  Create token at: https://github.com/settings/tokens"
    echo "  Then: git push https://YOUR_TOKEN@github.com/grahama1970/arangodb.git main"
    echo ""
    echo "After authentication is set up, run:"
    echo "  cd /home/graham/workspace/experiments/arangodb"
    echo "  git push origin main"
    echo ""
    echo "Then return here and run:"
    echo "  cd /home/graham/workspace/shared_claude_docs"
    echo "  uv sync"
fi