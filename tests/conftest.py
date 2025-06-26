"""Pytest configuration for project tests."""

import sys
import pytest
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))

# Configure asyncio
pytest_plugins = ["pytest_asyncio"]

@pytest.fixture
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture
def test_data_dir(project_root):
    """Return test data directory."""
    data_dir = project_root / "tests" / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir
