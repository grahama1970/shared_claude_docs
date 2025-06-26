#!/bin/bash

echo "=== Committing and pushing arangodb fixes ==="

# Navigate to arangodb
cd /home/graham/workspace/experiments/arangodb

# Add the pyproject.toml fix
git add pyproject.toml

# Commit the fix
git commit -m "fix: remove stray quotes from pyproject.toml section headers

- Fixed malformed TOML syntax where section headers had trailing quotes
- Corrected [project.scripts], [project.optional-dependencies], etc.
- This was preventing the package from being installed via git+https"

# Push to origin
echo "Pushing to GitHub..."
git push origin main

# Come back to shared_claude_docs
cd /home/graham/workspace/shared_claude_docs

echo ""
echo "=== Now syncing shared_claude_docs ==="

# The arangodb line was already uncommented by the user, so just sync
echo "Running uv sync..."
uv sync

# If successful, install in editable mode
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ uv sync successful!"
    echo "Installing shared_claude_docs in editable mode..."
    uv pip install -e .
else
    echo "❌ uv sync still failing. Check error messages above."
fi