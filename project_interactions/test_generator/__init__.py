"""
Test Generator Interaction Module

Automated test generation from documentation and code examples.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from .test_generator_interaction import (
    TestGenerator,
    TestCase,
    CodeExample
)

__all__ = [
    'TestGenerator',
    'TestCase', 
    'CodeExample'
]

__version__ = '1.0.0'