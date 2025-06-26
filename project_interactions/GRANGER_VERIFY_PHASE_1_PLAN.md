# Granger Verify - Phase 1: Remove Mocks and Fix Imports

## Overview
Before any cleaning can be done, we must ensure all Granger projects have:
1. **NO MOCKS** - All tests use real APIs/services
2. **Absolute imports** - No relative imports that break in different contexts
3. **Working dependencies** - All pyproject.toml imports actually work

## Phase 1 Tasks

### 1. Remove All Mocks and Simulations
For each project in `/home/graham/workspace/shared_claude_docs/docs/GRANGER_PROJECTS.md`:

```python
# Find all mock usage
for project in GRANGER_PROJECTS:
    scan_directory(f"{project}/tests/")
    scan_directory(f"{project}/src/")
    
    # Look for:
    - Mock, MagicMock, patch, mock imports
    - @patch decorators
    - unittest.mock usage
    - Fake/stub classes
    - Simulated API responses
    - Hardcoded test data instead of real calls
```

Replace with real calls:
```python
# BEFORE (Bad)
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {"data": "fake"}
    result = my_function()
    assert result == "fake"

# AFTER (Good)
def test_api_call():
    # Real API call
    result = my_function()  # Actually calls the API
    assert result is not None  # Verify real response
```

### 2. Convert Relative to Absolute Imports
```python
# BEFORE (Bad)
from ..utils import helper
from .config import settings
from ...core.module import BaseClass

# AFTER (Good)
from myproject.utils import helper
from myproject.config import settings
from myproject.core.module import BaseClass
```

### 3. Verify All pyproject.toml Dependencies

Check each project can actually import its dependencies:
```python
# For each project
def verify_imports(project_path):
    pyproject = load_pyproject_toml(project_path)
    
    for dep in pyproject['dependencies']:
        if dep.startswith('git+'):
            # Verify GitHub project is accessible
            verify_github_import(dep)
        else:
            # Verify PyPI package
            verify_pypi_import(dep)
```

## Implementation Script Structure

```python
#!/usr/bin/env python3
"""
granger_verify_phase1.py - Remove mocks and fix imports across all Granger projects
"""

import os
import sys
import ast
import toml
from pathlib import Path
from typing import List, Dict, Tuple

class GrangerVerifier:
    def __init__(self):
        self.projects = self.load_project_registry()
        self.issues = {
            'mocks': [],
            'relative_imports': [],
            'missing_deps': []
        }
    
    def load_project_registry(self) -> Dict[str, str]:
        """Load all projects from GRANGER_PROJECTS.md"""
        # Parse the markdown file
        # Return dict of project_name: project_path
        pass
    
    def scan_for_mocks(self, project_path: str) -> List[Dict]:
        """Find all mock usage in a project"""
        mock_patterns = [
            'from unittest.mock import',
            'from unittest import mock',
            'from mock import',
            '@patch',
            '@mock',
            'MagicMock',
            'Mock(',
            'create_autospec',
            'patch.object'
        ]
        # Scan all Python files
        pass
    
    def fix_relative_imports(self, project_path: str) -> List[Tuple[str, str]]:
        """Convert relative imports to absolute"""
        # Parse AST and find relative imports
        # Generate absolute import statements
        pass
    
    def verify_dependencies(self, project_path: str) -> List[str]:
        """Check all dependencies can be imported"""
        # Load pyproject.toml
        # Try importing each dependency
        # Return list of failures
        pass
    
    def generate_report(self) -> str:
        """Generate comprehensive report of all issues"""
        pass
    
    def auto_fix_issues(self):
        """Automatically fix issues where possible"""
        pass
```

## Verification Checklist

For each project, verify:

- [ ] **No Mock Imports**: Zero imports of mock/patch/MagicMock
- [ ] **No Fake Data**: All tests use real services/databases
- [ ] **No Simulated Responses**: No hardcoded API responses
- [ ] **Absolute Imports Only**: No relative imports (no dots)
- [ ] **All Dependencies Work**: Can import every dependency
- [ ] **GitHub Projects Accessible**: All git+ dependencies clone successfully
- [ ] **Tests Still Pass**: After fixes, tests work with real services

## Expected Issues and Solutions

### 1. Tests Fail Without Mocks
**Issue**: Tests expect specific responses
**Solution**: Make tests more flexible
```python
# Instead of expecting exact data
assert response == {"id": 123, "name": "test"}

# Accept any valid response
assert "id" in response
assert isinstance(response["id"], int)
```

### 2. External Services Unavailable
**Issue**: API/database not running
**Solution**: Document prerequisites
```python
# Add to test file
"""
Prerequisites:
- ArangoDB running on localhost:8529
- Redis running on localhost:6379
- LLM_CALL service on localhost:8001
"""
```

### 3. Circular Import Issues
**Issue**: Absolute imports cause circular dependencies
**Solution**: Refactor module structure or use lazy imports

## Success Criteria

Phase 1 is complete when:
1. Zero mock usage across all test files
2. All imports are absolute (module.submodule.item)
3. Every dependency can be successfully imported
4. All tests pass using real services
5. No simulation of module functionality

## Next Steps

After Phase 1 completion:
- Phase 2: Run comprehensive integration tests
- Phase 3: Fix any remaining bugs found
- Phase 4: Performance optimization
- Phase 5: Documentation updates

This ensures a solid foundation before any cleanup or refactoring work begins.