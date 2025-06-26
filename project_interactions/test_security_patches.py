"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Security regression test suite
Ensures security patches remain effective
"""

import pytest
from granger_security_middleware_simple import GrangerSecurity

class TestSecurityPatches:
    """Test security patches are working"""
    
    def setup_method(self):
        self.security = GrangerSecurity()
    
    def test_sql_injection_protection(self):
        """Test SQL injection is blocked"""
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "1; DELETE FROM accounts",
            "admin'--",
            "' UNION SELECT * FROM passwords"
        ]
        
        for payload in malicious_inputs:
            result = self.security.validate_request({
                "token": "granger_valid_token_12345",
                "query": payload
            })
            assert not result['valid'], f"SQL injection not blocked: {payload}"
    
    def test_authentication_validation(self):
        """Test authentication is properly validated"""
        invalid_tokens = [
            "",
            " ",
            None,
            "invalid",
            "fake_token",
            "' OR '1'='1"
        ]
        
        for token in invalid_tokens:
            result = self.security.validate_request({
                "token": token,
                "action": "read"
            })
            assert not result['valid'], f"Invalid token accepted: {token}"
    
    def test_error_sanitization(self):
        """Test stack traces are removed"""
        error = 'File "/home/user/secret/path.py", line 42\nSecretError'
        cleaned = self.security.remove_stack_traces(error)
        
        assert "/home/user" not in cleaned
        assert "line 42" not in cleaned
        assert "secret" not in cleaned.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
