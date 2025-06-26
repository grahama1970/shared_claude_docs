#!/usr/bin/env python3
"""
Task #010: Accessibility Compliance - Full Journey
Tests WCAG AA compliance, keyboard navigation, screen reader support

External Dependencies:
- playwright: https://playwright.dev/python/
- axe-core: https://github.com/dequelabs/axe-core
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
from playwright.sync_api import Page
from loguru import logger


async def test_keyboard_navigation_full_journey(page: Page):
    """Test 010.1: Full keyboard navigation across all modules"""
    logger.info("Testing keyboard navigation journey")
    
    # Start at chat
    await page.goto("http://localhost:3000/chat")
    
    # Tab through all interactive elements
    tab_count = 0
    focused_elements = []
    
    for i in range(50):  # Max 50 tabs to prevent infinite loop
        await page.keyboard.press("Tab")
        
        focused = await page.evaluate("""
            () => {
                const el = document.activeElement;
                return {
                    tag: el.tagName,
                    role: el.getAttribute('role'),
                    label: el.getAttribute('aria-label') || el.textContent?.substring(0, 20),
                    visible: el.offsetParent !== null
                };
            }
        """)
        
        if focused["tag"] == "BODY":
            break  # Completed full cycle
            
        focused_elements.append(focused)
        tab_count += 1
    
    # Verify all elements are accessible
    assert tab_count > 10, "Too few tabbable elements"
    assert all(el["visible"] for el in focused_elements), "Hidden elements in tab order"
    
    # Test reverse tabbing
    await page.keyboard.press("Shift+Tab")
    await page.keyboard.press("Shift+Tab")
    
    # Navigate to annotator module via keyboard
    await page.keyboard.press("Control+Alt+2")
    await page.wait_for_url("**/annotator")
    
    logger.info(f"Keyboard navigation test passed with {tab_count} focusable elements")


async def test_screen_reader_compatibility(page: Page):
    """Test 010.2: Screen reader compatibility testing"""
    logger.info("Testing screen reader compatibility")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check ARIA landmarks
    landmarks = await page.evaluate("""
        () => {
            const roles = ['banner', 'navigation', 'main', 'contentinfo'];
            return roles.map(role => ({
                role: role,
                exists: document.querySelector(`[role="${role}"]`) !== null
            }));
        }
    """)
    
    for landmark in landmarks:
        assert landmark["exists"], f"Missing ARIA landmark: {landmark['role']}"
    
    # Check form labels
    form_elements = await page.query_selector_all("input, textarea, select")
    
    for element in form_elements:
        has_label = await element.evaluate("""
            (el) => {
                // Check for associated label
                if (el.id && document.querySelector(`label[for="${el.id}"]`)) return true;
                // Check for aria-label
                if (el.getAttribute('aria-label')) return true;
                // Check for aria-labelledby
                if (el.getAttribute('aria-labelledby')) return true;
                // Check if wrapped in label
                if (el.closest('label')) return true;
                return false;
            }
        """)
        
        assert has_label, "Form element without accessible label"
    
    # Check heading hierarchy
    headings = await page.evaluate("""
        () => {
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
            return headings.map(h => ({
                level: parseInt(h.tagName[1]),
                text: h.textContent?.substring(0, 50)
            }));
        }
    """)
    
    # Verify proper heading hierarchy
    for i in range(1, len(headings)):
        level_diff = headings[i]["level"] - headings[i-1]["level"]
        assert level_diff <= 1, f"Heading hierarchy skip: H{headings[i-1]['level']} to H{headings[i]['level']}"


async def test_wcag_aa_compliance(page: Page):
    """Test 010.3: WCAG AA compliance verification"""
    logger.info("Testing WCAG AA compliance")
    
    await page.goto("http://localhost:3000/chat")
    
    # Inject axe-core
    await page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.0/axe.min.js")
    
    # Run accessibility audit
    violations = await page.evaluate("""
        async () => {
            const results = await axe.run(document, {
                runOnly: {
                    type: 'tag',
                    values: ['wcag2a', 'wcag2aa']
                }
            });
            return results.violations;
        }
    """)
    
    # Log violations for debugging
    for violation in violations:
        logger.warning(f"WCAG violation: {violation['id']} - {violation['description']}")
    
    # Critical violations that must be fixed
    critical_violations = [v for v in violations if v["impact"] in ["critical", "serious"]]
    assert len(critical_violations) == 0, f"Found {len(critical_violations)} critical WCAG violations"
    
    # Check color contrast specifically
    contrast_issues = [v for v in violations if "contrast" in v["id"]]
    assert len(contrast_issues) == 0, "Color contrast does not meet WCAG AA"


async def test_focus_management_transitions(page: Page):
    """Test 010.4: Focus management during module transitions"""
    logger.info("Testing focus management during transitions")
    
    # Start in chat
    await page.goto("http://localhost:3000/chat")
    
    # Focus on an element
    await page.focus(".chat-input, textarea")
    initial_focus = await page.evaluate("() => document.activeElement.tagName")
    
    # Navigate to annotator
    await page.click('a[href*="annotator"]')
    await page.wait_for_url("**/annotator")
    
    # Check focus moved appropriately
    new_focus = await page.evaluate("() => document.activeElement.tagName")
    assert new_focus != "BODY", "Focus lost during transition"
    
    # Verify focus is on a meaningful element
    focus_role = await page.evaluate("() => document.activeElement.getAttribute('role')")
    assert focus_role or new_focus in ["INPUT", "BUTTON", "A"], "Focus not on interactive element"


async def test_reduced_motion_support(page: Page):
    """Test 010.5: Respect prefers-reduced-motion"""
    logger.info("Testing reduced motion support")
    
    # Enable reduced motion preference
    await page.emulate_media(reduced_motion="reduce")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check if animations are disabled
    animations_disabled = await page.evaluate("""
        () => {
            const elements = document.querySelectorAll('*');
            let hasAnimations = false;
            
            for (const el of elements) {
                const styles = window.getComputedStyle(el);
                if (styles.animationDuration !== '0s' || 
                    styles.transitionDuration !== '0s') {
                    // Check if it's instant or very fast
                    const animDuration = parseFloat(styles.animationDuration);
                    const transDuration = parseFloat(styles.transitionDuration);
                    
                    if (animDuration > 0.1 || transDuration > 0.1) {
                        hasAnimations = true;
                        break;
                    }
                }
            }
            
            return !hasAnimations;
        }
    """)
    
    assert animations_disabled, "Animations not reduced when prefers-reduced-motion is set"


async def test_error_announcements(page: Page):
    """Test 010.6: Error messages are announced to screen readers"""
    logger.info("Testing error announcements")
    
    await page.goto("http://localhost:3000/chat")
    
    # Submit invalid form to trigger error
    form = await page.query_selector("form")
    if form:
        await form.evaluate("(f) => f.submit()")
    
    # Check for ARIA live regions
    live_regions = await page.query_selector_all('[aria-live], [role="alert"], [role="status"]')
    assert len(live_regions) > 0, "No ARIA live regions for announcements"
    
    # Verify error messages have proper ARIA
    error_messages = await page.query_selector_all('.error, [role="alert"]')
    
    for error in error_messages:
        aria_attrs = await error.evaluate("""
            (el) => ({
                live: el.getAttribute('aria-live'),
                role: el.getAttribute('role'),
                atomic: el.getAttribute('aria-atomic')
            })
        """)
        
        assert aria_attrs["live"] in ["polite", "assertive"] or aria_attrs["role"] == "alert"


async def test_skip_navigation_links(page: Page):
    """Test 010.7: Skip navigation links"""
    logger.info("Testing skip navigation links")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check for skip links
    skip_links = await page.query_selector_all('a[href^="#"]:has-text("Skip")')
    assert len(skip_links) > 0, "No skip navigation links found"
    
    # Test skip link functionality
    if skip_links:
        skip_link = skip_links[0]
        target_id = await skip_link.get_attribute("href")
        
        # Click skip link
        await skip_link.click()
        
        # Verify focus moved to target
        focused_id = await page.evaluate("() => '#' + document.activeElement.id")
        assert focused_id == target_id, "Skip link did not move focus"


async def test_high_contrast_mode(page: Page):
    """Test 010.8: High contrast mode support"""
    logger.info("Testing high contrast mode")
    
    # Enable high contrast
    await page.emulate_media(color_scheme="high-contrast")
    
    await page.goto("http://localhost:3000/chat")
    
    # Check if styles adapt
    contrast_mode = await page.evaluate("""
        () => {
            const body = document.body;
            const styles = window.getComputedStyle(body);
            
            // Check for high contrast indicators
            return {
                hasHighContrastClass: body.classList.contains('high-contrast'),
                backgroundColor: styles.backgroundColor,
                color: styles.color
            };
        }
    """)
    
    # Verify visual changes for high contrast
    # Either has class or significantly different colors
    assert contrast_mode["hasHighContrastClass"] or 
           contrast_mode["backgroundColor"] != "rgb(249, 250, 251)"  # Not default bg


# Main test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])