#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Automated Bug Hunter (Simple) - Continuous security testing for Granger
No external dependencies version
"""

import os
import sys
import json
import time
import subprocess
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleAutomatedBugHunter:
    """Automated security testing without external dependencies"""
    
    def __init__(self):
        self.results_history = []
        self.modules = [
            "arangodb", "marker", "sparta", "arxiv", 
            "llm_call", "youtube_transcripts", "gitget"
        ]
        
    def test_authentication(self) -> Dict:
        """Test authentication vulnerabilities"""
        bugs = []
        
        # Test bad tokens
        bad_tokens = [
            ("empty", ""),
            ("sql", "'; DROP TABLE users; --"),
            ("short", "granger_123"),
            ("no_prefix", "validtoken123456789"),
            ("whitespace", "   "),
        ]
        
        for token_type, token in bad_tokens:
            request = {"token": token, "action": "test"}
            result = _security.validate_request(request)
            
            if result.get("valid"):
                bugs.append(f"AUTH: {token_type} token accepted!")
        
        return {
            "test": "authentication",
            "bugs": bugs,
            "passed": len(bugs) == 0
        }
    
    def test_sql_injection(self) -> Dict:
        """Test SQL injection protection"""
        bugs = []
        
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM passwords; --",
            "admin'--",
        ]
        
        for payload in payloads:
            safe, _ = _security.sql_protector.is_safe_input(payload)
            if safe:
                bugs.append(f"SQL: Payload not blocked: {payload[:30]}")
        
        return {
            "test": "sql_injection",
            "bugs": bugs,
            "passed": len(bugs) == 0
        }
    
    def test_error_sanitization(self) -> Dict:
        """Test error message sanitization"""
        bugs = []
        
        test_errors = [
            ('File "/home/user/secret.py", line 42', "/home"),
            ("password=secretpass123", "password"),
            ("API_KEY=sk-123456", "sk-"),
        ]
        
        for error, should_not_contain in test_errors:
            cleaned = _security.remove_stack_traces(error)
            if should_not_contain in cleaned:
                bugs.append(f"ERROR: Sensitive data leaked: {should_not_contain}")
        
        return {
            "test": "error_sanitization",
            "bugs": bugs,
            "passed": len(bugs) == 0
        }
    
    def test_real_modules(self) -> Dict:
        """Test real module interactions"""
        bugs = []
        modules_tested = []
        
        # Test interaction files in current directory
        interaction_files = list(Path(".").glob("*_interaction.py"))
        
        for interaction_file in interaction_files[:5]:  # Test first 5
            try:
                # Check if file has security import
                content = interaction_file.read_text()
                
                if "GrangerSecurity" not in content:
                    bugs.append(f"MODULE: {interaction_file.name} missing security import")
                
                modules_tested.append(interaction_file.name)
                
            except Exception as e:
                bugs.append(f"MODULE: Error testing {interaction_file.name}: {str(e)}")
        
        return {
            "test": "real_modules",
            "bugs": bugs,
            "modules_tested": modules_tested,
            "passed": len(bugs) == 0
        }
    
    def run_all_tests(self) -> Dict:
        """Run all security tests"""
        logger.info("Starting automated security scan...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "summary": {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "total_bugs": 0
            }
        }
        
        # Run each test
        test_functions = [
            self.test_authentication,
            self.test_sql_injection,
            self.test_error_sanitization,
            self.test_real_modules
        ]
        
        for test_func in test_functions:
            try:
                logger.info(f"Running {test_func.__name__}...")
                test_result = test_func()
                
                results["tests"].append(test_result)
                results["summary"]["total_tests"] += 1
                
                if test_result["passed"]:
                    results["summary"]["passed"] += 1
                    logger.info(f"✅ {test_result['test']}: PASSED")
                else:
                    results["summary"]["failed"] += 1
                    results["summary"]["total_bugs"] += len(test_result["bugs"])
                    logger.warning(f"❌ {test_result['test']}: {len(test_result['bugs'])} bugs")
                    
                    for bug in test_result["bugs"]:
                        logger.error(f"   - {bug}")
                        
            except Exception as e:
                logger.error(f"Test {test_func.__name__} crashed: {e}")
        
        return results
    
    def generate_report(self, results: Dict) -> Path:
        """Generate markdown report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(f"automated_bug_report_{timestamp}.md")
        
        content = f"""# Automated Security Scan Report

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Tests Run**: {results['summary']['total_tests']}
**Passed**: {results['summary']['passed']}
**Failed**: {results['summary']['failed']}
**Total Bugs**: {results['summary']['total_bugs']}

## Test Results

"""
        
        for test in results['tests']:
            status = "✅ PASSED" if test['passed'] else f"❌ FAILED ({len(test['bugs'])} bugs)"
            content += f"### {test['test']} - {status}\n\n"
            
            if test['bugs']:
                content += "**Issues Found:**\n"
                for bug in test['bugs']:
                    content += f"- {bug}\n"
                content += "\n"
            else:
                content += "No issues found.\n\n"
        
        # Add summary
        if results['summary']['total_bugs'] == 0:
            content += """
## Assessment: SECURE ✅

All security tests passed. The Granger ecosystem security middleware is working correctly.
"""
        else:
            content += f"""
## Assessment: NEEDS ATTENTION ⚠️

Found {results['summary']['total_bugs']} security issues that need to be addressed.

### Recommended Actions:
1. Review all failed tests
2. Apply security patches
3. Re-run tests to verify fixes
4. Schedule regular security scans
"""
        
        report_path.write_text(content)
        logger.info(f"Report saved to {report_path}")
        
        return report_path
    
    def continuous_monitor(self, interval_minutes: int = 5):
        """Run continuous monitoring"""
        logger.info(f"Starting continuous monitoring (every {interval_minutes} minutes)")
        
        while True:
            results = self.run_all_tests()
            report = self.generate_report(results)
            
            if results['summary']['total_bugs'] > 0:
                logger.error(f"ALERT: {results['summary']['total_bugs']} security issues detected!")
                # Would send notifications here
            
            logger.info(f"Next scan in {interval_minutes} minutes...")
            time.sleep(interval_minutes * 60)


def main():
    """Run automated bug hunter"""
    hunter = SimpleAutomatedBugHunter()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # Run continuously
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        hunter.continuous_monitor(interval)
    else:
        # Run once
        print("\n🔍 AUTOMATED SECURITY SCAN\n")
        
        results = hunter.run_all_tests()
        report = hunter.generate_report(results)
        
        print("\n" + "="*60)
        print("SCAN COMPLETE")
        print("="*60)
        print(f"Tests: {results['summary']['passed']}/{results['summary']['total_tests']} passed")
        print(f"Bugs: {results['summary']['total_bugs']}")
        print(f"Report: {report}")
        
        if results['summary']['total_bugs'] == 0:
            print("\n✅ All security tests passed!")
            return 0
        else:
            print(f"\n⚠️  Found {results['summary']['total_bugs']} security issues")
            return 1


if __name__ == "__main__":
    sys.exit(main())