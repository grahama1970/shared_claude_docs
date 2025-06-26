#!/bin/bash

echo "=== Pushing arangodb pyproject.toml fix ==="

# Go to arangodb
cd /home/graham/workspace/experiments/arangodb

# Check current branch and commits
echo "Current branch status:"
git status -sb
echo ""

# Show the commit that needs to be pushed
echo "Commit to push:"
git log --oneline -1

# Try different push methods
echo ""
echo "Attempting to push with gh CLI..."
if command -v gh &> /dev/null; then
    gh auth status
    if [ $? -eq 0 ]; then
        echo "Using gh to push..."
        git push origin main
    else
        echo "gh CLI not authenticated. Run: gh auth login"
    fi
else
    echo "gh CLI not installed"
fi

# If that didn't work, check SSH
echo ""
echo "Checking SSH configuration..."
if [ -f ~/.ssh/id_rsa ] || [ -f ~/.ssh/id_ed25519 ]; then
    echo "SSH key found. Checking remote URL..."
    REMOTE_URL=$(git remote get-url origin)
    echo "Current remote: $REMOTE_URL"
    
    if [[ "$REMOTE_URL" == "https://"* ]]; then
        echo "Converting to SSH URL..."
        git remote set-url origin git@github.com:grahama1970/arangodb.git
        echo "Attempting SSH push..."
        git push origin main
    else
        echo "Already using SSH. Attempting push..."
        git push origin main
    fi
else
    echo "No SSH key found"
fi

# Return to shared_claude_docs
cd /home/graham/workspace/shared_claude_docs

echo ""
echo "=== Authentication Setup Instructions ==="
echo "If push failed, please run ONE of these:"
echo ""
echo "Option 1 - GitHub CLI (easiest):"
echo "  gh auth login"
echo ""
echo "Option 2 - SSH key:"
echo "  ssh-keygen -t ed25519 -C 'your-email@example.com'"
echo "  cat ~/.ssh/id_ed25519.pub"
echo "  # Add the key to: https://github.com/settings/keys"
echo ""
echo "After authentication is set up, run:"
echo "  cd /home/graham/workspace/experiments/arangodb"
echo "  git push origin main"