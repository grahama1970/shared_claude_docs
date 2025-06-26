# Test Verification Template Guide

**Purpose**: Systematic verification of test authenticity across codebases  
**Focus**: Iterating, debugging, and critically resolving test validity  
**Standard**: All tests must use REAL APIs/services - NO MOCKS ALLOWED  

---

## 📜 Core Principles

1. **REAL Tests Only**: Must interact with live systems (databases, APIs, files)
2. **Duration Requirements**: Tests must meet minimum time thresholds
3. **Confidence Validation**: ≥90% confidence required with evidence
4. **Maximum 3 Loops**: Fix and retry up to 3 times before escalation
5. **Honeypot Verification**: Include tests designed to fail
6. **NO SIMULATIONS**: NEVER simulate module functionality - use real modules even if they fail
7. **BE PROACTIVE WITH IMPORTS**: If a module fails to import, FIX IT:
   - Run `uv pip list` to check installed packages
   - Check `pyproject.toml` for dependencies
   - Use `uv add package` to add missing packages
   - Run `uv pip install -e .` to reinstall
   - Connection failures after import works ARE valuable test results
8. **MULTI-AI VERIFICATION**: Always verify critical results with both Perplexity and Gemini for well-rounded critique

---

## ⏱️ Duration Thresholds

| Operation Type | Minimum Duration | Rationale |
|----------------|------------------|-----------|
| Database Query | >0.1s | Connection overhead + query execution |
| API Call | >0.05s | Network latency + processing |
| File I/O | >0.01s | Disk access time |
| Integration Test | >0.5s | Multiple system interactions |
| Browser Automation | >1.0s | Page load + rendering |

---

## 🔧 Proactive Import Management (CRITICAL - DO NOT SKIP!)

**LESSON LEARNED**: Past bug hunts failed because they treated import errors as bugs instead of setup issues to fix immediately!

### IMMEDIATE ACTION REQUIRED for Import Errors

**STOP! Before reporting ANY import error as a bug, you MUST:**

1. **Fix it immediately** - No exceptions, no delays
2. **Document what you fixed** - For future reference
3. **Update all dependent modules** - Or the fix won't propagate
4. **Only THEN continue testing** - With working imports

**Import errors are NEVER bugs - they are YOUR responsibility to fix FIRST!**

### Import Error Response Protocol - EXECUTE IMMEDIATELY!
```bash
# When you see: ModuleNotFoundError: No module named 'package_name'
# DO THIS NOW (not later):
cd /path/to/project
uv add package_name
uv pip install -e .
python -c "import package_name"  # Verify it worked

# When you see: ImportError: cannot import name 'ClassName'
# DO THIS NOW:
uv pip install -e .  # Reinstall in editable mode
python -c "from module import ClassName"  # Verify it worked
# If still fails, check if the import path changed in recent commits

# When tests won't collect due to imports
# DO THIS NOW:
pytest --collect-only 2>&1 | grep -E "ModuleNotFound|ImportError" | while read line; do
    MODULE=$(echo $line | grep -oP "No module named '\K[^']+")
    echo "🔧 Fixing missing module: $MODULE"
    uv add $MODULE
done
uv pip install -e .
pytest --collect-only  # Verify all tests now collect
```

### Common GRANGER Module Dependencies
```bash
# Marker
uv add pdftext pymupdf4llm pillow

# ArXiv MCP Server  
uv add arxiv tree-sitter tree-sitter-language-pack

# SPARTA
uv add requests beautifulsoup4 lxml

# ArangoDB
uv add python-arango

# YouTube Transcripts
uv add youtube-transcript-api yt-dlp

# LLM Call
uv add litellm openai anthropic
```

### After ANY Module Update
```bash
# Critical: Update ALL modules that depend on the changed module
for proj in /home/graham/workspace/experiments/*/; do
    if grep -q "from updated_module" $proj/src/**/*.py 2>/dev/null; then
        cd $proj && uv pip install -e .
    fi
done
```

---

