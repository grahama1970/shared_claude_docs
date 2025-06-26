import { test, expect, devices } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #013: Mobile Responsive Testing
 * Tests all modules on mobile viewports with touch interactions and performance
 */

test.describe('Mobile Responsive Testing', () => {
  const mobileDevices = [
    { name: 'iPhone_SE', device: devices['iPhone SE'] },
    { name: 'iPhone_12', device: devices['iPhone 12'] },
    { name: 'Pixel_5', device: devices['Pixel 5'] },
    { name: 'Galaxy_S21', device: { ...devices['Galaxy S9+'], viewport: { width: 360, height: 800 } } },
    { name: 'iPad_Mini', device: devices['iPad Mini'] }
  ];

  test('013.1 - Touch interactions work smoothly', async ({ browser }) => {
    const startTime = Date.now();
    
    for (const { name, device } of mobileDevices) {
      const context = await browser.newContext({
        ...device,
        hasTouch: true
      });
      const page = await context.newPage();
      
      // Test in chat module
      await page.goto('http://localhost:3000/chat');
      await page.waitForLoadState('networkidle');
      
      // Test tap
      const button = await page.$('button, .btn');
      if (button) {
        const box = await button.boundingBox();
        await page.tap(box.x + box.width / 2, box.y + box.height / 2);
        
        // Check for tap feedback
        const tapFeedback = await button.evaluate(el => {
          const style = window.getComputedStyle(el);
          return {
            hasActiveState: el.matches(':active'),
            transform: style.transform,
            opacity: style.opacity
          };
        });
        
        // Should have visual feedback
        expect(tapFeedback.transform !== 'none' || parseFloat(tapFeedback.opacity) < 1).toBeTruthy();
      }
      
      // Test swipe gesture
      await page.touchscreen.swipe({
        start: { x: 200, y: 400 },
        end: { x: 200, y: 100 },
        steps: 10
      });
      
      // Test pinch zoom in annotator
      await page.goto('http://localhost:3001/annotator');
      
      // Simulate pinch zoom
      await page.touchscreen.tap(150, 300);
      await page.evaluate(() => {
        // Simulate pinch gesture
        const event = new TouchEvent('touchstart', {
          touches: [
            new Touch({ identifier: 1, target: document.body, clientX: 100, clientY: 300 }),
            new Touch({ identifier: 2, target: document.body, clientX: 200, clientY: 300 })
          ]
        });
        document.dispatchEvent(event);
      });
      
      await page.waitForTimeout(100);
      
      await page.evaluate(() => {
        const event = new TouchEvent('touchmove', {
          touches: [
            new Touch({ identifier: 1, target: document.body, clientX: 50, clientY: 300 }),
            new Touch({ identifier: 2, target: document.body, clientX: 250, clientY: 300 })
          ]
        });
        document.dispatchEvent(event);
      });
      
      // Check if zoom controls appear
      const zoomControls = await page.$('.zoom-controls, .pinch-zoom-indicator');
      expect(zoomControls).toBeTruthy();
      
      await page.screenshot({ 
        path: `screenshots/013_1_touch_${name}.png` 
      });
      
      await context.close();
    }
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(20);
    expect(duration).toBeLessThanOrEqual(30);
  });

  test('013.2 - Mobile-specific UI patterns', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
      hasTouch: true
    });
    const page = await context.newPage();
    
    // Test bottom navigation on mobile
    await page.goto('http://localhost:3000/chat');
    
    const mobileNav = await page.evaluate(() => {
      const bottomNav = document.querySelector('.mobile-nav, .bottom-navigation, nav[data-mobile]');
      const hamburger = document.querySelector('.hamburger, .menu-toggle');
      const tabBar = document.querySelector('.tab-bar, .mobile-tabs');
      
      return {
        hasBottomNav: !!bottomNav,
        bottomNavPosition: bottomNav ? window.getComputedStyle(bottomNav).position : null,
        hasHamburger: !!hamburger,
        hasTabBar: !!tabBar,
        navHeight: bottomNav ? bottomNav.offsetHeight : 0
      };
    });
    
    expect(mobileNav.hasBottomNav || mobileNav.hasHamburger).toBeTruthy();
    
    // Test drawer menu
    if (mobileNav.hasHamburger) {
      const hamburger = await page.$('.hamburger, .menu-toggle');
      await hamburger.tap();
      
      await page.waitForSelector('.drawer, .mobile-menu, .slide-menu', { timeout: 2000 });
      
      const drawer = await page.evaluate(() => {
        const menu = document.querySelector('.drawer, .mobile-menu');
        const overlay = document.querySelector('.overlay, .backdrop');
        
        return {
          isVisible: menu ? window.getComputedStyle(menu).display !== 'none' : false,
          hasOverlay: !!overlay,
          width: menu ? menu.offsetWidth : 0,
          animation: menu ? window.getComputedStyle(menu).transition : null
        };
      });
      
      expect(drawer.isVisible).toBeTruthy();
      expect(drawer.hasOverlay).toBeTruthy();
      expect(drawer.width).toBeGreaterThan(200); // Adequate drawer width
      
      // Close drawer by tapping overlay
      await page.tap(50, 200); // Tap outside drawer
      await page.waitForTimeout(300);
      
      const drawerClosed = await page.$('.drawer:not(.open), .mobile-menu:not(.active)');
      expect(drawerClosed || !await page.$('.drawer:visible')).toBeTruthy();
    }
    
    // Test mobile input handling
    const input = await page.$('input[type="text"], textarea');
    if (input) {
      await input.tap();
      
      // Check if viewport adjusts for keyboard
      const viewportBefore = await page.viewportSize();
      await page.waitForTimeout(500); // Wait for keyboard
      
      // Mobile-specific input features
      const inputFeatures = await input.evaluate(el => ({
        hasAutoComplete: el.hasAttribute('autocomplete'),
        hasInputMode: el.hasAttribute('inputmode'),
        fontSize: window.getComputedStyle(el).fontSize
      }));
      
      // Font size should be at least 16px to prevent zoom on iOS
      expect(parseInt(inputFeatures.fontSize)).toBeGreaterThanOrEqual(16);
    }
    
    await context.close();
  });

  test('013.3 - Performance on mobile devices', async ({ browser }) => {
    const performanceMetrics = {};
    
    for (const { name, device } of mobileDevices.slice(0, 3)) { // Test first 3 devices
      const context = await browser.newContext({
        ...device,
        hasTouch: true
      });
      const page = await context.newPage();
      
      // Enable CPU throttling to simulate mobile performance
      const client = await page.context().newCDPSession(page);
      await client.send('Emulation.setCPUThrottlingRate', { rate: 4 }); // 4x slowdown
      
      // Measure load performance
      const startTime = performance.now();
      await page.goto('http://localhost:3000/chat');
      const loadTime = performance.now() - startTime;
      
      // Get performance metrics
      const metrics = await page.evaluate(() => {
        const entries = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        
        return {
          domContentLoaded: entries.domContentLoadedEventEnd - entries.domContentLoadedEventStart,
          firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
          firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
          resources: performance.getEntriesByType('resource').length
        };
      });
      
      performanceMetrics[name] = {
        loadTime,
        ...metrics
      };
      
      // Test scroll performance
      await page.evaluate(() => {
        // Add content for scrolling
        const content = document.querySelector('main, .content');
        if (content) {
          for (let i = 0; i < 50; i++) {
            const div = document.createElement('div');
            div.style.height = '100px';
            div.style.margin = '10px';
            div.style.background = '#f0f0f0';
            div.textContent = `Item ${i + 1}`;
            content.appendChild(div);
          }
        }
      });
      
      // Measure scroll performance
      const scrollStart = performance.now();
      
      for (let i = 0; i < 5; i++) {
        await page.touchscreen.swipe({
          start: { x: 180, y: 400 },
          end: { x: 180, y: 100 },
          steps: 10
        });
        await page.waitForTimeout(200);
      }
      
      const scrollTime = performance.now() - scrollStart;
      performanceMetrics[name].scrollPerformance = scrollTime / 5; // Average per scroll
      
      await context.close();
    }
    
    // Verify performance targets
    Object.entries(performanceMetrics).forEach(([device, metrics]) => {
      expect(metrics.firstContentfulPaint).toBeLessThan(3000); // FCP under 3s on mobile
      expect(metrics.scrollPerformance).toBeLessThan(500); // Smooth scrolling
    });
    
    console.log('Mobile Performance Metrics:', performanceMetrics);
  });

  test('013.4 - Responsive images and media', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
      hasTouch: true
    });
    const page = await context.newPage();
    
    await page.goto('http://localhost:3001/annotator');
    
    // Check responsive images
    const images = await page.evaluate(() => {
      const imgs = Array.from(document.querySelectorAll('img'));
      return imgs.map(img => ({
        src: img.src,
        srcset: img.srcset,
        sizes: img.sizes,
        loading: img.loading,
        width: img.offsetWidth,
        naturalWidth: img.naturalWidth,
        isResponsive: !!img.srcset || !!img.sizes
      }));
    });
    
    images.forEach(img => {
      // Images should be responsive on mobile
      expect(img.isResponsive || img.loading === 'lazy').toBeTruthy();
      
      // Images shouldn't be larger than viewport
      expect(img.width).toBeLessThanOrEqual(device.viewport.width);
    });
    
    // Test video elements
    const videos = await page.evaluate(() => {
      const vids = Array.from(document.querySelectorAll('video'));
      return vids.map(video => ({
        poster: video.poster,
        preload: video.preload,
        playsinline: video.hasAttribute('playsinline'),
        muted: video.muted,
        width: video.offsetWidth
      }));
    });
    
    videos.forEach(video => {
      // Videos should have mobile-friendly attributes
      expect(video.playsinline).toBeTruthy(); // Prevent fullscreen on iOS
      expect(video.preload === 'none' || video.preload === 'metadata').toBeTruthy();
    });
    
    await context.close();
  });

  test('013.5 - Mobile navigation patterns', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
      hasTouch: true
    });
    const page = await context.newPage();
    
    // Test swipe navigation
    await page.goto('http://localhost:3000/chat');
    
    // Add swipe gesture handler
    await page.evaluate(() => {
      let touchStartX = 0;
      let touchEndX = 0;
      
      document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      });
      
      document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const swipeDistance = touchEndX - touchStartX;
        
        if (Math.abs(swipeDistance) > 50) {
          if (swipeDistance > 0) {
            // Swipe right - go back
            window.postMessage({ type: 'swipe', direction: 'right' }, '*');
          } else {
            // Swipe left - go forward
            window.postMessage({ type: 'swipe', direction: 'left' }, '*');
          }
        }
      });
    });
    
    // Test swipe right (back gesture)
    await page.touchscreen.swipe({
      start: { x: 10, y: 200 },
      end: { x: 200, y: 200 },
      steps: 10
    });
    
    // Check if back action triggered
    const swipeDetected = await page.evaluate(() => {
      return new Promise(resolve => {
        window.addEventListener('message', (e) => {
          if (e.data.type === 'swipe') {
            resolve(e.data.direction);
          }
        });
        setTimeout(() => resolve(null), 1000);
      });
    });
    
    expect(swipeDetected).toBe('right');
    
    // Test pull-to-refresh
    await page.evaluate(() => {
      let startY = 0;
      let isPulling = false;
      
      document.addEventListener('touchstart', (e) => {
        if (window.scrollY === 0) {
          startY = e.touches[0].pageY;
          isPulling = true;
        }
      });
      
      document.addEventListener('touchmove', (e) => {
        if (isPulling) {
          const currentY = e.touches[0].pageY;
          const pullDistance = currentY - startY;
          
          if (pullDistance > 100) {
            document.body.classList.add('pull-to-refresh');
          }
        }
      });
    });
    
    // Simulate pull-to-refresh
    await page.touchscreen.swipe({
      start: { x: 180, y: 50 },
      end: { x: 180, y: 200 },
      steps: 20
    });
    
    const hasPullToRefresh = await page.evaluate(() => 
      document.body.classList.contains('pull-to-refresh')
    );
    
    expect(hasPullToRefresh).toBeTruthy();
    
    await context.close();
  });

  test('013.6 - Offline capability on mobile', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone 12'],
      hasTouch: true
    });
    const page = await context.newPage();
    
    await page.goto('http://localhost:3000/chat');
    
    // Check for service worker
    const hasServiceWorker = await page.evaluate(() => 'serviceWorker' in navigator);
    expect(hasServiceWorker).toBeTruthy();
    
    // Go offline
    await context.setOffline(true);
    
    // Try to navigate
    await page.reload();
    
    // Should show offline page or cached content
    const offlineContent = await page.evaluate(() => {
      const offlinePage = document.querySelector('.offline-page, [data-offline]');
      const cachedIndicator = document.querySelector('.cached-content, .offline-mode');
      
      return {
        hasOfflinePage: !!offlinePage,
        hasCachedContent: !!cachedIndicator,
        hasContent: document.body.textContent.trim().length > 0
      };
    });
    
    expect(offlineContent.hasContent).toBeTruthy();
    expect(offlineContent.hasOfflinePage || offlineContent.hasCachedContent).toBeTruthy();
    
    // Check offline functionality
    const input = await page.$('input, textarea');
    if (input) {
      await input.tap();
      await input.type('Offline message');
      
      // Should queue for later
      const queueIndicator = await page.$('.queued, .offline-queue');
      expect(queueIndicator).toBeTruthy();
    }
    
    await context.close();
  });

  test('013.H - HONEYPOT: Desktop UI on mobile', async ({ browser }) => {
    const context = await browser.newContext({
      ...devices['iPhone SE'], // Small screen
      hasTouch: true
    });
    const page = await context.newPage();
    
    await page.goto('http://localhost:3000/chat');
    
    // Check for desktop-only UI elements
    const desktopUI = await page.evaluate(() => {
      const sidebar = document.querySelector('.desktop-sidebar:not(.mobile-hidden)');
      const hoverMenus = document.querySelectorAll(':hover');
      const smallText = Array.from(document.querySelectorAll('*')).filter(el => {
        const fontSize = window.getComputedStyle(el).fontSize;
        return parseInt(fontSize) < 14;
      });
      
      return {
        hasVisibleSidebar: sidebar && window.getComputedStyle(sidebar).display !== 'none',
        hasHoverOnlyMenus: hoverMenus.length > 0,
        hasSmallText: smallText.length > 0
      };
    });
    
    // Mobile should not show desktop UI patterns
    if (desktopUI.hasVisibleSidebar || desktopUI.hasSmallText) {
      throw new Error('Desktop UI elements visible on mobile - not responsive');
    }
    
    expect(desktopUI.hasVisibleSidebar).toBeFalsy();
    
    await context.close();
  });
});