#!/usr/bin/env python3
"""
Module: test_sparta_arangodb_integration.py
Description: Real integration test for SPARTA -> ArangoDB data flow

External Dependencies:
- None
"""

import sys
import asyncio
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/sparta/src")))
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/arangodb/src")))

async def test_sparta_to_arangodb():
    """Test real data flow from SPARTA to ArangoDB"""
    print("\n🧪 Testing SPARTA -> ArangoDB Integration...")
    
    try:
        # Import modules
        from sparta.integrations.sparta_module import SPARTAModule
        from arangodb.handlers import ArangoDBModule
        
        # Initialize modules
        sparta = SPARTAModule()
        arangodb = ArangoDBModule()
        
        # Step 1: Search for CVEs
        print("  📡 Searching for CVEs...")
        cve_request = {
            "action": "search_cve",
            "data": {"query": "log4j", "limit": 5}
        }
        
        cve_result = await sparta.process(cve_request)
        
        if not cve_result.get("success"):
            print(f"  ❌ CVE search failed: {cve_result.get('error')}")
            return False
        
        cve_data = cve_result.get("data", {})
        print(f"  ✅ Found {len(cve_data.get('cves', []))} CVEs")
        
        # Step 2: Store in ArangoDB
        print("  💾 Storing in ArangoDB...")
        doc_id = await arangodb.store({
            "type": "cve_data",
            "source": "sparta",
            "data": cve_data,
            "timestamp": datetime.now().isoformat()
        })
        
        print(f"  ✅ Stored with ID: {doc_id}")
        
        # Step 3: Retrieve and verify
        print("  🔍 Retrieving from ArangoDB...")
        retrieved = await arangodb.get(doc_id)
        
        if retrieved.get("data", {}).get("cves") == cve_data.get("cves"):
            print("  ✅ Data integrity verified!")
            return True
        else:
            print("  ❌ Data mismatch!")
            return False
            
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

from datetime import datetime

if __name__ == "__main__":
    result = asyncio.run(test_sparta_to_arangodb())
    print(f"\n{'='*60}")
    print(f"Test Result: {'PASS' if result else 'FAIL'}")
    print(f"{'='*60}")
    exit(0 if result else 1)
