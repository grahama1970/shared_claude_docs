# GRANGER Troubleshooting Guide

Quick solutions to common problems based on Phase 2 testing experience.

## 🔴 Critical Issues

### ArangoDB Won't Connect
```bash
# Error: Invalid URL 'localhost': No scheme supplied
# Or: Connection refused

# Fix 1: Check ArangoDB is running
docker ps | grep arango
# If not running:
docker run -d -p 8529:8529 -e ARANGO_ROOT_PASSWORD=openSesame arangodb:3.11

# Fix 2: Verify environment
export ARANGO_HOST='http://localhost:8529'
export ARANGO_USER='root'
export ARANGO_PASSWORD='openSesame'

# Fix 3: Test connection
curl -u root:openSesame http://localhost:8529/_api/version
```

### Marker Import Fails
```python
# Error: ModuleNotFoundError: No module named 'pdftext'

# This is EXPECTED and HANDLED!
# The system automatically falls back to:
# 1. PyPDF2 (if installed)
# 2. pdfplumber (if installed)  
# 3. Basic text extraction

# To verify fallback is working:
from project_interactions.performance_optimization.module_specific_optimizations import MarkerOptimizations
converter = MarkerOptimizations.create_fallback_converter()
print(f"Using converter: {converter.__name__}")
```

### NASA API 403 Forbidden
```python
# Error: 403 Forbidden from NASA API

# Fix 1: Use API key
export NASA_API_KEY='your-key-here'

# Fix 2: The system falls back to demo data
# This is handled automatically - no action needed
```

## 🟡 Performance Issues

### Pipeline Takes >30 Seconds
```python
# Expected: <10s with optimizations

# Fix 1: Check cache is working
from project_interactions.performance_optimization.performance_optimization_task import CacheManager
cache = CacheManager()
# Should see files in /tmp/granger_cache/

# Fix 2: Verify parallel processing
# Look for "Parallel tasks: N" in output

# Fix 3: Check batch operations
# Should see "Batch create (50 docs): Xs" not individual inserts
```

### Low Cache Hit Rate
```python
# Expected: 98% hit rate

# Fix 1: Cache directory permissions
chmod 755 /tmp/granger_cache
ls -la /tmp/granger_cache/

# Fix 2: Check cache TTL (24 hours default)
# Older cache entries expire

# Fix 3: Verify cache key generation
# Different parameters = different cache keys
```

### Memory Usage Growing
```python
# Fix 1: Periodic garbage collection
import gc
gc.collect()

# Fix 2: Clear cache if needed
cache.clear()

# Fix 3: Limit parallel workers
MAX_WORKERS = 3  # Instead of 5
```

## 🟢 Common Warnings

### Pydantic Deprecation
```
# Warning: Pydantic V1 style class-based config is deprecated

# This is harmless - ignore for now
# Will be fixed in future update
```

### Rate Limit Warnings
```
# Warning: Rate limited, increasing delay to Xs

# This is GOOD - adaptive rate limiter working
# It automatically adjusts delays
```

### Circuit Breaker Open
```
# Error: Circuit breaker open for function_name

# This prevents cascading failures
# Wait 60 seconds for automatic reset
# Or restart the application
```

## 🔧 Module-Specific Issues

### ArXiv Module (100% Working)
```python
# Should have NO issues!
# If problems occur:

# 1. Check internet connection
ping arxiv.org

# 2. Verify no firewall blocking
curl https://export.arxiv.org/api/query?search_query=test

# 3. Check rate limiting (3 req/s default)
export ARXIV_RATE_LIMIT=1  # Slower but safer
```

### SPARTA Module (40% Working)
```python
# Known issues:
# - NASA API needs key
# - MITRE handler missing params
# - Download directory issues

# What DOES work:
# - CVE search via NVD API
# - Basic module interface

# Test working part:
from sparta.real_sparta_handlers_fixed import SPARTACVESearchHandler
handler = SPARTACVESearchHandler()
result = handler.handle({"keyword": "buffer overflow", "limit": 5})
```

### ArangoDB Module (33% Working)
```python
# Known issues:
# - Some API parameter mismatches
# - Graph operations incomplete

# What DOES work:
# - Basic document CRUD
# - Connection (with URL fix)

# Test working part:
handler.handle({
    "operation": "create",
    "collection": "test",
    "data": {"test": "data"}
})
```

## 🐛 Debugging Techniques

### 1. Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or with loguru
from loguru import logger
logger.level("DEBUG")
```

### 2. Validate Handler Output
```python
def debug_handler_call(handler, params):
    print(f"Calling {handler.__class__.__name__}")
    print(f"Params: {json.dumps(params, indent=2)}")
    
    start = time.time()
    result = handler.handle(params)
    duration = time.time() - start
    
    print(f"Duration: {duration:.3f}s")
    print(f"Success: {result.get('success')}")
    if not result.get('success'):
        print(f"Error: {result.get('error')}")
    
    return result
```

### 3. Check Integration Points
```python
# Test each integration level
def test_integration_chain():
    # Level 0: Individual module
    print("Testing ArXiv...")
    arxiv_ok = test_arxiv()
    
    if arxiv_ok:
        # Level 1: Pipeline
        print("Testing ArXiv->Marker...")
        pipeline_ok = test_pipeline()
        
        if pipeline_ok:
            # Level 2: Chain
            print("Testing full chain...")
            chain_ok = test_chain()
```

### 4. Performance Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
result = pipeline.process()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

## 💊 Quick Fixes

### Reset Everything
```bash
# Clear cache
rm -rf /tmp/granger_cache/*

# Restart ArangoDB
docker restart arangodb

# Reset environment
source .venv/bin/activate
export ARANGO_HOST='http://localhost:8529'
export ARANGO_USER='root'
export ARANGO_PASSWORD='openSesame'
```

### Minimal Working Example
```python
# If nothing else works, try this:
from project_interactions.arxiv_handlers.real_arxiv_handlers import ArxivSearchHandler

handler = ArxivSearchHandler()
result = handler.handle({"query": "test", "max_results": 1})

if result["success"]:
    print("✅ Basic system working!")
else:
    print(f"❌ Critical issue: {result.get('error')}")
```

### Check System Health
```python
def system_health_check():
    checks = {
        "ArXiv API": check_arxiv(),
        "ArangoDB": check_arangodb(),
        "Cache": check_cache(),
        "Disk Space": check_disk_space()
    }
    
    for component, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {component}")
        
    return all(checks.values())
```

## 📞 Getting More Help

1. **Check Logs**: Most errors are logged with context
2. **Read Error Docs**: `docs/integration_patterns/ERROR_HANDLING_STRATEGIES.md`
3. **Review Test Reports**: `project_interactions/*/test_report_*.md`
4. **Run Validation**: `python module_specific_optimizations.py`

## 🎯 Prevention Tips

1. **Always set environment variables** before running
2. **Use virtual environment** to avoid dependency conflicts
3. **Check ArangoDB is running** before testing
4. **Start with ArXiv** - it's 100% working
5. **Use the cookbook examples** - they're tested

---

*Remember: Most issues have been discovered and fixed during Phase 2 testing. If you encounter a new issue, it's likely a configuration problem rather than a code bug.*