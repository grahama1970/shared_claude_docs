import { test, expect, Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Task #010: Accessibility Compliance - Full Journey
 * Tests WCAG AA compliance across all modules with keyboard navigation and screen reader support
 */

test.describe('Accessibility Compliance - Full Journey', () => {
  test.beforeEach(async ({ page }) => {
    // Inject accessibility testing utilities
    await page.addScriptTag({
      content: `
        window.a11yMonitor = {
          focusPath: [],
          keyPresses: [],
          announcements: [],
          
          trackFocus: function() {
            document.addEventListener('focusin', (e) => {
              this.focusPath.push({
                element: e.target.tagName,
                id: e.target.id,
                class: e.target.className,
                label: e.target.getAttribute('aria-label') || e.target.textContent?.substring(0, 50),
                timestamp: Date.now()
              });
            });
          },
          
          trackKeys: function() {
            document.addEventListener('keydown', (e) => {
              this.keyPresses.push({
                key: e.key,
                code: e.code,
                target: e.target.tagName,
                timestamp: Date.now()
              });
            });
          },
          
          trackAnnouncements: function() {
            // Monitor ARIA live regions
            const observer = new MutationObserver((mutations) => {
              mutations.forEach(mutation => {
                const target = mutation.target;
                if (target.getAttribute('aria-live') || 
                    target.getAttribute('role') === 'alert' ||
                    target.getAttribute('role') === 'status') {
                  this.announcements.push({
                    text: target.textContent,
                    role: target.getAttribute('role'),
                    timestamp: Date.now()
                  });
                }
              });
            });
            
            observer.observe(document.body, {
              childList: true,
              subtree: true,
              characterData: true
            });
          }
        };
        
        // Start monitoring
        window.a11yMonitor.trackFocus();
        window.a11yMonitor.trackKeys();
        window.a11yMonitor.trackAnnouncements();
      `
    });
  });

  test('010.1 - Full keyboard navigation across all modules', async ({ page }) => {
    const startTime = Date.now();
    
    // Start at chat module
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
    
    // Press Tab to start keyboard navigation
    await page.keyboard.press('Tab');
    
    // Navigate through chat interface
    const chatElements = [
      'Skip to main content',
      'Navigation',
      'Chat',
      'Annotator', 
      'Terminal',
      'New conversation',
      'Message input',
      'Send button'
    ];
    
    for (const expectedElement of chatElements) {
      const focusedElement = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tag: el?.tagName,
          text: el?.textContent?.trim(),
          label: el?.getAttribute('aria-label'),
          role: el?.getAttribute('role'),
          tabindex: el?.getAttribute('tabindex')
        };
      });
      
      // Verify element is focusable
      expect(focusedElement.tag).not.toBe('BODY');
      
      // Press Tab to next element
      await page.keyboard.press('Tab');
      await page.waitForTimeout(100);
    }
    
    // Navigate to annotator using keyboard
    await page.keyboard.press('Tab'); // Focus on annotator link
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    
    // Find and activate annotator link
    const focusedLink = await page.evaluate(() => {
      const el = document.activeElement;
      return el?.textContent?.includes('Annotator');
    });
    
    if (focusedLink) {
      await page.keyboard.press('Enter');
      await page.waitForURL('**/annotator');
    }
    
    // Test keyboard navigation in annotator
    const annotatorElements = [
      'Document viewer',
      'Annotation tools',
      'Highlight',
      'Comment',
      'Save'
    ];
    
    for (let i = 0; i < annotatorElements.length; i++) {
      await page.keyboard.press('Tab');
      await page.waitForTimeout(100);
      
      const focused = await page.evaluate(() => {
        return document.activeElement?.getAttribute('aria-label') || 
               document.activeElement?.textContent;
      });
      
      console.log(`Focused element ${i}: ${focused}`);
    }
    
    // Navigate to terminal
    await page.keyboard.down('Shift');
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press('Tab'); // Shift+Tab to go backwards
    }
    await page.keyboard.up('Shift');
    
    // Test terminal keyboard access
    await page.goto('http://localhost:3002/terminal');
    await page.keyboard.press('Tab');
    
    const terminalInput = await page.evaluate(() => {
      return document.activeElement?.tagName === 'INPUT' || 
             document.activeElement?.tagName === 'TEXTAREA' ||
             document.activeElement?.contentEditable === 'true';
    });
    
    expect(terminalInput).toBeTruthy();
    
    // Verify focus indicators are visible
    const focusStyle = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return null;
      
      const computed = window.getComputedStyle(el);
      return {
        outline: computed.outline,
        outlineColor: computed.outlineColor,
        boxShadow: computed.boxShadow
      };
    });
    
    // Should have visible focus indicator
    expect(
      focusStyle?.outline !== 'none' || 
      focusStyle?.boxShadow.includes('0 0')
    ).toBeTruthy();
    
    await page.screenshot({ 
      path: 'screenshots/010_1_keyboard_navigation.png' 
    });
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(20);
    expect(duration).toBeLessThanOrEqual(30);
  });

  test('010.2 - Screen reader compatibility', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Check ARIA landmarks
    const landmarks = await page.evaluate(() => {
      const roles = ['banner', 'navigation', 'main', 'complementary', 'contentinfo'];
      const found = {};
      
      roles.forEach(role => {
        const elements = document.querySelectorAll(`[role="${role}"]`);
        const tagElements = role === 'banner' ? document.querySelectorAll('header') :
                          role === 'navigation' ? document.querySelectorAll('nav') :
                          role === 'main' ? document.querySelectorAll('main') :
                          role === 'contentinfo' ? document.querySelectorAll('footer') : [];
        
        found[role] = elements.length + tagElements.length;
      });
      
      return found;
    });
    
    // Should have essential landmarks
    expect(landmarks.navigation).toBeGreaterThan(0);
    expect(landmarks.main).toBeGreaterThan(0);
    
    // Check heading hierarchy
    const headings = await page.evaluate(() => {
      const h1s = document.querySelectorAll('h1');
      const h2s = document.querySelectorAll('h2');
      const h3s = document.querySelectorAll('h3');
      
      return {
        h1Count: h1s.length,
        h2Count: h2s.length,
        h3Count: h3s.length,
        h1Text: Array.from(h1s).map(h => h.textContent),
        hierarchy: []
      };
    });
    
    // Should have exactly one h1
    expect(headings.h1Count).toBe(1);
    
    // Check form labels
    const forms = await page.evaluate(() => {
      const inputs = document.querySelectorAll('input, textarea, select');
      const results = [];
      
      inputs.forEach(input => {
        const label = input.labels?.[0]?.textContent || 
                     input.getAttribute('aria-label') ||
                     input.getAttribute('aria-labelledby');
        
        results.push({
          type: input.type || input.tagName,
          hasLabel: !!label,
          label: label
        });
      });
      
      return results;
    });
    
    // All form inputs should have labels
    forms.forEach(input => {
      expect(input.hasLabel).toBeTruthy();
    });
    
    // Check button accessibility
    const buttons = await page.evaluate(() => {
      const btns = document.querySelectorAll('button, [role="button"]');
      return Array.from(btns).map(btn => ({
        text: btn.textContent?.trim(),
        ariaLabel: btn.getAttribute('aria-label'),
        hasAccessibleName: !!(btn.textContent?.trim() || btn.getAttribute('aria-label'))
      }));
    });
    
    buttons.forEach(btn => {
      expect(btn.hasAccessibleName).toBeTruthy();
    });
    
    // Test live regions
    await page.evaluate(() => {
      // Create a live region
      const liveRegion = document.createElement('div');
      liveRegion.setAttribute('role', 'status');
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.id = 'test-live-region';
      document.body.appendChild(liveRegion);
    });
    
    // Update live region
    await page.evaluate(() => {
      const region = document.getElementById('test-live-region');
      if (region) {
        region.textContent = 'New message received';
      }
    });
    
    await page.waitForTimeout(500);
    
    // Check if announcement was tracked
    const announcements = await page.evaluate(() => window.a11yMonitor.announcements);
    const hasAnnouncement = announcements.some(a => a.text?.includes('New message'));
    expect(hasAnnouncement).toBeTruthy();
  });

  test('010.3 - WCAG AA compliance verification', async ({ page }) => {
    // Test each module for WCAG compliance
    const modules = [
      { name: 'chat', url: 'http://localhost:3000/chat' },
      { name: 'annotator', url: 'http://localhost:3001/annotator' },
      { name: 'terminal', url: 'http://localhost:3002/terminal' }
    ];
    
    for (const module of modules) {
      await page.goto(module.url);
      await page.waitForLoadState('networkidle');
      
      // Run axe accessibility tests
      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();
      
      // Should have no violations
      expect(accessibilityScanResults.violations).toHaveLength(0);
      
      // If violations exist, log them
      if (accessibilityScanResults.violations.length > 0) {
        console.log(`${module.name} violations:`, 
          accessibilityScanResults.violations.map(v => ({
            id: v.id,
            impact: v.impact,
            description: v.description,
            nodes: v.nodes.length
          }))
        );
      }
      
      // Manual contrast checks for custom components
      const contrastChecks = await page.evaluate(() => {
        const getContrastRatio = (color1: string, color2: string) => {
          // Simplified contrast calculation
          const getLuminance = (rgb: number[]) => {
            const [r, g, b] = rgb.map(val => {
              val = val / 255;
              return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
          };
          
          const parseColor = (color: string) => {
            const match = color.match(/\d+/g);
            return match ? match.slice(0, 3).map(Number) : [0, 0, 0];
          };
          
          const rgb1 = parseColor(color1);
          const rgb2 = parseColor(color2);
          
          const l1 = getLuminance(rgb1);
          const l2 = getLuminance(rgb2);
          
          return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
        };
        
        const elements = document.querySelectorAll('p, span, div, button, a');
        const issues = [];
        
        elements.forEach(el => {
          const style = window.getComputedStyle(el);
          const color = style.color;
          const bgColor = style.backgroundColor;
          
          if (color && bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
            const ratio = getContrastRatio(color, bgColor);
            
            if (ratio < 4.5) { // WCAG AA requires 4.5:1 for normal text
              issues.push({
                element: el.tagName,
                color,
                background: bgColor,
                ratio: ratio.toFixed(2)
              });
            }
          }
        });
        
        return issues;
      });
      
      // Should have no contrast issues
      expect(contrastChecks.length).toBe(0);
      
      await page.screenshot({ 
        path: `screenshots/010_3_wcag_${module.name}.png` 
      });
    }
  });

  test('010.4 - Focus management during transitions', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Set up focus tracking
    await page.evaluate(() => {
      window.focusHistory = [];
      document.addEventListener('focusin', (e) => {
        window.focusHistory.push({
          element: e.target.tagName,
          id: e.target.id,
          time: Date.now()
        });
      });
    });
    
    // Focus on chat input
    await page.focus('.chat-input, textarea');
    
    // Navigate to annotator
    await page.click('a[href*="annotator"]');
    await page.waitForURL('**/annotator');
    
    // Check where focus landed
    const focusAfterTransition = await page.evaluate(() => {
      return {
        activeElement: document.activeElement?.tagName,
        isBody: document.activeElement === document.body,
        hasTabIndex: document.activeElement?.getAttribute('tabindex')
      };
    });
    
    // Focus should not be on body after navigation
    expect(focusAfterTransition.isBody).toBeFalsy();
    
    // Focus should be on a meaningful element
    expect(['MAIN', 'H1', 'NAV', 'INPUT', 'BUTTON']).toContain(
      focusAfterTransition.activeElement
    );
    
    // Test focus trap in modal
    await page.evaluate(() => {
      // Create and show modal
      const modal = document.createElement('div');
      modal.innerHTML = `
        <div role="dialog" aria-modal="true" aria-label="Test Modal">
          <h2 id="modal-title">Modal Title</h2>
          <input type="text" placeholder="Input 1">
          <input type="text" placeholder="Input 2">
          <button>Close</button>
        </div>
      `;
      modal.id = 'test-modal';
      modal.style.cssText = 'position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 9999;';
      document.body.appendChild(modal);
      
      // Focus first input
      modal.querySelector('input')?.focus();
    });
    
    // Tab through modal elements
    for (let i = 0; i < 4; i++) {
      await page.keyboard.press('Tab');
      
      const focusedInModal = await page.evaluate(() => {
        const modal = document.getElementById('test-modal');
        return modal?.contains(document.activeElement);
      });
      
      // Focus should stay trapped in modal
      expect(focusedInModal).toBeTruthy();
    }
    
    // Clean up
    await page.evaluate(() => {
      document.getElementById('test-modal')?.remove();
    });
  });

  test('010.5 - Accessible animations (prefers-reduced-motion)', async ({ page }) => {
    // Test with reduced motion preference
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('http://localhost:3000/chat');
    
    // Check if animations are disabled/reduced
    const animationCheck = await page.evaluate(() => {
      const elements = document.querySelectorAll('*');
      const animations = [];
      
      elements.forEach(el => {
        const style = window.getComputedStyle(el);
        
        if (style.animationDuration !== '0s' || 
            style.transitionDuration !== '0s') {
          animations.push({
            element: el.tagName,
            animation: style.animationDuration,
            transition: style.transitionDuration
          });
        }
      });
      
      return animations;
    });
    
    // With reduced motion, animations should be minimal or instant
    animations.forEach(anim => {
      const duration = parseFloat(anim.transition || anim.animation);
      expect(duration).toBeLessThanOrEqual(0.1); // Max 100ms for reduced motion
    });
    
    // Test without reduced motion
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    await page.reload();
    
    const normalAnimations = await page.evaluate(() => {
      const button = document.querySelector('button');
      if (button) {
        const style = window.getComputedStyle(button);
        return {
          transition: style.transition,
          hasAnimation: style.transition !== 'none'
        };
      }
      return null;
    });
    
    expect(normalAnimations?.hasAnimation).toBeTruthy();
  });

  test('010.6 - Accessible error messages', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Submit form with invalid data
    const input = await page.$('.chat-input, input[type="text"]');
    if (input) {
      await input.click();
      await input.fill(''); // Empty message
      await page.keyboard.press('Enter');
    }
    
    // Wait for error message
    await page.waitForSelector('.error, [role="alert"]', { timeout: 5000 });
    
    // Check error accessibility
    const errorAccessibility = await page.evaluate(() => {
      const error = document.querySelector('.error, [role="alert"]');
      if (!error) return null;
      
      return {
        role: error.getAttribute('role'),
        ariaLive: error.getAttribute('aria-live'),
        ariaInvalid: document.querySelector('[aria-invalid="true"]') !== null,
        describedBy: document.querySelector('[aria-describedby]') !== null,
        errorText: error.textContent,
        isVisible: window.getComputedStyle(error).display !== 'none'
      };
    });
    
    expect(errorAccessibility?.role).toBe('alert');
    expect(errorAccessibility?.isVisible).toBeTruthy();
    expect(errorAccessibility?.errorText).toBeTruthy();
    
    // Error should be announced to screen readers
    const announcements = await page.evaluate(() => window.a11yMonitor.announcements);
    const errorAnnounced = announcements.some(a => 
      a.role === 'alert' || a.text?.includes('error')
    );
    expect(errorAnnounced).toBeTruthy();
  });

  test('010.H - HONEYPOT: Inaccessible UI elements', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Create intentionally inaccessible elements
    await page.evaluate(() => {
      // Button with no text or label
      const badButton = document.createElement('button');
      badButton.innerHTML = '<i class="icon-send"></i>'; // Icon only, no text
      document.body.appendChild(badButton);
      
      // Image with no alt text
      const badImage = document.createElement('img');
      badImage.src = 'test.jpg';
      document.body.appendChild(badImage);
      
      // Form input with no label
      const badInput = document.createElement('input');
      badInput.type = 'text';
      document.body.appendChild(badInput);
    });
    
    // Run accessibility check
    const violations = await page.evaluate(() => {
      const issues = [];
      
      // Check buttons
      document.querySelectorAll('button').forEach(btn => {
        if (!btn.textContent?.trim() && !btn.getAttribute('aria-label')) {
          issues.push('Button without accessible name');
        }
      });
      
      // Check images
      document.querySelectorAll('img').forEach(img => {
        if (!img.getAttribute('alt')) {
          issues.push('Image without alt text');
        }
      });
      
      // Check inputs
      document.querySelectorAll('input').forEach(input => {
        if (!input.labels?.length && !input.getAttribute('aria-label')) {
          issues.push('Input without label');
        }
      });
      
      return issues;
    });
    
    // Should detect accessibility violations
    expect(violations.length).toBeGreaterThan(0);
    
    // This test should fail due to violations
    if (violations.length === 0) {
      throw new Error('Failed to detect intentionally inaccessible elements');
    }
  });
});