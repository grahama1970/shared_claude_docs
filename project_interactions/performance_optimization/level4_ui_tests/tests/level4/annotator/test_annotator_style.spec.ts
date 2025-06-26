import { test, expect } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #003: Annotator Module Style Guide Compliance
 * Special focus on annotation overlays, toolbar styling, and document readability
 */

test.describe('Annotator Module - Style Guide Compliance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3001/annotator');
    await page.waitForLoadState('networkidle');
    
    // Load a sample PDF for testing
    await page.evaluate(() => {
      // Simulate PDF loaded state
      document.body.classList.add('pdf-loaded');
    });
  });

  test('003.1 - Annotation overlay styling', async ({ page }) => {
    const startTime = Date.now();
    
    // Create test annotation
    await page.evaluate(() => {
      const viewer = document.querySelector('.pdf-viewer, .document-viewer');
      if (viewer) {
        const annotation = document.createElement('div');
        annotation.className = 'annotation-overlay';
        annotation.style.cssText = `
          position: absolute;
          top: 100px;
          left: 100px;
          width: 200px;
          height: 50px;
          background: rgba(79, 70, 229, 0.1);
          border: 2px solid #4F46E5;
          border-radius: 4px;
        `;
        viewer.appendChild(annotation);
      }
    });
    
    // Check annotation overlays
    const annotations = await page.$$('.annotation-overlay, .annotation');
    
    for (const annotation of annotations) {
      // Check opacity for subtle overlay
      const opacity = await annotation.evaluate(el => {
        const bg = window.getComputedStyle(el).backgroundColor;
        const match = bg.match(/rgba?\([\d\s,]+?([\d.]+)?\)/);
        return match && match[1] ? parseFloat(match[1]) : 1;
      });
      
      expect(opacity).toBeLessThanOrEqual(0.3); // Subtle overlay
      
      // Check border styling
      const borderColor = await annotation.evaluate(el => 
        window.getComputedStyle(el).borderColor
      );
      
      if (borderColor && borderColor !== 'none') {
        expect(borderColor).toContain(STYLE_GUIDE.colors.primary_start);
      }
      
      // Check shadow for depth
      const shadow = await annotation.evaluate(el => 
        window.getComputedStyle(el).boxShadow
      );
      
      if (shadow && shadow !== 'none') {
        expect(shadow).toMatch(/rgba?\(0,\s*0,\s*0,\s*0\.\d+\)/); // Subtle shadow
      }
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(3);
    expect(duration).toBeLessThanOrEqual(8);
    
    await page.screenshot({ 
      path: 'screenshots/003_1_annotator_overlays.png',
      fullPage: true 
    });
  });

  test('003.2 - Toolbar and control panel layouts', async ({ page }) => {
    // Check toolbar styling
    const toolbar = await page.$('.toolbar, .annotation-toolbar, [role="toolbar"]');
    expect(toolbar).toBeTruthy();
    
    if (toolbar) {
      // Check toolbar background
      const bg = await toolbar.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      
      // Should use light background or white
      expect(bg).toMatch(/rgb\(2[4-5]\d|white/);
      
      // Check toolbar spacing
      const padding = await toolbar.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return {
          top: parseInt(computed.paddingTop),
          right: parseInt(computed.paddingRight),
          bottom: parseInt(computed.paddingBottom),
          left: parseInt(computed.paddingLeft)
        };
      });
      
      Object.values(padding).forEach(value => {
        expect(value % STYLE_GUIDE.spacing.base).toBe(0);
      });
      
      // Check toolbar buttons
      const toolButtons = await toolbar.$$('button, .tool-button');
      
      for (const button of toolButtons.slice(0, 5)) {
        // Check button sizing
        const box = await button.boundingBox();
        if (box) {
          expect(box.width).toBeGreaterThanOrEqual(32);
          expect(box.height).toBeGreaterThanOrEqual(32);
          
          // Square buttons for tools
          expect(Math.abs(box.width - box.height)).toBeLessThanOrEqual(4);
        }
        
        // Check hover states
        await button.hover();
        await page.waitForTimeout(150);
        
        const hoverBg = await button.evaluate(el => 
          window.getComputedStyle(el).backgroundColor
        );
        
        // Should have hover effect
        expect(hoverBg).not.toBe('transparent');
      }
    }
    
    // Check control panel
    const controlPanel = await page.$('.control-panel, .sidebar, .annotation-panel');
    if (controlPanel) {
      // Check panel width
      const width = await controlPanel.evaluate(el => el.offsetWidth);
      expect(width % STYLE_GUIDE.spacing.base).toBe(0); // Multiple of 8px
      
      // Check panel separation
      const borderOrShadow = await controlPanel.evaluate(el => ({
        border: window.getComputedStyle(el).borderLeft || window.getComputedStyle(el).borderRight,
        shadow: window.getComputedStyle(el).boxShadow
      }));
      
      // Should have visual separation
      expect(borderOrShadow.border !== 'none' || borderOrShadow.shadow !== 'none').toBeTruthy();
    }
  });

  test('003.3 - Annotation animation smoothness', async ({ page }) => {
    // Inject FPS monitor
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
    
    // Create animated annotation
    await page.evaluate(() => {
      const annotation = document.createElement('div');
      annotation.className = 'annotation-animated';
      annotation.style.cssText = `
        position: absolute;
        top: 200px;
        left: 200px;
        width: 100px;
        height: 100px;
        background: rgba(99, 102, 241, 0.2);
        border: 2px solid #6366F1;
        border-radius: 8px;
        transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
      `;
      document.body.appendChild(annotation);
      
      // Animate it
      setTimeout(() => {
        annotation.style.transform = 'scale(1.1)';
        annotation.style.opacity = '0.8';
      }, 100);
    });
    
    await page.waitForTimeout(500);
    
    // Check FPS during animation
    const fps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(fps).toBeGreaterThanOrEqual(55);
    
    // Test selection animation
    const textElement = await page.$('.document-content, .pdf-text-layer');
    if (textElement) {
      // Simulate text selection
      await page.mouse.move(100, 100);
      await page.mouse.down();
      await page.mouse.move(300, 150);
      await page.mouse.up();
      
      await page.waitForTimeout(300);
      
      // Check if selection highlight appears smoothly
      const selection = await page.$('.text-selection, .selection-overlay');
      if (selection) {
        const transition = await selection.evaluate(el => 
          window.getComputedStyle(el).transition
        );
        expect(transition).toContain('250ms');
      }
    }
  });

  test('003.4 - Document viewer readability', async ({ page }) => {
    // Check document viewer styling
    const viewer = await page.$('.pdf-viewer, .document-viewer, .viewer-container');
    expect(viewer).toBeTruthy();
    
    if (viewer) {
      // Check background for readability
      const bg = await viewer.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      
      // Should have neutral background
      expect(bg).toMatch(/rgb\(24[0-9]|25[0-5]|#[Ff]/); // Light gray or white
      
      // Check zoom controls
      const zoomControls = await page.$$('.zoom-control, [aria-label*="zoom"]');
      expect(zoomControls.length).toBeGreaterThan(0);
      
      // Test zoom functionality maintains readability
      const zoomIn = await page.$('[aria-label*="zoom in"], .zoom-in');
      if (zoomIn) {
        await zoomIn.click();
        await page.waitForTimeout(300);
        
        // Check text is still crisp (no blur)
        const textLayer = await page.$('.text-layer, .document-text');
        if (textLayer) {
          const filter = await textLayer.evaluate(el => 
            window.getComputedStyle(el).filter
          );
          expect(filter).toBe('none');
        }
      }
    }
    
    // Check page navigation
    const pageNav = await page.$('.page-navigation, .page-controls');
    if (pageNav) {
      const navButtons = await pageNav.$$('button');
      
      for (const button of navButtons) {
        // Check button styling matches style guide
        const styles = await button.evaluate(el => ({
          borderRadius: window.getComputedStyle(el).borderRadius,
          padding: window.getComputedStyle(el).padding
        }));
        
        expect(parseInt(styles.borderRadius)).toBe(STYLE_GUIDE.border_radius.base);
      }
    }
  });

  test('003.5 - Color contrast in annotation mode', async ({ page }) => {
    // Switch to dark document background (common for PDFs)
    await page.evaluate(() => {
      const viewer = document.querySelector('.pdf-viewer, .document-viewer');
      if (viewer) {
        viewer.style.backgroundColor = '#1a1a1a';
      }
    });
    
    // Check annotation visibility on dark background
    const annotation = await page.evaluateHandle(() => {
      const ann = document.createElement('div');
      ann.className = 'annotation-highlight';
      ann.style.cssText = `
        position: absolute;
        top: 150px;
        left: 150px;
        width: 250px;
        height: 40px;
        background: rgba(16, 185, 129, 0.3);
        border: 1px solid #10B981;
      `;
      document.body.appendChild(ann);
      return ann;
    });
    
    // Verify annotation colors have sufficient contrast
    const annotationColors = await annotation.evaluate(el => ({
      background: window.getComputedStyle(el).backgroundColor,
      border: window.getComputedStyle(el).borderColor
    }));
    
    // Green accent should be visible on dark background
    expect(annotationColors.border).toContain(STYLE_GUIDE.colors.accent);
    
    await page.screenshot({ 
      path: 'screenshots/003_5_annotator_contrast.png' 
    });
  });

  test('003.H - HONEYPOT: Invalid annotation colors', async ({ page }) => {
    // This test checks for non-compliant annotation colors
    const invalidAnnotation = await page.evaluateHandle(() => {
      const ann = document.createElement('div');
      ann.className = 'annotation-invalid';
      ann.style.cssText = `
        background: #FF0000;
        border: 3px solid #00FF00;
      `;
      document.body.appendChild(ann);
      return ann;
    });
    
    const colors = await invalidAnnotation.evaluate(el => ({
      background: window.getComputedStyle(el).backgroundColor,
      border: window.getComputedStyle(el).borderColor
    }));
    
    // Should fail - these colors are not in the style guide
    const validColors = Object.values(STYLE_GUIDE.colors).filter(c => typeof c === 'string');
    
    if (!validColors.some(c => colors.background.includes(c))) {
      throw new Error('Invalid annotation colors detected - not following style guide');
    }
  });
});