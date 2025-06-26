# Granger Hub-Spoke Integration Guide

**Version**: 1.0.0  
**Date**: 2025-06-03  
**Status**: All Spokes Hub-Ready ✅

## Overview

The Granger ecosystem consists of a central hub (granger_hub) and 11 spoke projects, all implementing consistent MCP prompts for seamless integration.

## Hub Architecture

```
┌─────────────────────────────────────┐
│        Granger Hub (Hub)            │
│  /hub:discover → Lists all spokes   │
│  /hub:orchestrate → Cross-module    │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┬────────────┬─────────────┐
    │                     │            │             │
┌───▼────┐         ┌─────▼─────┐ ┌───▼──────┐ ┌────▼────┐
│  DARPA  │         │  GitGet   │ │  Marker  │ │  ArXiv  │
│  Crawl  │         │           │ │          │ │   MCP   │
└─────────┘         └───────────┘ └──────────┘ └─────────┘
    ...                 ...           ...          ...
```

## Spoke Consistency Matrix

| Project | Slash Command | MCP Config | FastMCP | Hub-Ready |
|---------|---------------|------------|---------|-----------|
| darpa_crawl | `/darpa_crawl:*` | ✅ | ✅ | ✅ |
| gitget | `/gitget:*` | ✅ | ✅ | ✅ |
| aider-daemon | `/aider-daemon:*` | ✅ | ✅ | ✅ |
| sparta | `/sparta:*` | ✅ | ✅ | ✅ |
| marker | `/marker:*` | ✅ | ✅ | ✅ |
| arangodb | `/arangodb:*` | ✅ | ✅ | ✅ |
| youtube_transcripts | `/youtube:*` | ✅ | ✅ | ✅ |
| claude_max_proxy | `/claude_max_proxy:*` | ✅ | ✅ | ✅ |
| arxiv-mcp-server | `/arxiv-mcp-server:*` | ✅ | ✅ | ✅ |
| fine_tuning | `/fine_tuning:*` | ✅ | ✅ | ✅ |
| mcp-screenshot | `/mcp-screenshot:*` | ✅ | ✅ | ✅ |

## Standard Spoke Interface

Every spoke implements:

### 1. Required Prompts
```
/PROJECT:capabilities  - List all features
/PROJECT:help         - Context-aware help
/PROJECT:quick-start  - Getting started guide
```

### 2. MCP Configuration (mcp.json)
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "main": "src/module_name/mcp/server.py",
  "prompts": {
    "capabilities": {
      "slash_command": "/project:capabilities"
    },
    // ... other prompts
  }
}
```

### 3. CLI Integration
```python
from granger_slash_mcp_mixin import add_slash_mcp_commands
add_slash_mcp_commands(app, project_name="project-name")
```

### 4. FastMCP Server
```python
from fastmcp import FastMCP
mcp = FastMCP("project-name")

@mcp.prompt()
async def capabilities() -> str:
    return await prompt_registry.execute("project:capabilities")
```

## Hub Discovery Pattern

The hub can discover all spokes:

```python
# In granger_hub
@mcp_prompt(name="hub:discover")
async def discover_spokes() -> str:
    spokes = []
    for project in SPOKE_PROJECTS:
        try:
            # Execute capabilities prompt
            caps = await execute_prompt(f"{project}:capabilities")
            spokes.append({
                "name": project,
                "capabilities": parse_capabilities(caps)
            })
        except:
            spokes.append({
                "name": project,
                "status": "offline"
            })
    
    return format_spoke_discovery(spokes)
```

## Cross-Module Orchestration

Example: Research workflow across multiple spokes

```python
@mcp_prompt(name="hub:research-workflow")
async def research_workflow(topic: str) -> str:
    # 1. Search ArXiv for papers
    papers = await execute_prompt(
        "arxiv-mcp-server:research-topic",
        query=topic
    )
    
    # 2. Search YouTube for discussions
    videos = await execute_prompt(
        "youtube:research",
        query=topic
    )
    
    # 3. Extract key concepts
    concepts = await execute_prompt(
        "gitget:extract-patterns",
        content=papers + videos
    )
    
    # 4. Store in knowledge graph
    await execute_prompt(
        "arangodb:import-data",
        data=concepts
    )
    
    return format_research_results(papers, videos, concepts)
```

## Spoke Categories

### Research & Analysis
- **arxiv-mcp-server**: Academic papers
- **youtube_transcripts**: Video content
- **gitget**: Code analysis

### Processing & Enhancement
- **marker**: Document conversion
- **aider-daemon**: Code improvement
- **claude_max_proxy**: LLM optimization

### Data & Security
- **arangodb**: Knowledge storage
- **sparta**: Security scanning
- **darpa_crawl**: Funding opportunities

### Tools & Training
- **fine_tuning**: Model fine-tuning
- **mcp-screenshot**: UI analysis

## Integration Testing

Run the consistency check:
```bash
python /path/to/check_hub_consistency.py
```

Test hub discovery:
```
/hub:discover
```

Test cross-module workflow:
```
/hub:orchestrate --modules "arxiv,youtube,arangodb" --task "research AI safety"
```

## Best Practices

1. **Consistent Naming**: Always use project name from mcp.json
2. **Error Handling**: Spokes should handle offline/error states gracefully
3. **Performance**: Use async execution for parallel spoke queries
4. **Caching**: Hub should cache spoke capabilities for efficiency
5. **Monitoring**: Track spoke availability and response times

## Future Enhancements

1. **Dynamic Discovery**: Auto-discover new spokes
2. **Load Balancing**: Distribute work across similar spokes
3. **Failover**: Automatic fallback when spokes are offline
4. **Metrics**: Usage tracking and optimization
5. **Security**: Spoke authentication and authorization

## Conclusion

All 11 spoke projects are fully consistent and ready for hub integration. The standardized interface ensures:
- Easy discovery via `/PROJECT:capabilities`
- Consistent orchestration patterns
- Maintainable codebase
- Scalable architecture

The Granger ecosystem is ready for intelligent, cross-module workflows! 🚀