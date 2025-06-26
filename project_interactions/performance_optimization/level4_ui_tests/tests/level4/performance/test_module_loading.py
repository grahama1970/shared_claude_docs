#!/usr/bin/env python3
"""
Task #009: Performance Optimization - Module Loading
Tests lazy loading, prefetching, and bundle optimization

External Dependencies:
- playwright: https://playwright.dev/python/
- pytest: https://docs.pytest.org/
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import time
import json
from typing import Dict, List
import pytest
from playwright.sync_api import Page, Browser
from loguru import logger


class ModuleLoadingPerformance:
    """Test suite for module loading performance"""
    
    def __init__(self, page: Page):
        self.page = page
        self.metrics = {
            "cold_start": {},
            "warm_start": {},
            "lazy_load": {},
            "prefetch": {}
        }
    
    async def measure_cold_start(self, module: str, url: str) -> Dict:
        """Measure cold start performance"""
        # Clear cache
        await self.page.context.clear_cookies()
        await self.page.context.clear_permissions()
        
        start_time = time.time()
        
        # Navigate with performance monitoring
        await self.page.goto(url, wait_until="networkidle")
        
        # Get performance metrics
        perf_data = await self.page.evaluate("""
            () => {
                const nav = performance.getEntriesByType('navigation')[0];
                const resources = performance.getEntriesByType('resource');
                
                return {
                    domContentLoaded: nav.domContentLoadedEventEnd - nav.domContentLoadedEventStart,
                    loadComplete: nav.loadEventEnd - nav.loadEventStart,
                    firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime || 0,
                    firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0,
                    resources: resources.length,
                    totalResourceSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                    jsResources: resources.filter(r => r.name.endsWith('.js')).length,
                    cssResources: resources.filter(r => r.name.endsWith('.css')).length
                };
            }
        """)
        
        load_time = time.time() - start_time
        
        self.metrics["cold_start"][module] = {
            "total_time": load_time,
            "dom_content_loaded": perf_data["domContentLoaded"],
            "first_paint": perf_data["firstPaint"],
            "first_contentful_paint": perf_data["firstContentfulPaint"],
            "resources_loaded": perf_data["resources"],
            "total_size_bytes": perf_data["totalResourceSize"],
            "js_bundles": perf_data["jsResources"],
            "css_bundles": perf_data["cssResources"]
        }
        
        return self.metrics["cold_start"][module]


@pytest.fixture
def perf_tester(page: Page) -> ModuleLoadingPerformance:
    return ModuleLoadingPerformance(page)


async def test_cold_start_performance(page: Page, perf_tester: ModuleLoadingPerformance):
    """Test 009.1: Cold start times for each module"""
    logger.info("Testing cold start performance for all modules")
    
    modules = [
        ("chat", "http://localhost:3000/chat"),
        ("annotator", "http://localhost:3001/annotator"),
        ("terminal", "http://localhost:3002/terminal")
    ]
    
    for module_name, url in modules:
        metrics = await perf_tester.measure_cold_start(module_name, url)
        
        # Verify performance targets
        assert metrics["total_time"] < 2.0, f"{module_name} cold start exceeds 2s"
        assert metrics["first_contentful_paint"] < 1500, f"{module_name} FCP exceeds 1.5s"
        
        logger.info(f"{module_name} cold start: {metrics['total_time']:.2f}s")
        
        await page.screenshot(path=f"screenshots/009_1_cold_start_{module_name}.png")


async def test_lazy_loading_implementation(page: Page):
    """Test 009.2: Lazy loading for heavy components"""
    logger.info("Testing lazy loading implementation")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check initial bundle size
    initial_resources = await page.evaluate("""
        () => performance.getEntriesByType('resource').length
    """)
    
    # Trigger lazy-loaded component
    await page.evaluate("""
        () => {
            // Simulate scrolling to trigger lazy load
            window.scrollTo(0, document.body.scrollHeight);
            
            // Open a modal that should be lazy-loaded
            const modalTrigger = document.querySelector('[data-lazy="modal"]');
            if (modalTrigger) modalTrigger.click();
        }
    """)
    
    await page.wait_for_timeout(1000)
    
    # Check if new resources were loaded
    final_resources = await page.evaluate("""
        () => performance.getEntriesByType('resource').length
    """)
    
    assert final_resources > initial_resources, "No lazy loading detected"
    
    # Verify lazy-loaded components
    lazy_components = await page.evaluate("""
        () => {
            const scripts = Array.from(document.scripts);
            return scripts.filter(s => 
                s.src.includes('chunk') || 
                s.src.includes('lazy') ||
                s.getAttribute('data-lazy')
            ).length;
        }
    """)
    
    assert lazy_components > 0, "No lazy-loaded chunks found"


async def test_prefetching_next_modules(page: Page):
    """Test 009.3: Prefetching for likely next modules"""
    logger.info("Testing module prefetching")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check for prefetch links
    prefetch_links = await page.evaluate("""
        () => {
            const links = Array.from(document.querySelectorAll('link[rel="prefetch"], link[rel="preload"]'));
            return links.map(link => ({
                href: link.href,
                rel: link.rel,
                as: link.as || 'unknown'
            }));
        }
    """)
    
    # Should prefetch annotator (most likely next module)
    annotator_prefetch = any("annotator" in link["href"] for link in prefetch_links)
    assert annotator_prefetch, "Annotator module not prefetched"
    
    # Measure transition speed with prefetch
    start_time = time.time()
    
    await page.click('a[href*="annotator"], button:has-text("Annotator")')
    await page.wait_for_load_state("networkidle")
    
    transition_time = time.time() - start_time
    assert transition_time < 0.5, f"Module transition too slow: {transition_time}s"


async def test_bundle_optimization(page: Page):
    """Test 009.4: Bundle sizes and code splitting"""
    logger.info("Testing bundle optimization")
    
    await page.goto("http://localhost:3000/chat")
    
    # Analyze bundle sizes
    bundles = await page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const jsBundles = resources.filter(r => r.name.endsWith('.js'));
            
            return jsBundles.map(bundle => ({
                name: bundle.name.split('/').pop(),
                size: bundle.transferSize || 0,
                duration: bundle.duration,
                compressed: bundle.encodedBodySize < bundle.decodedBodySize
            }));
        }
    """)
    
    # Check bundle sizes
    main_bundle = next((b for b in bundles if "main" in b["name"]), None)
    assert main_bundle, "Main bundle not found"
    assert main_bundle["size"] < 500000, "Main bundle too large (>500KB)"
    
    # Verify code splitting
    chunk_count = len([b for b in bundles if "chunk" in b["name"]])
    assert chunk_count > 0, "No code splitting detected"
    
    # Check compression
    compressed_bundles = [b for b in bundles if b["compressed"]]
    assert len(compressed_bundles) == len(bundles), "Not all bundles are compressed"


