#!/bin/bash

echo "=== Fixing arangodb repository pyproject.toml ==="

# Create a temporary directory for the fix
TEMP_DIR=$(mktemp -d)
cd $TEMP_DIR

# Clone the arangodb repository
echo "Cloning arangodb repository..."
git clone https://github.com/grahama1970/arangodb.git
cd arangodb

# Check current content around line 70
echo "Current content around line 70:"
sed -n '68,75p' pyproject.toml

# Fix the issue - remove stray quotes from section headers
echo "Fixing pyproject.toml..."
sed -i 's/\[project\.scripts\]"/[project.scripts]/' pyproject.toml
sed -i 's/\[project\.optional-dependencies\]"/[project.optional-dependencies]/' pyproject.toml
sed -i 's/\[build-system\]"/[build-system]/' pyproject.toml
sed -i 's/\[tool\.\([^]]*\)\]"/[tool.\1]/' pyproject.toml

# Show the fix
echo "Fixed content around line 70:"
sed -n '68,75p' pyproject.toml

# Try to parse the fixed file
echo "Validating fixed TOML..."
python3 -c "import toml; toml.load(open('pyproject.toml'))" && echo "✅ TOML is valid!" || echo "❌ TOML still has issues"

# Commit and push the fix
echo "Committing fix..."
git add pyproject.toml
git commit -m "fix: remove stray quotes from pyproject.toml section headers

- Fixed [project.scripts]\" to [project.scripts]
- Fixed similar issues in other section headers
- This was preventing pip/uv from installing the package"

# Push the fix
echo "Pushing to GitHub..."
git push origin main

# Clean up
cd /home/graham/workspace/shared_claude_docs
rm -rf $TEMP_DIR

echo ""
echo "=== Now syncing shared_claude_docs ==="
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