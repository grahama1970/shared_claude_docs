# Granger MCP Prompts Standard

**Version**: 1.0.0  
**Date**: 2025-06-03  
**Status**: Active Standard  

## 🎯 Executive Summary

This document defines the standard for implementing MCP (Model Context Protocol) prompts across all Granger ecosystem projects. Based on the principles from "How I build Agentic MCP Servers for Claude Code (Prompts CHANGE Everything)", this standard ensures consistent, discoverable, and powerful agentic workflows across all spoke projects.

## 📚 Core Principles

### The MCP Hierarchy
1. **Resources** → Basic data access (lowest capability)
2. **Tools** → Individual actions (mid-level)
3. **Prompts** → Workflows composing tools (highest leverage)

### Why Prompts Matter
- **10x Leverage**: Prompts compose multiple tools into complete workflows
- **Self-Documenting**: Agents discover capabilities without external docs
- **Guided Experience**: Each prompt suggests next steps
- **Context Preservation**: Build on previous interactions

## 🏗️ Architecture Standard

### Directory Structure
```
project_name/
├── src/
│   └── project_name/
│       └── mcp/
│           ├── __init__.py
│           ├── prompts.py          # Core infrastructure (copy from template)
│           ├── server.py           # FastMCP server with prompts
│           ├── [project]_prompts.py # Project-specific prompts
│           └── tools/              # Individual tool implementations
│               ├── __init__.py
│               └── *.py            # One tool per file
├── mcp.json                        # MCP configuration
└── claude_workspace.json           # Claude Code workspace config
```

### Naming Conventions
- **Prompts**: `project:action` (e.g., `youtube:research`, `sparta:analyze`)
- **Slash Commands**: `/project:action` or `/project action`
- **Categories**: discovery, research, analysis, integration, export, help

## 🔧 Implementation Requirements

### 1. Core Infrastructure
Every spoke project MUST implement these base files:

#### `mcp/prompts.py` - Core Infrastructure
```python
"""
MCP Prompt Infrastructure for [Project Name]

Copy this file from the YouTube Transcripts reference implementation.
DO NOT MODIFY the core classes unless extending functionality.
"""
# Copy from: youtube_transcripts/src/youtube_transcripts/mcp/prompts.py
```

#### `mcp/[project]_prompts.py` - Project Prompts
```python
"""
[Project Name] MCP Prompts

Implements domain-specific prompts for [project description].
"""

from .prompts import mcp_prompt, format_prompt_response, get_prompt_registry

# REQUIRED: Capabilities discovery prompt
@mcp_prompt(
    name="project:capabilities",
    description="List all available MCP server capabilities",
    category="discovery"
)
async def list_capabilities(registry: Any = None) -> str:
    """MUST be implemented by every project"""
    # Implementation

# REQUIRED: Help prompt
@mcp_prompt(
    name="project:help",
    description="Get context-aware help",
    category="help"
)
async def get_help(context: Optional[str] = None) -> str:
    """MUST be implemented by every project"""
    # Implementation

# REQUIRED: Quick start prompt
@mcp_prompt(
    name="project:quick-start",
    description="Quick start guide for new users",
    category="discovery"
)
async def quick_start() -> str:
    """MUST be implemented by every project"""
    # Implementation
```

### 2. FastMCP Server Implementation
```python
"""
[Project Name] FastMCP Server
"""
from fastmcp import FastMCP
from .[project]_prompts import register_all_prompts

mcp = FastMCP("project-name")

# Register all prompts
register_all_prompts()
prompt_registry = get_prompt_registry()

# Expose prompts as FastMCP prompts
@mcp.prompt()
async def capabilities() -> str:
    return await prompt_registry.execute("project:capabilities")

# ... expose other prompts ...
```

### 3. MCP Configuration
```json
{
  "name": "project-name",
  "version": "1.0.0",
  "description": "Project description with prompt support",
  "prompts": {
    "capabilities": {
      "description": "List all capabilities",
      "slash_command": "/project:capabilities"
    }
    // ... other prompts
  }
}
```

