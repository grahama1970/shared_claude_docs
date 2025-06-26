# Master Task List - GRANGER Bug Hunter Verification System

**Total Tasks**: 67 (Scenarios) + 5 (System Tasks) = 72  
**Completed**: 0/72  
**Active Tasks**: #001 (Primary - System Health), #002 (Level 0 Tests)  
**Last Updated**: 2025-06-09 09:15 EDT  

## 🔧 CRITICAL: Proactive Dependency Management

**LEARNED FROM PAST FAILURES**: Import errors are NOT bugs to report - they're issues to FIX immediately!

### When You Encounter Import Errors:
```bash
# 1. Check what's installed
cd /path/to/project
uv pip list

# 2. Compare with requirements
cat pyproject.toml | grep -A 20 "dependencies"

# 3. Add missing packages
uv add missing_package

# 4. Reinstall in editable mode
uv pip install -e .

# 5. Verify fix
python -c "import problematic_module; print('✅ Fixed!')"
```

### Common Import Fixes:
| Error | Fix Command | Why It Happens |
|-------|-------------|----------------|
| `ModuleNotFoundError: pdftext` | `uv add pdftext` | Marker dependency |
| `ModuleNotFoundError: arxiv` | `uv add arxiv` | ArXiv MCP dependency |
| `ModuleNotFoundError: pymupdf4llm` | `uv add pymupdf4llm` | PDF processing |
| `ModuleNotFoundError: tree-sitter` | `uv add tree-sitter tree-sitter-language-pack` | Code analysis |
| `ImportError: cannot import name 'SomeClass'` | `uv pip install -e .` | Stale installation |

### After Fixing Any Module:
```bash
# Update ALL dependent modules (CRITICAL!)
./update_module_deps.sh module_name

# Or manually for each dependent:
cd /path/to/dependent/module
uv pip install -e .
```

**REMEMBER**: Past attempts failed because they treated import errors as test failures instead of setup issues to fix!

## 🏥 Project Health Check (Run BEFORE Creating Tasks)

### Python Version Check
```bash
# Check Python version requirement across all GRANGER modules
for proj in /home/graham/workspace/experiments/*/; do
    echo -n "$(basename $proj): "
    grep python $proj/pyproject.toml 2>/dev/null | grep -v python- | head -1
done

# Verify granger_hub environment
cd /home/graham/workspace/experiments/granger_hub
python --version  # Should match pyproject.toml requirement
```

### Service Availability Check
```bash
# Check all required GRANGER services
curl -s http://localhost:8529/_api/version || echo "❌ ArangoDB not running"
curl -s http://localhost:8000/health || echo "❌ GrangerHub not running"
curl -s http://localhost:11434/api/tags || echo "❌ Ollama not running"
docker ps | grep -E "(arango|redis|postgres|runpod)" || echo "❌ Missing containers"

# Check MCP servers
ps aux | grep "arxiv-mcp-server" || echo "❌ ArXiv MCP not running"
ps aux | grep "mcp-screenshot" || echo "❌ Screenshot MCP not running"
```

### Test Infrastructure Check
```bash
# Verify granger-verify command availability
/granger-verify --help || echo "❌ granger-verify command not available"

# Check claude-test-reporter
cd /home/graham/workspace/experiments/claude-test-reporter
python -m pytest --collect-only 2>&1 | grep -E "(collected|error)"
```

### Existing Configuration Check
```bash
# Check for GRANGER ecosystem credentials
if [ -f ~/.env ]; then
    echo "=== Available GRANGER credentials ==="
    grep -E "(ARANGO|GRANGER_HUB|LLM_CALL|RUNPOD|NASA|YOUTUBE)" ~/.env | cut -d= -f1
fi

# Check module interaction readiness
for module in sparta marker arangodb arxiv-mcp-server youtube_transcripts llm_call; do
    echo -n "$module: "
    grep -l "granger_hub\|handle_message" /home/graham/workspace/experiments/$module/src/**/*.py 2>/dev/null | wc -l
done
```

