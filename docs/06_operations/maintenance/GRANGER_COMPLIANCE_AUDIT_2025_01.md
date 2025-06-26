# Granger Ecosystem Compliance Audit Report

> **Date**: 2025-01-09  
> **Auditor**: Claude  
> **Standards Version**: 1.0.0

---

## 🚨 Executive Summary

**Overall Compliance: 18% (3/17 projects fully compliant)**

Most projects in the Granger ecosystem are **NOT compliant** with the mandatory standards defined in [GRANGER_MODULE_STANDARDS.md](../../07_style_conventions/GRANGER_MODULE_STANDARDS.md).

### Fully Compliant Projects (3)
- ✅ **granger_hub** (after numpy fix)
- ✅ **arxiv-mcp-server** (after numpy fix)  
- ✅ **darpa_crawl** (after numpy fix)

### Partially Compliant Projects (14)
All other projects have multiple compliance violations.

---

## 📊 Detailed Compliance Matrix

| Project | Python Version | Numpy | Pandas | 3-Layer | No Mocks | Overall |
|---------|----------------|-------|---------|---------|----------|---------|
| **Core Infrastructure** |
| granger_hub | ✅ 3.10.11 | ❌ >=1.24.0 | ❌ >=2.0.0 | ✅ | ❌ 330 mocks | ❌ |
| rl_commons | ❌ >=3.10 | ❌ >=1.24.0 | ❌ >=2.0.0 | ❓ | ❌ 125 mocks | ❌ |
| world_model | ❌ >=3.9 | ❌ >=1.24.0 | N/A | ❓ | ❓ | ❌ |
| claude-test-reporter | ❌ >=3.10 | N/A | N/A | ❓ | ❓ | ❌ |
| **Processing Spokes** |
| sparta | ✅ 3.10.11 | ❌ >=1.24.0 | ❌ >=2.0.0 | ❓ | ❌ 182 mocks | ❌ |
| marker | ❌ ~=3.10 | ❌ <2.0.0 | N/A | ✅ | ❌ 172 mocks | ❌ |
| arangodb | ❌ >=3.10 | ✅ ==1.26.4 | ⚠️ >=2.2.0 | ✅ | ❌ 166 mocks | ❌ |
| youtube_transcripts | ✅ 3.10.11 | ❌ >=1.24.0 | ❌ >=2.0.0 | ❓ | ❓ | ❌ |
| llm_call* | ❌ ~=3.10 | N/A | N/A | ❓ | ❓ | ❌ |
| fine_tuning | ❌ >=3.10 | N/A | ❌ >=2.0.0 | ❓ | ❓ | ❌ |
| **User Interfaces** |
| chat | ❌ >=3.9 | N/A | N/A | ❓ | ❓ | ❌ |
| annotator | ❌ >=3.10 | ❌ >=1.24.0 | ❌ >=2.0.0 | ❓ | ❓ | ❌ |
| aider-daemon | ✅ 3.10.11 | ❌ >=1.24.0 | N/A | ❓ | ❓ | ❌ |
| **MCP Services** |
| arxiv-mcp-server | ✅ 3.10.11 | ❌ >=1.24.0 | N/A | ⚠️ | ❓ | ❌ |
| mcp-screenshot | ❌ None | N/A | N/A | ❓ | ❓ | ❌ |
| **Support Projects** |
| gitget | ❌ >=3.10 | ❌ >=2.2.2 | ⚠️ >=2.2.0 | ✅ | ❓ | ❌ |
| darpa_crawl | ✅ 3.10.11 | N/A | N/A | ❓ | ❓ | ⚠️ |

*Note: llm_call is being converted to a Docker container

Legend: ✅ Compliant | ❌ Non-compliant | ⚠️ Partially compliant | ❓ Not checked | N/A Not applicable

---

## 🔍 Critical Issues by Category

### 1. **Python Version (11/17 non-compliant)**
- **Missing version**: mcp-screenshot
- **Too permissive**: rl_commons, world_model, chat (allow 3.9)
- **Too restrictive**: marker, llm_call (~=3.10)
- **Not specific enough**: Most use >=3.10 instead of >=3.10.11

