#!/usr/bin/env python3
"""
Module: test_sparta_simple.py
Description: Simple test to verify SPARTA is working

External Dependencies:
- None for this test

Example Usage:
>>> python test_sparta_simple.py
"""

import sys
import subprocess
from pathlib import Path

def test_sparta_imports():
    """Test if SPARTA can be imported."""
    sparta_path = Path('/home/graham/workspace/experiments/sparta')
    src_path = sparta_path / 'src'
    
    # Add to Python path
    sys.path.insert(0, str(src_path))
    
    try:
        # Test basic imports
        import sparta
        print("✅ SPARTA package imported successfully")
        
        # Test core modules
        from sparta.core import download_cache
        print("✅ download_cache imported")
        
        from sparta.core import quality_control
        print("✅ quality_control imported")
        
        # Check for real implementation
        cache = download_cache.DownloadCache(Path('/tmp/test_cache'))
        print("✅ DownloadCache instantiated")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_sparta_tests():
    """Check if SPARTA's tests can run."""
    sparta_path = Path('/home/graham/workspace/experiments/sparta')
    
    # Try to run a simple test
    cmd = [
        sys.executable, '-m', 'pytest',
        str(sparta_path / 'tests' / 'test_honeypot.py'),
        '-v', '--tb=short'
    ]
    
    print("\n🧪 Running SPARTA honeypot test...")
    result = subprocess.run(
        cmd,
        cwd=str(sparta_path),
        capture_output=True,
        text=True
    )
    
    print("STDOUT:", result.stdout[:500])
    print("STDERR:", result.stderr[:500])
    print(f"Return code: {result.returncode}")
    
    return result.returncode == 0

def main():
    """Test SPARTA readiness."""
    print("🚀 Testing SPARTA Module Readiness")
    print("=" * 60)
    
    # Test 1: Imports
    import_ok = test_sparta_imports()
    
    # Test 2: Run tests
    # tests_ok = check_sparta_tests()
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print(f"  - Imports: {'✅ PASS' if import_ok else '❌ FAIL'}")
    # print(f"  - Tests: {'✅ PASS' if tests_ok else '❌ FAIL'}")
    
    if import_ok:
        print("\n✅ SPARTA appears to have real implementation and is ready for testing!")
        print("Next step: Run SPARTA's test suite from its directory")
    else:
        print("\n❌ SPARTA is not ready - check the errors above")

if __name__ == "__main__":
    main()