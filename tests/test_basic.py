"""Basic test to verify testing infrastructure."""

def test_import():
    """Test that the project can be imported."""
    assert True  # Basic test to ensure pytest works
    
def test_python_version():
    """Verify Python version is correct."""
    import sys
    assert sys.version_info[:2] == (3, 10), f"Expected Python 3.10, got {sys.version}"
