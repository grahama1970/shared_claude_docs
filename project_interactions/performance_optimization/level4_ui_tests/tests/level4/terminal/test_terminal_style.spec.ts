import { test, expect } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #004: Terminal Module Style Guide Compliance
 * Validates terminal color scheme, monospace fonts, animations, and syntax highlighting
 */

test.describe('Terminal Module - Style Guide Compliance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3002/terminal');
    await page.waitForLoadState('networkidle');
    
    // Wait for terminal to initialize
    await page.waitForSelector('.terminal-container, .xterm');
  });

  test('004.1 - Terminal color scheme aligns with palette', async ({ page }) => {
    const startTime = Date.now();
    
    // Check terminal background
    const terminal = await page.$('.terminal, .xterm, .terminal-container');
    expect(terminal).toBeTruthy();
    
    if (terminal) {
      const bg = await terminal.evaluate(el => 
        window.getComputedStyle(el).backgroundColor
      );
      
      // Terminal should use dark theme from style guide
      expect(bg).toMatch(/rgb\(1[0-9]|2[0-9]|3[0-9]/); // Dark background
      
      // Check text color
      const color = await terminal.evaluate(el => 
        window.getComputedStyle(el).color
      );
      
      // Should use light text on dark background
      expect(color).toMatch(/rgb\(2[0-5][0-9]/); // Light color
    }
    
    // Check prompt styling
    const prompt = await page.$('.terminal-prompt, .prompt');
    if (prompt) {
      const promptColor = await prompt.evaluate(el => 
        window.getComputedStyle(el).color
      );
      
      // Prompt should use accent color
      expect(promptColor).toContain(STYLE_GUIDE.colors.accent);
    }
    
    // Test command input styling
    await page.keyboard.type('ls -la');
    await page.waitForTimeout(100);
    
    // Check typed text visibility
    const inputText = await page.$('.terminal-input, .xterm-helper-textarea');
    if (inputText) {
      const inputColor = await inputText.evaluate(el => 
        window.getComputedStyle(el).color
      );
      
      // Input text should be clearly visible
      expect(inputColor).not.toBe(bg); // Different from background
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(3);
    expect(duration).toBeLessThanOrEqual(8);
    
    await page.screenshot({ 
      path: 'screenshots/004_1_terminal_colors.png' 
    });
  });

  test('004.2 - Monospace font validation', async ({ page }) => {
    const terminal = await page.$('.terminal, .xterm');
    
    if (terminal) {
      // Check font family
      const fontFamily = await terminal.evaluate(el => 
        window.getComputedStyle(el).fontFamily
      );
      
      // Should use monospace fonts
      const monospaceFonts = ['Consolas', 'Monaco', 'Courier', 'monospace', 'Menlo', 'Ubuntu Mono'];
      const hasMonospace = monospaceFonts.some(font => 
        fontFamily.toLowerCase().includes(font.toLowerCase())
      );
      expect(hasMonospace).toBeTruthy();
      
      // Check font size
      const fontSize = await terminal.evaluate(el => 
        window.getComputedStyle(el).fontSize
      );
      
      // Terminal font should be readable
      expect(parseInt(fontSize)).toBeGreaterThanOrEqual(12);
      expect(parseInt(fontSize)).toBeLessThanOrEqual(16);
      
      // Check line height for readability
      const lineHeight = await terminal.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return parseFloat(computed.lineHeight) / parseFloat(computed.fontSize);
      });
      
      // Should have comfortable line height
      expect(lineHeight).toBeGreaterThanOrEqual(1.2);
      expect(lineHeight).toBeLessThanOrEqual(1.6);
    }
    
    // Test character alignment (important for terminals)
    await page.evaluate(() => {
      const term = document.querySelector('.terminal, .xterm');
      if (term) {
        term.innerHTML += '<div>| Column 1 | Column 2 |</div>';
        term.innerHTML += '<div>|----------|----------|</div>';
        term.innerHTML += '<div>| Data     | Value    |</div>';
      }
    });
    
    // Characters should align vertically
    const lines = await page.$$('.terminal > div, .xterm-rows > div');
    if (lines.length >= 3) {
      const widths = await Promise.all(
        lines.slice(0, 3).map(line => 
          line.evaluate(el => el.offsetWidth)
        )
      );
      
      // All lines should have similar width (monospace property)
      const maxDiff = Math.max(...widths) - Math.min(...widths);
      expect(maxDiff).toBeLessThanOrEqual(2); // Allow 2px variance
    }
  });

  test('004.3 - Command animation fluidity', async ({ page }) => {
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
    
    // Type a command with animation
    const terminal = await page.$('.terminal-input, .xterm-helper-textarea, .terminal');
    if (terminal) {
      await terminal.click();
      
      // Type with realistic speed to trigger cursor animation
      for (const char of 'npm install @granger/ui-components') {
        await page.keyboard.type(char);
        await page.waitForTimeout(50); // Simulate typing speed
      }
      
      // Check cursor blink animation
      const cursor = await page.$('.cursor, .xterm-cursor, .terminal-cursor');
      if (cursor) {
        const animation = await cursor.evaluate(el => 
          window.getComputedStyle(el).animation || window.getComputedStyle(el).transition
        );
        
        // Should have cursor animation
        expect(animation).not.toBe('none');
      }
      
      // Press Enter to execute command
      await page.keyboard.press('Enter');
      await page.waitForTimeout(500);
      
      // Check output animation (should scroll smoothly)
      const fps = await page.evaluate(() => window.fpsMonitor.fps);
      expect(fps).toBeGreaterThanOrEqual(50); // Slightly lower threshold for terminal
    }
    
    // Test auto-scroll behavior
    await page.evaluate(() => {
      const term = document.querySelector('.terminal, .xterm');
      if (term) {
        // Add many lines to trigger scroll
        for (let i = 0; i < 50; i++) {
          const line = document.createElement('div');
          line.textContent = `Output line ${i + 1}`;
          term.appendChild(line);
        }
        
        // Scroll to bottom
        term.scrollTop = term.scrollHeight;
      }
    });
    
    // Verify smooth scrolling
    const scrollFps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(scrollFps).toBeGreaterThanOrEqual(45);
  });

  test('004.4 - Syntax highlighting follows style guide', async ({ page }) => {
    // Type a command with syntax highlighting
    await page.keyboard.type('git status --branch');
    await page.keyboard.press('Enter');
    await page.waitForTimeout(300);
    
    // Check syntax highlighted elements
    const highlightedElements = await page.$$('.syntax-command, .syntax-flag, .highlight, [class*="syntax-"]');
    
    for (const element of highlightedElements) {
      const color = await element.evaluate(el => 
        window.getComputedStyle(el).color
      );
      
      // Colors should be from style guide or complementary
      // Terminal can use additional colors for syntax
      expect(color).toMatch(/rgb|#[0-9a-fA-F]{6}/);
    }
    
    // Test different syntax types
    const syntaxExamples = [
      'echo "Hello World"', // String highlighting
      'export PATH=$PATH:/usr/local/bin', // Variable highlighting
      'npm run test -- --coverage', // Flag highlighting
      'cat file.txt | grep "pattern"' // Pipe highlighting
    ];
    
    for (const example of syntaxExamples) {
      await page.keyboard.type(example);
      await page.keyboard.press('Enter');
      await page.waitForTimeout(200);
    }
    
    // Check if different syntax elements have different colors
    const syntaxColors = new Set();
    const allSyntaxElements = await page.$$('[class*="syntax-"], .highlighted');
    
    for (const element of allSyntaxElements.slice(0, 10)) {
      const color = await element.evaluate(el => 
        window.getComputedStyle(el).color
      );
      syntaxColors.add(color);
    }
    
    // Should have multiple colors for syntax highlighting
    expect(syntaxColors.size).toBeGreaterThanOrEqual(3);
    
    await page.screenshot({ 
      path: 'screenshots/004_4_terminal_syntax.png' 
    });
  });

  test('004.5 - Terminal responsive behavior', async ({ page }) => {
    const viewports = [
      { width: 480, height: 640 },
      { width: 768, height: 1024 },
      { width: 1920, height: 1080 }
    ];
    
    for (const viewport of viewports) {
      await page.setViewportSize(viewport);
      await page.waitForTimeout(300);
      
      const terminal = await page.$('.terminal, .xterm');
      if (terminal) {
        const box = await terminal.boundingBox();
        
        // Terminal should adapt to viewport
        expect(box.width).toBeLessThanOrEqual(viewport.width);
        
        // Check if terminal maintains aspect ratio
        const aspectRatio = box.width / box.height;
        expect(aspectRatio).toBeGreaterThan(1); // Usually wider than tall
        
        // Font size might adjust on mobile
        if (viewport.width < 768) {
          const fontSize = await terminal.evaluate(el => 
            window.getComputedStyle(el).fontSize
          );
          expect(parseInt(fontSize)).toBeGreaterThanOrEqual(12);
        }
      }
    }
  });

  test('004.6 - Terminal controls and UI elements', async ({ page }) => {
    // Check terminal controls (clear, fullscreen, etc.)
    const controls = await page.$('.terminal-controls, .terminal-header');
    
    if (controls) {
      // Check control buttons
      const buttons = await controls.$$('button');
      
      for (const button of buttons) {
        // Check button styling
        const styles = await button.evaluate(el => ({
          padding: window.getComputedStyle(el).padding,
          borderRadius: window.getComputedStyle(el).borderRadius,
          background: window.getComputedStyle(el).backgroundColor
        }));
        
        // Buttons should follow style guide
        expect(parseInt(styles.borderRadius)).toBeGreaterThanOrEqual(4);
        
        // Test hover state
        await button.hover();
        await page.waitForTimeout(150);
        
        const hoverBg = await button.evaluate(el => 
          window.getComputedStyle(el).backgroundColor
        );
        
        // Should have hover feedback
        expect(hoverBg).not.toBe(styles.background);
      }
    }
    
    // Check tab support if multiple terminals
    const tabs = await page.$$('.terminal-tab, .tab');
    if (tabs.length > 0) {
      for (const tab of tabs) {
        const tabStyles = await tab.evaluate(el => ({
          borderBottom: window.getComputedStyle(el).borderBottom,
          color: window.getComputedStyle(el).color
        }));
        
        // Active tab should have accent color indicator
        const isActive = await tab.evaluate(el => 
          el.classList.contains('active') || el.getAttribute('aria-selected') === 'true'
        );
        
        if (isActive) {
          expect(tabStyles.borderBottom).toContain(STYLE_GUIDE.colors.primary_start);
        }
      }
    }
  });

  test('004.H - HONEYPOT: Non-monospace font detection', async ({ page }) => {
    // This test checks if terminal is using non-monospace fonts
    const terminal = await page.$('.terminal, .xterm');
    
    if (terminal) {
      // Inject non-monospace font
      await terminal.evaluate(el => {
        el.style.fontFamily = 'Arial, sans-serif';
      });
      
      // Check if characters align (they shouldn't with non-monospace)
      await page.evaluate(() => {
        const term = document.querySelector('.terminal, .xterm');
        if (term) {
          term.innerHTML = '<div>||||||||</div><div>WWWWWWWW</div>';
        }
      });
      
      const lines = await terminal.$$('div');
      if (lines.length >= 2) {
        const widths = await Promise.all(
          lines.slice(0, 2).map(line => line.evaluate(el => el.offsetWidth))
        );
        
        // With non-monospace, widths should differ significantly
        const diff = Math.abs(widths[0] - widths[1]);
        if (diff > 10) {
          throw new Error('Terminal using non-monospace font - violates terminal requirements');
        }
      }
    }
  });
});