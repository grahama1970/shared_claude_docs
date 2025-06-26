"""
Module: marker.src.marker.settings adapter
Description: Maps marker settings imports
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/marker/src')

try:
    from marker.core.settings import Settings
except ImportError as e:
    print(f"Warning: Could not import marker settings: {e}")
    
    class Settings:
        def __init__(self):
            raise NotImplementedError("Marker settings not properly installed")