## 🔍 Pre-Verification Checklist

### 0. Project Structure and Dependencies Check 🆕
```bash
# CRITICAL: Check these BEFORE any testing to avoid wasted effort

# 1. Check Python version requirement
cat pyproject.toml | grep -E "python.*=" | grep -v python-
# If shows 3.12 but you have 3.10, STOP and fix this first!

# 2. Check project structure
ls -la src/  # Should have actual source files
find . -name "*.py" -path "*/src/*" | wc -l  # Should be > 0

# 3. Check for existing setup patterns
find . -name "*setup*.py" -o -name "*config*.py" | grep -v test
# Look especially for: arango_setup.py, db_setup.py, config.py

# 4. Check .env for service credentials
if [ -f .env ]; then
    echo "=== Service credentials in .env ==="
    grep -E "(ARANGO|REDIS|POSTGRES|API_KEY)" .env | sed 's/=.*/=***/'
fi

# 5. Check if tests can even be collected
python -m pytest --collect-only 2>&1 | head -20
# If "0 collected", you have bigger problems than test quality
```

### 0.1 Skeleton Project Detection
```bash
# Check for skeleton project indicators BEFORE running tests
# A skeleton project has <30% real implementation

# Count total lines vs implementation lines
find . -name "*.py" -not -path "./tests/*" -exec wc -l {} + | tail -1

# Check for skeleton patterns
grep -r "pass$" --include="*.py" | grep -v test | wc -l
grep -r "raise NotImplementedError" --include="*.py" | wc -l
grep -r "TODO\|FIXME\|XXX" --include="*.py" | wc -l
grep -r "return None$" --include="*.py" | grep -v test | wc -l

# If skeleton indicators > working functions, project needs implementation first
echo "⚠️ WARNING: If this is a skeleton project, tests will be meaningless"
echo "Run /granger-feature-sync first to detect and create implementation tasks"
```

### 1. Service Availability
```bash
# Check databases
docker ps | grep -E "(arangodb|redis|postgres|mysql)"
netstat -tuln | grep -E "(3306|5432|6379|8529)"

# Check API services
curl -s http://localhost:11434/api/tags | jq  # Ollama
curl -s http://localhost:8000/health          # Custom APIs

# Check browser automation
playwright install --check
which chromium || which google-chrome
```

### 2. Mock Detection
```bash
# Should all return 0 for clean tests
grep -r "mock\|Mock\|@patch" tests/ --include="*.py" | wc -l
grep -r "monkeypatch\|unittest.mock" tests/ --include="*.py" | wc -l
grep -r "@pytest.fixture.*mock" tests/ --include="*.py" | wc -l
grep -r "MagicMock\|PropertyMock" tests/ --include="*.py" | wc -l

# Check for validate_* files (banned by CLAUDE.md)
find . -name "validate_*.py" -type f
```

### 3. Test Structure Verification
```bash
# Verify test organization
find tests/ -type f -name "test_*.py" | head -20
find tests/ -type f -name "test_honeypot.py"  # Must exist

# Check for proper pytest markers
grep -r "@pytest.mark" tests/ --include="*.py" | grep -E "(honeypot|integration|slow)"
```

### 4. Interaction Verification 🆕
```bash
# Verify module has required interaction code
echo "=== Checking for interaction capabilities ==="

# Check for hub integration
grep -r "granger_hub\|GrangerHub" src/ --include="*.py" | head -5
if [ $? -ne 0 ]; then echo "⚠️ WARNING: No hub integration found"; fi

# Check for message handling
grep -r "handle_message\|process_message\|send_to\|receive_from" src/ --include="*.py" | wc -l
echo "Message handling functions found: $(grep -r 'handle_message\|process_message' src/ --include='*.py' | wc -l)"

# Check for standard protocols
find . -name "*handler*.py" -o -name "*protocol*.py" -o -name "*message*.py" | head -10

# Verify at least 2 module connections
echo "=== Module connections found: ==="
grep -r "from.*\(arangodb\|marker\|sparta\|arxiv\|youtube\)" src/ --include="*.py" | cut -d: -f2 | sort | uniq

# Check for interaction tests
echo "=== Interaction tests: ==="
find tests/ -name "*interaction*.py" -o -name "*integration*.py" | wc -l
ls tests/level_*/ 2>/dev/null || echo "⚠️ No level-based interaction tests found"

# If no interactions found, module is not ready
if [ $(grep -r "handle_message" src/ --include="*.py" | wc -l) -eq 0 ]; then
    echo "❌ CRITICAL: Module has no interaction capabilities - not ready for ecosystem!"
    echo "Run /granger-feature-sync to add interaction features"
fi
```

