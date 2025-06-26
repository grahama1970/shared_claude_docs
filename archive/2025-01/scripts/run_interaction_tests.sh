#!/bin/bash
# Run Level 0-4 Interaction Tests

echo "🧪 Running Granger Interaction Tests"
echo "===================================="

# Activate virtual environment
source /home/graham/workspace/shared_claude_docs/.venv/bin/activate

# Level 0 Tests
echo -e "\n📊 Level 0: Basic Module Tests"
cd /home/graham/workspace/shared_claude_docs/project_interactions
python -m pytest arangodb/level_0_tests/test_query.py -v || true
python -m pytest arxiv-mcp-server/level_0_tests/test_search_papers.py -v || true

# Level 1 Tests
echo -e "\n📊 Level 1: Single Module Interactions"
# Add Level 1 tests here

# Level 2 Tests
echo -e "\n📊 Level 2: Two Module Interactions"
python -m pytest level_2_tests/test_arxiv_marker_arangodb.py -v || true

# Level 3 Tests
echo -e "\n📊 Level 3: Full Pipeline Tests"
python -m pytest level_3_tests/test_full_granger_pipeline.py -v || true

# Level 4 Tests
echo -e "\n📊 Level 4: UI Interaction Tests"
# Add UI tests here

echo -e "\n✅ Test run complete!"
