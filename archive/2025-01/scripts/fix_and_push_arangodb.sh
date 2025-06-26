#!/bin/bash

# Script to fix and push arangodb changes

echo "=== Fixing arangodb repository ==="

# Navigate to arangodb
cd /home/graham/workspace/experiments/arangodb

# Check git status
echo "Current git status:"
git status

# Check if pyproject.toml has changes
if git diff --name-only | grep -q "pyproject.toml"; then
    echo "pyproject.toml has uncommitted changes"
    
    # Show the diff
    echo "Changes in pyproject.toml:"
    git diff pyproject.toml
    
    # Commit and push
    git add pyproject.toml
    git commit -m "fix: correct pyproject.toml syntax"
    git push origin main
    echo "✅ Pushed pyproject.toml fixes"
else
    echo "No changes in pyproject.toml to commit"
    
    # Pull latest to ensure we're up to date
    echo "Pulling latest changes..."
    git pull origin main
fi

# Now go back to shared_claude_docs and uncomment arangodb
cd /home/graham/workspace/shared_claude_docs

echo ""
echo "=== Updating shared_claude_docs ==="

# Uncomment the arangodb line
sed -i 's/# "arangodb @ git+https:\/\/github.com\/grahama1970\/arangodb.git",.*/"arangodb @ git+https:\/\/github.com\/grahama1970\/arangodb.git",/' pyproject.toml

echo "Uncommenting arangodb dependency..."
grep "arangodb @" pyproject.toml

# Run uv sync
echo ""
echo "Running uv sync..."
uv sync

# If successful, install in editable mode
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ uv sync successful!"
    echo "Installing in editable mode..."
    uv pip install -e .
else
    echo "❌ uv sync failed. The arangodb repository might still have issues."
fi