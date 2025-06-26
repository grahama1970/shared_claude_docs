# Files to Archive - January 2025

## Immediate Archive Candidates

### Root Level Docs - Move to archive/2025-01/
- `DOCS_REORGANIZATION_SUMMARY.md` - Old reorganization summary
- `DOCUMENTATION_UPDATE_REPORT_20250603.md` - Old update report  
- `SPOKE_MODULE_FIXES_REPORT.md` - Completed fixes report
- `UI_UNIFICATION_PROGRESS.md` - Completed UI work
- `CHAT_MIGRATION_PLAN.md` - Completed migration
- `DAILY_STANDUP_2025_06_04.md` - Old standup (June 2025)
- `REORGANIZATION_PLAN.md` - Replaced by REORGANIZATION_PLAN_2025.md
- `ORGANIZATION_GUIDE.md` - Generic, replaced by new structure
- `PROJECT_STRUCTURE.md` - Generic, replaced by GRANGER_PROJECTS.md

### Duplicate Module Indexes - Keep only latest
- `02_modules/000_INDEX_UPDATED.md.backup` → Archive
- Keep only the most recent 000_INDEX.md

### Old Task Progress Reports - Move to archive/2025-06/
- `tasks/054_GRANGER_PHASE2_TASK001_COMPLETE.md`
- `tasks/054_GRANGER_PHASE2_TASK001_UPDATE.md`  
- `tasks/090_GRANGER_INTEGRATION_COMPLETION_REPORT.md`
- `tasks/091_GRANGER_PHASE2_COMPLETE.md`
- `tasks/092_GRANGER_PHASE2_FINAL_SUMMARY.md`
- `tasks/093_GRANGER_PHASE2_PROGRESS_87_PERCENT.md`
- `tasks/094_GRANGER_PHASE2_PROGRESS_SUMMARY.md`
- `tasks/095_GRANGER_PHASE2_PROGRESS_UPDATE.md`
- `tasks/096_PHASE2_FINAL_VERIFICATION.md`

### Individual Test Reports - Consolidate
Move all individual test reports to archive, keep only comprehensive summaries:
- `reports/task_017_test_report_*.md` (multiple versions)
- `reports/task_018_test_report_*.md`
- `reports/task_019_test_report_*.md`
- `reports/task_38_test_report_*.md` (multiple versions)
- `reports/task_61_test_report_*.md`
- `reports/task_62_test_report_*.md`
- All `test_report_task_*` files with timestamps

Keep only:
- `reports/GRANGER_TEST_VERIFICATION_REPORT.md`
- `reports/test_report_tasks_*_summary.md` files

### Old Implementation Reports
- `reports/GRANGER_IMPLEMENTATION_PROGRESS.md` → Archive
- `reports/GRANGER_IMPLEMENTATION_SUMMARY.md` → Archive
- `reports/granger_phase2_progress_report.md` → Archive

### Completed Integration Docs
- `integration_patterns/TASK_012_COMPLETION_REPORT.md` → Archive
- `visual_diagrams/TASK_013_COMPLETION_REPORT.md` → Archive

### Old State Documents
Move to archive if these represent past states:
- `current_state_of_granger/ACTION_PLAN_RL_HUB_INTEGRATION_OLD.md`
- `current_state_of_granger/FINAL_GRANGER_STATE_SUMMARY.md.backup`

### UX Documentation - Check if current
Review and potentially archive:
- `ux_documentation/IMPLEMENTATION_PROGRESS_REPORT.md`
- `ux_documentation/FINAL_IMPLEMENTATION_SUMMARY.md`

## Archive Organization

```
archive/
├── 2025-01/          # Current archival
│   ├── reports/      # Old reports
│   ├── tasks/        # Completed tasks
│   └── planning/     # Old planning docs
│
├── 2025-06/          # Existing archive
│   ├── duplicates/   # Already organized
│   ├── outdated/     # Already organized
│   └── temp_files/   # Already organized
│
└── README.md         # Archive index
```

## Archival Rules

1. **Keep Latest Only**: For duplicate files, keep newest version
2. **Consolidate Reports**: Individual test reports → summary reports
3. **Preserve History**: Don't delete, move to dated archive
4. **Update References**: Fix any docs that reference archived files
5. **Document Moves**: Note in archive README what was moved when

## Priority Order

1. **High Priority** (Immediate):
   - Duplicate files
   - Old dated reports
   - Completed task progress files

2. **Medium Priority** (This week):
   - Old planning documents
   - Superseded guides
   - Individual test reports

3. **Low Priority** (Review first):
   - Current state documents (verify if still current)
   - UX documentation (check completion status)
   - Tutorial content (ensure still relevant)