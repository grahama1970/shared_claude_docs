# Task 010: Fix UI Project Dependencies and Tests

**Status**: 🟡 In Progress  
**Priority**: Critical  
**Category**: Infrastructure Setup  
**Created**: 2025-01-06  
**Dependencies**: Task 009 (UI Testing)  

## 🎯 Objective

Fix all failing tests in UI projects by installing dependencies, removing deprecated code, and ensuring basic functionality for Level 0-4 interaction testing. This is critical for testing the scenarios in `/project_interactions` and `/granger_hub/scenarios`.

## 📋 Success Criteria

- [ ] All UI project dependencies installed
- [ ] Deprecated tests removed or archived
- [ ] Basic tests passing for each project
- [ ] Projects can be imported and used in interaction scenarios
- [ ] No mock usage in tests (per TEST_VERIFICATION_TEMPLATE_GUIDE)

## 🚀 Implementation Tasks

### Phase 1: Granger-UI Fixes

#### Task 1.1: Install Dependencies
```bash
cd /home/graham/workspace/granger-ui
pnpm install --frozen-lockfile
```

#### Task 1.2: Fix Test Issues
- [ ] Verify Jest is installed in ui-web
- [ ] Fix any import path issues
- [ ] Remove deprecated tests
- [ ] Ensure basic component tests pass

#### Task 1.3: Verify Basic Functionality
- [ ] Components can be imported
- [ ] Design tokens accessible
- [ ] No runtime errors

### Phase 2: Annotator Fixes

#### Task 2.1: Install Dependencies
```bash
cd /home/graham/workspace/experiments/annotator
uv sync
```

#### Task 2.2: Fix Missing Dependencies
- [ ] Install websockets: `uv add websockets`
- [ ] Install sklearn: `uv add scikit-learn`
- [ ] Install playwright: `uv add playwright`
- [ ] Run `playwright install`

#### Task 2.3: Remove/Fix Deprecated Tests
- [ ] Archive tests requiring unavailable services
- [ ] Fix import errors in remaining tests
- [ ] Ensure PDF processing tests work

### Phase 3: Chat Interface Fixes

#### Task 3.1: Backend Dependencies
```bash
cd /home/graham/workspace/experiments/chat
uv sync
```

#### Task 3.2: Frontend Dependencies
```bash
cd frontend
npm install
```

#### Task 3.3: Fix Code Issues
- [ ] Fix import aliases in frontend (@ imports)
- [ ] Update tsconfig paths or use relative imports
- [ ] Fix Docker configuration
- [ ] Remove mock-based tests

### Phase 4: Aider-Daemon Fixes

#### Task 4.1: Install Dependencies
```bash
cd /home/graham/workspace/experiments/aider-daemon
uv sync
```

#### Task 4.2: Handle Git Dependencies
- [ ] Install git dependencies manually if needed
- [ ] Fix import errors
- [ ] Ensure CLI entry point works

#### Task 4.3: Keep Honeypot Tests
- [ ] Honeypot tests should fail (working as designed)
- [ ] Fix only real functionality tests

### Phase 5: Verification

#### Task 5.1: Run Basic Import Tests
```python
# Test each project can be imported
import sys
sys.path.insert(0, '/home/graham/workspace/granger-ui/packages/ui-core/src')
sys.path.insert(0, '/home/graham/workspace/experiments/annotator/src')
sys.path.insert(0, '/home/graham/workspace/experiments/chat/backend')
sys.path.insert(0, '/home/graham/workspace/experiments/aider-daemon/src')
```

#### Task 5.2: Test Interaction Readiness
- [ ] Can create instances of key classes
- [ ] Basic operations work
- [ ] No critical runtime errors

## 🎯 Priority Order

1. **aider-daemon** - Most mature, needed for many scenarios
2. **annotator** - PDF processing critical for document scenarios
3. **chat** - Interface for user interactions
4. **granger-ui** - Design system (lower priority for functionality)

## 🔄 Dependencies

- Python 3.10+ with uv installed
- Node.js 18+ with npm/pnpm
- Playwright browsers (for UI testing)
- Git (for git-based dependencies)

## ✅ Completion Checklist

- [ ] All dependencies installed
- [ ] No import errors
- [ ] Basic functionality verified
- [ ] Deprecated tests removed/archived
- [ ] Ready for Level 0-4 interaction testing

## 📝 Notes

- Focus on getting basic functionality working
- Don't worry about 100% test coverage
- Prioritize real functionality over test perfection
- Keep honeypot tests (they should fail)
- Remove all mock-based tests per guidelines