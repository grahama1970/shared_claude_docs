# Quick Setup Guide for Testing Module Integration

## Prerequisites

### 1. Environment Variables
Create a `.env` file with required API keys:
```bash
# API Keys
export ANTHROPIC_API_KEY="your-anthropic-key"
export GEMINI_API_KEY="your-gemini-key"
export YOUTUBE_API_KEY="your-youtube-key"
export OPENAI_API_KEY="your-openai-key"  # Optional

# Vertex AI (for mcp-screenshot)
export VERTEX_AI_PROJECT="your-project-id"
export VERTEX_AI_LOCATION="us-central1"
export VERTEX_AI_SERVICE_ACCOUNT_FILE="./vertex_ai_service_account.json"

# ArangoDB
export ARANGO_HOST="localhost"
export ARANGO_PORT="8529"
export ARANGO_USERNAME="root"
export ARANGO_PASSWORD="your-password"
export ARANGO_DATABASE="memory_bank"
```

### 2. Install All Modules
```bash
# Install each module
cd /home/graham/workspace/experiments/sparta && pip install -e .
cd /home/graham/workspace/experiments/marker && pip install -e .
cd /home/graham/workspace/experiments/arangodb && pip install -e .
cd /home/graham/workspace/experiments/youtube_transcripts && pip install -e .
cd /home/graham/workspace/experiments/llm_call && pip install -e .
cd /home/graham/workspace/mcp-servers/arxiv-mcp-server && pip install -e .
cd /home/graham/workspace/experiments/granger_hub && pip install -e .
cd /home/graham/workspace/experiments/claude-test-reporter && pip install -e .
cd /home/graham/workspace/experiments/mcp-screenshot && pip install -e .
```

### 3. Start Required Services

#### Terminal 1: ArangoDB
```bash
# Using Docker
docker run -d \
  --name arangodb \
  -p 8529:8529 \
  -e ARANGO_ROOT_PASSWORD=your_password \
  arangodb/arangodb:latest

# Or native installation
arangod
```

#### Terminal 2: Granger Hub
```bash
cd /home/graham/workspace/experiments/granger_hub
python -m granger_hub.cli.main serve --port 8000
```

#### Terminal 3: Marker Server (Optional)
```bash
cd /home/graham/workspace/experiments/marker
MCP_SERVER_PORT=3000 uv run python -m marker.mcp.server
```

#### Terminal 4: ArangoDB MCP Server (Optional)
```bash
cd /home/graham/workspace/experiments/arangodb
python -m arangodb.cli.main serve-mcp --host localhost --port 5000
```

## Running the Tests

### Option 1: Run All Tests
```bash
cd /home/graham/workspace/shared_claude_docs/docs/test_scenarios
python test_implementation.py
```

### Option 2: Test Individual Modules
```bash
# Test ArXiv
python -c "
import asyncio
from test_implementation import ModuleCommunicatorTester
tester = ModuleCommunicatorTester()
result = asyncio.run(tester.execute_mcp_tool_command(
    'arxiv-mcp-server',
    'search_papers',
    {'query': 'test', 'max_results': 1}
))
print(result)
"

# Test YouTube
youtube-cli search "test" --limit 1

# Test Screenshot
mcp-screenshot regions

# Test SPARTA
sparta-cli search "test"
```

### Option 3: Test Specific Scenario
```bash
python -c "
import asyncio
from test_implementation import ModuleCommunicatorTester
tester = ModuleCommunicatorTester()
# Choose scenario: 1, 2, or 3
result = asyncio.run(tester.test_scenario_1_research_pipeline())
"
```

## Verification Checklist

### ✅ Basic Health Checks
- [ ] granger_hub responds on port 8000
- [ ] arxiv-mcp-server accepts search commands
- [ ] sparta-mcp-server returns resources
- [ ] youtube-cli searches and returns results
- [ ] mcp-screenshot lists screen regions
- [ ] claude-test-report shows version

### ✅ Integration Tests
- [ ] Data flows from ArXiv → Marker → ArangoDB
- [ ] YouTube transcripts can be searched and analyzed
- [ ] Screenshots can be captured and analyzed
- [ ] Multi-model analysis works via llm_call
- [ ] Test reports generate successfully

### ✅ Advanced Features
- [ ] Knowledge graphs visualize correctly
- [ ] Real-time monitoring updates work
- [ ] Learning paths generate appropriately
- [ ] Progress tracking persists data

## Troubleshooting

### "Connection refused" errors
```bash
# Check service is running
lsof -i :8000  # granger_hub
lsof -i :3000  # marker
lsof -i :5000  # arangodb mcp
lsof -i :8529  # arangodb
```

### "Module not found" errors
```bash
# Ensure module is in Python path
python -c "import granger_hub; print('✅ Found')"
python -c "import arxiv_mcp_server; print('✅ Found')"
```

### API Key errors
```bash
# Verify environment variables
echo $ANTHROPIC_API_KEY
echo $YOUTUBE_API_KEY
```

### MCP Tool errors
```bash
# Test MCP tools directly
python -m arxiv_mcp_server  # Should show MCP protocol output
sparta-mcp-server  # Should show FastMCP output
```

## Expected Output

When all tests pass, you should see:
```
✅ Granger Hub is running

=== Testing Scenario 1: Research Pipeline ===
✅ Found 5 papers
✅ Found 10 SPARTA resources
✅ Found 5 videos
✅ Marker service is available
✅ ArangoDB service is available
✅ Screenshot service supports 5 regions

=== Testing Scenario 2: Security Monitoring ===
✅ Found 10 security videos
✅ Found 3 recent papers
✅ Alert storage capability verified

=== Testing Scenario 3: Learning System ===
✅ machine learning basics: 5 videos, 5 papers
✅ neural networks: 5 videos, 5 papers
✅ Visualization capability verified
✅ Progress tracking structure validated

Test Summary
============
Total Scenarios: 3
Successful: 3
Failed: 0

Results saved to: test_results_20250529_120000.json
```

## Next Steps

1. Review test results in the generated JSON file
2. Check logs for any warnings or optimization opportunities
3. Run specific scenarios with real data
4. Monitor resource usage during tests
5. Implement continuous integration tests
