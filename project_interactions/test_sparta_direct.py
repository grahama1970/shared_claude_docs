#!/usr/bin/env python3
"""
Module: test_sparta_direct.py
Description: Direct test of SPARTA module without assumptions about structure

External Dependencies:
- sparta module from experiments

Sample Input:
>>> python test_sparta_direct.py

Expected Output:
>>> SPARTA module structure and available functions
"""

import sys
from pathlib import Path

# Add SPARTA to path
sparta_path = Path("/home/graham/workspace/experiments/sparta/src")
sys.path.insert(0, str(sparta_path))

print("Attempting to import SPARTA module...")

try:
    import sparta
    print(f"✅ Successfully imported sparta: {sparta}")
    print(f"   Location: {sparta.__file__}")
    print(f"   Available attributes: {dir(sparta)}")
    
    # Try to find integration modules
    if hasattr(sparta, 'integrations'):
        print("\n✅ Found integrations submodule")
        from sparta import integrations
        print(f"   Available integrations: {dir(integrations)}")
        
        # Try to import SPARTAModule
        if hasattr(integrations, 'sparta_module'):
            from sparta.integrations.sparta_module import SPARTAModule
            print("\n✅ Successfully imported SPARTAModule")
            
            # Try to create instance
            module = SPARTAModule()
            print(f"   Created instance: {module}")
            
            # Check methods
            print(f"   Available methods: {[m for m in dir(module) if not m.startswith('_')]}")
            
            # Try a simple test
            import asyncio
            
            async def test_module():
                result = await module.process({
                    "action": "search_cve",
                    "data": {"query": "test", "limit": 1}
                })
                return result
            
            print("\n🧪 Testing module with real API call...")
            result = asyncio.run(test_module())
            print(f"   Result: {result}")
            
    else:
        print("❌ No integrations submodule found")
        
        # Try direct imports
        print("\nTrying direct imports...")
        from sparta.integrations.sparta_module import SPARTAModule
        print("✅ Direct import successful")
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
    
    # Show what's actually available
    print("\nChecking file system...")
    sparta_src = Path("/home/graham/workspace/experiments/sparta/src/sparta")
    if sparta_src.exists():
        print(f"✅ SPARTA source directory exists: {sparta_src}")
        print("   Contents:")
        for item in sparta_src.iterdir():
            if item.is_dir():
                print(f"   📁 {item.name}/")
            else:
                print(f"   📄 {item.name}")
                
        # Check integrations
        integrations_dir = sparta_src / "integrations"
        if integrations_dir.exists():
            print(f"\n   Integrations directory contents:")
            for item in integrations_dir.iterdir():
                print(f"     📄 {item.name}")
    else:
        print(f"❌ SPARTA source directory not found: {sparta_src}")

except Exception as e:
    print(f"❌ Unexpected error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("Test complete")

# Now check if the module needs dependencies installed
print("\nChecking SPARTA dependencies...")
try:
    pyproject_path = Path("/home/graham/workspace/experiments/sparta/pyproject.toml")
    if pyproject_path.exists():
        print(f"✅ Found pyproject.toml")
        # Could parse and check dependencies here
    else:
        print("❌ No pyproject.toml found")
except Exception as e:
    print(f"❌ Error checking dependencies: {e}")