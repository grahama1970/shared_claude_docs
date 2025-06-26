# LLM Call

## Overview
A flexible command-line tool and library that lets you interact with any LLM through a unified interface. Whether you prefer typing commands, using it within Claude Desktop/Code as an MCP tool, or integrating it into your Python scripts - llm_call handles it all with built-in response validation.

## Core Capabilities
- **project_cleanup.py**: Contains 3 classes and 11 functions
- **check_project_setup.py**: Contains 0 classes and 7 functions
- **conftest.py**: Contains 2 classes and 11 functions
- **run_tests_with_report.py**: Contains 0 classes and 2 functions
- **llm_gemini.py**: Contains 7 classes and 18 functions
- **embeddings_migrations.py**: Contains 0 classes and 7 functions
- **hookspecs.py**: Contains 0 classes and 6 functions
- Web API/Server capabilities

## Technical Architecture
### Directory Structure
- `scripts/`: 3 Python files
- `src/`: 1 Python files
- `tests/`: 3 Python files

### Source Organization
- Follows standard src/ layout
- Test suite included
- Documentation directory present

## Installation & Setup
```bash
pip install -e .
```

See README.md for detailed installation instructions

### Docker Installation
```bash
# Quick start with Docker Compose
cd llm_call
docker compose up -d

# For Claude Max users: Authenticate Claude CLI
./docker/claude-proxy/authenticate.sh

# Test authentication
./docker/claude-proxy/test_claude.sh
```

See [Docker Authentication Guide](../../04_implementation/tutorials/LLM_CALL_DOCKER_AUTHENTICATION.md) for detailed setup.

## Usage Examples

### From README
See README.md for usage examples

## API/Interface Documentation
### API Endpoints
- `repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/generic_api_callback.py`
- `repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/example_logging_api.py`
- `repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/secrets_plugins/twitch_api_token.py`
- `repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/secrets_plugins/databricks_api_token.py`
- `repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/secrets_plugins/doppler_api_token.py`
- GraphQL API detected

## Integration Points
### Direct Integrations
- All Claude-interfacing modules
- API management
- References claude in project_cleanup.py
- References claude in test_imports.py
- References claude in __init__.py
- References marker in run_tests_with_report.py

## Dependencies

### Additional Requirements
- See README.md for system dependencies

## Current Limitations
### Known TODOs (1 found)
- Should  be _or_raise()

## Potential Improvements
### Missing Standard Files
- Add requirements.txt for dependency management
- Add setup.py for package installation
- Add .env.example for environment configuration example

### General Improvements
- Add comprehensive logging
- Implement error recovery mechanisms
- Add performance benchmarks

## Error Analysis
### Potential Issues Found

**Using print instead of logging**
- Found in project_cleanup.py
- Found in check_project_setup.py
- Found in test_imports.py
- ... and 3 more files

**Bare except clause (catches all exceptions)**
- Found in check_project_setup.py

**Unresolved technical debt**
- Found in models.py

## Missing Features
### Domain-Specific Features
- Request queuing and prioritization
- Cost optimization strategies
- Multi-model load balancing
- Usage analytics dashboard

### Common Features
- GitHub Actions CI/CD

### Research Needed
- Use `ask-perplexity` to research:
  - Latest best practices for llm_call
  - Competing solutions to llm_call
  - Performance optimization techniques for llm_call

## Related Projects
### Direct Dependencies
- granger_hub

### Ecosystem Role
- Claude API management and optimization

## Notes
### Project Metadata
- Version history available (CHANGELOG.md)

### Activity
- Last commit: 2025-05-25

### Development Status
- Packaged for distribution

---
*Generated: 2025-05-29 12:55:27*
