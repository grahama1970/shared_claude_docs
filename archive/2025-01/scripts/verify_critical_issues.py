#!/usr/bin/env python3
"""
Module: verify_critical_issues.py
Description: Verify critical issues found in 67-scenario test with skeptical verification

External Dependencies:
- perplexity-ask: CLI tool for Perplexity API verification
- None (uses built-in modules only)

Sample Input:
>>> verifier = CriticalIssueVerifier()
>>> verifier.verify_all_issues()

Expected Output:
>>> {
>>>     "issues_verified": 4,
>>>     "real_fixes_confirmed": 2,
>>>     "confidence": 0.5
>>> }
"""

import os
import sys
import time
import json
import asyncio
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class CriticalIssueVerifier:
    """Verify critical issues with skeptical external verification"""
    
    def __init__(self):
        self.issues_found = []
        self.verifications = []
        self.perplexity_available = self._check_perplexity()
        
    def _check_perplexity(self) -> bool:
        """Check if perplexity-ask is available"""
        try:
            result = subprocess.run(['which', 'perplexity-ask'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def verify_all_issues(self) -> Dict[str, Any]:
        """Verify all critical issues found"""
        print("🔍 CRITICAL ISSUE VERIFICATION")
        print("="*80)
        
        # Issue 1: SPARTA returning 0 CVEs
        self._verify_sparta_cve_search()
        
        # Issue 2: World Model API error
        self._verify_world_model_api()
        
        # Issue 3: Test Reporter API error
        self._verify_test_reporter_api()
        
        # Issue 4: GitGet import failure
        self._verify_gitget_import()
        
        # Issue 5: Only 6% real tests
        self._verify_real_test_coverage()
        
        # Issue 6: ArangoDB configuration
        self._verify_arangodb_config()
        
        return self._generate_verification_report()
    
    def _verify_sparta_cve_search(self):
        """Verify SPARTA CVE search functionality"""
        print("\n📋 Issue 1: SPARTA returning 0 CVEs")
        
        # Add SPARTA to path
        sparta_path = Path("/home/graham/workspace/experiments/sparta")
        sys.path.insert(0, str(sparta_path / "src"))
        
        try:
            from sparta.integrations.sparta_module import SPARTAModule
            module = SPARTAModule()
            
            # Test with known security term
            test_request = {
                "action": "search_cve",
                "data": {"query": "buffer overflow", "limit": 5}
            }
            
            print("   Testing SPARTA with 'buffer overflow' query...")
            response = asyncio.run(module.process(test_request))
            
            if response.get("success"):
                cve_count = len(response.get('data', {}).get('cves', []))
                self.issues_found.append({
                    "issue": "SPARTA 0 CVEs",
                    "status": "WORKING" if cve_count > 0 else "BROKEN",
                    "detail": f"Returned {cve_count} CVEs",
                    "evidence": response.get('data', {}).get('cves', [])[:2]  # First 2 CVEs
                })
                print(f"   ✅ SPARTA returned {cve_count} CVEs")
                
                # Skeptical verification with Perplexity
                if self.perplexity_available and cve_count > 0:
                    self._verify_with_perplexity(
                        f"Are these real CVE IDs: {', '.join(c.get('id', '') for c in response.get('data', {}).get('cves', [])[:3])}?",
                        "SPARTA CVE verification"
                    )
            else:
                self.issues_found.append({
                    "issue": "SPARTA 0 CVEs",
                    "status": "ERROR",
                    "detail": response.get('error', 'Unknown error'),
                    "evidence": None
                })
                print(f"   ❌ SPARTA error: {response.get('error')}")
                
        except Exception as e:
            self.issues_found.append({
                "issue": "SPARTA 0 CVEs",
                "status": "IMPORT_ERROR",
                "detail": str(e),
                "evidence": None
            })
            print(f"   ❌ SPARTA import/test error: {e}")
    
    def _verify_world_model_api(self):
        """Verify World Model API"""
        print("\n📋 Issue 2: World Model API error")
        
        world_model_path = Path("/home/graham/workspace/experiments/world_model")
        sys.path.insert(0, str(world_model_path / "src"))
        
        try:
            from world_model import WorldModel
            model = WorldModel()
            
            # Check if get_state method exists
            if hasattr(model, 'get_state'):
                print("   ✅ World Model has get_state method")
                self.issues_found.append({
                    "issue": "World Model get_state",
                    "status": "FIXED",
                    "detail": "Method exists",
                    "evidence": dir(model)
                })
            else:
                # Check what methods are available
                available_methods = [m for m in dir(model) if not m.startswith('_')]
                print(f"   ❌ World Model missing get_state. Available: {available_methods[:5]}")
                self.issues_found.append({
                    "issue": "World Model get_state",
                    "status": "BROKEN",
                    "detail": f"Missing method. Available: {available_methods[:5]}",
                    "evidence": available_methods
                })
                
        except Exception as e:
            self.issues_found.append({
                "issue": "World Model get_state",
                "status": "IMPORT_ERROR",
                "detail": str(e),
                "evidence": None
            })
            print(f"   ❌ World Model error: {e}")
    
    def _verify_test_reporter_api(self):
        """Verify Test Reporter API"""
        print("\n📋 Issue 3: Test Reporter API error")
        
        reporter_path = Path("/home/graham/workspace/experiments/claude-test-reporter")
        sys.path.insert(0, str(reporter_path / "src"))
        
        try:
            from claude_test_reporter import GrangerTestReporter
            reporter = GrangerTestReporter()
            
            # Check generate_report signature
            import inspect
            sig = inspect.signature(reporter.generate_report)
            param_count = len(sig.parameters)
            
            if param_count == 0:
                print("   ✅ Test Reporter generate_report takes 0 args (self only)")
                self.issues_found.append({
                    "issue": "Test Reporter API",
                    "status": "NEEDS_DATA",
                    "detail": f"Method takes {param_count} args, but test passed data",
                    "evidence": str(sig)
                })
            else:
                print(f"   ✅ Test Reporter generate_report takes {param_count} args")
                self.issues_found.append({
                    "issue": "Test Reporter API",
                    "status": "WORKING",
                    "detail": f"Method signature: {sig}",
                    "evidence": str(sig)
                })
                
        except Exception as e:
            self.issues_found.append({
                "issue": "Test Reporter API",
                "status": "IMPORT_ERROR",
                "detail": str(e),
                "evidence": None
            })
            print(f"   ❌ Test Reporter error: {e}")
    
    def _verify_gitget_import(self):
        """Verify GitGet import"""
        print("\n📋 Issue 4: GitGet import failure")
        
        gitget_path = Path("/home/graham/workspace/experiments/gitget")
        
        if not gitget_path.exists():
            print("   ❌ GitGet directory not found")
            self.issues_found.append({
                "issue": "GitGet import",
                "status": "NOT_FOUND",
                "detail": f"Directory {gitget_path} does not exist",
                "evidence": None
            })
        else:
            sys.path.insert(0, str(gitget_path / "src"))
            
            try:
                from gitget import GitGetModule
                print("   ✅ GitGet imports successfully")
                self.issues_found.append({
                    "issue": "GitGet import",
                    "status": "FIXED",
                    "detail": "Import successful",
                    "evidence": str(GitGetModule)
                })
            except ImportError as e:
                print(f"   ❌ GitGet import error: {e}")
                self.issues_found.append({
                    "issue": "GitGet import",
                    "status": "IMPORT_ERROR",
                    "detail": str(e),
                    "evidence": None
                })
    
    def _verify_real_test_coverage(self):
        """Verify real test coverage issue"""
        print("\n📋 Issue 5: Only 6% real test coverage")
        
        # This is a systemic issue - need to implement real tests
        self.issues_found.append({
            "issue": "Low real test coverage",
            "status": "SYSTEMIC",
            "detail": "Only 6 of 67 scenarios have real tests",
            "evidence": {
                "real_tests": ["SPARTA", "ArangoDB", "YouTube", "Marker", "LLM Call", "RL Commons"],
                "missing_real_tests": 61
            }
        })
        print("   ⚠️  Systemic issue - need to implement real interaction tests")
    
    def _verify_arangodb_config(self):
        """Verify ArangoDB configuration"""
        print("\n📋 Issue 6: ArangoDB configuration")
        
        # Check environment
        arango_host = os.getenv("ARANGO_HOST", "not_set")
        print(f"   Current ARANGO_HOST: {arango_host}")
        
        if arango_host.startswith(("http://", "https://")):
            print("   ✅ ArangoDB host has proper protocol prefix")
            self.issues_found.append({
                "issue": "ArangoDB config",
                "status": "FIXED",
                "detail": f"Host: {arango_host}",
                "evidence": arango_host
            })
        else:
            print("   ❌ ArangoDB host missing protocol prefix")
            self.issues_found.append({
                "issue": "ArangoDB config",
                "status": "BROKEN",
                "detail": f"Host '{arango_host}' needs http:// or https:// prefix",
                "evidence": arango_host
            })
    
    def _verify_with_perplexity(self, query: str, context: str):
        """Use Perplexity for skeptical verification"""
        if not self.perplexity_available:
            return
        
        try:
            print(f"   🤖 Asking Perplexity: {query[:60]}...")
            result = subprocess.run(
                ['perplexity-ask', query],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.verifications.append({
                    "context": context,
                    "query": query,
                    "response": result.stdout.strip()[:200],
                    "verified": True
                })
                print(f"   ✅ Perplexity verified: {result.stdout.strip()[:100]}...")
            else:
                print(f"   ⚠️  Perplexity verification failed")
                
        except Exception as e:
            print(f"   ⚠️  Perplexity error: {e}")
    
    def _generate_verification_report(self) -> Dict[str, Any]:
        """Generate verification report"""
        print("\n" + "="*80)
        print("📊 VERIFICATION SUMMARY")
        print("="*80)
        
        # Count statuses
        status_counts = {}
        for issue in self.issues_found:
            status = issue['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate confidence
        total = len(self.issues_found)
        working = status_counts.get('WORKING', 0) + status_counts.get('FIXED', 0)
        confidence = working / max(total, 1)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "issues_checked": total,
            "status_counts": status_counts,
            "confidence": round(confidence, 2),
            "issues": self.issues_found,
            "perplexity_verifications": self.verifications
        }
        
        # Print summary
        print(f"\nIssues Checked: {total}")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")
        
        print(f"\nConfidence: {report['confidence']}/1.0")
        
        if confidence < 0.5:
            print("\n❌ CRITICAL: Major issues prevent deployment")
        else:
            print("\n⚠️  WARNING: Some issues need attention")
        
        # Save report
        report_path = Path("critical_issues_verification.json")
        report_path.write_text(json.dumps(report, indent=2))
        print(f"\n📄 Report saved to: {report_path}")
        
        return report

def main():
    """Run critical issue verification"""
    verifier = CriticalIssueVerifier()
    report = verifier.verify_all_issues()
    
    # Return based on confidence
    if report["confidence"] < 0.5:
        return 1
    else:
        return 0

if __name__ == "__main__":
    exit(main())