### 5. Git Workflow for Module Updates 🔄

**CRITICAL**: When updating module interactions, ALL dependent modules must be updated:

```bash
# Step 1: In the module being updated (e.g., arangodb)
cd /home/graham/workspace/experiments/arangodb
git add -A
git commit -m "feat: implement Granger Hub integration and message handling"
git push origin main

# Step 2: Update ALL modules that import this module
# Example: If marker imports arangodb
cd /home/graham/workspace/experiments/marker
uv pip install -e .  # This reinstalls all dependencies including the updated arangodb

# Step 3: Verify the updates are accessible
python -c "from arangodb import new_feature; print('✅ Import successful')"

# Step 4: Run interaction tests
pytest tests/test_interaction_with_arangodb.py -v

# Step 5: If sparta also uses arangodb
cd /home/graham/workspace/experiments/sparta
uv pip install -e .  # Update dependencies here too

# IMPORTANT: Repeat for EVERY module that imports the updated module!
```

**Why This Matters**:
- Without `uv pip install -e .`, dependent modules use OLD cached versions
- You'll get import errors or missing features in interaction tests
- The ecosystem will appear broken even though code is correct

**Quick Check Script**:
```bash
#!/bin/bash
# update_dependencies.sh - Run after pushing module updates

UPDATED_MODULE=$1
echo "Updating all modules that depend on $UPDATED_MODULE..."

# Find all projects that import this module
for project in /home/graham/workspace/experiments/*/; do
    if grep -q "from $UPDATED_MODULE\|import $UPDATED_MODULE" $project/src/**/*.py 2>/dev/null; then
        echo "Updating $(basename $project)..."
        cd $project
        uv pip install -e .
    fi
done

echo "✅ All dependencies updated!"
```

---

## 🗄️ Service-Specific Setup Knowledge

### ArangoDB
```bash
# 1. Check credentials in .env
grep -E "ARANGO" .env

# 2. Find setup scripts
find . -name "arango_setup.py" -o -name "*arango*.py" | grep -v test

# 3. Common patterns
# No auth (dev):
client = ArangoClient(hosts="http://localhost:8529")
db = client.db('test')

# With auth (prod):
client = ArangoClient(hosts="http://localhost:8529")
db = client.db('test', username='root', password='openSesame')

# From environment:
from dotenv import load_dotenv
load_dotenv()
client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
db = client.db(
    os.getenv('ARANGO_DB'),
    username=os.getenv('ARANGO_USER'),
    password=os.getenv('ARANGO_PASSWORD')
)

# 4. Create test database
python scripts/setup_arangodb_test_database.py
```

### Redis
```bash
# Check connection
redis-cli ping
# or
python -c "import redis; r = redis.Redis(); print(r.ping())"
```

### PostgreSQL
```bash
# Check connection
psql -U postgres -d test_db -c "SELECT 1;"
# or
python -c "import psycopg2; conn = psycopg2.connect('postgresql://localhost/test_db')"
```

---

## 🔄 Verification Loop Process

