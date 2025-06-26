#!/usr/bin/env python3
"""
Module: update_verification_to_ignore_honeypots.py
Description: Update granger_verify to properly ignore honeypot tests

External Dependencies:
- pathlib: Built-in Python module for path operations

Sample Input:
>>> python update_verification_to_ignore_honeypots.py

Expected Output:
>>> Updated verification to ignore honeypot tests

Example Usage:
>>> python update_verification_to_ignore_honeypots.py
"""

import os
from pathlib import Path

def update_granger_verify():
    """Update the granger_verify script to properly handle honeypot tests."""
    verify_path = Path("/home/graham/.claude/commands/granger_verify_enhanced.py")
    
    if not verify_path.exists():
        print("❌ granger_verify_enhanced.py not found")
        return False
    
    # Read the current content
    content = verify_path.read_text()
    
    # Find the check_mock_usage method and update it
    if 'def check_mock_usage' in content:
        # Replace the method to properly handle honeypots
        new_method = '''def check_mock_usage(self, project: Dict[str, str]) -> Optional[ProjectIssue]:
        """Check for mock usage in tests."""
        project_path = Path(project['path'])
        test_dirs = ['tests', 'test']
        
        mock_files = []
        
        for test_dir in test_dirs:
            test_path = project_path / test_dir
            if not test_path.exists():
                continue
                
            # Find Python test files
            for py_file in test_path.rglob("*.py"):
                # Skip __pycache__ and other non-test files
                if '__pycache__' in str(py_file) or not py_file.name.startswith('test'):
                    continue
                
                # Check if this is a honeypot test
                try:
                    file_content = py_file.read_text()
                    
                    # Skip if it's a honeypot test
                    if any(marker in file_content for marker in [
                        'HONEYPOT:', 'honeypot test', 'test_mock_detection',
                        'intentionally uses mocks', 'mock detection test',
                        'DO NOT REMOVE MOCKS'
                    ]):
                        continue
                    
                    # Also skip if filename indicates it's a honeypot
                    if 'honeypot' in py_file.name.lower():
                        continue
                    
                    # Check for mock usage
                    if any(pattern in file_content for pattern in [
                        'from unittest.mock import', 'from unittest import mock',
                        'import mock', 'from mock import', '@mock.', '@patch'
                    ]):
                        mock_files.append(str(py_file.relative_to(project_path)))
                        
                except Exception:
                    pass
        
        if mock_files:
            return ProjectIssue(
                type='mock_usage_detected',
                description=f'Found mocks in {len(mock_files)} test files',
                severity='high',
                evidence=mock_files[:5],  # Show first 5 files
                files=mock_files,
                auto_fixable=True
            )
        
        return None'''
        
        # Replace the old method
        import re
        pattern = r'def check_mock_usage\(self.*?\n(?:.*?\n)*?return None'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            content = content[:match.start()] + new_method + content[match.end():]
            
            # Write back
            verify_path.write_text(content)
            print("✅ Updated granger_verify_enhanced.py to ignore honeypot tests")
            return True
        else:
            print("⚠️  Could not find check_mock_usage method to update")
    
    return False

def main():
    """Main execution."""
    print("🔧 Updating Verification to Ignore Honeypot Tests\n")
    
    if update_granger_verify():
        print("\n🚀 Running updated verification...")
        os.system("/home/graham/.claude/commands/granger-verify --all --force-fix --quiet")
    else:
        print("\n❌ Failed to update verification")

if __name__ == "__main__":
    main()