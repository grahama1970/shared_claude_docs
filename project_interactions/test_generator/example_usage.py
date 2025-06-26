"""
Example usage of the Test Generator Interaction

This script demonstrates how to use the test generator to create
comprehensive test suites from documented code.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from test_generator_interaction import TestGenerator
from pathlib import Path


def demonstrate_test_generation():
    """Demonstrate the test generator with a real example"""
    
    generator = TestGenerator()
    
    # Example 1: Math module with docstring examples
    math_module = '''
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount percentage (0-100)
    
    Returns:
        The price after applying the discount
    
    Examples:
        >>> calculate_discount(100, 20)
        80.0
        >>> calculate_discount(50, 10)
        45.0
        >>> calculate_discount(200, 0)
        200.0
        >>> calculate_discount(150, 100)
        0.0
    
    Raises:
        ValueError: If price is negative or discount is not between 0-100
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.
    
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
'''
    
    # Generate tests from the math module
    print("Generating tests from math module...")
    math_tests = generator.generate_from_docstring(math_module)
    print(f"Generated {len(math_tests)} tests")
    
    # Example 2: Markdown documentation
    api_docs = '''
# User API Documentation

## Create User

Create a new user account with the provided information.

```python
from user_api import create_user

user_data = {
    "username": "john_doe",
    "email": "john@example.com",
    "age": 25
}

new_user = create_user(user_data)
print(new_user["id"])
```

Output:
```
12345
```

## Update User

Update existing user information.

```python
from user_api import update_user

updates = {"email": "newemail@example.com"}
updated = update_user(user_id=12345, updates=updates)
print(updated["success"])
```

Output:
```
True
```
'''
    
    # Generate tests from markdown
    print("\nGenerating tests from API documentation...")
    api_tests = generator.generate_from_markdown(api_docs)
    print(f"Generated {len(api_tests)} tests")
    
    # Example 3: Generate complete test file
    all_tests = math_tests + api_tests
    test_file = generator.generate_test_file(all_tests, "example_module")
    
    # Save the generated test file
    output_path = Path("generated_test_example.py")
    output_path.write_text(test_file)
    print(f"\nGenerated test file saved to: {output_path}")
    
    # Show a preview of the generated tests
    print("\nTest file preview:")
    print("=" * 60)
    print(test_file[:1000] + "..." if len(test_file) > 1000 else test_file)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print(f"- Total tests generated: {len(all_tests)}")
    print(f"- Unit tests: {sum(1 for t in all_tests if t['test_type'] == 'unit')}")
    print(f"- Integration tests: {sum(1 for t in all_tests if t['test_type'] == 'integration')}")
    print(f"- Edge case tests: {sum(1 for t in all_tests if t['test_type'] == 'edge_case')}")
    
    return all_tests


if __name__ == "__main__":
    tests = demonstrate_test_generation()
    print("\n✅ Example completed successfully!")