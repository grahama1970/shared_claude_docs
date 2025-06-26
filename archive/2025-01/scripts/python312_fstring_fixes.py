#!/usr/bin/env python3
"""
Python 3.12 F-String Syntax Fixes

This module demonstrates how to properly handle percentage signs, pixel values,
and other special characters in f-strings for Python 3.12 compatibility.

The issue: Python 3.12 interprets characters like '%' or 'px' immediately after
a format specifier as part of a decimal literal, causing SyntaxError.
"""

# PROBLEM: These cause SyntaxError in Python 3.12
# f'{value:.1f}%'  # SyntaxError: invalid decimal literal
# f'{width}px'     # Can also cause issues in certain contexts

# SOLUTION 1: Use spaces to separate the format specifier from the literal
def format_with_spaces():
    """Add a space between the format specifier and the literal."""
    success_rate = 95.5
    width = 1200
    
    # Add space before %
    percentage = f'{success_rate:.1f} %'
    print(f"Success rate: {percentage}")
    
    # Add space before px
    css_width = f'{width} px'
    print(f"Width: {css_width}")
    
    # In HTML context
    html = f'<span class="metric-value">{success_rate:.1f} %</span>'
    print(f"HTML: {html}")


# SOLUTION 2: Use string concatenation
def format_with_concatenation():
    """Use string concatenation to avoid the issue."""
    success_rate = 95.5
    width = 1200
    
    # Concatenate the % sign
    percentage = f'{success_rate:.1f}' + '%'
    print(f"Success rate: {percentage}")
    
    # Concatenate px
    css_width = f'{width}' + 'px'
    print(f"Width: {css_width}")
    
    # In HTML context
    html = f'<span class="metric-value">{success_rate:.1f}' + '%</span>'
    print(f"HTML: {html}")


# SOLUTION 3: Use format() method or % formatting
def format_with_format_method():
    """Use .format() method or % formatting as alternatives."""
    success_rate = 95.5
    width = 1200
    
    # Using format()
    percentage = '{:.1f}%'.format(success_rate)
    print(f"Success rate: {percentage}")
    
    # Using % formatting
    percentage_old = '%.1f%%' % success_rate  # Note: %% for literal %
    print(f"Success rate (old style): {percentage_old}")
    
    # CSS with format()
    css_width = '{}px'.format(width)
    print(f"Width: {css_width}")


# SOLUTION 4: Use parentheses to clarify parsing
def format_with_parentheses():
    """Use parentheses to separate the format expression."""
    success_rate = 95.5
    width = 1200
    
    # Wrap the formatted value in parentheses and concatenate
    percentage = f'{(success_rate):.1f}' + '%'
    print(f"Success rate: {percentage}")
    
    # Alternative with the entire expression
    percentage_alt = f'{(f"{success_rate:.1f}")}%'
    print(f"Success rate alt: {percentage_alt}")


# SOLUTION 5: Use a separate variable
def format_with_variables():
    """Store the formatted value in a variable first."""
    success_rate = 95.5
    width = 1200
    
    # Format first, then use in f-string
    formatted_rate = f'{success_rate:.1f}'
    percentage = f'{formatted_rate}%'
    print(f"Success rate: {percentage}")
    
    # For CSS
    formatted_width = str(width)
    css_width = f'{formatted_width}px'
    print(f"Width: {css_width}")


# REAL-WORLD EXAMPLES
def real_world_examples():
    """Common real-world scenarios and their fixes."""
    
    # Example 1: Dashboard metrics
    metrics = {
        "success_rate": 98.7,
        "error_rate": 1.3,
        "uptime": 99.95
    }
    
    # Fixed HTML generation
    html_metrics = f'''
    <div class="metrics">
        <span class="success">{metrics["success_rate"]:.1f} %</span>
        <span class="error">{metrics["error_rate"]:.1f} %</span>
        <span class="uptime">{metrics["uptime"]:.2f} %</span>
    </div>
    '''
    print("HTML Metrics:", html_metrics.strip())
    
    # Example 2: CSS generation
    layout = {
        "width": 1200,
        "height": 800,
        "margin": 20,
        "padding": 10
    }
    
    # Fixed CSS generation
    css = f'''
    .container {{
        width: {layout["width"]}px;
        height: {layout["height"]}px;
        margin: {layout["margin"]}px;
        padding: {layout["padding"]}px;
    }}
    '''
    print("\nCSS:", css.strip())
    
    # Example 3: Financial calculations
    values = {
        "revenue": 1234567.89,
        "growth": 23.4,
        "margin": 15.7
    }
    
    # Fixed financial formatting
    report = f'''
    Revenue: ${values["revenue"]:,.2f}
    Growth: {values["growth"]:.1f} %
    Margin: {values["margin"]:.1f} %
    '''
    print("\nFinancial Report:", report.strip())
    
    # Example 4: Scientific notation
    measurements = {
        "accuracy": 0.9876,
        "precision": 0.9234,
        "recall": 0.8901
    }
    
    # Fixed scientific formatting
    ml_metrics = f'''
    Model Performance:
    - Accuracy: {measurements["accuracy"] * 100:.2f} %
    - Precision: {measurements["precision"] * 100:.2f} %
    - Recall: {measurements["recall"] * 100:.2f} %
    '''
    print("\nML Metrics:", ml_metrics.strip())


