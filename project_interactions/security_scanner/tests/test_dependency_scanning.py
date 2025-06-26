"""
Test dependency vulnerability scanning

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
    Severity
)


class TestDependencyScanning:
    """Test dependency vulnerability scanning capabilities"""
    
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
    
    def test_python_requirements_scanning(self, scanner, temp_project):
        """Test scanning Python requirements.txt"""
        # Create requirements.txt with vulnerable packages
        req_file = temp_project / "requirements.txt"
        req_file.write_text("""
# Web framework
django==1.11.0
flask==0.12.0

# Utilities
requests==2.18.0
pyyaml==3.13
urllib3==1.24.0

# Good versions
cryptography==41.0.0
numpy==1.24.0
""")
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Check for vulnerable dependencies
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        assert len(dep_vulns) >= 4, f"Expected at least 4 vulnerable dependencies, found {len(dep_vulns)}"
        
        # Check specific vulnerabilities
        vuln_packages = {v.description.lower() for v in dep_vulns}
        assert any('django' in pkg for pkg in vuln_packages)
        assert any('flask' in pkg for pkg in vuln_packages)
        assert any('requests' in pkg for pkg in vuln_packages)
        assert any('pyyaml' in pkg for pkg in vuln_packages)
        
        # All should have CVE IDs
        for vuln in dep_vulns:
            assert vuln.cve_id is not None
            assert vuln.cve_id.startswith('CVE-')
            assert vuln.remediation is not None
    
    def test_pyproject_toml_scanning(self, scanner, temp_project):
        """Test scanning pyproject.toml dependencies"""
        # Create pyproject.toml with dependencies
        pyproject_file = temp_project / "pyproject.toml"
        pyproject_file.write_text("""
[project]
name = "test-project"
dependencies = [
    "django<2.2",
    "flask<0.12.3",
    "requests<2.20.0",
    "pyyaml<5.4",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "black",
]
""")
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Check for vulnerable dependencies
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        assert len(dep_vulns) >= 4, f"Expected at least 4 vulnerable dependencies"
        
        # Verify pyproject.toml is being scanned
        assert any('pyproject.toml' in v.file_path for v in dep_vulns)
    
    def test_npm_package_json_scanning(self, scanner, temp_project):
        """Test scanning NPM package.json"""
        # Create package.json with vulnerable packages
        package_file = temp_project / "package.json"
        package_file.write_text(json.dumps({
            "name": "test-app",
            "version": "1.0.0",
            "dependencies": {
                "lodash": "4.17.15",
                "minimist": "1.2.0",
                "express": "4.16.0",
                "axios": "0.18.0"
            },
            "devDependencies": {
                "jest": "^29.0.0",
                "eslint": "^8.0.0"
            }
        }, indent=2))
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Check for vulnerable NPM packages
        npm_vulns = [v for v in result.vulnerabilities 
                     if 'package.json' in v.file_path]
        
        assert len(npm_vulns) >= 2, f"Expected at least 2 vulnerable NPM packages"
        
        # Check specific packages
        vuln_packages = {v.description.lower() for v in npm_vulns}
        assert any('lodash' in pkg for pkg in vuln_packages)
        assert any('minimist' in pkg for pkg in vuln_packages)
    
    def test_mixed_project_scanning(self, scanner, temp_project):
        """Test scanning project with multiple dependency files"""
        # Create Python requirements
        (temp_project / "requirements.txt").write_text("""