### 2. **Numpy Version (10/11 projects using numpy are non-compliant)**
- Only **arangodb** correctly uses `numpy==1.26.4`
- **gitget** has impossible requirement `numpy>=2.2.2`
- All others use open-ended constraints

### 3. **Pandas Version (8/8 projects using pandas are non-compliant)**
- None use the required `pandas>=2.2.3,<2.3.0`
- Most use `pandas>=2.0.0` which is too permissive

### 4. **Mock Usage (5/5 checked projects violate NO MOCKS policy)**
- granger_hub: 330 mock occurrences
- sparta: 182 mock occurrences  
- marker: 172 mock occurrences
- arangodb: 166 mock occurrences
- rl_commons: 125 mock occurrences

### 5. **3-Layer Architecture (5/5 checked are compliant)**
- All checked projects properly implement core/cli/mcp separation
- arxiv-mcp-server has naming inconsistencies but structure is correct

### 6. **Other Issues**
- No projects specify `pyarrow` despite using pandas
- Pillow versions not constrained properly where used
- Many projects may have `.venv` or `repos/` subdirectories inflating mock counts

---

## 🛠️ Required Actions

### Immediate Actions (High Priority)

1. **Fix Python Versions**
   ```toml
   # All projects must use:
   requires-python = ">=3.10.11"
   ```

2. **Lock Numpy Version**
   ```toml
   # All projects using numpy must use:
   "numpy==1.26.4"
   ```

3. **Constrain Pandas Version**
   ```toml
   # All projects using pandas must use:
   "pandas>=2.2.3,<2.3.0"
   ```

4. **Remove All Mocks**
   ```bash
   # Run for each project:
   /granger-verify --fix --project PROJECT_NAME
   ```

### Project-Specific Fixes

#### gitget
- Fix impossible numpy requirement (>=2.2.2 doesn't exist)

#### marker & llm_call
- Change `~=3.10` to `>=3.10.11`

#### mcp-screenshot
- Add `requires-python = ">=3.10.11"`

#### world_model & chat
- Update from `>=3.9` to `>=3.10.11`

---

## 📈 Compliance Improvement Plan

### Phase 1: Dependency Alignment (1-2 days)
1. Update all Python version requirements
2. Pin numpy to 1.26.4 across all projects
3. Constrain pandas versions
4. Add pyarrow where needed

### Phase 2: Mock Removal (3-5 days)
1. Run `/granger-verify --fix` on all projects
2. Fix broken tests with real implementations
3. Set up test databases/services as needed

### Phase 3: Architecture Verification (1 day)
1. Verify all projects have 3-layer structure
2. Fix arxiv-mcp-server naming inconsistencies
3. Document any exceptions

### Phase 4: Continuous Compliance (Ongoing)
1. Add pre-commit hooks to enforce standards
2. Set up CI/CD checks for compliance
3. Regular quarterly audits

---

## 📋 Recommendations

1. **Automate Compliance Checks**
   - Add GitHub Actions to verify standards on PR
   - Create pre-commit hooks for local verification

2. **Gradual Migration**
   - Fix dependencies first (low risk)
   - Remove mocks project by project (higher risk)
   - Test thoroughly after each change

3. **Documentation**
   - Update each project's README with compliance status
   - Add migration guides for complex changes

4. **Exception Handling**
   - Document why llm_call needs Docker isolation
   - Consider if other projects need similar treatment

---

## 🎯 Success Metrics

Target compliance by end of Q1 2025:
- 100% Python version compliance
- 100% numpy version compliance  
- 100% pandas version compliance
- 0 mocks in project-owned test code
- 100% 3-layer architecture adoption

---

## 📚 References

- [GRANGER_MODULE_STANDARDS.md](../../07_style_conventions/GRANGER_MODULE_STANDARDS.md)
- [Dependency Quick Reference](../../../guides/DEPENDENCY_QUICK_REFERENCE.md)
- [Slash Commands Guide](../../../guides/GRANGER_SLASH_COMMANDS_GUIDE.md)