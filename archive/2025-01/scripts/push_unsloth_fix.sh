#!/bin/bash
# Push unsloth_wip fixes to GitHub

UNSLOTH_DIR="/home/graham/workspace/experiments/unsloth_wip"

echo "📤 Pushing unsloth_wip fixes to GitHub..."

cd "$UNSLOTH_DIR"

# Check status
echo "📊 Git status:"
git status --short

# Push any unpushed commits
echo "🚀 Pushing to GitHub..."
git push

echo "✅ Push complete!"

# Show the last commit
echo ""
echo "📝 Last commit:"
git log -1 --oneline