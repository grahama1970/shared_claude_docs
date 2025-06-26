# Granger Ecosystem Test Report
Generated: 2025-06-07T18:51:55.871719

## Summary

- **Total Projects**: 20
- **Passed**: 19 ✅
- **Failed**: 1 ❌
- **No Tests**: 0 ⚠️
- **Errors**: 0 🚨

## Detailed Results

| Project | Status | Tests | Passed | Failed | Errors | Duration |
|---------|--------|-------|--------|--------|--------|----------|
| granger_hub | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| rl_commons | ✅ passed | 0 | 0 | 0 | 0 | 0.08s |
| world_model | ✅ passed | 0 | 0 | 0 | 0 | 0.11s |
| claude-test-reporter | ✅ passed | 9 | 9 | 0 | 0 | 0.04s |
| sparta | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| marker | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.03s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.30s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.40s |
| arxiv-mcp-server | ✅ passed | 0 | 0 | 0 | 0 | 0.13s |
| mcp-screenshot | ✅ passed | 0 | 0 | 0 | 0 | 0.06s |
| chat | ✅ passed | 0 | 0 | 0 | 0 | 0.57s |
| annotator | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| aider-daemon | ✅ passed | 0 | 0 | 0 | 0 | 0.21s |
| runpod_ops | ✅ passed | 0 | 0 | 0 | 0 | 1.84s |
| granger-ui | ✅ passed | 2 | 2 | 0 | 0 | 0.01s |
| shared_claude_docs | ✅ passed | 2 | 2 | 0 | 0 | 0.02s |

## Critical Issues

### marker

**Output**:
```
Cannot read termcap database;
using dumb terminal settings.
ImportError while loading conftest '/home/graham/workspace/experiments/marker/tests/conftest.py'.
tests/conftest.py:12: in <module>
    project_root = Path(__file__).parent.parent
E   NameError: name 'Path' is not defined

```


## Recommendations


## Next Steps

❌ Fix failing tests before proceeding to interaction testing.
