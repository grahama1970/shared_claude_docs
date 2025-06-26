# 🎨 GRANGER UI Quick Reference Card

## 📁 Key Locations
```bash
# Monorepo
cd /home/graham/workspace/granger-ui

# Projects to migrate
cd /home/graham/workspace/experiments/chat          # Chat Interface
cd /home/graham/workspace/experiments/marker-ground-truth  # Annotator
cd /home/graham/workspace/experiments/aider-daemon  # Terminal UI

# Documentation
cd /home/graham/workspace/shared_claude_docs/docs/03_ui_unification
```

## 🛠️ Common Commands
```bash
# Development
npx pnpm install          # Install all dependencies
npx pnpm run build        # Build all packages
npx pnpm run dev          # Start dev mode
npx pnpm run test         # Run tests

# Package-specific
npx pnpm --filter @granger/ui-web build
npx pnpm --filter @granger/ui-core dev

# Add dependency
npx pnpm add framer-motion --filter @granger/ui-web
```

## 🎨 Design Tokens
```typescript
// Colors
import { colors } from '@granger/ui-core';
colors.primary.DEFAULT  // #5B21B6
colors.accent          // #10B981

// Spacing (8px base)
import { spacing } from '@granger/ui-core';
spacing.scale[4]       // 32px

// Typography
import { typography } from '@granger/ui-core';
typography.fontSize.lg  // 1.125rem

// Animation
import { transitions } from '@granger/ui-core';
transitions.duration.normal  // 250ms
```

## 🧩 Component Usage
```tsx
// Web Components
import { Button, Card, MetricCard } from '@granger/ui-web';

<Button variant="primary" size="md">
  Click Me
</Button>

<MetricCard
  label="Success Rate"
  value={92.5}
  trend={3.2}
  icon={<TrendingUp />}
/>

// Terminal Components  
import { TerminalDashboard } from '@granger/ui-terminal';

<TerminalDashboard data={metrics} />
```

## 🎯 Style Guide Compliance
- **Colors**: Use design tokens, not hex values
- **Spacing**: Always use 8px multiples
- **Fonts**: Inter for web, system fonts for terminal
- **Animations**: 150-300ms with ease-in-out
- **Corners**: 6-8px border radius
- **Shadows**: Subtle, use shadow-sm/md/lg

## 📋 Migration Checklist
- [ ] Replace hardcoded colors with tokens
- [ ] Update spacing to use scale
- [ ] Convert custom components to shared
- [ ] Remove duplicate icon imports
- [ ] Use unified animation system
- [ ] Update import paths
- [ ] Test in Storybook
- [ ] Verify style guide compliance

## 🚀 Quick Start New Component
```bash
# Create component file
touch packages/ui-web/src/components/MyComponent.tsx

# Basic template
cat > packages/ui-web/src/components/MyComponent.tsx << 'EOF'
import React from 'react';
import { cn } from '../lib/utils';
import { motion } from 'framer-motion';

export interface MyComponentProps {
  className?: string;
  children?: React.ReactNode;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  className,
  children
}) => {
  return (
    <motion.div 
      className={cn("p-4 rounded-lg", className)}
      whileHover={{ scale: 1.02 }}
    >
      {children}
    </motion.div>
  );
};
EOF

# Export it
echo "export * from './MyComponent';" >> packages/ui-web/src/components/index.ts
```

## 🔗 Useful Links
- [Tailwind Docs](https://tailwindcss.com/docs)
- [Lucide Icons](https://lucide.dev/icons)
- [Framer Motion](https://www.framer.com/motion)
- [Radix UI](https://www.radix-ui.com)

---
**Remember**: Consistency > Creativity. Use existing components first!
