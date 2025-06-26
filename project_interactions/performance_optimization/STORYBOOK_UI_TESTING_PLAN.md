# GRANGER Storybook UI Testing Integration Plan

## Overview
Based on the storybook_ui_testing.md documentation, Storybook is the ideal solution for GRANGER's UI testing needs. It provides component isolation, visual documentation, and comprehensive testing capabilities that align perfectly with our Level 4 UI requirements.

## Why Storybook for GRANGER?

### Current Challenges
1. **Complex E2E Tests**: Our Playwright tests are becoming complex and prone to JavaScript errors
2. **Component Reusability**: Need better documentation for shared UI components
3. **Visual Regression**: Manual screenshot comparison is time-consuming
4. **Style Guide Compliance**: Need automated validation of 2025 Style Guide

### Storybook Solutions
1. **Component Isolation**: Test each UI component independently
2. **Visual Documentation**: Auto-generated component library
3. **Interaction Testing**: Test user workflows without full app setup
4. **Addon Ecosystem**: Accessibility, visual regression, performance monitoring

## UI Modules to Integrate

### 1. Chat Module
- **Path**: `/home/graham/workspace/experiments/chat/`
- **Components**: ChatInput, MessageList, AIResponse, SearchBar
- **Stories**: Different conversation states, error states, loading states

### 2. Annotator Module (marker-ground-truth)
- **Path**: `/home/graham/workspace/experiments/marker-ground-truth/`
- **Components**: PDFViewer, AnnotationToolbar, HighlightOverlay, CommentBox
- **Stories**: Document states, annotation types, collaboration views

### 3. Terminal Module (aider-daemon)
- **Path**: `/home/graham/workspace/experiments/aider-daemon/`
- **Components**: Terminal, CommandInput, OutputDisplay, SyntaxHighlighter
- **Stories**: Command execution, error outputs, syntax highlighting

## Implementation Strategy

### Phase 1: Setup & Infrastructure
```bash
# Install Storybook in each module
npx storybook@latest init

# Install testing addons
npm install --save-dev @storybook/addon-a11y
npm install --save-dev @storybook/addon-interactions
npm install --save-dev @storybook/test-runner
npm install --save-dev @storybook/addon-visual-tests
```

### Phase 2: Component Stories

#### Chat Module Example
```typescript
// chat/src/stories/ChatInput.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ChatInput } from '../components/ChatInput';

const meta: Meta<typeof ChatInput> = {
  title: 'Chat/ChatInput',
  component: ChatInput,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    placeholder: { control: 'text' },
    disabled: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: 'Type your message...',
  },
};

export const Disabled: Story = {
  args: {
    placeholder: 'Chat is disabled',
    disabled: true,
  },
};

export const WithError: Story = {
  args: {
    placeholder: 'Type your message...',
    error: 'Network connection lost',
  },
};
```

#### Annotator Module Example
```typescript
// annotator/src/stories/AnnotationToolbar.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { AnnotationToolbar } from '../components/AnnotationToolbar';

const meta: Meta<typeof AnnotationToolbar> = {
  title: 'Annotator/Toolbar',
  component: AnnotationToolbar,
  parameters: {
    backgrounds: {
      default: 'light',
    },
  },
};

export default meta;

export const Default: Story = {};

export const WithActiveHighlight: Story = {
  args: {
    activeTool: 'highlight',
  },
};

export const CollaborativeMode: Story = {
  args: {
    showCollaborators: true,
    collaborators: ['User1', 'User2'],
  },
};
```

### Phase 3: Interaction Testing

```typescript
// Interaction test example
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

export const UserTypesMessage: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Find input
    const input = canvas.getByPlaceholderText('Type your message...');
    
    // Type message
    await userEvent.type(input, 'Hello GRANGER!');
    
    // Verify
    await expect(input).toHaveValue('Hello GRANGER!');
    
    // Submit
    await userEvent.keyboard('{Enter}');
    
    // Verify submission
    await expect(canvas.getByText('Message sent')).toBeInTheDocument();
  },
};
```

### Phase 4: Visual Regression Testing

```javascript
// .storybook/test-runner.js
module.exports = {
  async postRender(page, context) {
    // Add visual regression snapshot
    await page.screenshot({ 
      path: `screenshots/${context.story.id}.png`,
      fullPage: true 
    });
  },
};
```

### Phase 5: Style Guide Validation

```typescript
// .storybook/decorators/StyleGuideValidator.tsx
import { useEffect } from 'react';
import { STYLE_GUIDE } from '../../utils/style-guide';

export const StyleGuideValidator = (Story) => {
  useEffect(() => {
    // Validate colors
    const elements = document.querySelectorAll('*');
    elements.forEach(el => {
      const styles = window.getComputedStyle(el);
      const bgColor = styles.backgroundColor;
      
      // Check if color matches style guide
      if (bgColor && !isValidStyleGuideColor(bgColor)) {
        console.warn(`Invalid color detected: ${bgColor}`);
      }
    });
  }, []);
  
  return <Story />;
};
```

## Integration with Level 4 Tests

### Mapping Playwright Tests to Storybook

| Playwright Test | Storybook Equivalent |
|----------------|---------------------|
| Style compliance | Decorators + Visual tests |
| User workflows | Interaction tests |
| Cross-module navigation | Composition stories |
| Performance | Performance addon |
| Accessibility | A11y addon |

### Example Migration

**Before (Playwright):**
```typescript
test('Chat input accepts text', async ({ page }) => {
  await page.goto('http://localhost:3000/chat');
  const input = await page.$('.chat-input');
  await input.type('Hello');
  expect(await input.inputValue()).toBe('Hello');
});
```

**After (Storybook):**
```typescript
export const AcceptsText: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByRole('textbox');
    await userEvent.type(input, 'Hello');
    await expect(input).toHaveValue('Hello');
  },
};
```

## Benefits for GRANGER

1. **Faster Development**: Develop components without running full modules
2. **Better Documentation**: Visual component library for all developers
3. **Reduced Test Complexity**: No more complex Playwright setups
4. **Style Guide Enforcement**: Automatic validation via decorators
5. **Collaboration**: Designers can review components directly

## Implementation Timeline

### Week 1
- Set up Storybook in all three modules
- Create stories for core components
- Add essential addons (a11y, interactions)

### Week 2
- Migrate critical Playwright tests to Storybook
- Implement style guide validation decorator
- Set up visual regression testing

### Week 3
- Create composition stories for cross-module flows
- Add performance monitoring
- Document component APIs

### Week 4
- Complete test migration
- Set up CI/CD integration
- Create shared component library

## Commands

```bash
# Run Storybook locally
npm run storybook

# Run interaction tests
npm run test-storybook

# Build static Storybook
npm run build-storybook

# Run visual regression tests
npm run test:visual

# Check accessibility
npm run test:a11y
```

## Conclusion

Storybook provides the perfect solution for GRANGER's UI testing needs:
- ✅ Solves JavaScript complexity issues
- ✅ Provides visual documentation
- ✅ Enables component isolation
- ✅ Supports all testing requirements
- ✅ Improves developer experience

This approach complements our existing Playwright tests while providing a more maintainable and scalable testing strategy.