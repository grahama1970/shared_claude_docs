#!/usr/bin/env python3
"""
Module: task_002_sparta_cve.py
Description: Task #002 - Quick CVE Check (SPARTA) Bug Hunter Test

External Dependencies:
- sparta: GRANGER cybersecurity module

Sample Input:
>>> test_sparta_cve_retrieval()

Expected Output:
>>> Valid CVE: Success/failure with timing
>>> Non-existent CVE: Proper error handling
>>> Malformed CVE: Input validation

Example Usage:
>>> python task_002_sparta_cve.py
"""

import sys
import time
import asyncio
from typing import Dict, Any, Optional
import json

# First check if sparta is available
try:
    sys.path.insert(0, '/home/graham/workspace/experiments/sparta/src')
    from sparta.core.cve_enrichment import get_cve_details
    from sparta.api.endpoints import cve_endpoint
    SPARTA_AVAILABLE = True
    print("✅ SPARTA module imported successfully")
except ImportError as e:
    print(f"⚠️ SPARTA import failed: {e}")
    # Try alternate import
    try:
        from sparta import get_cve_details
        SPARTA_AVAILABLE = True
        print("✅ SPARTA module imported via alternate path")
    except Exception as e2:
        SPARTA_AVAILABLE = False
        print(f"❌ SPARTA module unavailable: {e2}")
        

def test_cve_retrieval(cve_id: str) -> Dict[str, Any]:
    """Test CVE retrieval with timing and validation"""
    start_time = time.time()
    result = {
        "cve_id": cve_id,
        "success": False,
        "duration": 0,
        "data": None,
        "error": None,
        "bug_found": None
    }
    
    try:
        # Direct module test
        cve_data = get_cve_details(cve_id)
        duration = time.time() - start_time
        
        result["duration"] = duration
        result["success"] = True
        result["data"] = cve_data
        
        # Validation checks
        if cve_data:
            # Check required fields
            required_fields = ['id', 'description', 'severity']
            missing_fields = [f for f in required_fields if f not in cve_data]
            
            if missing_fields:
                result["bug_found"] = f"Missing required fields: {missing_fields}"
            
            # Performance check
            if duration > 5.0:
                result["bug_found"] = f"Performance issue: {duration:.2f}s (>5s threshold)"
                
        else:
            result["bug_found"] = "Empty response for valid CVE"
            
    except Exception as e:
        result["duration"] = time.time() - start_time
        result["error"] = str(e)
        result["bug_found"] = f"Exception: {type(e).__name__}"
        
    return result


async def test_concurrent_requests(cve_ids: list) -> list:
    """Test concurrent CVE lookups for rate limiting"""
    tasks = []
    
    for cve_id in cve_ids:
        task = asyncio.create_task(
            asyncio.to_thread(test_cve_retrieval, cve_id)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


def run_sparta_bug_hunt():
    """Run comprehensive SPARTA CVE bug hunting tests"""
    print("\n" + "="*60)
    print("🐛 TASK #002: SPARTA CVE Bug Hunter")
    print("="*60)
    
    if not SPARTA_AVAILABLE:
        print("❌ Cannot run tests - SPARTA module not available")
        return {
            "task": "002_sparta_cve",
            "status": "blocked",
            "reason": "Module import failure",
            "bugs_found": ["SPARTA module cannot be imported"]
        }
    
    bugs_found = []
    test_results = []
    
    # Test 1: Valid CVE
    print("\n📋 Test 1: Valid CVE lookup")
    result = test_cve_retrieval("CVE-2024-12345")
    test_results.append(result)
    print(f"  Duration: {result['duration']:.3f}s")
    print(f"  Success: {result['success']}")
    if result['bug_found']:
        bugs_found.append(result['bug_found'])
        print(f"  🐛 BUG: {result['bug_found']}")
    
    # Test 2: Non-existent CVE
    print("\n📋 Test 2: Non-existent CVE")
    result = test_cve_retrieval("CVE-9999-99999")
    test_results.append(result)
    print(f"  Duration: {result['duration']:.3f}s")
    print(f"  Success: {result['success']}")
    if not result['error']:
        bug = "Non-existent CVE returned success instead of error"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Test 3: Malformed CVE
    print("\n📋 Test 3: Malformed CVE format")
    malformed_tests = [
        "CVE-INVALID-FORMAT",
        "'; DROP TABLE vulnerabilities; --",
        "CVE-" + "X" * 1000,
        "",
        None
    ]
    
    for malformed in malformed_tests:
        try:
            result = test_cve_retrieval(malformed)
            test_results.append(result)
            if result['success']:
                bug = f"Accepted malformed input: {malformed}"
                bugs_found.append(bug)
                print(f"  🐛 BUG: {bug}")
        except Exception as e:
            print(f"  ✅ Correctly rejected: {malformed}")
    
    # Test 4: Concurrent requests
    print("\n📋 Test 4: Concurrent requests (rate limiting)")
    cve_list = [f"CVE-2024-{i:05d}" for i in range(10)]
    
    try:
        concurrent_results = asyncio.run(test_concurrent_requests(cve_list))
        
        # Check for rate limiting
        error_count = sum(1 for r in concurrent_results if isinstance(r, dict) and r.get('error'))
        if error_count == 0:
            print("  ⚠️ No rate limiting detected on 10 concurrent requests")
        else:
            print(f"  ✅ Rate limiting active: {error_count} requests throttled")
            
    except Exception as e:
        bug = f"Concurrent request handling failed: {e}"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SPARTA CVE Bug Hunt Summary")
    print("="*60)
    print(f"Total tests run: {len(test_results)}")
    print(f"Bugs found: {len(bugs_found)}")
    
    if bugs_found:
        print("\n🐛 Bugs discovered:")
        for i, bug in enumerate(bugs_found, 1):
            print(f"  {i}. {bug}")
    else:
        print("\n✅ No bugs found in SPARTA CVE retrieval")
    
    # Save detailed report
    report = {
        "task": "002_sparta_cve",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "module": "sparta",
        "bugs_found": bugs_found,
        "test_results": test_results,
        "recommendations": [
            "Implement proper rate limiting",
            "Add input validation for CVE format",
            "Ensure all required fields in response",
            "Optimize performance for <1s response time"
        ]
    }
    
    with open("bug_hunter_results_002.json", "w") as f:
        json.dump(report, f, indent=2)
    
    return report


if __name__ == "__main__":
    # Check if running as part of comprehensive test
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        report = run_sparta_bug_hunt()
        print(json.dumps(report))
    else:
        run_sparta_bug_hunt()