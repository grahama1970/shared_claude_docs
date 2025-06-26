# Granger Ecosystem Test Report
Generated: 2025-06-07T18:40:43.532851

## Summary

- **Total Projects**: 20
- **Passed**: 16 ✅
- **Failed**: 4 ❌
- **No Tests**: 0 ⚠️
- **Errors**: 0 🚨

## Detailed Results

| Project | Status | Tests | Passed | Failed | Errors | Duration |
|---------|--------|-------|--------|--------|--------|----------|
| granger_hub | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| rl_commons | ✅ passed | 0 | 0 | 0 | 0 | 0.08s |
| world_model | ✅ passed | 0 | 0 | 0 | 0 | 0.10s |
| claude-test-reporter | ❌ failed | 3 | 2 | 1 | 0 | 0.06s |
| sparta | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| marker | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.04s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.30s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.27s |
| arxiv-mcp-server | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| mcp-screenshot | ✅ passed | 0 | 0 | 0 | 0 | 0.06s |
| chat | ✅ passed | 0 | 0 | 0 | 0 | 0.56s |
| annotator | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| aider-daemon | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| runpod_ops | ✅ passed | 0 | 0 | 0 | 0 | 1.83s |
| granger-ui | ✅ passed | 2 | 2 | 0 | 0 | 0.01s |
| shared_claude_docs | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |

## Critical Issues

### claude-test-reporter

**Output**:
```
nings.html
--------------------------------- JSON report ----------------------------------
report saved to: test_report.json
=========================== short test summary info ============================
FAILED tests/core/test_test_result_verifier.py::TestHallucinationDetector::test_check_response_basic - KeyError: 'detection_count'
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
==================== 1 failed, 2 passed, 1 warning in 0.06s ====================

```

### marker

**Output**:
```
e>
    dill = import_dill()
.venv/lib/python3.10/site-packages/torch/utils/_import_utils.py:37: in import_dill
    import dill
.venv/lib/python3.10/site-packages/dill/__init__.py:40: in <module>
    from ._dill import (
E     File "/home/graham/workspace/experiments/marker/.venv/lib/python3.10/site-packages/dill/_dill.py", line 42
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

### shared_claude_docs

**Output**:
```
python3.10/site-packages/_pytest/compat.py", line 35, in <module>
    import py
  File "/home/graham/workspace/shared_claude_docs/.venv/lib/python3.10/site-packages/py.py", line 26, in <module>
    import _pytest._py.path as path
  File "/home/graham/workspace/shared_claude_docs/.venv/lib/python3.10/site-packages/_pytest/_py/path.py", line 18
    from __future__ import annotations
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: from __future__ imports must occur at the beginning of the file

```


## Recommendations


## Next Steps

❌ Fix failing tests before proceeding to interaction testing.
