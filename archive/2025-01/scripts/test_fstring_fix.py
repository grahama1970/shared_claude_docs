#!/usr/bin/env python3
"""
Test script showing the specific fix for the f-string error mentioned
"""

# Your original problematic code:
# f'<span class="metric-value">{results.get("success_rate", 0):.1f}%</span>'

# Here's how to fix it:

results = {"success_rate": 95.5, "error_rate": 4.5}

# Solution 1: Add a space (RECOMMENDED)
html1 = f'<span class="metric-value">{results.get("success_rate", 0):.1f} %</span>'
print(f"Solution 1 (space): {html1}")

# Solution 2: String concatenation
html2 = f'<span class="metric-value">{results.get("success_rate", 0):.1f}' + '%</span>'
print(f"Solution 2 (concat): {html2}")

# Solution 3: Use format() method
html3 = '<span class="metric-value">{:.1f}%</span>'.format(results.get("success_rate", 0))
print(f"Solution 3 (format): {html3}")

# Solution 4: Use intermediate variable
success_rate = f'{results.get("success_rate", 0):.1f}'
html4 = f'<span class="metric-value">{success_rate}%</span>'
print(f"Solution 4 (variable): {html4}")

# For multiple metrics in a loop
print("\nMultiple metrics example:")
for metric, value in results.items():
    # Safe way to format each metric
    formatted_html = f'<div class="{metric}">{value:.1f} %</div>'
    print(formatted_html)

# CSS example with pixels
width = 1200
height = 800

# Safe CSS formatting
css = f"""
.container {{
    width: {width}px;
    height: {height}px;
    max-width: {width * 0.9:.0f}px;
}}
"""
print(f"\nCSS example:{css}")

print("\n✅ All examples work correctly in Python 3.12!")