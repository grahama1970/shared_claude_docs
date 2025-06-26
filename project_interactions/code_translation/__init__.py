
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Code Translation Pipeline Module

Provides AST-based code translation between Python, JavaScript, and Go.
"""

from .code_translation_interaction import (
    CodeTranslationPipeline,
    TranslationResult,
    PythonToJavaScriptTransformer,
    JavaScriptToPythonTransformer,
    GoTransformer,
)

__all__ = [
    "CodeTranslationPipeline",
    "TranslationResult", 
    "PythonToJavaScriptTransformer",
    "JavaScriptToPythonTransformer",
    "GoTransformer",
]

__version__ = "1.0.0"