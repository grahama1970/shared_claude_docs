#!/bin/bash
"""
Install all Granger projects in editable mode for local development.
This avoids authentication issues with private GitHub repositories.
"""

set -e  # Exit on error

echo "🔧 Installing Granger Ecosystem in Development Mode"
echo "=================================================="

# Ensure we're in the right directory
cd /home/graham/workspace/shared_claude_docs

# Activate virtual environment
source .venv/bin/activate

echo "✅ Virtual environment activated: $(which python)"

# Install shared_claude_docs first
echo "📦 Installing shared_claude_docs..."
uv pip install -e .

# Core Infrastructure (Level 0-1)
echo "📦 Installing Core Infrastructure..."
uv pip install -e /home/graham/workspace/experiments/granger_hub
uv pip install -e /home/graham/workspace/experiments/rl_commons  
uv pip install -e /home/graham/workspace/experiments/world_model
uv pip install -e /home/graham/workspace/experiments/claude-test-reporter

# Processing Infrastructure (Level 2)
echo "📦 Installing Processing Infrastructure..."
uv pip install -e /home/graham/workspace/experiments/llm_call
uv pip install -e /home/graham/workspace/experiments/arangodb

# Processing Spokes (Level 3)
echo "📦 Installing Processing Spokes..."
uv pip install -e /home/graham/workspace/experiments/sparta
uv pip install -e /home/graham/workspace/experiments/marker
uv pip install -e /home/graham/workspace/experiments/youtube_transcripts
uv pip install -e /home/graham/workspace/experiments/unsloth_wip
uv pip install -e /home/graham/workspace/experiments/darpa_crawl

# User Interfaces (Level 4)
echo "📦 Installing User Interfaces..."
uv pip install -e /home/graham/workspace/granger-ui
uv pip install -e /home/graham/workspace/experiments/chat
uv pip install -e /home/graham/workspace/experiments/annotator
uv pip install -e /home/graham/workspace/experiments/aider-daemon

# MCP Services (Level 5)
echo "📦 Installing MCP Services..."
uv pip install -e /home/graham/workspace/mcp-servers/arxiv-mcp-server
uv pip install -e /home/graham/workspace/experiments/mcp-screenshot
uv pip install -e /home/graham/workspace/experiments/gitget

echo ""
echo "✅ All Granger projects installed in editable mode!"
echo ""
echo "To verify installation:"
echo "  python -c 'import granger_hub; import llm_call; import sparta; print(\"✅ Core imports working!\")'"