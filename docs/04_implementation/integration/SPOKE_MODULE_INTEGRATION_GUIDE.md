# Spoke Module Integration Guide for Claude Module Communicator

This guide provides a comprehensive framework for integrating any spoke module with the Claude Module Communicator hub, based on lessons learned from the DARPA Crawl integration.

## Overview

The Claude Module Communicator uses a hub-and-spoke architecture where:
- **Hub**: The central `claude-module-communicator` orchestrates all modules
- **Spokes**: Individual modules (DARPA Crawl, SPARTA, Marker, etc.) that provide specific capabilities

## Table of Contents

1. [Module Interface Requirements](#module-interface-requirements)
2. [Database Integration Pattern](#database-integration-pattern)
3. [Error Handling Best Practices](#error-handling-best-practices)
4. [Testing Strategy](#testing-strategy)
5. [Module-Specific Integration Notes](#module-specific-integration-notes)
6. [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)

## Module Interface Requirements

### 1. Base Module Class

Every spoke module should implement these core components:

```python
# src/your_module/core/your_module.py
from claude_coms.base_module import BaseModule
from typing import Dict, Any, List, Optional
from loguru import logger

class YourModule(BaseModule):
    """Your module for claude-module-communicator"""
    
    def __init__(self, registry=None):
        super().__init__(
            name="your_module_name",  # Unique identifier
            system_prompt="Brief description of module purpose",
            capabilities=[
                "capability_1",
                "capability_2",
                # List all actions this module can perform
            ],
            registry=registry
        )
        
        # IMPORTANT: Add these attributes for compatibility
        self.version = "1.0.0"
        self.description = "Detailed module description"
        
        # Initialize your module components
        self._initialized = False
        
    async def start(self) -> None:
        """Initialize the module"""
        if not self._initialized:
            # Initialize databases, connections, etc.
            await self._initialize_components()
            self._initialized = True
            logger.info(f"{self.name} module started")
            
    async def stop(self) -> None:
        """Cleanup resources"""
        # Close connections, save state, etc.
        await self._cleanup_components()
        logger.info(f"{self.name} module stopped")
        
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process requests from the communicator"""
        try:
            action = request.get("action")
            
            if action not in self.capabilities:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}",
                    "available_actions": self.capabilities
                }
            
            # Route to appropriate handler
            result = await self._route_action(action, request)
            
            return {
                "success": True,
                "module": self.name,
                **result
            }
            
        except Exception as e:
            logger.error(f"Module error in {self.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "module": self.name
            }
```

### 2. Action Routing Pattern

```python
async def _route_action(self, action: str, request: Dict[str, Any]) -> Dict[str, Any]:
    """Route actions to appropriate handlers"""
    
    # Map actions to handler methods
    action_handlers = {
        "capability_1": self._handle_capability_1,
        "capability_2": self._handle_capability_2,
        # Add all your capabilities
    }
    
    handler = action_handlers.get(action)
    if not handler:
        raise ValueError(f"No handler for action: {action}")
        
    return await handler(request)
```

### 3. Standard Response Format

Always return responses in this format:

```python
# Success response
{
    "success": True,
    "module": "your_module_name",
    "data": {
        # Your response data
    },
    "metadata": {
        "timestamp": datetime.utcnow().isoformat(),
        "version": self.version,
        "processing_time": 0.123  # seconds
    }
}

# Error response
{
    "success": False,
    "module": "your_module_name",
    "error": "Detailed error message",
    "error_type": "ValueError",  # Exception class name
    "traceback": "..."  # Optional, for debugging
}
```

## Database Integration Pattern

### 1. ArangoDB Integration

Most Granger modules should integrate with ArangoDB. Here's the pattern:

```python
# src/your_module/core/database/database_factory.py
import os
from loguru import logger

def get_database():
    """Factory function to get appropriate database backend"""
    
    # Check if ArangoDB is available and configured
    use_arango = os.getenv("DATABASE_BACKEND", "").lower() == "arangodb"
    
    if use_arango:
        try:
            from .database_arango import ArangoDatabase
            
            # Test connection
            db = ArangoDatabase(
                host=os.getenv("ARANGO_HOST", "http://localhost:8529"),
                username=os.getenv("ARANGO_USER", "root"),
                password=os.getenv("ARANGO_PASSWORD", "openSesame"),
                db_name=os.getenv("ARANGO_DB_NAME", "granger")
            )
            
            logger.info(f"Using ArangoDB for {__name__}")
            return db
            
        except Exception as e:
            logger.warning(f"ArangoDB unavailable: {e}")
    
    # Fallback to your module's default database
    from .database_default import DefaultDatabase
    logger.info(f"Using default database for {__name__}")
    return DefaultDatabase()
```

### 2. Database Adapter Pattern

Create an adapter to provide a consistent interface:

```python
# src/your_module/core/database/database_adapter.py
class DatabaseAdapter:
    """Unified interface for different database backends"""
    
    def __init__(self):
        self.db = get_database()
        
    async def initialize(self) -> None:
        """Initialize database connection"""
        if hasattr(self.db, 'initialize'):
            await self.db.initialize()
        elif hasattr(self.db, 'connect'):
            await self.db.connect()
            
    async def store_item(self, item: Dict[str, Any]) -> bool:
        """Store an item (adapter method)"""
        # Map to backend-specific method
        if hasattr(self.db, 'add_item'):
            result = await self.db.add_item(item)
        elif hasattr(self.db, 'insert'):
            result = await self.db.insert(item)
        else:
            raise NotImplementedError("Database missing store method")
            
        # Normalize response
        return self._normalize_result(result)
```

### 3. Collection Naming Convention

Use module-specific prefixes to avoid conflicts:

```python
# For ArangoDB collections
collections = {
    'items': f'{module_name}_items',
    'metadata': f'{module_name}_metadata',
    'relationships': f'{module_name}_relationships'
}

# Example for different modules:
# sparta_missions, sparta_datasets
# marker_documents, marker_extractions
# arxiv_papers, arxiv_authors
```

## Error Handling Best Practices

### 1. Graceful Degradation

```python
async def get_enhanced_data(self, query: str) -> Dict[str, Any]:
    """Example of graceful degradation"""
    
    try:
        # Try advanced method first
        return await self._get_semantic_search_results(query)
    except Exception as e:
        logger.warning(f"Semantic search failed, falling back: {e}")
        
        try:
            # Fall back to simpler method
            return await self._get_fulltext_search_results(query)
        except Exception as e2:
            logger.error(f"Fulltext search also failed: {e2}")
            
            # Final fallback
            return {
                "results": [],
                "error": "Search temporarily unavailable",
                "fallback": True
            }
```

### 2. Context Managers for Resources

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_client(self):
    """Safely manage client connections"""
    client = None
    try:
        client = await self._create_client()
        yield client
    finally:
        if client:
            await client.close()
            
# Usage
async def fetch_data(self):
    async with self.get_client() as client:
        return await client.fetch(...)
```

### 3. Comprehensive Logging

```python
from loguru import logger

# Configure module-specific logging
logger.add(
    f"logs/{module_name}_{{time}}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time} | {level} | {module}:{function}:{line} - {message}"
)

# Use structured logging
logger.info("Processing request", 
    module=self.name,
    action=action,
    request_id=request.get("id"),
    user=request.get("user")
)
```

## Testing Strategy

### 1. Integration Test Template

```python
# tests/test_integration.py
import pytest
from your_module.core.your_module import YourModule

@pytest.mark.asyncio
async def test_module_lifecycle():
    """Test module can start and stop"""
    module = YourModule()
    
    # Test initialization
    await module.start()
    assert module._initialized
    
    # Test processing
    result = await module.process({
        "action": "test_action",
        "data": "test"
    })
    assert result["success"]
    
    # Test cleanup
    await module.stop()

@pytest.mark.asyncio
async def test_communicator_integration():
    """Test module works with communicator patterns"""
    module = YourModule()
    await module.start()
    
    # Test all required attributes exist
    assert hasattr(module, 'name')
    assert hasattr(module, 'version')
    assert hasattr(module, 'capabilities')
    assert hasattr(module, 'description')
    
    # Test response format
    result = await module.process({"action": "get_status"})
    assert "success" in result
    assert "module" in result
```

### 2. Database Integration Tests

```python
@pytest.mark.asyncio
async def test_database_selection():
    """Test correct database backend is selected"""
    from your_module.core.database.database_factory import get_database
    
    db = get_database()
    
    # If ArangoDB is available, it should be selected
    if os.getenv("ARANGO_HOST"):
        assert "Arango" in type(db).__name__
    else:
        assert "Default" in type(db).__name__
```

### 3. Mock External Services

```python
# tests/conftest.py
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
async def mock_external_api():
    """Mock external API calls"""
    mock = AsyncMock()
    mock.fetch.return_value = {"status": "success", "data": []}
    return mock
    
# Use in tests
async def test_with_mock(mock_external_api, monkeypatch):
    monkeypatch.setattr("your_module.api_client", mock_external_api)
    # Test your module
```

## Module-Specific Integration Notes

### 1. SPARTA Module
```python
class SPARTAModule(BaseModule):
    capabilities = [
        "search_datasets",
        "download_dataset", 
        "analyze_space_data",
        "extract_cybersecurity_metrics"
    ]
    
    # Special considerations:
    # - Handle large dataset downloads asynchronously
    # - Implement progress callbacks for long operations
    # - Cache dataset metadata in ArangoDB
```

### 2. Marker Module
```python
class MarkerModule(BaseModule):
    capabilities = [
        "convert_pdf_to_markdown",
        "extract_tables",
        "validate_extraction",
        "get_ground_truth"
    ]
    
    # Special considerations:
    # - Stream large file processing
    # - Store extractions in ArangoDB with source references
    # - Implement quality scores for extractions
```

### 3. ArXiv MCP Server
```python
class ArXivModule(BaseModule):
    capabilities = [
        "search_papers",
        "get_paper_details",
        "download_paper",
        "extract_citations"
    ]
    
    # Special considerations:
    # - Respect ArXiv rate limits
    # - Cache paper metadata
    # - Link papers to other modules (DARPA opportunities, etc.)
```

### 4. YouTube Transcripts
```python
class YouTubeTranscriptsModule(BaseModule):
    capabilities = [
        "get_transcript",
        "search_transcripts",
        "extract_technical_content",
        "summarize_video"
    ]
    
    # Special considerations:
    # - Handle missing transcripts gracefully
    # - Store transcripts with timestamps
    # - Link to related papers/opportunities
```

### 5. Claude Max Proxy
```python
class ClaudeMaxProxyModule(BaseModule):
    capabilities = [
        "unified_llm_call",
        "model_selection",
        "token_optimization",
        "response_caching"
    ]
    
    # Special considerations:
    # - Implement timeout handling
    # - Track token usage per module
    # - Cache responses in ArangoDB
```

### 6. RL Commons
```python
class RLCommonsModule(BaseModule):
    capabilities = [
        "train_agent",
        "evaluate_policy",
        "score_opportunity",
        "optimize_selection"
    ]
    
    # Special considerations:
    # - Handle long-running training jobs
    # - Store model checkpoints
    # - Provide progress updates
```

## Common Pitfalls and Solutions

### 1. Missing Required Attributes

**Problem**: `AttributeError: 'Module' object has no attribute 'version'`

**Solution**:
```python
def __init__(self, registry=None):
    super().__init__(...)
    # Add these required attributes
    self.version = "1.0.0"
    self.description = "Your module description"
```

### 2. Import Errors in Database Code

**Problem**: `ImportError: No module named 'SomeClass'`

**Solution**:
```python
# Ensure all required classes are defined
# In models.py:
class YourModelCreate(BaseModel):
    """Pydantic model for creation"""
    pass

class YourModelInDB(YourModelCreate):
    """Pydantic model for database storage"""
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 3. Database Method Mismatches

**Problem**: Database adapter expects methods that don't exist

**Solution**:
```python
# Implement all required methods in your database class
class YourDatabase:
    async def get_item_count(self) -> int:
        """Required by adapter"""
        pass
        
    async def get_item_by_id(self, item_id: str) -> Optional[Dict]:
        """Required by adapter"""
        pass
```

### 4. Unique Constraint Violations

**Problem**: ArangoDB unique constraint errors

**Solution**:
```python
# Add field mappings for compatibility
doc = item.dict()
doc['_key'] = hashlib.md5(item.unique_id.encode()).hexdigest()
doc['source_id'] = item.unique_id  # For index compatibility
doc['created_at'] = datetime.utcnow().isoformat()

# Use upsert instead of insert
collection.insert(doc, overwrite=True)  # or update existing
```

### 5. Async Context Issues

**Problem**: `RuntimeError: Event loop is closed`

**Solution**:
```python
# Properly manage async resources
class YourModule(BaseModule):
    async def __aenter__(self):
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        
# Usage
async with YourModule() as module:
    result = await module.process(request)
```

## Environment Configuration

### Standard .env Template

```bash
# REQUIRED - First line must be:
PYTHONPATH=./src

# Module-specific configuration
MODULE_NAME=your_module
MODULE_VERSION=1.0.0
LOG_LEVEL=INFO

# API Keys (if needed)
YOUR_API_KEY=your_key_here

# ArangoDB Configuration (shared across Granger)
ARANGO_HOST="http://localhost:8529"
ARANGO_USER="root"
ARANGO_PASSWORD="openSesame"
ARANGO_DB_NAME="granger"

# Optional: Force database backend
DATABASE_BACKEND=arangodb  # or sqlite, postgres, etc.
```

## Deployment Checklist

Before deploying your spoke module:

- [ ] ✅ Implements all required BaseModule methods
- [ ] ✅ Has `version` and `description` attributes
- [ ] ✅ All actions in `capabilities` are implemented
- [ ] ✅ Returns standardized response format
- [ ] ✅ Handles errors gracefully
- [ ] ✅ Integrates with ArangoDB (if applicable)
- [ ] ✅ Has comprehensive logging
- [ ] ✅ Includes integration tests
- [ ] ✅ Documents all available actions
- [ ] ✅ Follows collection naming conventions

## Example Integration Script

```python
#!/usr/bin/env python3
# scripts/test_integration.py

import asyncio
from claude_module_communicator import ModuleCommunicator
from your_module.core.your_module import YourModule

async def test_integration():
    """Test your module with the communicator"""
    
    # Initialize communicator
    communicator = ModuleCommunicator()
    
    # Register your module
    module = YourModule()
    communicator.register_module("your_module", module)
    
    # Test sending a request
    response = await communicator.send_to_module("your_module", {
        "action": "test_action",
        "data": "test"
    })
    
    print(f"Response: {response}")
    
    # Test inter-module communication
    if "darpa_crawl" in communicator.modules:
        opportunity_response = await communicator.send_to_module("darpa_crawl", {
            "action": "search_opportunities",
            "keywords": ["related to your module"]
        })
        print(f"Found opportunities: {len(opportunity_response.get('opportunities', []))}")

if __name__ == "__main__":
    asyncio.run(test_integration())
```

## Support and Troubleshooting

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
export LOG_LEVEL=DEBUG
python -m your_module
```

### Common Debug Commands

```python
# Check module registration
print(communicator.list_modules())

# Verify module capabilities
module = communicator.get_module("your_module")
print(module.capabilities)

# Test module directly
result = await module.process({"action": "get_status"})
print(result)
```

### Getting Help

1. Check the Claude Module Communicator documentation
2. Review this guide and the DARPA Crawl implementation
3. Enable debug logging and check for specific errors
4. Ensure all dependencies are installed with `uv`
5. Verify ArangoDB connection if using it

## Conclusion

By following this guide, you can successfully integrate any spoke module with the Claude Module Communicator hub. The key principles are:

1. **Consistent Interface**: Implement the required methods and attributes
2. **Robust Error Handling**: Gracefully handle failures with fallbacks
3. **Database Integration**: Use ArangoDB when available, with fallbacks
4. **Comprehensive Testing**: Test both standalone and integrated scenarios
5. **Clear Documentation**: Document all actions and expected inputs/outputs

Remember that the hub-and-spoke architecture allows modules to work independently while benefiting from orchestration and inter-module communication through the central hub.