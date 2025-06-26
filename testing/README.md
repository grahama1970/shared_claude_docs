# Testing Directory

This directory contains all testing-related code for the shared_claude_docs ecosystem.

## 📁 Structure

```
testing/
├── interaction_tests/     # Test module interactions (Levels 0-3)
├── visualization_tests/   # Test visualization decisions
├── self_evolution/        # Test self-improvement capabilities
└── integration_tests/     # Full system integration tests
```

## 🎯 Purpose

Each subdirectory focuses on a specific testing concern:

### `interaction_tests/`
Tests how modules work together at different complexity levels:
- Level 0: Single module calls
- Level 1: Sequential pipelines
- Level 2: Parallel execution
- Level 3: Complex orchestration

### `visualization_tests/`
Tests intelligent visualization selection:
- Detecting inappropriate visualizations
- Recommending alternatives (including tables)
- Style guide compliance

### `self_evolution/`
Tests autonomous improvement:
- Research using ArXiv/YouTube
- Code generation
- Testing and validation
- Git commits

### `integration_tests/`
Tests with real external APIs:
- ArXiv paper search
- YouTube transcript fetching
- End-to-end workflows

## 🚀 Quick Start

Run all interaction tests:
```bash
cd interaction_tests
python3 interaction_test_framework.py
```

Test visualization decisions:
```bash
cd visualization_tests
python3 visualization_decision_tests.py
```

See self-evolution demo:
```bash
cd self_evolution
python3 demo_self_evolution.py
```

## 📝 Best Practices

1. **Isolate Tests**: Each test should be independent
2. **Mock When Needed**: Use mocks for external dependencies
3. **Clear Output**: Make test results human-readable
4. **Document Failures**: Explain why tests fail
5. **Version Control**: Track test evolution

## 🔧 Adding New Tests

1. Choose the appropriate subdirectory
2. Follow existing patterns
3. Add clear documentation
4. Update the relevant README
5. Test your tests!

---

*This testing suite ensures robust module interactions and continuous improvement capabilities.*