#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Fix the HIGH priority security bugs found in the bug hunt.
Implements token validation and rate limiting across all modules.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def add_security_middleware():
    """Add comprehensive security middleware to granger_hub."""
    security_path = Path("/home/graham/workspace/experiments/granger_hub/src/granger_hub/security.py")
    
    security_code = '''"""
Granger Hub Security Middleware
Provides authentication, rate limiting, and security utilities.
"""

import time
import hashlib
import secrets
from typing import Dict, Any, Optional, Callable
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
import threading

class TokenValidator:
    """Validates authentication tokens for inter-module communication."""
    
    def __init__(self):
        self.valid_tokens = set()
        self._lock = threading.Lock()
        
    def generate_token(self, module_name: str) -> str:
        """Generate a secure token for a module."""
        token = f"granger_{module_name}_{secrets.token_urlsafe(32)}"
        with self._lock:
            self.valid_tokens.add(token)
        return token
    
    def validate_token(self, token: str) -> bool:
        """Validate an authentication token."""
        if not token or not isinstance(token, str):
            return False
        
        # Check if token follows expected format
        if not token.startswith("granger_"):
            return False
            
        with self._lock:
            return token in self.valid_tokens
    
    def revoke_token(self, token: str):
        """Revoke a token."""
        with self._lock:
            self.valid_tokens.discard(token)


class RateLimiter:
    """Implements rate limiting for API endpoints."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self._lock = threading.Lock()
    
    def check_rate_limit(self, identifier: str) -> bool:
        """Check if identifier has exceeded rate limit."""
        now = time.time()
        cutoff = now - self.window_seconds
        
        with self._lock:
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > cutoff
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False
            
            # Record request
            self.requests[identifier].append(now)
            return True
    
    def get_retry_after(self, identifier: str) -> int:
        """Get seconds until rate limit resets."""
        if not self.requests[identifier]:
            return 0
            
        oldest_request = min(self.requests[identifier])
        retry_after = int(self.window_seconds - (time.time() - oldest_request))
        return max(0, retry_after)


class SQLInjectionProtector:
    """Protects against SQL injection attacks."""
    
    DANGEROUS_PATTERNS = [
        "';", '";', '--', '/*', '*/', 'xp_', 'sp_',
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'UNION',
        'SELECT', 'FROM', 'WHERE', 'OR 1=1', 'OR "1"="1"',
        'exec', 'execute', 'script', '<script', '</script'
    ]
    
    @classmethod
    def is_safe(cls, query: str) -> bool:
        """Check if a query string is safe from SQL injection."""
        if not query or not isinstance(query, str):
            return True
            
        query_upper = query.upper()
        for pattern in cls.DANGEROUS_PATTERNS:
            if pattern.upper() in query_upper:
                return False
        
        # Check for hex encoding attempts
        if '0x' in query.lower():
            return False
            
        return True
    
    @classmethod
    def sanitize(cls, query: str) -> str:
        """Sanitize a query string."""
        if not query:
            return ""
            
        # Replace dangerous characters
        safe_query = query.replace("'", "''")
        safe_query = safe_query.replace('"', '""')
        safe_query = safe_query.replace(';', '')
        safe_query = safe_query.replace('--', '')
        
        return safe_query


# Global instances
token_validator = TokenValidator()
rate_limiter = RateLimiter()

def require_auth(func: Callable) -> Callable:
    """Decorator to require authentication for a function."""
    @wraps(func)
    def wrapper(request: Dict[str, Any], *args, **kwargs):
        token = request.get("auth")
        
        if not token_validator.validate_token(token):
            return {
                "success": False,
                "error": "Invalid authentication",
                "code": "AUTH_FAILED"
            }
        
        return func(request, *args, **kwargs)
    
    return wrapper


def rate_limit(identifier_func: Callable[[Dict], str]) -> Callable:
    """Decorator to apply rate limiting."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: Dict[str, Any], *args, **kwargs):
            identifier = identifier_func(request)
            
            if not rate_limiter.check_rate_limit(identifier):
                retry_after = rate_limiter.get_retry_after(identifier)
                return {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "code": "RATE_LIMITED",
                    "retry_after": retry_after
                }
            
            return func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator


def sql_protection(func: Callable) -> Callable:
    """Decorator to protect against SQL injection."""
    @wraps(func)
    def wrapper(request: Dict[str, Any], *args, **kwargs):
        # Check all string parameters for SQL injection
        for key, value in request.items():
            if isinstance(value, str) and not SQLInjectionProtector.is_safe(value):
                return {
                    "success": False,
                    "error": f"Potential SQL injection detected in parameter: {key}",
                    "code": "SQL_INJECTION_BLOCKED"
                }
        
        return func(request, *args, **kwargs)
    
    return wrapper


# Combined security decorator
def secure_endpoint(func: Callable) -> Callable:
    """Apply all security measures to an endpoint."""
    @require_auth
    @rate_limit(lambda req: req.get("auth", "anonymous")[:50])  # Use token prefix as identifier
    @sql_protection
    @wraps(func)
    def wrapper(request: Dict[str, Any], *args, **kwargs):
        return func(request, *args, **kwargs)
    
    return wrapper
'''
    
    security_path.parent.mkdir(parents=True, exist_ok=True)
    security_path.write_text(security_code)
    print(f"✅ Created security middleware: {security_path}")
    
    # Update granger_hub __init__.py
    init_path = security_path.parent / "__init__.py"
    if init_path.exists():
        content = init_path.read_text()
        if "security" not in content:
            content += "\nfrom .security import token_validator, rate_limiter, secure_endpoint, require_auth, rate_limit, sql_protection\n"
            init_path.write_text(content)
            print("✅ Updated granger_hub __init__.py with security imports")


