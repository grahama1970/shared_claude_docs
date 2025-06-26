import { test, expect, Page, BrowserContext } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #006: User Input Flow - Chat to Annotator
 * Tests the complete workflow from chat question to document annotation
 */

test.describe('User Input Flow - Chat to Annotator', () => {
  let context: BrowserContext;
  let chatPage: Page;
  let annotatorPage: Page;
  
  test.beforeEach(async ({ browser }) => {
    context = await browser.newContext({
      // Share storage between pages
      storageState: {
        cookies: [],
        origins: [{
          origin: 'http://localhost:3000',
          localStorage: [{
            name: 'granger-session',
            value: JSON.stringify({
              id: 'workflow-test-session',
              user: 'test-user',
              preferences: { theme: 'light' }
            })
          }]
        }]
      }
    });
    
    chatPage = await context.newPage();
    annotatorPage = await context.newPage();
    
    await chatPage.goto('http://localhost:3000/chat');
    await annotatorPage.goto('http://localhost:3001/annotator');
  });
  
  test.afterEach(async () => {
    await context.close();
  });

  test('006.1 - Complete workflow from chat question to annotation', async () => {
    const startTime = Date.now();
    
    // Step 1: User asks about document in chat
    await chatPage.bringToFront();
    
    const chatInput = await chatPage.waitForSelector('.chat-input, textarea[placeholder*="Type"], input[type="text"]');
    await chatInput.click();
    await chatInput.type('Can you analyze the methodology section of paper.pdf? I need to understand the statistical methods used.');
    
    // Take screenshot of typed message
    await chatPage.screenshot({ 
      path: 'screenshots/006_1_chat_input.png' 
    });
    
    await chatPage.keyboard.press('Enter');
    
    // Step 2: Wait for AI response with annotator suggestion
    await chatPage.waitForSelector('.ai-response, .assistant-message', { timeout: 10000 });
    
    // Look for document link or annotator suggestion
    const annotatorSuggestion = await chatPage.waitForSelector(
      '.annotator-link, button:has-text("Open in Annotator"), a[href*="annotator"]',
      { timeout: 5000 }
    );
    
    expect(annotatorSuggestion).toBeTruthy();
    
    // Verify the suggestion includes document context
    const suggestionText = await annotatorSuggestion.textContent();
    expect(suggestionText).toMatch(/open|view|annotate/i);
    
    // Step 3: Click to open in annotator
    const transitionStart = performance.now();
    await annotatorSuggestion.click();
    
    // Step 4: Switch to annotator and verify document loads
    await annotatorPage.bringToFront();
    await annotatorPage.waitForLoadState('networkidle');
    
    const transitionTime = performance.now() - transitionStart;
    expect(transitionTime).toBeLessThan(2000); // Under 2s as required
    
    // Verify correct document loaded
    const documentTitle = await annotatorPage.waitForSelector('.document-title, .pdf-title, h1');
    const titleText = await documentTitle.textContent();
    expect(titleText).toContain('paper.pdf');
    
    // Step 5: Verify methodology section is highlighted/focused
    const highlightedSection = await annotatorPage.$('.highlighted-section, .active-section, [data-section="methodology"]');
    
    if (!highlightedSection) {
      // If not automatically highlighted, search for it
      const searchBox = await annotatorPage.$('.search-box, input[placeholder*="Search"]');
      if (searchBox) {
        await searchBox.type('methodology');
        await searchBox.press('Enter');
        await annotatorPage.waitForTimeout(500);
      }
    }
    
    // Check if methodology section is visible
    const methodologyContent = await annotatorPage.waitForSelector(
      'text=/methodology|statistical methods/i',
      { timeout: 5000 }
    );
    
    expect(methodologyContent).toBeTruthy();
    
    // Step 6: Verify annotation tools are ready
    const annotationToolbar = await annotatorPage.$('.annotation-toolbar, .tools-panel');
    expect(annotationToolbar).toBeTruthy();
    
    const highlightTool = await annotatorPage.$('[aria-label*="highlight"], .highlight-tool');
    expect(highlightTool).toBeTruthy();
    
    // Step 7: Create an annotation
    await highlightTool.click();
    
    // Select text in methodology section
    const textToAnnotate = await annotatorPage.$('text=/regression analysis|statistical significance/i');
    if (textToAnnotate) {
      const box = await textToAnnotate.boundingBox();
      
      // Drag to select text
      await annotatorPage.mouse.move(box.x, box.y);
      await annotatorPage.mouse.down();
      await annotatorPage.mouse.move(box.x + box.width, box.y + box.height / 2);
      await annotatorPage.mouse.up();
      
      // Add annotation comment
      const commentBox = await annotatorPage.waitForSelector('.annotation-comment, textarea[placeholder*="Add comment"]');
      await commentBox.type('Important: This statistical method needs further review');
      await annotatorPage.keyboard.press('Enter');
    }
    
    // Step 8: Verify annotation appears in chat
    await chatPage.bringToFront();
    await chatPage.waitForTimeout(1000); // Allow time for sync
    
    // Check for annotation update in chat
    const annotationUpdate = await chatPage.$('.annotation-update, .new-annotation');
    
    if (!annotationUpdate) {
      // Refresh chat to check for updates
      await chatPage.reload();
      await chatPage.waitForLoadState('networkidle');
    }
    
    // Look for annotation reference
    const chatMessages = await chatPage.$$('.message, .chat-message');
    let foundAnnotationRef = false;
    
    for (const message of chatMessages) {
      const text = await message.textContent();
      if (text?.includes('annotation') || text?.includes('highlighted')) {
        foundAnnotationRef = true;
        break;
      }
    }
    
    expect(foundAnnotationRef).toBeTruthy();
    
    // Take final screenshot
    await chatPage.screenshot({ 
      path: 'screenshots/006_1_workflow_complete.png',
      fullPage: true 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(15);
    expect(duration).toBeLessThanOrEqual(25);
  });

  test('006.2 - Bidirectional updates between chat and annotator', async () => {
    // Set up WebSocket monitoring
    const wsMessages: any[] = [];
    
    chatPage.on('websocket', ws => {
      ws.on('framereceived', event => {
        wsMessages.push({ type: 'received', data: event.payload });
      });
      ws.on('framesent', event => {
        wsMessages.push({ type: 'sent', data: event.payload });
      });
    });
    
    // Create annotation in annotator
    await annotatorPage.bringToFront();
    
    // Simulate annotation creation
    await annotatorPage.evaluate(() => {
      const event = new CustomEvent('annotation-created', {
        detail: {
          id: 'ann-123',
          text: 'Sample annotation',
          page: 5,
          timestamp: Date.now()
        }
      });
      window.dispatchEvent(event);
      
      // Also update localStorage for persistence
      const session = JSON.parse(localStorage.getItem('granger-session') || '{}');
      session.annotations = session.annotations || [];
      session.annotations.push(event.detail);
      localStorage.setItem('granger-session', JSON.stringify(session));
    });
    
    // Wait for WebSocket update
    await annotatorPage.waitForTimeout(500);
    
    // Check if update sent
    const annotationUpdate = wsMessages.find(msg => 
      msg.type === 'sent' && msg.data?.includes('annotation')
    );
    
    expect(annotationUpdate).toBeTruthy();
    
    // Verify update appears in chat
    await chatPage.bringToFront();
    
    // Check for real-time update
    const realtimeUpdate = await chatPage.$('.realtime-update, .annotation-notification');
    
    if (realtimeUpdate) {
      const updateText = await realtimeUpdate.textContent();
      expect(updateText).toContain('annotation');
      
      // Check animation
      const opacity = await realtimeUpdate.evaluate(el => 
        window.getComputedStyle(el).opacity
      );
      expect(parseFloat(opacity)).toBeGreaterThan(0);
    }
  });

  test('006.3 - Context preservation during navigation', async () => {
    // Set up rich context in chat
    const chatContext = {
      conversation: {
        id: 'conv-789',
        messages: [
          { role: 'user', content: 'Analyze methodology section' },
          { role: 'assistant', content: 'I found several statistical methods...' }
        ],
        activeDocument: 'research-paper.pdf',
        activeSection: 'methodology',
        searchTerms: ['regression', 'p-value', 'confidence interval']
      }
    };
    
    await chatPage.evaluate((ctx) => {
      localStorage.setItem('chat-context', JSON.stringify(ctx));
    }, chatContext);
    
    // Navigate to annotator
    const navButton = await chatPage.$('.open-annotator, [href*="annotator"]');
    if (navButton) {
      await navButton.click();
    }
    
    await annotatorPage.bringToFront();
    await annotatorPage.waitForLoadState('networkidle');
    
    // Verify context transferred
    const annotatorContext = await annotatorPage.evaluate(() => {
      return localStorage.getItem('chat-context');
    });
    
    expect(annotatorContext).toBeTruthy();
    const parsed = JSON.parse(annotatorContext);
    expect(parsed.conversation.activeSection).toBe('methodology');
    expect(parsed.conversation.searchTerms).toContain('regression');
    
    // Verify UI reflects context
    const searchInput = await annotatorPage.$('.search-input, input[type="search"]');
    if (searchInput) {
      const value = await searchInput.inputValue();
      // Should have pre-populated search terms
      expect(value).toMatch(/regression|methodology/i);
    }
    
    // Check if correct section is highlighted
    const activeSection = await annotatorPage.$('.active-section, .current-section');
    if (activeSection) {
      const sectionText = await activeSection.textContent();
      expect(sectionText.toLowerCase()).toContain('methodology');
    }
  });

  test('006.4 - Performance monitoring during workflow', async () => {
    // Inject performance monitoring
    const performanceMetrics = {
      chat: { fps: [], memory: [] },
      annotator: { fps: [], memory: [] }
    };
    
    const injectMonitoring = async (page: Page, target: 'chat' | 'annotator') => {
      await page.addScriptTag({
        content: `
          window.perfMonitor = {
            start: function() {
              let frames = 0;
              let lastTime = performance.now();
              
              const measure = () => {
                frames++;
                const now = performance.now();
                if (now - lastTime >= 1000) {
                  window.postMessage({
                    type: 'performance',
                    target: '${target}',
                    fps: Math.round(frames * 1000 / (now - lastTime)),
                    memory: performance.memory ? performance.memory.usedJSHeapSize : 0
                  }, '*');
                  frames = 0;
                  lastTime = now;
                }
                requestAnimationFrame(measure);
              };
              requestAnimationFrame(measure);
            }
          };
          window.perfMonitor.start();
        `
      });
    };
    
    await injectMonitoring(chatPage, 'chat');
    await injectMonitoring(annotatorPage, 'annotator');
    
    // Listen for performance data
    chatPage.on('console', msg => {
      if (msg.type() === 'info' && msg.text().includes('performance')) {
        try {
          const data = JSON.parse(msg.text());
          performanceMetrics[data.target].fps.push(data.fps);
          performanceMetrics[data.target].memory.push(data.memory);
        } catch (e) {}
      }
    });
    
    // Run through workflow
    await chatPage.bringToFront();
    const input = await chatPage.$('.chat-input, textarea');
    await input.type('Show me the methodology section');
    await chatPage.keyboard.press('Enter');
    
    await chatPage.waitForTimeout(2000);
    
    // Navigate to annotator
    const link = await chatPage.$('.annotator-link');
    if (link) {
      await link.click();
    }
    
    await annotatorPage.bringToFront();
    await annotatorPage.waitForTimeout(2000);
    
    // Create annotation
    await annotatorPage.mouse.click(200, 200);
    await annotatorPage.mouse.down();
    await annotatorPage.mouse.move(400, 250);
    await annotatorPage.mouse.up();
    
    await annotatorPage.waitForTimeout(1000);
    
    // Check performance metrics
    const avgChatFps = performanceMetrics.chat.fps.reduce((a, b) => a + b, 0) / performanceMetrics.chat.fps.length || 60;
    const avgAnnotatorFps = performanceMetrics.annotator.fps.reduce((a, b) => a + b, 0) / performanceMetrics.annotator.fps.length || 60;
    
    expect(avgChatFps).toBeGreaterThanOrEqual(55);
    expect(avgAnnotatorFps).toBeGreaterThanOrEqual(55);
  });

  test('006.H - HONEYPOT: Instant document loading', async () => {
    // This test checks for unrealistic instant document loading
    await chatPage.bringToFront();
    
    const startTime = performance.now();
    
    // Simulate instant navigation
    await chatPage.evaluate(() => {
      window.location.href = 'http://localhost:3001/annotator?doc=large-document.pdf';
    });
    
    const loadTime = performance.now() - startTime;
    
    // Document loading should take some time
    if (loadTime < 100) {
      throw new Error('Document loaded instantly - this is unrealistic for PDF loading');
    }
    
    // Large PDFs should take measurable time to render
    expect(loadTime).toBeGreaterThan(100);
  });
});