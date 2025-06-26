#!/bin/bash

echo "=== Fixing Private Repository Authentication for SPARTA ==="
echo ""
echo "Since SPARTA is a private repository, you need one of these authentication methods:"
echo ""

echo "Option 1: Use GitHub CLI token for HTTPS (Recommended)"
echo "=================================================="
echo "Create a GitHub token with 'repo' scope and configure git:"
echo ""
echo "# Get your token from: https://github.com/settings/tokens"
echo "# Then run:"
echo 'export GITHUB_TOKEN=your_token_here'
echo 'git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"'
echo ""

echo "Option 2: Use SSH instead of HTTPS"
echo "================================="
echo "Change your git config to use SSH for GitHub:"
echo ""
echo 'git config --global url."git@github.com:".insteadOf "https://github.com/"'
echo ""
echo "Make sure your SSH key is added to GitHub:"
echo "cat ~/.ssh/id_ed25519.pub"
echo "# Add this key to: https://github.com/settings/keys"
echo ""

echo "Option 3: Use GitHub CLI authentication"
echo "======================================="
echo "Ensure gh is authenticated and refresh:"
echo ""
echo "gh auth login"
echo "gh auth setup-git"
echo ""

echo "Option 4: Use .netrc file"
echo "========================"
echo "Create ~/.netrc with:"
echo ""
echo "cat > ~/.netrc << EOF"
echo "machine github.com"
echo "login your_github_username"
echo "password your_github_token"
echo "EOF"
echo "chmod 600 ~/.netrc"
echo ""

echo "Option 5: Use environment variable for uv"
echo "========================================"
echo "Set the UV_GITHUB_TOKEN environment variable:"
echo ""
echo "export UV_GITHUB_TOKEN=your_github_token"
echo "uv sync"
echo ""

echo "Current git remote configs:"
git config --global --list | grep url || echo "No URL replacements configured"

echo ""
echo "After setting up authentication, run:"
echo "cd /home/graham/workspace/shared_claude_docs"
echo "uv sync"