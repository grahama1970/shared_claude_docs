"""
Test remediation suggestion generation

External Dependencies:
- pytest: https://docs.pytest.org/
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
from pathlib import Path
import tempfile
import shutil
import json

from security_scanner_interaction import (
    SecurityScannerInteraction,
    VulnerabilityType,
    Severity,
    ScanResult
)


class TestRemediationSuggestions:
    """Test remediation suggestion generation and quality"""
    
    @pytest.fixture
    def scanner(self):
        """Create scanner instance"""
        return SecurityScannerInteraction()
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)
    
    def test_sql_injection_remediation(self, scanner, temp_project):
        """Test SQL injection remediation suggestions"""
        # Create file with SQL injection
        vuln_file = temp_project / "database.py"
        vuln_file.write_text('''
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    
def search_products(name):
    sql = "SELECT * FROM products WHERE name LIKE '%" + name + "%'"
    cursor.execute(sql)
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        sql_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.INJECTION]
        
        # Check remediation suggestions
        for vuln in sql_vulns:
            assert vuln.remediation is not None
            assert 'parameterized' in vuln.remediation.lower() or 'orm' in vuln.remediation.lower()
            
            # Should provide specific guidance
            assert len(vuln.remediation) > 20, "Remediation should be detailed"
    
    def test_xss_remediation(self, scanner, temp_project):
        """Test XSS remediation suggestions"""
        # Create file with XSS vulnerabilities
        vuln_file = temp_project / "frontend.js"
        vuln_file.write_text('''
function displayComment(comment) {
    document.getElementById('comments').innerHTML = comment;
}

function showAlert(message) {
    document.write('<div class="alert">' + message + '</div>');
}
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        xss_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.XSS]
        
        # Check remediation suggestions
        for vuln in xss_vulns:
            assert vuln.remediation is not None
            
            if 'innerHTML' in vuln.code_snippet:
                assert 'textContent' in vuln.remediation or 'sanitize' in vuln.remediation
            if 'document.write' in vuln.code_snippet:
                assert 'avoid' in vuln.remediation.lower() or 'alternative' in vuln.remediation.lower()
    
    def test_hardcoded_secret_remediation(self, scanner, temp_project):
        """Test hardcoded secret remediation suggestions"""
        # Create file with various secrets
        vuln_file = temp_project / "config.py"
        vuln_file.write_text('''
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "super_secret_password"
AWS_SECRET_KEY = "aws_secret_key_example"

class Settings:
    oauth_token = "ya29.a0AfH6SMBx-0bDi"
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        secret_vulns = [v for v in result.vulnerabilities 
                       if v.type == VulnerabilityType.HARDCODED_SECRET]
        
        # Check remediation suggestions
        for vuln in secret_vulns:
            assert vuln.remediation is not None
            assert 'environment' in vuln.remediation.lower() or 'key management' in vuln.remediation.lower()
            
            # Should mention specific approaches
            assert any(term in vuln.remediation.lower() 
                      for term in ['variable', 'vault', 'secrets', 'manager'])
    
    def test_weak_crypto_remediation(self, scanner, temp_project):
        """Test weak cryptography remediation suggestions"""
        # Create file with weak crypto
        vuln_file = temp_project / "crypto.py"
        vuln_file.write_text('''
import hashlib

def hash_password_md5(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_data_sha1(data):
    return hashlib.sha1(data.encode()).hexdigest()

def custom_hash(data):
    # Custom weak implementation
    return sum(ord(c) for c in data)
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        crypto_vulns = [v for v in result.vulnerabilities 
                       if v.type == VulnerabilityType.WEAK_CRYPTO]
        
        # Check remediation suggestions
        for vuln in crypto_vulns:
            assert vuln.remediation is not None
            
            if 'md5' in vuln.code_snippet.lower():
                assert 'sha-256' in vuln.remediation.lower() or 'sha256' in vuln.remediation.lower()
            if 'sha1' in vuln.code_snippet.lower():
                assert 'stronger' in vuln.remediation.lower()
            
            # Should suggest specific algorithms
            assert any(algo in vuln.remediation.upper() 
                      for algo in ['SHA-256', 'SHA256', 'AES', 'RSA'])
    
    def test_dependency_remediation(self, scanner, temp_project):
        """Test dependency vulnerability remediation"""
        # Create requirements with vulnerable packages
        req_file = temp_project / "requirements.txt"
        req_file.write_text("""
