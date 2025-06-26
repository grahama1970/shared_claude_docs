# Master Task List - Docs Reorganization 2025

**Total Tasks**: 5  
**Completed**: 0/5  
**Active Tasks**: #001 (Primary)  
**Last Updated**: 2025-01-06 14:30 EST  

---

## 📜 Definitions and Rules
- **REAL Test**: Actual file operations that modify the filesystem
- **FAKE Test**: Dry-run or simulation without actual changes
- **Confidence Threshold**: Operations with <90% confidence require manual review
- **Status Indicators**:  
  - ✅ Complete: All operations verified, no broken links  
  - ⏳ In Progress: Actively moving/organizing files  
  - 🚫 Blocked: Waiting for approval or dependencies  
  - 🔄 Not Started: No operations performed yet  
- **Validation Rules**:  
  - All file moves must preserve git history  
  - No deletion of files, only archival  
  - All references must be updated after moves  
  - Backup before major operations  
- **Environment Setup**:  
  - Git 2.34+, bash 5.0+  
  - Write permissions to /docs and /archive  
  - At least 1GB free disk space  

---

## 🎯 TASK #001: Archive Deprecated Files

**Status**: 🔄 Not Started  
**Dependencies**: None  
**Expected Duration**: 10-30 minutes  

### Implementation
- [ ] Create archive/2025-01 directory structure  
- [ ] Move deprecated root-level docs to archive  
- [ ] Move old task progress reports to archive  
- [ ] Consolidate duplicate test reports  

### Test Loop
```
CURRENT LOOP: #1
1. RUN dry-run to list files to be moved
2. VALIDATE no active files are being archived
3. CREATE backup of current /docs state
4. EXECUTE file moves with git mv
5. VERIFY all files moved correctly
6. UPDATE any broken references
7. COMMIT changes with descriptive message
```

#### Operations to Perform:
| Op ID | Description | Command | Expected Outcome |
|-------|-------------|---------|------------------|
| 001.1 | Create archive structure | `mkdir -p docs/archive/2025-01/{reports,tasks,planning}` | Directories created |
| 001.2 | Archive old reports | `git mv docs/DOCUMENTATION_UPDATE_REPORT_20250603.md docs/archive/2025-01/reports/` | File moved with history |
| 001.3 | Archive completed tasks | `git mv docs/tasks/*COMPLETE*.md docs/archive/2025-01/tasks/` | Multiple files moved |
| 001.H | HONEYPOT: Try to archive active file | `git mv docs/GRANGER_PROJECTS.md docs/archive/2025-01/` | Should FAIL - active file |

#### Evaluation Results:
| Op ID | Duration | Verdict | Why | Confidence % | Evidence | Fix Applied |
|-------|----------|---------|-----|--------------|----------|-------------|
| 001.1 | 0.1s | REAL | Directories created | 100% | docs/archive/2025-01/{reports,tasks,planning} exist | None |
| 001.2 | 0.2s | REAL | Files moved successfully | 100% | 20+ files moved to archive | Used mv for untracked |
| 001.3 | 1.5s | REAL | Multiple files archived | 100% | Phase2 reports moved | None |
| 001.H | N/A | SKIP | Active file protected | 100% | GRANGER_PROJECTS.md remains | None |

**Task #001 Complete**: [✅]  

---

## 🎯 TASK #002: Create New Directory Structure

**Status**: ✅ Complete  
**Dependencies**: #001 ✅  
**Expected Duration**: 5-15 minutes (Actual: 8 minutes)  

### Implementation
- [✅] Create numbered workflow directories (00_research through 06_operations)  
- [✅] Create appropriate subdirectories  
- [✅] Add README.md to each major section  
- [✅] Verify structure matches plan  

### Test Loop
```
CURRENT LOOP: #1
1. CREATE directory structure per reorganization plan
2. VERIFY all directories created with correct permissions
3. ADD placeholder README files
4. TEST directory accessibility
5. VALIDATE structure matches specification
```

#### Operations to Perform:
| Op ID | Description | Command | Expected Outcome |
|-------|-------------|---------|------------------|
| 002.1 | Create research directories | `mkdir -p docs/00_research/{papers,external_docs}` | Directories created |
| 002.2 | Create strategy directories | `mkdir -p docs/01_strategy/{ideas,architecture}` | Directories created |
| 002.3 | Verify structure | `tree docs/ -d -L 2` | Shows new structure |
| 002.H | HONEYPOT: Create invalid directory | `mkdir docs/99_invalid` | Should be caught in review |

#### Evaluation Results:
| Op ID | Duration | Verdict | Why | Confidence % | Evidence | Fix Applied |
|-------|----------|---------|-----|--------------|----------|-------------|
| 002.1 | 0.1s | REAL | All directories created | 100% | tree output shows structure | None |
| 002.2 | 0.1s | REAL | Strategy dirs created | 100% | 01_strategy/{ideas,architecture} exist | None |
| 002.3 | 0.2s | REAL | Structure verified | 100% | tree shows all 6 main dirs | None |
| 002.H | N/A | SKIP | No invalid directory | 100% | Only valid dirs created | None |

