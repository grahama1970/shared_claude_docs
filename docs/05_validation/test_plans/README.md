# Granger Hub Test Scenarios

This directory contains comprehensive test scenarios demonstrating how the granger_hub integrates all registered modules to solve complex, real-world problems.

## Overview

The granger_hub serves as the central hub for orchestrating communication between:
- **arxiv-mcp-server** - Academic paper discovery and analysis
- **sparta** - Space cybersecurity threat intelligence
- **marker** - Document processing and text extraction
- **arangodb** - Graph database for knowledge storage
- **youtube_transcripts** - Video content discovery and analysis
- **llm_call** - Multi-model AI analysis
- **mcp-screenshot** - Visual capture and analysis
- **claude-test-reporter** - Testing and validation
- **annotator** - Content extraction validation
- **fine_tuning** - Fine-tuning capabilities (future)

## Test Scenarios

### Scenario 1: Comprehensive Research Pipeline
**File**: `scenario_01_research_pipeline.md`

**Purpose**: Demonstrates a complete academic research workflow combining multiple data sources.

**Modules Used**: All modules

**Key Features**:
- Multi-source data collection (ArXiv, SPARTA, YouTube)
- Document processing and structure extraction
- Knowledge graph construction
- AI-powered analysis with multiple models
- Visual reporting and validation

**Test Commands**:
```bash
# Start granger_hub
cd /home/graham/workspace/experiments/granger_hub
python -m granger_hub.cli.main serve --port 8000

# In another terminal, run the test
python test_research_pipeline.py
```

### Scenario 2: Real-Time Security Monitoring
**File**: `scenario_02_real_time_monitoring.md`

**Purpose**: Shows continuous monitoring and alert generation for security threats.

**Modules Used**: All modules

**Key Features**:
- Continuous source monitoring
- Threat correlation and analysis
- Visual dashboard generation
- Multi-model threat assessment
- Automated alert distribution

**Test Commands**:
```bash
# Start monitoring system
python test_security_monitoring.py --continuous

# Check dashboard
open http://localhost:5000/security_dashboard
```

### Scenario 3: Automated Learning System
**File**: `scenario_03_learning_system.md`

**Purpose**: Creates personalized learning paths from diverse educational content.

**Modules Used**: All modules

**Key Features**:
- Educational content discovery
- Prerequisite detection
- Personalized path generation
- Progress tracking
- Assessment creation

**Test Commands**:
```bash
# Generate learning path
python test_learning_system.py --profile learner_profile.json

# View dashboard
open learning_dashboard.html
```

## Module Communication Patterns

### MCP Tool Communication (via granger_hub)
```python
# For arxiv-mcp-server and sparta
result = await communicator.execute_mcp_tool_command(
    tool_name="arxiv-mcp-server",
    command="search_papers",
    args={...}
)
```

### HTTP API Communication
```python
# For marker and arangodb
result = await communicator.execute_http_api(
    module="marker",
    endpoint="/convert_pdf",
    method="POST",
    data={...}
)
```

### CLI Communication
```python
# For youtube_transcripts, mcp-screenshot, claude-test-reporter
result = await communicator.execute_cli_command(
    module="youtube_transcripts",
    command="search",
    args={...}
)
```

## Testing the System

### Prerequisites
1. All modules must be installed and configured
2. Required API keys in environment variables:
   - `ANTHROPIC_API_KEY`
   - `GEMINI_API_KEY`
   - `YOUTUBE_API_KEY`
   - `VERTEX_AI_SERVICE_ACCOUNT_FILE`

3. Services running:
   - ArangoDB on port 8529
   - granger_hub on port 8000
   - marker server on port 3000 (optional)
   - arangodb MCP server on port 5000

### Quick Test Script
```python
# test_all_modules.py
import asyncio
from granger_hub import ModuleCommunicator

async def test_all_modules():
    comm = ModuleCommunicator()
    
    # Test each module
    modules = [
        ("arxiv-mcp-server", "search_papers", {"query": "test", "max_results": 1}),
        ("sparta-mcp-server", "search_resources", {"query": "test"}),
        ("marker", "/health", {}),  # HTTP health check
        ("arangodb", "/health", {}),  # HTTP health check
        ("youtube_transcripts", "search", {"query": "test", "limit": 1}),
        ("mcp-screenshot", "regions", {}),
        ("claude-test-reporter", "--version", {})
    ]
    
    results = {}
    for module, command, args in modules:
        try:
            if module in ["arxiv-mcp-server", "sparta-mcp-server"]:
                result = await comm.execute_mcp_tool_command(module, command, args)
            elif module in ["marker", "arangodb"]:
                result = await comm.execute_http_api(module, command, "GET", args)
            else:
                result = await comm.execute_cli_command(module, command, args)
            results[module] = "✅ Working"
        except Exception as e:
            results[module] = f"❌ Error: {str(e)}"
    
    return results

# Run test
if __name__ == "__main__":
    results = asyncio.run(test_all_modules())
    for module, status in results.items():
        print(f"{module}: {status}")
```

### Validation Checklist

- [ ] All modules respond to health checks
- [ ] MCP tools accept commands via communicator
- [ ] HTTP APIs return expected schemas
- [ ] CLI tools execute without errors
- [ ] Data flows correctly between modules
- [ ] No schema mismatches
- [ ] Error handling works properly
- [ ] Visual outputs generated correctly
- [ ] Test reports validate pipeline success

## Troubleshooting

### Common Issues

1. **Module Not Found**
   - Ensure module is installed: `pip install -e <module_path>`
   - Check PATH for CLI tools
   - Verify MCP server is running

2. **Connection Refused**
   - Check service is running on expected port
   - Verify firewall settings
   - Check localhost vs 0.0.0.0 binding

3. **Schema Mismatch**
   - Review module documentation
   - Check API version compatibility
   - Validate JSON structure

4. **Timeout Errors**
   - Increase timeout in communicator config
   - Check module resource requirements
   - Monitor system resources

## Next Steps

1. Implement automated test suite
2. Add performance benchmarks
3. Create CI/CD pipeline
4. Build monitoring dashboard
5. Document module-specific optimizations
