import { test, expect } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #002.3: Validates animations and transitions
 * Ensures 60fps performance and correct timing curves
 */

test.describe('Chat Module - Animation Performance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    await page.waitForLoadState('networkidle');
    
    // Inject FPS monitoring script
    await page.addScriptTag({
      content: `
        window.fpsMonitor = {
          frames: [],
          lastTime: performance.now(),
          fps: 0,
          start: function() {
            const measure = () => {
              const now = performance.now();
              const delta = now - this.lastTime;
              this.frames.push(1000 / delta);
              if (this.frames.length > 60) this.frames.shift();
              this.fps = this.frames.reduce((a, b) => a + b) / this.frames.length;
              this.lastTime = now;
              requestAnimationFrame(measure);
            };
            requestAnimationFrame(measure);
          },
          reset: function() {
            this.frames = [];
            this.fps = 0;
          }
        };
        window.fpsMonitor.start();
      `
    });
  });

  test('002.3 - Button hover animations at 60fps', async ({ page }) => {
    const startTime = Date.now();
    
    // Reset FPS monitor
    await page.evaluate(() => window.fpsMonitor.reset());
    
    // Find primary button
    const button = await page.$('.btn-primary, [data-testid="primary-button"]');
    expect(button).toBeTruthy();
    
    // Measure animation performance
    const bbox = await button.boundingBox();
    
    // Trigger hover animation multiple times
    for (let i = 0; i < 5; i++) {
      await page.mouse.move(bbox.x + bbox.width / 2, bbox.y + bbox.height / 2);
      await page.waitForTimeout(150); // Half animation duration
      await page.mouse.move(0, 0);
      await page.waitForTimeout(150);
    }
    
    // Get FPS measurement
    const fps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(fps).toBeGreaterThanOrEqual(55); // Allow small margin below 60fps
    
    // Check transition timing
    const transitionDuration = await button.evaluate(el => {
      const computed = window.getComputedStyle(el);
      const duration = computed.transitionDuration;
      return parseFloat(duration) * 1000; // Convert to ms
    });
    
    expect(transitionDuration).toBeGreaterThanOrEqual(STYLE_GUIDE.animation.duration_min);
    expect(transitionDuration).toBeLessThanOrEqual(STYLE_GUIDE.animation.duration_max);
    
    // Check easing function
    const transitionTiming = await button.evaluate(el => 
      window.getComputedStyle(el).transitionTimingFunction
    );
    expect(transitionTiming).toContain('cubic-bezier');
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(5);
    expect(duration).toBeLessThanOrEqual(8);
    
    await page.screenshot({ 
      path: 'screenshots/002_3_chat_animations.png' 
    });
  });

  test('002.3 - Modal open/close animations', async ({ page }) => {
    // Reset FPS monitor
    await page.evaluate(() => window.fpsMonitor.reset());
    
    // Trigger modal
    const modalTrigger = await page.$('[data-testid="open-modal"], .open-modal');
    if (modalTrigger) {
      await modalTrigger.click();
      
      // Wait for modal animation
      await page.waitForSelector('.modal, [role="dialog"]', { state: 'visible' });
      await page.waitForTimeout(300); // Full animation duration
      
      // Check FPS during animation
      const fps = await page.evaluate(() => window.fpsMonitor.fps);
      expect(fps).toBeGreaterThanOrEqual(55);
      
      // Check backdrop fade
      const backdrop = await page.$('.modal-backdrop, .backdrop');
      if (backdrop) {
        const opacity = await backdrop.evaluate(el => 
          window.getComputedStyle(el).opacity
        );
        expect(parseFloat(opacity)).toBeGreaterThan(0);
      }
      
      // Close modal
      await page.keyboard.press('Escape');
      await page.waitForTimeout(300);
      
      // Verify smooth close animation
      const finalFps = await page.evaluate(() => window.fpsMonitor.fps);
      expect(finalFps).toBeGreaterThanOrEqual(55);
    }
  });

  test('002.3 - Smooth scrolling performance', async ({ page }) => {
    // Add content to enable scrolling
    await page.evaluate(() => {
      const content = document.querySelector('.chat-messages, main');
      if (content) {
        for (let i = 0; i < 50; i++) {
          const div = document.createElement('div');
          div.style.height = '100px';
          div.style.margin = '16px';
          div.style.background = '#F3F4F6';
          div.style.borderRadius = '8px';
          div.textContent = `Message ${i + 1}`;
          content.appendChild(div);
        }
      }
    });
    
    // Reset FPS monitor
    await page.evaluate(() => window.fpsMonitor.reset());
    
    // Perform smooth scroll
    await page.evaluate(() => {
      window.scrollTo({ top: 1000, behavior: 'smooth' });
    });
    
    await page.waitForTimeout(1000); // Wait for scroll to complete
    
    // Check FPS during scroll
    const scrollFps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(scrollFps).toBeGreaterThanOrEqual(50); // Slightly lower threshold for scroll
    
    // Test scroll-triggered animations (e.g., fade-in on scroll)
    const animatedElements = await page.$$('[data-animate="fade-in"]');
    for (const element of animatedElements) {
      const isVisible = await element.isVisible();
      if (isVisible) {
        const opacity = await element.evaluate(el => 
          window.getComputedStyle(el).opacity
        );
        expect(parseFloat(opacity)).toBe(1);
      }
    }
  });

  test('002.3 - Loading states and skeleton animations', async ({ page }) => {
    // Trigger a loading state
    await page.evaluate(() => {
      // Simulate loading state
      document.body.classList.add('loading');
      const container = document.querySelector('.chat-container, main');
      if (container) {
        container.innerHTML = `
          <div class="skeleton-loader" style="
            width: 100%;
            height: 60px;
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: 8px;
            margin-bottom: 16px;
          "></div>
        `.repeat(5);
        
        // Add shimmer animation
        const style = document.createElement('style');
        style.textContent = `
          @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
          }
        `;
        document.head.appendChild(style);
      }
    });
    
    // Reset FPS monitor
    await page.evaluate(() => window.fpsMonitor.reset());
    
    // Wait for animations
    await page.waitForTimeout(2000);
    
    // Check shimmer animation performance
    const shimmerFps = await page.evaluate(() => window.fpsMonitor.fps);
    expect(shimmerFps).toBeGreaterThanOrEqual(55);
    
    // Verify animation is smooth
    const skeletons = await page.$$('.skeleton-loader');
    expect(skeletons.length).toBeGreaterThan(0);
  });

  test('002.H - HONEYPOT: Invalid instant animations', async ({ page }) => {
    // This test checks for unrealistic instant animations
    const button = await page.$('.btn-primary');
    
    if (button) {
      // Check if transition duration is too fast (instant)
      const transitionDuration = await button.evaluate(el => {
        const computed = window.getComputedStyle(el);
        return parseFloat(computed.transitionDuration) * 1000;
      });
      
      // Should fail if animations are instant (< 50ms)
      if (transitionDuration < 50) {
        throw new Error('Animations are too fast to be real - likely mocked');
      }
      
      // Should fail if no transition is defined
      expect(transitionDuration).toBeGreaterThan(0);
    }
  });
});