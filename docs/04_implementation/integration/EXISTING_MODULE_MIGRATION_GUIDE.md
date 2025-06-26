# Migrating Existing Modules to Claude Module Communicator

This guide helps you migrate existing Granger modules to work with the Claude Module Communicator hub.

## Module Migration Status

| Module | Current State | Migration Complexity | Key Changes Needed |
|--------|--------------|---------------------|-------------------|
| **shared_claude_docs** | Documentation only | N/A | No code to migrate |
| **darpa_crawl** | ✅ Complete | Reference | Already integrated |
| **rl_commons** | Standalone library | Medium | Wrap in BaseModule, async methods |
| **aider-daemon** | CLI tool | High | Major refactoring needed |
| **sparta** | MCP server | Low | Already has MCP interface |
| **marker** | Library + CLI | Medium | Create module wrapper |
| **arangodb** | Database utilities | Low | Utility module, minimal changes |
| **chat** | MCP client | Low | Already communicates with MCP |
| **youtube_transcripts** | Standalone | Medium | Add module interface |
| **claude_max_proxy** | Proxy service | Medium | Wrap proxy in module |
| **arxiv-mcp-server** | MCP server | Low | Already has MCP interface |
| **claude-module-communicator** | Hub | N/A | This is the hub |
| **claude-test-reporter** | Utility | Low | Simple wrapper needed |
| **fine_tuning** | Training tool | High | Complex async operations |
| **marker-ground-truth** | Evaluation tool | Medium | Database integration needed |
| **mcp-screenshot** | MCP server | Low | Already has MCP interface |

## Migration Patterns by Module Type

### 1. MCP Servers (sparta, arxiv-mcp-server, mcp-screenshot)

These already have MCP interfaces, so migration is straightforward:

```python
# src/mcp_module_wrapper.py
from claude_coms.base_module import BaseModule
from your_mcp_server import YourMCPServer

class YourMCPModule(BaseModule):
    def __init__(self, registry=None):
        super().__init__(
            name="your_mcp_module",
            system_prompt="MCP server wrapper",
            capabilities=[
                # Map MCP tools to capabilities
                "mcp_tool_1",
                "mcp_tool_2"
            ],
            registry=registry
        )
        self.version = "1.0.0"
        self.mcp_server = YourMCPServer()
        
    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route to MCP server"""
        action = request.get("action")
        
        # Map action to MCP tool call
        if action in self.mcp_server.tools:
            result = await self.mcp_server.call_tool(
                action, 
                request.get("params", {})
            )
            return {
                "success": True,
                "module": self.name,
                "data": result
            }
```

### 2. Libraries (rl_commons, marker)

Wrap existing functionality in a module interface:

```python
# Example for rl_commons
from claude_coms.base_module import BaseModule
from rl_commons import RLAgent, Environment

class RLCommonsModule(BaseModule):
    def __init__(self, registry=None):
        super().__init__(
            name="rl_commons",
            system_prompt="Reinforcement learning operations",
            capabilities=[
                "create_agent",
                "train_agent",
                "evaluate_policy",
                "score_opportunity"
            ],
            registry=registry
        )
        self.version = "1.0.0"
        self.agents = {}  # Store active agents
        
    async def _handle_create_agent(self, request: Dict[str, Any]):
        """Create new RL agent"""
        agent_type = request.get("agent_type", "dqn")
        agent_id = request.get("agent_id", str(uuid.uuid4()))
        
        # Create agent with rl_commons
        agent = RLAgent(agent_type, **request.get("config", {}))
        self.agents[agent_id] = agent
        
        return {
            "agent_id": agent_id,
            "agent_type": agent_type,
            "status": "created"
        }
```

### 3. CLI Tools (aider-daemon)

These need significant refactoring:

```python
# Extract core functionality into async methods
class AiderModule(BaseModule):
    def __init__(self, registry=None):
        super().__init__(
            name="aider_daemon",
            system_prompt="AI coding assistant",
            capabilities=[
                "analyze_code",
                "suggest_changes",
                "apply_edits",
                "run_tests"
            ],
            registry=registry
        )
        self.version = "1.0.0"
        
    async def _handle_analyze_code(self, request: Dict[str, Any]):
        """Analyze code without CLI"""
        file_path = request.get("file_path")
        
        # Extract aider's analysis logic
        # Make it async and return results
        analysis = await self._run_aider_analysis(file_path)
        
        return {"analysis": analysis}
```

