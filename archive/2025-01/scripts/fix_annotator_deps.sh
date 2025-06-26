#!/bin/bash
# Fix annotator specific dependencies

echo "🔧 Fixing annotator dependencies..."

# Navigate to annotator directory
cd /home/graham/workspace/experiments/annotator

# Activate virtual environment
source /home/graham/workspace/shared_claude_docs/.venv/bin/activate

# Install core dependencies
echo "Installing core dependencies..."
uv add fastapi uvicorn python-multipart aiofiles websockets

# Install ML dependencies
echo "Installing ML dependencies..."
uv add scikit-learn modAL-python

# Install testing dependencies
echo "Installing test dependencies..."
uv add --dev pytest pytest-asyncio pytest-cov

# Install playwright for UI tests
echo "Installing playwright..."
uv add --dev playwright
playwright install chromium

echo "✅ Annotator dependencies fixed!"

# Quick test
echo "Testing import..."
python -c "import annotator.api.app; print('✅ Import successful')" || echo "❌ Import failed"