#!/bin/bash
# Fix unsloth_wip broken submodule - Version 2

set -e

UNSLOTH_DIR="/home/graham/workspace/experiments/unsloth_wip"

echo "🔧 Fixing unsloth_wip submodule issue (v2)..."

cd "$UNSLOTH_DIR"

# Remove any existing submodule configuration
echo "🧹 Cleaning up old submodule configuration..."
git config --file .git/config --remove-section submodule.repos/runpod_llm_ops 2>/dev/null || true
rm -f .gitmodules
rm -rf .git/modules/repos/runpod_llm_ops

# Remove the directory if it exists
if [ -d "repos/runpod_llm_ops" ]; then
    echo "🗑️  Removing existing directory..."
    rm -rf repos/runpod_llm_ops
fi

# Add the submodule fresh
echo "➕ Adding submodule fresh..."
git submodule add https://github.com/grahama1970/runpod_ops.git repos/runpod_llm_ops

# Stage and commit changes
echo "💾 Committing submodule fixes..."
git add .gitmodules repos/runpod_llm_ops
git commit -m "fix: repair broken runpod_llm_ops submodule

- Removed old broken submodule references
- Added fresh submodule pointing to runpod_ops
- This should resolve the 'No url found' error"

echo "📤 Pushing to GitHub..."
git push

echo "✅ Submodule fix complete!"