# Docs Reorganization Plan - January 2025

## Overview

This plan reorganizes `/docs/` to follow the natural Granger development workflow:

1. **Research** → Transcripts & Papers
2. **Strategy** → Ideas & Architecture  
3. **Planning** → Task Lists (TASK_LIST_TEMPLATE_GUIDE_V2.md compliant)
4. **Implementation** → Code & Integration
5. **Validation** → Test Reports & Verification
6. **Operations** → Current State & Maintenance

## Proposed Structure

```
docs/
├── 00_research/              # Starting point: Raw inputs
│   ├── transcripts/          # Video transcripts (existing)
│   ├── papers/               # Scientific papers & references
│   └── external_docs/        # Third-party documentation
│
├── 01_strategy/              # Ideas & architectural decisions
│   ├── ideas/                # Strategy documents (existing)
│   ├── architecture/         # Core concepts & patterns
│   └── whitepaper/           # Vision documents (existing)
│
├── 02_planning/              # Task lists & project planning
│   ├── active_tasks/         # Current sprint tasks
│   ├── completed_tasks/      # Archived completed tasks
│   └── templates/            # Task list templates
│
├── 03_modules/               # Module documentation
│   ├── hub/                  # granger_hub docs
│   ├── spokes/               # All spoke project docs
│   └── infrastructure/       # RL Commons, Test Reporter, etc.
│
├── 04_implementation/        # Implementation guides
│   ├── integration/          # Integration patterns
│   ├── tutorials/            # How-to guides (existing)
│   └── examples/             # Code examples (existing)
│
├── 05_validation/            # Testing & verification
│   ├── test_plans/           # Test strategies
│   ├── test_reports/         # Test execution reports
│   └── verification/         # Critical verification docs
│
├── 06_operations/            # Current state & ops
│   ├── current_state/        # Live system status
│   ├── monitoring/           # Dashboards & metrics
│   └── maintenance/          # Operational procedures
│
├── archive/                  # Historical documents
│   ├── 2025-01/             # Monthly archives
│   ├── 2025-06/             # Existing archive
│   └── deprecated/          # Outdated docs
│
└── README.md                # Navigation guide
```

## Files to Archive

### Duplicate/Outdated Index Files
- `02_modules/000_INDEX_UPDATED.md` → Keep latest only
- `02_modules/000_INDEX_UPDATED.md.backup` → Archive
- Multiple compliance reports with same date → Keep one

### Completed/Old Planning Docs
- `REORGANIZATION_PLAN.md` → Archive (replaced by this)
- `DOCS_REORGANIZATION_SUMMARY.md` → Archive
- `DOCUMENTATION_UPDATE_REPORT_20250603.md` → Archive
- `SPOKE_MODULE_FIXES_REPORT.md` → Archive to 2025-06/

### Old State/Progress Files
- `UI_UNIFICATION_PROGRESS.md` → Archive if completed
- `CHAT_MIGRATION_PLAN.md` → Archive if completed
- Various PHASE2 progress files in tasks/ → Archive to completed_tasks/

### Gemini Correspondence
- All gemini files already in archive/gemini_correspondence/ ✓

### Test Reports
- Consolidate old test reports by date
- Keep only latest comprehensive reports
- Archive individual task reports older than 30 days

## Migration Steps

### Step 1: Create New Structure
```bash
# Create new directories
mkdir -p docs/{00_research,01_strategy,02_planning,03_modules,04_implementation,05_validation,06_operations}
mkdir -p docs/00_research/{papers,external_docs}
mkdir -p docs/01_strategy/architecture
mkdir -p docs/02_planning/{active_tasks,completed_tasks,templates}
mkdir -p docs/03_modules/{hub,spokes,infrastructure}
mkdir -p docs/04_implementation/integration
mkdir -p docs/05_validation/{test_plans,test_reports,verification}
mkdir -p docs/06_operations/{current_state,monitoring,maintenance}
mkdir -p docs/archive/2025-01
```

### Step 2: Move Existing Content
```bash
# Research
mv docs/transcripts/ docs/00_research/

# Strategy
mv docs/ideas/ docs/01_strategy/
mv docs/whitepaper/ docs/01_strategy/
mv docs/01_core_concepts/ docs/01_strategy/architecture/

# Planning
mv docs/tasks/*ACTIVE*.md docs/02_planning/active_tasks/
mv docs/tasks/*COMPLETE*.md docs/02_planning/completed_tasks/

# Modules
mv docs/02_modules/007_Describe_granger_hub.md docs/03_modules/hub/
mv docs/02_modules/*_Describe_*.md docs/03_modules/spokes/

# Implementation
mv docs/03_integration/ docs/04_implementation/integration/
mv docs/integration_patterns/ docs/04_implementation/integration/

# Validation
mv docs/04_testing/ docs/05_validation/test_plans/
mv docs/reports/ docs/05_validation/test_reports/

# Operations
mv docs/current_state_of_granger/ docs/06_operations/current_state/
```

### Step 3: Archive Old Files
```bash
# Archive outdated files
mv docs/*_REPORT_*.md docs/archive/2025-01/
mv docs/*_SUMMARY.md docs/archive/2025-01/
mv docs/02_modules/*.backup docs/archive/2025-01/
```

### Step 4: Update References
- Update CLAUDE.md to reference new structure
- Update README.md with new navigation
- Create index files for each major section

## Benefits

1. **Clear Workflow**: Follows research → strategy → planning → implementation → validation cycle
2. **Easy Navigation**: Numbered directories show progression
3. **Clean Separation**: Active work vs. archived content
4. **Scalability**: Room for growth in each section
5. **Discoverability**: Easier to find relevant documents

## Timeline

- Phase 1 (Immediate): Archive obvious duplicates and old reports
- Phase 2 (This Week): Create new directory structure
- Phase 3 (Next Week): Migrate content and update references
- Phase 4 (Ongoing): Maintain organization standards

## Success Criteria

- [ ] All active documents accessible in logical locations
- [ ] No duplicate files in main directories
- [ ] Clear distinction between active and archived content
- [ ] Updated navigation in README.md
- [ ] All project references updated to new paths