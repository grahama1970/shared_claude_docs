"""
Module: marker adapter
Description: Adapter module to make Marker accessible with expected import paths
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/marker/src')

# Re-export marker module components
try:
    from marker import *
except ImportError:
    pass