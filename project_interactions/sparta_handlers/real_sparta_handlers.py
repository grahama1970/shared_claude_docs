"""
Module: real_sparta_handlers.py
Description: Adapter to provide expected SPARTA handler interface for tests
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/sparta/src')

try:
    from sparta.integrations.sparta_module import SPARTAModule
    
    class SPARTAHandler(SPARTAModule):
        """Adapter class for SPARTA module to match test expectations"""
        pass
    
    class SPARTACVESearchHandler(SPARTAModule):
        """Adapter for CVE search functionality"""
        pass
        
except ImportError:
    # Fallback to trying other possible locations
    try:
        from sparta.integrations.sparta_module_real_api import SPARTAModule
        
        class SPARTAHandler(SPARTAModule):
            """Adapter class for SPARTA module to match test expectations"""
            pass
        
        class SPARTACVESearchHandler(SPARTAModule):
            """Adapter for CVE search functionality"""
            pass
            
    except ImportError as e:
        print(f"Warning: Could not import SPARTA module: {e}")
        
        class SPARTAHandler:
            def __init__(self):
                raise NotImplementedError("SPARTA module not properly installed")
        
        class SPARTACVESearchHandler:
            def __init__(self):
                raise NotImplementedError("SPARTA module not properly installed")