# 🚀 GRANGER Next Actions - UI Unification Phase

**Generated**: 2025-06-03 20:35 EST  
**Priority**: Execute in order listed  
**Context**: Following successful monorepo setup at `/home/graham/workspace/granger-ui/`

---

## 🎯 Immediate Actions (Next 24 Hours)

### 1. Fix Build System ⚡ CRITICAL
```bash
cd /home/graham/workspace/granger-ui

# Add missing type dependencies
npx pnpm add -D lucide-react -w
npx pnpm add -D @types/react @types/react-dom -w

# Fix module resolution in packages
cd packages/ui-core
echo '{"type": "commonjs"}' > package.json.tmp
jq -s '.[0] * .[1]' package.json package.json.tmp > package.json.new
mv package.json.new package.json
rm package.json.tmp

# Test build
npm run build
```

### 2. Complete Core Components
Create these essential components in `packages/ui-web/src/components/`:

- **Card.tsx** - Base card component with hover effects
- **Input.tsx** - Form input with validation states  
- **Select.tsx** - Dropdown with search capability
- **Modal.tsx** - Dialog/overlay component
- **Toast.tsx** - Notification system
- **Table.tsx** - Data table with sorting

### 3. Wire Up Example Dashboard
```bash
cd /home/graham/workspace/granger-ui/apps/example-dashboard

# Create Vite config
cat > vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@granger/ui-web': path.resolve(__dirname, '../../packages/ui-web/src'),
      '@granger/ui-core': path.resolve(__dirname, '../../packages/ui-core/src')
    }
  }
})
EOF

# Create index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>GRANGER UI Example</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
EOF

# Run dev server
npx vite
```

---

## 📋 This Week's Priorities

### Monday (June 3) ✅ DONE
- [x] Create unified UI documentation
- [x] Set up monorepo structure
- [x] Initialize core packages
- [x] Create design tokens

### Tuesday (June 4) 
- [ ] Fix build system issues
- [ ] Complete 6 core components
- [ ] Get example dashboard running
- [ ] Create first Storybook story

### Wednesday (June 5)
- [ ] Migrate Chat interface Button component
- [ ] Migrate Chat interface Card component  
- [ ] Update Chat dashboard to use SharedDashboard
- [ ] Test WebSocket integration

### Thursday (June 6)
- [ ] Complete Chat interface migration
- [ ] Start Marker Ground Truth migration
- [ ] Create terminal dashboard components
- [ ] Document component APIs

### Friday (June 7)
- [ ] Complete Marker Ground Truth migration
- [ ] Implement Aider Daemon terminal UI
- [ ] Set up visual regression tests
- [ ] Create migration guide for teams

---

## 🔧 Technical Debt to Address

1. **TypeScript Configurations**
   - Create shared tsconfig.base.json
   - Ensure proper module resolution
   - Fix type exports

2. **Build Optimization**
   - Set up proper tree shaking
   - Configure CSS purging
   - Implement code splitting

3. **Testing Infrastructure**
   - Add Jest configuration
   - Create component test utilities
   - Set up React Testing Library

4. **Developer Experience**
   - Create component generator script
   - Add hot module replacement
   - Improve error messages

---

## 📊 Success Metrics

By end of week, we should have:
- ✅ All packages building successfully
- ✅ 15+ shared components created
- ✅ Chat interface fully migrated
- ✅ Storybook with all components
- ✅ Performance: <100ms component render
- ✅ Bundle size: <50KB for core components

---

## 🚨 Potential Blockers

1. **React Version Conflicts**
   - Terminal UI needs React 19 for Ink
   - Web UI uses React 18
   - Solution: Separate builds, shared interfaces

2. **CSS-in-JS vs Tailwind**
   - Some components use emotion/styled
   - Migration path: Gradual conversion to Tailwind

3. **WebSocket Integration**
   - Real-time updates need careful state management
   - Solution: Create unified WebSocket hook

---

## 📚 Resources

- **Monorepo**: `/home/graham/workspace/granger-ui/`
- **Style Guide**: `/home/graham/workspace/shared_claude_docs/guides/2025_STYLE_GUIDE.md`
- **UI Docs**: `/home/graham/workspace/shared_claude_docs/docs/03_ui_unification/`
- **Tasks**: `/home/graham/workspace/shared_claude_docs/docs/000_UNIFIED_TASKS_LIST.md`

---

## 💡 Quick Wins

1. **Component Showcase**
   ```bash
   # Create a quick visual test page
   cd packages/ui-web
   npm run build
   npx http-server dist
   ```

2. **Auto-generate Icons Index**
   ```bash
   # Create script to auto-export all Lucide icons
   node scripts/generate-icons.js
   ```

3. **CSS Variables Helper**
   ```css
   /* Add to globals.css for easy theming */
   [data-theme="dark"] {
     --background: #111827;
     --foreground: #F9FAFB;
   }
   ```

---

**Remember**: Every component created brings us closer to a unified, maintainable system. The investment in this infrastructure will pay dividends across all GRANGER projects.

**Next Check-in**: Tomorrow 09:00 EST
**Questions**: Create issue in granger-ui repo
