#!/bin/bash

echo "=== Temporary workaround for arangodb dependency ==="

# Comment out arangodb dependency temporarily
echo "Commenting out arangodb dependency..."
sed -i 's/^    "arangodb @ git/    # "arangodb @ git/' pyproject.toml

# Run uv sync
echo "Running uv sync without arangodb..."
uv sync

if [ $? -eq 0 ]; then
    echo "✅ uv sync successful without arangodb!"
    
    # Install in editable mode
    echo "Installing shared_claude_docs in editable mode..."
    uv pip install -e .
    
    echo ""
    echo "⚠️  IMPORTANT: arangodb dependency is temporarily disabled!"
    echo "To re-enable after fixing GitHub authentication:"
    echo "  1. Fix arangodb repo: gh auth login"
    echo "  2. Push the fix: cd /tmp/*/arangodb && git push"
    echo "  3. Uncomment in pyproject.toml: sed -i 's/# \"arangodb/\"arangodb/' pyproject.toml"
    echo "  4. Run: uv sync"
else
    echo "❌ uv sync still failing even without arangodb"
fi