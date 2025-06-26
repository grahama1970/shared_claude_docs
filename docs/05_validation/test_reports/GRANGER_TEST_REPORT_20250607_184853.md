# Granger Ecosystem Test Report
Generated: 2025-06-07T18:49:23.243236

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
| sparta | ✅ passed | 0 | 0 | 0 | 0 | 0.13s |
| marker | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.06s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.30s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.64s |
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
t (sin, cos, tan,
.venv/lib/python3.10/site-packages/sympy/functions/elementary/trigonometric.py:34: in <module>
    from sympy.functions.elementary._trigonometric_special import (
E     File "/home/graham/workspace/experiments/marker/.venv/lib/python3.10/site-packages/sympy/functions/elementary/_trigonometric_special.py", line 49
E       from __future__ import annotations
E       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   SyntaxError: from __future__ imports must occur at the beginning of the file

```


## Recommendations


## Next Steps

❌ Fix failing tests before proceeding to interaction testing.
