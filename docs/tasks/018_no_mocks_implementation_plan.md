# Task 018: NO MOCKS Implementation Plan

**Date**: 2025-01-07
**Status**: Critical - Immediate Action Required
**Mandate**: CLAUDE.md explicitly states "Real data only: Never use fake/mocked data for core tests"

## 🚫 The NO MOCKS Policy

Per CLAUDE.md requirements:
- **ALL tests MUST use real data**
- **NO fake/mocked data for core tests**
- **ALL package management through uv**
- **ALL projects use Python 3.10.11**

## 🔍 Current Violations

### 1. Mock Usage Found
The mock removal script found and modified numerous files:
- **granger_hub**: 100+ files with mock usage (includes embedded aider repo)
- **world_model**: Honeypot test uses MagicMock (but import was removed)
- **Many .venv files**: Shows tests in dependencies use mocks

### 2. Python Version Issues
- **granger_hub**: Python 3.11.12 (corrupt pytest)
- **rl_commons**: Python 3.12.3
- **claude-test-reporter**: Python 3.11.12
- Multiple projects not using 3.10.11

### 3. Broken Tests After Mock Removal
- **world_model/tests/test_honeypot.py**: Uses MagicMock without import (NameError)
- Many tests will fail after mock removal because they need real connections

## 📋 Implementation Plan

### Phase 1: Fix Python Versions (ALL projects to 3.10.11)
```bash
# For each project:
cd /project
rm -rf .venv venv env
uv venv --python=3.10.11
uv sync
uv pip install pytest pytest-json-report
```

### Phase 2: Start Required Services
All tests need REAL services running:

1. **ArangoDB** (localhost:8529)
   ```bash
   docker run -d -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb
   ```

2. **GrangerHub** (localhost:8000)
   ```bash
   cd /home/graham/workspace/experiments/granger_hub
   source .venv/bin/activate
   python -m granger_hub.server
   ```

3. **Other Services**:
   - LLM Call Service (localhost:8001)
   - Test Reporter (localhost:8002)
   - Any other required services

### Phase 3: Fix Honeypot Tests
Honeypot tests should detect mocks, not use them:

```python
# WRONG (current):
mock_db = MagicMock()  # NameError!
orchestrator.db = mock_db

# RIGHT (should be):
# Test that real DB connection is required
with pytest.raises(ConnectionError):
    orchestrator = WorldModelOrchestrator()
    # Should fail without real DB at localhost:8529
    await orchestrator.connect()
```

### Phase 4: Implement Real Connections

For each test file that had mocks removed:

1. **Database Tests**:
   ```python
   # Connect to real ArangoDB
   from arango import ArangoClient
   client = ArangoClient(hosts='http://localhost:8529')
   db = client.db('test_db', username='root', password='')
   ```

2. **API Tests**:
   ```python
   # Make real HTTP calls
   import httpx
   response = httpx.get('http://localhost:8000/api/status')
   assert response.status_code == 200
   ```

3. **File I/O Tests**:
   ```python
   # Use real temp files
   import tempfile
   with tempfile.NamedTemporaryFile() as f:
       f.write(b'test data')
       f.flush()
       # Test with real file
   ```

### Phase 5: Verify Real Test Behavior

Add timing assertions to ensure real operations:

```python
def test_real_database_operation():
    start = time.time()
    # Do real database operation
    result = db.collection('test').insert({'data': 'test'})
    duration = time.time() - start
    
    assert duration > 0.01  # Real DB ops take time
    assert result['_id'] is not None  # Real insert returns ID
```

## 🚨 Critical Requirements

1. **NO MOCKS MEANS NO MOCKS**
   - No unittest.mock
   - No pytest-mock
   - No MagicMock, Mock, patch, monkeypatch
   - No fake objects pretending to be real services

2. **Real Services Required**
   - Tests WILL FAIL without services running
   - This is CORRECT behavior
   - Document service requirements clearly

3. **Test Duration Matters**
   - Instant tests (0.00s) indicate mocking
   - Real operations have latency:
     - Network calls: >0.05s
     - Database ops: >0.01s
     - File I/O: >0.001s

## 📝 Example: Converting Mocked Test to Real Test

### Before (WRONG):
```python
@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'data': 'fake'}
    
    result = my_function()
    assert result == 'fake'
```

### After (CORRECT):
```python
def test_api_call():
    # Requires real API service running
    response = requests.get('http://localhost:8000/api/endpoint')
    assert response.status_code == 200
    
    data = response.json()
    assert 'data' in data
    assert response.elapsed.total_seconds() > 0.05  # Real network latency
```

## 🔄 Rollout Plan

1. **Fix Python versions first** (all to 3.10.11)
2. **Start all required services**
3. **Fix honeypot tests** to detect mocks properly
4. **Convert mocked tests to real tests** one project at a time
5. **Verify with granger-verify** that no mocks remain

## ⚡ Quick Commands

```bash
# Fix Python version for a project
cd /project && rm -rf .venv && uv venv --python=3.10.11 && uv sync

# Start services (example)
docker run -d -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb

# Run tests with timing
pytest -v --durations=0

# Check for remaining mocks
grep -r "mock\|Mock\|patch" tests/ | grep -v "__pycache__"
```

## 🎯 Success Criteria

1. All projects use Python 3.10.11
2. Zero mock imports in any test file
3. All tests connect to real services
4. Test durations reflect real operations
5. Honeypot tests fail appropriately
6. granger-verify shows no mock usage

---

**Remember**: The goal is REAL TESTS with REAL DATA. If it's not connecting to a real service, it's not a valid test.