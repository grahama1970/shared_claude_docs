# 🔧 AGENT FIX DIRECTIVE - IMMEDIATE ACTION REQUIRED

**Generated**: 2025-06-07 16:19:27
**Project**: runpod_ops
**Path**: /home/graham/workspace/experiments/runpod_ops
**Total Issues**: 4

## 🎯 YOUR MISSION

You MUST fix all the issues listed below in the runpod_ops project. This is not optional - these fixes are required for the Granger ecosystem to function properly.

## 📋 ISSUES TO FIX


### Issue #1: missing_description

**Description**: Documentation header missing description
**Evidence**: ['No Description or Purpose field found']

### Required Actions:
1. Investigate the issue in detail
2. Implement appropriate fixes
3. Verify the fix resolves the issue
4. Run tests to confirm


### Issue #2: missing_description

**Description**: Documentation header missing description
**Evidence**: ['No Description or Purpose field found']

### Required Actions:
1. Investigate the issue in detail
2. Implement appropriate fixes
3. Verify the fix resolves the issue
4. Run tests to confirm


### Issue #3: missing_description

**Description**: Documentation header missing description
**Evidence**: ['No Description or Purpose field found']

### Required Actions:
1. Investigate the issue in detail
2. Implement appropriate fixes
3. Verify the fix resolves the issue
4. Run tests to confirm


### Issue #4: mock_usage_detected

## Fix Required: Remove Mock Usage in runpod_ops

**Issue**: Tests are using mocks instead of real system interactions.
**Files**: ['tests/test_core/test_ssh_manager_enhanced_standalone.py']

### Required Actions:
1. Navigate to the project: `cd /home/graham/workspace/experiments/runpod_ops`
2. Remove all mock decorators and mock imports from test files
3. Replace mocked calls with real service connections:
   - For database tests: Connect to localhost:8529 (ArangoDB)
   - For API tests: Use real HTTP endpoints
   - For file operations: Use actual file I/O
4. Add proper test fixtures that create/clean real test data
5. Ensure all tests meet minimum duration requirements:
   - Database operations: >0.1s
   - API calls: >0.05s
   - File I/O: >0.01s

### Example Fix:
```python
# REMOVE THIS:
@mock.patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    
# REPLACE WITH:
def test_api_call():
    response = requests.get('http://localhost:8000/api/endpoint')
    assert response.status_code == 200
    assert response.elapsed.total_seconds() > 0.05  # Ensure real network call
```

**IMPORTANT**: After making changes, run tests again to verify they use real systems.

## 🚀 EXECUTION INSTRUCTIONS

1. **START HERE**: Navigate to the project directory
   ```bash
   cd /home/graham/workspace/experiments/runpod_ops
   source .venv/bin/activate || source venv/bin/activate
   ```

2. **FIX EACH ISSUE**: Work through the issues systematically
   - Read each issue description carefully
   - Implement the suggested fixes
   - Test after each fix to verify it works

3. **VERIFY ALL FIXES**: After fixing all issues, run:
   ```bash
   pytest tests/ -v --durations=0
   ```
   
4. **CONFIRM SUCCESS**: Ensure:
   - All tests pass (except honeypots which should fail)
   - No mocks are used in tests
   - Test durations meet minimum thresholds
   - Real services are being used

## ⚠️ IMPORTANT NOTES

- **NO MOCKS**: Do not use any mocking in tests. All tests must use real services.
- **REAL DATA**: Tests must interact with actual databases, APIs, and file systems.
- **TIMING MATTERS**: Fast tests indicate mocking. Real operations take time.
- **HONEYPOTS FAIL**: Honeypot tests must always fail. If they pass, something is wrong.

## 📊 SUCCESS CRITERIA

Your fixes are successful when:
- [ ] All mock usage has been removed
- [ ] Tests connect to real services
- [ ] Test durations reflect real operations
- [ ] Honeypot tests are present and failing
- [ ] All non-honeypot tests pass
- [ ] No fake test indicators remain

**START FIXING NOW** - Do not wait for further instructions. Begin with Issue #1 and work through all issues systematically.
