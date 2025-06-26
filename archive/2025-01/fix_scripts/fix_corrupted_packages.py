#!/usr/bin/env python3
"""
Module: fix_corrupted_packages.py
Description: Find and reinstall corrupted Python packages

External Dependencies:
- subprocess: https://docs.python.org/3/library/subprocess.html
- pathlib: https://docs.python.org/3/library/pathlib.html

Sample Input:
>>> fixer = CorruptedPackageFixer()
>>> fixer.fix_all()

Expected Output:
>>> Finds packages with syntax errors
>>> Reinstalls them using uv
"""

import subprocess
import sys
from pathlib import Path
import re


class CorruptedPackageFixer:
    """Find and fix corrupted packages in the virtual environment"""
    
    def __init__(self):
        self.site_packages = Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        self.corrupted_packages = set()
        self.fixed_packages = []
        
    def find_corrupted_packages(self):
        """Find all packages with syntax errors"""
        print("🔍 Scanning for corrupted packages...")
        
        # Common patterns that indicate corruption
        corruption_patterns = [
            r'if\s+\w+\s*==\s*"\("\s*"\)"?\s*:',  # if var == "("):
            r'elif\s+\w+\s*==\s*"\("\s*"\)"?\s*:',  # elif var == "("):
            r'stream\.consume\(\'\(\'\)\)',  # stream.consume('('))
        ]
        
        for py_file in self.site_packages.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                
                # Check for unmatched parentheses patterns
                for pattern in corruption_patterns:
                    if re.search(pattern, content):
                        # Find the package name
                        relative_path = py_file.relative_to(self.site_packages)
                        package_name = str(relative_path).split('/')[0].split('-')[0]
                        
                        if '.' not in package_name and package_name not in ['__pycache__', '_distutils_hack']:
                            self.corrupted_packages.add(package_name)
                            print(f"  ❌ Found corruption in {package_name}: {py_file}")
                            
            except Exception as e:
                # Skip files we can't read
                pass
                
    def fix_package(self, package_name):
        """Reinstall a corrupted package"""
        print(f"\n🔧 Fixing {package_name}...")
        
        try:
            # Uninstall
            result = subprocess.run(
                ["uv", "pip", "uninstall", package_name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Reinstall
                result = subprocess.run(
                    ["uv", "pip", "install", package_name],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"  ✅ Successfully reinstalled {package_name}")
                    self.fixed_packages.append(package_name)
                    return True
                else:
                    print(f"  ❌ Failed to reinstall {package_name}: {result.stderr}")
            else:
                print(f"  ❌ Failed to uninstall {package_name}: {result.stderr}")
                
        except Exception as e:
            print(f"  ❌ Error fixing {package_name}: {e}")
            
        return False
        
    def fix_all(self):
        """Find and fix all corrupted packages"""
        print("🔨 Corrupted Package Fixer")
        print("=" * 60)
        
        # Find corrupted packages
        self.find_corrupted_packages()
        
        if not self.corrupted_packages:
            print("\n✅ No corrupted packages found!")
            return
            
        print(f"\n📦 Found {len(self.corrupted_packages)} corrupted packages:")
        for pkg in sorted(self.corrupted_packages):
            print(f"  - {pkg}")
            
        # Fix each package
        print("\n🔧 Fixing packages...")
        for package in sorted(self.corrupted_packages):
            self.fix_package(package)
            
        # Summary
        print(f"\n📊 Summary:")
        print(f"  - Packages found: {len(self.corrupted_packages)}")
        print(f"  - Packages fixed: {len(self.fixed_packages)}")
        
        if self.fixed_packages:
            print("\n✅ Fixed packages:")
            for pkg in sorted(self.fixed_packages):
                print(f"  - {pkg}")
                
        failed = self.corrupted_packages - set(self.fixed_packages)
        if failed:
            print("\n❌ Failed to fix:")
            for pkg in sorted(failed):
                print(f"  - {pkg}")


if __name__ == "__main__":
    fixer = CorruptedPackageFixer()
    fixer.fix_all()
    
    print("\n🎯 Next: Run granger-verify --test again")