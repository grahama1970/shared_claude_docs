# Level 4 Interactions - Quick Reference

## What is Level 4?

Level 4 extends the GRANGER interaction model to include **real human users** interacting through **browser-based UI modules** with full visual validation, style guide compliance, and adaptive behavior.

## Key Components

### UI Modules
1. **Chat** - Natural language interface
2. **Annotator** - Document analysis and markup
3. **Terminal** - Developer command-line interface

### Core Features
- 🎨 **Style Guide Compliance** - 2025 Modern UX standards
- 🚀 **Performance Targets** - 60fps, <500ms transitions
- ♿ **Accessibility First** - WCAG AA compliance
- 🤖 **RL Adaptation** - UI learns from user behavior
- 👥 **Real-time Collaboration** - Multi-user support
- 📱 **Responsive Design** - Works on all devices

## Testing with Playwright

### Setup
```bash
npm install -D @playwright/test
npx playwright install
```

### Example Test
```javascript
test('Cross-module navigation', async ({ page }) => {
  await page.goto('/chat');
  await page.click('[data-testid="open-annotator"]');
  await expect(page).toHaveURL('/annotator');
  // Verify context preserved
});
```

## Performance Requirements

| What | Target | How to Measure |
|------|--------|----------------|
| Load Time | < 2s | Lighthouse |
| Switch Time | < 500ms | Performance API |
| Animations | 60fps | DevTools |
| Memory | < 500MB | Heap Profiler |

## Style Guide Essentials

- **Colors**: #4F46E5 (primary), #10B981 (accent)
- **Font**: Inter, system-ui
- **Spacing**: 8px grid
- **Animations**: 150-300ms ease-in-out

## RL Integration Points

1. **Track**: User actions → RL states
2. **Adapt**: RL agent → UI configuration
3. **Learn**: User satisfaction → Rewards
4. **Improve**: Continuous optimization

## Common Workflows

### Research Flow
Chat → Search papers → Annotator → Highlight → Terminal → Analyze

### Collaboration Flow
User A (Terminal) → Start task → User B (Chat) notified → Real-time sync

### Adaptive Flow
New user → Track patterns → RL learns → Personalized shortcuts

## Checklist for Implementation

- [ ] Playwright tests for all user journeys
- [ ] Visual regression baseline screenshots
- [ ] Style guide validation utilities
- [ ] Performance monitoring setup
- [ ] RL Commons integration
- [ ] Cross-module navigation
- [ ] Context preservation
- [ ] Accessibility audit
- [ ] Mobile testing
- [ ] Load testing

## File Locations

- **Chat UI**: /home/graham/workspace/experiments/chat/
- **Annotator UI**: /home/graham/workspace/experiments/marker-ground-truth/
- **Terminal UI**: /home/graham/workspace/experiments/aider-daemon/
- **Task List**: /home/graham/workspace/shared_claude_docs/docs/tasks/101_GRANGER_LEVEL_4_UI_INTERACTIONS_TASKS.md
- **Full Guide**: /home/graham/workspace/shared_claude_docs/docs/01_core_concepts/MODULE_INTERACTION_LEVELS_EXTENDED.md

## Quick Commands

```bash
# Run Level 4 tests
playwright test tests/level4/

# Check style compliance
npm run check:styles

# Performance profiling
npm run profile:performance

# Accessibility audit
npm run audit:a11y
```

---
*For detailed information, see MODULE_INTERACTION_LEVELS_EXTENDED.md*
