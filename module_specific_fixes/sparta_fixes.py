#!/usr/bin/env python3
"""
Module: sparta_fixes.py
Description: SPARTA-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
"""

from pathlib import Path
import re

def apply_sparta_fixes():
    """Apply all SPARTA-specific fixes."""
    print("\n🛡️  Applying SPARTA fixes...")
    
    # 1. Add rate limiting to NVD API calls
    nvd_rate_limit_code = '''
# Add at the top of the file after imports
from granger_common import get_rate_limiter

# Initialize NVD rate limiter (NVD allows 5 requests per second)
nvd_limiter = get_rate_limiter("nvd", calls_per_second=5.0, burst_size=10)

# Wrap all NVD API calls
async def fetch_cve_data(cve_id: str):
    """Fetch CVE data with rate limiting."""
    async with nvd_limiter:
        # Original fetch code here
        response = await self._make_nvd_request(cve_id)
        return response
'''
    
    # 2. Fix path traversal in downloader
    path_validation_code = '''
def validate_download_path(self, file_path: str) -> Path:
    """Validate download path to prevent directory traversal."""
    from granger_common import validate_safe_path
    
    allowed_dirs = [
        self.download_dir,
        self.cache_dir,
        "/tmp/sparta_downloads"
    ]
    
    return validate_safe_path(file_path, allowed_dirs)
'''
    
    # 3. Add error context for better debugging
    error_context_code = '''
from contextlib import contextmanager
from loguru import logger

@contextmanager
def cve_context(cve_id: str):
    """Add CVE context to all operations."""
    logger.bind(cve_id=cve_id)
    try:
        yield
    except Exception as e:
        logger.error(f"Error processing CVE {cve_id}: {e}")
        raise
    finally:
        logger.unbind("cve_id")
'''
    
    print("✅ SPARTA fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# SPARTA Module Fix Implementation Guide

## 1. Rate Limiting (HIGH PRIORITY)
Location: src/sparta/core/downloader.py
- Add import: from granger_common import get_rate_limiter
- Initialize: nvd_limiter = get_rate_limiter("nvd", calls_per_second=5.0)
- Wrap all NVD API calls with: async with nvd_limiter:

## 2. Path Traversal Fix (CRITICAL)
Location: src/sparta/core/downloader.py
- Add path validation before any file operations
- Use validate_safe_path from granger_common
- Define allowed directories explicitly

## 3. Error Context (MEDIUM)
Location: All SPARTA modules
- Use loguru for structured logging
- Add CVE ID context to all operations
- Include full stack traces in error reports

## 4. Memory Management
Location: src/sparta/core/download_cache.py
- Implement LRU cache with size limits
- Stream large files instead of loading to memory
- Add periodic cache cleanup

## Testing
1. Test rate limiting: Run 20 CVE queries rapidly
2. Test path validation: Try "../../../etc/passwd" as download path
3. Test error handling: Query non-existent CVE
4. Monitor memory: Process 100 large CVE reports
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/sparta_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")

if __name__ == "__main__":
    apply_sparta_fixes()