# COMMON PITFALLS AND SOLUTIONS
def common_pitfalls():
    """Demonstrate common pitfalls and their solutions."""
    
    print("\n=== Common Pitfalls and Solutions ===\n")
    
    # Pitfall 1: Multiple format specifiers
    value = 12.34567
    # WRONG: f'{value:.2f:.1%}'  # SyntaxError
    # RIGHT:
    as_percentage = f'{value * 100:.1f} %'
    print(f"Pitfall 1 - Multiple formats: {as_percentage}")
    
    # Pitfall 2: Units in expressions
    temperature = 23.5
    # WRONG: f'{temperature + 273.15:.1f}K'  # SyntaxError
    # RIGHT:
    kelvin = f'{temperature + 273.15:.1f} K'
    print(f"Pitfall 2 - Units in expressions: {kelvin}")
    
    # Pitfall 3: Nested f-strings
    name = "Python"
    version = 3.12
    # WRONG: f'{f"{name} {version}"}%'  # Can be problematic
    # RIGHT:
    full_name = f'{name} {version}'
    with_suffix = f'{full_name} %'
    print(f"Pitfall 3 - Nested f-strings: {with_suffix}")
    
    # Pitfall 4: Dynamic format specifiers
    precision = 2
    value = 3.14159
    # WRONG in some contexts: f'{value:.{precision}f}%'
    # SAFER:
    formatted = f'{value:.{precision}f}'
    with_percent = f'{formatted} %'
    print(f"Pitfall 4 - Dynamic precision: {with_percent}")


# BEST PRACTICES
def best_practices():
    """Recommended best practices for Python 3.12 f-strings."""
    
    print("\n=== Best Practices ===\n")
    
    # 1. Always use spaces for readability and compatibility
    rate = 95.5
    good_format = f'{rate:.1f} %'  # Clear and compatible
    print(f"1. Use spaces: {good_format}")
    
    # 2. For complex formatting, use intermediate variables
    complex_value = 1234.5678
    formatted_value = f'{complex_value:,.2f}'
    final_output = f'${formatted_value} USD'
    print(f"2. Intermediate variables: {final_output}")
    
    # 3. Consider using template strings for HTML/CSS
    from string import Template
    
    css_template = Template('.box { width: ${width}px; height: ${height}px; }')
    css_output = css_template.substitute(width=800, height=600)
    print(f"3. Template strings: {css_output}")
    
    # 4. Use helper functions for repeated patterns
    def format_percentage(value: float, decimals: int = 1) -> str:
        """Helper function to format percentages consistently."""
        return f'{value:.{decimals}f} %'
    
    def format_pixels(value: int) -> str:
        """Helper function to format pixel values."""
        return f'{value}px'
    
    print(f"4. Helper functions: {format_percentage(87.3)} / {format_pixels(1024)}")


# MIGRATION HELPER
def migrate_old_code():
    """Example of migrating old code to Python 3.12 compatible format."""
    
    print("\n=== Migration Examples ===\n")
    
    # Old code examples and their fixes
    old_patterns = [
        ('f"{value:.1f}%"', 'f"{value:.1f} %"'),
        ('f"{width}px"', 'f"{width}px"'),  # This one might work
        ('f"{rate:.2%}"', 'f"{rate * 100:.2f} %"'),  # % format specifier
        ('f"{price:.2f}$"', 'f"${price:.2f}"'),  # Move $ to front
    ]
    
    for old, new in old_patterns:
        print(f"OLD: {old:30} → NEW: {new}")


if __name__ == "__main__":
    print("Python 3.12 F-String Fixes Demo\n")
    print("=" * 50)
    
    print("\n--- Solution 1: Using Spaces ---")
    format_with_spaces()
    
    print("\n--- Solution 2: Using Concatenation ---")
    format_with_concatenation()
    
    print("\n--- Solution 3: Using format() Method ---")
    format_with_format_method()
    
    print("\n--- Solution 4: Using Parentheses ---")
    format_with_parentheses()
    
    print("\n--- Solution 5: Using Variables ---")
    format_with_variables()
    
    print("\n--- Real World Examples ---")
    real_world_examples()
    
    # Show common pitfalls
    common_pitfalls()
    
    # Show best practices
    best_practices()
    
    # Show migration examples
    migrate_old_code()
    
    print("\n✅ All examples work in Python 3.12!")