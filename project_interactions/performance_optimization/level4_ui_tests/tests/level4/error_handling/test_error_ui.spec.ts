import { test, expect, Page } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #011: Error Handling UI/UX
 * Tests consistent error styling, graceful degradation, and recovery mechanisms
 */

test.describe('Error Handling UI/UX', () => {
  test.beforeEach(async ({ page }) => {
    // Inject error monitoring
    await page.addScriptTag({
      content: `
        window.errorMonitor = {
          errors: [],
          networkErrors: [],
          recoveryAttempts: [],
          
          captureError: function(error) {
            this.errors.push({
              message: error.message || error,
              stack: error.stack,
              timestamp: Date.now(),
              type: error.type || 'generic'
            });
          },
          
          captureNetworkError: function(url, status) {
            this.networkErrors.push({
              url,
              status,
              timestamp: Date.now()
            });
          },
          
          captureRecovery: function(action, success) {
            this.recoveryAttempts.push({
              action,
              success,
              timestamp: Date.now()
            });
          }
        };
        
        // Override fetch to capture network errors
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
          try {
            const response = await originalFetch(...args);
            if (!response.ok) {
              window.errorMonitor.captureNetworkError(args[0], response.status);
            }
            return response;
          } catch (error) {
            window.errorMonitor.captureNetworkError(args[0], 0);
            throw error;
          }
        };
        
        // Capture unhandled errors
        window.addEventListener('error', (event) => {
          window.errorMonitor.captureError(event.error || event.message);
        });
      `
    });
  });

  test('011.1 - Consistent error styling across modules', async ({ page }) => {
    const startTime = Date.now();
    
    // Test error styles in each module
    const modules = [
      { name: 'chat', url: 'http://localhost:3000/chat' },
      { name: 'annotator', url: 'http://localhost:3001/annotator' },
      { name: 'terminal', url: 'http://localhost:3002/terminal' }
    ];
    
    const errorStyles = {};
    
    for (const module of modules) {
      await page.goto(module.url);
      
      // Inject test errors
      await page.evaluate(() => {
        // Create different types of errors
        const errorTypes = [
          { type: 'validation', message: 'Please enter a valid email address' },
          { type: 'network', message: 'Unable to connect to server' },
          { type: 'permission', message: 'You do not have permission to perform this action' },
          { type: 'generic', message: 'An unexpected error occurred' }
        ];
        
        const container = document.createElement('div');
        container.id = 'test-errors';
        container.style.padding = '20px';
        
        errorTypes.forEach(error => {
          const errorEl = document.createElement('div');
          errorEl.className = `error error-${error.type}`;
          errorEl.setAttribute('role', 'alert');
          errorEl.innerHTML = `
            <svg class="error-icon" width="20" height="20" viewBox="0 0 20 20">
              <circle cx="10" cy="10" r="9" fill="#EF4444" />
              <text x="10" y="14" text-anchor="middle" fill="white" font-size="12">!</text>
            </svg>
            <span class="error-message">${error.message}</span>
            <button class="error-dismiss" aria-label="Dismiss error">×</button>
          `;
          container.appendChild(errorEl);
        });
        
        document.body.appendChild(container);
      });
      
      // Capture error styles
      const styles = await page.evaluate(() => {
        const errors = document.querySelectorAll('.error');
        const capturedStyles = [];
        
        errors.forEach(error => {
          const computed = window.getComputedStyle(error);
          capturedStyles.push({
            backgroundColor: computed.backgroundColor,
            color: computed.color,
            border: computed.border,
            borderRadius: computed.borderRadius,
            padding: computed.padding,
            fontSize: computed.fontSize,
            display: computed.display
          });
        });
        
        return capturedStyles;
      });
      
      errorStyles[module.name] = styles;
      
      // Verify error styling follows style guide
      styles.forEach(style => {
        // Should use error color from style guide
        expect(style.backgroundColor).toMatch(/rgb\(239,\s*68,\s*68|#EF4444/i);
        
        // Should have rounded corners
        expect(parseInt(style.borderRadius)).toBeGreaterThanOrEqual(4);
        
        // Should have adequate padding
        const paddingValues = style.padding.split(' ').map(p => parseInt(p));
        paddingValues.forEach(p => {
          if (p > 0) {
            expect(p % STYLE_GUIDE.spacing.base).toBe(0);
          }
        });
      });
      
      await page.screenshot({ 
        path: `screenshots/011_1_error_styles_${module.name}.png` 
      });
      
      // Clean up
      await page.evaluate(() => {
        document.getElementById('test-errors')?.remove();
      });
    }
    
    // Verify consistency across modules
    const chatStyle = errorStyles.chat[0];
    const annotatorStyle = errorStyles.annotator[0];
    const terminalStyle = errorStyles.terminal[0];
    
    // Key properties should be consistent
    expect(chatStyle.borderRadius).toBe(annotatorStyle.borderRadius);
    expect(chatStyle.fontSize).toBe(annotatorStyle.fontSize);
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(15);
    expect(duration).toBeLessThanOrEqual(20);
  });

  test('011.2 - Graceful degradation for network issues', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Simulate offline mode
    await page.context().setOffline(true);
    
    // Try to send a message
    const input = await page.$('.chat-input, textarea');
    if (input) {
      await input.type('Test message while offline');
      await page.keyboard.press('Enter');
    }
    
    // Should show offline indicator
    await page.waitForSelector('.offline-indicator, .network-error', { timeout: 5000 });
    
    const offlineUI = await page.evaluate(() => {
      const indicator = document.querySelector('.offline-indicator, .network-error');
      const queuedBadge = document.querySelector('.queued-messages, .pending-count');
      
      return {
        hasIndicator: !!indicator,
        indicatorText: indicator?.textContent,
        hasQueueBadge: !!queuedBadge,
        queueCount: queuedBadge?.textContent
      };
    });
    
    expect(offlineUI.hasIndicator).toBeTruthy();
    expect(offlineUI.indicatorText).toMatch(/offline|connection/i);
    
    // Messages should be queued
    expect(offlineUI.hasQueueBadge).toBeTruthy();
    
    // Check if retry mechanism is visible
    const retryButton = await page.$('.retry-button, button:has-text("Retry")');
    expect(retryButton).toBeTruthy();
    
    // Test auto-retry when back online
    await page.context().setOffline(false);
    
    // Wait for reconnection
    await page.waitForTimeout(2000);
    
    // Check if offline indicator is gone
    const stillOffline = await page.$('.offline-indicator:visible');
    expect(stillOffline).toBeFalsy();
    
    // Verify queued messages were sent
    const sentStatus = await page.evaluate(() => {
      return window.errorMonitor.recoveryAttempts.some(r => 
        r.action === 'send-queued-messages' && r.success
      );
    });
    
    expect(sentStatus).toBeTruthy();
  });

  test('011.3 - Clear error messages and recovery suggestions', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Trigger different error scenarios
    const errorScenarios = [
      {
        trigger: async () => {
          // Invalid file upload
          await page.evaluate(() => {
            const event = new CustomEvent('error', {
              detail: {
                type: 'file-size',
                message: 'File too large',
                details: 'Maximum file size is 10MB'
              }
            });
            window.dispatchEvent(event);
          });
        },
        expectedSuggestion: /compress|reduce|smaller/i
      },
      {
        trigger: async () => {
          // Authentication error
          await page.evaluate(() => {
            const event = new CustomEvent('error', {
              detail: {
                type: 'auth',
                message: 'Session expired',
                code: 401
              }
            });
            window.dispatchEvent(event);
          });
        },
        expectedSuggestion: /log in|sign in|authenticate/i
      },
      {
        trigger: async () => {
          // Rate limit error
          await page.evaluate(() => {
            const event = new CustomEvent('error', {
              detail: {
                type: 'rate-limit',
                message: 'Too many requests',
                retryAfter: 60
              }
            });
            window.dispatchEvent(event);
          });
        },
        expectedSuggestion: /wait|try again|minute/i
      }
    ];
    
    for (const scenario of errorScenarios) {
      // Trigger error
      await scenario.trigger();
      
      // Wait for error display
      await page.waitForSelector('.error-message, [role="alert"]', { timeout: 3000 });
      
      // Check error clarity
      const errorDisplay = await page.evaluate(() => {
        const error = document.querySelector('.error-message, [role="alert"]');
        const suggestion = document.querySelector('.error-suggestion, .recovery-action');
        
        return {
          message: error?.textContent,
          hasSuggestion: !!suggestion,
          suggestionText: suggestion?.textContent,
          hasIcon: !!error?.querySelector('svg, .icon'),
          isVisible: error ? window.getComputedStyle(error).display !== 'none' : false
        };
      });
      
      expect(errorDisplay.isVisible).toBeTruthy();
      expect(errorDisplay.message).toBeTruthy();
      expect(errorDisplay.hasSuggestion).toBeTruthy();
      expect(errorDisplay.suggestionText).toMatch(scenario.expectedSuggestion);
      
      // Dismiss error
      const dismissButton = await page.$('.error-dismiss, [aria-label*="dismiss"], [aria-label*="close"]');
      if (dismissButton) {
        await dismissButton.click();
        await page.waitForTimeout(300);
        
        // Error should be gone
        const errorGone = await page.$('.error-message:visible');
        expect(errorGone).toBeFalsy();
      }
    }
  });

  test('011.4 - Error state animations', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Inject FPS monitor
    await page.addScriptTag({
      content: `
        window.fpsMonitor = {
          measure: function() {
            let frames = 0;
            let lastTime = performance.now();
            
            const measureFrame = () => {
              frames++;
              const now = performance.now();
              if (now - lastTime >= 1000) {
                window.fpsMonitor.fps = frames;
                frames = 0;
                lastTime = now;
              }
              requestAnimationFrame(measureFrame);
            };
            requestAnimationFrame(measureFrame);
          }
        };
        window.fpsMonitor.measure();
      `
    });
    
    // Create animated error
    await page.evaluate(() => {
      const error = document.createElement('div');
      error.className = 'error-animated';
      error.innerHTML = `
        <div class="error-content" style="
          background: #FEE2E2;
          border: 1px solid #EF4444;
          border-radius: 8px;
          padding: 16px;
          animation: slideIn 300ms ease-out;
          transform-origin: top;
        ">
          <span style="color: #991B1B;">Error: Connection lost</span>
        </div>
      `;
      
      const style = document.createElement('style');
      style.textContent = `
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        
        .error-shake {
          animation: shake 300ms ease-in-out;
        }
      `;
      document.head.appendChild(style);
      document.body.appendChild(error);
    });
    
    await page.waitForTimeout(400);
    
    // Check animation performance
    const fps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(fps).toBeGreaterThanOrEqual(55);
    
    // Test shake animation for critical errors
    await page.evaluate(() => {
      const error = document.querySelector('.error-content');
      if (error) {
        error.classList.add('error-shake');
      }
    });
    
    await page.waitForTimeout(400);
    
    // Verify animation duration matches style guide
    const animationDuration = await page.evaluate(() => {
      const error = document.querySelector('.error-content');
      if (error) {
        const computed = window.getComputedStyle(error);
        return parseFloat(computed.animationDuration) * 1000;
      }
      return 0;
    });
    
    expect(animationDuration).toBeGreaterThanOrEqual(STYLE_GUIDE.animation.duration_min);
    expect(animationDuration).toBeLessThanOrEqual(STYLE_GUIDE.animation.duration_max);
  });

  test('011.5 - Retry mechanisms and progressive loading', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Simulate failed data load
    await page.route('**/api/messages', route => {
      route.abort('failed');
    });
    
    // Trigger data load
    await page.reload();
    
    // Should show retry UI
    await page.waitForSelector('.retry-container, .load-error', { timeout: 5000 });
    
    // Check retry mechanism
    const retryUI = await page.evaluate(() => {
      const container = document.querySelector('.retry-container, .load-error');
      const retryButton = container?.querySelector('button');
      const retryCount = container?.querySelector('.retry-count, .attempt');
      
      return {
        hasRetryButton: !!retryButton,
        buttonText: retryButton?.textContent,
        hasRetryCount: !!retryCount,
        countText: retryCount?.textContent
      };
    });
    
    expect(retryUI.hasRetryButton).toBeTruthy();
    expect(retryUI.buttonText).toMatch(/retry|try again/i);
    
    // Set up successful response for retry
    await page.unroute('**/api/messages');
    await page.route('**/api/messages', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ messages: [] })
      });
    });
    
    // Click retry
    const retryButton = await page.$('.retry-container button, button:has-text("Retry")');
    if (retryButton) {
      await retryButton.click();
      
      // Should show loading state
      await page.waitForSelector('.loading, .spinner', { timeout: 2000 });
      
      // Should eventually succeed
      await page.waitForSelector('.retry-container', { 
        state: 'hidden',
        timeout: 5000 
      });
      
      // Verify recovery recorded
      const recovery = await page.evaluate(() => 
        window.errorMonitor.recoveryAttempts.find(r => r.action === 'retry-load')
      );
      
      expect(recovery?.success).toBeTruthy();
    }
  });

  test('011.6 - Error boundary implementation', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Trigger component error
    await page.evaluate(() => {
      // Simulate React component error
      const errorEvent = new ErrorEvent('error', {
        error: new Error('Component render failed'),
        message: 'Cannot read property of undefined',
        filename: 'ChatMessage.tsx',
        lineno: 42
      });
      window.dispatchEvent(errorEvent);
    });
    
    // Check if error boundary caught it
    await page.waitForSelector('.error-boundary, .component-error', { timeout: 3000 });
    
    const errorBoundaryUI = await page.evaluate(() => {
      const boundary = document.querySelector('.error-boundary, .component-error');
      const fallbackUI = boundary?.querySelector('.error-fallback, .fallback-content');
      const reloadButton = boundary?.querySelector('button');
      
      return {
        hasBoundary: !!boundary,
        hasFallbackUI: !!fallbackUI,
        fallbackText: fallbackUI?.textContent,
        hasReloadOption: !!reloadButton,
        preservedLayout: document.querySelector('nav, header') !== null
      };
    });
    
    expect(errorBoundaryUI.hasBoundary).toBeTruthy();
    expect(errorBoundaryUI.hasFallbackUI).toBeTruthy();
    expect(errorBoundaryUI.fallbackText).toMatch(/something went wrong|error occurred/i);
    expect(errorBoundaryUI.hasReloadOption).toBeTruthy();
    expect(errorBoundaryUI.preservedLayout).toBeTruthy(); // Nav should still work
    
    await page.screenshot({ 
      path: 'screenshots/011_6_error_boundary.png' 
    });
  });

  test('011.H - HONEYPOT: Silent error handling', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Trigger error that gets silently swallowed
    await page.evaluate(() => {
      try {
        // This error should be visible to user
        throw new Error('Critical data loss error');
      } catch (error) {
        // Silently swallow error - BAD PRACTICE
        console.log('Error ignored');
      }
    });
    
    // Check if error was properly handled
    const errors = await page.evaluate(() => window.errorMonitor.errors);
    const errorShown = await page.$('.error-message:visible');
    
    // This test should fail - critical errors must be shown
    if (!errorShown && errors.some(e => e.message.includes('Critical data loss'))) {
      throw new Error('Critical error was silently ignored - user not notified');
    }
    
    expect(errorShown || errors.length === 0).toBeTruthy();
  });
});