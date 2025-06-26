"""
Module: marker.src.marker adapter
Description: Maps expected marker imports to actual module structure
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/marker/src')

# Import the actual convert function
try:
    from marker.core.scripts.convert import convert_pdf_to_markdown
    from marker.core.converters.pdf import PDFConverter
    
    # Also try to import from convert_single if convert doesn't have it
    try:
        from marker.core.scripts.convert_single import convert_single_pdf
        # If convert_pdf_to_markdown doesn't exist, use convert_single_pdf
        if 'convert_pdf_to_markdown' not in locals():
            convert_pdf_to_markdown = convert_single_pdf
    except ImportError:
        pass
        
except ImportError as e:
    print(f"Warning: Could not import marker convert functions: {e}")
    
    def convert_pdf_to_markdown(*args, **kwargs):
        raise NotImplementedError("Marker module not properly installed")

# Re-export everything
__all__ = ['convert_pdf_to_markdown', 'PDFConverter']