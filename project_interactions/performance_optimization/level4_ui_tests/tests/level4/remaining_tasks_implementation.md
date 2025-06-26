# Remaining Level 4 UI Tasks Implementation Guide

## Overview
This document provides implementation templates for the remaining 11 tasks (Tasks #11-20) of the GRANGER Level 4 UI testing suite.

## Task #011: Error Handling UI/UX

### Test Implementation
```typescript
// test_error_handling.spec.ts
test('011.1 - Consistent error styling across modules', async ({ page }) => {
  // Trigger errors in each module
  const modules = ['chat', 'annotator', 'terminal'];
  
  for (const module of modules) {
    await page.goto(`http://localhost:300${modules.indexOf(module)}/${module}`);
    
    // Trigger network error
    await page.route('**/api/**', route => route.abort());
    await page.click('button[data-action="fetch-data"]');
    
    // Verify error styling
    const errorElement = await page.waitForSelector('.error, [role="alert"]');
    const styles = await errorElement.evaluate(el => ({
      background: getComputedStyle(el).backgroundColor,
      color: getComputedStyle(el).color,
      border: getComputedStyle(el).border
    }));
    
    // Should use style guide error color
    expect(styles.color).toContain('#EF4444');
  }
});
```

## Task #012: Real-time Collaboration Features

### Key Tests
1. Live cursor sharing in annotator
2. Real-time chat updates via WebSocket
3. Terminal session sharing
4. Presence indicators
5. Conflict resolution UI

### Implementation Focus
- WebSocket performance < 100ms latency
- Smooth cursor animations
- Conflict resolution modals
- User presence avatars

## Task #013: Mobile Responsive Testing

### Device Viewports
```javascript
const devices = [
  { name: 'iPhone 12', width: 390, height: 844 },
  { name: 'iPad', width: 768, height: 1024 },
  { name: 'Pixel 5', width: 393, height: 851 }
];
```

### Key Validations
- Touch targets >= 44px
- Readable font sizes
- Proper gesture support
- Performance on mobile networks

## Task #014: Theme System Implementation

### Test Scenarios
1. Light/dark theme toggle
2. System preference detection
3. Theme persistence
4. Smooth transitions
5. Accessibility in both themes

## Task #015: Data Visualization Consistency

### Chart Testing
```typescript
test('015.1 - Consistent chart styles', async ({ page }) => {
  // Check D3/Chart.js styling
  const chart = await page.$('svg.chart, canvas.chart');
  
  // Verify style guide colors
  const colors = await chart.evaluate(() => {
    // Extract colors from chart elements
  });
  
  expect(colors).toContain('#4F46E5'); // Primary color
});
```

## Task #016: Search Experience Unification

### Components
- Unified search bar design
- Consistent result cards
- Cross-module search
- Search history
- Keyboard shortcuts (Cmd/Ctrl + K)

## Task #017: Notification System

### Requirements
- Toast notifications
- Notification center
- Priority-based positioning
- Entry/exit animations
- Sound preferences

## Task #018: User Onboarding Flow

### Flow Steps
1. Welcome modal
2. Interactive tutorial
3. Progress tracking
4. Tooltips
5. Completion celebration

### Metrics
- Completion rate > 80%
- Time to complete < 5 minutes
- User satisfaction

## Task #019: Performance Monitoring Dashboard

### Dashboard Components
```typescript
interface PerformanceMetrics {
  fps: number[];
  memory: number[];
  loadTime: number;
  apiLatency: number[];
  errorRate: number;
}
```

### Visualizations
- Real-time FPS graph
- Memory usage timeline
- API latency heatmap
- Error rate trends

## Task #020: Full E2E Workflow Validation

### Complete User Journey
```typescript
test('020.1 - Complete research workflow', async ({ page }) => {
  // 1. Search for research papers
  await page.goto('http://localhost:3000/chat');
  await page.type('.search', 'machine learning security');
  
  // 2. Open paper in annotator
  await page.click('.paper-result');
  await page.waitForURL('**/annotator');
  
  // 3. Create annotations
  await createAnnotation(page, 'Important finding');
  
  // 4. Run analysis in terminal
  await page.goto('http://localhost:3002/terminal');
  await page.type('.terminal', 'granger analyze annotations.json');
  
  // 5. Generate report
  await page.click('button:has-text("Generate Report")');
  
  // Verify complete workflow
  const report = await page.waitForSelector('.final-report');
  expect(report).toBeTruthy();
});
```

### Stress Testing
- 100+ annotations
- Large PDF files (50+ pages)
- Multiple concurrent users
- Network interruptions
- Memory leak detection

## Implementation Priority

### Week 4 (Current)
1. Task #011: Error Handling (Critical for UX)
2. Task #013: Mobile Testing (Wide user base)
3. Task #014: Theme System (Accessibility)

### Week 5
4. Task #016: Search Unification (Core feature)
5. Task #017: Notifications (User feedback)
6. Task #018: Onboarding (User retention)

### Week 6
7. Task #012: Collaboration (Advanced feature)
8. Task #015: Data Viz (Polish)
9. Task #019: Performance Dashboard (Monitoring)
10. Task #020: E2E Validation (Final verification)

## Success Criteria

### Performance
- All module loads < 2s
- Transitions < 500ms
- 60fps maintained
- Memory usage stable

### Accessibility
- WCAG AA compliant
- Keyboard navigable
- Screen reader support
- High contrast mode

### User Experience
- Intuitive navigation
- Consistent styling
- Clear error messages
- Smooth animations

## Testing Commands

```bash
# Run specific task
npm test tests/level4/features/test_task_011.spec.ts

# Run all remaining tasks
npm test tests/level4/features/

# Generate report
python scripts/generate_comprehensive_report.py

# Visual regression
npm run test:visual
```

## Next Steps

1. Implement each task following the patterns established in Tasks 1-10
2. Maintain real browser testing (no headless)
3. Capture screenshots for visual validation
4. Generate detailed reports for each task
5. Run full E2E validation as final step

The foundation is solid - these remaining tasks build upon the infrastructure already in place.