⚠️ **BUG HUNTER MODE**: This task list is designed to autonomously hunt for bugs, weaknesses, and missing functionality through REAL module interactions. Each scenario tests the dynamic decision-making of the granger_hub when pipelines are NOT predefined.

🚫 **NO SIMULATIONS ALLOWED**: When testing module interactions, NEVER simulate functionality. However, BE PROACTIVE about fixing import issues:
- If module import fails: `uv pip list` → check `pyproject.toml` → `uv add package` → `uv pip install -e .`
- Module connection failures ARE valuable test results
- Import failures should be FIXED, not just reported

🔌 **DYNAMIC PIPELINE TESTING**: The core mission is to find weaknesses where the agent (granger_hub) chooses which spoke modules to call and in what order, especially under:
- Ambiguous user requests
- Resource constraints
- Module failures
- Contradictory requirements

🔄 **MULTI-AI VERIFICATION**: All critical findings must be verified by BOTH Perplexity and Gemini to ensure comprehensive bug detection.

---

## 📋 Task Priority Guidelines

### Correct Task Order (CRITICAL)
1. **System Verification Tasks** (#001-#005) - Ensure all infrastructure is ready
2. **Level 0: Single Module Tests** (#006-#015) - Test individual spoke competencies
3. **Level 1: Binary Interactions** (#016-#025) - Test simple pipelines
4. **Level 2: Multi-Module Workflows** (#026-#040) - Test complex workflows
5. **Level 3: Chaos & Resilience** (#041-#067) - Test system resilience
6. **Level X: Ambiguous Scenarios** (#068-#072) - Test emergent intelligence

### Bug Categories to Hunt
| Bug Type | Priority | Detection Method | Granger-Verify Flag |
|----------|----------|------------------|---------------------|
| Module communication failures | HIGH | Integration tests | `--tests-only` |
| Nonsensical pipeline creation | HIGH | Trap scenarios | `--force-fix` |
| Memory/state corruption | CRITICAL | Concurrent tests | `--parallel` |
| Resource constraint handling | HIGH | Chaos injection | `--max-iterations 3` |
| User preference learning | MEDIUM | Multi-turn tests | `--verify-docs` |

---

## 🎯 TASK #001: GRANGER Ecosystem Health Verification

**Status**: 🔄 Not Started  
**Dependencies**: None  
**Expected Duration**: 5-10 minutes  

### Implementation
- [ ] **RUN**: `/granger-verify --all --tests-only --json`
- [ ] **CAPTURE**: Store baseline health report
- [ ] **IDENTIFY**: List all failing modules
- [ ] **CATEGORIZE**: Skeleton vs implemented projects
- [ ] **PRIORITIZE**: Focus on implemented modules first

### Verification Command
```bash
# Generate comprehensive ecosystem health report
/granger-verify --all --tests-only --report-dir ./bug_hunter_baseline --json

# Extract critical metrics
jq '.summary.failed_projects' bug_hunter_baseline/summary.json
jq '.projects[] | select(.status == "skeleton") | .name' bug_hunter_baseline/summary.json
```

### Expected Outcomes
- Identify which modules are ready for bug hunting
- Baseline performance metrics for each module
- List of integration points between modules
- Honeypot test status across ecosystem

**Task #001 Complete**: [ ]

---

## 🎯 TASK #002-#011: Level 0 - Single Module Bug Hunt

### 🎯 TASK #002: Quick CVE Check (SPARTA)

**Status**: 🔄 Not Started  
**Dependencies**: #001  
**Expected Test Duration**: 1-5s  
**Bug Target**: CVE data retrieval, parsing, response speed

### User Story
*"As a cybersecurity analyst, I just saw a CVE ID mentioned in a morning briefing. I need to get the essential details immediately."*

### Implementation
- [ ] **TEST 1**: Valid CVE lookup: `CVE-2024-12345`
- [ ] **TEST 2**: Non-existent CVE: `CVE-9999-99999`
- [ ] **TEST 3**: Malformed CVE: `CVE-INVALID-FORMAT`
- [ ] **TEST 4**: Rapid sequential requests (rate limiting)
- [ ] **VERIFY**: Response structure contains all required fields

### Test Loop
```bash
# PROACTIVE SETUP: Fix any import issues first
cd /home/graham/workspace/experiments/sparta
if ! python -c "import sparta" 2>/dev/null; then
    echo "🔧 Fixing sparta imports..."
    uv pip list
    uv add requests beautifulsoup4  # Common sparta deps
    uv pip install -e .
fi

# Direct module test
pytest tests/test_cve_retrieval.py -v --json-report || {
    echo "🔧 Test collection failed - checking dependencies"
    grep "ModuleNotFoundError" pytest.log && {
        MODULE=$(grep "ModuleNotFoundError" pytest.log | sed 's/.*: //')
        uv add $MODULE
        uv pip install -e .
    }
}

# Via granger-verify
/granger-verify --project sparta --tests-only

# Bug hunter verification (with import protection)
python -c "
try:
    import sparta
    import time
    start = time.time()
    result = sparta.get_cve('CVE-2024-12345')
    duration = time.time() - start
    print(f'Duration: {duration}s')
    print(f'Has required fields: {all(f in result for f in ['id', 'description', 'severity'])}')
except ImportError as e:
    print(f'⚠️ Import issue detected: {e}')
    print('Run: uv add [missing_package] && uv pip install -e .')
    exit(1)
"
```

### Multi-AI Verification
```bash
# Send to Perplexity
/ask-perplexity "Analyze this SPARTA CVE retrieval test result: [paste output]. Is this a real API call or mocked? What bugs are evident?"

# Send to Gemini
/ask "Review this SPARTA module test for CVE retrieval: [paste output]. Identify any performance issues or missing error handling."
```

**Task #002 Complete**: [ ]

---

### 🎯 TASK #003: Find Research Paper (ArXiv MCP)

**Status**: 🔄 Not Started  
**Dependencies**: #001  
**Expected Test Duration**: 2-10s  
**Bug Target**: Research paper search, special characters, pagination

### User Story
*"A colleague mentioned 'that new paper on diffusion models by Chen et al.' I need to find it on ArXiv."*

### Implementation
- [ ] **TEST 1**: Author search: "Chen diffusion models 2024"
- [ ] **TEST 2**: Special characters: "Müller ∇f(x) optimization"
- [ ] **TEST 3**: Empty query handling
- [ ] **TEST 4**: Large result set pagination (>100 results)
- [ ] **TEST 5**: Concurrent searches

### Bug Hunter Tests
```python
# Test special character handling
test_queries = [
    "Müller quantum",  # Umlaut
    "∇f(x) optimization",  # Math symbols
    "Chen et al.",  # Common academic format
    "",  # Empty query
    "a" * 1000  # Extremely long query
]

for query in test_queries:
    try:
        results = arxiv_mcp_server.search(query)
        print(f"Query '{query[:20]}...': {len(results)} results")
    except Exception as e:
        print(f"BUG FOUND - Query '{query[:20]}...': {type(e).__name__}: {e}")
```

**Task #003 Complete**: [ ]

---

### 🎯 TASK #004: Store Finding in Knowledge Graph (ArangoDB)

**Status**: 🔄 Not Started  
**Dependencies**: #001  
**Expected Test Duration**: 0.1-2s  
**Bug Target**: Graph CRUD operations, concurrent access

### User Story
*"I've discovered Component A depends on Library X. Remember this relationship."*

### Implementation
- [ ] **TEST 1**: Create node with relationships
- [ ] **TEST 2**: Query graph traversal with depth limits
- [ ] **TEST 3**: Concurrent write operations
- [ ] **TEST 4**: Large batch inserts (1000+ nodes)
- [ ] **TEST 5**: Delete cascade behavior

### Concurrent Bug Test
```python
import asyncio
import arangodb

async def concurrent_writes():
    tasks = []
    for i in range(100):
        task = arangodb.create_node(f"Component_{i}", {"depends_on": f"Library_{i}"})
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    bugs = [r for r in results if isinstance(r, Exception)]
    print(f"Concurrent write bugs: {len(bugs)}")
    return bugs
```

**Task #004 Complete**: [ ]

---

## 🎯 TASK #012-#025: Level 1 - Binary Module Interactions

### 🎯 TASK #012: Download and Prep Paper (ArXiv → Marker)

**Status**: 🔄 Not Started  
**Dependencies**: #003, #005  
**Expected Test Duration**: 5-30s  
**Bug Target**: PDF handoff, unicode preservation, metadata flow

### User Story
*"Find a paper on ArXiv and immediately get it as clean Markdown for annotation."*

### Dynamic Pipeline Test
```python
# Test if granger_hub correctly chains these modules
user_request = "Get me the latest quantum computing paper as markdown"

# Expected pipeline: arxiv_mcp_server → marker
# Bug opportunities:
# 1. PDF URL vs file content handoff
# 2. Metadata preservation through pipeline
# 3. Unicode in paper titles/content
# 4. Large PDF handling (>100MB)
```

### Verification Points
- [ ] ArXiv provides valid PDF URL/content
- [ ] Marker receives correct input format
- [ ] Metadata (title, authors) preserved
- [ ] Unicode characters maintained
- [ ] Pipeline completes without manual intervention

**Task #012 Complete**: [ ]

---

### 🎯 TASK #013: Scan DEFCON Talk for CVEs (YouTube → SPARTA)

**Status**: 🔄 Not Started  
**Dependencies**: #002, #006  
**Expected Test Duration**: 10-60s  
**Bug Target**: Cross-domain analysis, entity extraction from speech

### User Story
*"I'm watching a DEFCON talk where hackers discuss new exploits. Pull out any CVEs mentioned."*

### Creative Pipeline Test
```python
# Non-obvious pipeline that granger_hub might miss
video_url = "https://youtube.com/watch?v=DEFCON_TALK_ID"

# Challenge: Will hub recognize this needs:
# 1. youtube_transcripts → get transcript
# 2. sparta → extract CVEs from text

# Bug opportunities:
# - Hub might not connect video → security analysis
# - CVE patterns in spoken vs written text
# - Timestamp alignment with mentions
```

**Task #013 Complete**: [ ]

---

## 🎯 TASK #026-#040: Level 2 - Complex Multi-Module Workflows

### 🎯 TASK #026: Build Custom Model from Research

**Status**: 🔄 Not Started  
**Dependencies**: Level 0 & 1 tasks  
**Expected Test Duration**: 5-30 minutes  
**Bug Target**: End-to-end data integrity, long pipeline management

### User Story
*"Create a model that's an expert on 'quantum cryptography' using latest research."*

### Complex Pipeline Test
```python
# Ultimate research-to-training pipeline
# Expected: arxiv → marker → arangodb → unsloth

# Bug hunting points:
# 1. Data volume handling (100+ papers)
# 2. Quality filtering decisions
# 3. Memory/state management
# 4. Error recovery in long chains
# 5. Progress tracking/reporting

test_pipeline = {
    "request": "Build quantum crypto expert model",
    "expected_modules": ["arxiv_mcp_server", "marker", "arangodb", "unsloth"],
    "constraints": {
        "max_papers": 100,
        "min_quality_score": 0.7,
        "time_limit": "30m",
        "cost_limit": "$10"
    }
}
```

### Chaos Injection
- [ ] Kill ArXiv mid-download
- [ ] Fill disk during Marker processing  
- [ ] Corrupt ArangoDB connection
- [ ] GPU unavailable for Unsloth

**Task #026 Complete**: [ ]

---

## 🎯 TASK #041-#067: Level 3 - Chaos & Resilience Testing

### 🎯 TASK #043: Module Resilience Testing

**Status**: 🔄 Not Started  
**Dependencies**: All Level 2 tasks  
**Expected Test Duration**: Variable  
**Bug Target**: Input validation, resource limits, graceful degradation

### User Story
*"As an SRE, I need every module to handle malformed input without crashing."*

### Malformed Input Battery
```python
malformed_inputs = {
    "marker": [
        b"\x00\x01\x02\x03",  # Binary data
        "corrupted.pdf",  # Non-existent file
        {"not": "a_pdf"},  # Wrong type
        "../../../etc/passwd",  # Path traversal
        "x" * 10**9  # Memory bomb
    ],
    "sparta": [
        "'; DROP TABLE vulnerabilities; --",  # SQL injection
        {"cve": None},  # Null values
        ["CVE-1", "CVE-2"] * 10000  # Large batch
    ],
    "arangodb": [
        {"_key": "../../admin"},  # Key injection
        {"data": {"$ne": None}},  # NoSQL injection
        circular_reference_object()  # Circular refs
    ]
}

# Test each module's resilience
for module, inputs in malformed_inputs.items():
    for bad_input in inputs:
        try:
            result = module.process(bad_input)
            print(f"BUG: {module} accepted malformed input: {bad_input[:50]}")
        except Exception as e:
            print(f"GOOD: {module} rejected input with: {type(e).__name__}")
```

**Task #043 Complete**: [ ]

---

### 🎯 TASK #050: Error Cascade Prevention

**Status**: 🔄 Not Started  
**Dependencies**: #043  
**Expected Test Duration**: Variable  
**Bug Target**: Circuit breakers, retry storms, fault isolation

### User Story
*"If ArXiv API goes down, it cannot take down the entire granger_hub."*

### Cascade Test Scenario
```python
# Simulate cascading failure
async def test_cascade_prevention():
    # 1. Make ArXiv fail
    arxiv_mcp_server.mock_failure_rate = 1.0
    
    # 2. Send 100 requests that need ArXiv
    tasks = []
    for i in range(100):
        task = granger_hub.process(f"Find paper about topic {i}")
        tasks.append(task)
    
    # 3. Measure:
    # - Does hub implement circuit breaker?
    # - Are retries exponentially backed off?
    # - Can hub suggest alternatives?
    # - Is overall system still responsive?
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Bug indicators:
    # - All 100 requests timeout (no circuit breaker)
    # - Retry storm detected (no backoff)
    # - Other modules become slow (cascade)
```

**Task #050 Complete**: [ ]

---

## 🎯 TASK #068-#072: Level X - Ambiguous & Dynamic Scenarios

### 🎯 TASK #068: Ambiguous Security Research

**Status**: 🔄 Not Started  
**Dependencies**: All previous levels  
**Expected Test Duration**: Variable  
**Bug Target**: Pipeline selection under ambiguity

### User Story
*"Show me the latest on quantum threats"*

### Ambiguity Factors
```yaml
interpretations:
  "latest": 
    - last_24_hours
    - last_week  
    - since_last_major_conference
  "quantum threats":
    - quantum_computing_breaking_encryption
    - post_quantum_cryptography_vulnerabilities
    - quantum_key_distribution_attacks
  "show me":
    - detailed_technical_report
    - executive_summary
    - raw_data_dump

valid_pipelines:
  - [sparta, llm_call]  # CVE-focused
  - [arxiv_mcp_server, marker, llm_call]  # Research-focused
  - [youtube_transcripts, llm_call]  # Conference-focused
  - [sparta, arxiv_mcp_server, youtube_transcripts, llm_call]  # Comprehensive

test_points:
  - Which pipeline does hub choose?
  - Does it ask for clarification?
  - Does it use world_model for user context?
  - How does rl_commons influence selection?
```

### Grading with Multi-AI
```bash
# Execute ambiguous request
result=$(granger_hub.process("Show me the latest on quantum threats"))

# Grade with Perplexity
/ask-perplexity "Given the request 'Show me the latest on quantum threats', 
analyze if this pipeline choice was optimal: $result. 
What ambiguities were not addressed?"

# Grade with Gemini  
/ask "Evaluate this granger_hub response to an ambiguous request: $result.
Did it handle the ambiguity appropriately? What bugs in decision-making are evident?"
```

**Task #068 Complete**: [ ]

---

### 🎯 TASK #069: Nonsensical Pipeline Trap

**Status**: 🔄 Not Started  
**Dependencies**: #068  
**Expected Test Duration**: <30s  
**Bug Target**: Internal constraints, module understanding

### Trap Scenarios
```python
trap_requests = [
    "Convert this YouTube video to a PDF",  # Video → PDF?
    "Find CVEs in this Python code",  # Code → CVEs?
    "Train a model on this single tweet",  # Insufficient data
    "Analyze the security of this image",  # Wrong domain
    "Download all of ArXiv",  # Resource constraint
]

for request in trap_requests:
    result = granger_hub.process(request)
    
    # FAIL if hub creates pipeline like:
    # - youtube_transcripts → marker (can't convert video to PDF)
    # - gitget → sparta (code isn't CVE data)
    # - single_tweet → unsloth (insufficient training data)
    
    if result.pipeline_used in NONSENSICAL_PIPELINES:
        print(f"BUG: Hub created nonsensical pipeline for '{request}'")
        print(f"Pipeline: {result.pipeline_used}")
```

**Task #069 Complete**: [ ]

---

### 🎯 TASK #070: Memory Corruption Test

**Status**: 🔄 Not Started  
**Dependencies**: #068  
**Expected Test Duration**: 5-10 minutes  
**Bug Target**: World model state consistency, user isolation

### Concurrent User Test
```python
async def test_user_isolation():
    # Create conflicting user preferences
    user_a_tasks = [
        granger_hub.process("I prefer technical papers", user="A"),
        granger_hub.process("I work in quantum computing", user="A"),
        granger_hub.process("Show me latest research", user="A")
    ]
    
    user_b_tasks = [
        granger_hub.process("Keep it simple, no jargon", user="B"),
        granger_hub.process("I'm new to security", user="B"),  
        granger_hub.process("Show me latest research", user="B")
    ]
    
    # Run concurrently
    results = await asyncio.gather(
        *user_a_tasks, 
        *user_b_tasks,
        return_exceptions=True
    )
    
    # Check for cross-contamination
    user_a_final = results[2]  # "Show me latest research" for A
    user_b_final = results[5]  # "Show me latest research" for B
    
    # BUG if:
    # - User B gets technical papers
    # - User A gets simplified content
    # - World model mixed user preferences
```

**Task #070 Complete**: [ ]

---

### 🎯 TASK #071: Self-Learning Verification

**Status**: 🔄 Not Started  
**Dependencies**: All previous tasks  
**Expected Test Duration**: 30-60 minutes  
**Bug Target**: RL Commons policy updates, learning from feedback

### Learning Loop Test
```python
# Phase 1: Establish baseline
baseline_pipeline = granger_hub.process("Find security research")

# Phase 2: Provide negative feedback
feedback = {
    "user_satisfaction": -1,
    "reason": "Too many old papers, wanted recent only"
}
granger_hub.provide_feedback(baseline_pipeline.id, feedback)

# Phase 3: Retry same request
improved_pipeline = granger_hub.process("Find security research")

# Phase 4: Verify learning
assert improved_pipeline != baseline_pipeline, "No learning occurred"
assert improved_pipeline.includes_recency_filter, "Didn't learn from feedback"

# Phase 5: Test generalization
related_request = granger_hub.process("Find AI research")
assert related_request.includes_recency_filter, "Learning didn't generalize"
```

**Task #071 Complete**: [ ]

---

### 🎯 TASK #072: Chaos Orchestration Finale

**Status**: 🔄 Not Started  
**Dependencies**: All tasks  
**Expected Test Duration**: 60+ minutes  
**Bug Target**: System-wide resilience under multiple failures

### Ultimate Chaos Test
```python
chaos_conditions = {
    "arxiv_api": "rate_limited",
    "arangodb": "slow_responses_10s", 
    "marker": "fails_30_percent",
    "gpu": "unavailable",
    "disk_space": "90_percent_full",
    "memory": "high_pressure",
    "network": "packet_loss_5_percent"
}

# Apply all chaos conditions
for service, condition in chaos_conditions.items():
    apply_chaos(service, condition)

# Run comprehensive test suite
test_requests = [
    "Build an expert model on quantum security",  # Needs all services
    "Urgent: Find today's new CVEs",  # Time sensitive
    "Analyze this 500MB PDF",  # Resource intensive
    "Compare these 10 research papers",  # Complex coordination
]

results = await asyncio.gather(
    *[granger_hub.process(req) for req in test_requests],
    return_exceptions=True
)

# Success criteria:
# - No complete system failure
# - Graceful degradation messages
# - Alternative pipelines attempted
# - Clear user communication about limitations
```

**Task #072 Complete**: [ ]

---

## 📊 Overall Progress

### By Status:
- ✅ Complete: 0 ([])  
- ⏳ In Progress: 0 ([])  
- 🚫 Blocked: 0 ([])  
- 🔄 Not Started: 72 (All tasks)  

### Bug Categories Found:
- Module Communication Failures: 0 instances
- Nonsensical Pipelines: 0 instances  
- Memory/State Corruption: 0 instances
- Resource Constraint Bugs: 0 instances
- Learning/Adaptation Failures: 0 instances

### Granger-Verify Integration:
```bash
# Generate comprehensive bug report
/granger-verify --all \
  --tests-only \
  --force-fix \
  --max-iterations 3 \
  --report-dir ./bug_hunter_results \
  --json

# Extract bug patterns
jq '.bugs[] | {module: .module, type: .bug_type, severity: .severity}' \
  bug_hunter_results/bug_summary.json
```

### Multi-AI Verification Summary:
- Perplexity Confirmations: 0/0
- Gemini Confirmations: 0/0  
- Consensus Bugs: 0
- Disputed Findings: 0

### Critical Issues:
1. [Pending first run]
2. [Pending first run]
3. [Pending first run]

### Next Actions:
1. Run Task #001 to establish ecosystem baseline
2. Begin Level 0 single module tests
3. Document all bugs found with reproduction steps
4. Create fix directives for granger-verify --force-fix
5. Schedule multi-AI verification for critical findings

---

## 🛠️ Bug Hunter Automation Scripts

### Run All Bug Hunter Tests
```bash
#!/bin/bash
# bug_hunter_runner.sh - Execute all bug hunting scenarios

echo "🐛 Starting GRANGER Bug Hunter..."

# Run baseline
/granger-verify --all --tests-only --json > baseline.json

# Run each level
for level in 0 1 2 3 X; do
    echo "Running Level $level tests..."
    python run_bug_hunter_level_$level.py
done

# Generate report
python generate_bug_report.py

# Multi-AI verification
/ask-perplexity "Review these bug findings: $(cat bug_report.json)"
/ask "Validate these GRANGER bugs: $(cat bug_report.json)"
```

### Bug Pattern Analyzer
```python
# analyze_bug_patterns.py
import json
from collections import defaultdict

def analyze_patterns(bug_reports):
    patterns = defaultdict(list)
    
    for bug in bug_reports:
        # Categorize by module interaction
        if len(bug['modules_involved']) > 1:
            pattern = f"{bug['modules_involved'][0]}→{bug['modules_involved'][1]}"
            patterns['pipeline_bugs'].append(pattern)
        
        # Categorize by failure type
        patterns[bug['failure_type']].append(bug)
        
        # Track ambiguity handling
        if 'ambiguous_request' in bug['trigger']:
            patterns['ambiguity_bugs'].append(bug)
    
    return patterns

# Generate recommendations
def generate_fixes(patterns):
    fixes = []
    
    if len(patterns['pipeline_bugs']) > 5:
        fixes.append({
            'type': 'systematic',
            'description': 'Hub pipeline selection logic needs constraints',
            'affected_modules': list(set(patterns['pipeline_bugs']))
        })
    
    return fixes
```

---

## 🔍 Programmatic Access

```python
# Access bug hunter results programmatically
import json

# Load results
with open('bug_hunter_results/summary.json') as f:
    results = json.load(f)

# Query specific bug types
nonsensical_pipelines = [
    bug for bug in results['bugs'] 
    if bug['type'] == 'nonsensical_pipeline'
]

# Generate fix commands
for bug in nonsensical_pipelines:
    print(f"/granger-verify --project {bug['module']} --force-fix")
```

---

This task list represents a comprehensive bug hunting framework that combines:
1. The scenarios from the Granger Bug Hunter document
2. The granger-verify command capabilities
3. Multi-AI verification requirements
4. Compliance with test verification standards

The hunt begins! 🐛🔍