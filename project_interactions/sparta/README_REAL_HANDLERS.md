# Real SPARTA Handlers for GRANGER Integration

This directory contains real SPARTA handlers that integrate with the actual SPARTA module functionality for the GRANGER ecosystem.

## Overview

The real SPARTA handlers provide Level 0 interactions that directly use SPARTA's core functionality:

1. **Resource Download** - Downloads cybersecurity resources from STIX datasets
2. **NASA Mission Search** - Searches NASA mission data via NASA Open APIs
3. **CVE Search** - Queries the National Vulnerability Database (NVD)
4. **MITRE Integration** - Accesses MITRE ATT&CK, CAPEC, and D3FEND frameworks
5. **Module Interface** - Uses SPARTA's claude-module-communicator interface

## Handler Classes

### SPARTADownloadHandler
Downloads cybersecurity resources using SPARTA's smart downloader with paywall bypass capabilities.

```python
handler = SPARTADownloadHandler()
result = await handler.execute(limit=10)
print(f"Downloaded {result.output_data['resources_downloaded']} resources")
```

### SPARTAMissionSearchHandler
Searches NASA mission data using the NASA Images and Video Library API.

```python
handler = SPARTAMissionSearchHandler()
result = await handler.execute(query="Apollo", limit=5)
print(f"Found {result.output_data['missions_found']} missions")
```

### SPARTACVESearchHandler
Queries the National Vulnerability Database for CVE information.

```python
handler = SPARTACVESearchHandler()
result = await handler.execute(keywords="satellite", severity="HIGH", limit=10)
print(f"Found {result.output_data['vulnerabilities_found']} vulnerabilities")
```

### SPARTAMITREHandler
Accesses MITRE framework data (ATT&CK, CAPEC, D3FEND).

```python
handler = SPARTAMITREHandler()
result = await handler.execute(framework="attack", query="T1055")
print(f"Found: {result.output_data['found']}")
```

### SPARTAModuleHandler
Uses SPARTA's module interface for claude-module-communicator integration.

```python
handler = SPARTAModuleHandler()
result = await handler.execute(
    action="search_space_missions",
    data={"query": "Mars", "limit": 3}
)
```

## Key Features

- **Real API Integration**: Uses actual NASA and NVD APIs
- **Smart Download**: Handles paywalls and multiple download strategies
- **MITRE Frameworks**: Full integration with ATT&CK, CAPEC, and D3FEND
- **Async Support**: All handlers are async for efficient processing
- **Error Handling**: Graceful degradation when SPARTA is not available

## Requirements

- SPARTA module must be installed at `/home/graham/workspace/experiments/sparta/`
- Dependencies: `aiohttp`, `fastmcp`, `loguru`
- Optional: NASA API key (uses DEMO_KEY by default)
- Optional: NVD API key (for higher rate limits)

## Testing

Run the test suite to validate all handlers:

```bash
python test_real_sparta_handlers.py
```

This will:
1. Test each handler with real data
2. Measure performance and timing
3. Generate a detailed JSON report
4. Provide a summary of results

## Integration with GRANGER

These handlers are designed to work within the GRANGER hub-spoke architecture:

1. **Level 0**: Direct module functionality (these handlers)
2. **Level 1**: Module-to-module interactions
3. **Level 2**: Multi-module workflows
4. **Level 3**: Complex scenarios with RL optimization

## Example Usage in GRANGER

```python
# In a GRANGER workflow
from project_interactions.sparta.real_sparta_handlers import (
    SPARTADownloadHandler,
    SPARTAMissionSearchHandler
)

# Download space cybersecurity resources
download_handler = SPARTADownloadHandler()
download_result = await download_handler.execute(limit=100)

# Search for related missions
mission_handler = SPARTAMissionSearchHandler()
mission_result = await mission_handler.execute(query="ISS security")

# Combine results for further processing
combined_data = {
    "resources": download_result.output_data,
    "missions": mission_result.output_data
}
```

## Differences from Mock Handlers

The `cybersecurity_enrichment_interaction.py` file contains mock handlers for testing without SPARTA. The real handlers:

- Use actual APIs instead of mock data
- Have real network latency and rate limits
- Provide authentic data from NASA and NVD
- May fail due to network issues or API limits
- Require proper SPARTA installation

## Environment Variables

- `NASA_API_KEY`: NASA API key (optional, defaults to DEMO_KEY)
- `NVD_API_KEY`: NVD API key (optional, for higher rate limits)
- `SPARTA_USE_MOCK`: Set to "false" to force real API usage in SPARTAModule

## Troubleshooting

1. **SPARTA not available**: Ensure SPARTA is installed at the correct path
2. **API rate limits**: Add API keys for higher limits
3. **Network errors**: Check internet connectivity
4. **Import errors**: Install missing dependencies with `pip install aiohttp loguru`

## Future Enhancements

- Add caching for API responses
- Implement retry logic for failed requests
- Add more granular error handling
- Support for batch operations
- Integration with SPARTA's MCP server