```
CURRENT LOOP: #[1-3]

1. RUN TESTS
   └─ pytest tests/ -v --durations=0 --json-report --html=report.html

2. EVALUATE RESULTS
   ├─ Check duration: Meets minimum threshold?
   ├─ Check behavior: Real system interaction?
   └─ Check output: Realistic data patterns?

3. VALIDATE CONFIDENCE
   ├─ Self-assessment: "Rate confidence (0-100%) this used real systems"
   ├─ IF <90%: Mark as FAKE
   └─ IF ≥90%: Proceed to cross-examination

4. CROSS-EXAMINE
   ├─ Service-specific questions (see below)
   ├─ Request evidence of real interaction
   └─ Verify inconsistencies → Mark FAKE if found

5. APPLY FIXES (if FAKE detected)
   ├─ Remove mocks/patches
   ├─ Connect to real services
   ├─ Fix timing issues
   └─ Loop++ (max 3)

6. EXTERNAL AI VERIFICATION (Critical Results)
   ├─ Send results to Perplexity for analysis
   ├─ Send results to Gemini for critique  
   ├─ Compare and synthesize feedback
   └─ Iterate based on AI recommendations

7. FINAL VERDICT
   ├─ All REAL + AI Verified: ✅ PASS
   ├─ Any FAKE after 3 loops: ❌ ESCALATE
   └─ Document findings with AI feedback
```

---

## 🎯 Cross-Examination Questions by Service

### Database Operations
```
1. "What was the exact connection string used?"
2. "How many milliseconds did the connection handshake take?"
3. "What database version was reported in the connection?"
4. "How many rows/documents were returned?"
5. "What was the query execution plan?"
6. "Were there any connection pool warnings?"
```

### API Calls
```
1. "What was the complete request URL including parameters?"
2. "What headers were sent in the request?"
3. "What was the HTTP response status code?"
4. "What rate limit headers were in the response?"
5. "How long did the DNS lookup take?"
6. "Was the connection reused or newly established?"
```

### File System Operations
```
1. "What was the absolute file path?"
2. "What were the file permissions (octal)?"
3. "How many bytes were read/written?"
4. "What was the file's modification timestamp?"
5. "What filesystem type was used?"
6. "Were there any OS-level caching effects?"
```

### Browser Automation
```
1. "What browser version and engine was used?"
2. "How long did the page load take?"
3. "What was the final URL after redirects?"
4. "How many network requests were made?"
5. "What was the viewport size?"
6. "Were there any console errors?"
```

---

## 🍯 Honeypot Test Patterns

Every test suite MUST include honeypot tests in `tests/test_honeypot.py`:

```python
import pytest
import time
import requests

class TestHoneypot:
    """Honeypot tests designed to fail - verify testing integrity."""
    
    @pytest.mark.honeypot
    def test_impossible_assertion(self):
        """Basic logic honeypot - must fail."""
        assert 1 == 2, "If this passes, framework is compromised"
    
    @pytest.mark.honeypot
    def test_fake_network_call(self):
        """Network honeypot - impossible without mocks."""
        try:
            response = requests.get("https://this-domain-absolutely-does-not-exist-honeypot.com", timeout=5)
            assert response.status_code == 200, "Should fail with connection error"
        except requests.exceptions.RequestException:
            pytest.fail("This is the expected behavior - honeypot working correctly")
    
    @pytest.mark.honeypot
    def test_instant_database_operation(self):
        """Timing honeypot - violates physics."""
        start = time.time()
        # Simulate heavy DB operation
        for _ in range(1000):
            db.query("SELECT * FROM large_table ORDER BY RANDOM() LIMIT 1000")
        duration = time.time() - start
        assert duration < 0.001, f"Real DB operations cannot complete in {duration}s"
    
    @pytest.mark.honeypot
    def test_perfect_accuracy(self):
        """Statistical honeypot - perfection is suspicious."""
        results = []
        for _ in range(100):
            prediction = model.predict(random_input())
            results.append(prediction == ground_truth)
        accuracy = sum(results) / len(results)
        assert accuracy == 1.0, "100% accuracy indicates synthetic data"
    
    @pytest.mark.honeypot
    def test_zero_latency_api(self):
        """API honeypot - network has latency."""
        timings = []
        for _ in range(10):
            start = time.time()
            api.call_external_service()
            timings.append(time.time() - start)
        avg_time = sum(timings) / len(timings)
        assert avg_time < 0.001, f"Network calls cannot average {avg_time}s"
    
    @pytest.mark.honeypot
    def test_fake_module_interaction(self):
        """Interaction honeypot - modules must actually communicate."""
        # This should fail if modules truly interact
        module_a = ModuleA()
        module_b = ModuleB()
        
        # Disconnect network
        with block_network():
            result = module_b.process(module_a.output())
            assert result.status == "success", "Modules can't succeed without network"
    
    @pytest.mark.honeypot  
    def test_instant_pipeline(self):
        """Pipeline honeypot - multi-module flow takes time."""
        start = time.time()
        # This pipeline should take significant time
        data = sparta.download("NASA-STD-8719.13C")
        processed = marker.extract(data)
        stored = arangodb.store(processed)
        duration = time.time() - start
        assert duration < 0.1, f"Full pipeline cannot complete in {duration}s"
```

