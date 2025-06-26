# 🚨 GRANGER Priority Fixes & Known Issues

**Document Version**: 1.0.0  
**Created**: 2025-06-04  
**Purpose**: Critical issues that need immediate attention

---

## 🔴 Critical Issues (Fix Immediately)

### 1. Terminal UI Build Failure
**Severity**: High  
**Impact**: Blocks Aider Daemon UI development  
**Location**: `/granger-ui/packages/ui-terminal`

**Problem**:
- React version mismatch (Ink requires v19, web uses v18)
- TypeScript module resolution failing
- ESM/CommonJS conflicts

**Proposed Solutions**:
```bash
# Option 1: Use esbuild
cd packages/ui-terminal
pnpm add -D esbuild
# Create custom build script

# Option 2: Separate React versions
# Use React 19 for terminal only

# Option 3: Pre-built terminal package
# Create standalone terminal UI package
```

**Temporary Workaround**:
```bash
# Skip terminal build for now
cd granger-ui
pnpm build --filter=!ui-terminal
```

---

### 2. WebSocket Connection Drops
**Severity**: High  
**Impact**: Modules lose connection to hub  
**Location**: All modules

**Problem**:
- No automatic reconnection
- No connection state management
- Silent failures

**Fix Required**:
```javascript
class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
    this.connect();
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onclose = () => {
      this.handleDisconnect();
    };
    
    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      this.handleDisconnect();
    };
  }

  handleDisconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++;
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    }
  }
}
```

---

### 3. State Synchronization Issues
**Severity**: Medium  
**Impact**: UI shows stale data  
**Location**: Chat and Marker interfaces

**Problem**:
- No optimistic updates
- Cache invalidation missing
- Race conditions

**Fix Required**:
- Implement Redux or Zustand for state management
- Add optimistic UI updates
- Implement proper cache invalidation

---

## 🟡 Medium Priority Issues

### 4. Missing Error Boundaries
**Impact**: Entire app crashes on component errors  
**Fix**: Add error boundaries to all major components

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };
  
  static getDerivedStateFromError(error) {
    return { hasError: true };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error("Error caught:", error, errorInfo);
    // Send to error tracking service
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### 5. No Loading States
**Impact**: Poor UX during data fetching  
**Fix**: Add loading skeletons

```jsx
const TableSkeleton = () => (
  <div className="animate-pulse">
    <div className="h-10 bg-gray-200 rounded mb-2" />
    <div className="h-10 bg-gray-200 rounded mb-2" />
    <div className="h-10 bg-gray-200 rounded" />
  </div>
);
```

### 6. Bundle Size Growing
**Impact**: Slow initial load  
**Current**: ~250KB (target: <200KB)  
**Fix**: 
- Implement code splitting
- Tree shake unused imports
- Lazy load heavy components

---

## 🟢 Low Priority Issues

### 7. Inconsistent Naming
- Some files use kebab-case, others camelCase
- Standardize on kebab-case for files

### 8. Missing PropTypes/TypeScript
- Some older components lack proper typing
- Gradually add types during refactoring

### 9. Console Warnings
- React key warnings in lists
- Unused variable warnings
- Clean up during next refactor

---

## 🔧 Quick Fixes (Can do now)

### Fix 1: Add Missing Keys
```jsx
// Before
{items.map(item => <Item {...item} />)}

// After
{items.map(item => <Item key={item.id} {...item} />)}
```

### Fix 2: Remove Unused Imports
```bash
# Run in each package
npx eslint --fix .
```

### Fix 3: Update Dependencies
```bash
cd granger-ui
pnpm update --interactive
```

---

## 📋 Testing Gaps

### Missing Tests For:
1. **WebSocket communication**
   - Connection/disconnection
   - Message handling
   - Error scenarios

2. **UI Components**
   - Interaction tests
   - Accessibility tests
   - Visual regression tests

3. **Integration**
   - Module registration
   - Data flow
   - Error propagation

### Test Implementation Priority:
```bash
# 1. Unit tests for utilities
cd packages/ui-core
pnpm test:unit

# 2. Component tests
cd packages/ui-web
pnpm test:components

# 3. E2E tests
cd apps/web-showcase
pnpm test:e2e
```

---

## 🚀 Performance Bottlenecks

### 1. Table Rendering
**Issue**: Slow with >100 rows  
**Fix**: Implement virtual scrolling
```jsx
import { VariableSizeList } from "react-window";
```

### 2. Re-renders
**Issue**: Unnecessary re-renders in dashboard  
**Fix**: Add React.memo and useMemo
```jsx
const MemoizedComponent = React.memo(Component);
const expensiveValue = useMemo(() => compute(data), [data]);
```

### 3. Bundle Loading
**Issue**: Large initial bundle  
**Fix**: Split by route
```jsx
const Dashboard = lazy(() => import("./Dashboard"));
```

---

## 🔒 Security Vulnerabilities

### 1. No Input Sanitization
**Risk**: XSS attacks  
**Fix**: Sanitize all user inputs
```javascript
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(userInput);
```

### 2. Exposed API Keys
**Risk**: Keys in frontend code  
**Fix**: Move to environment variables

### 3. No Rate Limiting
**Risk**: DoS attacks  
**Fix**: Implement rate limiting on API

---

## 📝 Documentation Gaps

### Missing Documentation:
1. API endpoint documentation
2. Component prop documentation
3. Deployment guide
4. Contributing guidelines
5. Architecture decision records (ADRs)

### Documentation Priority:
1. Create API docs with Swagger/OpenAPI
2. Generate component docs from TypeScript
3. Write deployment playbook
4. Create CONTRIBUTING.md

---

## 🎯 Action Items for Claude Code

### Week 1 Priorities:
1. [ ] Fix terminal build issue
2. [ ] Implement WebSocket reconnection
3. [ ] Add error boundaries
4. [ ] Create loading states

### Week 2 Priorities:
1. [ ] Add comprehensive tests
2. [ ] Optimize performance
3. [ ] Fix security issues
4. [ ] Complete documentation

### Week 3 Priorities:
1. [ ] Implement monitoring
2. [ ] Set up CI/CD
3. [ ] Create deployment scripts
4. [ ] Performance audit

---

## 🆘 Getting Unstuck

### If build fails:
```bash
pnpm clean
rm -rf node_modules
pnpm install
```

### If types are wrong:
```bash
pnpm tsc --noEmit
```

### If WebSocket won't connect:
1. Check hub is running
2. Verify port 8765 is open
3. Check WebSocket URL format

### If UI looks broken:
1. Clear browser cache
2. Rebuild CSS: `pnpm build:css`
3. Check Tailwind config

---

**Remember**: Fix critical issues first, then move to medium priority. Document all fixes!
'EOF'