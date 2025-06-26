# Dependency Resolution Lessons Learned

> **Documentation of dependency conflict resolution in the Granger ecosystem**  
> **Date**: 2025-01-09  
> **Session Duration**: ~2 hours  
> **Modules Fixed**: 8 (arangodb, marker, fine_tuning, rl_commons, mcp-screenshot, runpod_ops enabled)

---

## 🎯 Executive Summary

Successfully resolved all dependency conflicts in the Granger ecosystem, enabling `uv sync` to complete without errors. Key issues included numpy version conflicts, broken git submodules, package naming mismatches, and missing module imports.

---

## 🔍 Issues Encountered and Solutions

### 1. **ArangoDB NumPy Version Conflict**

**Problem**: ArangoDB required numpy>=2.2.2 but marker and other modules needed numpy<2
```
✗ No solution found when resolving dependencies:
  ╰─▶ Because marker==0.3.5 depends on surya-ocr~=0.13.1 
      and surya-ocr==0.13.1 depends on numpy<2.0.0 and >=1.21.6, 
      we can conclude that marker==0.3.5 depends on numpy>=1.21.6,<2.0.0.
      And because arangodb==0.1.0 depends on numpy>=2.2.2 
      and only arangodb==0.1.0 is available, 
      we can conclude that marker==0.3.5 and arangodb==0.1.0 are incompatible.
```

**Solution**: Pinned numpy to 1.26.4 across all projects
```toml
# In arangodb/pyproject.toml
"numpy==1.26.4",  # Changed from >=2.2.2

# In shared_claude_docs/pyproject.toml
"numpy==1.26.4",  # Pinned to match marker and arangodb
```

**Lesson**: When multiple packages have conflicting version requirements, find a version that satisfies all constraints rather than using the latest.

### 2. **Unused Dependencies in ArangoDB**

**Problem**: ArangoDB had dependencies it didn't actually use
- qdrant-client (vector database competitor)
- markitdown (document processing, marker does this)

**Solution**: Removed unused dependencies
```bash
# Removed from arangodb/pyproject.toml:
# "qdrant-client>=1.12.1",
# "markitdown>=0.0.1a3",
```

**Lesson**: Audit dependencies regularly and remove unused ones to prevent unnecessary conflicts.

### 3. **Unsloth Broken Git Submodule**

**Problem**: fine_tuning had a broken git submodule preventing installation
```
error: No url found for submodule path 'repos/runpod_llm_ops' in .gitmodules
Failed to clone 'repos/runpod_llm_ops'. Retry scheduled
```

**Solution**: Removed the broken submodule
```bash
cd /home/graham/workspace/experiments/fine_tuning
rm -rf repos/runpod_llm_ops
rm -f .gitmodules
git rm --cached repos/runpod_llm_ops
git commit -m "fix: remove broken runpod_llm_ops submodule"
```

**Lesson**: Git submodules can break package installation. Consider alternatives like direct dependencies or vendoring.

### 4. **Package Name vs Distribution Name Mismatch**

**Problem**: fine_tuning distributed as "unsloth" not "unsloth-wip"
```
error: Package metadata name `unsloth` does not match given name `unsloth-wip`
```

**Solution**: Use the correct package name in dependencies
```toml
# Changed from:
"unsloth-wip @ git+https://github.com/grahama1970/fine_tuning.git"
# To:
"unsloth @ git+https://github.com/grahama1970/fine_tuning.git"
```

**Lesson**: Always check the actual package name in pyproject.toml, not the repository name.

### 5. **PyArrow Version Conflict**

**Problem**: unsloth's mlflow dependency required pyarrow<20
```
Because mlflow==2.19.0 depends on pyarrow>=4.0.0,<20 
and arangodb==0.1.0 depends on pyarrow>=20.0.0
```

**Solution**: Adjusted pyarrow constraint
```toml
"pyarrow>=4.0.0,<20",  # Compatible with unsloth's mlflow requirement
```

**Lesson**: Check transitive dependencies (dependencies of dependencies) for conflicts.

### 6. **Surya-OCR Version Conflict**

**Problem**: marker needed surya-ocr<0.14, granger-hub needed >=0.14.5
```
Because only surya-ocr<=0.13.1 is available and granger-hub==0.2.7 
depends on surya-ocr>=0.14.5, granger-hub==0.2.7 requires surya-ocr>0.13.1.
```

**Solution**: Updated marker to use newer surya-ocr
```toml
# In marker/pyproject.toml
"surya-ocr>=0.14.5,<0.15.0",  # Updated from ~=0.13.1
```

**Lesson**: When possible, update packages to use newer versions rather than holding back the entire ecosystem.

### 7. **Missing Module Imports**

**Problem**: rl_commons and mcp-screenshot had missing submodules
```python
ModuleNotFoundError: No module named 'rl_commons.algorithms.meta'
ModuleNotFoundError: No module named 'mcp_screenshot.core'
```

