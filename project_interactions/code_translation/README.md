# Code Translation Pipeline

A Level 1 task implementation for GRANGER Task #22: Multi-Language Code Translation Pipeline.

## Overview

This module provides AST-based code translation between programming languages while preserving functionality, comments, and idiomatic patterns.

## Features

- **Supported Languages**: Python ↔ JavaScript ↔ Go
- **AST-based transformation** for accurate code structure preservation
- **Comment preservation** across translations
- **Idiomatic pattern mapping** (e.g., list comprehensions → map/filter)
- **Language-specific construct handling**
- **Validation framework** to ensure functional equivalence

## Usage

```python
from code_translation_interaction import CodeTranslationPipeline

# Initialize pipeline
pipeline = CodeTranslationPipeline()

# Translate Python to JavaScript
python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""

result = pipeline.translate(python_code, "python", "javascript")
print(result.translated_code)
```

## Translation Examples

### Python to JavaScript

```python
# Python
def process_list(items):
    # Filter and transform
    result = [x * 2 for x in items if x > 0]
    return result
```

```javascript
// JavaScript
function process_list(items) {
  // Filter and transform
  let result = items.filter(x => x > 0).map(x => (x * 2));
  return result;
}
```

### Python to Go

```python
# Python
def add(a, b):
    return a + b
```

```go
// Go
func add(a interface{}, b interface{}) interface{} {
    return (a + b)
}
```

## Supported Constructs

### Python → JavaScript

- Functions and classes
- Control flow (if/else, for, while)
- List/dict comprehensions → map/filter
- f-strings → template literals
- Built-in mappings (print → console.log)
- self → this in classes

### Python → Go

- Basic functions
- Control flow structures
- Built-in mappings (print → fmt.Println)
- Package structure generation

## Implementation Details

The pipeline uses:
1. Python's `ast` module for parsing source code
2. Custom transformers for each language pair
3. Pattern matching for idiomatic translations
4. Comment extraction and preservation
5. Validation for functional equivalence

## Testing

Run the comprehensive test suite:

```bash
python code_translation_interaction.py
```

Test coverage includes:
- Basic function translation
- Class and method translation
- Control flow structures
- List comprehensions and idiomatic patterns
- Comment preservation
- Error handling
- Performance benchmarks

## Limitations

- JavaScript parsing is simplified (full parser would be needed for production)
- Go type inference is basic (uses interface{} as default)
- Some advanced language features may not be fully supported
- Translation validation is heuristic-based

## Future Enhancements

- Add support for more languages (TypeScript, Rust, Java)
- Implement full JavaScript/Go parsers
- Enhanced type inference
- Support for async/await patterns
- More sophisticated validation
- IDE integration