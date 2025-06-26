# Lessons Learned from Granger Ecosystem Restoration

## Key Insights to Add to TEST_VERIFICATION_TEMPLATE_GUIDE.md

### 1. **Check Project Structure and Dependencies FIRST**
```bash
# CRITICAL: Before any testing, understand the project
cat pyproject.toml | grep -E "(name|version|dependencies|python)"
ls -la src/
find . -name "*.py" -path "*/tests/*" | wc -l
```

**Why**: I wasted time not checking that projects were using Python 3.12 when they needed 3.10.11. Always verify Python version requirements first.

### 2. **Service-Specific Setup Knowledge**
Add section for ArangoDB specifically:
```bash
# ArangoDB Test Setup
# 1. Check existing .env for credentials
grep -E "ARANGO_|ARANGODB_" .env

# 2. Look for arango_setup.py files
find . -name "arango_setup.py" -o -name "*arango*.py" | grep -v test

# 3. Create test database using credentials from .env
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print(f'Host: {os.getenv(\"ARANGO_HOST\")}')
print(f'User: {os.getenv(\"ARANGO_USER\")}') 
print(f'Pass: {os.getenv(\"ARANGO_PASSWORD\")}')
print(f'Test DB: {os.getenv(\"ARANGO_TEST_DB_NAME\")}')
"
```

### 3. **Test Output Verification**
Add warning signs that tests aren't really running:
```yaml
red_flags:
  - pattern: "0 tests collected"
    action: "Check for syntax errors, import issues, or missing __init__.py"
    
  - pattern: "collected N items" but no output
    action: "Missing pytest plugins (pytest-json-report)"
    
  - pattern: "All projects show 0 tests"
    action: "Systematic issue - check pytest configuration"
```

### 4. **Dependency Hell Solutions**
New section on fixing cascading dependency issues:
```bash
# When you see hundreds of import errors in site-packages
# Example: __future__ imports not at top of file

# 1. Identify the pattern
find .venv -name "*.py" -exec grep -l "from __future__" {} \; | wc -l

# 2. Create targeted fix script instead of manual editing
# 3. Fix at source (use correct Python version) not symptoms
```

### 5. **Real Service Authentication Patterns**
```python
# Pattern 1: No auth (development)
client = ArangoClient(hosts="http://localhost:8529")
db = client.db('test')

# Pattern 2: With auth (production)
client = ArangoClient(hosts="http://localhost:8529")
db = client.db('test', username='root', password='openSesame')

# Pattern 3: From environment
client = ArangoClient(hosts=os.getenv('ARANGO_HOST'))
db = client.db(
    os.getenv('ARANGO_DB'),
    username=os.getenv('ARANGO_USER'),
    password=os.getenv('ARANGO_PASSWORD')
)
```

## Key Insights to Add to TASK_LIST_TEMPLATE_GUIDE_V2.md

### 1. **Project Health Check BEFORE Task Creation**
Add new pre-task section:
```markdown
## 🏥 Project Health Check (Run BEFORE Creating Tasks)

### Python Version Check
```bash
# Check all projects use same Python version
for proj in /path/to/projects/*/; do
    echo -n "$(basename $proj): "
    grep python $proj/pyproject.toml | grep -v python- | head -1
done
```

### Service Availability Check
```bash
# Check all required services
curl -s http://localhost:8529/_api/version  # ArangoDB
curl -s http://localhost:8000/health        # GrangerHub
docker ps | grep -E "(arango|redis|postgres)"
```

### Test Infrastructure Check
```bash
# Verify pytest works in a project
cd project && python -m pytest --collect-only
```
```

### 2. **Task Ordering Based on Infrastructure**
Add guidance on task prioritization:
```markdown
### Task Priority Order
1. **Infrastructure Tasks** (Python version, service setup)
2. **Individual Project Tests** (get each project working)
3. **Level 0 Integration** (basic cross-module)
4. **Level 1-4 Integration** (complex workflows)

Never attempt integration tests until individual projects pass!
```

### 3. **Tracking Fixes Across Projects**
New section for managing multi-project fixes:
```markdown
### Cross-Project Fix Tracking
When fixing systematic issues (e.g., Python version):

| Fix Type | Projects Affected | Script Created | Status |
|----------|------------------|----------------|---------|
| Python 3.10.11 | ALL (20/20) | fix_python_versions.sh | ✅ |
| pytest-json-report | 15/20 | install_pytest_plugins.sh | ✅ |
| __future__ imports | marker dependencies | fix_future_imports.py | ✅ |
```

### 4. **Test Result Skepticism**
Enhance the evaluation section:
```markdown
### Skeptical Test Evaluation
⚠️ **"Passing" tests may be lying!**

Check for these patterns:
1. **Too Fast**: Operations < 0.001s are suspicious
2. **Too Consistent**: Same duration every run = cached/mocked
3. **No Failures**: 100% pass rate across all projects = broken tests
4. **No Output**: Tests that produce no stdout/stderr = not running

Real tests have:
- Variable execution times
- Occasional warnings/deprecations
- Some failures (especially honeypots)
- Actual output (logs, print statements)
```

### 5. **Service-Specific Task Templates**
Add templates for common services:
```markdown
## 🎯 TASK #0XX: ArangoDB Integration Test

**Special Considerations**:
- [ ] Check .env for ARANGO_* variables
- [ ] Look for arango_setup.py in project
- [ ] Create test database: `{name}_test`
- [ ] Use credentials from .env, not hardcoded
- [ ] Clean up test database after tests

**Common Issues**:
- Authentication errors → Check if Docker container has auth enabled
- Empty test DB → Run setup script or create collections
- Import errors → Install python-arango with uv
```

### 6. **Batch Operations for Efficiency**
```markdown
### Batch Fix Scripts
For systematic issues affecting multiple projects:

1. **Diagnose Pattern**
   ```bash
   # Example: Find all projects with wrong Python version
   for p in */pyproject.toml; do
       grep -H "python.*3.12" $p
   done
   ```

2. **Create Fix Script**
   ```python
   # fix_all_projects.py
   for project in projects:
       fix_issue(project)
       verify_fix(project)
   ```

3. **Track Application**
   - [ ] Script created
   - [ ] Tested on 1 project
   - [ ] Applied to all projects
   - [ ] Verified results
```

## Summary of Critical Lessons

1. **Always check basics first**: Python version, service availability, .env files
2. **Read existing code**: Look for setup scripts (arango_setup.py), configuration patterns
3. **Fix root causes**: Don't patch symptoms (like import errors) - fix the source
4. **Batch similar fixes**: Create scripts for systematic issues
5. **Verify with skepticism**: "Passing" tests often aren't really running
6. **Track cross-project dependencies**: One change may require updates in many places
7. **Use real service credentials**: Check .env files and existing setup patterns
8. **Archive broken tests**: Don't waste time fixing deprecated code

These lessons would have saved ~3 hours of debugging time!