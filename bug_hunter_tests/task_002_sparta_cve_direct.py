#!/usr/bin/env python3
"""
Module: task_002_sparta_cve_direct.py
Description: Task #002 - Direct CVE API test for SPARTA

This directly tests the CVE functionality without complex imports.

External Dependencies:
- aiohttp: https://docs.aiohttp.org/
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> test_cve_direct("CVE-2024-12345")

Expected Output:
>>> API response or error with timing

Example Usage:
>>> python task_002_sparta_cve_direct.py
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, Any, List, Optional


class CVEApiBugHunter:
    """Direct CVE API testing for bug hunting"""
    
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    async def get_cve(self, cve_id: str) -> Dict[str, Any]:
        """Get specific CVE details"""
        async with aiohttp.ClientSession() as session:
            params = {"cveId": cve_id}
            
            try:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "data": data,
                            "status": response.status
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}",
                            "status": response.status
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "exception_type": type(e).__name__
                }
    
    async def search_cves(self, keywords: str, limit: int = 10) -> Dict[str, Any]:
        """Search CVEs by keywords"""
        async with aiohttp.ClientSession() as session:
            params = {
                "keywordSearch": keywords,
                "resultsPerPage": min(limit, 100)
            }
            
            try:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "count": len(data.get("vulnerabilities", [])),
                            "data": data
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}"
                        }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }


async def run_bug_hunt():
    """Run comprehensive CVE API bug hunting tests"""
    print("\n" + "="*60)
    print("🐛 TASK #002: SPARTA CVE API Bug Hunter (Direct)")
    print("="*60)
    
    api = CVEApiBugHunter()
    bugs_found = []
    test_results = []
    
    # Test 1: Valid recent CVE
    print("\n📋 Test 1: Valid CVE lookup (CVE-2024-3094 - XZ backdoor)")
    start = time.time()
    result = await api.get_cve("CVE-2024-3094")
    duration = time.time() - start
    
    test_results.append({
        "test": "valid_cve",
        "duration": duration,
        "result": result
    })
    
    print(f"  Duration: {duration:.3f}s")
    print(f"  Success: {result.get('success', False)}")
    
    if duration > 5.0:
        bug = f"Performance issue: {duration:.3f}s exceeds 5s threshold"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Test 2: Non-existent CVE
    print("\n📋 Test 2: Non-existent CVE (CVE-9999-99999)")
    start = time.time()
    result = await api.get_cve("CVE-9999-99999")
    duration = time.time() - start
    
    test_results.append({
        "test": "nonexistent_cve", 
        "duration": duration,
        "result": result
    })
    
    print(f"  Duration: {duration:.3f}s")
    print(f"  Success: {result.get('success', False)}")
    
    # Check if it returns empty result vs error
    if result.get('success') and result.get('data', {}).get('vulnerabilities'):
        bug = "Non-existent CVE returned data instead of empty result"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Test 3: Malformed CVE formats
    print("\n📋 Test 3: Malformed CVE formats")
    malformed_tests = [
        "CVE-INVALID",
        "'; DROP TABLE cves; --",
        "CVE-" + "X" * 1000,
        "../../../etc/passwd"
    ]
    
    for malformed in malformed_tests:
        try:
            result = await api.get_cve(malformed)
            if result.get('success'):
                bug = f"Accepted malformed CVE ID: {malformed[:50]}"
                bugs_found.append(bug)
                print(f"  🐛 BUG: {bug}")
            else:
                print(f"  ✅ Correctly rejected: {malformed[:50]}")
        except Exception as e:
            print(f"  ✅ Exception thrown for: {malformed[:50]} - {type(e).__name__}")
    
    # Test 4: Concurrent requests
    print("\n📋 Test 4: Concurrent CVE lookups (rate limiting)")
    cve_ids = [f"CVE-2024-{i:04d}" for i in range(1, 11)]
    
    start = time.time()
    tasks = [api.get_cve(cve_id) for cve_id in cve_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = time.time() - start
    
    errors = sum(1 for r in results if isinstance(r, Exception) or (isinstance(r, dict) and not r.get('success')))
    rate_limit_errors = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 403)
    
    print(f"  Total duration: {duration:.3f}s")
    print(f"  Errors: {errors}/10")
    print(f"  Rate limit errors: {rate_limit_errors}")
    
    if rate_limit_errors > 0:
        print("  ⚠️ Rate limiting detected (403 errors)")
    elif errors == 0 and duration < 1.0:
        bug = "No rate limiting on rapid requests"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Test 5: Search functionality
    print("\n📋 Test 5: CVE search functionality")
    search_result = await api.search_cves("buffer overflow", limit=5)
    
    if search_result.get('success'):
        count = search_result.get('count', 0)
        print(f"  ✅ Found {count} CVEs for 'buffer overflow'")
        
        if count == 0:
            bug = "Search returned 0 results for common term 'buffer overflow'"
            bugs_found.append(bug)
            print(f"  🐛 BUG: {bug}")
    else:
        bug = f"Search failed: {search_result.get('error')}"
        bugs_found.append(bug)
        print(f"  🐛 BUG: {bug}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 CVE API Bug Hunt Summary")
    print("="*60)
    print(f"Total tests run: {len(test_results) + len(malformed_tests) + 10 + 1}")
    print(f"Bugs found: {len(bugs_found)}")
    
    if bugs_found:
        print("\n🐛 Bugs discovered:")
        for i, bug in enumerate(bugs_found, 1):
            print(f"  {i}. {bug}")
    else:
        print("\n✅ No bugs found in CVE API")
    
    # Save report
    report = {
        "task": "002_sparta_cve_direct",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "module": "CVE API (Direct)",
        "bugs_found": bugs_found,
        "test_results": test_results,
        "recommendations": [
            "Implement API key support for higher rate limits",
            "Add request caching to improve performance",
            "Validate CVE ID format before API call",
            "Handle empty results vs errors consistently"
        ]
    }
    
    with open("bug_hunter_results_002_direct.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: bug_hunter_results_002_direct.json")
    
    return report


if __name__ == "__main__":
    asyncio.run(run_bug_hunt())