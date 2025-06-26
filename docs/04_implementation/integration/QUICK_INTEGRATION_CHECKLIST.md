# Quick Integration Checklist for Claude Module Communicator

A rapid reference for integrating spoke modules with the hub. Copy this checklist for each new module integration.

## Pre-Integration Setup

```bash
# 1. Navigate to your module
cd /home/graham/workspace/experiments/your_module/

# 2. Ensure Python 3.10.11 environment
uv venv .venv --python 3.10.11
source .venv/bin/activate

# 3. Install base dependencies
uv add loguru pydantic aiohttp python-arango

# 4. Create required structure
mkdir -p src/your_module/core/database
mkdir -p tests/integration
mkdir -p docs/usage
```

## Module Class Template

Copy and modify this template:

```python
# src/your_module/core/your_module.py
from claude_coms.base_module import BaseModule
from typing import Dict, Any, List, Optional
from loguru import logger
import asyncio

class YourModule(BaseModule):
    """Your module for claude-module-communicator"""
    
    def __init__(self, registry=None):
        super().__init__(
            name="your_module",  # CHANGE THIS
            system_prompt="What this module does",  # CHANGE THIS
            capabilities=[
                # LIST YOUR ACTIONS HERE
                "action_1",
                "action_2",
            ],
            registry=registry
        )
        
        # REQUIRED ATTRIBUTES - DO NOT SKIP
        self.version = "1.0.0"
        self.description = "Detailed description"
        
        # Your initialization
        self._initialized = False
        
    async def start(self) -> None:
        """Initialize the module"""
        if not self._initialized:
            # Your initialization here
            self._initialized = True
            logger.info(f"{self.name} module started")
            
    async def stop(self) -> None:
        """Cleanup resources"""
        # Your cleanup here
        logger.info(f"{self.name} module stopped")
        
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process requests from the communicator"""
        try:
            action = request.get("action")
            
            # Route to handlers
            if action == "action_1":
                result = await self._handle_action_1(request)
            elif action == "action_2":
                result = await self._handle_action_2(request)
            else:
                return {
                    "success": False,
                    "error": f"Unknown action: {action}",
                    "available_actions": self.capabilities
                }
            
            return {
                "success": True,
                "module": self.name,
                **result
            }
            
        except Exception as e:
            logger.error(f"Error in {self.name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "module": self.name
            }
    
    # Implement your handlers
    async def _handle_action_1(self, request: Dict[str, Any]) -> Dict[str, Any]:
        # Your logic here
        return {"data": "result"}
```

## Database Integration Checklist

- [ ] Create `database_factory.py`:
```python
# src/your_module/core/database/database_factory.py
import os
from loguru import logger

def get_database():
    """Get appropriate database backend"""
    
    # Try ArangoDB first
    if os.getenv("ARANGO_HOST"):
        try:
            from .database_arango import ArangoDatabase
            db = ArangoDatabase()
            logger.info("Using ArangoDB")
            return db
        except Exception as e:
            logger.warning(f"ArangoDB unavailable: {e}")
    
    # Your fallback
    from .database_default import DefaultDatabase
    return DefaultDatabase()
```

- [ ] Create `database_adapter.py`:
```python
# src/your_module/core/database/database_adapter.py
class DatabaseAdapter:
    def __init__(self):
        self.db = get_database()
        
    async def initialize(self):
        if hasattr(self.db, 'initialize'):
            await self.db.initialize()
```

- [ ] Use module-specific collection names:
```python
# In ArangoDB implementation
self.collections = {
    'items': f'{module_name}_items',  # e.g., sparta_missions
    'metadata': f'{module_name}_metadata'
}
```

## Common Fixes Applied to DARPA Crawl

