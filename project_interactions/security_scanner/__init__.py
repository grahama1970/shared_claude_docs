
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""Security Scanner - Comprehensive vulnerability detection and remediation"""

from .security_scanner_interaction import (
    SecurityScannerInteraction,
    Vulnerability,
    VulnerabilityType,
    Severity,
    ScanResult,
    SecurityPatterns
)

__all__ = [
    'SecurityScannerInteraction',
    'Vulnerability',
    'VulnerabilityType', 
    'Severity',
    'ScanResult',
    'SecurityPatterns'
]

__version__ = '1.0.0'