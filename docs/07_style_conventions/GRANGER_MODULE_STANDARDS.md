# Granger Module Standards and Requirements

> **Canonical reference for all Granger ecosystem module development**  
> **Version**: 1.0.0  
> **Date**: 2025-01-09  
> **Status**: MANDATORY for all modules

---

## 🚨 CRITICAL REQUIREMENTS

Every module in the Granger ecosystem MUST follow these standards. No exceptions.

### 1. Package Management
- **USE UV EXCLUSIVELY** - Never use pip directly
- **Python Version**: 3.10.11 (unless explicitly overridden)
- **Virtual Environment**: Always use `.venv/` in project root

### 2. Dependency Constraints
These versions are LOCKED across the ecosystem:
```toml
# In pyproject.toml
[project]
requires-python = ">=3.10.11"
dependencies = [
    "numpy==1.26.4",          # LOCKED - Do not change
    "pandas>=2.2.3,<2.3.0",   # Compatible with numpy 1.26.4
    "pyarrow>=4.0.0,<20",     # Required for mlflow compatibility
    "pillow>=10.1.0,<11.0.0", # Security constraints
    # ... other dependencies
]
```

### 3. Git Dependencies
All GitHub dependencies MUST use this format:
```toml
"package_name @ git+https://github.com/grahama1970/repo_name.git"
```
- ✅ CORRECT: `git+https://github.com/grahama1970/project.git`
- ❌ WRONG: `file:///home/graham/workspace/...`
- ❌ WRONG: `https://github.com/grahama1970/project`

---

## 📁 Project Structure (3-Layer Architecture)

```
project_name/
├── .env.example              # MUST start with PYTHONPATH=./src
├── .gitignore               
├── pyproject.toml           # UV package management
├── uv.lock                  # Lock file (committed)
├── README.md               
├── src/
│   └── project_name/
│       ├── __init__.py      # Exports and version
│       ├── core/            # Business logic (no UI/framework deps)
│       │   ├── __init__.py
│       │   └── functions.py # Pure functions
│       ├── cli/             # Typer-based CLI
│       │   ├── __init__.py
│       │   ├── app.py       # Typer application
│       │   ├── formatters.py # Rich formatting
│       │   ├── validators.py # Input validation
│       │   └── schemas.py    # Pydantic models
│       └── mcp/             # MCP integration
│           ├── __init__.py
│           ├── schema.py     # JSON schemas
│           └── server.py     # FastMCP server
├── tests/                   # Mirror src/ structure
│   ├── __init__.py
│   ├── conftest.py         
│   ├── unit/               # Fast, no I/O
│   ├── integration/        # Component tests
│   └── e2e/                # Full workflows
├── docs/
│   ├── CHANGELOG.md        
│   └── reports/            # Test reports
└── examples/               # Mirror src/ structure
```

---

## 🔧 Module Configuration

### pyproject.toml Template
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "project-name"  # Match distribution name
version = "0.1.0"
description = "Brief description"
readme = "README.md"
requires-python = ">=3.10.11"
license = {text = "MIT"}
authors = [{name = "Graham Anderson", email = "graham@grahama.co"}]

dependencies = [
    # Core dependencies with locked versions
    "numpy==1.26.4",
    "loguru>=0.7.0",
    "pydantic>=2.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
    "fastmcp>=0.1.0",
    # Project-specific dependencies
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-json-report>=1.5.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]

[project.scripts]
project-cli = "project_name.cli.app:app"
project-mcp = "project_name.mcp.server:main"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

[tool.hatch.metadata]
allow-direct-references = true  # Required for git+https:// deps
```

### .env.example Template
```bash
# FIRST LINE MUST BE:
PYTHONPATH=./src

# Project configuration
MODULE_NAME=project_name
MODULE_VERSION=0.1.0

# Granger ecosystem connections
GRANGER_HUB_URL=http://localhost:8000
ARANGODB_URL=http://localhost:8529
ARANGODB_USER=root
ARANGODB_PASSWORD=openSesame
LLM_CALL_URL=http://localhost:8001
TEST_REPORTER_URL=http://localhost:8002