## 📋 Required Prompts

Every Granger spoke project MUST implement these prompts:

### 1. Discovery Prompts
- `project:capabilities` - List all features
- `project:quick-start` - Getting started guide
- `project:help` - Context-aware assistance

### 2. Domain-Specific Prompts
Based on project type:

#### Data/Research Projects
- `project:find` - Discover available data
- `project:research` - Research workflows
- `project:analyze` - Deep analysis

#### Processing/Tool Projects
- `project:process` - Main processing workflow
- `project:status` - Check processing status
- `project:export` - Export results

#### Integration Projects
- `project:connect` - Connect to services
- `project:sync` - Synchronization workflows
- `project:monitor` - Monitoring capabilities

## 🔄 Integration with Claude Module Communicator

The hub project (claude-module-communicator) should:

1. **Discovery**: Automatically discover all spoke prompts
2. **Routing**: Route `/hub:discover` to list all spokes
3. **Orchestration**: Compose spoke prompts into meta-workflows

Example hub prompt:
```python
@mcp_prompt(
    name="hub:orchestrate",
    description="Orchestrate multiple spoke modules",
    category="integration"
)
async def orchestrate_workflow(
    workflow: str,
    modules: List[str]
) -> str:
    """Coordinate actions across multiple spokes"""
    # Implementation
```

## 🧪 Testing Requirements

### Unit Tests
```python
# tests/mcp/test_prompts.py
class TestProjectPrompts:
    def test_all_required_prompts_exist(self):
        """Verify all required prompts are implemented"""
        
    def test_prompt_categories(self):
        """Verify prompts are properly categorized"""
        
    def test_prompt_discovery(self):
        """Test that prompts are discoverable"""
```

### Integration Tests
- Test with Claude Code slash commands
- Verify autocomplete shows all prompts
- Test prompt chaining and workflows

## 📊 Compliance Checklist

Before marking a spoke project as compliant:

- [ ] Core infrastructure files exist
- [ ] All required prompts implemented
- [ ] FastMCP server exposes prompts
- [ ] MCP configuration includes prompts
- [ ] Slash commands work in Claude Code
- [ ] Tests pass (unit and integration)
- [ ] Documentation updated

## 🚀 Migration Guide

For existing spoke projects:

1. **Copy Infrastructure**
   ```bash
   cp youtube_transcripts/src/youtube_transcripts/mcp/prompts.py \
      your_project/src/your_project/mcp/prompts.py
   ```

2. **Implement Required Prompts**
   - Start with capabilities, help, quick-start
   - Add domain-specific prompts

3. **Update MCP Server**
   - Switch to FastMCP if needed
   - Expose prompts alongside tools

4. **Test Integration**
   - Verify in Claude Code
   - Check slash command autocomplete

## 📚 Reference Implementation

The YouTube Transcripts project serves as the reference implementation:
- Path: `/home/graham/workspace/experiments/youtube_transcripts/`
- Study: `src/youtube_transcripts/mcp/` directory
- Test: `/youtube:capabilities` in Claude Code

## 🎓 Training Resources

1. **Video**: "How I build Agentic MCP Servers for Claude Code"
2. **Transcript**: Available in YouTube Transcripts docs
3. **Key Insight**: "Prompts are recipes for repeat solutions"

## 🔒 Security Considerations

- Never expose sensitive operations in prompts
- Validate all prompt inputs
- Use proper authentication for privileged actions
- Log prompt usage for audit trails

## 📈 Future Enhancements

### Phase 2: Cross-Module Prompts
- Prompts that coordinate multiple spokes
- Shared context between modules
- Meta-workflows spanning projects

### Phase 3: Learning Prompts
- Prompts that adapt based on usage
- Personalized workflows
- Performance optimization

## 🤝 Contributing

To propose changes to this standard:
1. Create implementation in a spoke project
2. Document benefits and use cases
3. Submit to graham@granger-project.com
4. Test with at least 2 other spokes

---

**Remember**: Tools are just the beginning. Prompts are where the real power lies!