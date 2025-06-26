# GRANGER Storybook Implementation - Actionable Tasks

## 🚀 Implementation Tasks for Storybook Integration

Based on the comprehensive analysis, here are the concrete tasks to implement Storybook for GRANGER's web-based UI modules.

## Phase 1: Core Setup (Week 1)

### Task 1: Initialize Storybook in Granger UI System
```bash
# Location: /home/graham/workspace/granger-ui/
cd /home/graham/workspace/granger-ui/

# Initialize Storybook
npx storybook@latest init --type react --yes

# Install essential addons
npm install --save-dev @storybook/addon-a11y \
  @storybook/addon-interactions \
  @storybook/test-runner \
  @storybook/addon-docs \
  @storybook/addon-viewport \
  @storybook/addon-measure \
  @storybook/addon-outline
```

### Task 2: Configure Storybook for GRANGER
Create `.storybook/main.js`:
```javascript
module.exports = {
  stories: [
    "../src/**/*.stories.@(js|jsx|ts|tsx|mdx)",
    "../src/**/*.story.@(js|jsx|ts|tsx|mdx)"
  ],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
    "@storybook/addon-interactions",
    "@storybook/addon-viewport",
    "@storybook/addon-measure",
    "@storybook/addon-outline"
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {}
  },
  features: {
    storyStoreV7: true,
    buildStoriesJson: true
  }
};
```

### Task 3: Create Style Guide Decorator
Create `.storybook/decorators/StyleGuideDecorator.tsx`:
```typescript
import React, { useEffect } from 'react';
import { STYLE_GUIDE } from '../../src/utils/style-guide';

export const StyleGuideDecorator = (Story: any) => {
  useEffect(() => {
    // Validate style guide compliance
    const validateColors = () => {
      const elements = document.querySelectorAll('*');
      const violations = [];
      
      elements.forEach(el => {
        const styles = window.getComputedStyle(el);
        const bgColor = styles.backgroundColor;
        const color = styles.color;
        
        // Check background colors
        if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
          const isValid = Object.values(STYLE_GUIDE.colors)
            .some(validColor => bgColor.includes(validColor));
          
          if (!isValid) {
            violations.push({
              element: el,
              property: 'backgroundColor',
              value: bgColor
            });
          }
        }
      });
      
      if (violations.length > 0) {
        console.warn('Style Guide Violations:', violations);
      }
    };
    
    // Run validation after render
    setTimeout(validateColors, 100);
  }, []);
  
  return (
    <div className="granger-storybook-wrapper">
      <Story />
    </div>
  );
};
```

### Task 4: Create First Core Component Stories
Create `src/components/Button/Button.stories.tsx`:
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta: Meta<typeof Button> = {
  title: 'Core/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Core button component following 2025 Style Guide'
      }
    }
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger', 'ghost']
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg']
    },
    disabled: {
      control: 'boolean'
    }
  }
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me'
  }
};

// Interactive story with play function
export const InteractiveButton: Story = {
  args: {
    variant: 'primary',
    children: 'Interactive Button'
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');
    
    // Test hover state
    await userEvent.hover(button);
    await expect(button).toHaveStyle('transform: translateY(-1px)');
    
    // Test click
    await userEvent.click(button);
    await expect(button).toHaveFocus();
  }
};

// All variants
export const AllVariants: Story = {
  render: () => (
    <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="danger">Danger</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  )
};

// Loading state
export const Loading: Story = {
  args: {
    loading: true,
    children: 'Loading...'
  }
};
```

## Phase 2: Module Integration (Week 2)

### Task 5: Chat Module Stories
Create stories for Chat module components:

```typescript
// chat/MessageList.stories.tsx
export default {
  title: 'Chat/MessageList',
  component: MessageList,
  parameters: {
    layout: 'fullscreen'
  }
};

export const EmptyState: Story = {
  args: {
    messages: []
  }
};

export const WithMessages: Story = {
  args: {
    messages: [
      { id: 1, type: 'user', text: 'Hello GRANGER!' },
      { id: 2, type: 'ai', text: 'Hello! How can I help you today?' }
    ]
  }
};

export const TypingIndicator: Story = {
  args: {
    messages: [],
    showTyping: true
  }
};

export const ErrorState: Story = {
  args: {
    messages: [],
    error: 'Failed to connect to chat service'
  }
};
```

### Task 6: Annotator Module Stories
Create stories for Annotator components:

```typescript
// annotator/PDFViewer.stories.tsx
export default {
  title: 'Annotator/PDFViewer',
  component: PDFViewer,
  parameters: {
    layout: 'fullscreen',
    viewport: {
      defaultViewport: 'desktop'
    }
  }
};

export const LoadingPDF: Story = {
  args: {
    loading: true
  }
};

export const WithAnnotations: Story = {
  args: {
    document: mockPDFData,
    annotations: [
      {
        id: 'ann1',
        pageNumber: 1,
        text: 'Important finding',
        position: { x: 100, y: 200, width: 200, height: 50 },
        color: '#6366F1'
      }
    ]
  }
};

