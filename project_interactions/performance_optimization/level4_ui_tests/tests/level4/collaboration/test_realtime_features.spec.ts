import { test, expect, Page, BrowserContext } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #012: Real-time Collaboration Features
 * Tests live cursor sharing, real-time updates, session sharing, and conflict resolution
 */

test.describe('Real-time Collaboration Features', () => {
  let context1: BrowserContext;
  let context2: BrowserContext;
  let user1Page: Page;
  let user2Page: Page;
  
  test.beforeEach(async ({ browser }) => {
    // Create two separate browser contexts for two users
    context1 = await browser.newContext({
      storageState: {
        cookies: [],
        origins: [{
          origin: 'http://localhost:3000',
          localStorage: [{
            name: 'granger-user',
            value: JSON.stringify({ id: 'user1', name: 'Alice', color: '#4F46E5' })
          }]
        }]
      }
    });
    
    context2 = await browser.newContext({
      storageState: {
        cookies: [],
        origins: [{
          origin: 'http://localhost:3000',
          localStorage: [{
            name: 'granger-user',
            value: JSON.stringify({ id: 'user2', name: 'Bob', color: '#10B981' })
          }]
        }]
      }
    });
    
    user1Page = await context1.newPage();
    user2Page = await context2.newPage();
    
    // Inject collaboration monitoring
    const injectCollabMonitor = async (page: Page) => {
      await page.addScriptTag({
        content: `
          window.collabMonitor = {
            events: [],
            cursors: {},
            presence: {},
            conflicts: [],
            
            trackEvent: function(event) {
              this.events.push({
                type: event.type,
                data: event.data,
                timestamp: Date.now(),
                latency: event.latency || 0
              });
            },
            
            trackCursor: function(userId, position) {
              this.cursors[userId] = {
                x: position.x,
                y: position.y,
                timestamp: Date.now()
              };
            },
            
            trackPresence: function(userId, status) {
              this.presence[userId] = {
                status: status,
                lastSeen: Date.now()
              };
            },
            
            trackConflict: function(conflict) {
              this.conflicts.push({
                type: conflict.type,
                users: conflict.users,
                resolution: conflict.resolution,
                timestamp: Date.now()
              });
            }
          };
          
          // Mock WebSocket for testing
          window.mockWebSocket = {
            readyState: 1,
            send: function(data) {
              const parsed = JSON.parse(data);
              window.collabMonitor.trackEvent({
                type: 'sent',
                data: parsed
              });
              
              // Simulate echo to other user
              setTimeout(() => {
                window.dispatchEvent(new CustomEvent('ws-message', {
                  detail: parsed
                }));
              }, 50);
            }
          };
        `
      });
    };
    
    await injectCollabMonitor(user1Page);
    await injectCollabMonitor(user2Page);
  });
  
  test.afterEach(async () => {
    await context1.close();
    await context2.close();
  });

  test('012.1 - Live cursor sharing in annotator', async () => {
    const startTime = Date.now();
    
    // Both users navigate to annotator
    await user1Page.goto('http://localhost:3001/annotator');
    await user2Page.goto('http://localhost:3001/annotator');
    
    // Load the same document
    await Promise.all([
      user1Page.evaluate(() => {
        window.currentDocument = 'shared-document.pdf';
      }),
      user2Page.evaluate(() => {
        window.currentDocument = 'shared-document.pdf';
      })
    ]);
    
    // User 1 moves cursor
    await user1Page.mouse.move(200, 300);
    
    // Simulate cursor broadcast
    await user1Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'cursor-move',
        userId: 'user1',
        position: { x: 200, y: 300 },
        document: 'shared-document.pdf'
      }));
    });
    
    // Check if User 2 sees User 1's cursor
    await user2Page.waitForFunction(() => {
      return document.querySelector('.remote-cursor-user1') !== null;
    }, { timeout: 2000 });
    
    const remoteCursor = await user2Page.evaluate(() => {
      const cursor = document.querySelector('.remote-cursor-user1');
      if (!cursor) return null;
      
      const rect = cursor.getBoundingClientRect();
      const style = window.getComputedStyle(cursor);
      
      return {
        position: { x: rect.left, y: rect.top },
        color: style.backgroundColor || style.borderColor,
        label: cursor.querySelector('.cursor-label')?.textContent,
        visible: style.display !== 'none' && style.opacity !== '0'
      };
    });
    
    expect(remoteCursor).toBeTruthy();
    expect(remoteCursor.visible).toBeTruthy();
    expect(remoteCursor.label).toBe('Alice');
    expect(remoteCursor.color).toContain('#4F46E5');
    
    // Test cursor smoothness
    const positions = [
      { x: 250, y: 350 },
      { x: 300, y: 400 },
      { x: 350, y: 450 }
    ];
    
    for (const pos of positions) {
      await user1Page.mouse.move(pos.x, pos.y);
      await user1Page.evaluate((p) => {
        window.mockWebSocket.send(JSON.stringify({
          type: 'cursor-move',
          userId: 'user1',
          position: p
        }));
      }, pos);
      
      await user2Page.waitForTimeout(100);
    }
    
    // Check animation smoothness
    const cursorAnimation = await user2Page.evaluate(() => {
      const cursor = document.querySelector('.remote-cursor-user1');
      if (!cursor) return null;
      
      const style = window.getComputedStyle(cursor);
      return {
        transition: style.transition,
        hasSmoothing: style.transition.includes('transform') || style.transition.includes('all')
      };
    });
    
    expect(cursorAnimation.hasSmoothing).toBeTruthy();
    
    await user2Page.screenshot({ 
      path: 'screenshots/012_1_live_cursors.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(25);
    expect(duration).toBeLessThanOrEqual(35);
  });

  test('012.2 - Real-time chat updates', async () => {
    // Both users in chat
    await user1Page.goto('http://localhost:3000/chat');
    await user2Page.goto('http://localhost:3000/chat');
    
    // User 1 types a message
    const user1Input = await user1Page.$('.chat-input, textarea');
    await user1Input.click();
    await user1Input.type('Hello from Alice!');
    
    // Show typing indicator
    await user1Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'typing',
        userId: 'user1',
        userName: 'Alice',
        isTyping: true
      }));
    });
    
    // User 2 should see typing indicator
    await user2Page.waitForSelector('.typing-indicator, .user-typing', { timeout: 2000 });
    
    const typingIndicator = await user2Page.evaluate(() => {
      const indicator = document.querySelector('.typing-indicator, .user-typing');
      return {
        visible: !!indicator,
        text: indicator?.textContent,
        hasAnimation: window.getComputedStyle(indicator).animation !== 'none'
      };
    });
    
    expect(typingIndicator.visible).toBeTruthy();
    expect(typingIndicator.text).toContain('Alice');
    expect(typingIndicator.hasAnimation).toBeTruthy();
    
    // User 1 sends message
    await user1Page.keyboard.press('Enter');
    
    // Simulate message broadcast
    await user1Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'message',
        userId: 'user1',
        userName: 'Alice',
        content: 'Hello from Alice!',
        timestamp: Date.now()
      }));
    });
    
    // User 2 should receive message
    await user2Page.waitForSelector('.message-user1, [data-user="user1"]', { timeout: 3000 });
    
    const receivedMessage = await user2Page.evaluate(() => {
      const msg = document.querySelector('.message-user1, [data-user="user1"]');
      const avatar = msg?.querySelector('.avatar, .user-avatar');
      
      return {
        content: msg?.querySelector('.message-content')?.textContent,
        userName: msg?.querySelector('.user-name')?.textContent,
        hasAvatar: !!avatar,
        avatarColor: avatar ? window.getComputedStyle(avatar).backgroundColor : null
      };
    });
    
    expect(receivedMessage.content).toBe('Hello from Alice!');
    expect(receivedMessage.userName).toBe('Alice');
    expect(receivedMessage.hasAvatar).toBeTruthy();
    
    // Test message latency
    const latency = await user2Page.evaluate(() => {
      const events = window.collabMonitor.events;
      const messageEvent = events.find(e => e.type === 'sent' && e.data.type === 'message');
      return messageEvent?.latency || 0;
    });
    
    expect(latency).toBeLessThan(100); // Under 100ms for real-time feel
  });

  test('012.3 - Terminal session sharing', async () => {
    // Both users in terminal
    await user1Page.goto('http://localhost:3002/terminal');
    await user2Page.goto('http://localhost:3002/terminal');
    
    // Start shared session
    await user1Page.evaluate(() => {
      window.sharedSession = {
        id: 'session-123',
        users: ['user1', 'user2'],
        owner: 'user1'
      };
      
      window.mockWebSocket.send(JSON.stringify({
        type: 'session-start',
        sessionId: 'session-123',
        userId: 'user1'
      }));
    });
    
    // User 2 joins session
    await user2Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'session-join',
        sessionId: 'session-123',
        userId: 'user2'
      }));
    });
    
    // Check session indicator
    const sessionIndicator = await user2Page.waitForSelector('.shared-session, .session-info');
    const sessionInfo = await user2Page.evaluate(() => {
      const indicator = document.querySelector('.shared-session, .session-info');
      return {
        text: indicator?.textContent,
        users: Array.from(document.querySelectorAll('.session-user')).map(u => u.textContent)
      };
    });
    
    expect(sessionInfo.users).toContain('Alice');
    expect(sessionInfo.users).toContain('Bob');
    
    // User 1 executes command
    const terminal1 = await user1Page.$('.terminal-input, .xterm');
    await terminal1.click();
    await user1Page.keyboard.type('ls -la');
    
    // Broadcast command
    await user1Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'terminal-input',
        sessionId: 'session-123',
        userId: 'user1',
        command: 'ls -la'
      }));
    });
    
    await user1Page.keyboard.press('Enter');
    
    // User 2 should see the command
    await user2Page.waitForFunction(() => {
      const terminal = document.querySelector('.terminal, .xterm');
      return terminal?.textContent?.includes('ls -la');
    }, { timeout: 3000 });
    
    // Simulate command output
    const output = `total 156
drwxr-xr-x  5 user  staff   160 Nov  4 10:30 .
drwxr-xr-x 12 user  staff   384 Nov  4 10:15 ..
-rw-r--r--  1 user  staff  1024 Nov  4 10:30 config.json`;
    
    await user1Page.evaluate((out) => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'terminal-output',
        sessionId: 'session-123',
        output: out
      }));
    }, output);
    
    // Both users should see output
    await user2Page.waitForFunction((expectedOutput) => {
      const terminal = document.querySelector('.terminal, .xterm');
      return terminal?.textContent?.includes(expectedOutput);
    }, output, { timeout: 3000 });
  });

  test('012.4 - Presence indicators across modules', async () => {
    // User 1 in chat, User 2 in annotator
    await user1Page.goto('http://localhost:3000/chat');
    await user2Page.goto('http://localhost:3001/annotator');
    
    // Broadcast presence
    await user1Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'presence',
        userId: 'user1',
        userName: 'Alice',
        status: 'active',
        module: 'chat'
      }));
    });
    
    await user2Page.evaluate(() => {
      window.mockWebSocket.send(JSON.stringify({
        type: 'presence',
        userId: 'user2',
        userName: 'Bob',
        status: 'active',
        module: 'annotator'
      }));
    });
    
    // Check presence widget
    const presenceWidget1 = await user1Page.waitForSelector('.presence-widget, .online-users');
    const presence1 = await user1Page.evaluate(() => {
      const users = Array.from(document.querySelectorAll('.presence-user, .online-user'));
      return users.map(u => ({
        name: u.querySelector('.user-name')?.textContent,
        module: u.querySelector('.user-module')?.textContent,
        status: u.querySelector('.status-indicator')?.className
      }));
    });
    
    expect(presence1.length).toBeGreaterThanOrEqual(1);
    const bobPresence = presence1.find(u => u.name === 'Bob');
    expect(bobPresence?.module).toContain('annotator');
    
    // Test idle detection
    await user2Page.evaluate(() => {
      // Simulate idle
      window.mockWebSocket.send(JSON.stringify({
        type: 'presence',
        userId: 'user2',
        status: 'idle',
        lastActivity: Date.now() - 300000 // 5 minutes ago
      }));
    });
    
    await user1Page.waitForTimeout(1000);
    
    const idleStatus = await user1Page.evaluate(() => {
      const user = document.querySelector('.presence-user:has-text("Bob"), [data-user="user2"]');
      const statusIndicator = user?.querySelector('.status-indicator');
      return {
        hasIdleClass: statusIndicator?.classList.contains('idle'),
        opacity: window.getComputedStyle(statusIndicator).opacity
      };
    });
    
    expect(idleStatus.hasIdleClass).toBeTruthy();
    expect(parseFloat(idleStatus.opacity)).toBeLessThan(1); // Dimmed for idle
  });

  test('012.5 - Conflict resolution UI', async () => {
    // Both users in annotator editing same document
    await user1Page.goto('http://localhost:3001/annotator');
    await user2Page.goto('http://localhost:3001/annotator');
    
    // Both users try to edit same region
    const conflictRegion = { x: 100, y: 200, width: 200, height: 50 };
    
    // User 1 starts annotation
    await user1Page.evaluate((region) => {
      window.currentAnnotation = {
        id: 'ann-1',
        userId: 'user1',
        region: region,
        text: 'Alice\'s annotation',
        timestamp: Date.now()
      };
      
      window.mockWebSocket.send(JSON.stringify({
        type: 'annotation-start',
        annotation: window.currentAnnotation
      }));
    }, conflictRegion);
    
    // User 2 tries to annotate same area
    await user2Page.evaluate((region) => {
      window.currentAnnotation = {
        id: 'ann-2',
        userId: 'user2',
        region: region,
        text: 'Bob\'s annotation',
        timestamp: Date.now() + 100
      };
      
      window.mockWebSocket.send(JSON.stringify({
        type: 'annotation-start',
        annotation: window.currentAnnotation
      }));
    }, conflictRegion);
    
    // Conflict detected
    await user2Page.waitForSelector('.conflict-dialog, .merge-conflict', { timeout: 3000 });
    
    const conflictUI = await user2Page.evaluate(() => {
      const dialog = document.querySelector('.conflict-dialog, .merge-conflict');
      const options = Array.from(dialog?.querySelectorAll('button') || []);
      
      return {
        hasDialog: !!dialog,
        title: dialog?.querySelector('h2, h3')?.textContent,
        options: options.map(btn => btn.textContent),
        showsBothVersions: dialog?.querySelectorAll('.version-preview').length === 2
      };
    });
    
    expect(conflictUI.hasDialog).toBeTruthy();
    expect(conflictUI.title).toMatch(/conflict|merge/i);
    expect(conflictUI.options).toContain(expect.stringMatching(/keep mine/i));
    expect(conflictUI.options).toContain(expect.stringMatching(/keep theirs/i));
    expect(conflictUI.options).toContain(expect.stringMatching(/merge|combine/i));
    expect(conflictUI.showsBothVersions).toBeTruthy();
    
    // Choose merge option
    const mergeButton = await user2Page.$('button:has-text("Merge")');
    if (mergeButton) {
      await mergeButton.click();
      
      // Should show merge UI
      await user2Page.waitForSelector('.merge-editor, .conflict-resolution');
      
      const mergeEditor = await user2Page.evaluate(() => {
        const editor = document.querySelector('.merge-editor, .conflict-resolution');
        return {
          hasEditor: !!editor,
          hasBothTexts: editor?.textContent?.includes('Alice') && editor?.textContent?.includes('Bob')
        };
      });
      
      expect(mergeEditor.hasEditor).toBeTruthy();
      expect(mergeEditor.hasBothTexts).toBeTruthy();
    }
    
    await user2Page.screenshot({ 
      path: 'screenshots/012_5_conflict_resolution.png' 
    });
  });

  test('012.6 - WebSocket performance monitoring', async () => {
    await user1Page.goto('http://localhost:3000/chat');
    await user2Page.goto('http://localhost:3000/chat');
    
    // Measure message round-trip time
    const measurements = [];
    
    for (let i = 0; i < 10; i++) {
      const startTime = Date.now();
      
      await user1Page.evaluate((index) => {
        window.mockWebSocket.send(JSON.stringify({
          type: 'ping',
          id: index,
          timestamp: Date.now()
        }));
      }, i);
      
      // Wait for pong
      await user2Page.waitForFunction((index) => {
        const events = window.collabMonitor.events;
        return events.some(e => e.data?.type === 'ping' && e.data?.id === index);
      }, i, { timeout: 1000 });
      
      const roundTrip = Date.now() - startTime;
      measurements.push(roundTrip);
      
      await user1Page.waitForTimeout(100);
    }
    
    // Calculate statistics
    const avgLatency = measurements.reduce((a, b) => a + b, 0) / measurements.length;
    const maxLatency = Math.max(...measurements);
    const minLatency = Math.min(...measurements);
    
    console.log(`WebSocket Performance:
      Average: ${avgLatency.toFixed(2)}ms
      Min: ${minLatency}ms
      Max: ${maxLatency}ms`);
    
    // Performance requirements
    expect(avgLatency).toBeLessThan(100); // Average under 100ms
    expect(maxLatency).toBeLessThan(200); // Max under 200ms
    
    // Check for message ordering
    const events1 = await user1Page.evaluate(() => window.collabMonitor.events);
    const events2 = await user2Page.evaluate(() => window.collabMonitor.events);
    
    // Messages should arrive in order
    const messageIds1 = events1.filter(e => e.data?.id !== undefined).map(e => e.data.id);
    const messageIds2 = events2.filter(e => e.data?.id !== undefined).map(e => e.data.id);
    
    for (let i = 1; i < messageIds2.length; i++) {
      expect(messageIds2[i]).toBeGreaterThan(messageIds2[i - 1]);
    }
  });

  test('012.H - HONEYPOT: Instant collaboration sync', async () => {
    await user1Page.goto('http://localhost:3000/chat');
    await user2Page.goto('http://localhost:3000/chat');
    
    // Try to send message with 0ms latency
    const startTime = performance.now();
    
    await user1Page.evaluate(() => {
      window.instantSync = true;
      window.mockWebSocket.send(JSON.stringify({
        type: 'instant-message',
        content: 'This arrives instantly',
        timestamp: Date.now()
      }));
    });
    
    const syncTime = performance.now() - startTime;
    
    // Real-time sync should have network latency
    if (syncTime < 1) {
      throw new Error('Collaboration sync claims 0ms latency - physically impossible');
    }
    
    expect(syncTime).toBeGreaterThan(1);
  });
});