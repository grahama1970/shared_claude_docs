# 🔧 GRANGER Technical Implementation Guide

**Document Version**: 1.0.0  
**Created**: 2025-06-04  
**Purpose**: Technical details for Claude Code implementation

---

## 🏗️ Technology Stack

### Frontend Technologies
- **React 18.3.1** - Web interfaces
- **React 19.0.0** - Terminal interfaces (Ink requirement)
- **TypeScript 5.4.0** - Type safety
- **Tailwind CSS 3.4.1** - Styling
- **Framer Motion 11.18.2** - Animations
- **Lucide React** - Iconography

### Backend Technologies
- **Python 3.10+** - Hub and services
- **Node.js 18+** - Web servers
- **WebSocket** - Real-time communication
- **SQLite** - Local data storage
- **Express.js** - API servers

### Build Tools
- **pnpm** - Package management
- **Rollup** - Web package bundling
- **Vite** - Development server
- **Next.js 14** - Web applications
- **Storybook 7** - Component documentation

---

## 🔌 Module Communication Protocol

### Message Format
```typescript
interface GrangerMessage {
  id: string;                    // UUID
  timestamp: number;             // Unix timestamp
  source: string;                // Module identifier
  target: string;                // Target module or "broadcast"
  type: MessageType;             // Enum of message types
  payload: Record<string, any>;  // Message data
  metadata?: {
    version: string;
    correlationId?: string;
    priority?: "low" | "normal" | "high";
  };
}

enum MessageType {
  // System messages
  REGISTER = "REGISTER",
  HEARTBEAT = "HEARTBEAT",
  STATUS = "STATUS",
  ERROR = "ERROR",
  
  // Data messages
  DATA_REQUEST = "DATA_REQUEST",
  DATA_RESPONSE = "DATA_RESPONSE",
  DATA_UPDATE = "DATA_UPDATE",
  
  // Control messages
  COMMAND = "COMMAND",
  CONFIG_UPDATE = "CONFIG_UPDATE",
  SHUTDOWN = "SHUTDOWN",
}
```

### WebSocket Connection
```javascript
// Example module connection
const ws = new WebSocket("ws://localhost:8765");

ws.on("open", () => {
  // Register module
  ws.send(JSON.stringify({
    id: generateUUID(),
    timestamp: Date.now(),
    source: "module-name",
    target: "hub",
    type: "REGISTER",
    payload: {
      name: "Module Name",
      version: "1.0.0",
      capabilities: ["feature1", "feature2"]
    }
  }));
});

// Handle messages
ws.on("message", (data) => {
  const message = JSON.parse(data);
  handleMessage(message);
});

// Heartbeat every 30 seconds
setInterval(() => {
  ws.send(JSON.stringify({
    id: generateUUID(),
    timestamp: Date.now(),
    source: "module-name",
    target: "hub",
    type: "HEARTBEAT",
    payload: { status: "healthy" }
  }));
}, 30000);
```

---

## 🎨 UI Component Standards

### Component Structure
```typescript
// Standard component interface
interface ComponentProps {
  className?: string;
  children?: React.ReactNode;
  // Component-specific props
}

// Example implementation
export const Component: React.FC<ComponentProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={cn("base-styles", className)} {...props}>
      {children}
    </div>
  );
};

Component.displayName = "Component";
```

### Styling Guidelines
1. **Use Tailwind classes** for styling
2. **CSS variables** for theming
3. **cn() utility** for class merging
4. **Consistent spacing** using design tokens
5. **Responsive by default**

### Animation Standards
```typescript
// Use Framer Motion for complex animations
const animationVariants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};

// Simple transitions with Tailwind
className="transition-all duration-200 hover:scale-105"
```

---

## 🧪 Testing Strategy

### Unit Testing
```javascript
// Jest + React Testing Library
import { render, screen } from "@testing-library/react";
import { Button } from "@granger/ui-web";

describe("Button", () => {
  it("renders with text", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });
});
```

### Integration Testing
```javascript
// Test module communication
describe("Module Registration", () => {
  it("registers with hub successfully", async () => {
    const ws = new WebSocket("ws://localhost:8765");
    
    await waitFor(() => {
      expect(ws.readyState).toBe(WebSocket.OPEN);
    });
    
    // Send registration
    ws.send(JSON.stringify(registrationMessage));
    
    // Verify acknowledgment
    const response = await waitForMessage(ws);
    expect(response.type).toBe("REGISTER_ACK");
  });
});
```

