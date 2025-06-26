# Migration Plan: Renaming fine_tuning to fine_tuning

**Generated:** 2025-06-10  
**Scope:** Complete migration of `fine_tuning` project to `fine_tuning`

## Overview

This document provides a comprehensive plan for renaming the `fine_tuning` project to `fine_tuning` across the entire Granger ecosystem.

## Current State Analysis

### GitHub Repository
- Current: `git+https://github.com/grahama1970/fine_tuning.git`
- Target: `git+https://github.com/grahama1970/fine_tuning.git`

### Local Directory
- Current: `/home/graham/workspace/experiments/fine_tuning/`
- Target: `/home/graham/workspace/experiments/fine_tuning/`

### References Found
Based on analysis, `fine_tuning` is referenced in:
1. **Documentation files** (231 files total)
2. **pyproject.toml** dependencies
3. **CLAUDE.md** project registry
4. **GRANGER_PROJECTS.md** (primary registry)
5. **Various scripts and test files**

## Migration Checklist

### Phase 1: GitHub Repository Rename

```bash
# 1. Navigate to the project directory
cd /home/graham/workspace/experiments/fine_tuning

# 2. Update the GitHub repository name
gh repo rename fine_tuning

# 3. Update local git remote URL
git remote set-url origin git+https://github.com/grahama1970/fine_tuning.git

# 4. Verify the change
git remote -v
```

### Phase 2: Local Directory Rename

```bash
# 1. Navigate to experiments directory
cd /home/graham/workspace/experiments

# 2. Rename the directory
mv fine_tuning fine_tuning

# 3. Update any symbolic links if they exist
# Check for symlinks first:
find . -type l -ls | grep fine_tuning
```

### Phase 3: Update Package Configuration

#### In `/home/graham/workspace/experiments/fine_tuning/pyproject.toml`:
```toml
# Change:
name = "fine_tuning"
# To:
name = "fine_tuning"

# Update any internal references
```

### Phase 4: Update Documentation References

#### 1. Update GRANGER_PROJECTS.md
Replace all occurrences of:
- `fine_tuning` → `fine_tuning`
- `git+https://github.com/grahama1970/fine_tuning.git` → `git+https://github.com/grahama1970/fine_tuning.git`
- `/home/graham/workspace/experiments/fine_tuning/` → `/home/graham/workspace/experiments/fine_tuning/`

#### 2. Update CLAUDE.md
Replace:
- Line 59: `**Unsloth:** `/home/graham/workspace/experiments/fine_tuning/` - Model training`
- To: `**Fine Tuning:** `/home/graham/workspace/experiments/fine_tuning/` - Model training`

#### 3. Update pyproject.toml dependencies
```toml
# Line 66 - Change:
"unsloth @ git+https://github.com/grahama1970/fine_tuning.git",
# To:
"fine_tuning @ git+https://github.com/grahama1970/fine_tuning.git",
```

### Phase 5: Update Cross-Project Dependencies

#### Projects that may depend on fine_tuning:
1. **runpod_ops** - GPU compute (critical dependency)
2. **arangodb** - Q&A data provider
3. **granger_hub** - Orchestration
4. **llm_call** - Model serving

For each dependent project:
```bash
# Update pyproject.toml dependencies
# Change: fine_tuning @ git+...
# To: fine_tuning @ git+...
```

### Phase 6: Update Import Statements

Search and replace in all Python files:
```python
# Change:
from fine_tuning import ...
import fine_tuning
# To:
from fine_tuning import ...
import fine_tuning
```

### Phase 7: Update Test Files

Update any test files that reference fine_tuning:
- `bug_hunter_tests/task_009_unsloth_training.py`
- `bug_hunter_tests/bug_hunter_tests/task_009_fine_tuning_test.py`

### Phase 8: Update Scripts and Automation

Files to update:
- Any bash scripts referencing the path
- CI/CD configurations
- Deployment scripts
- Documentation generation scripts

## Automated Update Script

```bash
#!/bin/bash
# save as: migrate_unsloth_to_fine_tuning.sh

echo "Starting migration from fine_tuning to fine_tuning..."

# Phase 1: Update documentation files
echo "Updating documentation files..."
find /home/graham/workspace/shared_claude_docs -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) -exec sed -i 's/fine_tuning/fine_tuning/g' {} +

# Phase 2: Update GitHub URLs
echo "Updating GitHub URLs..."
find /home/graham/workspace/shared_claude_docs -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) -exec sed -i 's|git+https://github.com/grahama1970/fine_tuning.git|git+https://github.com/grahama1970/fine_tuning.git|g' {} +

# Phase 3: Update paths
echo "Updating local paths..."
find /home/graham/workspace/shared_claude_docs -type f \( -name "*.md" -o -name "*.toml" -o -name "*.py" \) -exec sed -i 's|/experiments/fine_tuning/|/experiments/fine_tuning/|g' {} +

echo "Migration complete! Please review changes before committing."
```

## Verification Steps

After migration:
1. Run tests in the renamed project
2. Verify all imports work correctly
3. Check that dependent projects can still access fine_tuning
4. Update any documentation that describes the project's purpose
5. Commit and push all changes

## Rollback Plan

If issues arise:
1. GitHub allows renaming back within 30 days
2. Keep a backup of the original directory
3. Git history preserves all changes

## Notes

- The name "fine_tuning" better reflects the project's purpose
- This aligns with industry-standard terminology
- Consider updating the project description to emphasize its fine-tuning capabilities beyond just Unsloth integration