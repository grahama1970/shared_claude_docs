#!/usr/bin/env python3
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
    print("\n🔐 Testing Token Validation...")
    
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
    print("\n⏱️  Testing Rate Limiting...")
    
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
    print("\n💉 Testing SQL Injection Protection...")
    
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
    print("\nToken Validation Results:")
    for module, result in token_results.items():
        print(f"  {module}: {result}")
    
    # Test rate limiting
    rate_results = test_rate_limiting()
    print("\nRate Limiting Results:")
    for module, result in rate_results.items():
        print(f"  {module}: {result}")
    
    # Test SQL injection
    sql_results = test_sql_injection_protection()
    print("\nSQL Injection Protection Results:")
    for module, result in sql_results.items():
        print(f"  {module}: {result}")
    
    # Summary
    all_results = {**token_results, **rate_results, **sql_results}
    passed = sum(1 for r in all_results.values() if "✅ PASS" in r)
    total = len(all_results)
    
    print(f"\n📊 Summary: {passed}/{total} tests passed")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
