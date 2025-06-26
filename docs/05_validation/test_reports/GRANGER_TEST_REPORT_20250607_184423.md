# Granger Ecosystem Test Report
Generated: 2025-06-07T18:44:55.272184

## Summary

- **Total Projects**: 20
- **Passed**: 18 ✅
- **Failed**: 2 ❌
- **No Tests**: 0 ⚠️
- **Errors**: 0 🚨

## Detailed Results

| Project | Status | Tests | Passed | Failed | Errors | Duration |
|---------|--------|-------|--------|--------|--------|----------|
| granger_hub | ✅ passed | 0 | 0 | 0 | 0 | 0.11s |
| rl_commons | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| world_model | ✅ passed | 0 | 0 | 0 | 0 | 0.11s |
| claude-test-reporter | ✅ passed | 9 | 9 | 0 | 0 | 0.04s |
| sparta | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| marker | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.11s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.30s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.11s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.31s |
| arxiv-mcp-server | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| mcp-screenshot | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| chat | ✅ passed | 0 | 0 | 0 | 0 | 0.59s |
| annotator | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| aider-daemon | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| runpod_ops | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| granger-ui | ✅ passed | 2 | 2 | 0 | 0 | 0.01s |
| shared_claude_docs | ✅ passed | 2 | 2 | 0 | 0 | 0.02s |

## Critical Issues

### marker

**Output**:
```
hardata.py:56: in _build_regexes
    charlist = byte_range.decode(encoding)
.venv/lib/python3.10/site-packages/ftfy/bad_codecs/__init__.py:93: in search_function
    from ftfy.bad_codecs.sloppy import CODECS
E     File "/home/graham/workspace/experiments/marker/.venv/lib/python3.10/site-packages/ftfy/bad_codecs/sloppy.py", line 89
E       from __future__ import annotations
E       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   SyntaxError: from __future__ imports must occur at the beginning of the file

```

### aider-daemon

**Output**:
```
n/.venv/lib/python3.10/site-packages/_pytest/assertion/rewrite.py", line 357, in _rewrite_test
    tree = ast.parse(source, filename=strfn)
  File "/home/graham/.local/share/uv/python/cpython-3.10.11-linux-x86_64-gnu/lib/python3.10/ast.py", line 50, in parse
    return compile(source, filename, mode, flags,
  File "/home/graham/workspace/experiments/aider-daemon/.venv/lib/python3.10/site-packages/allure_pytest/plugin.py", line 70
    from pathlib import Path
    ^^^^
SyntaxError: invalid syntax

```


## Recommendations


## Next Steps

❌ Fix failing tests before proceeding to interaction testing.
