# Shared Claude Docs - Test Suite

## Overview

This directory contains all tests for the shared_claude_docs project. Tests are organized to mirror the src/ directory structure for easy navigation.

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared pytest fixtures
├── test_basic.py        # Basic smoke tests
├── README.md           # This file
├── unit/               # Fast, isolated unit tests
│   └── (mirrors src/ structure)
└── integration/        # Integration tests requiring services
    └── granger_interaction_tests/  # Granger ecosystem tests
```

## Running Tests

### Run All Tests
```bash
# From project root
pytest

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Basic smoke tests
pytest tests/test_basic.py
```

### Run Tests by Marker
```bash
# Fast tests only
pytest -m "not slow"

# Specific module tests
pytest -k "test_cli"
```

## Test Categories

1. **Unit Tests** (`tests/unit/`)
   - No external dependencies
   - No file I/O or network calls
   - Fast execution (< 1 second each)
   - Test individual functions/classes

2. **Integration Tests** (`tests/integration/`)
   - May require external services
   - Test module interactions
   - Can use real file I/O
   - May be slower

3. **Smoke Tests** (`tests/test_basic.py`)
   - Basic sanity checks
   - Verify installation works
   - Import tests

## Writing Tests

### Test File Naming
- Test files: `test_*.py`
- Test classes: `TestClassName`
- Test functions: `test_should_do_something_when_condition()`

### Example Test Structure
```python
import pytest
from shared_claude_docs.module import function_to_test

class TestModuleName:
    def test_function_returns_expected_value(self):
        # Arrange
        input_data = {"key": "value"}
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == {"processed": True}
    
    def test_function_raises_on_invalid_input(self):
        with pytest.raises(ValueError):
            function_to_test(None)
```

## Fixtures

Common fixtures are defined in `conftest.py`:
- `tmp_workspace`: Temporary directory for file operations
- `mock_config`: Test configuration

## Coverage Requirements

- Minimum coverage: 80%
- New code must include tests
- Critical paths require 100% coverage

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Push to main branch
- Daily scheduled runs

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure PYTHONPATH is set
   export PYTHONPATH=./src
   ```

2. **Missing Dependencies**
   ```bash
   # Install test dependencies
   uv sync --dev
   ```

3. **Slow Tests**
   ```bash
   # Skip slow tests
   pytest -m "not slow"
   ```

## Contributing

1. Write tests for new features
2. Ensure all tests pass locally
3. Update this README if adding new test categories
4. Follow the project's coding standards
