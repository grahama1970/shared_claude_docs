# GRANGER Simple UI Switching Solution

## Overview
A straightforward method for users to seamlessly switch between GRANGER's three interfaces: Chat, Annotator, and Terminal.

## Core Solution: Universal Quick Switch Bar

### 1. Persistent UI Element
A slim, always-visible bar at the top of each interface (30px height) containing:

```
[📱 Chat] [📝 Annotator] [⌨️ Terminal] | Current: Chat | Session: abc123
```

- Current interface highlighted
- Single click to switch
- Shows session ID for reference
- Minimal screen real estate

### 2. Keyboard Shortcuts (Universal)
```
Ctrl+Alt+1  →  Chat
Ctrl+Alt+2  →  Annotator  
Ctrl+Alt+3  →  Terminal
Ctrl+Tab    →  Cycle through interfaces
```

### 3. Deep Linking Protocol
Simple URL scheme that works across all platforms:
```
granger://switch/chat?session=abc123&context=current
granger://switch/annotator?doc=xyz789&page=5
granger://switch/terminal?workspace=main&cmd=last
```

## Implementation Phases

### Phase 1: Basic Switching (Week 1)
1. **Shared Auth Token**
   ```javascript
   // Store in secure location per platform
   const token = localStorage.getItem('granger-jwt');
   const session = localStorage.getItem('granger-session');
   ```

2. **Switch Handler**
   ```javascript
   function switchInterface(target) {
     // Save current state
     saveState();
     
     // Show transition overlay
     showTransition(`Switching to ${target}...`);
     
     // Launch target interface
     if (target === 'terminal') {
       window.location = 'granger://terminal/open';
     } else {
       window.location = `https://granger.local/${target}`;
     }
   }
   ```

3. **State Preservation**
   ```javascript
   const state = {
     interface: 'chat',
     position: { scrollY: 500, cursorPos: 120 },
     context: { conversationId: 'abc123', lastMessage: 42 },
     timestamp: Date.now()
   };
   
   // Save to shared storage
   localStorage.setItem('granger-state', JSON.stringify(state));
   ```

### Phase 2: Smart Context (Week 2)
1. **Context Detection**
   - If viewing PDF → Suggest Annotator
   - If running commands → Suggest Terminal
   - If asking questions → Suggest Chat

2. **Smooth Transitions**
   ```css
   .interface-transition {
     animation: fadeSwitch 0.3s ease-in-out;
   }
   
   @keyframes fadeSwitch {
     0% { opacity: 1; transform: scale(1); }
     50% { opacity: 0.5; transform: scale(0.98); }
     100% { opacity: 1; transform: scale(1); }
   }
   ```

### Phase 3: Advanced Features (Week 3)
1. **Floating Switch Widget**
   - Draggable mini-widget
   - Shows mini-previews of other interfaces
   - One-click switching

2. **Voice Commands**
   - "Switch to annotator"
   - "Open in terminal"
   - "Back to chat"

## Technical Architecture

### Shared Components
```
granger-switch/
├── switch-bar/          # Universal switch bar component
├── state-manager/       # Cross-interface state sync
├── deep-link-handler/   # URL protocol handling
└── transition-effects/  # Visual transitions
```

### Communication Flow
```
User Action → Switch Bar → State Manager → Target Interface
                              ↓
                        WebSocket Sync → Other Interfaces
```

## User Experience Flow

### Scenario 1: Chat to Annotator
1. User discussing PDF in Chat
2. Clicks PDF preview
3. System shows: "Open in Annotator?" 
4. One click → Annotator opens with PDF at exact location
5. Chat conversation preserved in background

### Scenario 2: Terminal to Chat
1. User encounters error in Terminal
2. Presses Ctrl+Alt+1
3. Chat opens with error context pre-loaded
4. "I see you encountered error X, here's how to fix it..."

### Scenario 3: Cycle Through All
1. User presses Ctrl+Tab repeatedly
2. Smooth transitions: Chat → Annotator → Terminal → Chat
3. Each interface maintains its state
4. Visual preview during transition

## Implementation Checklist

### Week 1 Deliverables
- [ ] Universal switch bar component
- [ ] Basic keyboard shortcuts
- [ ] JWT token sharing
- [ ] Simple state preservation

### Week 2 Deliverables  
- [ ] Context-aware suggestions
- [ ] Smooth visual transitions
- [ ] WebSocket state sync
- [ ] Deep link protocol

### Week 3 Deliverables
- [ ] Floating widget
- [ ] Voice commands
- [ ] Performance optimization
- [ ] Full integration testing

## Success Metrics
- Switch time: <1.5 seconds (beating 2s requirement)
- State preservation: 100% accuracy
- User satisfaction: >90% prefer new switching
- Zero data loss during switches

## Immediate Next Steps
1. Implement switch bar in all three interfaces
2. Set up shared JWT storage
3. Create basic state manager
4. Test keyboard shortcuts
5. Deploy Phase 1 for user feedback

This solution prioritizes **simplicity** and **speed** while ensuring a seamless user experience across all GRANGER interfaces.