def fix_module_security(module_name: str):
    """Fix security issues in a specific module."""
    module_path = Path(f"/home/graham/workspace/shared_claude_docs/project_interactions/{module_name}/__init__.py")
    
    if not module_path.exists():
        print(f"❌ Module {module_name} __init__.py not found")
        return
    
    content = module_path.read_text()
    
    # Check if security is already implemented
    if "secure_endpoint" in content:
        print(f"✅ {module_name} already has security implementation")
        return
    
    # Add security implementation
    security_addition = '''

# Security implementation
try:
    from granger_hub.security import token_validator, rate_limiter, SQLInjectionProtector
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False

def handle_request_secure(request):
    """Enhanced handle_request with security measures."""
    # Check authentication
    if SECURITY_AVAILABLE:
        token = request.get("auth")
        if not token or not token_validator.validate_token(token):
            return {
                "success": False,
                "error": "Invalid authentication",
                "code": "AUTH_FAILED"
            }
        
        # Check rate limit
        identifier = token[:50] if token else "anonymous"
        if not rate_limiter.check_rate_limit(identifier):
            return {
                "success": False,
                "error": "Rate limit exceeded",
                "code": "RATE_LIMITED",
                "retry_after": rate_limiter.get_retry_after(identifier)
            }
        
        # Check for SQL injection
        query = request.get("query", "")
        if query and not SQLInjectionProtector.is_safe(query):
            return {
                "success": False,
                "error": "Potential SQL injection detected",
                "code": "SQL_INJECTION_BLOCKED"
            }
    
    # Call original handle_request if it exists
    if 'handle_request_original' in globals():
        return handle_request_original(request)
    else:
        # Default implementation
        return {
            "success": True,
            "message": f"Request handled by {__name__}",
            "security": "enabled" if SECURITY_AVAILABLE else "disabled"
        }

# Replace original handle_request if it exists
if 'handle_request' in globals():
    handle_request_original = handle_request
    handle_request = handle_request_secure
else:
    handle_request = handle_request_secure
'''
    
    # Append security implementation
    content += security_addition
    module_path.write_text(content)
    print(f"✅ Added security implementation to {module_name}")


