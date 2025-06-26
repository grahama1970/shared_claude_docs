"""
Test script for real SPARTA handlers (synchronous version)
Validates that handlers properly integrate with actual SPARTA functionality
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from real_sparta_handlers_fixed import (
    SPARTADownloadHandler,
    SPARTAMissionSearchHandler,
    SPARTACVESearchHandler,
    SPARTAMITREHandler,
    SPARTAModuleHandler,
    SPARTA_AVAILABLE
)


class SPARTAHandlerTester:
    """Test suite for SPARTA handlers"""
    
    def __init__(self):
        self.results = []
        self.start_time = time.time()
        
    def test_download_handler(self) -> Dict[str, Any]:
        """Test resource download functionality"""
        print("\n🔍 Testing SPARTA Download Handler...")
        
        handler = SPARTADownloadHandler()
        result = handler.run(limit=3)  # Small limit for testing
        
        test_result = {
            "handler": "SPARTADownloadHandler",
            "success": result.success,
            "duration": result.duration,
            "resources_downloaded": result.output_data.get("result", {}).get("resources_downloaded", 0),
            "failures": result.output_data.get("result", {}).get("download_failures", 0),
            "error": result.error
        }
        
        if result.success:
            print(f"   ✅ Downloaded {test_result['resources_downloaded']} resources")
            print(f"   ⏱️  Duration: {result.duration:.2f}s")
        else:
            print(f"   ❌ Failed: {result.error}")
            
        return test_result
    
    def test_mission_search_handler(self) -> Dict[str, Any]:
        """Test NASA mission search"""
        print("\n🚀 Testing NASA Mission Search Handler...")
        
        handler = SPARTAMissionSearchHandler()
        result = handler.run(query="Apollo", limit=5)
        
        test_result = {
            "handler": "SPARTAMissionSearchHandler",
            "success": result.success,
            "duration": result.duration,
            "missions_found": result.output_data.get("result", {}).get("missions_found", 0),
            "sample_mission": result.output_data.get("result", {}).get("missions", [{}])[0] if result.output_data.get("result", {}).get("missions") else None,
            "error": result.error
        }
        
        if result.success:
            print(f"   ✅ Found {test_result['missions_found']} missions")
            print(f"   ⏱️  Duration: {result.duration:.2f}s")
            if test_result['sample_mission']:
                print(f"   📋 Sample: {test_result['sample_mission'].get('name', 'Unknown')}")
        else:
            print(f"   ❌ Failed: {result.error}")
            
        return test_result
    
    def test_cve_search_handler(self) -> Dict[str, Any]:
        """Test CVE vulnerability search"""
        print("\n🔒 Testing CVE Search Handler...")
        
        handler = SPARTACVESearchHandler()
        result = handler.run(keywords="satellite", severity="HIGH", limit=5)
        
        test_result = {
            "handler": "SPARTACVESearchHandler",
            "success": result.success,
            "duration": result.duration,
            "vulnerabilities_found": result.output_data.get("result", {}).get("vulnerabilities_found", 0),
            "severity_distribution": result.output_data.get("result", {}).get("severity_distribution", {}),
            "sample_cve": result.output_data.get("result", {}).get("vulnerabilities", [{}])[0] if result.output_data.get("result", {}).get("vulnerabilities") else None,
            "error": result.error
        }
        
        if result.success:
            print(f"   ✅ Found {test_result['vulnerabilities_found']} vulnerabilities")
            print(f"   ⏱️  Duration: {result.duration:.2f}s")
            print(f"   📊 Severity: {test_result['severity_distribution']}")
        else:
            print(f"   ❌ Failed: {result.error}")
            
        return test_result
    
    def test_mitre_handler(self) -> Dict[str, Any]:
        """Test MITRE framework query"""
        print("\n🎯 Testing MITRE Handler...")
        
        handler = SPARTAMITREHandler()
        result = handler.run(framework="attack", query="T1055")
        
        test_result = {
            "handler": "SPARTAMITREHandler",
            "success": result.success,
            "duration": result.duration,
            "framework": result.input_data.get("framework"),
            "query": result.input_data.get("query"),
            "found": result.output_data.get("result", {}).get("found", False),
            "result_summary": str(result.output_data.get("result", {}).get("result", ""))[:100] if result.output_data.get("result", {}).get("result") else None,
            "error": result.error
        }
        
        if result.success:
            print(f"   ✅ Query successful: {test_result['framework']}/{test_result['query']}")
            print(f"   ⏱️  Duration: {result.duration:.2f}s")
            print(f"   📄 Found: {test_result['found']}")
        else:
            print(f"   ❌ Failed: {result.error}")
            
        return test_result
    
    def test_module_handler(self) -> Dict[str, Any]:
        """Test SPARTA module interface"""
        print("\n🔧 Testing SPARTA Module Handler...")
        
        handler = SPARTAModuleHandler()
        result = handler.run(
            action="search_space_missions",
            data={"query": "Mars", "limit": 3}
        )
        
        test_result = {
            "handler": "SPARTAModuleHandler",
            "success": result.success,
            "duration": result.duration,
            "action": result.input_data.get("action"),
            "module_response": result.output_data.get("result", {}).get("success", False),
            "data_received": bool(result.output_data.get("result", {}).get("data")),
            "error": result.error
        }
        
        if result.success:
            print(f"   ✅ Module action successful: {test_result['action']}")
            print(f"   ⏱️  Duration: {result.duration:.2f}s")
            print(f"   📦 Data received: {test_result['data_received']}")
        else:
            print(f"   ❌ Failed: {result.error}")
            
        return test_result
    
    def run_all_tests(self):
        """Run all handler tests"""
        print("=" * 60)
        print("🧪 SPARTA Real Handler Test Suite")
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔌 SPARTA Available: {SPARTA_AVAILABLE}")
        print("=" * 60)
        
        if not SPARTA_AVAILABLE:
            print("\n⚠️  WARNING: SPARTA module not available!")
            print("   Some tests may fail or use mock data.")
        
        # Run all tests
        test_methods = [
            self.test_download_handler,
            self.test_mission_search_handler,
            self.test_cve_search_handler,
            self.test_mitre_handler,
            self.test_module_handler
        ]
        
        for test_method in test_methods:
            try:
                result = test_method()
                self.results.append(result)
            except Exception as e:
                print(f"   ⚠️  Test failed with exception: {e}")
                self.results.append({
                    "handler": test_method.__name__,
                    "success": False,
                    "error": str(e)
                })
        
        # Summary
        self.print_summary()
        
    def print_summary(self):
        """Print test summary"""
        total_duration = time.time() - self.start_time
        successful = sum(1 for r in self.results if r.get("success", False))
        failed = len(self.results) - successful
        
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"Total Tests: {len(self.results)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Total Duration: {total_duration:.2f}s")
        
        if failed > 0:
            print("\n❌ Failed Tests:")
            for result in self.results:
                if not result.get("success", False):
                    print(f"   - {result['handler']}: {result.get('error', 'Unknown error')}")
        
        # Save detailed results
        output_file = f"sparta_handler_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                "test_run": {
                    "timestamp": datetime.now().isoformat(),
                    "sparta_available": SPARTA_AVAILABLE,
                    "total_duration": total_duration,
                    "summary": {
                        "total": len(self.results),
                        "successful": successful,
                        "failed": failed
                    }
                },
                "results": self.results
            }, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        
        # Return status
        return failed == 0


def main():
    """Main test runner"""
    tester = SPARTAHandlerTester()
    success = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All SPARTA handler tests passed!")
    else:
        print("❌ Some SPARTA handler tests failed!")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    import sys
    # sys.exit() removed)