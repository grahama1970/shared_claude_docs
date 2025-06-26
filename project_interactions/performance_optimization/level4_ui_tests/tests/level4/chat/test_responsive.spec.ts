import { test, expect, devices } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #002.4: Validates responsive design
 * Tests all breakpoints and ensures proper rendering across devices
 */

test.describe('Chat Module - Responsive Design', () => {
  const breakpoints = [
    { name: 'mobile-sm', width: 375, height: 667 },
    { name: 'mobile-lg', width: 414, height: 896 },
    { name: 'tablet', width: 768, height: 1024 },
    { name: 'desktop', width: 1280, height: 800 },
    { name: 'desktop-xl', width: 1920, height: 1080 }
  ];

  test('002.4 - Layout adapts correctly at all breakpoints', async ({ page }) => {
    const startTime = Date.now();
    
    for (const breakpoint of breakpoints) {
      await page.setViewportSize({ width: breakpoint.width, height: breakpoint.height });
      await page.goto('http://localhost:3000/chat');
      await page.waitForLoadState('networkidle');
      
      // Check navigation layout
      const nav = await page.$('nav, .navigation, header');
      if (nav) {
        const navDisplay = await nav.evaluate(el => 
          window.getComputedStyle(el).display
        );
        
        if (breakpoint.width < STYLE_GUIDE.breakpoints.md) {
          // Mobile: Should have hamburger menu
          const hamburger = await page.$('.hamburger, .menu-toggle, [aria-label*="menu"]');
          expect(hamburger).toBeTruthy();
        } else {
          // Desktop: Should have horizontal nav
          const navItems = await nav.$$('a, .nav-item');
          expect(navItems.length).toBeGreaterThan(0);
        }
      }
      
      // Check container max-width
      const container = await page.$('.container, main > div');
      if (container) {
        const width = await container.evaluate(el => el.offsetWidth);
        
        if (breakpoint.width >= STYLE_GUIDE.breakpoints.xl) {
          expect(width).toBeLessThanOrEqual(1200); // Max container width
        }
      }
      
      // Check chat layout
      const chatContainer = await page.$('.chat-container, [data-testid="chat-container"]');
      if (chatContainer) {
        const layout = await chatContainer.evaluate(el => ({
          display: window.getComputedStyle(el).display,
          flexDirection: window.getComputedStyle(el).flexDirection,
          gridTemplateColumns: window.getComputedStyle(el).gridTemplateColumns
        }));
        
        // Mobile: Single column
        if (breakpoint.width < STYLE_GUIDE.breakpoints.md) {
          if (layout.display === 'flex') {
            expect(layout.flexDirection).toBe('column');
          }
        }
      }
      
      await page.screenshot({ 
        path: `screenshots/002_4_responsive_${breakpoint.name}.png`,
        fullPage: false 
      });
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(5);
    expect(duration).toBeLessThanOrEqual(8);
  });

  test('002.4 - Touch targets meet mobile requirements', async ({ page }) => {
    // Use mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('http://localhost:3000/chat');
    
    // Find all interactive elements
    const interactiveElements = await page.$$('button, a, input, textarea, [role="button"], [onclick]');
    
    for (const element of interactiveElements.slice(0, 10)) { // Check first 10
      const box = await element.boundingBox();
      if (box) {
        // Minimum touch target size is 44x44px (iOS) or 48x48px (Android)
        expect(box.width).toBeGreaterThanOrEqual(44);
        expect(box.height).toBeGreaterThanOrEqual(44);
        
        // Check padding around small elements
        if (box.width < 44 || box.height < 44) {
          const padding = await element.evaluate(el => {
            const computed = window.getComputedStyle(el);
            return {
              top: parseInt(computed.paddingTop),
              right: parseInt(computed.paddingRight),
              bottom: parseInt(computed.paddingBottom),
              left: parseInt(computed.paddingLeft)
            };
          });
          
          // Total size including padding should meet requirements
          const totalWidth = box.width + padding.left + padding.right;
          const totalHeight = box.height + padding.top + padding.bottom;
          expect(totalWidth).toBeGreaterThanOrEqual(44);
          expect(totalHeight).toBeGreaterThanOrEqual(44);
        }
      }
    }
  });

  test('002.4 - Text remains readable at all sizes', async ({ page }) => {
    for (const breakpoint of breakpoints) {
      await page.setViewportSize({ width: breakpoint.width, height: breakpoint.height });
      await page.goto('http://localhost:3000/chat');
      
      // Check font sizes
      const textElements = await page.$$('p, span, div:not(:empty)');
      
      for (const element of textElements.slice(0, 5)) {
        const fontSize = await element.evaluate(el => 
          parseFloat(window.getComputedStyle(el).fontSize)
        );
        
        // Minimum readable font size
        if (breakpoint.width < STYLE_GUIDE.breakpoints.md) {
          expect(fontSize).toBeGreaterThanOrEqual(14); // 14px minimum on mobile
        } else {
          expect(fontSize).toBeGreaterThanOrEqual(12); // 12px minimum on desktop
        }
      }
      
      // Check line length (measure)
      const contentContainers = await page.$$('p, .content');
      for (const container of contentContainers.slice(0, 3)) {
        const width = await container.evaluate(el => el.offsetWidth);
        
        // Optimal line length is 45-75 characters
        // Approximate: 600-900px at 16px font size
        if (breakpoint.width >= STYLE_GUIDE.breakpoints.lg) {
          expect(width).toBeLessThanOrEqual(900);
        }
      }
    }
  });

  test('002.4 - Images and media scale properly', async ({ page }) => {
    for (const breakpoint of breakpoints) {
      await page.setViewportSize({ width: breakpoint.width, height: breakpoint.height });
      await page.goto('http://localhost:3000/chat');
      
      // Check images
      const images = await page.$$('img, picture, video');
      
      for (const img of images) {
        const box = await img.boundingBox();
        if (box) {
          // Images shouldn't exceed viewport width
          expect(box.width).toBeLessThanOrEqual(breakpoint.width);
          
          // Check responsive image attributes
          const srcset = await img.getAttribute('srcset');
          const sizes = await img.getAttribute('sizes');
          
          if (breakpoint.width < STYLE_GUIDE.breakpoints.md) {
            // Mobile images should have responsive attributes
            expect(srcset || sizes).toBeTruthy();
          }
        }
        
        // Check aspect ratio is maintained
        const aspectRatio = await img.evaluate(el => {
          const computed = window.getComputedStyle(el);
          return computed.objectFit || computed.aspectRatio;
        });
        
        if (aspectRatio) {
          expect(['cover', 'contain', 'scale-down']).toContain(aspectRatio);
        }
      }
    }
  });

  test('002.4 - Orientation changes handled gracefully', async ({ context }) => {
    // Create new page with mobile device
    const iPhone = devices['iPhone 12'];
    const page = await context.newPage({
      ...iPhone,
      viewport: { width: 390, height: 844 } // Portrait
    });
    
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
    
    // Take portrait screenshot
    await page.screenshot({ 
      path: 'screenshots/002_4_orientation_portrait.png' 
    });
    
    // Rotate to landscape
    await page.setViewportSize({ width: 844, height: 390 });
    await page.waitForTimeout(500); // Wait for reflow
    
    // Check layout adjusted
    const container = await page.$('.chat-container, main');
    if (container) {
      const height = await container.evaluate(el => el.offsetHeight);
      expect(height).toBeLessThanOrEqual(390); // Should fit in landscape
    }
    
    // Take landscape screenshot
    await page.screenshot({ 
      path: 'screenshots/002_4_orientation_landscape.png' 
    });
    
    await page.close();
  });

  test('002.H - HONEYPOT: Wrong responsive breakpoints', async ({ page }) => {
    // This test checks for incorrect breakpoint implementations
    await page.setViewportSize({ width: 767, height: 1024 }); // Just below tablet breakpoint
    await page.goto('http://localhost:3000/chat');
    
    // Should show mobile layout at 767px
    const hamburger = await page.$('.hamburger, .menu-toggle');
    
    // Fail if desktop nav is shown at mobile width
    const desktopNav = await page.$('.desktop-nav:visible');
    if (desktopNav) {
      throw new Error('Desktop navigation shown at mobile breakpoint - responsive design failure');
    }
    
    expect(hamburger).toBeTruthy();
  });
});