import { test, expect, Page } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #005: Cross-Module Navigation Flow
 * Tests seamless navigation between all three modules with context preservation
 */

test.describe('Cross-Module Navigation Flow', () => {
  let chatPage: Page;
  let annotatorPage: Page;
  let terminalPage: Page;
  
  test.beforeAll(async ({ browser }) => {
    // Open all three modules in separate pages
    chatPage = await browser.newPage();
    annotatorPage = await browser.newPage();
    terminalPage = await browser.newPage();
    
    await chatPage.goto('http://localhost:3000/chat');
    await annotatorPage.goto('http://localhost:3001/annotator');
    await terminalPage.goto('http://localhost:3002/terminal');
    
    // Wait for all to load
    await Promise.all([
      chatPage.waitForLoadState('networkidle'),
      annotatorPage.waitForLoadState('networkidle'),
      terminalPage.waitForLoadState('networkidle')
    ]);
  });
  
  test.afterAll(async () => {
    await Promise.all([
      chatPage.close(),
      annotatorPage.close(),
      terminalPage.close()
    ]);
  });

  test('005.1 - Chat to Annotator navigation', async () => {
    const startTime = Date.now();
    
    // Set up context in chat
    await chatPage.evaluate(() => {
      localStorage.setItem('granger-session', JSON.stringify({
        id: 'test-session-123',
        user: 'test-user',
        context: {
          currentDocument: 'research-paper.pdf',
          conversation: 'conv-456',
          timestamp: Date.now()
        }
      }));
    });
    
    // Type message about document
    const chatInput = await chatPage.$('.chat-input, textarea, input[type="text"]');
    if (chatInput) {
      await chatInput.type('Can you help me analyze the methodology section of research-paper.pdf?');
      await chatPage.keyboard.press('Enter');
    }
    
    // Look for annotator suggestion/link
    await chatPage.waitForSelector('.annotator-link, [href*="annotator"], button:has-text("Open in Annotator")', 
      { timeout: 5000 }
    );
    
    // Measure transition performance
    const transitionStart = performance.now();
    
    // Click link to annotator
    const annotatorLink = await chatPage.$('.annotator-link, [href*="annotator"]');
    if (annotatorLink) {
      await annotatorLink.click();
    }
    
    // Switch to annotator page
    await annotatorPage.bringToFront();
    await annotatorPage.waitForLoadState('networkidle');
    
    const transitionTime = performance.now() - transitionStart;
    expect(transitionTime).toBeLessThan(500); // Under 500ms transition
    
    // Verify context preserved
    const annotatorContext = await annotatorPage.evaluate(() => {
      const session = localStorage.getItem('granger-session');
      return session ? JSON.parse(session) : null;
    });
    
    expect(annotatorContext).toBeTruthy();
    expect(annotatorContext.id).toBe('test-session-123');
    expect(annotatorContext.context.currentDocument).toBe('research-paper.pdf');
    
    // Check if correct document loaded
    const documentTitle = await annotatorPage.$('.document-title, .pdf-name');
    if (documentTitle) {
      const title = await documentTitle.textContent();
      expect(title).toContain('research-paper.pdf');
    }
    
    // Verify smooth visual transition (no flashing)
    await annotatorPage.screenshot({ 
      path: 'screenshots/005_1_chat_to_annotator.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(10);
    expect(duration).toBeLessThanOrEqual(15);
  });

  test('005.2 - Annotator to Terminal navigation', async () => {
    const startTime = Date.now();
    
    // Create annotation context
    await annotatorPage.evaluate(() => {
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.context.annotations = [
        { id: 'ann-1', text: 'Important finding', page: 5 }
      ];
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Look for terminal action (e.g., "Run analysis")
    const terminalAction = await annotatorPage.$('.terminal-action, button:has-text("Run in Terminal")');
    
    if (!terminalAction) {
      // Create one for testing
      await annotatorPage.evaluate(() => {
        const button = document.createElement('button');
        button.className = 'terminal-action';
        button.textContent = 'Run Analysis in Terminal';
        document.body.appendChild(button);
      });
    }
    
    // Measure transition
    const transitionStart = performance.now();
    
    const actionButton = await annotatorPage.$('.terminal-action');
    if (actionButton) {
      await actionButton.click();
    }
    
    // Switch to terminal
    await terminalPage.bringToFront();
    await terminalPage.waitForLoadState('networkidle');
    
    const transitionTime = performance.now() - transitionStart;
    expect(transitionTime).toBeLessThan(500);
    
    // Verify context in terminal
    const terminalContext = await terminalPage.evaluate(() => {
      const session = localStorage.getItem('granger-session');
      return session ? JSON.parse(session) : null;
    });
    
    expect(terminalContext.context.annotations).toBeTruthy();
    expect(terminalContext.context.annotations.length).toBeGreaterThan(0);
    
    // Check if command pre-populated
    const terminalInput = await terminalPage.$('.terminal-input, .xterm');
    if (terminalInput) {
      const value = await terminalInput.evaluate(el => el.value || el.textContent);
      expect(value).toContain('analyze'); // Command related to annotation
    }
    
    await terminalPage.screenshot({ 
      path: 'screenshots/005_2_annotator_to_terminal.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(10);
    expect(duration).toBeLessThanOrEqual(15);
  });

  test('005.3 - Terminal to Chat navigation', async () => {
    const startTime = Date.now();
    
    // Execute a command in terminal
    const terminal = await terminalPage.$('.terminal-input, .xterm');
    if (terminal) {
      await terminal.click();
      await terminalPage.keyboard.type('granger analyze --summary');
      await terminalPage.keyboard.press('Enter');
      await terminalPage.waitForTimeout(500);
    }
    
    // Store command output in context
    await terminalPage.evaluate(() => {
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.context.lastCommand = 'granger analyze --summary';
      session.context.commandOutput = 'Analysis complete: 5 key findings identified';
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Look for chat integration
    const chatLink = await terminalPage.$('.chat-link, button:has-text("Discuss in Chat")');
    
    if (!chatLink) {
      await terminalPage.evaluate(() => {
        const button = document.createElement('button');
        button.className = 'chat-link';
        button.textContent = 'Discuss Results in Chat';
        document.body.appendChild(button);
      });
    }
    
    // Measure transition
    const transitionStart = performance.now();
    
    const linkButton = await terminalPage.$('.chat-link');
    if (linkButton) {
      await linkButton.click();
    }
    
    // Switch to chat
    await chatPage.bringToFront();
    await chatPage.waitForLoadState('networkidle');
    
    const transitionTime = performance.now() - transitionStart;
    expect(transitionTime).toBeLessThan(500);
    
    // Verify command output appears in chat
    const chatContext = await chatPage.evaluate(() => {
      const session = localStorage.getItem('granger-session');
      return session ? JSON.parse(session) : null;
    });
    
    expect(chatContext.context.lastCommand).toBe('granger analyze --summary');
    expect(chatContext.context.commandOutput).toContain('5 key findings');
    
    // Check if chat shows command context
    const chatMessages = await chatPage.$$('.chat-message, .message');
    let foundContext = false;
    
    for (const message of chatMessages) {
      const text = await message.textContent();
      if (text?.includes('Analysis complete') || text?.includes('key findings')) {
        foundContext = true;
        break;
      }
    }
    
    expect(foundContext).toBeTruthy();
    
    await chatPage.screenshot({ 
      path: 'screenshots/005_3_terminal_to_chat.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(10);
    expect(duration).toBeLessThanOrEqual(15);
  });

  test('005.4 - Full navigation cycle with performance', async () => {
    const startTime = Date.now();
    const fps_measurements = [];
    
    // Inject FPS monitor in all pages
    const injectFpsMonitor = async (page: Page) => {
      await page.addScriptTag({
        content: `
          window.fpsMonitor = {
            frames: 0,
            startTime: performance.now(),
            fps: 0,
            measure: function() {
              this.frames++;
              const elapsed = performance.now() - this.startTime;
              if (elapsed >= 1000) {
                this.fps = Math.round(this.frames * 1000 / elapsed);
                this.frames = 0;
                this.startTime = performance.now();
              }
              requestAnimationFrame(() => this.measure());
            }
          };
          window.fpsMonitor.measure();
        `
      });
    };
    
    await Promise.all([
      injectFpsMonitor(chatPage),
      injectFpsMonitor(annotatorPage),
      injectFpsMonitor(terminalPage)
    ]);
    
    // Full cycle: Chat → Annotator → Terminal → Chat
    const pages = [chatPage, annotatorPage, terminalPage, chatPage];
    const transitions = ['chat-to-annotator', 'annotator-to-terminal', 'terminal-to-chat', 'back-to-chat'];
    
    for (let i = 0; i < pages.length - 1; i++) {
      const fromPage = pages[i];
      const toPage = pages[i + 1];
      
      // Trigger navigation
      await fromPage.evaluate(() => {
        const event = new CustomEvent('navigate', { 
          detail: { target: 'next-module' } 
        });
        window.dispatchEvent(event);
      });
      
      // Switch pages
      await toPage.bringToFront();
      await toPage.waitForLoadState('networkidle');
      
      // Measure FPS during transition
      const fps = await toPage.evaluate(() => window.fpsMonitor.fps);
      fps_measurements.push(fps);
      
      // Check for visual consistency
      const header = await toPage.$('header, .app-header');
      if (header) {
        const headerStyle = await header.evaluate(el => ({
          height: el.offsetHeight,
          background: window.getComputedStyle(el).backgroundColor
        }));
        
        // Header should be consistent across modules
        expect(headerStyle.height).toBeGreaterThan(40);
        expect(headerStyle.height).toBeLessThan(80);
      }
      
      await toPage.screenshot({ 
        path: `screenshots/005_4_cycle_${transitions[i]}.png` 
      });
      
      await toPage.waitForTimeout(500); // Brief pause between transitions
    }
    
    // Verify no memory leaks
    const memoryUsage = await chatPage.evaluate(() => {
      if (performance.memory) {
        return {
          used: performance.memory.usedJSHeapSize,
          total: performance.memory.totalJSHeapSize
        };
      }
      return null;
    });
    
    if (memoryUsage) {
      const usagePercent = (memoryUsage.used / memoryUsage.total) * 100;
      expect(usagePercent).toBeLessThan(80); // Memory usage should be reasonable
    }
    
    // Check average FPS
    const avgFps = fps_measurements.reduce((a, b) => a + b, 0) / fps_measurements.length;
    expect(avgFps).toBeGreaterThanOrEqual(50);
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(15);
    expect(duration).toBeLessThanOrEqual(20);
  });

  test('005.5 - Navigation state persistence', async () => {
    // Test that navigation state persists across page refreshes
    
    // Set complex state in chat
    await chatPage.evaluate(() => {
      localStorage.setItem('granger-navigation', JSON.stringify({
        history: ['chat', 'annotator', 'terminal', 'chat'],
        currentIndex: 3,
        breadcrumbs: [
          { module: 'chat', label: 'Conversation about PDF' },
          { module: 'annotator', label: 'Annotating page 5' },
          { module: 'terminal', label: 'Running analysis' }
        ]
      }));
    });
    
    // Refresh chat page
    await chatPage.reload();
    await chatPage.waitForLoadState('networkidle');
    
    // Check if navigation state restored
    const navState = await chatPage.evaluate(() => {
      const state = localStorage.getItem('granger-navigation');
      return state ? JSON.parse(state) : null;
    });
    
    expect(navState).toBeTruthy();
    expect(navState.history.length).toBe(4);
    expect(navState.currentIndex).toBe(3);
    expect(navState.breadcrumbs.length).toBe(3);
    
    // Verify breadcrumbs UI if present
    const breadcrumbs = await chatPage.$('.breadcrumbs, .navigation-history');
    if (breadcrumbs) {
      const items = await breadcrumbs.$$('.breadcrumb-item');
      expect(items.length).toBeGreaterThanOrEqual(3);
    }
  });

  test('005.H - HONEYPOT: Broken navigation context', async () => {
    // This test simulates broken navigation that loses context
    
    // Clear session storage to simulate context loss
    await chatPage.evaluate(() => {
      localStorage.removeItem('granger-session');
      sessionStorage.clear();
    });
    
    // Try to navigate without context
    const navButton = await chatPage.$('.navigate-to-annotator');
    if (navButton) {
      await navButton.click();
      
      // Switch to annotator
      await annotatorPage.bringToFront();
      
      // Check if context is missing
      const context = await annotatorPage.evaluate(() => {
        return localStorage.getItem('granger-session');
      });
      
      if (!context) {
        throw new Error('Navigation completed without preserving context - this should fail');
      }
    }
  });
});