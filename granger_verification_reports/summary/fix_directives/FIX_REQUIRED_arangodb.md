# 🔧 AGENT FIX DIRECTIVE - IMMEDIATE ACTION REQUIRED

**Generated**: 2025-06-05 18:14:23
**Project**: arangodb
**Path**: /home/graham/workspace/experiments/arangodb
**Total Issues**: 1

## 🎯 YOUR MISSION

You MUST fix all the issues listed below in the arangodb project. This is not optional - these fixes are required for the Granger ecosystem to function properly.

## 📋 ISSUES TO FIX


### Issue #1: missing_doc_header

**Description**: Missing documentation header
**Evidence**: ['File has no docstring header']

### Required Actions:
1. Investigate the issue in detail
2. Implement appropriate fixes
3. Verify the fix resolves the issue
4. Run tests to confirm


## 🚀 EXECUTION INSTRUCTIONS

1. **START HERE**: Navigate to the project directory
   ```bash
   cd /home/graham/workspace/experiments/arangodb
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
