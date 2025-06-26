import { test, expect } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #002.2: Validates typography and spacing
 * Ensures font weights, sizes, and 8px grid compliance
 */

test.describe('Chat Module - Typography & Spacing Validation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
  });

  test('002.2 - Typography hierarchy follows style guide', async ({ page }) => {
    const startTime = Date.now();
    
    // Check headings
    const headingSelectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
    
    for (const selector of headingSelectors) {
      const elements = await page.$$(selector);
      
      for (const element of elements) {
        // Check font family
        const fontFamily = await element.evaluate(el => 
          window.getComputedStyle(el).fontFamily
        );
        expect(fontFamily.toLowerCase()).toContain('inter');
        
        // Check font weight
        const fontWeight = await element.evaluate(el => 
          window.getComputedStyle(el).fontWeight
        );
        const weight = parseInt(fontWeight);
        expect([600, 700]).toContain(weight); // Semibold or bold for headings
        
        // Check line height
        const lineHeight = await element.evaluate(el => {
          const computed = window.getComputedStyle(el);
          const lh = parseFloat(computed.lineHeight);
          const fs = parseFloat(computed.fontSize);
          return lh / fs;
        });
        expect(lineHeight).toBeGreaterThanOrEqual(STYLE_GUIDE.typography.line_heights.tight);
        expect(lineHeight).toBeLessThanOrEqual(STYLE_GUIDE.typography.line_heights.relaxed);
      }
    }
    
    // Check body text
    const paragraphs = await page.$$('p, .body-text');
    for (const p of paragraphs.slice(0, 5)) { // Sample first 5
      const fontSize = await p.evaluate(el => 
        window.getComputedStyle(el).fontSize
      );
      expect(['14px', '16px', '18px']).toContain(fontSize); // sm, base, lg
      
      const fontWeight = await p.evaluate(el => 
        window.getComputedStyle(el).fontWeight
      );
      expect(['400', '500']).toContain(fontWeight); // Regular or medium
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(3);
    expect(duration).toBeLessThanOrEqual(5);
    
    await page.screenshot({ 
      path: 'screenshots/002_2_chat_typography.png',
      fullPage: true 
    });
  });

  test('002.2 - Spacing follows 8px grid system', async ({ page }) => {
    // Check container padding/margins
    const containers = await page.$$('[class*="container"], [class*="card"], [class*="section"]');
    
    for (const container of containers.slice(0, 10)) { // Sample first 10
      // Check padding
      const padding = await container.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          top: parseInt(computed.paddingTop),
          right: parseInt(computed.paddingRight),
          bottom: parseInt(computed.paddingBottom),
          left: parseInt(computed.paddingLeft)
        };
      });
      
      Object.values(padding).forEach(value => {
        if (value > 0) {
          expect(value % STYLE_GUIDE.spacing.base).toBe(0);
          expect(STYLE_GUIDE.spacing.scale).toContain(value);
        }
      });
      
      // Check margins
      const margin = await container.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          top: parseInt(computed.marginTop),
          right: parseInt(computed.marginRight),
          bottom: parseInt(computed.marginBottom),
          left: parseInt(computed.marginLeft)
        };
      });
      
      Object.values(margin).forEach(value => {
        if (value > 0) {
          expect(value % STYLE_GUIDE.spacing.base).toBe(0);
        }
      });
    }
    
    // Check gaps in flex/grid layouts
    const flexContainers = await page.$$('[style*="display: flex"], [style*="display: grid"]');
    for (const flex of flexContainers.slice(0, 5)) {
      const gap = await flex.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return parseInt(computed.gap || '0');
      });
      
      if (gap > 0) {
        expect(gap % STYLE_GUIDE.spacing.base).toBe(0);
      }
    }
  });

  test('002.2 - Letter spacing and text rendering', async ({ page }) => {
    // Check heading letter spacing
    const headings = await page.$$('h1, h2, h3');
    
    for (const heading of headings) {
      const letterSpacing = await heading.evaluate(el => 
        window.getComputedStyle(el).letterSpacing
      );
      
      if (letterSpacing !== 'normal') {
        const value = parseFloat(letterSpacing);
        expect(value).toBeGreaterThan(0); // Should have positive letter spacing
      }
    }
    
    // Check text rendering optimization
    const textElements = await page.$$('p, span, h1, h2, h3, h4, h5, h6');
    
    for (const element of textElements.slice(0, 5)) {
      const rendering = await element.evaluate(el => ({
        smoothing: window.getComputedStyle(el).webkitFontSmoothing,
        ligatures: window.getComputedStyle(el).fontVariantLigatures
      }));
      
      // Should use antialiased text rendering
      expect(rendering.smoothing).toBe('antialiased');
    }
  });

  test('002.2 - Responsive typography scaling', async ({ page }) => {
    // Test different viewport sizes
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1440, height: 900, name: 'desktop' }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(300); // Wait for responsive adjustments
      
      const h1 = await page.$('h1');
      if (h1) {
        const fontSize = await h1.evaluate(el => 
          parseFloat(window.getComputedStyle(el).fontSize)
        );
        
        // Font sizes should scale appropriately
        if (viewport.name === 'mobile') {
          expect(fontSize).toBeLessThanOrEqual(36); // Max 2.25rem on mobile
        } else if (viewport.name === 'desktop') {
          expect(fontSize).toBeGreaterThanOrEqual(36); // Min 2.25rem on desktop
        }
      }
      
      await page.screenshot({ 
        path: `screenshots/002_2_typography_${viewport.name}.png`,
        fullPage: false 
      });
    }
  });
});