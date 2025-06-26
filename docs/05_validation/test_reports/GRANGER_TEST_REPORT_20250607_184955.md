# Granger Ecosystem Test Report
Generated: 2025-06-07T18:50:31.450289

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
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.02s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.31s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.33s |
| arxiv-mcp-server | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| mcp-screenshot | ✅ passed | 0 | 0 | 0 | 0 | 0.06s |
| chat | ✅ passed | 0 | 0 | 0 | 0 | 0.56s |
| annotator | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| aider-daemon | ✅ passed | 0 | 0 | 0 | 0 | 0.21s |
| runpod_ops | ✅ passed | 0 | 0 | 0 | 0 | 1.84s |
| granger-ui | ✅ passed | 2 | 2 | 0 | 0 | 0.01s |
| shared_claude_docs | ✅ passed | 2 | 2 | 0 | 0 | 0.02s |

## Critical Issues

### marker

**Output**:
```
c/marker/core/processors/enhanced_camelot/__init__.py:28: in <module>
    from marker.core.processors.enhanced_camelot.processor import EnhancedTableProcessor
src/marker/core/processors/enhanced_camelot/processor.py:42: in <module>
    from marker.core.config.table import (
E     File "/home/graham/workspace/experiments/marker/src/marker/core/config/table.py", line 8
E       Description: Implementation of table functionality
E                                   ^^
E   SyntaxError: invalid syntax

```


## Recommendations


## Next Steps

❌ Fix failing tests before proceeding to interaction testing.