### 1. Missing Model Classes
If you get `ImportError: No module named 'ModelInDB'`:
```python
# In models.py, add:
class YourModelCreate(BaseModel):
    """For creating items"""
    field1: str
    field2: Optional[str] = None

class YourModelInDB(YourModelCreate):
    """For database storage"""
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. ArangoDB Unique Constraints
If you get unique constraint violations:
```python
# When storing documents
doc = item.dict()
doc['_key'] = hashlib.md5(item.unique_id.encode()).hexdigest()
doc['source_id'] = item.unique_id  # Add this for indexes
collection.insert(doc, overwrite=True)  # Use overwrite
```

### 3. Missing Adapter Methods
Common methods your database class needs:
```python
async def get_item_count(self) -> int:
    """Count items in database"""
    
async def get_item_by_id(self, item_id: str) -> Optional[Dict]:
    """Retrieve specific item"""
    
async def search_items(self, query: str, limit: int = 50) -> List[Dict]:
    """Search functionality"""
```

## Integration Test Template

```python
# tests/test_integration.py
import pytest
from your_module.core.your_module import YourModule

@pytest.mark.asyncio
async def test_module_basics():
    """Test module has required interface"""
    module = YourModule()
    
    # Check required attributes
    assert hasattr(module, 'name')
    assert hasattr(module, 'version')
    assert hasattr(module, 'capabilities')
    assert hasattr(module, 'description')
    
    # Test lifecycle
    await module.start()
    assert module._initialized
    
    # Test basic action
    result = await module.process({
        "action": "your_action",
        "test": True
    })
    assert result["success"]
    assert result["module"] == module.name
    
    await module.stop()

@pytest.mark.asyncio 
async def test_error_handling():
    """Test module handles errors gracefully"""
    module = YourModule()
    await module.start()
    
    # Test unknown action
    result = await module.process({
        "action": "unknown_action"
    })
    assert not result["success"]
    assert "error" in result
    assert "available_actions" in result
```

## Environment File Template

```bash
# .env
PYTHONPATH=./src

# Module configuration
MODULE_NAME=your_module
LOG_LEVEL=INFO

# ArangoDB (if using)
ARANGO_HOST="http://localhost:8529"
ARANGO_USER="root"
ARANGO_PASSWORD="openSesame"
ARANGO_DB_NAME="granger"

# Your API keys
YOUR_API_KEY=key_here
```

## Final Checklist

Before marking integration complete:

- [ ] Module class inherits from BaseModule
- [ ] Has name, version, description, capabilities
- [ ] Implements start(), stop(), process()
- [ ] Returns standard response format
- [ ] Database adapter created (if needed)
- [ ] ArangoDB integration tested (if applicable)
- [ ] Integration tests pass
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Documentation updated

## Quick Test Script

```bash
# Create test_module.py
cat > test_module.py << 'EOF'
import asyncio
from your_module.core.your_module import YourModule

async def test():
    module = YourModule()
    await module.start()
    
    result = await module.process({
        "action": "get_status"
    })
    
    print(f"Module: {module.name} v{module.version}")
    print(f"Result: {result}")
    
    await module.stop()

asyncio.run(test())
EOF

python test_module.py
```

## Common Commands

```bash
# Run tests
pytest tests/test_integration.py -v

# Check which database is being used
python -c "from your_module.core.database.database_factory import get_database; print(type(get_database()).__name__)"

# Test module import
python -c "from your_module.core.your_module import YourModule; print('✅ Import successful')"
```

## If Something Goes Wrong

1. **Check imports**: Make sure all classes exist and are imported correctly
2. **Check async**: Ensure all database/API methods are `async`
3. **Check attributes**: Verify `version` and `description` are set
4. **Check logs**: Enable `LOG_LEVEL=DEBUG` for detailed errors
5. **Check database**: Verify ArangoDB is running if configured

## Success Indicators

✅ Module imports without errors  
✅ Integration tests pass  
✅ Module responds to process() calls  
✅ Database operations work (if applicable)  
✅ Logging shows expected messages  

---

Remember: The DARPA Crawl module integration is your reference implementation. When in doubt, check how it was done there!