# Granger Dependency Quick Reference

> **Quick solutions for common dependency issues**  
> **Keep this handy when running `uv sync`**

---

## 🚨 Common Errors and Fixes

### 1. NumPy Version Conflict
```
✗ No solution found when resolving dependencies:
  Because X depends on numpy<2.0.0 and Y depends on numpy>=2.2.2
```
**Fix**: Pin numpy to 1.26.4 in ALL projects
```toml
"numpy==1.26.4",  # Ecosystem-wide version
```

### 2. Package Name Mismatch
```
error: Package metadata name `unsloth` does not match given name `unsloth-wip`
```
**Fix**: Use package name from pyproject.toml, not repo name
```bash
# Check actual package name
grep "^name = " /path/to/repo/pyproject.toml

# Use in dependencies
"unsloth @ git+https://..."  # Not unsloth-wip
```

### 3. Git Submodule Error
```
error: No url found for submodule path 'repos/xyz' in .gitmodules
```
**Fix**: Remove broken submodule
```bash
cd /path/to/repo
rm -rf repos/xyz
git rm --cached repos/xyz
git commit -m "fix: remove broken submodule"
```

### 4. Missing Module Import
```
ModuleNotFoundError: No module named 'package.submodule'
```
**Fix**: Check if module exists first!
```bash
# Check what's actually there
ls -la /path/to/repo/src/package/submodule/

# If it exists, update packaging
# In pyproject.toml:
packages = ["package", "package.submodule"]
```

### 5. Transitive Dependency Conflict
```
Because mlflow==2.19.0 depends on pyarrow<20 and you require pyarrow>=20
```
**Fix**: Find compatible version range
```toml
"pyarrow>=4.0.0,<20",  # Works with mlflow
```

---

## 📋 Diagnostic Commands

```bash
# Show dependency tree
uv pip tree

# Check why package is needed
uv pip show package-name

# Find usage in code
grep -r "import package" src/

# Check package metadata
cd /path/to/repo && grep -A5 "^\[project\]" pyproject.toml

# List git submodules
git submodule status

# Test single package install
uv add "package @ git+https://github.com/user/repo.git"
```

---

## 🔒 Locked Versions (DO NOT CHANGE)

```toml
# Core dependencies - ecosystem-wide
"numpy==1.26.4"           # Many packages depend on this
"pandas>=2.2.3,<2.3.0"    # Compatible with numpy 1.26.4
"pyarrow>=4.0.0,<20"      # mlflow constraint
"pillow>=10.1.0,<11.0.0"  # Security constraints

# Python version
requires-python = ">=3.10.11"
```

---

## ✅ Pre-Sync Checklist

Before running `uv sync`:

1. **Check Python version**
   ```bash
   python --version  # Should be 3.10.11+
   ```

2. **Activate virtual environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Clean cache if needed**
   ```bash
   uv cache clean
   ```

4. **Update uv itself**
   ```bash
   pip install --upgrade uv
   ```

---

## 🚑 Emergency Fixes

### Full Reset
```bash
# Nuclear option - start fresh
rm -rf .venv uv.lock
uv venv --python=3.10.11
source .venv/bin/activate
uv sync
```

### Force Specific Version
```bash
# Override version temporarily
uv add --force "numpy==1.26.4"
```

### Skip Problem Package
```toml
# Comment out in pyproject.toml temporarily
# "problem-package @ git+...",
```

---

## 📞 When to Escalate

Contact team if:
- Locked versions need changing
- New package conflicts with ecosystem
- Git submodule is actually needed
- Multiple packages need major updates

---

## 🔗 Resources

- [Full Module Standards](../docs/07_style_conventions/GRANGER_MODULE_STANDARDS.md)
- [Detailed Lessons Learned](../docs/06_operations/maintenance/DEPENDENCY_RESOLUTION_LESSONS_LEARNED.md)
- [UV Documentation](https://github.com/astral-sh/uv)