def create_security_tests():
    """Create comprehensive security tests."""
    test_path = Path("/home/graham/workspace/shared_claude_docs/project_interactions/test_security_fixes.py")
    
    test_code = '''#!/usr/bin/env python3
"""
Test the security fixes implementation.
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.insert(0, "/home/graham/workspace/experiments/granger_hub/src")
sys.path.insert(0, str(Path(__file__).parent))

def test_token_validation():
    """Test token validation in all modules."""
    print("\\n🔐 Testing Token Validation...")
    
    modules = ["arangodb", "marker", "sparta"]
    results = {}
    
    for module_name in modules:
        try:
            module = __import__(module_name)
            
            # Test with invalid token
            result = module.handle_request({
                "auth": "invalid_token",
                "command": "test"
            })
            
            # Should fail authentication
            if result.get("code") == "AUTH_FAILED":
                results[module_name] = "✅ PASS - Correctly rejects invalid token"
            else:
                results[module_name] = f"❌ FAIL - Accepted invalid token: {result}"
                
        except Exception as e:
            results[module_name] = f"❌ ERROR - {str(e)}"
    
    return results


def test_rate_limiting():
    """Test rate limiting implementation."""
    print("\\n⏱️  Testing Rate Limiting...")
    
    modules = ["arangodb", "marker", "sparta"]
    results = {}
    
    for module_name in modules:
        try:
            module = __import__(module_name)
            
            # Generate valid token
            from granger_hub.security import token_validator
            token = token_validator.generate_token(module_name)
            
            # Make many rapid requests
            triggered = False
            for i in range(150):  # Exceed default limit of 100
                result = module.handle_request({
                    "auth": token,
                    "command": "test",
                    "id": i
                })
                
                if result.get("code") == "RATE_LIMITED":
                    triggered = True
                    results[module_name] = f"✅ PASS - Rate limit triggered at request {i}"
                    break
            
            if not triggered:
                results[module_name] = "❌ FAIL - Rate limit not triggered after 150 requests"
                
        except Exception as e:
            results[module_name] = f"❌ ERROR - {str(e)}"
    
    return results


def test_sql_injection_protection():
    """Test SQL injection protection."""
    print("\\n💉 Testing SQL Injection Protection...")
    
    modules = ["arangodb", "sparta"]  # Modules likely to use queries
    results = {}
    
    sql_injections = [
        "'; DROP TABLE users; --",
        "1' OR '1'='1",
        "admin'--",
        "' UNION SELECT * FROM passwords--"
    ]
    
    for module_name in modules:
        try:
            module = __import__(module_name)
            
            # Generate valid token
            from granger_hub.security import token_validator
            token = token_validator.generate_token(module_name)
            
            blocked_count = 0
            for injection in sql_injections:
                result = module.handle_request({
                    "auth": token,
                    "operation": "search",
                    "query": injection
                })
                
                if result.get("code") == "SQL_INJECTION_BLOCKED":
                    blocked_count += 1
            
            if blocked_count == len(sql_injections):
                results[module_name] = f"✅ PASS - Blocked all {blocked_count} injection attempts"
            else:
                results[module_name] = f"⚠️  PARTIAL - Blocked {blocked_count}/{len(sql_injections)} attempts"
                
        except Exception as e:
            results[module_name] = f"❌ ERROR - {str(e)}"
    
    return results


def main():
    """Run all security tests."""
    print("🔒 Security Fix Verification Tests")
    print("=" * 50)
    
    # Test token validation
    token_results = test_token_validation()
    print("\\nToken Validation Results:")
    for module, result in token_results.items():
        print(f"  {module}: {result}")
    
    # Test rate limiting
    rate_results = test_rate_limiting()
    print("\\nRate Limiting Results:")
    for module, result in rate_results.items():
        print(f"  {module}: {result}")
    
    # Test SQL injection
    sql_results = test_sql_injection_protection()
    print("\\nSQL Injection Protection Results:")
    for module, result in sql_results.items():
        print(f"  {module}: {result}")
    
    # Summary
    all_results = {**token_results, **rate_results, **sql_results}
    passed = sum(1 for r in all_results.values() if "✅ PASS" in r)
    total = len(all_results)
    
    print(f"\\n📊 Summary: {passed}/{total} tests passed")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
'''
    
    test_path.write_text(test_code)
    os.chmod(test_path, 0o755)
    print(f"✅ Created security test suite: {test_path}")


def main():
    """Implement security fixes for all HIGH priority bugs."""
    print("🔧 Implementing Security Fixes for HIGH Priority Bugs\\n")
    
    # Step 1: Create security middleware in granger_hub
    print("1. Creating security middleware...")
    add_security_middleware()
    
    # Step 2: Fix security in each module
    print("\\n2. Fixing security in modules...")
    modules = ["arangodb", "marker", "sparta"]
    for module in modules:
        fix_module_security(module)
    
    # Step 3: Create security tests
    print("\\n3. Creating security test suite...")
    create_security_tests()
    
    print("\\n✅ Security fixes implemented!")
    print("\\nNext steps:")
    print("1. Run security tests to verify fixes")
    print("2. Re-run bug hunter to confirm issues resolved")
    print("3. Get AI feedback on the implementation")


if __name__ == "__main__":
    main()