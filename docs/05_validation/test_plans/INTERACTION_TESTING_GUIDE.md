# Module Interaction Testing Guide

This guide explains how to test and debug module interactions across Levels 0-3.

## 🎯 Overview

The interaction testing system provides:
1. **Clear categorization** of interactions by complexity level
2. **Easy-to-use tools** for running and debugging interactions
3. **Human-readable output** for understanding data flow
4. **Visual dashboards** for test results

## 📁 Key Files

### Testing Tools
- `utils/interaction_test_framework.py` - Comprehensive test suite for all levels
- `utils/interaction_runner.py` - Interactive runner for specific patterns
- `utils/visualization_decision_tests.py` - Tests for intelligent viz decisions
- `utils/self_evolving_analyzer.py` - Autonomous improvement system

### Documentation
- `docs/big_picture/MODULE_INTERACTION_LEVELS.md` - Detailed level definitions
- `docs/big_picture/INTERACTION_EXAMPLES_VISUAL.md` - Visual examples
- `docs/big_picture/INTERACTION_PATTERNS_ANALYSIS.md` - Pattern analysis

## 🚀 Quick Start

### 1. Run All Interaction Tests
```bash
cd /home/graham/workspace/shared_claude_docs/utils
python3 interaction_test_framework.py
```

This will:
- Test all interaction levels (0-3)
- Check module availability
- Generate a report and visual dashboard
- Show data flow for each interaction

### 2. Test Specific Level
```bash
# Test only Level 2 (parallel/branching)
python3 interaction_test_framework.py --level 2
```

### 3. Interactive Testing
```bash
python3 interaction_runner.py interactive
```

This opens an interactive menu to:
- Run specific interactions
- See detailed execution logs
- Debug data flow step-by-step

### 4. Run Specific Interaction
```bash
# Run multi-source research
python3 interaction_runner.py multi_source_research --topic "machine learning"

# Run visualization decision
python3 interaction_runner.py visualization_decision
```

## 📊 Interaction Levels

### Level 0: Direct Module Calls
Simple, single-module operations:
```python
# Example: Search ArXiv
papers = await arxiv_search("quantum computing")
```

### Level 1: Sequential Pipeline
Output from one module feeds into the next:
```python
# Example: Paper → Extract → Analyze
arxiv_search() → marker_extract() → sparta_analyze()
```

### Level 2: Parallel & Branching
Multiple paths execute simultaneously:
```python
# Example: Parallel research
├─→ arxiv_search()
└─→ youtube_search()
    ↓
merge_results()
```

### Level 3: Orchestrated Collaboration
Complex workflows with feedback loops:
```python
# Example: Self-improving system
research() ↔ implement() ↔ test() ↔ learn()
```

## 🧪 Testing Patterns

### Visualization Decision Testing
Test intelligent visualization selection:
```bash
python3 visualization_decision_tests.py
```

Tests include:
- Detecting inappropriate visualizations
- Recommending alternatives (including tables)
- Providing clear reasoning

### Self-Evolution Testing
Test autonomous improvement:
```bash
python3 self_evolving_analyzer.py marker --iterations 1
```

This will:
- Research improvements using ArXiv/YouTube
- Implement changes
- Test and validate
- Commit if successful

## 📝 Example Outputs

### Test Framework Output
```
🚀 Running Interaction Tests
============================================================

📊 Level 0: Direct Module Calls
----------------------------------------

✅ L0_ArXiv_Search
   Duration: 1.23s
   Modules: arxiv-mcp-server
   Data flow:
      → Found 5 papers
   Result: Successfully searched ArXiv

✅ L0_YouTube_Search
   Duration: 0.45s
   Modules: youtube_transcripts
   Data flow:
      → Found 3 videos
   Result: Successfully searched YouTube
```

### Interaction Runner Output
```
[14:23:15.123] START: Starting interaction: multi_source_research
[14:23:15.234] INFO: Multi-source research: 'machine learning'
[14:23:15.345] INFO: Launching parallel searches...
[14:23:15.456] INFO: ArXiv search: 'machine learning'
[14:23:15.567] INFO: YouTube search: 'machine learning'
[14:23:16.789] INFO: Found 5 papers
[14:23:16.890] INFO: Found 3 videos in local database
[14:23:16.901] INFO: Merging results...
[14:23:17.012] SUCCESS: Completed: multi_source_research
```

## 🔍 Debugging Tips

### 1. Enable Verbose Logging
```python
runner = InteractionRunner(verbose=True)
```

### 2. Check Module Availability
The test framework automatically checks if modules are installed:
```
🔍 Checking module availability...
   ✅ arxiv-mcp-server
   ✅ youtube_transcripts
   ❌ marker (not found)
```

### 3. Save Execution Logs
```bash
python3 interaction_runner.py arxiv_search --save-log
```

### 4. View Visual Dashboard
After running tests, open:
```
interaction_test_results/interaction_test_dashboard.html
```

## 🎯 Best Practices

### 1. Start Simple
- Begin with Level 0 tests
- Ensure each module works independently
- Then move to higher levels

### 2. Use Clear Data Flow
```python
self.log("Step 1: Searching papers...")
self.log("Step 2: Extracting content...")
self.log("Step 3: Analyzing results...")
```

### 3. Handle Failures Gracefully
```python
if not papers:
    self.log("No papers found", "WARNING")
    return None
```

### 4. Test Edge Cases
- Empty results
- API failures
- Timeout scenarios
- Invalid data formats

## 🔧 Extending the Framework

### Adding New Tests
1. Define test in `_define_tests()`:
```python
InteractionTest(
    name="L1_New_Pipeline",
    level=InteractionLevel.LEVEL_1,
    description="New pipeline description",
    modules=["module1", "module2"],
    test_function=self._test_new_pipeline,
    expected_output_type="dict"
)
```

2. Implement test function:
```python
async def _test_new_pipeline(self) -> Dict[str, Any]:
    data_flow = []
    # Implementation
    return {"data_flow": data_flow, "summary": "Result"}
```

### Adding New Interaction Patterns
Add to `interaction_runner.py`:
```python
async def new_pattern(self, **kwargs):
    """New interaction pattern"""
    self.log("Starting new pattern...")
    # Implementation
    return result
```

## 🚦 Where to Run Tests

### Development Testing
Run in `shared_claude_docs` for initial development and debugging.

### Integration Testing
Eventually move to `claude-module-communicator` as the central orchestrator.

### CI/CD Pipeline
Can be integrated into automated testing workflows.

## 📊 Monitoring & Metrics

The framework tracks:
- Execution time per interaction
- Success/failure rates
- Module availability
- Data flow paths
- Error patterns

Use these metrics to:
- Identify bottlenecks
- Find common failures
- Optimize interactions
- Plan improvements

---

This testing framework provides a solid foundation for understanding, testing, and debugging module interactions across all complexity levels.