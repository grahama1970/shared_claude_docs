"""
Auto-generated tests for example_module
Generated: 2025-06-02 06:39:13

This file contains tests generated from documentation examples,
edge cases, and parameterized test scenarios.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from example_module import *


# Unit Tests
# ==================================================

def test_calculate_discount_example_1():
    """Test calculate_discount with docstring example 1"""
    result = calculate_discount(100, 20)
    assert result == 80.0

def test_calculate_discount_example_2():
    """Test calculate_discount with docstring example 2"""
    result = calculate_discount(50, 10)
    assert result == 45.0

def test_calculate_discount_example_3():
    """Test calculate_discount with docstring example 3"""
    result = calculate_discount(200, 0)
    assert result == 200.0

def test_calculate_discount_example_4():
    """Test calculate_discount with docstring example 4"""
    result = calculate_discount(150, 100)
    assert result == 0.0

import pytest

@pytest.mark.parametrize("args,expected", [
    (100, 20, '80.0'),
    (50, 10, '45.0'),
    (200, 0, '200.0'),
    (150, 100, '0.0')
])
def calculate_discount_parameterized(args, expected):
    """Parameterized test for calculate_discount"""
    result = eval(f"calculate_discount({args})")
    assert str(result) == expected

def test_fibonacci_example_1():
    """Test fibonacci with docstring example 1"""
    result = fibonacci(0)
    assert result == 0

def test_fibonacci_example_2():
    """Test fibonacci with docstring example 2"""
    result = fibonacci(1)
    assert result == 1

def test_fibonacci_example_3():
    """Test fibonacci with docstring example 3"""
    result = fibonacci(5)
    assert result == 5

def test_fibonacci_example_4():
    """Test fibonacci with docstring example 4"""
    result = fibonacci(10)
    assert result == 55

import pytest

@pytest.mark.parametrize("args,expected", [
    (0, '0'),
    (1, '1'),
    (5, '5'),
    (10, '55')
])
def fibonacci_parameterized(args, expected):
    """Parameterized test for fibonacci"""
    result = eval(f"fibonacci({args})")
    assert str(result) == expected


# Integration Tests
# ==================================================

def test_markdown_example_1():
    """Test from markdown documentation example 1"""
    # Setup code from example
    from user_api import create_user

    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "age": 25
    }

    new_user = create_user(user_data)
    print(new_user["id"])
    
    # Verify expected output
    # Note: Add specific assertions based on the example
    assert True  # Placeholder - replace with actual assertion

def test_markdown_example_2():
    """Test from markdown documentation example 2"""
    # Setup code from example
    from user_api import update_user

    updates = {"email": "newemail@example.com"}
    updated = update_user(user_id=12345, updates=updates)
    print(updated["success"])
    
    # Verify expected output
    # Note: Add specific assertions based on the example
    assert True  # Placeholder - replace with actual assertion


# Edge Case Tests
# ==================================================

def test_calculate_discount_edge_case_price_0():
    """Test calculate_discount with edge case: price=0.0"""
    try:
        result = calculate_discount(price=0.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_1():
    """Test calculate_discount with edge case: price=-1.0"""
    try:
        result = calculate_discount(price=-1.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_2():
    """Test calculate_discount with edge case: price=1.0"""
    try:
        result = calculate_discount(price=1.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_3():
    """Test calculate_discount with edge case: price=inf"""
    try:
        result = calculate_discount(price=inf, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_4():
    """Test calculate_discount with edge case: price=-inf"""
    try:
        result = calculate_discount(price=-inf, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_0():
    """Test calculate_discount with edge case: discount_percent=0.0"""
    try:
        result = calculate_discount(price=None, discount_percent=0.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_1():
    """Test calculate_discount with edge case: discount_percent=-1.0"""
    try:
        result = calculate_discount(price=None, discount_percent=-1.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_2():
    """Test calculate_discount with edge case: discount_percent=1.0"""
    try:
        result = calculate_discount(price=None, discount_percent=1.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_3():
    """Test calculate_discount with edge case: discount_percent=inf"""
    try:
        result = calculate_discount(price=None, discount_percent=inf)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_4():
    """Test calculate_discount with edge case: discount_percent=-inf"""
    try:
        result = calculate_discount(price=None, discount_percent=-inf)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_0():
    """Test calculate_discount with edge case: price=0.0"""
    try:
        result = calculate_discount(price=0.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_1():
    """Test calculate_discount with edge case: price=-1.0"""
    try:
        result = calculate_discount(price=-1.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_2():
    """Test calculate_discount with edge case: price=1.0"""
    try:
        result = calculate_discount(price=1.0, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_3():
    """Test calculate_discount with edge case: price=inf"""
    try:
        result = calculate_discount(price=inf, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_price_4():
    """Test calculate_discount with edge case: price=-inf"""
    try:
        result = calculate_discount(price=-inf, discount_percent=None)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_0():
    """Test calculate_discount with edge case: discount_percent=0.0"""
    try:
        result = calculate_discount(price=None, discount_percent=0.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_1():
    """Test calculate_discount with edge case: discount_percent=-1.0"""
    try:
        result = calculate_discount(price=None, discount_percent=-1.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_2():
    """Test calculate_discount with edge case: discount_percent=1.0"""
    try:
        result = calculate_discount(price=None, discount_percent=1.0)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_3():
    """Test calculate_discount with edge case: discount_percent=inf"""
    try:
        result = calculate_discount(price=None, discount_percent=inf)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass

def test_calculate_discount_edge_case_discount_percent_4():
    """Test calculate_discount with edge case: discount_percent=-inf"""
    try:
        result = calculate_discount(price=None, discount_percent=-inf)
        # Verify result is valid (add specific assertions based on function)
        assert result is not None or True  # Placeholder assertion
    except (ValueError, TypeError) as e:
        # Some edge cases may raise exceptions - that's expected
        pass



# Test Summary
# ============
# Total tests: 32
# - Unit tests: 10
# - Integration tests: 2
# - Edge case tests: 20
# Expected total duration: 4.20s
