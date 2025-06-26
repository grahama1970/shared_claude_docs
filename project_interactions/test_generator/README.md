# Test Generator Interaction

## Overview

The Test Generator Interaction (GRANGER Task #31) is a Level 2 automated tool that analyzes documentation and code examples to generate comprehensive test suites. It extracts examples from docstrings and markdown documentation to create unit tests, integration tests, edge cases, and parameterized tests.

## Features

- **Documentation Parsing**: Extracts code examples from Python docstrings and markdown files
- **Example Validation**: Identifies expected outputs and generates appropriate assertions
- **Edge Case Generation**: Automatically creates tests for boundary conditions based on parameter types
- **Parameterized Tests**: Groups similar examples into efficient parameterized test cases
- **Test Organization**: Generates well-structured test files with proper categorization

## Usage

```python
from test_generator_interaction import TestGenerator

# Initialize the generator
generator = TestGenerator()

# Generate tests from a function with docstring
source_code = '''
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle.
    
    Examples:
        >>> calculate_area(5, 3)
        15
        >>> calculate_area(10, 10)
        100
    """
    return length * width
'''

tests = generator.generate_from_docstring(source_code)

# Generate tests from markdown documentation
markdown = '''
## Usage Example

```python
def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)
```

Output:
```
Hello, Alice!
```
'''

md_tests = generator.generate_from_markdown(markdown)

# Create complete test file
all_tests = tests + md_tests
test_file_content = generator.generate_test_file(all_tests, 'my_module')
```

## Test Types Generated

### 1. Unit Tests
- Generated from docstring examples
- Direct function call validation
- Assertion-based verification

### 2. Edge Case Tests
- Boundary value testing
- Type-specific edge cases (0, -1, empty strings, etc.)
- Exception handling tests

### 3. Integration Tests
- Generated from markdown documentation
- Complete workflow testing
- Multi-step scenarios

### 4. Parameterized Tests
- Groups similar test cases
- Efficient test execution
- Reduces code duplication

## Edge Case Patterns

The generator includes predefined edge cases for common types:

- **int**: 0, -1, 1, -999999, 999999
- **float**: 0.0, -1.0, 1.0, inf, -inf
- **str**: '', ' ', 'a', long strings, special characters
- **list**: [], [None], [1], large lists
- **dict**: {}, {'key': None}, nested dictionaries
- **bool**: True, False
- **None**: None

## Output Format

Generated test files include:

1. Proper imports and path setup
2. Test functions organized by type
3. Descriptive test names and docstrings
4. Expected duration estimates
5. Test summary statistics

## Example Generated Test

```python
def test_multiply_example_1():
    """Test multiply with docstring example 1"""
    result = multiply(2, 3)
    assert result == 6

def test_multiply_edge_case_a_0():
    """Test multiply with edge case: a=0"""
    try:
        result = multiply(a=0, b=1)
        assert result == 0
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions
        pass
```

## Integration with Other Tools

This tool can be integrated with:

- **Claude Test Reporter**: For generating test reports
- **Code Documentation Tools**: To analyze existing documentation
- **CI/CD Pipelines**: For automated test generation
- **IDE Plugins**: For on-the-fly test creation

## Best Practices

1. **Clear Examples**: Ensure documentation includes clear input/output examples
2. **Type Hints**: Use type annotations for better edge case generation
3. **Expected Outputs**: Always include expected outputs in examples
4. **Edge Case Documentation**: Document known edge cases and exceptions
5. **Review Generated Tests**: Always review and enhance generated tests as needed

## Limitations

- Requires well-formatted documentation with examples
- Generated tests may need manual refinement for complex scenarios
- Edge cases are based on common patterns and may not cover all scenarios
- Cannot generate tests for functions without documentation

## Future Enhancements

- Support for more documentation formats (RST, etc.)
- AI-powered test case generation
- Property-based testing generation
- Test coverage analysis integration
- Custom edge case configurations