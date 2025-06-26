#!/bin/bash

echo "=== Directly fixing arangodb repository ==="

# Save current directory
CURRENT_DIR=$(pwd)

# Go to arangodb repository
cd /home/graham/workspace/experiments/arangodb

echo "Current directory: $(pwd)"
echo "Git status:"
git status

# Check if we have the pyproject.toml fix
if git diff --name-only | grep -q "pyproject.toml"; then
    echo "Found uncommitted changes to pyproject.toml"
    
    # Show the changes
    echo "Changes:"
    git diff pyproject.toml | head -20
    
    # Add and commit
    git add pyproject.toml
    git commit -m "fix: remove stray quotes from pyproject.toml section headers

- Fixed [project.scripts]\" to [project.scripts]  
- Fixed [project.optional-dependencies]\" to [project.optional-dependencies]
- Fixed other section headers with trailing quotes
- This was preventing uv/pip from installing the package via git+https"
    
    # Push
    echo "Pushing to GitHub..."
    git push origin main
else
    echo "No changes to commit. Checking if fix is needed..."
    
    # Check for the issue
    if grep -q '\[project.scripts\]"' pyproject.toml; then
        echo "Found issue - applying fix..."
        
        # Fix all section headers
        sed -i 's/\[project\.scripts\]"/[project.scripts]/' pyproject.toml
        sed -i 's/\[project\.optional-dependencies\]"/[project.optional-dependencies]/' pyproject.toml
        sed -i 's/\[build-system\]"/[build-system]/' pyproject.toml
        sed -i 's/\[tool\.\([^]]*\)\]"/[tool.\1]/g' pyproject.toml
        
        # Add and commit
        git add pyproject.toml
        git commit -m "fix: remove stray quotes from pyproject.toml section headers

- Fixed [project.scripts]\" to [project.scripts]
- Fixed [project.optional-dependencies]\" to [project.optional-dependencies]  
- Fixed other section headers with trailing quotes
- This was preventing uv/pip from installing the package via git+https"
        
        # Push
        echo "Pushing to GitHub..."
        git push origin main
    else
        echo "pyproject.toml appears to be already fixed"
        
        # Pull latest to make sure we're in sync
        git pull origin main
    fi
fi

# Return to original directory
cd "$CURRENT_DIR"

echo ""
echo "Now running uv sync in shared_claude_docs..."
uv sync