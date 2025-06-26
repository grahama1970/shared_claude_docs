"""
Module: api_wrapper.py
Description: Universal API wrapper for Granger modules

External Dependencies:
- typing: https://docs.python.org/3/library/typing.html

Sample Input:
>>> wrapper = GrangerAPIWrapper(module)
>>> result = wrapper.call({"operation": "test"})

Expected Output:
>>> {"status": "success", "data": {...}}

Example Usage:
>>> from api_wrapper import wrap_module
>>> wrapped = wrap_module(my_module)
"""

from typing import Dict, Any, Callable

class GrangerAPIWrapper:
    """Wraps modules to provide consistent API"""
    
    def __init__(self, module: Any):
        self.module = module
        
        # Detect available methods
        self.has_handle = hasattr(module, 'handle')
        self.has_process_request = hasattr(module, 'process_request')
        self.has_process = hasattr(module, 'process')
        self.has_execute = hasattr(module, 'execute')
        
    def call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Universal method to call the module"""
        try:
            # Try methods in order of preference
            if self.has_handle:
                return self.module.handle(request)
            elif self.has_process_request:
                return self.module.process_request(request)
            elif self.has_process:
                return self.module.process(request)
            elif self.has_execute:
                return self.module.execute(request)
            else:
                # Fallback: try to call the module directly
                if callable(self.module):
                    return self.module(request)
                else:
                    return {"error": "No suitable method found on module"}
        except Exception as e:
            return {"error": f"API call failed: {str(e)}"}
    
    def __getattr__(self, name):
        """Delegate other attributes to the wrapped module"""
        return getattr(self.module, name)

def wrap_module(module: Any) -> GrangerAPIWrapper:
    """Convenience function to wrap a module"""
    return GrangerAPIWrapper(module)

# Standard API interface
class GrangerModuleInterface:
    """Standard interface that all Granger modules should implement"""
    
    def handle(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming requests"""
        raise NotImplementedError("Modules must implement handle method")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return module capabilities"""
        return {
            "name": self.__class__.__name__,
            "version": "1.0.0",
            "operations": []
        }

# Ensure all modules have standard methods
def ensure_standard_api(module_class):
    """Decorator to ensure a module has standard API methods"""
    
    # Add handle method if missing
    if not hasattr(module_class, 'handle'):
        def handle(self, request: Dict[str, Any]) -> Dict[str, Any]:
            if hasattr(self, 'process_request'):
                return self.process_request(request)
            elif hasattr(self, 'process'):
                return self.process(request)
            else:
                return {"error": "No processing method available"}
        
        module_class.handle = handle
    
    # Add process_request method if missing
    if not hasattr(module_class, 'process_request'):
        def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
            if hasattr(self, 'handle'):
                return self.handle(request)
            elif hasattr(self, 'process'):
                return self.process(request)
            else:
                return {"error": "No processing method available"}
        
        module_class.process_request = process_request
    
    return module_class
