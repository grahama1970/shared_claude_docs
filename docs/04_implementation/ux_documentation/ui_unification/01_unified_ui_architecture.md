# Unified UI Architecture Strategy for GRANGER Projects

## Executive Summary

This document outlines a comprehensive strategy to unify the UI architectures across three GRANGER projects while maintaining compliance with the 2025 Style Guide inspired by Vercel v0 aesthetics.

## Current State Analysis

### 1. **Marker Ground Truth** (Annotator)
- **Tech Stack**: React + Tailwind CSS + shadcn/ui components
- **Location**: `/home/graham/workspace/experiments/marker-ground-truth/`
- **UI Structure**: 
  - Has a `shared-ui` package (`@granger/shared-ui`)
  - Uses Radix UI primitives with custom styling
  - Implements Storybook for component development

### 2. **Chat Interface**
- **Tech Stack**: React + Tailwind CSS + Headless UI + Framer Motion
- **Location**: `/home/graham/workspace/experiments/chat/`
- **UI Structure**:
  - Multiple dashboard components (DashboardView, EmbeddedDashboard, FullscreenDashboard)
  - Custom component implementations
  - D3.js for data visualizations

### 3. **Aider Daemon** (Terminal Replacement)
- **Tech Stack**: React Ink (Terminal UI)
- **Location**: `/home/graham/workspace/experiments/aider-daemon/`
- **UI Structure**:
  - Terminal-based UI using Ink
  - Different paradigm from web-based UIs

## Proposed Unified Architecture

### 1. **Monorepo Structure**

```
/home/graham/workspace/granger-ui/
├── packages/
│   ├── @granger/ui-core/          # Core design system
│   ├── @granger/ui-web/           # Web components (React/Tailwind)
│   ├── @granger/ui-terminal/      # Terminal components (React Ink)
│   └── @granger/ui-shared/        # Shared utilities & types
├── apps/
│   ├── marker-ground-truth/
│   ├── chat/
│   └── aider-daemon/
└── tools/
    ├── storybook/
    └── build-scripts/
```### 2. **Core Design System Package** (`@granger/ui-core`)

#### Design Tokens (Following 2025 Style Guide)
```typescript
// tokens/colors.ts
export const colors = {
  primary: {
    start: '#4F46E5',
    end: '#6366F1',
    DEFAULT: '#5B21B6'
  },
  secondary: '#6B7280',
  background: '#F9FAFB',
  accent: '#10B981',
  // ... rest of color palette
};

// tokens/spacing.ts
export const spacing = {
  base: 8,
  scale: [0, 8, 16, 24, 32, 40, 48, 56, 64]
};

// tokens/typography.ts
export const typography = {
  fontFamily: {
    base: "'Inter', system-ui, sans-serif"
  },
  fontWeight: {
    regular: 400,
    semibold: 600,
    bold: 700
  }
};
```

### 3. **Web Components Package** (`@granger/ui-web`)

#### Component Architecture
```typescript
// Base component structure
interface ComponentProps {
  className?: string;
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children?: React.ReactNode;
}

// Example: Button component
export const Button = forwardRef<HTMLButtonElement, ButtonProps>(  ({ className, variant = 'primary', size = 'md', ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          buttonVariants({ variant, size }),
          className
        )}
        {...props}
      />
    );
  }
);
```

#### Shared Components to Build
1. **Layout Components**
   - Container
   - Grid/FlexGrid
   - Stack
   - Spacer

2. **Data Display**
   - Card
   - Table
   - List
   - Badge
   - Avatar

3. **Form Controls**
   - Input
   - Select
   - Checkbox
   - Radio
   - Switch
   - Form/FormField

4. **Feedback**
   - Alert
   - Toast
   - Progress
   - Skeleton
   - Spinner

5. **Navigation**
   - Tabs
   - Breadcrumb
   - Pagination
   - Menu/Dropdown
6. **Overlays**
   - Modal/Dialog
   - Popover
   - Tooltip
   - Drawer

7. **Dashboard Specific**
   - MetricCard
   - ChartContainer
   - ModuleCard
   - PipelineViewer
   - LogViewer

### 4. **Terminal Components Package** (`@granger/ui-terminal`)

Map web components to terminal equivalents:
```javascript
// Terminal UI components using Ink
export const TerminalCard = ({ title, children }) => (
  <Box borderStyle="round" padding={1}>
    <Text bold>{title}</Text>
    <Box marginTop={1}>{children}</Box>
  </Box>
);

export const TerminalMetric = ({ label, value, trend }) => (
  <Box>
    <Text color="gray">{label}: </Text>
    <Text bold color={trend > 0 ? 'green' : 'red'}>
      {value} {trend > 0 ? '↑' : '↓'}
    </Text>
  </Box>
);
```

### 5. **Shared Dashboard Implementation**

Create a flexible dashboard system that works across projects:

```typescript
// @granger/ui-web/src/dashboard/DashboardLayout.tsx
export interface DashboardConfig {
  layout: 'grid' | 'flex' | 'custom';
  sections: DashboardSection[];
  theme?: 'light' | 'dark';
}