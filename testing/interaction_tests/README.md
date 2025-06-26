# Interaction Tests

This directory contains tools for testing module interactions at different complexity levels (0-3).

## 📁 Files

- `interaction_test_framework.py` - Comprehensive test suite for all levels
- `interaction_runner.py` - Interactive runner for debugging specific patterns
- `stress_test_interactions.py` - Stress testing for robustness

## 🎯 Interaction Levels

### Level 0: Direct Module Calls
Single module performing its core function:
```python
arxiv_search("quantum computing") → papers
```

### Level 1: Sequential Pipeline
Output from one module feeds the next:
```python
arxiv_search() → marker_extract() → sparta_analyze()
```

### Level 2: Parallel & Branching
Multiple paths execute simultaneously:
```python
├─→ arxiv_search()
└─→ youtube_search()
    ↓
    merge_results()
```

### Level 3: Orchestrated Collaboration
Complex workflows with feedback loops:
```python
research() ↔ implement() ↔ test() ↔ learn()
```

## 🚀 Usage

### Run All Tests
```bash
python3 interaction_test_framework.py
```

### Test Specific Level
```bash
python3 interaction_test_framework.py --level 2
```

### Interactive Mode
```bash
python3 interaction_runner.py interactive
```

### Run Specific Pattern
```bash
python3 interaction_runner.py multi_source_research --topic "transformers"
```

### Stress Testing
```bash
python3 stress_test_interactions.py --type all
```

## 📊 Output

### Test Framework
- Generates markdown report
- Creates HTML dashboard
- Shows pass/fail for each level
- Tracks execution times

### Interaction Runner
- Real-time execution logs
- Step-by-step data flow
- Can save logs for debugging

### Example Output
```
✅ L1_Paper_Analysis_Pipeline
   Duration: 2.34s
   Modules: arxiv-mcp-server → marker → sparta
   Data flow:
      → ArXiv: Found 5 papers
      → Selected paper: 2401.12345
      → Marker: Extracted text
      → Analysis: Identified key concepts
   Result: Pipeline completed successfully
```

## 🔧 Adding New Tests

1. Add test definition in `interaction_test_framework.py`:
```python
InteractionTest(
    name="L2_New_Test",
    level=InteractionLevel.LEVEL_2,
    description="Test description",
    modules=["module1", "module2"],
    test_function=self._test_new_test,
    expected_output_type="dict"
)
```

2. Implement test function:
```python
async def _test_new_test(self) -> Dict[str, Any]:
    data_flow = []
    # Implementation
    return {
        "data_flow": data_flow,
        "summary": "Test completed"
    }
```

## 🐛 Debugging

### Enable Verbose Output
```python
runner = InteractionRunner(verbose=True)
```

### Save Execution Logs
```bash
python3 interaction_runner.py arxiv_search --save-log
```

### Check Module Status
The framework automatically detects which modules are available.

## 📈 Metrics Tracked

- Execution time per interaction
- Success/failure rates
- Module availability
- Data flow paths
- Error patterns

---

*These tests ensure reliable module interactions across all complexity levels.*