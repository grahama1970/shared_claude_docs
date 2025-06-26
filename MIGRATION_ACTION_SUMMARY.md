# Migration Action Summary: fine_tuning → fine_tuning

## Quick Action Commands

### Step 1: Update shared_claude_docs repository
```bash
cd /home/graham/workspace/shared_claude_docs
./execute_unsloth_migration.sh
```

### Step 2: Rename GitHub repository
```bash
cd /home/graham/workspace/experiments/fine_tuning
gh repo rename fine_tuning
git remote set-url origin git+https://github.com/grahama1970/fine_tuning.git
```

### Step 3: Rename local directory
```bash
cd /home/graham/workspace/experiments
mv fine_tuning fine_tuning
```

### Step 4: Update the project itself
```bash
cd /home/graham/workspace/experiments/fine_tuning
# Edit pyproject.toml to change name = "fine_tuning" to name = "fine_tuning"
# Update any internal references
```

### Step 5: Update dependent projects
For each project that depends on fine_tuning:
- runpod_ops
- Any other projects with fine_tuning in their pyproject.toml

```bash
# In each dependent project's pyproject.toml, change:
# "fine_tuning @ git+https://github.com/grahama1970/fine_tuning.git"
# To:
# "fine_tuning @ git+https://github.com/grahama1970/fine_tuning.git"
```

### Step 6: Commit all changes
```bash
cd /home/graham/workspace/shared_claude_docs
git add -A
git commit -m "Rename fine_tuning to fine_tuning across documentation"
git push
```

## Files That Will Be Updated

### Primary Documentation
1. `docs/GRANGER_PROJECTS.md` - Main project registry ✓ (already updated)
2. `CLAUDE.md` - Workspace context
3. `pyproject.toml` - Dependencies

### Additional Documentation
4. `docs/04_implementation/integration/MODULE_INTEGRATION_SUMMARY.md`
5. `docs/04_implementation/integration/GRANGER_MCP_MIGRATION_REPORT.md`
6. `docs/04_implementation/integration/EXISTING_MODULE_MIGRATION_GUIDE.md`
7. Various test and script files

### Total Impact
- **231 files** contain references to fine_tuning
- Most are documentation, test reports, and scripts
- Core changes needed in ~10 key files

## Verification Checklist

After migration:
- [ ] GitHub repository accessible at new URL
- [ ] Local directory renamed successfully
- [ ] All imports work in dependent projects
- [ ] Documentation reflects new name
- [ ] No broken links or references
- [ ] Tests pass in the renamed project

## Why This Migration?

1. **Clarity**: "fine_tuning" better describes the project's purpose
2. **Professionalism**: Removes the "wip" (work in progress) suffix
3. **Alignment**: Matches industry terminology for model adaptation
4. **Scope**: The project does more than just Unsloth integration