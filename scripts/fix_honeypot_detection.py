#!/usr/bin/env python3
"""
Module: fix_honeypot_detection.py
Description: Update granger_verify.py to properly ignore honeypot tests when checking for mocks

External Dependencies:
- pathlib: Built-in Python module for path operations

Sample Input:
>>> python fix_honeypot_detection.py

Expected Output:
>>> ✅ Updated granger_verify.py to ignore honeypot tests
>>> 🚀 Running updated verification...

Example Usage:
>>> python fix_honeypot_detection.py
"""

import os
import re
from pathlib import Path

def update_mock_detection():
    """Update the mock detection logic to ignore honeypot tests."""
    verify_path = Path("/home/graham/.claude/commands/granger_verify.py")
    
    if not verify_path.exists():
        print("❌ granger_verify.py not found")
        return False
    
    # Read the current content
    content = verify_path.read_text()
    
    # Find the mock detection section
    # Look for the pattern where mock files are checked
    pattern = r"(for test_file in tests_dir\.rglob\('test_\*\.py'\):\s*try:\s*content = test_file\.read_text\(\)\s*mock_patterns = \[.*?\]\s*if any\(pattern in content for pattern in mock_patterns\):)"
    
    replacement = '''for test_file in tests_dir.rglob('test_*.py'):
            try:
                content = test_file.read_text()
                
                # Skip honeypot tests
                honeypot_markers = [
                    'HONEYPOT:', 'honeypot test', 'test_mock_detection',
                    'intentionally uses mocks', 'mock detection test',
                    'DO NOT REMOVE MOCKS', 'Honeypot tests', 
                    'honeypot_tests', 'test_honeypot'
                ]
                
                # Check if this is a honeypot test (by content or filename)
                is_honeypot = any(marker in content for marker in honeypot_markers)
                is_honeypot = is_honeypot or 'honeypot' in test_file.name.lower()
                is_honeypot = is_honeypot or 'honeypot' in str(test_file).lower()
                
                if is_honeypot:
                    continue  # Skip honeypot tests
                
                mock_patterns = ['@mock', '@patch', 'Mock(', 'MagicMock', 'monkeypatch']
                
                if any(pattern in content for pattern in mock_patterns):'''
    
    # Search and replace
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Write back
        verify_path.write_text(content)
        print("✅ Updated granger_verify.py to ignore honeypot tests")
        return True
    else:
        print("⚠️  Could not find mock detection pattern to update")
        print("Attempting alternative approach...")
        
        # Try a simpler pattern
        simple_pattern = r"if any\(pattern in content for pattern in mock_patterns\):"
        simple_replacement = '''# Skip honeypot tests
                honeypot_markers = [
                    'HONEYPOT:', 'honeypot test', 'test_mock_detection',
                    'intentionally uses mocks', 'mock detection test',
                    'DO NOT REMOVE MOCKS', 'Honeypot tests', 
                    'honeypot_tests', 'test_honeypot'
                ]
                
                # Check if this is a honeypot test
                is_honeypot = any(marker in content for marker in honeypot_markers)
                is_honeypot = is_honeypot or 'honeypot' in test_file.name.lower()
                
                if not is_honeypot and any(pattern in content for pattern in mock_patterns):'''
        
        if simple_pattern in content:
            content = content.replace(simple_pattern, simple_replacement)
            verify_path.write_text(content)
            print("✅ Updated granger_verify.py using alternative method")
            return True
    
    return False

def main():
    """Main execution."""
    print("🔧 Updating Mock Detection to Ignore Honeypot Tests\n")
    
    if update_mock_detection():
        print("\n🚀 Running updated verification...")
        os.system("/home/graham/.claude/commands/granger-verify --all --force-fix --quiet")
    else:
        print("\n❌ Failed to update mock detection")
        print("\nManual fix required:")
        print("Edit /home/graham/.claude/commands/granger_verify.py")
        print("Find the mock detection loop and add honeypot detection logic")

if __name__ == "__main__":
    main()