### 4. Database Utilities (arangodb)

Minimal wrapper needed:

```python
class ArangoDBModule(BaseModule):
    """Utility module for ArangoDB operations"""
    
    def __init__(self, registry=None):
        super().__init__(
            name="arangodb_utils",
            system_prompt="ArangoDB utility operations",
            capabilities=[
                "create_collection",
                "create_indexes",
                "backup_database",
                "query_graph"
            ],
            registry=registry
        )
        self.version = "1.0.0"
        
    async def _handle_create_collection(self, request: Dict[str, Any]):
        """Create new collection"""
        from arangodb.core.db_connection import get_db_connection
        
        db = get_db_connection()
        collection_name = request.get("collection_name")
        
        if not db.has_collection(collection_name):
            db.create_collection(collection_name)
            
        return {"created": True, "collection": collection_name}
```

## Specific Module Migration Steps

### SPARTA Migration

1. **Current Structure**: MCP server with NASA data tools
2. **Migration Steps**:
   ```python
   # src/sparta_module.py
   from claude_coms.base_module import BaseModule
   from sparta.mcp_server import SPARTAServer
   
   class SPARTAModule(BaseModule):
       def __init__(self, registry=None):
           super().__init__(
               name="sparta",
               system_prompt="Space cybersecurity data",
               capabilities=[
                   "search_cve",
                   "get_space_assets",
                   "analyze_vulnerabilities"
               ],
               registry=registry
           )
           self.sparta_server = SPARTAServer()
   ```

3. **Database Integration**:
   - Keep existing SQLite for CVE data
   - Add ArangoDB for relationships with other modules

### Marker Migration

1. **Current Structure**: PDF processing library
2. **Migration Steps**:
   ```python
   # src/marker_module.py
   class MarkerModule(BaseModule):
       capabilities = [
           "convert_pdf",
           "extract_tables", 
           "validate_extraction"
       ]
       
       async def _handle_convert_pdf(self, request):
           file_path = request.get("file_path")
           
           # Use marker's conversion
           from marker.convert import convert_single_pdf
           from marker.models import load_all_models
           
           # Make async
           result = await asyncio.to_thread(
               convert_single_pdf,
               file_path,
               self.models
           )
           
           # Store in ArangoDB
           await self._store_extraction(result)
   ```

### YouTube Transcripts Migration

1. **Current Structure**: Transcript fetcher with embeddings
2. **Migration Steps**:
   ```python
   class YouTubeTranscriptsModule(BaseModule):
       capabilities = [
           "fetch_transcript",
           "search_transcripts",
           "get_channel_videos"
       ]
       
       async def _handle_fetch_transcript(self, request):
           video_id = request.get("video_id")
           
           # Reuse existing logic
           from youtube_transcripts.core import get_transcript
           
           transcript = await get_transcript(video_id)
           
           # Store in shared ArangoDB
           await self.db.store_transcript(transcript)
   ```

### Claude Max Proxy Migration

1. **Current Structure**: LLM proxy service
2. **Migration Steps**:
   ```python
   class ClaudeMaxProxyModule(BaseModule):
       capabilities = [
           "unified_llm_call",
           "get_best_model",
           "estimate_tokens"
       ]
       
       async def _handle_unified_llm_call(self, request):
           # Route through existing proxy
           from claude_max_proxy import proxy_call
           
           response = await proxy_call(
               model=request.get("model"),
               messages=request.get("messages"),
               module_name=request.get("requesting_module")
           )
           
           # Track usage per module
           await self._track_usage(request.get("requesting_module"))
   ```

## Database Migration Strategy

### 1. Shared Collections

Create shared collections in ArangoDB for cross-module data:

```python
# Shared collections for all modules
SHARED_COLLECTIONS = {
    'granger_documents': 'All processed documents',
    'granger_entities': 'Extracted entities',
    'granger_relationships': 'Cross-module relationships',
    'granger_metrics': 'Performance and usage metrics'
}
```

### 2. Module-Specific Collections

Each module gets its own namespace:

```python
# Module collection naming
def get_collection_name(module_name: str, collection_type: str) -> str:
    """Generate consistent collection names"""
    return f"{module_name}_{collection_type}"

# Examples:
# sparta_vulnerabilities
# marker_extractions
# youtube_transcripts_videos
```

### 3. Migration Script

