# Documentation Reorganization Plan

**Created**: 2025-06-04  
**Status**: PROPOSED  
**Purpose**: Improve navigation and consistency in GRANGER documentation

---

## Summary of Findings

After analyzing 197 documents across 26 directories, the documentation is generally well-organized but has some areas for improvement:

### Strengths
1. Clear directory hierarchy with logical grouping
2. Numbered module descriptions for easy reference
3. Good separation of concerns (concepts, modules, testing, etc.)
4. Recent additions well-integrated (Level 4 docs)

### Areas for Improvement
1. Multiple index files causing confusion (000_INDEX.md vs README.md)
2. Inconsistent naming conventions
3. Missing cross-references between related documents
4. No Level 4 examples yet
5. Some directories lack README files

---

## Proposed Changes

### 1. Navigation Consolidation
- **Action**: Merge 000_INDEX.md content into README.md
- **Reason**: Single source of truth for navigation
- **Files affected**: 
  - Delete: 000_INDEX.md
  - Update: README.md (incorporate useful content)
  - Add: Link to DOCUMENT_MAP.md in README

### 2. Naming Standardization
Adopt consistent pattern: 

**Examples**:
- OLD: 
- NEW: 

- OLD: 
- NEW: 

### 3. Add Missing Documents

#### Level 4 Examples
Create in :
- 
- 
- 

#### Performance Documentation
Create in new  directory:
- 
- 
- 

#### Deployment Guides
Create in new  directory:
- 
- 
- 

### 4. Cross-Reference System

Add to each document:


### 5. Directory README Files

Add README.md to directories missing them:
-  - API documentation overview
-  - How to read/generate reports
-  - Meeting notes organization
-  - Tutorial index

---

## Implementation Plan

### Phase 1: Navigation (Week 1)
1. Back up current structure
2. Merge index files
3. Update all internal links
4. Add DOCUMENT_MAP.md reference to README

### Phase 2: Naming (Week 2)
1. Create rename script
2. Update all file references
3. Test all links work
4. Commit with clear message

### Phase 3: Content (Week 3-4)
1. Create Level 4 examples
2. Add performance documentation
3. Create deployment guides
4. Add cross-references to top 20 docs

### Phase 4: Polish (Week 5)
1. Add missing READMEs
2. Update DOCUMENT_MAP.md
3. Create topic-based indexes
4. Final link verification

---

## Benefits

1. **Easier Navigation**: Single entry point, clear structure
2. **Better Discovery**: Cross-references and tags
3. **Consistency**: Standardized naming and format
4. **Completeness**: Fill gaps in Level 4 and deployment docs
5. **AI-Friendly**: Predictable structure for automated tools

---

## Risks and Mitigation

### Risk: Broken Links
- **Mitigation**: Automated link checker before/after
- **Tool**: 

### Risk: Lost History
- **Mitigation**: Git preserves all history
- **Backup**: Create archive branch before changes

### Risk: User Confusion
- **Mitigation**: Announce changes, provide migration guide
- **Timeline**: Give 1 week notice

---

## Decision Required

**Options**:
1. **Full Reorganization**: Implement all changes (5 weeks)
2. **Minimal Fix**: Just merge indexes and add Level 4 examples (1 week)
3. **Gradual Migration**: Phase changes over 3 months

**Recommendation**: Option 2 (Minimal Fix) to address immediate needs, then gradual migration for the rest.

---

## Next Steps

1. Review and approve plan
2. Create backup branch
3. Start with Phase 1 (Navigation)
4. Weekly progress updates

---

*For questions or concerns, contact graham@granger-aerospace.com*
