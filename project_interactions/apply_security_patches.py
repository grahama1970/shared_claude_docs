#!/usr/bin/env python3
"""
Module: apply_security_patches.py
Description: Apply security patches to all Granger modules to fix SQL injection and authentication vulnerabilities

Example Usage:
>>> python apply_security_patches.py
Patching all modules with security fixes...
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
import shutil
from datetime import datetime

# Security middleware code to inject
SECURITY_IMPORT = """
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()
"""

SECURE_ENDPOINT_WRAPPER = """
def secure_endpoint(func):
    \"\"\"Security wrapper for endpoints\"\"\"
    def wrapper(*args, **kwargs):
        # Extract request
        request = kwargs.get('request', {})
        if args and isinstance(args[0], dict) and 'token' in args[0]:
            request = args[0]
        
        # Validate request
        validation = _security.validate_request(request)
        if not validation['valid']:
            raise ValueError(f"Security validation failed: {validation['errors']}")
        
        # Use sanitized inputs
        if args and isinstance(args[0], dict):
            args = (validation['sanitized'],) + args[1:]
        elif 'request' in kwargs:
            kwargs['request'] = validation['sanitized']
            
        return func(*args, **kwargs)
    return wrapper
"""

class SecurityPatcher:
    """Apply security patches to Python files"""
    
    def __init__(self):
        self.patches_applied = []
        self.errors = []
        
    def patch_file(self, filepath: Path) -> bool:
        """Apply security patches to a single file"""
        try:
            content = filepath.read_text()
            original_content = content
            
            # Skip if already patched
            if "granger_security_middleware" in content:
                print(f"✓ {filepath.name} already patched")
                return True
            
            # Apply patches based on patterns found
            content = self._patch_authentication(content)
            content = self._patch_sql_queries(content)
            content = self._patch_error_handling(content)
            content = self._add_security_import(content)
            
            # Only write if changes were made
            if content != original_content:
                # Backup original
                backup_path = filepath.with_suffix(filepath.suffix + '.backup')
                shutil.copy2(filepath, backup_path)
                
                # Write patched content
                filepath.write_text(content)
                self.patches_applied.append(str(filepath))
                print(f"✅ Patched {filepath.name}")
                return True
            else:
                print(f"ℹ️  No changes needed for {filepath.name}")
                return True
                
        except Exception as e:
            self.errors.append(f"{filepath}: {str(e)}")
            print(f"❌ Error patching {filepath.name}: {e}")
            return False
    
    def _add_security_import(self, content: str) -> str:
        """Add security import at the top of the file"""
        # Find the right place to insert (after existing imports)
        import_section_end = 0
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith(('import ', 'from ', '#')):
                import_section_end = i
                break
        
        # Insert security import
        lines.insert(import_section_end, SECURITY_IMPORT)
        return '\n'.join(lines)
    
    def _patch_authentication(self, content: str) -> str:
        """Fix authentication vulnerabilities"""
        # Pattern 1: Empty token checks
        content = re.sub(
            r'if\s+not\s+token\s*:',
            'if not token or token.strip() == "":',
            content
        )
        
        # Pattern 2: Weak token validation
        content = re.sub(
            r'token\s*==\s*["\'][\s]*["\']',
            'False',  # Never accept empty tokens
            content
        )
        
        # Pattern 3: Add validation to token checks
        content = re.sub(
            r'if\s+token\s*==\s*["\']([^"\']+)["\']:',
            r'if _security.token_validator.validate_token(token)[0]:',
            content
        )
        
        return content
    
    def _patch_sql_queries(self, content: str) -> str:
        """Fix SQL injection vulnerabilities"""
        # Pattern 1: String formatting in queries
        content = re.sub(
            r'f["\']([^"\']*SELECT[^"\']*){([^}]+)}([^"\']*)["\']',
            r'_security.sql_protector.sanitize_input(f"\1{\2}\3")',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 2: Direct concatenation
        content = re.sub(
            r'["\']SELECT\s+\*\s+FROM\s+\w+\s+WHERE\s+\w+\s*=\s*["\'\s]*\+\s*(\w+)',
            r'"SELECT * FROM table WHERE column = " + _security.sql_protector.sanitize_input(\1)',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 3: Format method
        content = re.sub(
            r'\.format\(([^)]+)\)[\s]*#[\s]*SQL',
            r'.format(_security.sql_protector.sanitize_input(\1))',
            content
        )
        
        return content
    
    def _patch_error_handling(self, content: str) -> str:
        """Remove stack traces from error messages"""
        # Pattern 1: Direct exception returns
        content = re.sub(
            r'return\s+[{"]error[":]?\s*:\s*str\(e\)[}"]',
            r'return {"error": _security.remove_stack_traces(str(e))}',
            content
        )
        
        # Pattern 2: Exception in response
        content = re.sub(
            r'["\']error["\']:\s*f?["\']({[^}]*})?{str\(e\)}',
            r'"error": _security.remove_stack_traces(str(e))',
            content
        )
        
        # Pattern 3: Traceback imports
        if 'import traceback' in content:
            content = re.sub(
                r'traceback\.format_exc\(\)',
                r'_security.remove_stack_traces(traceback.format_exc())',
                content
            )
        
        return content
    
    def apply_patches_to_directory(self, directory: Path, patterns: List[str] = None) -> Dict:
        """Apply patches to all Python files in directory"""
        if patterns is None:
            patterns = ['*.py']
        
        results = {
            'total_files': 0,
            'patched': 0,
            'already_patched': 0,
            'errors': 0
        }
        
        for pattern in patterns:
            for filepath in directory.rglob(pattern):
                # Skip test files and backups
                if any(skip in str(filepath) for skip in ['test_', '.backup', '__pycache__']):
                    continue
                
                results['total_files'] += 1
                
                if self.patch_file(filepath):
                    if str(filepath) in self.patches_applied:
                        results['patched'] += 1
                    else:
                        results['already_patched'] += 1
                else:
                    results['errors'] += 1
        
        return results


def patch_specific_modules():
    """Patch specific vulnerable modules identified in bug hunt"""
    vulnerable_modules = {
        'arangodb': [
            '/home/graham/workspace/experiments/arangodb/src/arangodb/auth.py',
            '/home/graham/workspace/experiments/arangodb/src/arangodb/client.py',
        ],
        'marker': [
            '/home/graham/workspace/experiments/marker/src/marker/api.py',
            '/home/graham/workspace/experiments/marker/src/marker/processor.py',
        ],
        'sparta': [
            '/home/graham/workspace/experiments/sparta/src/sparta/handlers.py',
            '/home/graham/workspace/experiments/sparta/src/sparta/api.py',
        ],
        'llm_call': [
            '/home/graham/workspace/experiments/llm_call/src/llm_call/auth.py',
        ]
    }
    
    patcher = SecurityPatcher()
    
    for module, files in vulnerable_modules.items():
        print(f"\n🔧 Patching {module} module...")
        for filepath in files:
            path = Path(filepath)
            if path.exists():
                patcher.patch_file(path)
            else:
                print(f"⚠️  File not found: {filepath}")
    
    return patcher


def create_security_test_suite():
    """Create regression tests for security fixes"""
    test_content = '''#!/usr/bin/env python3
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
        error = 'File "/home/user/secret/path.py", line 42\\nSecretError'
        cleaned = self.security.remove_stack_traces(error)
        
        assert "/home/user" not in cleaned
        assert "line 42" not in cleaned
        assert "secret" not in cleaned.lower()

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''
    
    test_path = Path("test_security_patches.py")
    test_path.write_text(test_content)
    print(f"\n📝 Created security test suite: {test_path}")


def main():
    """Main execution"""
    print("🔒 Granger Security Patch Application")
    print("=" * 60)
    
    # First, copy security middleware to all module directories
    middleware_source = Path("granger_security_middleware_simple.py")
    
    if not middleware_source.exists():
        print("❌ Security middleware not found!")
        return 1
    
    target_dirs = [
        "/home/graham/workspace/experiments/arangodb/src",
        "/home/graham/workspace/experiments/marker/src",
        "/home/graham/workspace/experiments/sparta/src",
        "/home/graham/workspace/experiments/llm_call/src",
        "/home/graham/workspace/shared_claude_docs/project_interactions"
    ]
    
    print("\n📦 Distributing security middleware...")
    for target_dir in target_dirs:
        target_path = Path(target_dir)
        if target_path.exists():
            dest = target_path / middleware_source.name
            if not dest.exists() or dest.resolve() != middleware_source.resolve():
                shutil.copy2(middleware_source, dest)
                print(f"✅ Copied to {target_dir}")
            else:
                print(f"✓ Already exists in {target_dir}")
    
    # Apply patches
    print("\n🔧 Applying security patches...")
    patcher = patch_specific_modules()
    
    # Patch project_interactions directory
    print("\n🔧 Patching project_interactions...")
    pi_results = patcher.apply_patches_to_directory(
        Path("/home/graham/workspace/shared_claude_docs/project_interactions")
    )
    
    # Create test suite
    create_security_test_suite()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Security Patch Summary")
    print("=" * 60)
    print(f"Files patched: {len(patcher.patches_applied)}")
    print(f"Errors: {len(patcher.errors)}")
    
    if patcher.patches_applied:
        print("\n✅ Successfully patched:")
        for file in patcher.patches_applied[:10]:  # Show first 10
            print(f"  - {Path(file).name}")
    
    if patcher.errors:
        print("\n❌ Errors encountered:")
        for error in patcher.errors[:5]:  # Show first 5
            print(f"  - {error}")
    
    print("\n🎯 Next steps:")
    print("1. Run security test suite: pytest test_security_patches.py")
    print("2. Re-run bug hunter to verify fixes")
    print("3. Deploy to staging for integration testing")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())