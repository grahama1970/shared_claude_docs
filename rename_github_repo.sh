#!/bin/bash
# Script to rename GitHub repository and update git remote

echo "=== Renaming GitHub Repository ==="
echo "Current directory: /home/graham/workspace/experiments/fine_tuning"
echo ""

# Navigate to the project directory
cd /home/graham/workspace/experiments/fine_tuning || exit 1

# Show current remote
echo "Current git remote:"
git remote -v
echo ""

# Rename the GitHub repository
echo "Renaming GitHub repository to 'fine_tuning'..."
gh repo rename fine_tuning

# Update the git remote URL
echo "Updating git remote URL..."
git remote set-url origin git+https://github.com/grahama1970/fine_tuning.git

# Verify the change
echo ""
echo "New git remote:"
git remote -v

echo ""
echo "=== GitHub Repository Rename Complete ==="