# API keys (optional)
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
```

---

## 📝 Code Standards

### Module Documentation Header
Every Python file MUST include:
```python
"""
Module: module_name.py
Description: Brief description of what this script file does

External Dependencies:
- requests: https://docs.python-requests.org/
- pydantic: https://docs.pydantic.dev/

Sample Input:
>>> input_data = {"query": "test", "limit": 10}

Expected Output:
>>> result = search_function(input_data)
>>> print(result)
{"results": [...], "total": 10, "status": "success"}

Example Usage:
>>> from module_name import search_function
>>> result = search_function({"query": "test"})
"""
```

### Import Standards
```python
# Standard library imports first
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Third-party imports
import numpy as np  # Always 1.26.4
from loguru import logger
from pydantic import BaseModel

# Local imports (absolute only)
from project_name.core.functions import process_data
from project_name.cli.formatters import format_output

# NEVER use relative imports
# ❌ from ..core import functions
# ✅ from project_name.core import functions
```

### Validation Function
Every module MUST include real-world validation:
```python
if __name__ == "__main__":
    import sys
    
    # Track all validation failures
    all_validation_failures = []
    total_tests = 0
    
    # Test 1: Basic functionality with REAL data
    total_tests += 1
    try:
        # Use actual API/service - NO MOCKS
        result = search_arxiv("quantum computing")
        if not result or len(result) == 0:
            all_validation_failures.append("No results returned from ArXiv")
    except Exception as e:
        all_validation_failures.append(f"ArXiv search failed: {str(e)}")
    
    # Final validation result
    if all_validation_failures:
        print(f"❌ VALIDATION FAILED - {len(all_validation_failures)} of {total_tests} tests failed:")
        for failure in all_validation_failures:
            print(f"  - {failure}")
        sys.exit(1)
    else:
        print(f"✅ VALIDATION PASSED - All {total_tests} tests passed")
        sys.exit(0)
```

---

## 🧪 Testing Requirements

### NO MOCKS Policy
```python
# ❌ FORBIDDEN - Never do this
from unittest.mock import Mock, patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"fake": "data"}
    
# ✅ REQUIRED - Always use real services
def test_api_call():
    # Use real API with test credentials
    response = requests.get("https://api.example.com/test")
    assert response.status_code == 200
    assert "real" in response.json()
```

### Test Structure
```python
# tests/conftest.py
import pytest
import os

@pytest.fixture(scope="session")
def test_db():
    """Provide test database connection"""
    # Use real test database, not mocks
    from python_arango import ArangoClient
    client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
    db = client.db(
        os.getenv('ARANGO_DB') + '_test',  # Test suffix
        username=os.getenv('ARANGO_USER'),
        password=os.getenv('ARANGO_PASSWORD')
    )
    yield db
    # Cleanup after tests
```

### Honeypot Tests
Include intentional failure tests to verify test framework:
```python
@pytest.mark.honeypot
def test_honeypot_always_fails():
    """This test should always fail to verify our test system works"""
    assert False, "Honeypot test - should fail"
```

---

## 🔌 Hub Integration

### Required MCP Prompts
Every module MUST implement:
```python
# src/project_name/mcp/prompts.py
from fastmcp import FastMCP

mcp = FastMCP("project-name")

@mcp.prompt()
async def capabilities() -> str:
    """List all module capabilities"""
    return """
    Project: project-name
    Capabilities:
    - Feature 1: Description
    - Feature 2: Description
    Commands:
    - /project:command1 - Does X
    - /project:command2 - Does Y
    """

@mcp.prompt()
async def help(context: str = "") -> str:
    """Context-aware help"""
    # Provide help based on context

@mcp.prompt()
async def quick_start() -> str:
    """Getting started guide"""
    return "Quick start instructions..."
```

### mcp.json Configuration
```json
{
  "name": "project-name",
  "version": "0.1.0",
  "description": "Module description",
  "main": "src/project_name/mcp/server.py",
  "prompts": {
    "capabilities": {
      "description": "List module capabilities",
      "slash_command": "/project:capabilities"
    },
    "help": {
      "description": "Get help",
      "slash_command": "/project:help",
      "parameters": {
        "context": {
          "type": "string",
          "description": "Optional context"
        }
      }
    }
  }
}
```

---

## 🚀 Slash Command Integration

### CLI Integration
```python
# src/project_name/cli/app.py
import typer
from granger_slash_mcp_mixin import add_slash_mcp_commands