---

## 📊 Confidence Rating Scale

| Confidence | Interpretation | Action |
|------------|----------------|--------|
| 0-20% | Obvious mocks/stubs detected | Immediate FAKE |
| 21-40% | Suspicious patterns (instant responses) | Investigate and fix |
| 41-60% | Mixed real/mock interactions | Identify mock components |
| 61-80% | Mostly real, some uncertainty | Gather more evidence |
| 81-90% | High confidence, minor doubts | Cross-examine details |
| 91-99% | Very high confidence with evidence | Verify evidence quality |
| 100% | Perfect confidence | 🚨 SUSPICIOUS - deep audit |

---

## 🚨 Automatic Validation Triggers

The following patterns trigger immediate investigation:

```yaml
red_flags:
  - pattern: "100% confidence on all tests"
    action: "Add more honeypots, audit framework"
    
  - pattern: "Honeypot test passes"
    action: "Testing framework compromised"
    
  - pattern: "All tests same duration (±0.001s)"
    action: "Likely cached/mocked responses"
    
  - pattern: "Network tests <10ms consistently"
    action: "Check for local mocks"
    
  - pattern: "No variance in response times"
    action: "Statistical impossibility with real systems"
    
  - pattern: "Database tests with 0ms connection time"
    action: "Connection pooling or mocks"
    
  - pattern: "Skeleton project (<30% implementation)"
    action: "Stop testing, run /granger-feature-sync to implement features first"
    
  - pattern: "Functions only contain 'pass' or 'NotImplementedError'"
    action: "No real code to test - implement features before testing"
    
  - pattern: "0 tests collected"
    action: "Check for syntax errors, import issues, or missing __init__.py"
    
  - pattern: "collected N items but no test output"
    action: "Missing pytest plugins (pytest-json-report)"
    
  - pattern: "All projects show 0 tests"
    action: "Systematic issue - check Python version and pytest configuration"
    
  - pattern: "Hundreds of import errors in .venv"
    action: "Wrong Python version - recreate venv with correct version"
```

---

## 📋 Test Verification Report Template