```python
# scripts/migrate_to_arangodb.py
import asyncio
from arangodb import ArangoDatabase

async def migrate_module_data(module_name: str, source_db_path: str):
    """Migrate module data to ArangoDB"""
    
    # Connect to ArangoDB
    arango = ArangoDatabase()
    await arango.initialize()
    
    # Create module collections
    collections = [
        f"{module_name}_items",
        f"{module_name}_metadata"
    ]
    
    for collection in collections:
        if not arango.db.has_collection(collection):
            arango.db.create_collection(collection)
    
    # Migrate data (example for SQLite source)
    import sqlite3
    conn = sqlite3.connect(source_db_path)
    
    # ... migration logic ...
```

## Testing Migration

### 1. Module Interface Test

```python
# tests/test_module_interface.py
@pytest.mark.asyncio
async def test_migrated_module():
    """Test module meets interface requirements"""
    
    module = YourMigratedModule()
    
    # Check interface
    assert hasattr(module, 'process')
    assert hasattr(module, 'start')
    assert hasattr(module, 'stop')
    assert hasattr(module, 'version')
    
    # Test basic operation
    await module.start()
    result = await module.process({
        "action": "test_action"
    })
    assert result["success"]
```

### 2. Inter-Module Communication Test

```python
@pytest.mark.asyncio
async def test_module_communication():
    """Test module can communicate with others"""
    
    from claude_module_communicator import ModuleCommunicator
    
    comm = ModuleCommunicator()
    
    # Register modules
    module1 = Module1()
    module2 = Module2()
    
    comm.register_module("module1", module1)
    comm.register_module("module2", module2)
    
    # Test communication
    result = await comm.send_to_module("module2", {
        "action": "process_data",
        "from_module": "module1"
    })
```

## Deployment Strategy

### 1. Gradual Migration

1. Start with low-complexity modules (MCP servers)
2. Test each module independently
3. Test inter-module communication
4. Deploy to staging environment
5. Monitor for issues
6. Deploy to production

### 2. Backward Compatibility

Keep existing interfaces while adding module interface:

```python
class BackwardCompatibleModule(BaseModule):
    """Module that maintains old API"""
    
    def old_api_method(self, *args, **kwargs):
        """Existing API - maintained for compatibility"""
        # Original implementation
        
    async def process(self, request: Dict[str, Any]):
        """New module interface"""
        action = request.get("action")
        
        if action == "legacy_call":
            # Route to old API
            return await asyncio.to_thread(
                self.old_api_method,
                *request.get("args", []),
                **request.get("kwargs", {})
            )
```

### 3. Configuration Management

Update configurations for hub architecture:

```yaml
# config/modules.yaml
modules:
  sparta:
    enabled: true
    version: "2.0.0"
    database: "arangodb"
    collections:
      - sparta_vulnerabilities
      - sparta_assets
      
  marker:
    enabled: true
    version: "1.5.0"
    max_file_size: "100MB"
    output_format: "markdown"
```

## Common Migration Issues

### 1. Synchronous to Async

Convert synchronous code:
```python
# Old synchronous
def process_data(data):
    result = heavy_computation(data)
    return result

# New async
async def process_data(data):
    # Run in thread pool
    result = await asyncio.to_thread(heavy_computation, data)
    return result
```

### 2. Global State

Remove global state:
```python
# Old: Global state
global_cache = {}

def get_data(key):
    return global_cache.get(key)

# New: Instance state
class Module:
    def __init__(self):
        self.cache = {}
        
    async def get_data(self, key):
        return self.cache.get(key)
```

### 3. File I/O

Make file operations async:
```python
# Use aiofiles
import aiofiles

async def read_file(path):
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()
    return content
```

## Monitoring and Metrics

Add module metrics:

```python
class MonitoredModule(BaseModule):
    def __init__(self):
        super().__init__(...)
        self.metrics = {
            "requests_processed": 0,
            "errors": 0,
            "average_response_time": 0
        }
        
    async def process(self, request):
        start_time = time.time()
        
        try:
            result = await super().process(request)
            self.metrics["requests_processed"] += 1
        except Exception as e:
            self.metrics["errors"] += 1
            raise
        finally:
            elapsed = time.time() - start_time
            # Update average response time
            
        return result
```

## Conclusion

Migration complexity varies by module type:
- **Easy**: MCP servers, simple utilities
- **Medium**: Libraries with clear interfaces
- **Hard**: CLI tools, complex state management

Start with easy modules to establish patterns, then tackle more complex ones. Use DARPA Crawl as the reference implementation for all migrations.