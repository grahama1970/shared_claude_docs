"""
Module: sparta adapter
Description: Adapter module to make SPARTA accessible with expected import paths
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/sparta/src')

# Re-export sparta module components
from sparta import *