# MCP (Model Context Protocol) Setup Guide

## Overview

The Model Context Protocol (MCP) enables Claude to interact with external tools and services. This guide covers setup for all MCP servers in our ecosystem.

## Prerequisites

- Claude Desktop App (latest version)
- Python 3.10+ or Node.js 18+
- Git
- Admin access to modify Claude configuration

## Configuration File Location

### Find Your Config File
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Our MCP Servers

### 1. ArXiv MCP Server

**Purpose**: Search and download research papers from ArXiv

**Installation**:
```bash
cd /home/graham/workspace/experiments/
git clone [arxiv-mcp-server-repo]
cd arxiv-mcp-server
uv venv --python=3.10.11 .venv
source .venv/bin/activate
uv pip install -e .
```

**Configuration**:
```json
{
  "mcpServers": {
    "arxiv": {
      "command": "python",
      "args": ["-m", "arxiv_mcp_server"],
      "cwd": "/home/graham/workspace/experiments/arxiv-mcp-server"
    }
  }
}
```

### 2. Claude Module Communicator

**Purpose**: Enable communication between Claude projects

**Installation**:
```bash
cd /home/graham/workspace/experiments/claude-module-communicator
uv venv --python=3.10.11 .venv
source .venv/bin/activate
uv pip install -e .
```

**Configuration**:
```json
{
  "mcpServers": {
    "module-communicator": {
      "command": "python",
      "args": ["-m", "claude_module_communicator.mcp_server"],
      "cwd": "/home/graham/workspace/experiments/claude-module-communicator",
      "env": {
        "CMC_BASE_URL": "http://localhost:8080",
        "CMC_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 3. ArangoDB MCP Server

**Purpose**: Query and manage ArangoDB graph database

**Installation**:
```bash
cd /home/graham/workspace/experiments/mcp-server-arangodb
npm install
```

**Configuration**:
```json
{
  "mcpServers": {
    "arangodb": {
      "command": "node",
      "args": ["dist/index.js"],
      "cwd": "/home/graham/workspace/experiments/mcp-server-arangodb",
      "env": {
        "ARANGO_HOST": "localhost",
        "ARANGO_PORT": "8529",
        "ARANGO_USERNAME": "root",
        "ARANGO_PASSWORD": "your-password",
        "ARANGO_DATABASE": "claude_projects"
      }
    }
  }
}
```

### 4. File System MCP

**Purpose**: Access local file system

**Configuration**:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/graham/workspace/experiments"
      ]
    }
  }
}
```

### 5. Git MCP Server

**Purpose**: Perform Git operations

**Configuration**:
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git"
      ]
    }
  }
}
```

## Complete Configuration Example

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "python",
      "args": ["-m", "arxiv_mcp_server"],
      "cwd": "/home/graham/workspace/experiments/arxiv-mcp-server"
    },
    "module-communicator": {
      "command": "python",
      "args": ["-m", "claude_module_communicator.mcp_server"],
      "cwd": "/home/graham/workspace/experiments/claude-module-communicator",
      "env": {
        "CMC_BASE_URL": "http://localhost:8080"
      }
    },
    "arangodb": {
      "command": "node",
      "args": ["dist/index.js"],
      "cwd": "/home/graham/workspace/experiments/mcp-server-arangodb",
      "env": {
        "ARANGO_HOST": "localhost",
        "ARANGO_PORT": "8529",
        "ARANGO_USERNAME": "root",
        "ARANGO_PASSWORD": ""
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/graham/workspace/experiments"
      ]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    }
  }
}
```

## Troubleshooting

### Server Not Starting

1. **Check logs**: Claude Desktop logs are in:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%LOCALAPPDATA%\Claude\logs\`

2. **Verify installation**:
   ```bash
   # For Python servers
   python -m arxiv_mcp_server --help
   
   # For Node servers
   node dist/index.js --version
   ```

3. **Test environment variables**:
   ```bash
   export ARANGO_HOST=localhost
   echo 
   ```

### Tools Not Appearing

1. Restart Claude Desktop completely
2. Check server is in the mcpServers config
3. Verify no JSON syntax errors
4. Ensure server implements tool capability

### Permission Errors

1. Check file permissions:
   ```bash
   ls -la /path/to/server
   chmod +x server_executable
   ```

2. For filesystem access, ensure paths are allowed
3. For database access, verify credentials

## Development Tips

### Creating a Python MCP Server

```python
# my_mcp_server/__main__.py
from mcp import Server, Tool
import asyncio

app = Server("my-server")

@app.tool()
async def my_tool(param: str) -> str:
    """Description of what the tool does."""
    return f"Processed: {param}"

if __name__ == "__main__":
    asyncio.run(app.run())
```

### Testing MCP Servers

1. **Manual testing**:
   ```bash
   # Start server directly
   python -m my_mcp_server
   
   # In another terminal, send test requests
   curl -X POST http://localhost:3000/tools/my_tool \
     -H "Content-Type: application/json" \
     -d '{"param": "test"}'
   ```

2. **Integration testing**:
   ```python
   import pytest
   from my_mcp_server import app
   
   @pytest.mark.asyncio
   async def test_my_tool():
       result = await app.tools["my_tool"](param="test")
       assert result == "Processed: test"
   ```

## Best Practices

1. **Use environment variables** for sensitive data
2. **Implement proper error handling** in tools
3. **Add comprehensive logging** for debugging
4. **Document all tools** with clear descriptions
5. **Version your MCP servers** properly
6. **Test thoroughly** before adding to Claude

## Security Notes

1. Never hardcode passwords in config
2. Use read-only database users when possible
3. Limit filesystem access to specific directories
4. Validate all inputs in your tools
5. Implement rate limiting for expensive operations

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [Example Servers](https://github.com/modelcontextprotocol/servers)
