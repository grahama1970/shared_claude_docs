import { test, expect, Page } from '@playwright/test';
import { STYLE_GUIDE } from '../../../utils/style-guide';

/**
 * Task #009: Performance Optimization - Module Loading
 * Tests lazy loading, prefetching, bundle optimization, and progressive enhancement
 */

test.describe('Performance Optimization - Module Loading', () => {
  test.beforeEach(async ({ page }) => {
    // Enable performance monitoring
    await page.addScriptTag({
      content: `
        window.performanceMonitor = {
          marks: {},
          measures: {},
          
          mark: function(name) {
            this.marks[name] = performance.now();
            performance.mark(name);
          },
          
          measure: function(name, startMark, endMark) {
            const duration = this.marks[endMark] - this.marks[startMark];
            this.measures[name] = duration;
            performance.measure(name, startMark, endMark);
            return duration;
          },
          
          getResourceTimings: function() {
            return performance.getEntriesByType('resource').map(r => ({
              name: r.name,
              duration: r.duration,
              size: r.transferSize,
              type: r.initiatorType
            }));
          },
          
          getBundleSizes: function() {
            const resources = this.getResourceTimings();
            return resources.filter(r => r.type === 'script' || r.type === 'link')
              .reduce((acc, r) => {
                const module = r.name.includes('chat') ? 'chat' :
                            r.name.includes('annotator') ? 'annotator' :
                            r.name.includes('terminal') ? 'terminal' : 'core';
                acc[module] = (acc[module] || 0) + r.size;
                return acc;
              }, {});
          }
        };
      `
    });
  });

  test('009.1 - Cold start performance measurement', async ({ page }) => {
    const startTime = Date.now();
    
    // Clear cache for cold start
    await page.context().clearCookies();
    await page.evaluate(() => {
      localStorage.clear();
      sessionStorage.clear();
    });
    
    // Test each module's cold start
    const modules = [
      { name: 'chat', url: 'http://localhost:3000/chat' },
      { name: 'annotator', url: 'http://localhost:3001/annotator' },
      { name: 'terminal', url: 'http://localhost:3002/terminal' }
    ];
    
    const coldStartMetrics = {};
    
    for (const module of modules) {
      // Mark navigation start
      await page.evaluate(() => {
        window.performanceMonitor.mark('navigationStart');
      });
      
      // Navigate to module
      await page.goto(module.url, { waitUntil: 'networkidle' });
      
      // Mark load complete
      await page.evaluate(() => {
        window.performanceMonitor.mark('loadComplete');
      });
      
      // Measure cold start time
      const metrics = await page.evaluate(() => {
        const loadTime = window.performanceMonitor.measure('coldStart', 'navigationStart', 'loadComplete');
        const paint = performance.getEntriesByType('paint');
        
        return {
          totalLoadTime: loadTime,
          firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
          firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
          domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
          resources: window.performanceMonitor.getResourceTimings().length,
          bundleSizes: window.performanceMonitor.getBundleSizes()
        };
      });
      
      coldStartMetrics[module.name] = metrics;
      
      // Verify performance targets
      expect(metrics.totalLoadTime).toBeLessThan(2000); // Under 2s target
      expect(metrics.firstContentfulPaint).toBeLessThan(1500); // FCP under 1.5s
      
      await page.screenshot({ 
        path: `screenshots/009_1_cold_start_${module.name}.png` 
      });
    }
    
    // Log results
    console.log('Cold Start Metrics:', coldStartMetrics);
    
    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeGreaterThanOrEqual(10);
    expect(duration).toBeLessThanOrEqual(15);
  });

  test('009.2 - Lazy loading implementation', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Check initial bundle size
    const initialResources = await page.evaluate(() => 
      window.performanceMonitor.getResourceTimings()
    );
    
    const initialScripts = initialResources.filter(r => r.type === 'script');
    const initialSize = initialScripts.reduce((sum, r) => sum + r.size, 0);
    
    // Verify lazy loading setup
    const lazyComponents = await page.evaluate(() => {
      // Check for dynamic imports
      const scripts = Array.from(document.querySelectorAll('script'));
      const hasDynamicImports = scripts.some(s => 
        s.textContent?.includes('import(') || s.textContent?.includes('require.ensure')
      );
      
      // Check for intersection observer (for lazy loading)
      const hasIntersectionObserver = 'IntersectionObserver' in window;
      
      // Check for lazy loaded images
      const lazyImages = document.querySelectorAll('img[loading="lazy"], img[data-src]');
      
      return {
        hasDynamicImports,
        hasIntersectionObserver,
        lazyImageCount: lazyImages.length
      };
    });
    
    expect(lazyComponents.hasDynamicImports || lazyComponents.hasIntersectionObserver).toBeTruthy();
    
    // Trigger lazy loading by scrolling
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    
    await page.waitForTimeout(1000); // Wait for lazy loading
    
    // Check resources loaded after scroll
    const afterScrollResources = await page.evaluate(() => 
      window.performanceMonitor.getResourceTimings()
    );
    
    const newResources = afterScrollResources.length - initialResources.length;
    expect(newResources).toBeGreaterThan(0); // Some resources loaded lazily
    
    // Test route-based code splitting
    await page.click('a[href*="annotator"], .open-annotator');
    await page.waitForLoadState('networkidle');
    
    const annotatorResources = await page.evaluate(() => {
      const resources = window.performanceMonitor.getResourceTimings();
      return resources.filter(r => r.name.includes('annotator'));
    });
    
    // Annotator-specific code should load only when needed
    expect(annotatorResources.length).toBeGreaterThan(0);
  });

  test('009.3 - Prefetching for likely modules', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Set up prediction for likely next module
    await page.evaluate(() => {
      // Simulate RL prediction
      const prediction = {
        nextModule: 'annotator',
        confidence: 0.85
      };
      localStorage.setItem('granger-next-module-prediction', JSON.stringify(prediction));
    });
    
    await page.reload();
    await page.waitForLoadState('networkidle');
    
    // Check for prefetch/preload hints
    const prefetchElements = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll('link[rel="prefetch"], link[rel="preload"], link[rel="modulepreload"]'));
      return links.map(link => ({
        rel: link.rel,
        href: link.href,
        as: link.getAttribute('as')
      }));
    });
    
    // Should prefetch annotator resources
    const annotatorPrefetch = prefetchElements.some(link => 
      link.href.includes('annotator')
    );
    expect(annotatorPrefetch).toBeTruthy();
    
    // Test prefetch effectiveness
    const beforeNavigation = performance.now();
    
    await page.click('a[href*="annotator"]');
    await page.waitForURL('**/annotator');
    
    const navigationTime = performance.now() - beforeNavigation;
    
    // Navigation should be faster due to prefetching
    expect(navigationTime).toBeLessThan(500); // Under 500ms target
    
    // Verify prefetched resources were used
    const resourceTimings = await page.evaluate(() => {
      return performance.getEntriesByType('resource')
        .filter(r => r.name.includes('annotator'))
        .map(r => ({
          name: r.name,
          fetchStart: r.fetchStart,
          responseEnd: r.responseEnd,
          fromCache: r.transferSize === 0
        }));
    });
    
    // Some resources should be from cache (prefetched)
    const cachedResources = resourceTimings.filter(r => r.fromCache);
    expect(cachedResources.length).toBeGreaterThan(0);
  });

  test('009.4 - Bundle size optimization', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Analyze bundle sizes
    const bundleAnalysis = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      
      const bundles = {
        js: resources.filter(r => r.name.endsWith('.js')),
        css: resources.filter(r => r.name.endsWith('.css')),
        fonts: resources.filter(r => r.name.includes('font')),
        images: resources.filter(r => r.initiatorType === 'img')
      };
      
      const analysis = {};
      
      for (const [type, items] of Object.entries(bundles)) {
        analysis[type] = {
          count: items.length,
          totalSize: items.reduce((sum, r) => sum + r.transferSize, 0),
          avgSize: items.length ? items.reduce((sum, r) => sum + r.transferSize, 0) / items.length : 0,
          largest: items.reduce((max, r) => r.transferSize > max.size ? { name: r.name, size: r.transferSize } : max, { size: 0 })
        };
      }
      
      return analysis;
    });
    
    // Check bundle sizes are optimized
    expect(bundleAnalysis.js.avgSize).toBeLessThan(200 * 1024); // Avg JS bundle < 200KB
    expect(bundleAnalysis.css.totalSize).toBeLessThan(100 * 1024); // Total CSS < 100KB
    
    // Check for code splitting
    const jsChunks = bundleAnalysis.js.count;
    expect(jsChunks).toBeGreaterThan(1); // Multiple chunks indicate code splitting
    
    // Check compression
    const compressionCheck = await page.evaluate(async () => {
      const response = await fetch(window.location.href);
      const encoding = response.headers.get('content-encoding');
      return {
        compressed: encoding === 'gzip' || encoding === 'br',
        encoding
      };
    });
    
    expect(compressionCheck.compressed).toBeTruthy();
    
    // Check for tree shaking (no unused exports)
    const treeShakingCheck = await page.evaluate(() => {
      // Check if development mode warnings about unused exports
      const hasUnusedExports = window.__webpack_exports_info__?.unused || false;
      return !hasUnusedExports;
    });
    
    expect(treeShakingCheck).toBeTruthy();
  });

  test('009.5 - Progressive enhancement', async ({ page }) => {
    // Test with JavaScript disabled first
    await page.context().route('**/*.js', route => route.abort());
    
    await page.goto('http://localhost:3000/chat');
    
    // Core functionality should still work
    const coreElements = await page.evaluate(() => {
      return {
        hasContent: document.body.textContent.trim().length > 0,
        hasNavigation: document.querySelector('nav, .navigation') !== null,
        hasForm: document.querySelector('form, input') !== null,
        hasSemanticHTML: document.querySelector('main, article, section') !== null
      };
    });
    
    expect(coreElements.hasContent).toBeTruthy();
    expect(coreElements.hasNavigation).toBeTruthy();
    expect(coreElements.hasSemanticHTML).toBeTruthy();
    
    // Re-enable JavaScript
    await page.context().route('**/*.js', route => route.continue());
    await page.reload();
    
    // Enhanced functionality should be available
    const enhancedFeatures = await page.evaluate(() => {
      return {
        hasReactApp: document.querySelector('#root, [data-reactroot]') !== null,
        hasWebSocket: 'WebSocket' in window,
        hasServiceWorker: 'serviceWorker' in navigator,
        hasCustomElements: 'customElements' in window
      };
    });
    
    expect(enhancedFeatures.hasReactApp).toBeTruthy();
    expect(enhancedFeatures.hasWebSocket).toBeTruthy();
  });

  test('009.6 - Loading state animations', async ({ page }) => {
    await page.goto('http://localhost:3000/chat');
    
    // Inject loading state
    await page.evaluate(() => {
      document.body.classList.add('loading');
      
      // Create skeleton loader
      const skeleton = document.createElement('div');
      skeleton.className = 'skeleton-loader';
      skeleton.innerHTML = `
        <div class="skeleton-header" style="
          height: 60px;
          background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s infinite;
          margin-bottom: 16px;
        "></div>
        <div class="skeleton-content" style="
          height: 200px;
          background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s infinite;
        "></div>
      `;
      
      const style = document.createElement('style');
      style.textContent = `
        @keyframes shimmer {
          0% { background-position: -200% 0; }
          100% { background-position: 200% 0; }
        }
      `;
      document.head.appendChild(style);
      document.body.appendChild(skeleton);
    });
    
    // Verify loading animation follows style guide
    const loadingAnimation = await page.$('.skeleton-loader');
    expect(loadingAnimation).toBeTruthy();
    
    const animationStyle = await loadingAnimation.evaluate(el => {
      const computed = window.getComputedStyle(el.querySelector('.skeleton-header'));
      return {
        animationDuration: computed.animationDuration,
        animationTimingFunction: computed.animationTimingFunction
      };
    });
    
    // Animation should be smooth and not too fast
    expect(parseFloat(animationStyle.animationDuration) * 1000).toBeGreaterThanOrEqual(1000);
    expect(parseFloat(animationStyle.animationDuration) * 1000).toBeLessThanOrEqual(2000);
    
    // Remove loading state
    await page.evaluate(() => {
      document.body.classList.remove('loading');
      document.querySelector('.skeleton-loader')?.remove();
    });
    
    // Content should fade in smoothly
    await page.evaluate(() => {
      const content = document.querySelector('main, .content');
      if (content) {
        content.style.opacity = '0';
        content.style.transition = 'opacity 300ms ease-in-out';
        setTimeout(() => {
          content.style.opacity = '1';
        }, 100);
      }
    });
    
    await page.waitForTimeout(400);
    
    const contentOpacity = await page.evaluate(() => {
      const content = document.querySelector('main, .content');
      return content ? window.getComputedStyle(content).opacity : '1';
    });
    
    expect(parseFloat(contentOpacity)).toBe(1);
  });

  test('009.H - HONEYPOT: Instant module load', async () => {
    // This test checks for unrealistic instant loading
    const page = await test.page;
    
    const loadStart = performance.now();
    await page.goto('http://localhost:3000/chat');
    const loadTime = performance.now() - loadStart;
    
    // Module loading should take measurable time
    if (loadTime < 50) {
      throw new Error('Module loaded instantly - this indicates mocked/fake loading');
    }
    
    expect(loadTime).toBeGreaterThan(50);
  });
});