django==1.11.0
flask==0.12.0
requests==2.18.0
pyyaml==3.13
""")
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        # Check remediation suggestions
        for vuln in dep_vulns:
            assert vuln.remediation is not None
            
            # Should mention updating/upgrading
            assert 'update' in vuln.remediation.lower() or 'upgrade' in vuln.remediation.lower()
            
            # Should mention the package name
            package_name = vuln.description.split()[-1].lower()
            assert package_name in vuln.remediation.lower()
            
            # Should suggest a version or "latest"
            assert 'version' in vuln.remediation.lower() or 'latest' in vuln.remediation.lower()
    
    def test_command_injection_remediation(self, scanner, temp_project):
        """Test command injection remediation suggestions"""
        # Create file with command injection
        vuln_file = temp_project / "commands.py"
        vuln_file.write_text('''
import os
import subprocess

def run_command(user_input):
    os.system("echo " + user_input)

def execute_shell(cmd):
    subprocess.run(f"ls {cmd}", shell=True)

def dangerous_eval(code):
    result = eval(code)
    return result
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        cmd_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.COMMAND_INJECTION]
        
        # Check remediation suggestions
        for vuln in cmd_vulns:
            assert vuln.remediation is not None
            
            if 'os.system' in vuln.code_snippet:
                assert 'subprocess' in vuln.remediation
            if 'shell=True' in vuln.code_snippet:
                assert 'shell=False' in vuln.remediation
            if 'eval' in vuln.code_snippet:
                assert 'avoid' in vuln.remediation.lower() or 'ast.literal_eval' in vuln.remediation
    
    def test_path_traversal_remediation(self, scanner, temp_project):
        """Test path traversal remediation suggestions"""
        # Create file with path traversal
        vuln_file = temp_project / "file_handler.py"
        vuln_file.write_text('''
import os

def read_file(filename):
    path = "uploads/" + filename
    with open(path, 'r') as f:
        return f.read()

def serve_static(user_path):
    full_path = os.path.join("/var/www", user_path)
    return open(full_path).read()
''')
        
        # Scan and get results
        result = scanner.scan_project(str(temp_project))
        path_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.PATH_TRAVERSAL]
        
        # Check remediation suggestions
        for vuln in path_vulns:
            assert vuln.remediation is not None
            assert 'validate' in vuln.remediation.lower() or 'sanitize' in vuln.remediation.lower()
            
            # Should mention specific techniques
            assert any(technique in vuln.remediation.lower() 
                      for technique in ['realpath', 'abspath', 'whitelist', 'basename'])
    
    def test_compliance_specific_remediation(self, scanner, temp_project):
        """Test compliance-specific remediation suggestions"""
        # Create files with various issues
        (temp_project / "auth.py").write_text('''
# Weak password storage
password_hash = hashlib.md5(password).hexdigest()

# No logging
def admin_action(action):
    # Missing audit log
    execute_privileged_action(action)
''')
        
        (temp_project / "crypto.py").write_text('''
# Weak encryption for PCI data
def encrypt_card_number(card_num):
    # Using DES instead of AES
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(card_num)
''')
        
        # Scan with compliance checks
        result = scanner.scan_project(
            str(temp_project),
            compliance_checks=['PCI-DSS', 'HIPAA']
        )
        
        # All vulnerabilities should have remediation
        for vuln in result.vulnerabilities:
            assert vuln.remediation is not None
            assert len(vuln.remediation) > 10, "Remediation should be meaningful"
    
    def test_report_generation_with_remediation(self, scanner, temp_project):
        """Test that reports include remediation suggestions"""
        # Create file with multiple vulnerabilities
        vuln_file = temp_project / "vulnerable_app.py"
        vuln_file.write_text('''
import os
import hashlib

API_KEY = "sk-secret-key-12345"
password = "admin123"

def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)

def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

def run_command(cmd):
    os.system("echo " + cmd)
''')
        
        # Scan project
        result = scanner.scan_project(str(temp_project))
        
        # Generate report
        markdown_report = scanner.generate_report(result, format='markdown')
        json_report = scanner.generate_report(result, format='json')
        
        # Check markdown report includes remediation
        assert 'Remediation:' in markdown_report
        assert result.vulnerabilities[0].remediation in markdown_report
        
        # Check JSON report includes remediation
        json_data = json.loads(json_report)
        assert all('remediation' in vuln for vuln in json_data['vulnerabilities'])
        assert all(vuln['remediation'] is not None for vuln in json_data['vulnerabilities'])
    
    def test_remediation_quality(self, scanner, temp_project):
        """Test overall quality of remediation suggestions"""
        # Create comprehensive vulnerable file
        vuln_file = temp_project / "full_app.py"
        vuln_file.write_text('''
import os
import subprocess
import hashlib
import mysql.connector

# Configuration
API_KEY = "sk-1234567890"
DB_PASSWORD = "root123"

# SQL Injection
def search_users(name):
    query = f"SELECT * FROM users WHERE name LIKE '%{name}%'"
    cursor.execute(query)

# Command Injection
def process_file(filename):
    subprocess.run(f"cat {filename}", shell=True)

# Weak Crypto
def store_password(password):
    return hashlib.sha1(password.encode()).hexdigest()

# Path Traversal
def download_file(path):
    with open(f"downloads/{path}", 'r') as f:
        return f.read()

# XXE (in comments for reference)
# DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

# XSS (in comments for JavaScript)
# document.getElementById('output').innerHTML = userInput;
''')
        
        # Scan project
        result = scanner.scan_project(str(temp_project))
        
        # Check remediation quality metrics
        remediations = [v.remediation for v in result.vulnerabilities if v.remediation]
        
        # All vulnerabilities should have remediation
        assert len(remediations) == len(result.vulnerabilities)
        
        # Remediation should be specific (not generic)
        for remediation in remediations:
            # Should be reasonably detailed
            assert len(remediation) >= 30, "Remediation too short"
            
            # Should not be placeholder text
            assert 'todo' not in remediation.lower()
            assert 'fix this' not in remediation.lower()
            
            # Should contain actionable advice
            action_words = ['use', 'replace', 'update', 'implement', 'avoid', 
                          'validate', 'sanitize', 'configure']
            assert any(word in remediation.lower() for word in action_words)


if __name__ == "__main__":
    # Run tests directly
    tester = TestRemediationSuggestions()
    scanner = SecurityScannerInteraction()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        
        print("Testing SQL injection remediation...")
        tester.test_sql_injection_remediation(scanner, temp_project)
        print("✅ SQL injection remediation passed")
        
        print("\nTesting XSS remediation...")
        tester.test_xss_remediation(scanner, temp_project)
        print("✅ XSS remediation passed")
        
        print("\nTesting hardcoded secret remediation...")
        tester.test_hardcoded_secret_remediation(scanner, temp_project)
        print("✅ Hardcoded secret remediation passed")
        
        print("\nTesting weak crypto remediation...")
        tester.test_weak_crypto_remediation(scanner, temp_project)
        print("✅ Weak crypto remediation passed")
        
        print("\nTesting command injection remediation...")
        tester.test_command_injection_remediation(scanner, temp_project)
        print("✅ Command injection remediation passed")
        
        print("\nTesting report generation with remediation...")
        tester.test_report_generation_with_remediation(scanner, temp_project)
        print("✅ Report generation passed")
        
        print("\n✅ All remediation suggestion tests passed!")