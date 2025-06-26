# GRANGER UI Switching Implementation Plan

## Executive Summary

This implementation plan provides a simple, user-focused solution for seamless switching between three GRANGER interfaces (Chat, Annotator, Terminal) with <2s context switching requirement. The solution emphasizes simplicity, performance, and user experience.

## Overview

### Core Requirements
- **Three Interfaces**: Chat (web), Annotator (Marker-Ground-Truth web), Terminal
- **Performance**: <2s context switching
- **Authentication**: JWT-based with SSO handoff
- **State Preservation**: Full context maintained across switches
- **Deep Linking**: granger://ui/context protocol
- **Visual Feedback**: Smooth transitions with loading indicators

### Key Design Principles
1. **Simplicity First**: Minimal complexity, maximum usability
2. **Performance Focused**: Every millisecond counts
3. **User-Centric**: Clear visual feedback at every step
4. **Fail-Safe**: Graceful degradation when services are unavailable

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Quick Switch Bar                         │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐ │
│  │  Chat   │  │ Annotator │  │ Terminal │  │ Search (⌘K) │ │
│  └─────────┘  └──────────┘  └──────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├── WebSocket Event Bus
                              ├── State Manager
                              ├── Auth Service
                              └── Deep Link Handler
```

### Data Flow

1. **User Action** → Quick Switch Bar / Keyboard Shortcut
2. **State Capture** → Current UI saves state to shared store
3. **Auth Handoff** → JWT token passed to target UI
4. **Deep Link** → Navigate to target with context
5. **State Restore** → Target UI loads preserved state
6. **Visual Transition** → Smooth fade with progress indicator

## Implementation Details

### Phase 1: Basic Switching (Week 1)

#### 1.1 Quick Switch Bar Component

```typescript
// packages/ui-core/src/components/QuickSwitchBar.tsx
interface QuickSwitchBarProps {
  currentUI: 'chat' | 'annotator' | 'terminal';
  onSwitch: (target: UITarget) => void;
  isTransitioning: boolean;
}

export const QuickSwitchBar: React.FC<QuickSwitchBarProps> = ({
  currentUI,
  onSwitch,
  isTransitioning
}) => {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b">
      <div className="max-w-7xl mx-auto px-4 h-12 flex items-center justify-between">
        <div className="flex gap-2">
          <SwitchButton
            label="Chat"
            icon={<MessageSquare />}
            active={currentUI === 'chat'}
            onClick={() => onSwitch('chat')}
            disabled={isTransitioning}
          />
          <SwitchButton
            label="Annotator"
            icon={<FileText />}
            active={currentUI === 'annotator'}
            onClick={() => onSwitch('annotator')}
            disabled={isTransitioning}
          />
          <SwitchButton
            label="Terminal"
            icon={<Terminal />}
            active={currentUI === 'terminal'}
            onClick={() => onSwitch('terminal')}
            disabled={isTransitioning}
          />
        </div>
        
        <div className="flex items-center gap-4">
          <kbd className="text-xs bg-gray-100 px-2 py-1 rounded">⌘K</kbd>
          <CurrentContext />
        </div>
      </div>
    </div>
  );
};
```

#### 1.2 Keyboard Shortcuts Manager

```typescript
// packages/ui-core/src/services/KeyboardShortcuts.ts
export class KeyboardShortcutsManager {
  private shortcuts: Map<string, ShortcutHandler> = new Map();
  
  constructor() {
    this.registerDefaultShortcuts();
  }
  
  private registerDefaultShortcuts() {
    // Universal shortcuts
    this.register('cmd+alt+c', () => this.switchTo('chat'));
    this.register('cmd+alt+a', () => this.switchTo('annotator'));
    this.register('cmd+alt+t', () => this.switchTo('terminal'));
    this.register('cmd+tab', () => this.cycleInterfaces());
    this.register('cmd+k', () => this.openQuickSearch());
  }
  
