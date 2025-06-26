"""
Module: marker.src.marker.tables adapter
Description: Maps marker table extraction imports
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/marker/src')

try:
    from marker.core.converters.table import extract_tables
except ImportError:
    try:
        # Alternative import path
        from marker.processors.table_processor import extract_tables
    except ImportError as e:
        print(f"Warning: Could not import marker table functions: {e}")
        
        def extract_tables(*args, **kwargs):
            raise NotImplementedError("Marker table extraction not properly installed")