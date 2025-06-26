# Granger Monorepo Architecture Guide

> **Best practices for managing the Granger ecosystem as a monorepo**  
> **Version**: 1.0.0  
> **Date**: 2025-01-09

---

## 🏗️ Architecture Overview

The Granger ecosystem follows a **modified monorepo approach** where:
- Each module lives in its own Git repository (for modularity)
- All modules follow identical standards (for consistency)
- Dependencies are managed centrally via shared_claude_docs
- Modules are installed via Git URLs in editable mode during development

```
Granger Ecosystem (Logical Monorepo)
├── shared_claude_docs/        # Central dependency management
│   ├── pyproject.toml        # Ecosystem-wide dependencies
│   └── CLAUDE.md            # Ecosystem standards
├── experiments/             # Core modules (separate repos)
│   ├── granger_hub/
│   ├── rl_commons/
│   ├── arangodb/
│   └── ...
└── mcp-servers/            # MCP services (separate repos)
    ├── arxiv-mcp-server/
    └── mcp-screenshot/
```

---

## 📦 Dependency Management Strategy

### 1. **Living at HEAD Philosophy**
All modules depend on the latest commit of other modules:
```toml
# Always use Git URLs, not published versions
"arangodb @ git+https://github.com/grahama1970/arangodb.git"
# NOT: "arangodb>=1.0.0"
```

### 2. **Shared Core Dependencies**
Critical dependencies are locked ecosystem-wide:
```toml
# In every module's pyproject.toml
[project]
requires-python = ">=3.10.11"
dependencies = [
    "numpy==1.26.4",          # Ecosystem lock
    "pandas>=2.2.3,<2.3.0",   # Compatible range
    "loguru>=0.7.0",          # Standard logging
    "pydantic>=2.0.0",        # Data validation
]
```

### 3. **Module-Specific Dependencies**
Modules can add their own dependencies but must respect ecosystem constraints:
```toml
# Good - respects ecosystem constraints
"torch>=2.0.0"              # Module-specific
"transformers>=4.35.0"      # Module-specific

# Bad - conflicts with ecosystem
"numpy>=2.0.0"              # Breaks ecosystem lock!
```

### 4. **Development Installation**
During development, install all modules in editable mode:
```bash
# From shared_claude_docs
uv sync  # Installs all ecosystem modules

# For individual module development
cd /path/to/module
uv venv --python=3.10.11
source .venv/bin/activate
uv pip install -e .
```

---

## 🔌 MCP Microservice Architecture

### 1. **Service Design Principles**

Each Granger module should expose MCP endpoints following these patterns:

```python
from fastmcp import FastMCP
from contextlib import asynccontextmanager

# Stateless service (recommended)
mcp = FastMCP("module-name", stateless_http=True)

# With lifecycle management
@asynccontextmanager
async def lifespan(server: FastMCP):
    # Startup
    db = await connect_arangodb()
    yield {"db": db}
    # Shutdown
    await db.close()

mcp = FastMCP("module-name", lifespan=lifespan)
```

### 2. **Standard MCP Endpoints**

Every module MUST implement:

```python
@mcp.prompt()
async def capabilities() -> str:
    """List module capabilities"""
    return "Module capabilities..."

@mcp.prompt()
async def health() -> dict:
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}

@mcp.tool()
async def process(data: dict) -> dict:
    """Main processing function"""
    # Implementation
```

### 3. **Inter-Module Communication**

Modules communicate via the Hub:

```python
# In any module
from granger_hub import execute_remote_prompt

async def cross_module_workflow(query: str):
    # Call another module via Hub
    arxiv_results = await execute_remote_prompt(
        "arxiv-mcp-server:search",
        {"query": query}
    )
    
    # Process locally
    processed = await local_process(arxiv_results)
    
    # Store in ArangoDB via Hub
    await execute_remote_prompt(
        "arangodb:store",
        {"data": processed}
    )
```

---

## 🧪 Testing in a Distributed Monorepo

### 1. **Test Categories**

```
tests/
├── unit/           # No external dependencies
├── integration/    # Single module + dependencies
├── ecosystem/      # Cross-module workflows
└── e2e/           # Complete pipelines
```

### 2. **Ecosystem Testing**

Test cross-module interactions:

```python
# tests/ecosystem/test_research_pipeline.py
@pytest.mark.ecosystem
async def test_research_pipeline():
    # Start required services
    async with start_services(["hub", "arxiv", "arangodb"]):
        # Test complete workflow
        result = await hub.execute_workflow("research", {
            "topic": "quantum computing"
        })
        assert result["status"] == "success"
        assert len(result["papers"]) > 0
```

### 3. **Service Mocking Policy**

**NEVER mock services in ecosystem tests!**
```python
# ❌ FORBIDDEN
@patch('arangodb.store')
def test_storage(mock_store):
    mock_store.return_value = {"id": "fake"}

# ✅ REQUIRED - Use real test instance
async def test_storage(test_arangodb):
    result = await test_arangodb.store(data)
    assert result["id"] is not None
```

---

## 🚀 Deployment Strategy

### 1. **Service Deployment Order**

Deploy in dependency order:
1. **Infrastructure**: ArangoDB, Redis
2. **Core Services**: Hub, RL Commons
3. **Processing Spokes**: SPARTA, Marker, etc.
4. **User Interfaces**: Chat, Annotator

### 2. **Configuration Management**

Each service gets its configuration from:
```bash
# Base configuration
GRANGER_HUB_URL=http://hub:8000
ARANGODB_URL=http://arangodb:8529

# Service-specific
MODULE_NAME=marker
MODULE_PORT=8002
ENABLE_CACHING=true
```

### 3. **Service Discovery**

Services register with the Hub on startup:
```python
@mcp.on_startup
async def register_with_hub():
    await hub.register_service({
        "name": "module-name",
        "url": f"http://{HOST}:{PORT}",
        "capabilities": await capabilities()
    })
```

---

## 📊 Monorepo Management Tools

### 1. **Dependency Updates**

Update all modules together:
```bash
# Update a shared dependency across all modules
/granger:update-dependency numpy==1.26.5

# Check for conflicts before updating
/granger:check-dependencies
```

### 2. **Cross-Module Changes**

Make atomic changes across modules:
```bash
# Create branch in all affected modules
/granger:branch feature/new-api

# Run tests across all modules
/granger:test --affected
```

### 3. **Release Coordination**

Coordinate releases across modules:
```bash
# Tag all modules for release
/granger:release --version 1.2.0

# Generate ecosystem changelog
/granger:changelog
```

---

## 🏛️ Architectural Patterns

### 1. **Hub-and-Spoke Pattern**

```
         ┌─────────────┐
         │ Granger Hub │ ← Service Registry
         └──────┬──────┘ ← Request Router
                │        ← Load Balancer
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐
│SPARTA │  │Marker │  │ArXiv  │
└───────┘  └───────┘  └───────┘
```

### 2. **Pipeline Pattern**

```
Input → SPARTA → Marker → ArangoDB → Unsloth → Output
         ↓        ↓         ↓          ↓
      [Hub Orchestration & Monitoring]
```

### 3. **Event-Driven Pattern**

```python
# Modules emit events
@mcp.on_complete
async def emit_completion(result):
    await hub.emit_event("processing.complete", {
        "module": "marker",
        "result": result
    })

# Other modules subscribe
@hub.on_event("processing.complete")
async def handle_completion(event):
    if event["module"] == "marker":
        await start_next_stage(event["result"])
```

---

## ✅ Monorepo Best Practices Checklist

### Development Workflow
- [ ] All modules cloned locally for development
- [ ] Virtual environments per module
- [ ] Editable installs for cross-module work
- [ ] Shared dependency versions respected

### Testing
- [ ] Unit tests run in isolation
- [ ] Integration tests use real services
- [ ] Ecosystem tests verify workflows
- [ ] No mocking of internal services

### Deployment
- [ ] Services deployed in dependency order
- [ ] Configuration centrally managed
- [ ] Service discovery via Hub
- [ ] Health checks on all services

### Maintenance
- [ ] Regular dependency updates
- [ ] Coordinated releases
- [ ] Atomic cross-module changes
- [ ] Comprehensive changelogs

---

## 📚 References

- [Granger Module Standards](./GRANGER_MODULE_STANDARDS.md)
- [Python Monorepo Best Practices](https://www.tweag.io/blog/2023-04-04-python-monorepo-1/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)