# Granger Integration Bug Report #002

*Generated: 2025-06-08*

## Summary

After fixing module import issues, we've discovered integration bugs that need to be addressed for the Granger ecosystem to work properly.

## Bugs Found

### 1. YouTube Transcripts Database Not Initialized ⚠️
**Issue**: `no such table: transcripts`
**Root Cause**: The YouTube transcripts module expects a SQLite database with FTS5 tables
**Fix**: Initialize database on first use
```python
# In youtube_transcripts/core/database.py
db = Database()
db.initialize()  # This creates the required tables
```

### 2. ArangoDB Database Missing ⚠️
**Issue**: `[HTTP 404][ERR 1228] database not found`
**Root Cause**: Trying to connect to 'granger_test' database that doesn't exist
**Fix**: Create database or use existing one
```bash
# Create test database
curl -X POST http://localhost:8529/_api/database \
  -d '{"name":"granger_test"}' \
  -H "Authorization: Basic $(echo -n 'root:' | base64)"
```

### 3. LLM Call Async/Await Mismatch ✅ (Fixed)
**Issue**: `RuntimeWarning: coroutine 'call' was never awaited`
**Root Cause**: llm_call.call is async but was called synchronously
**Fix**: Made calling function async and used await

### 4. Module Package Name Mismatches ⚠️
**Issue**: Package names in pyproject.toml don't match actual package names
**Examples**:
- `chat` → `granger-chat`
- `world_model` → `granger-world-model`
**Fix**: Update pyproject.toml references

## Integration Test Results

### Successful Integrations ✅
1. **youtube_transcripts**: Module imports and client creation work
2. **llm_call**: Successfully made LLM calls after async fix
3. **python-arango**: Installed and imports correctly
4. **Module discovery**: Found correct import patterns through investigation

### Failed Integrations ❌
1. **YouTube search**: Needs database initialization
2. **ArangoDB operations**: Needs database creation
3. **Full pipeline**: Can't complete anti-pattern analysis due to DB issues

## Recommendations

### Immediate Actions
1. **Initialize databases** before running integration tests
2. **Create setup script** that ensures all services are ready:
   ```bash
   #!/bin/bash
   # setup_granger_integration.sh
   
   # Start ArangoDB
   docker start arangodb || docker run -d --name arangodb -p 8529:8529 arangodb
   
   # Create test database
   sleep 5
   curl -X POST http://localhost:8529/_api/database \
     -d '{"name":"granger_test"}' \
     -H "Authorization: Basic $(echo -n 'root:' | base64)"
   
   # Initialize YouTube DB
   python -c "from youtube_transcripts.core.database import Database; db = Database(); db.initialize()"
   ```

3. **Fix package references** in all pyproject.toml files

### Long-term Improvements
1. **Add database initialization** to module __init__ files
2. **Create integration test suite** that sets up required infrastructure
3. **Document service dependencies** clearly in each module's README
4. **Add health checks** before attempting operations

## Positive Findings

1. **Module architecture is sound** - once dependencies are met, modules work
2. **Import patterns are discoverable** - we successfully found correct imports
3. **Error messages are informative** - helped diagnose issues quickly
4. **Modules are properly isolated** - failures in one don't crash others

## Next Steps

1. Run `setup_granger_integration.sh` to initialize services
2. Re-run anti-pattern analysis with proper infrastructure
3. Create PRs to fix package naming issues
4. Add database initialization to module setup