  private async switchTo(target: UITarget) {
    // Emit switch event
    eventBus.emit('ui:switch:start', { target });
    
    // Save current state
    await stateManager.saveCurrentState();
    
    // Perform switch
    const deepLink = deepLinkGenerator.generate(target);
    window.location.href = deepLink;
  }
}
```

#### 1.3 Basic State Manager

```typescript
// packages/ui-core/src/services/StateManager.ts
export class StateManager {
  private storage = new StateStorage();
  
  async saveCurrentState(): Promise<void> {
    const state: UIState = {
      timestamp: Date.now(),
      ui: getCurrentUI(),
      context: {
        url: window.location.href,
        scrollPosition: window.scrollY,
        activeElement: document.activeElement?.id,
        formData: this.captureFormData(),
        customData: await this.getCustomUIData()
      }
    };
    
    await this.storage.save(state);
    await this.broadcastState(state);
  }
  
  async restoreState(): Promise<void> {
    const state = await this.storage.getLatest();
    if (!state || Date.now() - state.timestamp > 300000) return; // 5 min expiry
    
    // Restore scroll position
    window.scrollTo(0, state.context.scrollPosition);
    
    // Restore form data
    this.restoreFormData(state.context.formData);
    
    // Restore custom UI state
    await this.restoreCustomUIData(state.context.customData);
  }
}
```

### Phase 2: State Preservation (Week 2)

#### 2.1 Enhanced State Storage

```typescript
// packages/ui-core/src/services/StateStorage.ts
interface StateStorage {
  // Local storage for immediate access
  local: Map<string, UIState>;
  
  // Shared storage via WebSocket
  shared: WebSocketStateSync;
  
  // Persistent storage
  persistent: IndexedDBStorage;
}

export class EnhancedStateManager {
  async captureState(): Promise<CapturedState> {
    return {
      // Basic state
      basic: this.captureBasicState(),
      
      // UI-specific state
      uiSpecific: await this.captureUISpecificState(),
      
      // File context
      files: await this.captureFileContext(),
      
      // Activity history
      history: this.captureRecentActivity()
    };
  }
  
  private async captureUISpecificState() {
    const ui = getCurrentUI();
    
    switch(ui) {
      case 'chat':
        return {
          conversation: this.getConversationState(),
          selectedModel: this.getSelectedModel(),
          settings: this.getChatSettings()
        };
        
      case 'annotator':
        return {
          document: this.getOpenDocument(),
          annotations: this.getUnsavedAnnotations(),
          viewport: this.getViewportState()
        };
        
      case 'terminal':
        return {
          workingDirectory: this.getCwd(),
          history: this.getCommandHistory(),
          environment: this.getEnvironmentVars()
        };
    }
  }
}
```

#### 2.2 WebSocket Synchronization

```typescript
// packages/ui-core/src/services/WebSocketSync.ts
export class WebSocketStateSync {
  private ws: WebSocket;
  private reconnectAttempts = 0;
  
  constructor(private config: WebSocketConfig) {
    this.connect();
  }
  
  private connect() {
    this.ws = new WebSocket(this.config.url);
    
    this.ws.onopen = () => {
      this.reconnectAttempts = 0;
      this.authenticate();
    };
    
    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
    
    this.ws.onclose = () => {
      this.handleReconnect();
    };
  }
  
  async broadcastState(state: UIState) {
    if (this.ws.readyState !== WebSocket.OPEN) return;
    
    this.ws.send(JSON.stringify({
      type: 'state:update',
      payload: state
    }));
  }
  
  subscribeToStateUpdates(callback: StateUpdateCallback) {
    eventBus.on('state:remote:update', callback);
  }
}
```

### Phase 3: Deep Linking (Week 3)

#### 3.1 Deep Link Protocol

```typescript
// packages/ui-core/src/services/DeepLinkProtocol.ts
export class DeepLinkProtocol {
  // URL Scheme: granger://[ui]/[resource]/[id]?[params]
  