django==1.11.0
requests==2.18.0
""")
        
        # Create package.json
        (temp_project / "package.json").write_text(json.dumps({
            "dependencies": {
                "lodash": "4.17.15",
                "jquery": "3.3.0"
            }
        }))
        
        # Create some source files too
        (temp_project / "app.py").write_text('''
password = "hardcoded123"
eval(user_input)
''')
        
        # Scan everything
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Should find both dependency and code vulnerabilities
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        code_vulns = [v for v in result.vulnerabilities 
                     if v.type != VulnerabilityType.KNOWN_VULNERABILITIES]
        
        assert len(dep_vulns) >= 3, "Should find dependency vulnerabilities"
        assert len(code_vulns) >= 2, "Should find code vulnerabilities"
        
        # Check both Python and NPM vulnerabilities found
        assert any('requirements.txt' in v.file_path for v in dep_vulns)
        assert any('package.json' in v.file_path for v in dep_vulns)
    
    def test_no_dependencies_scan(self, scanner, temp_project):
        """Test scanning with no dependency files"""
        # Create only source files
        (temp_project / "main.py").write_text('''
def hello():
    return "Hello, World!"
''')
        
        # Scan without dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=False)
        
        # Should not have dependency vulnerabilities
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        assert len(dep_vulns) == 0, "Should not find dependency vulnerabilities"
    
    def test_dependency_remediation_suggestions(self, scanner, temp_project):
        """Test that remediation suggestions are provided"""
        # Create requirements with vulnerable packages
        req_file = temp_project / "requirements.txt"
        req_file.write_text("""
django==1.11.0
flask==0.12.0
requests==2.18.0
""")
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Check remediation suggestions
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        for vuln in dep_vulns:
            assert vuln.remediation is not None
            assert 'update' in vuln.remediation.lower() or 'upgrade' in vuln.remediation.lower()
            assert 'version' in vuln.remediation.lower()
    
    def test_transitive_dependencies(self, scanner, temp_project):
        """Test handling of transitive dependencies"""
        # Create requirements with packages that have vulnerable transitive deps
        req_file = temp_project / "requirements.txt"
        req_file.write_text("""
# This might have vulnerable transitive dependencies
django==1.11.0
# Pinned transitive dependency
urllib3==1.24.0
""")
        
        # Note: In a real implementation, you would check lock files
        # (requirements-lock.txt, poetry.lock, etc.) for transitive deps
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Should detect direct dependencies at minimum
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        assert len(dep_vulns) >= 1, "Should detect vulnerable dependencies"
    
    def test_severity_levels(self, scanner, temp_project):
        """Test that dependency vulnerabilities have appropriate severity"""
        # Create requirements with various vulnerable packages
        req_file = temp_project / "requirements.txt"
        req_file.write_text("""
# Critical vulnerabilities
django==1.11.0
pyyaml==3.13

# High severity
requests==2.18.0
flask==0.12.0

# Medium severity (hypothetical)
some-package==1.0.0
""")
        
        # Scan dependencies
        result = scanner.scan_project(str(temp_project), scan_dependencies=True)
        
        # Check severity distribution
        dep_vulns = [v for v in result.vulnerabilities 
                     if v.type == VulnerabilityType.KNOWN_VULNERABILITIES]
        
        severities = [v.severity for v in dep_vulns]
        
        # Should have high severity vulnerabilities
        assert any(s == Severity.HIGH for s in severities)
        
        # All known vulnerabilities should be at least medium
        assert all(s in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM] 
                  for s in severities)


if __name__ == "__main__":
    # Run tests directly
    tester = TestDependencyScanning()
    scanner = SecurityScannerInteraction()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        
        print("Testing Python requirements scanning...")
        tester.test_python_requirements_scanning(scanner, temp_project)
        print("✅ Python requirements scanning passed")
        
        print("\nTesting pyproject.toml scanning...")
        tester.test_pyproject_toml_scanning(scanner, temp_project)
        print("✅ pyproject.toml scanning passed")
        
        print("\nTesting NPM package.json scanning...")
        tester.test_npm_package_json_scanning(scanner, temp_project)
        print("✅ NPM package.json scanning passed")
        
        print("\nTesting mixed project scanning...")
        tester.test_mixed_project_scanning(scanner, temp_project)
        print("✅ Mixed project scanning passed")
        
        print("\nTesting remediation suggestions...")
        tester.test_dependency_remediation_suggestions(scanner, temp_project)
        print("✅ Remediation suggestions passed")
        
        print("\n✅ All dependency scanning tests passed!")