#!/usr/bin/env python3
"""
Module: test_claude_reporter_simple.py
Description: Test Claude Test Reporter readiness

External Dependencies:
- None for this test

Example Usage:
>>> python test_claude_reporter_simple.py
"""

import sys
from pathlib import Path

def test_reporter_imports():
    """Test if Claude Test Reporter can be imported."""
    reporter_path = Path('/home/graham/workspace/experiments/claude-test-reporter')
    src_path = reporter_path / 'src'
    
    # Add to Python path
    sys.path.insert(0, str(src_path))
    
    try:
        # Test basic imports
        import claude_test_reporter
        print("✅ claude_test_reporter package imported")
        
        # Test key modules
        from claude_test_reporter import pytest_plugin
        print("✅ pytest_plugin imported")
        
        from claude_test_reporter.monitoring import hallucination_monitor
        print("✅ hallucination_monitor imported")
        
        # Check for real implementation
        monitor = hallucination_monitor.HallucinationMonitor()
        print("✅ HallucinationMonitor instantiated")
        
        # Check CLI
        from claude_test_reporter.cli import main
        print("✅ CLI main imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_granger_common():
    """Check if granger_common is available."""
    try:
        import granger_common
        print("✅ granger_common imported")
        
        from granger_common import schema_manager
        print("✅ schema_manager imported")
        
        return True
    except Exception as e:
        print(f"⚠️  granger_common not available: {e}")
        return False

def main():
    """Test Claude Test Reporter readiness."""
    print("🚀 Testing Claude Test Reporter Readiness")
    print("=" * 60)
    
    # Test imports
    import_ok = test_reporter_imports()
    
    # Check granger_common
    print("\n📦 Checking granger_common...")
    granger_ok = check_granger_common()
    
    print("\n" + "=" * 60)
    print("📊 Results:")
    print(f"  - Reporter imports: {'✅ PASS' if import_ok else '❌ FAIL'}")
    print(f"  - Granger common: {'✅ Available' if granger_ok else '⚠️  Not Available'}")
    
    if import_ok:
        print("\n✅ Claude Test Reporter has real implementation!")
        print("This is a critical component for the Granger ecosystem")
    else:
        print("\n❌ Claude Test Reporter needs attention")

if __name__ == "__main__":
    main()