  generate(target: UITarget, context?: DeepLinkContext): string {
    const base = `granger://${target}`;
    
    if (!context) return base;
    
    const parts = [base];
    
    if (context.resource) {
      parts.push(context.resource);
    }
    
    if (context.id) {
      parts.push(context.id);
    }
    
    const url = parts.join('/');
    const params = new URLSearchParams(context.params || {});
    
    return params.toString() ? `${url}?${params}` : url;
  }
  
  parse(url: string): DeepLinkData {
    const match = url.match(/^granger:\/\/([^\/]+)\/([^\/]+)\/([^?]+)(?:\?(.+))?$/);
    
    if (!match) throw new Error('Invalid deep link');
    
    return {
      ui: match[1] as UITarget,
      resource: match[2],
      id: match[3],
      params: new URLSearchParams(match[4] || '')
    };
  }
}

// Example deep links:
// granger://chat/conversation/abc123
// granger://annotator/document/xyz789?page=5
// granger://terminal/workspace/project1?cmd=npm%20test
```

#### 3.2 Deep Link Handlers

```typescript
// packages/ui-core/src/services/DeepLinkHandlers.ts
export class DeepLinkHandlers {
  private handlers = new Map<string, DeepLinkHandler>();
  
  constructor() {
    this.registerDefaultHandlers();
  }
  
  private registerDefaultHandlers() {
    // Chat handlers
    this.register('chat/conversation', async (data) => {
      await chatAPI.loadConversation(data.id);
    });
    
    // Annotator handlers
    this.register('annotator/document', async (data) => {
      await annotatorAPI.openDocument(data.id);
      const page = data.params.get('page');
      if (page) await annotatorAPI.navigateToPage(parseInt(page));
    });
    
    // Terminal handlers
    this.register('terminal/workspace', async (data) => {
      await terminalAPI.changeDirectory(data.id);
      const cmd = data.params.get('cmd');
      if (cmd) await terminalAPI.executeCommand(cmd);
    });
  }
}
```

### Phase 4: Advanced Features (Week 4)

#### 4.1 Visual Transitions

```typescript
// packages/ui-web/src/components/TransitionOverlay.tsx
export const TransitionOverlay: React.FC<TransitionProps> = ({
  isTransitioning,
  targetUI,
  progress
}) => {
  if (!isTransitioning) return null;
  
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-white/90 backdrop-blur-lg"
    >
      <div className="h-full flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          className="text-center"
        >
          <div className="mb-4">
            {getUIIcon(targetUI)}
          </div>
          <h2 className="text-2xl font-semibold mb-2">
            Switching to {targetUI}
          </h2>
          <ProgressBar value={progress} className="w-64" />
        </motion.div>
      </div>
    </motion.div>
  );
};
```

#### 4.2 Context-Aware Suggestions

```typescript
// packages/ui-core/src/services/ContextSuggestions.ts
export class ContextSuggestions {
  suggest(currentContext: Context): UISuggestion[] {
    const suggestions: UISuggestion[] = [];
    
    // File-based suggestions
    if (currentContext.activeFile?.endsWith('.pdf')) {
      suggestions.push({
        ui: 'annotator',
        reason: 'Open PDF in Annotator for markup',
        confidence: 0.9
      });
    }
    
    // Task-based suggestions
    if (currentContext.lastCommand?.includes('git')) {
      suggestions.push({
        ui: 'terminal',
        reason: 'Continue git operations in Terminal',
        confidence: 0.8
      });
    }
    
    // Conversation-based suggestions
    if (currentContext.hasActiveConversation) {
      suggestions.push({
        ui: 'chat',
        reason: 'Resume conversation in Chat',
        confidence: 0.85
      });
    }
    
    return suggestions.sort((a, b) => b.confidence - a.confidence);
  }
}
```

## Performance Optimizations

### 1. Pre-warming Target UI
```typescript
// Start loading target UI resources before switch
async function preWarmUI(target: UITarget) {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = getUIEntrypoint(target);
  document.head.appendChild(link);
}
```

### 2. State Compression
```typescript
// Compress state for faster transfer
function compressState(state: UIState): CompressedState {
  return {
    ...state,
    context: lz.compress(JSON.stringify(state.context))
  };
}
```

### 3. Smart Caching
```typescript
// Cache frequently accessed data
class SmartCache {
  private cache = new Map<string, CachedItem>();
  private accessCount = new Map<string, number>();
  
