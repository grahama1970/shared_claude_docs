# 🔄 Chat Interface Migration Plan

**Document Version**: 1.0.0  
**Created**: 2025-06-03 21:15 EST  
**Status**: Planning Phase  

---

## 📋 Overview

This document outlines the migration plan for transitioning the Chat interface from its current implementation to use the unified GRANGER UI component library.

---

## 🎯 Migration Scope

### Current State Analysis
The Chat interface currently has:
1. **Local UI components** in /frontend/src/components/ui/
   - Button2025.jsx - Custom button with loading states
   - Card.jsx - Simple card wrapper
   
2. **Dashboard components** in /frontend/src/components/dashboard/
   - MetricsCards.jsx
   - PipelineStatus.jsx
   - EmbeddedDashboardV2.jsx
   - Multiple dashboard views

3. **Chat-specific components** in /frontend/src/components/chat/
   - SmartChatInput.jsx
   - MessageRenderer.jsx
   - Dialog.jsx
   - Various chat UI elements

---

## 🗺️ Migration Strategy

### Phase 1: Component Mapping
Map existing components to unified library equivalents:

| Current Component | Unified Component | Notes |
|------------------|-------------------|-------|
| Button2025.jsx | @granger/ui-web/Button | Need to preserve gradient variant |
| Card.jsx | @granger/ui-web/Card | Direct replacement |
| Custom inputs | @granger/ui-web/Input | Add chat-specific styling |
| Dropdowns | @granger/ui-web/Select | Ensure search functionality |
| Dialog.jsx | @granger/ui-web/Modal | May need custom animations |

### Phase 2: Implementation Steps

1. **Setup** (Day 1)
   - Add @granger/ui-web dependency to Chat project
   - Configure build system to handle workspace packages
   - Set up CSS imports for Tailwind styles

2. **Core Components** (Day 2)
   - Replace Button2025 with unified Button
   - Replace Card with unified Card
   - Update imports throughout codebase
   - Test functionality

3. **Dashboard Migration** (Day 3)
   - Migrate MetricsCards to use unified MetricCard
   - Update dashboard layouts to use SharedDashboard
   - Ensure WebSocket integration works

4. **Chat Components** (Day 4)
   - Create ChatInput component using unified Input
   - Update message rendering with unified components
   - Migrate dialogs to unified Modal

5. **Testing & Polish** (Day 5)
   - End-to-end testing
   - Performance optimization
   - Visual regression testing
   - Documentation updates

---

## 🔧 Technical Considerations

### Build System Updates
The package.json will need updates to reference workspace packages.

### Import Path Updates
Components will need to be imported from @granger/ui-web instead of local paths.

### Style Migration
- Ensure Tailwind config includes ui-web paths
- Migrate custom CSS to use design tokens
- Update any inline styles to use utility classes

---

## ⚠️ Risk Mitigation

### Potential Issues
1. **Breaking Changes**
   - Keep old components during transition
   - Use feature flags for gradual rollout

2. **Performance Impact**
   - Monitor bundle size changes
   - Ensure tree-shaking works properly

3. **Visual Differences**
   - Create visual comparison tests
   - Document any intentional changes

### Rollback Strategy
- Git branch protection for main
- Tagged releases before major changes
- Ability to revert package versions

---

## 📊 Success Metrics

- [ ] All UI components migrated
- [ ] No visual regressions
- [ ] Bundle size reduced by >10%
- [ ] Consistent styling across all views
- [ ] Zero runtime errors
- [ ] Performance metrics maintained

---

## 🚀 Next Steps

1. Get approval on migration plan
2. Create feature branch for migration
3. Begin Phase 1 implementation
4. Daily progress updates
5. Demo after each phase

---

## 📚 Resources

- Unified UI Components: /home/graham/workspace/granger-ui/packages/ui-web/
- Chat Interface: /home/graham/workspace/experiments/chat/frontend/
- Style Guide: /home/graham/workspace/shared_claude_docs/guides/2025_STYLE_GUIDE.md
'EOF'