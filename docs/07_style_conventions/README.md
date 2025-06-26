# Granger Style Conventions and Standards

> **Central location for all Granger ecosystem development standards**  
> **Last Updated**: 2025-01-09

---

## 📋 Quick Navigation

### Core Standards
1. **[GRANGER_MODULE_STANDARDS.md](./GRANGER_MODULE_STANDARDS.md)** 🚨 MANDATORY
   - Package management (UV only)
   - Dependency constraints (numpy==1.26.4)
   - Project structure (3-layer architecture)
   - Testing requirements (NO MOCKS)
   - Hub integration patterns

2. **[GRANGER_MONOREPO_ARCHITECTURE.md](./GRANGER_MONOREPO_ARCHITECTURE.md)**
   - Distributed monorepo management
   - MCP microservice patterns
   - Cross-module testing strategies
   - Deployment coordination

3. **[3_LAYER_ARCHITECTURE.md](../01_strategy/architecture/3_LAYER_ARCHITECTURE.md)**
   - Core/CLI/MCP separation
   - Refactoring guidelines
   - Validation patterns

### Quick References
- **[Dependency Quick Reference](../../guides/DEPENDENCY_QUICK_REFERENCE.md)** ⚡
  - Common dependency errors and fixes
  - Diagnostic commands
  - Emergency procedures

- **[Module Standards Cheat Sheet](./GRANGER_MODULE_STANDARDS.md#✅-compliance-checklist)**
  - Pre-commit checklist
  - Common mistakes to avoid

---

## 🎯 Key Principles

### 1. **Consistency Over Flexibility**
All modules follow identical standards to ensure seamless integration.

### 2. **Real Testing Over Mocking**
Never mock internal services - broken tests reveal real integration issues.

### 3. **Living at HEAD**
Modules depend on latest commits, not published versions.

### 4. **Hub-Centric Communication**
All cross-module communication goes through the Granger Hub.

---

## 🚀 Getting Started

### For New Modules
1. Read [GRANGER_MODULE_STANDARDS.md](./GRANGER_MODULE_STANDARDS.md) completely
2. Use the [pyproject.toml template](./GRANGER_MODULE_STANDARDS.md#pyprojecttoml-template)
3. Follow the [3-layer architecture](../01_strategy/architecture/3_LAYER_ARCHITECTURE.md)
4. Implement [required MCP prompts](./GRANGER_MODULE_STANDARDS.md#required-mcp-prompts)

### For Existing Modules
1. Run compliance check: `/granger-verify --project module-name`
2. Fix dependency versions per [standards](./GRANGER_MODULE_STANDARDS.md#dependency-constraints)
3. Remove all mocks: `/granger-verify --fix --project module-name`
4. Update imports to absolute paths

---

## 📊 Standards Compliance Matrix

| Standard | Required | Automated Check | Fix Command |
|----------|----------|----------------|-------------|
| Python 3.10.11 | ✅ | Yes | `uv venv --python=3.10.11` |
| numpy==1.26.4 | ✅ | Yes | `uv add numpy==1.26.4` |
| UV package manager | ✅ | Yes | N/A |
| No mocks in tests | ✅ | Yes | `/granger-verify --fix` |
| 3-layer architecture | ✅ | Partial | Manual refactor |
| MCP prompts | ✅ | Yes | Use templates |
| Absolute imports | ✅ | Yes | `/granger-verify --fix` |

---

## 🔧 Tools and Commands

### Verification
```bash
# Check single module
/granger-verify --project module-name

# Fix common issues automatically
/granger-verify --fix --project module-name

# Check all modules
/granger-verify --all
```

### Development
```bash
# Set up new module
/granger:new-module --name module-name

# Update dependencies across ecosystem
/granger:update-dependency package==version

# Run cross-module tests
/granger:test --ecosystem
```

---

## 📈 Evolution of Standards

### Version 1.0.0 (2025-01-09)
- Initial standards based on dependency resolution lessons
- Established numpy==1.26.4 as ecosystem standard
- Defined NO MOCKS testing policy
- Created 3-layer architecture requirement

### Planned Improvements
- [ ] Automated module scaffolding
- [ ] Dependency conflict pre-check
- [ ] Cross-module refactoring tools
- [ ] Service mesh integration

---

## 🆘 Getting Help

### Common Issues
1. **Dependency conflicts** → [Dependency Quick Reference](../../guides/DEPENDENCY_QUICK_REFERENCE.md)
2. **Test failures** → [Test Lessons Summary](../../guides/GRANGER_TEST_LESSONS_SUMMARY.md)
3. **Module integration** → [Hub Integration Guide](../../guides/GRANGER_HUB_INTEGRATION_GUIDE.md)

### Contact
- Create issue in shared_claude_docs for standards questions
- Use `/granger:help` for immediate assistance
- Check [Lessons Learned](../../docs/06_operations/maintenance/) for historical context

---

## 📜 License

All standards and conventions are MIT licensed and mandatory for Granger ecosystem modules.