export const CollaborativeAnnotations: Story = {
  args: {
    document: mockPDFData,
    collaborators: [
      { id: 'user1', name: 'Alice', color: '#10B981' },
      { id: 'user2', name: 'Bob', color: '#F59E0B' }
    ],
    showCursors: true
  }
};
```

### Task 7: WebSocket State Stories
Create stories for real-time features:

```typescript
// shared/WebSocketIndicator.stories.tsx
export const ConnectionStates: Story = {
  render: () => {
    const [state, setState] = useState('connecting');
    
    useEffect(() => {
      const states = ['connecting', 'connected', 'disconnected', 'error'];
      let index = 0;
      
      const interval = setInterval(() => {
        index = (index + 1) % states.length;
        setState(states[index]);
      }, 2000);
      
      return () => clearInterval(interval);
    }, []);
    
    return <WebSocketIndicator connectionState={state} />;
  }
};
```

## Phase 3: Testing Integration (Week 3)

### Task 8: Set Up Visual Regression Testing
Create `.storybook/test-runner.js`:
```javascript
const { getStoryContext } = require('@storybook/test-runner');
const { injectAxe, checkA11y } = require('axe-playwright');

module.exports = {
  async preRender(page, context) {
    await injectAxe(page);
  },
  
  async postRender(page, context) {
    // Visual regression snapshot
    await page.screenshot({
      path: `screenshots/${context.id}.png`,
      fullPage: true
    });
    
    // Accessibility check
    await checkA11y(page, '#root', {
      detailedReport: true,
      detailedReportOptions: {
        html: true
      }
    });
    
    // Performance check
    const metrics = await page.evaluate(() => ({
      fps: window.fpsMonitor?.fps || 60,
      renderTime: performance.now()
    }));
    
    if (metrics.fps < 55) {
      throw new Error(`Low FPS detected: ${metrics.fps}`);
    }
  }
};
```

### Task 9: Create Interaction Test Suite
```typescript
// Create test scenarios that replace Playwright tests
export const CompleteUserFlow: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // User types in chat
    const input = canvas.getByPlaceholderText('Type your message...');
    await userEvent.type(input, 'Analyze document.pdf');
    await userEvent.keyboard('{Enter}');
    
    // Wait for response
    await waitFor(() => {
      expect(canvas.getByText(/Opening in annotator/)).toBeInTheDocument();
    });
    
    // Click annotator link
    const link = canvas.getByRole('link', { name: /annotator/i });
    await userEvent.click(link);
    
    // Verify navigation intent
    expect(link).toHaveAttribute('href', expect.stringContaining('/annotator'));
  }
};
```

### Task 10: CI/CD Integration
Create `.github/workflows/storybook.yml`:
```yaml
name: Storybook Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: npm ci
        
      - name: Build Storybook
        run: npm run build-storybook
        
      - name: Run Storybook tests
        run: |
          npx concurrently -k \
            "npm run storybook -- --no-open" \
            "npx wait-on http://localhost:6006 && npm run test-storybook"
            
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: storybook-screenshots
          path: screenshots/
```

## Phase 4: Documentation & Training (Week 4)

### Task 11: Create Component Documentation
```typescript
// Button.mdx
import { Meta, Story, Canvas, ArgsTable } from '@storybook/addon-docs';
import { Button } from './Button';

<Meta title="Core/Button/Documentation" />

# Button Component

The Button component follows the 2025 Style Guide and provides consistent interaction patterns across GRANGER.

## Usage

```jsx
import { Button } from '@granger/ui';

<Button variant="primary" onClick={handleClick}>
  Click me
</Button>
```

## Style Guide Compliance

- Primary color: `#4F46E5` → `#6366F1` (gradient)
- Border radius: 8px
- Padding: 12px 24px (follows 8px grid)
- Animation: 250ms ease-in-out

<Canvas>
  <Story id="core-button--primary" />
</Canvas>

<ArgsTable of={Button} />
```

### Task 12: Create Team Guidelines
Create `docs/STORYBOOK_GUIDELINES.md`:
```markdown
# GRANGER Storybook Guidelines

## Writing Stories

1. **One story per state**: Create separate stories for each component state
2. **Use play functions**: Test interactions directly in stories
3. **Follow naming convention**: `ComponentName.stories.tsx`
4. **Include all edge cases**: Loading, error, empty states

## Story Structure

```typescript
// 1. Meta configuration
const meta: Meta<typeof Component> = {
  title: 'Category/Component',
  component: Component,
  tags: ['autodocs']
};

// 2. Default export
export default meta;

// 3. Type for stories
type Story = StoryObj<typeof meta>;

// 4. Stories
export const Default: Story = {
  args: {
    // props
  }
};
```

## Testing in Storybook

- Use interaction tests instead of separate test files
- Visual regression runs automatically
- Accessibility checks on every story
- Performance monitoring integrated
```

## Success Metrics & Monitoring

### Metrics to Track
1. **Story Coverage**: % of components with stories
2. **Test Migration**: % of Playwright tests migrated
3. **Build Time**: Storybook build performance
4. **Visual Regression**: Number of unintended changes caught
5. **Developer Adoption**: Story creation rate

### Weekly Goals
- Week 1: 20% component coverage
- Week 2: 50% component coverage
- Week 3: 80% component coverage
- Week 4: 100% core components covered

## Commands Reference

```bash
# Development
npm run storybook                # Start Storybook dev server
npm run build-storybook         # Build static Storybook

# Testing
npm run test-storybook          # Run interaction tests
npm run test-storybook:watch    # Watch mode
npm run chromatic              # Visual regression testing

# Utilities
npm run storybook:extract      # Extract stories metadata
npm run storybook:stats        # Component coverage stats
```

## Next Steps

1. **Immediate**: Set up Storybook in granger-ui repository
2. **This Week**: Create stories for Button, Input, Card components
3. **Next Week**: Migrate Chat module components
4. **Following Week**: Migrate Annotator module components
5. **Month End**: Full test suite migration complete

This implementation plan provides concrete, actionable tasks that will transform GRANGER's UI testing from complex Playwright tests to maintainable, visual Storybook stories.