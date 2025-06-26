#!/bin/bash
# Set up Python paths for Granger ecosystem

export PYTHONPATH="/home/graham/workspace/experiments/sparta/src:/home/graham/workspace/experiments/marker/src:/home/graham/workspace/experiments/arangodb/src:/home/graham/workspace/experiments/youtube_transcripts/src:/home/graham/workspace/experiments/rl_commons/src:/home/graham/workspace/experiments/world_model/src:/home/graham/workspace/experiments/claude-test-reporter/src:/home/graham/workspace/experiments/llm_call/src:/home/graham/workspace/experiments/gitget/src:/home/graham/workspace/mcp-servers/arxiv-mcp-server/src:/home/graham/workspace/experiments/unsloth_wip/src:/home/graham/workspace/experiments/darpa_crawl/src:/home/graham/workspace/experiments/chat/src:/home/graham/workspace/experiments/annotator/src:/home/graham/workspace/experiments/aider-daemon/src:/home/graham/workspace/experiments/granger_hub/src:/home/graham/workspace/experiments/claude-module-communicator/src:/home/graham/workspace/experiments/mcp-screenshot/src:/home/graham/workspace/shared_claude_docs/project_interactions:/home/graham/workspace/shared_claude_docs:$PYTHONPATH"

echo "✅ Python paths configured for Granger ecosystem"
echo "You can now run: python run_final_ecosystem_test.py"
