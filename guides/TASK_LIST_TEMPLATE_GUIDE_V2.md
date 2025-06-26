# Master Task List - [Project Name]

**Total Tasks**: [Number, e.g., 10]  
**Completed**: [Number, e.g., 0/10]  
**Active Tasks**: [List task IDs, e.g., #001 (Primary), #002 (Blocked)]  
**Last Updated**: [YYYY-MM-DD HH:MM EDT, e.g., 2025-05-28 15:43 EDT]  

## 🏥 Project Health Check (Run BEFORE Creating Tasks)

### Python Version Check
```bash
# Check Python version requirement
cat pyproject.toml | grep -E "python.*=" | grep -v python-
# CRITICAL: If mismatch with your environment, fix this FIRST!

# Check all related projects use same version
for proj in /home/graham/workspace/experiments/*/; do
    echo -n "$(basename $proj): "
    grep python $proj/pyproject.toml 2>/dev/null | grep -v python- | head -1
done
```

### Service Availability Check
```bash
# Check all required services are running
curl -s http://localhost:8529/_api/version || echo "❌ ArangoDB not running"
curl -s http://localhost:8000/health || echo "❌ GrangerHub not running"
docker ps | grep -E "(arango|redis|postgres)" || echo "❌ No database containers"
```

### Test Infrastructure Check
```bash
# Verify pytest can collect tests
cd project && python -m pytest --collect-only 2>&1 | grep -E "(collected|error)"
# If "0 collected" or errors, fix infrastructure before creating test tasks
```

### Existing Configuration Check
```bash
# Look for setup patterns and credentials
find . -name "*setup*.py" -o -name "*config*.py" | grep -v test
if [ -f .env ]; then
    echo "=== Available credentials ==="
    grep -E "(ARANGO|REDIS|POSTGRES|API)" .env | cut -d= -f1
fi
```

⚠️ **SKELETON PROJECT WARNING**: If this project has <30% real implementation, prioritize implementing core features BEFORE extensive testing. Run `/granger-feature-sync` to detect skeleton status and generate implementation tasks.

🚫 **NO SIMULATIONS ALLOWED**: When testing module interactions, NEVER simulate functionality. However, BE PROACTIVE with import failures:
- **Import errors**: Fix immediately with `uv add package` → `uv pip install -e .`
- **Connection errors**: These ARE valuable test results (after imports work)
- **Past lesson**: 3 previous attempts failed by treating import errors as bugs instead of setup issues

🔌 **INTERACTION TESTING CRITICAL**: Project interactions are CRUCIAL tests that MUST pass. Every module MUST demonstrate real communication with other Granger components. Use `/ask-perplexity` to research optimal interaction patterns based on:
- Project README.md and codebase analysis
- @docs/GRANGER_PROJECTS.md for ecosystem architecture
- ~/.claude/commands for available integration patterns
- Existing interaction implementations in other modules

🔄 **GIT WORKFLOW REQUIREMENTS**: After implementing interaction features:
1. **Commit and Push**: Stage, commit, and push changes to the module's repo
2. **Update Dependencies**: In EVERY module that imports this one, run `uv pip install -e .`
3. **Verify Updates**: Test imports work: `python -c "from module import feature"`
4. **Run Tests**: Execute interaction tests to confirm modules work together
5. **Document**: Update task status only after ALL dependent modules are updated

---

## 🚨 MANDATORY: Fix Import Errors IMMEDIATELY!

**THIS IS NOT OPTIONAL - Past attempts failed because people skipped this!**

### When You See ANY Import Error - STOP AND FIX IT NOW!

```bash
# WRONG APPROACH (what failed 3 times before):
# ❌ "ModuleNotFoundError: requests" → "Oh, that's a bug in the module"
# ❌ "ImportError: cannot import X" → "I'll report this as a finding"
# ❌ "0 tests collected" → "The test suite is broken"

# CORRECT APPROACH (what you MUST do):
# ✅ "ModuleNotFoundError: requests" → uv add requests && uv pip install -e .
# ✅ "ImportError: cannot import X" → uv pip install -e . (reinstall)
# ✅ "0 tests collected" → pytest --collect-only -v (see errors) → fix each one
```

## 🔧 Proactive Troubleshooting (DO THIS FIRST!)

### Import Error Quick Fixes
```bash
# The #1 reason past bug hunts failed: treating these as bugs instead of fixing them!

# Pattern: ModuleNotFoundError: No module named 'X'
cd /project/path
uv add X
uv pip install -e .

# Pattern: ImportError: cannot import name 'Y' from 'X'
uv pip install -e .  # Stale installation
# Still fails? Check recent commits for API changes

# Pattern: pytest collects 0 tests
pytest --collect-only -v  # See the actual errors
# Fix each ModuleNotFoundError with uv add

# Pattern: "No module named 'src.module_name'"
# Wrong: Report as bug
# Right: Ensure PYTHONPATH includes ./src
export PYTHONPATH=./src:$PYTHONPATH
```

### Module-Specific Dependencies
```bash
# Save time - here are the common ones:
sparta:     uv add requests beautifulsoup4 lxml pyyaml
marker:     uv add pdftext pymupdf4llm pillow pypdf
arangodb:   uv add python-arango
arxiv:      uv add arxiv tree-sitter tree-sitter-language-pack
youtube:    uv add youtube-transcript-api yt-dlp
llm_call:   uv add litellm openai anthropic
unsloth:    uv add unsloth transformers torch
```

### Post-Fix Verification
```bash
# After fixing imports, verify the module works:
python -c "import module_name; print('✅ Import successful')"

# Update all dependent modules (CRITICAL!):
for dep in $(grep -l "import module_name" /workspace/*/src/**/*.py); do
    cd $(dirname $dep)/../.. && uv pip install -e .
done
```

### Import Error Decision Tree
```
Encounter Import Error
        ↓
Is it ModuleNotFoundError?
    ├─ YES → Run: uv add [module] && uv pip install -e .
    └─ NO → Is it ImportError?
            ├─ YES → Run: uv pip install -e .
            └─ NO → Check PYTHONPATH and file structure
        ↓
Did fix work?
    ├─ YES → Continue testing ✅
    └─ NO → Check pyproject.toml dependencies
            → Try: uv add [module]==specific_version
            → Still fails? Check module docs for dependencies
        ↓
NEVER report import errors as bugs!
They are ALWAYS fixable setup issues!
```

---

## 📋 Task Priority Guidelines

### Correct Task Order (CRITICAL)
1. **Infrastructure Tasks** - Fix Python versions, install dependencies, start services
2. **Individual Project Tests** - Get each project's tests passing independently  
3. **Level 0 Integration** - Basic cross-module communication tests
4. **Level 1-4 Integration** - Complex multi-module workflows

⚠️ **NEVER attempt integration tests until ALL individual projects pass their tests!**

### Cross-Project Fix Tracking
When fixing systematic issues across multiple projects:

| Fix Type | Projects Affected | Script/Command | Status |
|----------|------------------|----------------|---------|
| Python 3.10.11 upgrade | ALL (20/20) | `cd proj && uv venv --python=3.10.11` | [ ] |
| Install pytest-json-report | Projects with tests | `uv pip install pytest-json-report` | [ ] |
| Fix __future__ imports | marker dependencies | `python fix_future_imports.py` | [ ] |
| Start required services | All integration tests | `docker start arangodb` | [ ] |

### Batch Operations Template
```bash
#!/bin/bash
# fix_all_projects.sh - Apply same fix to multiple projects

PROJECTS="sparta marker arangodb youtube_transcripts llm_call"
FIX_COMMAND="uv pip install pytest-json-report"

for proj in $PROJECTS; do
    echo "Fixing $proj..."
    cd /home/graham/workspace/experiments/$proj
    eval $FIX_COMMAND
    echo "✅ $proj fixed"
done
```

---

## 📜 Definitions and Rules
- **REAL Test**: A test that interacts with live systems (e.g., real database, API) and meets minimum performance criteria (e.g., duration > 0.1s for DB operations).  
- **FAKE Test**: A test using mocks, stubs, or unrealistic data, or failing performance criteria (e.g., duration < 0.05s for DB operations).  
- **Skeleton Project**: A project with <30% real implementation, mostly containing placeholder code (pass statements, NotImplementedError, TODO markers).
- **Confidence Threshold**: Tests with <90% confidence are automatically marked FAKE.
- **Status Indicators**:  
  - ✅ Complete: All tests passed as REAL, verified in final loop.  
  - ⏳ In Progress: Actively running test loops.  
  - 🚫 Blocked: Waiting for dependencies (listed).  
  - 🔄 Not Started: No tests run yet.  
- **Validation Rules**:  
  - Test durations must be within expected ranges (defined per task).  
  - Tests must produce JSON and HTML reports with no errors.  
  - Self-reported confidence must be ≥90% with supporting evidence.
  - Maximum 3 test loops per task; escalate failures to [contact/project lead].  
- **Environment Setup**:  
  - Python 3.9+, pytest 7.4+, sparta-cli 2.0+  
  - [System-specific requirements, e.g., ArangoDB v3.10, credentials in `.env`]  
  - [API-specific requirements, e.g., YouTube API key in `config.yaml`]  

---

## 🎯 TASK #001: [Task Name]

**Status**: 🔄 Not Started  
**Dependencies**: [List task IDs or None]  
**Expected Test Duration**: [Range, e.g., 0.1s–5.0s]  

### Implementation
- [ ] **PRE-CHECK**: Verify this is not a skeleton project (>30% real implementation)
- [ ] **INTERACTION-CHECK**: Module can communicate with at least 2 other modules
- [ ] **HUB-INTEGRATION**: Module registers with and responds to Granger Hub
- [ ] **MESSAGE-FORMAT**: Implements standard Granger message format
- [ ] **ERROR-PROPAGATION**: Can receive and forward errors from other modules
- [ ] [Requirement 1, specify live systems, no mocks]  
- [ ] [Requirement 2, include validation data, e.g., `data/ground_truth.json`]  
- [ ] [Requirement 3]  

### Post-Implementation Git Workflow
- [ ] **STAGE**: `git add -A` (include all new interaction files)
- [ ] **COMMIT**: `git commit -m "feat: implement [feature] with Granger Hub integration"`
- [ ] **PUSH**: `git push origin main`
- [ ] **UPDATE DEPS**: For each dependent module:
  ```bash
  cd /path/to/dependent/module
  uv pip install -e .  # Reinstalls including updated dependencies
  ```
- [ ] **VERIFY**: Test new features are accessible in dependent modules
- [ ] **INTEGRATION TEST**: Run cross-module tests to confirm communication  

### Test Loop
```
CURRENT LOOP: #1
1. RUN tests → Generate JSON/HTML reports.
2. EVALUATE tests: Mark as REAL or FAKE based on duration, system interaction, and report contents.
3. VALIDATE authenticity and confidence:
   - Query LLM: "For test [Test ID], rate your confidence (0-100%) that this test used live systems (e.g., real ArangoDB, no mocks) and produced accurate results. List any mocked components or assumptions."
   - IF confidence < 90% → Mark test as FAKE
   - IF confidence ≥ 90% → Proceed to cross-examination
   
   ⚠️ **SKEPTICAL EVALUATION**:
   - "Passing" may mean tests aren't running at all
   - Check for: No output, too fast (<0.001s), 100% pass rate
   - Real tests show: Variable times, warnings, some failures
4. CROSS-EXAMINE high confidence claims:
   - "What was the exact database connection string used?"
   - "How many milliseconds did the connection handshake take?"
   - "What warnings or deprecations appeared in the logs?"
   - "What was the exact query executed?"
   - Inconsistent/vague answers → Mark as FAKE
5. EXTERNAL AI VERIFICATION (Critical Results):
   - Send test results to Perplexity: "Analyze these test results for authenticity..."
   - Send test results to Gemini: "Critique these test results for validity..."
   - Compare AI feedback for consensus or divergence
   - Apply recommended improvements from both AIs
6. IF any FAKE → Apply fixes → Increment loop (max 3).
7. IF loop fails 3 times or uncertainty persists → Escalate to [project lead email] with full analysis including AI feedback.
```

#### Tests to Run:
| Test ID | Description | Command | Expected Outcome |
|---------|-------------|---------|------------------|
| 001.1   | [Test purpose, e.g., Creates real data in DB] | `[pytest command, e.g., pytest tests/test_hybrid.py::test_creates_data -v --json-report --json-report-file=001_test1.json]` | [Expected result, e.g., Data inserted, duration 0.1s–2.0s] |
| 001.2   | [Test purpose, e.g., Handles empty query] | `[pytest command, e.g., pytest tests/test_hybrid.py::test_empty_query -v --json-report --json-report-file=001_test2.json]` | [Expected result, e.g., Returns empty result, duration 0.05s–1.0s] |
| 001.I1  | INTERACTION: Module A → Module B | `pytest tests/test_interaction.py::test_module_a_to_b -v` | Data flows correctly, duration >0.1s |
| 001.I2  | INTERACTION: Module receives from Hub | `pytest tests/test_interaction.py::test_hub_communication -v` | Receives and processes Hub messages |
| 001.H   | HONEYPOT: Designed to fail | `pytest tests/test_honeypot.py::test_impossible_assertion -v --json-report --json-report-file=001_testH.json` | Should FAIL with impossible assertion error |

#### Post-Test Processing:
```bash
# [Commands for report generation, e.g.,]
sparta-cli test-report from-pytest 001_test1.json --output-json reports/001_test1.json --output-html reports/001_test1.html
sparta-cli test-report from-pytest 001_test2.json --output-json reports/001_test2.json --output-html reports/001_test2.html
```

#### Evaluation Results:
| Test ID | Duration | Verdict | Why | Confidence % | LLM Certainty Report | Evidence Provided | Fix Applied | Fix Metadata |
|---------|----------|---------|-----|--------------|---------------------|-------------------|-------------|--------------|
| 001.1   | [e.g., 0.001s] | [REAL/FAKE] | [Reason] | [e.g., 45%] | [LLM response] | [e.g., "Connection: arango://192.168.1.10:8529, handshake: 47ms"] | [Fix] | [Metadata] |
| 001.2   | [e.g., 0.15s]  | [REAL/FAKE] | [Reason] | [e.g., 95%] | [LLM response] | [Evidence] | [None or fix] | [Metadata or -] |
| 001.H   | [duration] | [Should be FAIL] | [Reason] | [%] | [If claims success, all results suspect] | [Evidence] | [-] | [-] |

**Task #001 Complete**: [ ]  

---

## 📊 Overall Progress

### By Status:
- ✅ Complete: [Number, e.g., 0] ([List task IDs])  
- ⏳ In Progress: [Number, e.g., 1] ([List task IDs])  
- 🚫 Blocked: [Number, e.g., 0] ([List task IDs])  
- 🔄 Not Started: [Number, e.g., 9] ([List task IDs])  

### Self-Reporting Patterns:
- Always Certain (≥95%): [Number] tasks ([List task IDs]) ⚠️ Suspicious if >3
- Mixed Certainty (50-94%): [Number] tasks ([List task IDs]) ✓ Realistic  
- Always Uncertain (<50%): [Number] tasks ([List task IDs])
- Average Confidence: [Overall %]
- Honeypot Detection Rate: [Number passed]/[Number total] (Should be 0%)
- Skeleton Projects Detected: [Number] projects ⚠️ Implement features before testing

### Dependency Graph:
```
[List dependencies, e.g.,]
#001 → #002
#003 (Independent)
#004 (Independent)
```

### Critical Issues:
1. [Issue, e.g., Task #001: Mock DB connections detected (Fixed in Loop #2, 2025-05-28)]  
2. [Issue, e.g., Task #002: Blocked by #001 (Pending)]  
3. [Issue, e.g., Task #003: Failed honeypot test - results under review]  

### Certainty Validation Check:
```
⚠️ AUTOMATIC VALIDATION TRIGGERED if:
- Any task shows 100% confidence on ALL tests
- Honeypot test passes when it should fail
- Pattern of always-high confidence without evidence
- Project has <30% real implementation (skeleton project)
- Functions mostly contain 'pass' or 'raise NotImplementedError'

Action: 
- For skeleton projects: Run /granger-feature-sync --implement first
- For test issues: Insert additional honeypot tests and escalate to human review
```

### Next Actions:
1. [Action, e.g., Run Task #001 Loop #2 by 2025-05-29]  
2. [Action, e.g., Investigate suspicious confidence patterns in Task #003]  
3. [Action, e.g., Unblock Task #002 upon #001 completion]  

---

## 🛠️ Service-Specific Task Templates

### ArangoDB Integration Task
```markdown
## 🎯 TASK #0XX: ArangoDB [Operation] Test

**Status**: 🔄 Not Started  
**Dependencies**: Service running on :8529  
**Expected Test Duration**: 0.1s–2.0s (connection + query time)

### Pre-Implementation Checks
- [ ] Check .env for ARANGO_* variables
- [ ] Look for arango_setup.py: `find . -name "*arango*setup*.py"`
- [ ] Verify credentials: `grep ARANGO .env`
- [ ] Test connection: `curl http://localhost:8529/_api/version`

### Implementation
- [ ] Use credentials from .env (not hardcoded)
- [ ] Create test database with suffix `_test`
- [ ] Handle both auth and no-auth scenarios
- [ ] Clean up test data in teardown
```

### API Integration Task
```markdown
## 🎯 TASK #0XX: [Service] API Integration

**Status**: 🔄 Not Started  
**Dependencies**: API key in .env  
**Expected Test Duration**: 0.5s–10.0s (network latency)

### Pre-Implementation Checks
- [ ] Check .env for API_KEY
- [ ] Verify endpoint accessibility
- [ ] Check rate limits in API docs
- [ ] Look for existing client code
```

## 📋 Task Template (Copy for New Tasks)

```markdown
## 🎯 TASK #00X: [Name]

**Status**: 🔄 Not Started  
**Dependencies**: [List task IDs or None]  
**Expected Test Duration**: [Range, e.g., 0.1s–5.0s]  

### Pre-Task Import Check (MANDATORY - DO NOT SKIP!)
```bash
# Run this BEFORE starting ANY task work:
cd /path/to/module
python -c "import module_name" || {
    echo "🔧 Fixing imports FIRST..."
    uv pip install -e .
    # Still fails? Check and add dependencies:
    cat pyproject.toml | grep dependencies -A 10
    # Add any missing: uv add package_name
}
```

### Implementation
- [ ] **IMPORT-CHECK**: All module imports work (fixed if needed)
- [ ] **PRE-CHECK**: Verify this is not a skeleton project (>30% real implementation)
- [ ] **INTERACTION-CHECK**: Module can communicate with at least 2 other modules
- [ ] **HUB-INTEGRATION**: Module registers with and responds to Granger Hub
- [ ] **MESSAGE-FORMAT**: Implements standard Granger message format
- [ ] **ERROR-PROPAGATION**: Can receive and forward errors from other modules
- [ ] [Requirement 1, specify live systems, no mocks]  
- [ ] [Requirement 2, include validation data]  
- [ ] [Requirement 3]  

### Post-Implementation Git Workflow
- [ ] **STAGE**: `git add -A` (include all new interaction files)
- [ ] **COMMIT**: `git commit -m "feat: implement [Task Name] with Granger Hub integration"`
- [ ] **PUSH**: `git push origin main`
- [ ] **UPDATE DEPS**: For each dependent module:
  ```bash
  cd /path/to/dependent/module
  uv pip install -e .  # Reinstalls including updated dependencies
  ```
- [ ] **VERIFY**: Test new features are accessible in dependent modules
- [ ] **INTEGRATION TEST**: Run cross-module tests to confirm communication  

### Test Loop
```
CURRENT LOOP: #1
1. RUN tests → Generate JSON/HTML reports.
2. EVALUATE tests: Mark as REAL or FAKE based on duration, system interaction, and report contents.
3. VALIDATE authenticity and confidence:
   - Query LLM: "For test [Test ID], rate your confidence (0-100%) that this test used live systems (e.g., real ArangoDB, no mocks) and produced accurate results. List any mocked components or assumptions."
   - IF confidence < 90% → Mark test as FAKE
   - IF confidence ≥ 90% → Proceed to cross-examination
   
   ⚠️ **SKEPTICAL EVALUATION**:
   - "Passing" may mean tests aren't running at all
   - Check for: No output, too fast (<0.001s), 100% pass rate
   - Real tests show: Variable times, warnings, some failures
4. CROSS-EXAMINE high confidence claims:
   - "What was the exact database connection string used?"
   - "How many milliseconds did the connection handshake take?"
   - "What warnings or deprecations appeared in the logs?"
   - "What was the exact query executed?"
   - Inconsistent/vague answers → Mark as FAKE
5. EXTERNAL AI VERIFICATION (Critical Results):
   - Send test results to Perplexity: "Analyze these test results for authenticity..."
   - Send test results to Gemini: "Critique these test results for validity..."
   - Compare AI feedback for consensus or divergence
   - Apply recommended improvements from both AIs
6. IF any FAKE → Apply fixes → Increment loop (max 3).
7. IF loop fails 3 times or uncertainty persists → Escalate to [project lead email] with full analysis including AI feedback.
```

#### Tests to Run:
| Test ID | Description | Command | Expected Outcome |
|---------|-------------|---------|------------------|
| 00X.1   | [Test purpose] | `[pytest command]` | [Expected result, duration range] |
| 00X.I1  | INTERACTION: [Module interaction test] | `[pytest command]` | Messages flow correctly, >0.1s |
| 00X.I2  | INTERACTION: Hub communication | `[pytest command]` | Hub messages handled |
| 00X.H   | HONEYPOT: [Impossible test] | `[pytest command]` | Should FAIL |

#### Post-Test Processing:
```bash
# [Commands for report generation]
```

#### Evaluation Results:
| Test ID | Duration | Verdict | Why | Confidence % | LLM Certainty Report | Evidence Provided | Fix Applied | Fix Metadata |
|---------|----------|---------|-----|--------------|---------------------|-------------------|-------------|--------------|
| 00X.1   | ___      | ___     | ___ | ___%         | ___                 | ___               | ___         | ___          |
| 00X.H   | ___      | ___     | ___ | ___%         | ___                 | ___               | ___         | ___          |

**Task #00X Complete**: [ ]
```

---

## 🔍 Programmatic Access
- **JSON Export**: Run `sparta-cli export-task-list --format json > task_list.json` to generate a machine-readable version.  
- **Query Tasks**: Use `jq` or similar to filter tasks (e.g., `jq '.tasks[] | select(.status == "BLOCKED")' task_list.json`).  
- **Fake Test Detection**: Filter evaluation results for `"Verdict": "FAKE"`, `"Confidence %" < 90`, or honeypot passes.
- **Suspicious Pattern Detection**: `jq '.tasks[] | select(.average_confidence > 95 and .honeypot_failed == false)'`

---

## 🔄 Dependency Update Helper Scripts

### Auto-Update Dependencies Script
Save as `update_module_deps.sh`:
```bash
#!/bin/bash
# Usage: ./update_module_deps.sh <module_name>
# Example: ./update_module_deps.sh arangodb

MODULE=$1
if [ -z "$MODULE" ]; then
    echo "Usage: $0 <module_name>"
    exit 1
fi

echo "🔄 Finding all modules that depend on $MODULE..."

# Get all Granger projects
PROJECTS_DIR="/home/graham/workspace/experiments"

for project_dir in $PROJECTS_DIR/*/; do
    project_name=$(basename "$project_dir")
    
    # Skip the module itself
    if [ "$project_name" == "$MODULE" ]; then
        continue
    fi
    
    # Check if this project imports the module
    if grep -r "from $MODULE\|import $MODULE" "$project_dir/src" 2>/dev/null | grep -q .; then
        echo ""
        echo "📦 Updating $project_name..."
        cd "$project_dir"
        
        # Pull latest changes
        git pull
        
        # Update dependencies
        uv pip install -e .
        
        # Verify the update
        if python -c "import $MODULE" 2>/dev/null; then
            echo "✅ $project_name updated successfully"
        else
            echo "❌ Failed to update $project_name"
        fi
    fi
done

echo ""
echo "✅ Dependency updates complete!"
```

### Check Module Dependencies Script
Save as `check_module_deps.sh`:
```bash
#!/bin/bash
# Shows which modules depend on a given module

MODULE=$1
if [ -z "$MODULE" ]; then
    echo "Usage: $0 <module_name>"
    exit 1
fi

echo "🔍 Modules that depend on $MODULE:"
echo ""

PROJECTS_DIR="/home/graham/workspace/experiments"

for project_dir in $PROJECTS_DIR/*/; do
    project_name=$(basename "$project_dir")
    
    if [ "$project_name" == "$MODULE" ]; then
        continue
    fi
    
    if grep -r "from $MODULE\|import $MODULE" "$project_dir/src" 2>/dev/null | grep -q .; then
        echo "  - $project_name"
        grep -r "from $MODULE\|import $MODULE" "$project_dir/src" 2>/dev/null | head -3 | sed 's/^/    /'
    fi
done
```

### Full Ecosystem Update Script
Save as `update_all_granger.sh`:
```bash
#!/bin/bash
# Updates all Granger modules after major changes

echo "🔄 Updating entire Granger ecosystem..."
echo ""

PROJECTS_DIR="/home/graham/workspace/experiments"

for project_dir in $PROJECTS_DIR/*/; do
    project_name=$(basename "$project_dir")
    
    echo "📦 Updating $project_name..."
    cd "$project_dir"
    
    # Pull latest
    git pull
    
    # Update dependencies
    uv pip install -e .
    
    echo ""
done

echo "✅ Ecosystem update complete!"
```

Make scripts executable:
```bash
chmod +x update_module_deps.sh check_module_deps.sh update_all_granger.sh
```
