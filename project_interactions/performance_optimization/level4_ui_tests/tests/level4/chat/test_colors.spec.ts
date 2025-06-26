import { test, expect } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #002.1: Validates chat color palette compliance
 * Tests all color usage against 2025 Style Guide specifications
 */

test.describe('Chat Module - Color Palette Validation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
  });

  test('002.1 - Primary colors match style guide', async ({ page }) => {
    const startTime = Date.now();
    
    // Check primary gradient on main elements
    const primaryElements = await page.$$('[data-testid*="primary"], .btn-primary, .primary-gradient');
    
    for (const element of primaryElements) {
      const background = await element.evaluate(el => 
        window.getComputedStyle(el).background || window.getComputedStyle(el).backgroundColor
      );
      
      // Verify gradient contains our primary colors
      if (background.includes('gradient')) {
        expect(background).toContain(STYLE_GUIDE.colors.primary_start);
        expect(background).toContain(STYLE_GUIDE.colors.primary_end);
      } else {
        // For solid colors, check against primary start
        const rgb = background.match(/\d+/g);
        if (rgb) {
          const hex = `#${parseInt(rgb[0]).toString(16).padStart(2, '0')}${parseInt(rgb[1]).toString(16).padStart(2, '0')}${parseInt(rgb[2]).toString(16).padStart(2, '0')}`;
          expect(hex.toUpperCase()).toBe(STYLE_GUIDE.colors.primary_start);
        }
      }
    }
    
    // Check secondary colors
    const secondaryElements = await page.$$('.text-secondary, [data-testid*="secondary"]');
    for (const element of secondaryElements) {
      const color = await element.evaluate(el => window.getComputedStyle(el).color);
      expect(color).toContain(STYLE_GUIDE.colors.secondary);
    }
    
    // Check background colors
    const background = await page.evaluate(() => 
      window.getComputedStyle(document.body).backgroundColor
    );
    expect(background).toContain(STYLE_GUIDE.colors.background);
    
    // Check accent colors on interactive elements
    const accentElements = await page.$$('.success, [data-testid*="success"], .accent');
    for (const element of accentElements) {
      const color = await element.evaluate(el => 
        window.getComputedStyle(el).color || window.getComputedStyle(el).backgroundColor
      );
      expect(color).toContain(STYLE_GUIDE.colors.accent);
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(3);
    expect(duration).toBeLessThanOrEqual(5);
    
    // Take screenshot for visual validation
    await page.screenshot({ 
      path: 'screenshots/002_1_chat_colors.png',
      fullPage: true 
    });
  });

  test('002.1 - Dark mode color compliance', async ({ page }) => {
    // Toggle dark mode
    await page.click('[data-testid="theme-toggle"]');
    await page.waitForTimeout(500); // Wait for transition
    
    // Verify dark mode colors are still within style guide
    const darkBackground = await page.evaluate(() => 
      window.getComputedStyle(document.body).backgroundColor
    );
    
    // Dark mode should use darker variants but maintain brand colors
    expect(darkBackground).not.toBe(STYLE_GUIDE.colors.background);
    
    // Primary colors should remain consistent
    const primaryButton = await page.$('.btn-primary');
    if (primaryButton) {
      const buttonBg = await primaryButton.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      expect(buttonBg).toContain(STYLE_GUIDE.colors.primary_start);
    }
  });

  test('002.1 - Color contrast accessibility', async ({ page }) => {
    // Check text contrast ratios
    const textElements = await page.$$('p, h1, h2, h3, h4, h5, h6, span, a');
    
    for (const element of textElements.slice(0, 10)) { // Sample first 10
      const color = await element.evaluate(el => window.getComputedStyle(el).color);
      const bgColor = await element.evaluate(el => {
        let bg = window.getComputedStyle(el).backgroundColor;
        let parent = el.parentElement;
        while (bg === 'rgba(0, 0, 0, 0)' && parent) {
          bg = window.getComputedStyle(parent).backgroundColor;
          parent = parent.parentElement;
        }
        return bg;
      });
      
      // Calculate contrast ratio (simplified)
      const getLuminance = (rgb: number[]) => {
        const [r, g, b] = rgb.map(val => {
          val = val / 255;
          return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
      };
      
      const colorRgb = color.match(/\d+/g)?.map(Number) || [0, 0, 0];
      const bgRgb = bgColor.match(/\d+/g)?.map(Number) || [255, 255, 255];
      
      const l1 = getLuminance(colorRgb);
      const l2 = getLuminance(bgRgb);
      const contrast = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      
      // WCAG AA requires 4.5:1 for normal text
      expect(contrast).toBeGreaterThanOrEqual(4.5);
    }
  });
});