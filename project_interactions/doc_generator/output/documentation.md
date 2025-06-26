# Project Documentation
Generated: 2025-06-01 20:11:03

## Table of Contents

- [example_module](#example-module)

## Modules

### example_module

**Path:** `example_module.py`

**Description:**

Example module for testing documentation generator

This module demonstrates various Python constructs that the documentation
generator can extract and document.

#### Constants

- `DEFAULT_TIMEOUT` = `30`
- `MAX_RETRIES` = `3`

#### Functions

##### `__init__(self: Any, config: Dict[str, any])`

Initialize processor with configuration

Args:
    config: Configuration dictionary

- **Line:** 21
- **Complexity:** 1

##### `process(self: Any, data: List[str]) -> List[str]`

Process a list of data items

Args:
    data: List of strings to process
    
Returns:
    Processed data list

- **Line:** 30
- **Complexity:** 2

##### `_transform(self: Any, item: str) -> str`

Internal transformation method

- **Line:** 45
- **Complexity:** 1

##### async `process_async(self: Any, data: List[str]) -> List[str]`

Async version of process method

- **Line:** 49
- **Complexity:** 1

##### `validate_input(data: any) -> bool`

Validate input data

Args:
    data: Data to validate
    
Returns:
    True if valid, False otherwise

- **Line:** 55
- **Complexity:** 4

##### async `fetch_data(url: str, timeout: int) -> Optional[Dict]`

Fetch data from URL

Args:
    url: URL to fetch from
    timeout: Request timeout in seconds
    
Returns:
    JSON data or None if failed

- **Line:** 71
- **Complexity:** 1

##### `__init__(self: Any)`

- **Line:** 90
- **Complexity:** 1

##### `load(self: Any, path: str) -> None`

Load configuration from file

- **Line:** 93
- **Complexity:** 1

##### `get(self: Any, key: str, default: any) -> any`

Get configuration value

- **Line:** 98
- **Complexity:** 1

#### Classes

##### `class DataProcessor`

Processes data with various transformations

**Methods:**

##### `__init__(self: Any, config: Dict[str, any])`

Initialize processor with configuration

Args:
    config: Configuration dictionary

- **Line:** 21
- **Complexity:** 1

##### `process(self: Any, data: List[str]) -> List[str]`

Process a list of data items

Args:
    data: List of strings to process
    
Returns:
    Processed data list

- **Line:** 30
- **Complexity:** 2

##### `_transform(self: Any, item: str) -> str`

Internal transformation method

- **Line:** 45
- **Complexity:** 1

##### `class ConfigManager`

Manages application configuration

**Attributes:**

- `config_version: str`

**Methods:**

##### `__init__(self: Any)`

- **Line:** 90
- **Complexity:** 1

##### `load(self: Any, path: str) -> None`

Load configuration from file

- **Line:** 93
- **Complexity:** 1

##### `get(self: Any, key: str, default: any) -> any`

Get configuration value

- **Line:** 98
- **Complexity:** 1

---


## Module Dependencies

```
Module Dependency Graph
==================================================

example_module:
  └─> datetime
  └─> json
  └─> typing

```