  get(key: string): any {
    this.accessCount.set(key, (this.accessCount.get(key) || 0) + 1);
    return this.cache.get(key)?.value;
  }
  
  set(key: string, value: any, ttl: number = 300000) {
    this.cache.set(key, {
      value,
      expires: Date.now() + ttl
    });
  }
}
```

## Testing Strategy

### Performance Tests
```typescript
describe('UI Switching Performance', () => {
  it('should complete switch in under 2 seconds', async () => {
    const start = performance.now();
    await switchUI('chat', 'annotator');
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(2000);
  });
  
  it('should preserve all state data', async () => {
    const originalState = await captureState();
    await switchUI('chat', 'annotator');
    await switchUI('annotator', 'chat');
    const restoredState = await getCurrentState();
    expect(restoredState).toEqual(originalState);
  });
});
```

### Integration Tests
```typescript
describe('Cross-UI Integration', () => {
  it('should handle file drag from chat to annotator', async () => {
    // Upload file in chat
    await chatUI.uploadFile('test.pdf');
    
    // Switch to annotator
    await switchUI('chat', 'annotator');
    
    // Verify file is available
    const files = await annotatorUI.getAvailableFiles();
    expect(files).toContain('test.pdf');
  });
});
```

## Security Considerations

### JWT Token Handling
```typescript
class SecureTokenManager {
  private tokenStorage = new SecureStorage();
  
  async getToken(): Promise<string> {
    const token = await this.tokenStorage.get('jwt');
    
    // Verify token hasn't expired
    if (this.isExpired(token)) {
      return await this.refreshToken();
    }
    
    return token;
  }
  
  async passTokenToUI(target: UITarget): Promise<void> {
    const token = await this.getToken();
    
    // Use secure message passing
    window.postMessage({
      type: 'auth:token',
      token: await this.encryptForTarget(token, target),
      target
    }, getUIOrigin(target));
  }
}
```

## Implementation Timeline

### Week 1: Foundation
- [ ] Quick Switch Bar component
- [ ] Basic keyboard shortcuts
- [ ] Simple state capture/restore
- [ ] JWT token passing

### Week 2: State Management
- [ ] Enhanced state storage
- [ ] WebSocket synchronization
- [ ] File context preservation
- [ ] Activity history

### Week 3: Deep Linking
- [ ] URL protocol implementation
- [ ] Deep link handlers
- [ ] Parameter passing
- [ ] Navigation history

### Week 4: Polish
- [ ] Visual transitions
- [ ] Context suggestions
- [ ] Performance optimizations
- [ ] Comprehensive testing

## Success Metrics

1. **Performance**
   - Switch time < 2s (95th percentile)
   - State restoration < 500ms
   - Zero data loss rate

2. **User Experience**
   - Keyboard shortcut adoption > 60%
   - User satisfaction > 4.5/5
   - Support tickets < 5/week

3. **Technical**
   - Test coverage > 90%
   - Zero security incidents
   - WebSocket uptime > 99.9%

## Conclusion

This implementation plan provides a robust, performant solution for seamless UI switching in the GRANGER ecosystem. By focusing on simplicity and user experience, we can deliver a system that feels instantaneous while maintaining full context across transitions.

The phased approach allows for iterative development and testing, ensuring each component is solid before building on top of it. The emphasis on performance optimization and comprehensive testing ensures the system will meet the <2s switching requirement reliably.