**Initial Mistake**: Created placeholder modules with empty implementations

**Correct Solution**: The modules already existed! Just needed proper imports
```python
# rl_commons/algorithms/meta/__init__.py
from .maml import MAML, MAMLAgent
from .reptile import Reptile, ReptileAgent
from .task_distribution import TaskDistribution, TaskSampler

# mcp-screenshot - needed packaging update
packages = ["mcp_screenshot", "mcp_screenshot.core", "mcp_screenshot.cli"]
```

**Lesson**: Always check if functionality exists before creating placeholders. Missing imports doesn't mean missing code.

### 8. **RunPod Ops Enablement**

**Problem**: User asked if runpod_ops should be a separate module for inference

**Solution**: Enabled it in shared_claude_docs since unsloth already depends on it
```toml
"runpod_ops @ git+https://github.com/grahama1970/runpod_ops.git",  # Enabled for inference support
```

**Lesson**: Check if downstream packages already depend on a module before deciding on architecture.

---

## 📋 Resolution Process

### Step-by-Step Approach

1. **Run uv sync to identify conflicts**
   ```bash
   uv sync
   # Read error messages carefully
   ```

2. **Fix one conflict at a time**
   - Start with the most fundamental (numpy)
   - Work up the dependency tree

3. **Remove unnecessary dependencies**
   - Audit each package's actual usage
   - Remove competitors/duplicates

4. **Handle git submodules carefully**
   ```bash
   # Check for submodules
   git submodule status
   # Remove broken ones properly
   git rm --cached path/to/submodule
   ```

5. **Verify module structure**
   ```bash
   # Check what actually exists
   ls -la src/module_name/submodule/
   # Don't create placeholders if code exists
   ```

6. **Test each fix incrementally**
   ```bash
   uv sync
   # Don't move on until current issue is resolved
   ```

---

## 🛠️ Tools and Commands Used

### Diagnostic Commands
```bash
# Check package name in repository
grep "^name = " /path/to/repo/pyproject.toml

# Find dependency usage
grep -r "qdrant" /path/to/repo/src/

# Check git submodules
cd /path/to/repo && git submodule status

# List actual module structure
find /path/to/repo/src -name "*.py" | head -20
```

### Fix Commands
```bash
# Update git submodules
git submodule update --init --recursive

# Remove broken submodule
git rm --cached repos/submodule
rm -rf repos/submodule

# Test specific package installation
uv add "package @ git+https://github.com/user/repo.git"
```

---

## 🎓 Key Takeaways

1. **Version Pinning Strategy**
   - Pin critical packages (numpy) to specific versions
   - Use ranges for less critical packages
   - Document why versions are pinned

2. **Dependency Auditing**
   - Regularly check for unused dependencies
   - Remove competing solutions (qdrant vs arangodb)
   - Question every dependency

3. **Package Naming**
   - Repository name != package name
   - Always check pyproject.toml name field
   - Use correct name in dependencies

4. **Module Structure**
   - Check what exists before creating
   - Update packaging to include all submodules
   - Don't assume missing imports = missing code

5. **Git Submodules**
   - Avoid when possible
   - Can break installations
   - Consider direct dependencies instead

6. **Incremental Fixing**
   - Fix one issue at a time
   - Test after each fix
   - Don't try to fix everything at once

---

## 📊 Final Status

| Module | Status | Key Fix |
|--------|--------|---------|
| shared_claude_docs | ✅ Fixed | numpy pinned, runpod_ops enabled |
| arangodb | ✅ Fixed | numpy 1.26.4, removed unused deps |
| marker | ✅ Fixed | surya-ocr updated to 0.14.5 |
| fine_tuning | ✅ Fixed | removed submodule, fixed name |
| rl_commons | ✅ Fixed | imports already existed |
| mcp-screenshot | ✅ Fixed | packaging included submodules |
| granger-hub | ✅ Working | No changes needed |
| runpod_ops | ✅ Enabled | Uncommented for inference |

**Result**: `uv sync` completes successfully with all dependencies resolved!

---

## 🔮 Future Recommendations

1. **Establish Dependency Standards**
   - Document locked versions in module standards
   - Create automated checks for version conflicts
   - Regular dependency audits

2. **Improve Error Messages**
   - Add comments explaining version pins
   - Document why dependencies exist
   - Create dependency decision log

3. **Testing Infrastructure**
   - Add dependency conflict tests
   - Automated uv sync in CI/CD
   - Regular ecosystem-wide sync tests

4. **Module Structure Validation**
   - Tool to verify all imports resolve
   - Check packaging includes all submodules
   - Validate against 3-layer architecture

---

## 📚 Related Documentation

- [Granger Module Standards](../07_style_conventions/GRANGER_MODULE_STANDARDS.md)
- [Python Packaging Fix Summary](../../../PYTHON_PACKAGING_FIX_SUMMARY.md)
- [Dependency Conflicts Summary](../../../DEPENDENCY_CONFLICTS_SUMMARY.md)