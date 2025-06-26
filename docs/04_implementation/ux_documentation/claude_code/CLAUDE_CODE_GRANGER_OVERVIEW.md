# 🚀 GRANGER System Overview for Claude Code

**Document Version**: 1.0.0  
**Created**: 2025-06-04  
**Purpose**: Complete system context for Claude Code to continue GRANGER development

---

## 🎯 System Architecture

### Core Concept
GRANGER is a distributed AI system with multiple specialized modules communicating through a hub-and-spoke architecture. Each module serves a specific purpose while maintaining loose coupling for flexibility.

### System Components

The system consists of:
- GRANGER Hub (Central Command) - WebSocket Server on Port 8765
- Chat Interface (Port 3000)
- Marker Ground Truth (Port 3001)
- Claude Module Communicator
- Aider Daemon (Terminal UI)
- ArXiv MCP Server
- Future modules (planned)

All modules connect to the central hub for communication and coordination.

### Directory Structure

/home/graham/workspace/
- granger-ui/ (NEW: Unified UI monorepo)
  - packages/ui-core/ (Design tokens, shared utilities)
  - packages/ui-web/ (React components for web)
  - packages/ui-terminal/ (React Ink components for terminal)
  - apps/web-showcase/ (Component demonstration)
  - apps/storybook/ (Interactive documentation)

- central_command/ (Hub server implementation)
  - server.py (WebSocket hub)

- experiments/
  - chat/ (Chat interface module)
  - marker_ground_truth/ (Data annotation module)
  - claude_module_communicator/ (Claude integration)
  - arxiv_mcp/ (ArXiv research module)
  - aider_daemon/ (Git integration module)

- shared_claude_docs/ (System documentation)
  - docs/ (All documentation)
  - guides/ (Style guides, standards)

---

## 🔄 Current State (June 2025)

### What's Working
1. **UI Component Library** (95% complete)
   - 14 unified components across web and terminal
   - Consistent design language
   - TypeScript throughout

2. **Hub Architecture** (80% complete)
   - WebSocket communication established
   - Module registration working
   - Real-time data flow

3. **Individual Modules** (60% complete)
   - Chat Interface: Functional, needs UI migration
   - Marker Ground Truth: Working prototype
   - Claude Module: Basic integration
   - ArXiv MCP: Research capabilities

### What Needs Work
1. **Module Integration** (40% complete)
   - Standardize communication protocols
   - Implement error handling
   - Add authentication

2. **Testing Infrastructure** (20% complete)
   - Unit tests needed
   - Integration tests critical
   - Performance benchmarks

3. **Deployment Pipeline** (0% complete)
   - Docker containers needed
   - CI/CD pipeline
   - Production configuration

---

## 🎨 UI Unification Status

### Completed
- Component library created (ui-web, ui-terminal)
- Design system documented
- Migration strategy proven
- Storybook documentation

### In Progress
- Chat Interface migration (compatibility wrappers ready)
- Marker Ground Truth migration (planning phase)
- Terminal build configuration (React version issues)

### Next Steps
1. Complete Chat Interface migration
2. Migrate Marker Ground Truth UI
3. Create Aider Daemon terminal interface
4. Implement theming system

---

## 🚀 Critical Next Phase Tasks

### 1. Complete UI Migration (Week 1)
```bash
# Chat Interface
cd /home/graham/workspace/experiments/chat/frontend
npm install @granger/ui-web
# Run migration script
./migrate-buttons.sh

# Test the migration
npm run dev
```

### 2. Fix Terminal Build (Week 1)
```bash
# Try alternative build approach
cd /home/graham/workspace/granger-ui/packages/ui-terminal
# Consider using tsup or esbuild instead of tsc
```

### 3. Implement Module Communication Standards (Week 2)
- Create message type definitions
- Implement error handling
- Add retry logic
- Create health checks

### 4. Testing Infrastructure (Week 2)
- Set up Jest for unit tests
- Playwright for E2E tests
- Performance benchmarks
- Visual regression tests

### 5. Production Readiness (Week 3-4)
- Docker containers for each module
- Environment configuration
- Logging and monitoring
- Security hardening

---

## 📝 Key Files to Review

1. **Task Tracking**
   - /docs/000_UNIFIED_TASKS_LIST.md - Master task list
   - /docs/001_NEXT_ACTIONS.md - Immediate priorities

2. **Architecture**
   - /docs/00_GRANGER_OVERVIEW.md - System design
   - /docs/02_technical_stack/HUB_SPOKE_PATTERN.md - Communication

3. **UI System**
   - /docs/03_ui_unification/README.md - UI strategy
   - /guides/2025_STYLE_GUIDE.md - Design standards

4. **Progress Reports**
   - /docs/UI_UNIFICATION_PROGRESS.md - Current status
   - /docs/CHAT_MIGRATION_PLAN.md - Migration strategy

---

## 🔧 Development Commands

### Start the Hub
```bash
cd /home/graham/workspace/central_command
python server.py
```

### Run UI Development
```bash
cd /home/graham/workspace/granger-ui
pnpm install
pnpm dev  # Runs all packages in dev mode
```

### Test Individual Modules
```bash
# Chat Interface
cd /home/graham/workspace/experiments/chat
npm run dev

# Marker Ground Truth
cd /home/graham/workspace/experiments/marker_ground_truth
npm run dev
```

---

## ⚠️ Known Issues & Solutions

### Issue 1: Terminal Package Build
**Problem**: React version mismatch (v18 vs v19)
**Solution**: Use separate build process or compatibility layer

### Issue 2: WebSocket Reliability
**Problem**: Connections drop without reconnection
**Solution**: Implement reconnection logic with exponential backoff

### Issue 3: State Synchronization
**Problem**: Module states can drift
**Solution**: Implement event sourcing or state snapshots

---

## 🎯 Success Metrics

1. **All modules using unified UI** (Target: 100%)
2. **Test coverage** (Target: >80%)
3. **Performance** (Target: <100ms response)
4. **Uptime** (Target: 99.9%)
5. **Documentation** (Target: 100% API coverage)

---

## 💡 Architecture Decisions

1. **Monorepo for UI**: Ensures consistency
2. **Hub-and-Spoke**: Allows module independence
3. **TypeScript First**: Type safety critical
4. **React for All UIs**: Single framework
5. **WebSocket Communication**: Real-time updates

---

## 🚦 Go/No-Go Criteria for Production

- [ ] All modules integrated with hub
- [ ] UI migration complete
- [ ] Test coverage >80%
- [ ] Performance targets met
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Deployment automated

---

**Next Review Date**: June 11, 2025
**Contact**: graham@granger-aerospace.com
'EOF'