app = typer.Typer(help="Project description")

# Add standard commands
add_slash_mcp_commands(app, project_name="project-name")

# Add project-specific commands
@app.command()
def process(
    input_file: Path = typer.Argument(..., help="Input file path"),
    output_dir: Path = typer.Option("./output", help="Output directory")
):
    """Process input file"""
    # Implementation
```

### Command Naming Convention
- Always prefix with project name: `/project:command`
- Use kebab-case for multi-word commands
- Be descriptive but concise

---

## 📊 Performance Standards

### Caching Strategy
```python
from diskcache import Cache
from functools import wraps

cache = Cache('./cache')

def cached_operation(expire=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result, expire=expire)
            return result
        return wrapper
    return decorator

@cached_operation(expire=3600)
def expensive_api_call(query: str):
    # Real API call here
```

### Parallel Processing
```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

# For I/O bound operations
def process_batch(items: List[str]) -> List[dict]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_item, item) for item in items]
        return [f.result() for f in futures]

# For async operations
async def process_async_batch(items: List[str]) -> List[dict]:
    tasks = [process_item_async(item) for item in items]
    return await asyncio.gather(*tasks)
```

---

## ✅ Compliance Checklist

Before committing any module:

### Setup & Environment
- [ ] Python 3.10.11 in pyproject.toml
- [ ] UV used for all package management
- [ ] .env.example starts with `PYTHONPATH=./src`
- [ ] Virtual environment in `.venv/`

### Dependencies
- [ ] numpy==1.26.4 (if used)
- [ ] pyarrow<20 (if used)
- [ ] All GitHub deps use `git+https://` format
- [ ] No local file:// paths

### Code Quality
- [ ] Documentation header in all files
- [ ] External dependency URLs documented
- [ ] Sample input/output provided
- [ ] Validation function with real data
- [ ] No relative imports
- [ ] Files under 500 lines

### Testing
- [ ] NO mock imports or usage
- [ ] Real service connections
- [ ] Honeypot tests included
- [ ] Test database uses _test suffix
- [ ] All tests use pytest

### Integration
- [ ] MCP prompts implemented
- [ ] mcp.json configured
- [ ] Slash commands prefixed correctly
- [ ] Hub discovery compatible

### Project Structure
- [ ] 3-layer architecture (core/cli/mcp)
- [ ] Correct directory structure
- [ ] Examples mirror src/
- [ ] Tests mirror src/

---

## 🚫 Common Mistakes to Avoid

1. **Using pip instead of uv**
   ```bash
   ❌ pip install package
   ✅ uv add package
   ```

2. **Wrong numpy version**
   ```toml
   ❌ "numpy>=2.0.0"
   ✅ "numpy==1.26.4"
   ```

3. **Package name mismatch**
   ```toml
   ❌ name = "granger-hub"  # But import is "granger_hub"
   ✅ name = "granger_hub"   # Match import name with underscores
   ```

4. **Missing submodules in packaging**
   ```toml
   ❌ packages = ["mcp_screenshot"]
   ✅ packages = ["mcp_screenshot", "mcp_screenshot.core", "mcp_screenshot.cli"]
   ```

5. **Creating placeholder modules**
   ```python
   ❌ # Creating empty __init__.py when real modules exist
   ✅ # Import from actual implementation files
   ```

---

## 📚 Resources

- [Global CLAUDE.md Standards](~/.claude/CLAUDE.md)
- [Monorepo Architecture Guide](./GRANGER_MONOREPO_ARCHITECTURE.md)
- [3-Layer Architecture Guide](../01_strategy/architecture/3_LAYER_ARCHITECTURE.md)
- [Hub Integration Guide](../../guides/GRANGER_HUB_INTEGRATION_GUIDE.md)
- [Slash Commands Guide](../../guides/GRANGER_SLASH_COMMANDS_GUIDE.md)
- [Test Lessons Summary](../../guides/GRANGER_TEST_LESSONS_SUMMARY.md)
- [Dependency Quick Reference](../../guides/DEPENDENCY_QUICK_REFERENCE.md)

---

## 🔄 Version History

- **1.0.0** (2025-01-09): Initial standards based on dependency resolution lessons