#!/usr/bin/env python3
"""
Module: test_security_checks.py
Purpose: Tests for security vulnerability detection

External Dependencies:
- pytest: Testing framework - https://docs.pytest.org/

Example Usage:
>>> pytest test_security_checks.py -v
"""

import pytest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from code_reviewer_interaction import (
    SecurityAnalyzer, CodeReviewerInteraction,
    IssueSeverity, IssueCategory
)


class TestSecurityAnalyzer:
    """Test security analysis functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = SecurityAnalyzer()
    
    def test_hardcoded_credentials_detection(self):
        """Test detection of hardcoded credentials"""
        test_cases = [
            ('password = "secret123"', True),
            ('api_key = "sk-1234567890"', True),
            ('SECRET = "my-secret-value"', True),
            ('token = "Bearer xyz123"', True),
            ('username = "admin"', False),  # username alone is not a credential
            ('password = os.environ.get("PASSWORD")', False),  # environment variable
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            if should_detect:
                assert len(issues) > 0, f"Should detect credential in: {code}"
                assert issues[0].category == IssueCategory.SECURITY
                assert issues[0].severity == IssueSeverity.CRITICAL
            else:
                credential_issues = [i for i in issues if "credential" in i.message.lower()]
                assert len(credential_issues) == 0, f"Should not detect credential in: {code}"
    
    def test_sql_injection_detection(self):
        """Test detection of SQL injection vulnerabilities"""
        test_cases = [
            ('cursor.execute("SELECT * FROM users WHERE id = %s" % user_id)', True),
            ('db.query("DELETE FROM table WHERE name = %s" % name)', True),
            ('cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))', False),
            ('query = "SELECT * FROM users"', False),
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            sql_issues = [i for i in issues if "sql" in i.message.lower()]
            if should_detect:
                assert len(sql_issues) > 0, f"Should detect SQL injection in: {code}"
            else:
                assert len(sql_issues) == 0, f"Should not detect SQL injection in: {code}"
    
    def test_command_injection_detection(self):
        """Test detection of command injection vulnerabilities"""
        test_cases = [
            ('os.system("ls " + user_input)', True),
            ('subprocess.call("echo " + data)', True),
            ('exec("print(" + user_code + ")")', True),
            ('eval(user_expression)', True),
            ('subprocess.run(["ls", "-la"], check=True)', False),
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            cmd_issues = [i for i in issues if "command" in i.message.lower()]
            if should_detect:
                assert len(cmd_issues) > 0, f"Should detect command injection in: {code}"
    
    def test_path_traversal_detection(self):
        """Test detection of path traversal vulnerabilities"""
        test_cases = [
            ('open("../../../etc/passwd")', True),
            ('with open(f"../{filename}") as f:', True),
            ('open("/absolute/path/file.txt")', False),
            ('open("relative/path/file.txt")', False),
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            path_issues = [i for i in issues if "path traversal" in i.message.lower()]
            if should_detect:
                assert len(path_issues) > 0, f"Should detect path traversal in: {code}"
            else:
                assert len(path_issues) == 0, f"Should not detect path traversal in: {code}"
    
    def test_weak_random_detection(self):
        """Test detection of weak random number generation"""
        test_cases = [
            ('token = random.random()', True),
            ('session_id = random.randint(1000, 9999)', True),
            ('choice = random.choice(options)', True),
            ('secure_token = secrets.token_hex(16)', False),
            ('value = random.random()  # Not for security', False),  # Comment context matters
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            random_issues = [i for i in issues if "random" in i.message.lower()]
            if should_detect:
                assert len(random_issues) > 0, f"Should detect weak random in: {code}"
    
    def test_insecure_deserialization(self):
        """Test detection of insecure deserialization"""
        test_cases = [
            ('data = pickle.loads(user_data)', True),
            ('obj = pickle.load(file)', True),
            ('config = yaml.load(stream)', True),
            ('config = yaml.safe_load(stream)', False),
            ('data = json.loads(json_string)', False),
        ]
        
        for code, should_detect in test_cases:
            issues = self.analyzer.analyze(code)
            deser_issues = [i for i in issues if "deserialization" in i.message.lower()]
            if should_detect:
                assert len(deser_issues) > 0, f"Should detect insecure deserialization in: {code}"
            else:
                assert len(deser_issues) == 0, f"Should not detect in: {code}"


class TestSecurityInCodeReview:
    """Test security checks in full code review"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.reviewer = CodeReviewerInteraction()
    
    def test_comprehensive_security_review(self):
        """Test comprehensive security review of a file"""
        vulnerable_code = '''import os
import subprocess
import pickle
import random

# Multiple security issues
API_KEY = "sk-prod-1234567890abcdef"
DB_PASSWORD = "admin123"

def process_user_data(user_input, file_path):
    # SQL injection
    query = "SELECT * FROM users WHERE name = '%s'" % user_input
    
    # Command injection
    os.system("process_file " + file_path)
    
    # Path traversal
    with open("uploads/../" + file_path) as f:
        data = f.read()
    
    # Weak random for token
    token = random.randint(100000, 999999)
    
    # Insecure deserialization
    user_obj = pickle.loads(data)
    
    return token
'''
        
        test_file = Path("test_vulnerable.py")
        test_file.write_text(vulnerable_code)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            # Verify security issues are detected
            security_issues = [i for i in result.issues if i.category == IssueCategory.SECURITY]
            assert len(security_issues) >= 6, f"Should detect at least 6 security issues, found {len(security_issues)}"
            
            # Check that all are critical severity
            critical_issues = [i for i in security_issues if i.severity == IssueSeverity.CRITICAL]
            assert len(critical_issues) == len(security_issues), "All security issues should be critical"
            
            # Verify specific vulnerabilities
            vuln_types = {
                "credential": False,
                "sql injection": False,
                "command injection": False,
                "path traversal": False,
                "random": False,
                "deserialization": False
            }
            
            for issue in security_issues:
                msg_lower = issue.message.lower()
                for vuln_type in vuln_types:
                    if vuln_type in msg_lower:
                        vuln_types[vuln_type] = True
            
            for vuln_type, found in vuln_types.items():
                assert found, f"Should detect {vuln_type} vulnerability"
            
        finally:
            test_file.unlink()
    
    def test_security_suggestions(self):
        """Test that security issues have appropriate suggestions"""
        code_with_issues = '''
password = "hardcoded123"
query = "SELECT * FROM users WHERE id = %s" % user_id
'''
        
        test_file = Path("test_suggestions.py")
        test_file.write_text(code_with_issues)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            security_issues = [i for i in result.issues if i.category == IssueCategory.SECURITY]
            assert len(security_issues) >= 2, "Should find security issues"
            
            # Check all security issues have suggestions
            for issue in security_issues:
                assert issue.suggestion is not None, f"Security issue should have suggestion: {issue.message}"
                assert len(issue.suggestion) > 0, "Suggestion should not be empty"
            
        finally:
            test_file.unlink()
    
    def test_no_false_positives(self):
        """Test that secure code doesn't trigger false positives"""
        secure_code = '''import os
import secrets
import subprocess

# Environment variables, not hardcoded
API_KEY = os.environ.get("API_KEY")
PASSWORD = os.getenv("DB_PASSWORD", "")

def secure_operations(user_input):
    # Parameterized query
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
    
    # Safe subprocess call
    subprocess.run(["ls", "-la", "/safe/path"], check=True)
    
    # Secure random
    token = secrets.token_hex(16)
    
    # Safe file operation
    safe_path = Path("/uploads") / Path(user_input).name
    with open(safe_path) as f:
        data = f.read()
    
    return token
'''
        
        test_file = Path("test_secure.py")
        test_file.write_text(secure_code)
        
        try:
            result = self.reviewer.review_file(str(test_file))
            
            # Should have minimal security issues
            security_issues = [i for i in result.issues if i.category == IssueCategory.SECURITY]
            assert len(security_issues) == 0, f"Secure code should not have security issues, found: {[i.message for i in security_issues]}"
            
        finally:
            test_file.unlink()