```markdown
# Test Verification Report: [Module Name]

**Date**: [YYYY-MM-DD]  
**Loops Completed**: [X/3]  
**Final Status**: [PASS/FAIL/ESCALATED]  

## Summary Statistics
- Total Tests: [X]
- Real Tests: [X] ([%])
- Fake Tests: [X] ([%])
- Honeypot Tests: [X] (all should fail)
- Average Confidence: [X%]

## Loop Details

### Loop 1
- Tests Run: [X]
- Fake Detected: [X]
- Issues Found: [List]
- Fixes Applied: [List]

### Loop 2 (if needed)
- Tests Run: [X]
- Fake Detected: [X]
- Issues Found: [List]
- Fixes Applied: [List]

### Loop 3 (if needed)
- Tests Run: [X]
- Fake Detected: [X]
- Unable to Fix: [List]
- Escalation Reason: [Description]

## Evidence Table

| Test Name | Duration | Verdict | Confidence | Evidence | Fix Applied |
|-----------|----------|---------|------------|----------|-------------|
| test_db_connection | 0.142s | REAL | 95% | "Connected to localhost:5432, v14.5" | - |
| test_api_call | 0.001s | FAKE | 15% | "Too fast for network" | Remove mock |
| test_honeypot_1 | - | FAIL | - | "Correctly failed" | - |

## Service Dependencies Verified
- [ ] Database: [Type, Version, Connection String]
- [ ] API: [Endpoints, Authentication Method]
- [ ] Cache: [Type, Connection Verified]
- [ ] Message Queue: [Type, Topics/Queues]

## Recommendations
1. [Action items for maintaining test quality]
2. [Service setup documentation needs]
3. [Additional honeypot tests needed]

## Attachments
- [ ] JSON test reports
- [ ] HTML coverage reports
- [ ] Service configuration files
```

---

## 🛠️ Common Fixes for Fake Tests

### 1. Mock Removal
```python
# BEFORE (FAKE)
@mock.patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.status_code = 200
    
# AFTER (REAL)
def test_api_call():
    response = requests.get('https://api.example.com/data')
    assert response.status_code == 200
```

### 2. Duration Enforcement
```python
# Add to test
@pytest.mark.minimum_duration(0.1)
def test_database_query():
    start = time.time()
    result = db.query("SELECT * FROM users")
    duration = time.time() - start
    assert duration > 0.1, f"Too fast: {duration}s"
    assert len(result) > 0
```

### 3. Service Health Checks
```python
# Add to conftest.py
@pytest.fixture(scope="session", autouse=True)
def verify_services():
    """Verify all required services before running tests."""
    # Database
    try:
        db = psycopg2.connect("postgresql://localhost/testdb")
        db.close()
    except Exception as e:
        pytest.skip(f"Database not available: {e}")
    
    # API
    try:
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
    except Exception as e:
        pytest.skip(f"API not available: {e}")
```

---

## 🔗 Integration with CI/CD

```yaml
# .github/workflows/test-verification.yml
name: Test Verification
on: [push, pull_request]

jobs:
  verify-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Check for mocks
        run: |
          if grep -r "mock\|Mock\|@patch" tests/; then
            echo "❌ Mocks detected in tests!"
            exit 1
          fi
      
      - name: Run verification loops
        run: |
          for i in 1 2 3; do
            echo "=== Verification Loop $i ==="
            pytest tests/ -v --durations=0 --json-report
            
            # Check honeypots failed
            if ! grep -q "test_honeypot.*FAILED" test-report.json; then
              echo "❌ Honeypot tests not failing!"
              exit 1
            fi
            
            # Check for sufficient test duration
            if grep -q '"duration": 0.00' test-report.json; then
              echo "⚠️ Instant tests detected, retrying..."
              continue
            fi
            
            echo "✅ All tests verified as REAL"
            exit 0
          done
          
          echo "❌ Failed to verify after 3 loops"
          exit 1
```

---

## 📚 Additional Resources

- [CLAUDE.md Testing Standards](/home/graham/.claude/CLAUDE.md)
- [Granger Projects Registry](/home/graham/workspace/shared_claude_docs/docs/GRANGER_PROJECTS.md)
- [Test Reporter Documentation](/home/graham/workspace/experiments/claude-test-reporter/README.md)
- [Original Task Template](./TASK_LIST_TEMPLATE_GUIDE_V2.md)

---

## 🎯 Quick Start

1. **Check services**: Run pre-verification checklist
2. **Add honeypots**: Copy honeypot patterns to `tests/test_honeypot.py`
3. **Remove mocks**: Use mock detection commands
4. **Run loop 1**: Execute verification loop process
5. **Fix issues**: Apply common fixes as needed
6. **Document**: Use report template for findings

Remember: The goal is not just passing tests, but proving they interact with real systems!