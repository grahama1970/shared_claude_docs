# Scheduled Runs and CLAUDE.md Compliance

## 1. Scheduled/Cron Runs: Recommended Approach

### ❌ **DO NOT** Run Full Cleanup in Cron
Running the full cleanup utility automatically can:
- Create unwanted git branches while you're working
- Make changes without context
- Cause merge conflicts
- Run tests that might fail for environment reasons

### ✅ **DO** Run Read-Only Checks

#### Option A: Weekly Report (Recommended)
```bash
# Add to crontab for Monday mornings
0 7 * * 1 /path/to/scheduled_cleanup.sh
```

This script:
- Runs in **dry-run mode only**
- Generates reports without making changes
- Can email/webhook notify if issues found
- Preserves logs for trend analysis

#### Option B: Pre-Commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
cd /path/to/cleanup_utility
./run_enhanced_cleanup.sh --dry-run --sequential | grep -E "❌|⚠️" && {
    echo "⚠️  Project has cleanup issues. Run ./run_enhanced_cleanup.sh for details"
    exit 1
}
```

#### Option C: CI/CD Integration
```yaml
# .github/workflows/cleanup-check.yml
name: Project Cleanup Check
on: [push, pull_request]
jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run cleanup check
        run: |
          cd utils/cleanup_utility
          ./run_enhanced_cleanup.sh --dry-run
```

## 2. CLAUDE.md Compliance: Philosophy

### The Reality Check

CLAUDE.md files contain AI interaction guidelines that sometimes include:
- Strict coding standards
- Project-specific conventions  
- Ideal practices that may not match current code

**Auto-enforcing these would be dangerous** because:

1. **Context Matters**: Claude Code sometimes ignores rules for good reasons
2. **Massive Refactoring**: Could break working code
3. **Evolution**: Code evolves, CLAUDE.md might be outdated
4. **Practicality**: Some rules might be aspirational

### Recommended Approach

#### 1. **Compliance Checking** (Not Auto-Fixing)
```bash
# Check a single project
python claude_compliance_checker.py /path/to/project

# Check all projects
for project in /home/graham/workspace/experiments/*; do
    python claude_compliance_checker.py "$project"
done
```

#### 2. **Manual Review Process**
Use compliance reports for:
- Code review checklists
- Identifying technical debt
- Updating outdated CLAUDE.md files
- Gradual refactoring sprints

#### 3. **Selective Enforcement**
Only auto-enforce critical rules:
- Security (no hardcoded secrets)
- Basic formatting (via black/isort)
- Import organization

## 3. Practical Implementation Strategy

### Phase 1: Monitoring (Current Tools)
```bash
# Weekly status check
./scheduled_cleanup.sh

# Monthly compliance audit  
python claude_compliance_checker.py /path/to/project
```

### Phase 2: Gradual Improvement
1. Review reports manually
2. Update CLAUDE.md to match reality
3. Fix critical issues first
4. Plan refactoring sprints

### Phase 3: Selective Automation
Only automate safe, non-breaking changes:
```python
# Example: Auto-fix imports only
isort --profile black --check-only .
black --check .
```

## 4. Example Crontab Setup

```bash
# Edit crontab
crontab -e

# Add these lines:
# Weekly project health check (Mondays 7 AM)
0 7 * * 1 /home/graham/workspace/shared_claude_docs/utils/cleanup_utility/scheduled_cleanup.sh

# Monthly compliance report (1st of month)
0 8 1 * * cd /home/graham/workspace/shared_claude_docs/utils/cleanup_utility && python claude_compliance_checker.py /home/graham/workspace/experiments > /home/graham/logs/compliance_$(date +\%Y\%m).log 2>&1
```

## 5. Best Practices

### DO:
- ✅ Run read-only checks regularly
- ✅ Review reports manually
- ✅ Update CLAUDE.md to match reality
- ✅ Fix security issues immediately
- ✅ Use reports for sprint planning

### DON'T:
- ❌ Auto-refactor based on CLAUDE.md
- ❌ Run cleanup with --live in cron
- ❌ Enforce all rules blindly
- ❌ Create branches automatically
- ❌ Ignore context and evolution

## Summary

1. **Scheduled runs**: Use read-only monitoring, not automatic fixes
2. **CLAUDE.md compliance**: Check but don't auto-enforce
3. **Manual review**: Essential for context-aware decisions
4. **Gradual improvement**: Better than big-bang refactoring
5. **Safety first**: Preserve working code over perfect compliance