def main():
    """Run security tests with real data validation"""
    print("🔐 Running security check tests...")
    
    # Create test instances
    analyzer_tests = TestSecurityAnalyzer()
    review_tests = TestSecurityInCodeReview()
    
    tests_passed = 0
    tests_failed = 0
    
    # Run analyzer tests
    analyzer_tests.setup_method()
    
    test_methods = [
        ("Hardcoded credentials", analyzer_tests.test_hardcoded_credentials_detection),
        ("SQL injection", analyzer_tests.test_sql_injection_detection),
        ("Command injection", analyzer_tests.test_command_injection_detection),
        ("Path traversal", analyzer_tests.test_path_traversal_detection),
        ("Weak random", analyzer_tests.test_weak_random_detection),
        ("Insecure deserialization", analyzer_tests.test_insecure_deserialization),
    ]
    
    for test_name, test_method in test_methods:
        try:
            test_method()
            print(f"✅ {test_name} detection test passed")
            tests_passed += 1
        except AssertionError as e:
            print(f"❌ {test_name} detection test failed: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            tests_failed += 1
    
    # Run review tests
    review_tests.setup_method()
    
    review_methods = [
        ("Comprehensive security review", review_tests.test_comprehensive_security_review),
        ("Security suggestions", review_tests.test_security_suggestions),
        ("No false positives", review_tests.test_no_false_positives),
    ]
    
    for test_name, test_method in review_methods:
        try:
            test_method()
            print(f"✅ {test_name} test passed")
            tests_passed += 1
        except AssertionError as e:
            print(f"❌ {test_name} test failed: {e}")
            tests_failed += 1
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            tests_failed += 1
    
    print(f"\n📊 Test Results: {tests_passed} passed, {tests_failed} failed")
    
    if tests_failed > 0:
        return 1
    
    print("\n✅ All security tests passed!")
    return 0


if __name__ == "__main__":
    exit(main())