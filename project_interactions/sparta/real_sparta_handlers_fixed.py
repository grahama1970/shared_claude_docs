"""
Module: real_sparta_handlers_fixed.py 
Description: Fixed SPARTA handlers adapter for test compatibility
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/sparta/src')

try:
    from sparta.integrations.sparta_module import SPARTAModule as SPARTACVESearchHandler
except ImportError:
    try:
        from sparta.integrations.sparta_module_real_api import SPARTAModule as SPARTACVESearchHandler
    except ImportError:
        try:
            from sparta.integrations.real_apis_fixed import SPARTAModule as SPARTACVESearchHandler
        except ImportError as e:
            print(f"Warning: Could not import SPARTA module: {e}")
            
            class SPARTACVESearchHandler:
                def __init__(self):
                    raise NotImplementedError("SPARTA module not properly installed")