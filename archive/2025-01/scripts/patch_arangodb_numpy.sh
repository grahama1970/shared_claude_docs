#!/bin/bash

echo "=== Patching arangodb numpy requirement ==="

cd /home/graham/workspace/experiments/arangodb

# Check current requirement
echo "Current numpy requirement:"
grep "numpy" pyproject.toml

# Create a backup
cp pyproject.toml pyproject.toml.backup

# Change numpy requirement to be compatible
sed -i 's/"numpy>=2.2.2"/"numpy>=1.24.0,<2"/' pyproject.toml

echo ""
echo "Updated numpy requirement:"
grep "numpy" pyproject.toml

# Commit the change
git add pyproject.toml
git commit -m "fix: temporarily relax numpy requirement for ecosystem compatibility

- Changed from numpy>=2.2.2 to numpy>=1.24.0,<2
- This allows compatibility with marker and aider-chat
- TODO: Update code to support numpy 2.x properly"

echo ""
echo "Committed change. You'll need to push this to GitHub."

cd /home/graham/workspace/shared_claude_docs