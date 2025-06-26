"""SPARTA handlers compatibility module"""
# Re-export from actual location
try:
    from sparta.integrations.sparta_module import SPARTAModule as SPARTAHandler
except ImportError:
    # Fallback to real handlers if available
    try:
        from .real_sparta_handlers import SPARTAHandler
    except ImportError:
        SPARTAHandler = None

__all__ = ["SPARTAHandler"]