### Visual Regression Testing
```javascript
// Playwright visual tests
test("Button visual states", async ({ page }) => {
  await page.goto("/storybook/button");
  
  // Capture default state
  await expect(page.locator(".button-default")).toHaveScreenshot();
  
  // Capture hover state
  await page.hover(".button-default");
  await expect(page.locator(".button-default")).toHaveScreenshot();
});
```

---

## 🚀 Deployment Architecture

### Container Structure
```yaml
# docker-compose.yml
version: "3.8"

services:
  hub:
    build: ./central_command
    ports:
      - "8765:8765"
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8765/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  chat:
    build: ./experiments/chat
    ports:
      - "3000:3000"
    depends_on:
      - hub
    environment:
      - HUB_URL=ws://hub:8765
      - NODE_ENV=production

  marker:
    build: ./experiments/marker_ground_truth
    ports:
      - "3001:3001"
    depends_on:
      - hub
    volumes:
      - ./data:/app/data

  # Additional services...
```

### Environment Configuration
```bash
# .env.production
NODE_ENV=production
HUB_URL=ws://hub:8765
LOG_LEVEL=info
ENABLE_METRICS=true
SENTRY_DSN=your-sentry-dsn
```

---

## 📊 Performance Optimization

### Frontend Optimization
1. **Code Splitting**
   ```javascript
   const Modal = lazy(() => import("./components/Modal"));
   ```

2. **Memoization**
   ```javascript
   const MemoizedComponent = memo(Component);
   ```

3. **Virtual Scrolling**
   ```javascript
   import { FixedSizeList } from "react-window";
   ```

### Backend Optimization
1. **Message Queuing**
   ```python
   from asyncio import Queue
   
   message_queue = Queue(maxsize=1000)
   ```

2. **Connection Pooling**
   ```python
   connection_pool = ConnectionPool(max_connections=100)
   ```

3. **Caching Strategy**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def expensive_operation(param):
       # Cached computation
   ```

---

## 🔒 Security Considerations

### Authentication
```typescript
// JWT token validation
const validateToken = (token: string): boolean => {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return decoded.exp > Date.now() / 1000;
  } catch {
    return false;
  }
};
```

### Message Validation
```typescript
// Zod schema for message validation
const messageSchema = z.object({
  id: z.string().uuid(),
  timestamp: z.number(),
  source: z.string(),
  target: z.string(),
  type: z.enum(Object.values(MessageType)),
  payload: z.record(z.any())
});
```

### Rate Limiting
```javascript
const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: "Too many requests"
});
```

---

## 🐛 Debugging & Monitoring

### Logging Strategy
```javascript
// Structured logging with Winston
const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" })
  ]
});

// Usage
logger.info("Module registered", {
  module: moduleName,
  timestamp: Date.now(),
  metadata: { version, capabilities }
});
```

### Performance Monitoring
```javascript
// Performance tracking
performance.mark("operation-start");
// ... operation ...
performance.mark("operation-end");
performance.measure("operation", "operation-start", "operation-end");

const measure = performance.getEntriesByName("operation")[0];
logger.info("Performance", { operation: "name", duration: measure.duration });
```

### Error Tracking
```javascript
// Sentry integration
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  environment: process.env.NODE_ENV
});

// Capture errors
try {
  riskyOperation();
} catch (error) {
  Sentry.captureException(error);
  logger.error("Operation failed", { error: error.message });
}
```

---

## 📚 API Documentation

### REST Endpoints (per module)
```
GET    /api/v1/status         # Module status
GET    /api/v1/health         # Health check
POST   /api/v1/config         # Update configuration
GET    /api/v1/metrics        # Performance metrics
```

### WebSocket Events
```
Client -> Server:
- register: Register module
- heartbeat: Keep-alive signal
- message: Send message
- unregister: Disconnect

Server -> Client:
- registered: Registration confirmed
- message: Incoming message
- error: Error notification
- broadcast: System-wide message
```

---

## 🔄 Migration Checklist

### For Each Module:
- [ ] Update package.json dependencies
- [ ] Replace UI components with @granger/ui-web
- [ ] Implement standard message protocol
- [ ] Add error handling and retry logic
- [ ] Create unit tests
- [ ] Add performance monitoring
- [ ] Update documentation
- [ ] Create Docker configuration
- [ ] Add health check endpoint
- [ ] Implement graceful shutdown

---

**Next Steps**: Review this guide and begin implementing the standardized protocols across all modules.
'EOF'