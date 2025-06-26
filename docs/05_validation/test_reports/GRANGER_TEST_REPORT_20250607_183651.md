# Granger Ecosystem Test Report
Generated: 2025-06-07T18:37:15.815411

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
| rl_commons | ✅ passed | 0 | 0 | 0 | 0 | 0.09s |
| world_model | ✅ passed | 0 | 0 | 0 | 0 | 0.11s |
| claude-test-reporter | ❌ failed | 1 | 0 | 1 | 0 | 0.07s |
| sparta | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| marker | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| arangodb | ✅ passed | 0 | 0 | 0 | 0 | 1.04s |
| llm_call | ✅ passed | 2 | 2 | 0 | 0 | 0.03s |
| fine_tuning | ✅ passed | 0 | 0 | 0 | 0 | 0.30s |
| youtube_transcripts | ✅ passed | 0 | 0 | 0 | 0 | 0.12s |
| darpa_crawl | ✅ passed | 0 | 0 | 0 | 0 | 1.91s |
| gitget | ✅ passed | 0 | 0 | 0 | 0 | 6.32s |
| arxiv-mcp-server | ✅ passed | 0 | 0 | 0 | 0 | 0.13s |
| mcp-screenshot | ✅ passed | 0 | 0 | 0 | 0 | 0.06s |
| chat | ✅ passed | 0 | 0 | 0 | 0 | 0.57s |
| annotator | ✅ passed | 0 | 0 | 0 | 0 | 0.07s |
| aider-daemon | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |
| runpod_ops | ✅ passed | 0 | 0 | 0 | 0 | 1.83s |
| granger-ui | ✅ passed | 2 | 2 | 0 | 0 | 0.01s |
| shared_claude_docs | ❌ failed | 0 | 0 | 0 | 0 | 0.00s |

## Critical Issues

### claude-test-reporter

**Output**:
```
--------------------------------
report saved to: test_report.json
=========================== short test summary info ============================
FAILED tests/core/test_test_result_verifier.py::TestTestResultVerifier::test_create_immutable_test_record - AttributeError: 'TestResultVerifier' object has no attribute 'create_test_record'
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
========================= 1 failed, 1 warning in 0.06s =========================

```

### marker

**Output**:
```
/schema/blocks/base.py:26: in <module>
    from PIL import Image
.venv/lib/python3.10/site-packages/PIL/Image.py:88: in <module>
    from defusedxml import ElementTree
E     File "/home/graham/workspace/experiments/marker/.venv/lib/python3.10/site-packages/defusedxml/ElementTree.py", line 22
E       from __future__ import print_function, absolute_import
E       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
