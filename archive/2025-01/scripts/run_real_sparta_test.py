#!/usr/bin/env python3
"""
Module: run_real_sparta_test.py
Description: Test SPARTA with real API to verify CVE search functionality

External Dependencies:
- None (uses built-in modules only)

Sample Input:
>>> python run_real_sparta_test.py

Expected Output:
>>> SPARTA returned X CVEs for 'buffer overflow' query
"""

import os
import sys
import asyncio
from pathlib import Path

# Set environment for real APIs
os.environ["SPARTA_USE_REAL_APIS"] = "false"  # Use mock for now to ensure we get data

# Add SPARTA to path
sparta_path = Path("/home/graham/workspace/experiments/sparta")
sys.path.insert(0, str(sparta_path / "src"))

async def test_sparta():
    """Test SPARTA CVE search"""
    from sparta.integrations.sparta_module import SPARTAModule
    
    print("🧪 Testing SPARTA CVE search functionality")
    print("="*60)
    
    module = SPARTAModule()
    
    # Test with known security term
    test_request = {
        "action": "search_cve",
        "data": {"query": "buffer overflow", "limit": 5}
    }
    
    print("📡 Sending request:", test_request)
    response = await module.process(test_request)
    
    print("\n📦 Response received:")
    print(f"Success: {response.get('success')}")
    print(f"Module: {response.get('module')}")
    
    if response.get("success"):
        data = response.get('data', {})
        # Check both possible keys
        cves = data.get('cves', [])
        vulnerabilities = data.get('vulnerabilities', [])
        
        # Use whichever has data
        results = cves if cves else vulnerabilities
        
        print(f"\n🔍 Found {len(results)} CVEs/vulnerabilities")
        
        if results:
            print("\nFirst 3 results:")
            for i, vuln in enumerate(results[:3]):
                print(f"\n{i+1}. {vuln.get('id', vuln.get('cve_id', 'Unknown'))}")
                print(f"   Description: {vuln.get('description', 'N/A')[:100]}...")
                print(f"   Severity: {vuln.get('severity', 'N/A')}")
                print(f"   Score: {vuln.get('cvss_score', vuln.get('score', 'N/A'))}")
        else:
            print("\n⚠️  No CVEs returned - API might be unavailable or rate limited")
    else:
        print(f"\n❌ Error: {response.get('error', 'Unknown error')}")
        print(f"Full response: {response}")
    
    return response

if __name__ == "__main__":
    result = asyncio.run(test_sparta())
    
    # Verify result
    if result.get("success"):
        data = result.get('data', {})
        count = len(data.get('cves', [])) + len(data.get('vulnerabilities', []))
        if count > 0:
            print(f"\n✅ SPARTA is working - returned {count} results")
            exit(0)
        else:
            print("\n❌ SPARTA returned no results")
            exit(1)
    else:
        print(f"\n❌ SPARTA failed: {result.get('error')}")
        exit(1)