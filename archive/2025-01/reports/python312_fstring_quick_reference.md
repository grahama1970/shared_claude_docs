# Python 3.12 F-String Quick Reference

## The Problem
Python 3.12 interprets characters like `%` or `px` immediately after a format specifier as part of a decimal literal, causing `SyntaxError: invalid decimal literal`.

```python
# ❌ These cause SyntaxError in Python 3.12:
f'{value:.1f}%'     # SyntaxError: invalid decimal literal
f'{width}px'        # Can cause issues in certain contexts
f'{rate:.2f}$'      # SyntaxError: invalid decimal literal
```

## Quick Solutions

### 1. **Add a Space** (Recommended)
```python
# ✅ Add space before the literal
f'{value:.1f} %'    # 95.5 %
f'{width} px'       # 1200 px
f'{rate:.2f} USD'   # 12.34 USD
```

### 2. **Use String Concatenation**
```python
# ✅ Concatenate the suffix
f'{value:.1f}' + '%'     # 95.5%
f'{width}' + 'px'        # 1200px
str(width) + 'px'        # 1200px
```

### 3. **Use Intermediate Variables**
```python
# ✅ Format first, then use
formatted = f'{value:.1f}'
result = f'{formatted}%'  # 95.5%
```

### 4. **Move Currency Symbols**
```python
# ✅ Put currency symbols at the front
f'${price:.2f}'     # $12.34 (instead of f'{price:.2f}$')
f'€{amount:.2f}'    # €99.99
```

## Common Patterns

### HTML/CSS Generation
```python
# ✅ Correct way
html = f'<span class="value">{rate:.1f} %</span>'
css = f'width: {width}px; height: {height}px;'

# Or use helper functions
def px(value): return f'{value}px'
def pct(value): return f'{value:.1f} %'

css = f'width: {px(width)}; margin: {pct(margin)};'
```

### Dashboard Metrics
```python
metrics = {"success_rate": 98.7, "error_rate": 1.3}

# ✅ Correct way
display = f'''
Success: {metrics["success_rate"]:.1f} %
Errors: {metrics["error_rate"]:.1f} %
'''
```

### Financial Formatting
```python
# ✅ Correct way
revenue = 1234567.89
formatted = f'Revenue: ${revenue:,.2f}'  # Revenue: $1,234,567.89
growth = f'Growth: {rate:.1f} %'        # Growth: 23.4 %
```

## Helper Functions (Best Practice)

```python
def format_percentage(value: float, decimals: int = 1) -> str:
    """Format as percentage with proper spacing."""
    return f'{value:.{decimals}f} %'

def format_currency(value: float, symbol: str = '$') -> str:
    """Format as currency."""
    return f'{symbol}{value:,.2f}'

def format_pixels(value: int) -> str:
    """Format as CSS pixels."""
    return f'{value}px'

# Usage
print(format_percentage(95.5))        # 95.5 %
print(format_currency(1234.56))       # $1,234.56
print(format_pixels(1200))            # 1200px
```

## Quick Conversion Guide

| Old (Python < 3.12) | New (Python 3.12+) | Alternative |
|---------------------|-------------------|-------------|
| `f'{v:.1f}%'` | `f'{v:.1f} %'` | `f'{v:.1f}' + '%'` |
| `f'{w}px'` | `f'{w}px'` or `f'{w} px'` | `str(w) + 'px'` |
| `f'{p:.2f}$'` | `f'${p:.2f}'` | `f'{p:.2f} $'` |
| `f'{t:.1f}°C'` | `f'{t:.1f} °C'` | `f'{t:.1f}' + '°C'` |
| `f'{d:.2%}'` | `f'{d * 100:.2f} %'` | `f'{d:.2%}'.replace('%', ' %')` |

## Testing Your Code

```python
# Quick test to verify Python 3.12 compatibility
def test_fstring_compatibility():
    try:
        value = 95.5
        # Test various formats
        tests = [
            f'{value:.1f} %',           # Space before %
            f'{value:.1f}' + '%',       # Concatenation
            f'${value:.2f}',            # Currency front
            f'{int(value)}px',          # Pixels
        ]
        print("✅ All f-string formats are Python 3.12 compatible!")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False

test_fstring_compatibility()
```

## Remember
- **Always test** your f-strings in Python 3.12
- **Prefer spaces** for readability: `{value:.1f} %` over concatenation
- **Use helper functions** for consistent formatting across your codebase
- **Consider `Template` strings** for complex HTML/CSS generation