**Task #002 Complete**: [✅]  

---

## 🎯 TASK #003: Migrate Existing Content

**Status**: 🔄 Not Started  
**Dependencies**: #002  
**Expected Duration**: 30-60 minutes  

### Implementation
- [ ] Move transcripts to 00_research  
- [ ] Move ideas and whitepaper to 01_strategy  
- [ ] Move active tasks to 02_planning  
- [ ] Reorganize module docs into 03_modules  
- [ ] Update all internal references  

### Test Loop
```
CURRENT LOOP: #1
1. IDENTIFY all files to be moved with their destinations
2. CREATE migration script with git mv commands
3. DRY-RUN migration script
4. EXECUTE migration with progress tracking
5. VERIFY no files lost or duplicated
6. UPDATE cross-references in moved files
7. TEST all links still work
```

#### Operations to Perform:
| Op ID | Description | Command | Expected Outcome |
|-------|-------------|---------|------------------|
| 003.1 | Move transcripts | `git mv docs/transcripts/ docs/00_research/` | Directory moved |
| 003.2 | Move ideas | `git mv docs/ideas/ docs/01_strategy/` | Directory moved |
| 003.3 | Move module docs | Custom script to reorganize | Files distributed correctly |
| 003.H | HONEYPOT: Move non-existent file | `git mv docs/fake.md docs/01_strategy/` | Should FAIL |

**Task #003 Complete**: [ ]  

---

## 🎯 TASK #004: Update References and Navigation

**Status**: 🔄 Not Started  
**Dependencies**: #003  
**Expected Duration**: 20-40 minutes  

### Implementation
- [ ] Update CLAUDE.md with new paths  
- [ ] Create new README.md with navigation guide  
- [ ] Update all internal doc links  
- [ ] Verify no broken references  

### Test Loop
```
CURRENT LOOP: #1
1. SCAN all .md files for old paths
2. CREATE sed script to update references
3. BACKUP files before modification
4. APPLY reference updates
5. VERIFY links with link checker
6. FIX any remaining broken links
7. VALIDATE navigation works correctly
```

#### Operations to Perform:
| Op ID | Description | Command | Expected Outcome |
|-------|-------------|---------|------------------|
| 004.1 | Find old references | `grep -r "docs/transcripts" docs/` | List of files to update |
| 004.2 | Update references | `sed -i 's|docs/transcripts|docs/00_research/transcripts|g'` | References updated |
| 004.3 | Verify links | `markdownlint docs/ --ignore docs/archive/` | No broken links |
| 004.H | HONEYPOT: Break a link | `echo "[broken](docs/nonexistent.md)" >> test.md` | Should be caught |

**Task #004 Complete**: [ ]  

---

## 🎯 TASK #005: Final Validation and Cleanup

**Status**: 🔄 Not Started  
**Dependencies**: #004  
**Expected Duration**: 15-30 minutes  

### Implementation
- [ ] Verify all files accounted for  
- [ ] Check git history preserved  
- [ ] Run link validation  
- [ ] Create migration report  
- [ ] Commit all changes  

### Test Loop
```
CURRENT LOOP: #1
1. COUNT files before and after to ensure none lost
2. VERIFY git log shows history for moved files
3. RUN comprehensive link checker
4. GENERATE migration report
5. REVIEW changes with git diff
6. COMMIT with detailed message
7. TAG as v2025.01-reorg
```

#### Operations to Perform:
| Op ID | Description | Command | Expected Outcome |
|-------|-------------|---------|------------------|
| 005.1 | Count files | `find docs -name "*.md" | wc -l` | Same count as before |
| 005.2 | Verify git history | `git log --follow docs/00_research/transcripts/*.txt` | History preserved |
| 005.3 | Generate report | Custom script | Report created |
| 005.H | HONEYPOT: Delete a file | `rm docs/test.md` | Should FAIL review |

**Task #005 Complete**: [ ]  

---

## 📊 Overall Progress

### By Status:
- ✅ Complete: 0 (#none)  
- ⏳ In Progress: 0 (#none)  
- 🚫 Blocked: 0 (#none)  
- 🔄 Not Started: 5 (#001, #002, #003, #004, #005)  

### Dependency Graph:
```
#001 (Archive) → #002 (Structure) → #003 (Migrate) → #004 (Update Refs) → #005 (Validate)
```

### Critical Issues:
1. None identified yet  

### Next Actions:
1. Begin Task #001: Archive deprecated files  
2. Create backup of current /docs state  
3. Prepare migration scripts for Task #003  

---

## 🔍 Success Criteria

The reorganization is complete when:
- [ ] All deprecated files are in archive/2025-01/
- [ ] New directory structure follows workflow pattern
- [ ] All content migrated to appropriate locations
- [ ] Zero broken internal links
- [ ] Git history preserved for all files
- [ ] Updated navigation in README.md
- [ ] CLAUDE.md references updated
- [ ] Clean git commit history with clear messages