async def test_progressive_enhancement(page: Page):
    """Test 009.5: Progressive enhancement loading"""
    logger.info("Testing progressive enhancement")
    
    # Disable JavaScript to test base functionality
    await page.route("**/*.js", lambda route: route.abort())
    
    await page.goto("http://localhost:3000/chat")
    
    # Basic functionality should work without JS
    content = await page.content()
    assert "chat" in content.lower(), "No content without JavaScript"
    
    # Re-enable JavaScript
    await page.unroute("**/*.js")
    await page.reload()
    
    # Check enhanced features load progressively
    enhancements = await page.evaluate("""
        () => {
            const checkpoints = [];
            
            // Check if basic HTML loaded
            if (document.body.children.length > 0) {
                checkpoints.push('html-loaded');
            }
            
            // Check if CSS loaded
            if (window.getComputedStyle(document.body).backgroundColor !== 'rgba(0, 0, 0, 0)') {
                checkpoints.push('css-loaded');
            }
            
            // Check if JS enhanced
            if (document.querySelector('[data-enhanced="true"]')) {
                checkpoints.push('js-enhanced');
            }
            
            return checkpoints;
        }
    """)
    
    assert "html-loaded" in enhancements
    assert "css-loaded" in enhancements
    assert "js-enhanced" in enhancements


async def test_loading_animations(page: Page):
    """Test 009.6: Loading state animations per style guide"""
    logger.info("Testing loading animations")
    
    # Throttle network to see loading states
    await page.context.set_offline(False)
    await page.route("**/*", lambda route: route.continue_(throttle=1000))
    
    await page.goto("http://localhost:3000/chat")
    
    # Check for loading indicator
    loading_indicator = await page.wait_for_selector(".loading, .skeleton, [data-loading]", 
                                                     timeout=5000)
    
    # Verify animation properties
    animation_style = await loading_indicator.evaluate("""
        (el) => {
            const styles = window.getComputedStyle(el);
            return {
                animation: styles.animation,
                transition: styles.transition,
                opacity: styles.opacity
            };
        }
    """)
    
    assert animation_style["animation"] != "none" or animation_style["transition"] != "none"
    
    # Check skeleton loader if present
    skeleton = await page.query_selector(".skeleton-loader, .skeleton")
    if skeleton:
        skeleton_bg = await skeleton.evaluate("""
            (el) => window.getComputedStyle(el).background
        """)
        assert "gradient" in skeleton_bg.lower(), "Skeleton should use gradient animation"


# Performance summary generator
async def test_generate_performance_report(page: Page, perf_tester: ModuleLoadingPerformance):
    """Test 009.7: Generate comprehensive performance report"""
    
    # Run all performance tests
    modules = ["chat", "annotator", "terminal"]
    
    for module in modules:
        url = f"http://localhost:{3000 + modules.index(module)}/{module}"
        await perf_tester.measure_cold_start(module, url)
    
    # Generate report
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "average_cold_start": sum(m["total_time"] for m in perf_tester.metrics["cold_start"].values()) / len(modules),
            "total_resources": sum(m["resources_loaded"] for m in perf_tester.metrics["cold_start"].values()),
            "total_size_mb": sum(m["total_size_bytes"] for m in perf_tester.metrics["cold_start"].values()) / 1024 / 1024
        },
        "modules": perf_tester.metrics["cold_start"],
        "recommendations": []
    }
    
    # Add recommendations
    for module, metrics in perf_tester.metrics["cold_start"].items():
        if metrics["total_time"] > 2.0:
            report["recommendations"].append(f"Optimize {module} - exceeds 2s target")
        if metrics["js_bundles"] > 10:
            report["recommendations"].append(f"Reduce JS bundles for {module}")
    
    # Save report
    with open("reports/009_performance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Performance report generated: Average cold start: {report['summary']['average_cold_start']:.2f}s")
    
    # All modules should meet target
    assert report["summary"]["average_cold_start"] < 2.0


if __name__ == "__main__":
    import asyncio
    from playwright.async_api import async_playwright
    
    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            tester = ModuleLoadingPerformance(page)
            
            # Test cold start
            metrics = await tester.measure_cold_start("chat", "http://localhost:3000/chat")
            print(f"Chat cold start: {metrics['total_time']:.2f}s")
            print(f"First paint: {metrics['first_paint']:.0f}ms")
            print(f"Resources: {metrics['resources_loaded']}")
            
            await browser.close()
    
    asyncio.run(main())