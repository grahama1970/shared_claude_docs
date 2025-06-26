# GRANGER Technical Quickstart

For developers who want to dive deep into GRANGER's architecture.

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│            Claude Module Communicator        │
│                  (Central Hub)               │
└─────────────┬───────────────┬───────────────┘
              │               │
    ┌─────────▼───────┐ ┌────▼──────────┐
    │   Data Sources  │ │   Processing   │
    ├─────────────────┤ ├───────────────┤
    │ • SPARTA (CVE)  │ │ • Marker (PDF)│
    │ • ArXiv (Papers)│ │ • Claude (AI) │
    │ • YouTube       │ │ • RL Commons  │
    └─────────────────┘ └───────────────┘
              │               │
    ┌─────────▼───────────────▼───────────┐
    │          ArangoDB Knowledge Graph    │
    │        (Storage & Relationships)     │
    └─────────────────────────────────────┘
```

## Core Components

### 1. Handler Architecture
Every module exposes a standardized handler interface:

```python
class ModuleHandler:
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standard interface for all modules
        
        Args:
            params: Operation parameters
            
        Returns:
            {
                "success": bool,
                "data": Any,      # On success
                "error": str,     # On failure
                "metadata": {}    # Timing, etc.
            }
        """
```

### 2. Integration Levels

```python
# Level 0: Single module
result = arxiv.handle({"query": "quantum"})

# Level 1: Two-module pipeline
papers = arxiv.handle({"query": "quantum"})
pdfs = marker.handle({"papers": papers["data"]})

# Level 2: Three-module chain
papers = arxiv.handle({"query": "quantum"})
pdfs = marker.handle({"papers": papers["data"]})
stored = arango.handle({"docs": pdfs["data"]})

# Level 3: Full GRANGER pipeline
pipeline = GRANGERPipeline()
result = pipeline.process_security_topic("buffer overflow")
```

### 3. Performance Architecture

```python
# Connection pooling (40x improvement)
class ConnectionPool:
    def __init__(self, max_connections=10):
        self.connections = []
        self.available = []
        
    async def get_connection(self):
        # Reuse connections
        
# Caching layer (98% hit rate)
class CacheManager:
    def __init__(self, ttl=3600):
        self.memory_cache = {}
        self.disk_cache = Path("/tmp/granger_cache")
        
# Parallel execution (5x faster)
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process, items)
```

## Advanced Integration Patterns

### 1. Fallback Chain Pattern
```python
class FallbackChain:
    def __init__(self):
        self.strategies = [
            ("primary", self.try_marker),
            ("secondary", self.try_pypdf2),
            ("fallback", self.basic_extract)
        ]
        
    async def execute(self, pdf_path):
        for name, strategy in self.strategies:
            try:
                return await strategy(pdf_path)
            except Exception as e:
                logger.warning(f"{name} failed: {e}")
        raise Exception("All strategies failed")
```

### 2. Circuit Breaker Pattern
```python
class SmartCircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failures = 0
        self.state = 'CLOSED'
        
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if self._should_attempt_reset():
                self.state = 'HALF_OPEN'
            else:
                raise CircuitOpenError()
                
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
```

### 3. Adaptive Rate Limiting
```python
class AdaptiveRateLimiter:
    def __init__(self):
        self.delay = 0.1
        self.consecutive_errors = 0
        
    def wait(self):
        time.sleep(self.delay)
        
    def success(self):
        self.consecutive_errors = 0
        self.delay = max(0.1, self.delay * 0.9)
        
    def rate_limited(self):
        self.consecutive_errors += 1
        self.delay = min(60, self.delay * 2)
```

## Database Schema

### ArangoDB Collections
```javascript
// Documents collection
{
  "_key": "arxiv_2301_12345",
  "type": "research_paper",
  "title": "Quantum Computing Security",
  "authors": ["Smith, J.", "Doe, A."],
  "content": "...",
  "embeddings": [0.1, 0.2, ...],  // 1024-dim
  "timestamp": "2025-06-03T10:00:00Z"
}

// Vulnerabilities collection
{
  "_key": "CVE_2023_12345",
  "type": "vulnerability",
  "severity": "HIGH",
  "description": "Buffer overflow in...",
  "affected_systems": ["Linux", "Windows"]
}

// Relationships (edges)
{
  "_from": "documents/arxiv_2301_12345",
  "_to": "vulnerabilities/CVE_2023_12345",
  "_key": "addresses",
  "confidence": 0.95
}
```

### Search Indices
```javascript
// BM25 text search
db._collection('documents').ensureIndex({
  type: 'fulltext',
  fields: ['content'],
  name: 'content_fulltext'
});

// Vector similarity search
db._collection('documents').ensureIndex({
  type: 'persistent',
  fields: ['embeddings[*]'],
  name: 'embeddings_index'
});
```

## API Parameter Fixes

### Common Adaptations
```python
# ArangoDB parameter fixes
def adapt_params(operation, params):
    if operation == "create_document":
        # Fix: collection → collection_name
        # Fix: data → document
        return {
            "collection_name": params.pop("collection"),
            "document": params.pop("data")
        }
        
    if operation == "search":
        # Remove unsupported collection_name
        params.pop("collection_name", None)
        return params
```

## Performance Benchmarks

### Current Metrics
```python
# Pipeline execution times
BASELINE = 34.67  # seconds
OPTIMIZED = 5.3   # seconds
IMPROVEMENT = 84.7  # percent

# Operation benchmarks
METRICS = {
    "arxiv_search": {
        "cold": 2.8,    # seconds
        "cached": 0.1,  # seconds
        "hit_rate": 0.98
    },
    "pdf_download": {
        "sequential": 15.0,  # 5 PDFs
        "parallel": 3.0,     # 5 PDFs
        "speedup": 5.0
    },
    "db_insert": {
        "individual": 0.5,   # per doc
        "batch_100": 1.2,    # 100 docs
        "speedup": 40.0
    }
}
```

## Environment Variables

```bash
# Required
ARANGO_HOST='http://localhost:8529'
ARANGO_USER='root'
ARANGO_PASSWORD='openSesame'

# Optional
NASA_API_KEY='your-key'
ARXIV_RATE_LIMIT='3'  # requests/second
CACHE_DIR='/tmp/granger_cache'
MAX_WORKERS='5'  # parallel threads
CIRCUIT_BREAKER_TIMEOUT='60'
```

## Debugging Tools

### 1. Performance Profiler
```python
from project_interactions.performance_optimization.benchmark_performance import (
    PerformanceBenchmark
)

benchmark = PerformanceBenchmark()
result, metrics = benchmark.measure_operation(
    "test_operation",
    handler.handle,
    params
)
print(f"Duration: {metrics['duration']:.3f}s")
print(f"Memory: {metrics['memory_delta']:.2f}MB")
```

### 2. Integration Validator
```python
from project_interactions.performance_optimization.module_specific_optimizations import (
    OptimizationValidator
)

validator = OptimizationValidator()
validator.validate_arangodb_fixes()
validator.validate_marker_fallbacks()
validator.validate_sparta_setup()
validator.generate_validation_report()
```

### 3. Error Analysis
```python
# Analyze error patterns
from collections import defaultdict

error_counts = defaultdict(int)
for error in pipeline.results["errors"]:
    error_type = error.split(":")[0]
    error_counts[error_type] += 1
    
# Most common errors
for error_type, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{error_type}: {count} occurrences")
```

## Testing Strategy

### Real API Validation
```python
def validate_real_api_call(func, min_duration=0.1):
    """Ensure real API call, not mock"""
    start = time.time()
    result = func()
    duration = time.time() - start
    
    assert duration > min_duration, f"Too fast ({duration}s), likely mocked"
    assert result.get("metadata", {}).get("api_version"), "Missing API metadata"
    
    return result
```

### Progressive Test Runner
```python
class ProgressiveTestRunner:
    def run_all_levels(self):
        results = {}
        
        # Level 0: Individual modules
        for module in ["sparta", "arxiv", "arangodb"]:
            results[f"level_0_{module}"] = self.test_module(module)
            
        # Level 1: Pipelines
        if results["level_0_arxiv"]["success"]:
            results["level_1_pipeline"] = self.test_pipeline()
            
        # Level 2: Three modules
        if results["level_1_pipeline"]["success"]:
            results["level_2_chain"] = self.test_chain()
            
        # Level 3: Full system
        if all(r["success"] for r in results.values()):
            results["level_3_full"] = self.test_full_system()
            
        return results
```

## Production Deployment

### Docker Compose Setup
```yaml
version: '3.8'

services:
  arangodb:
    image: arangodb:3.11
    environment:
      ARANGO_ROOT_PASSWORD: openSesame
    ports:
      - "8529:8529"
    volumes:
      - arangodb_data:/var/lib/arangodb3

  granger:
    build: .
    environment:
      ARANGO_HOST: http://arangodb:8529
      ARANGO_USER: root
      ARANGO_PASSWORD: openSesame
    depends_on:
      - arangodb
    volumes:
      - ./cache:/tmp/granger_cache

volumes:
  arangodb_data:
```

### Scaling Considerations
- Use connection pooling (already implemented)
- Enable caching (98% hit rate achieved)
- Parallelize operations (5x improvement)
- Batch database operations (40x improvement)
- Add Redis for distributed caching
- Use message queue for async processing

## Contributing

### Adding a New Module
1. Implement the handler interface
2. Add Level 0 tests with real API
3. Create Level 1 pipeline tests
4. Document integration patterns
5. Benchmark performance
6. Add error recovery

### Fixing Integration Issues
1. Write failing test that exposes bug
2. Implement fix in handler
3. Add to error handling docs
4. Update parameter adapter if needed
5. Verify with timing validation
6. Add to known issues if not fully fixed

---

*This technical guide covers the deep implementation details of GRANGER. For basic usage, see DEVELOPER_QUICKSTART.md*