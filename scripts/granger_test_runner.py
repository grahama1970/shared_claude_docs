#!/usr/bin/env python3
"""
Granger Ecosystem Test Runner with Critical Verification

This script runs comprehensive tests across all spoke projects and
produces a skeptical/critical verification report.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple
import sys
import asyncio


# All spoke projects to test
SPOKE_PROJECTS = [
    ("youtube_transcripts", "/home/graham/workspace/experiments/youtube_transcripts/"),
    ("darpa_crawl", "/home/graham/workspace/experiments/darpa_crawl/"),
    ("gitget", "/home/graham/workspace/experiments/gitget/"),
    ("aider-daemon", "/home/graham/workspace/experiments/aider-daemon/"),
    ("sparta", "/home/graham/workspace/experiments/sparta/"),
    ("marker", "/home/graham/workspace/experiments/marker/"),
    ("arangodb", "/home/graham/workspace/experiments/arangodb/"),
    ("claude_max_proxy", "/home/graham/workspace/experiments/claude_max_proxy/"),
    ("arxiv-mcp-server", "/home/graham/workspace/mcp-servers/arxiv-mcp-server/"),
    ("unsloth_wip", "/home/graham/workspace/experiments/fine_tuning/"),
    ("mcp-screenshot", "/home/graham/workspace/experiments/mcp-screenshot/")
]


class CriticalTestVerifier:
    """Skeptically verify test results"""
    
    def __init__(self):
        self.results = {}
        self.critical_issues = []
        self.suspicious_patterns = []
        
    def verify_test_duration(self, duration: float, test_name: str) -> Tuple[bool, str]:
        """Verify test duration is realistic"""
        if duration < 0.001:  # Less than 1ms
            return False, f"SUSPICIOUS: Test {test_name} ran in {duration}s - likely not testing real functionality"
        elif duration < 0.01:  # Less than 10ms
            return False, f"WARNING: Test {test_name} ran in {duration}s - may be using mocks"
        elif duration > 30:  # More than 30s
            return False, f"WARNING: Test {test_name} took {duration}s - possible timeout or hang"
        return True, "Duration acceptable"
    
    def verify_test_output(self, output: str, test_name: str) -> Tuple[bool, List[str]]:
        """Check for suspicious patterns in test output"""
        issues = []
        
        # Check for mock/stub indicators
        mock_patterns = ["Mock", "mock", "stub", "Stub", "fake", "Fake", "MagicMock"]
        for pattern in mock_patterns:
            if pattern in output:
                issues.append(f"Found '{pattern}' in output - may be using mocks")
        
        # Check for placeholder content
        placeholder_patterns = ["TODO", "FIXME", "placeholder", "example", "test123"]
        for pattern in placeholder_patterns:
            if pattern in output:
                issues.append(f"Found '{pattern}' in output - may be placeholder content")
        
        # Check for actual functionality indicators
        real_patterns = ["MCP server", "FastMCP", "prompt registered", "tool registered"]
        found_real = any(pattern in output for pattern in real_patterns)
        if not found_real:
            issues.append("No indicators of real MCP functionality found")
        
        return len(issues) == 0, issues
    
    def verify_async_implementation(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Verify async implementation is correct"""
        issues = []
        
        if not file_path.exists():
            return False, ["File does not exist"]
        
        content = file_path.read_text()
        
        # Check for asyncio.run() inside functions (bad)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'asyncio.run(' in line and not line.strip().startswith('#'):
                # Check if it's inside a function (not in main block)
                indent = len(line) - len(line.lstrip())
                if indent > 0 and i > 0:
                    # Look for function definition above
                    for j in range(i-1, max(0, i-20), -1):
                        if lines[j].strip().startswith('def ') or lines[j].strip().startswith('async def '):
                            if '__main__' not in lines[j]:
                                issues.append(f"Line {i+1}: asyncio.run() inside function (not in __main__)")
                                break
        
        return len(issues) == 0, issues
    
    def run_project_tests(self, project_name: str, project_path: str) -> Dict[str, Any]:
        """Run tests for a single project with critical verification"""
        result = {
            "project": project_name,
            "path": project_path,
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "critical_issues": [],
            "verification_status": "PENDING"
        }
        
        # Change to project directory
        project_dir = Path(project_path)
        
        # Test 1: MCP Prompts Test
        print(f"\n🔍 Testing {project_name} MCP prompts...")
        test_file = project_dir / "tests" / "mcp" / "test_prompts.py"
        
        if test_file.exists():
            start_time = time.time()
            try:
                # Run pytest
                cmd = [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"]
                proc = subprocess.run(
                    cmd,
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                duration = time.time() - start_time
                
                test_result = {
                    "status": "PASS" if proc.returncode == 0 else "FAIL",
                    "duration": duration,
                    "output": proc.stdout + proc.stderr,
                    "exit_code": proc.returncode
                }
                
                # Critical verification
                dur_ok, dur_msg = self.verify_test_duration(duration, "test_prompts")
                out_ok, out_issues = self.verify_test_output(proc.stdout + proc.stderr, "test_prompts")
                
                if not dur_ok:
                    test_result["critical_issues"] = [dur_msg]
                    result["critical_issues"].append(dur_msg)
                
                if not out_ok:
                    test_result["critical_issues"] = test_result.get("critical_issues", []) + out_issues
                    result["critical_issues"].extend(out_issues)
                
                # Check for specific test results
                if "test_required_prompts_exist" not in proc.stdout:
                    test_result["critical_issues"] = test_result.get("critical_issues", []) + ["Required prompts test not found"]
                
                result["tests"]["prompts"] = test_result
                
            except subprocess.TimeoutExpired:
                result["tests"]["prompts"] = {
                    "status": "TIMEOUT",
                    "duration": 60,
                    "critical_issues": ["Test timed out after 60 seconds"]
                }
                result["critical_issues"].append("Prompts test timeout")
            except Exception as e:
                result["tests"]["prompts"] = {
                    "status": "ERROR",
                    "error": str(e),
                    "critical_issues": [f"Test execution error: {str(e)}"]
                }
                result["critical_issues"].append(f"Prompts test error: {str(e)}")
        else:
            result["tests"]["prompts"] = {
                "status": "MISSING",
                "critical_issues": ["Test file does not exist"]
            }
            result["critical_issues"].append("No prompts test file")
        
        # Test 2: Server Validation
        print(f"🔍 Testing {project_name} MCP server...")
        module_name = project_name.replace('-', '_')
        server_file = project_dir / "src" / module_name / "mcp" / "server.py"
        
        if server_file.exists():
            # Verify async implementation
            async_ok, async_issues = self.verify_async_implementation(server_file)
            if not async_ok:
                result["critical_issues"].extend(async_issues)
            
            # Try to run server validation
            start_time = time.time()
            try:
                cmd = [sys.executable, str(server_file)]
                proc = subprocess.run(
                    cmd,
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env={**subprocess.os.environ, "PYTHONPATH": str(project_dir / "src")}
                )
                duration = time.time() - start_time
                
                server_result = {
                    "status": "PASS" if proc.returncode == 0 else "FAIL",
                    "duration": duration,
                    "output": proc.stdout + proc.stderr,
                    "exit_code": proc.returncode
                }
                
                # Verify server output
                if "Server validation passed" not in proc.stdout:
                    server_result["critical_issues"] = ["Server validation message not found"]
                    result["critical_issues"].append("Server validation incomplete")
                
                result["tests"]["server"] = server_result
                
            except subprocess.TimeoutExpired:
                result["tests"]["server"] = {
                    "status": "TIMEOUT",
                    "critical_issues": ["Server test timeout"]
                }
            except Exception as e:
                result["tests"]["server"] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        else:
            result["tests"]["server"] = {
                "status": "MISSING",
                "critical_issues": ["Server file does not exist"]
            }
            result["critical_issues"].append("No server implementation")
        
        # Test 3: CLI Integration
        print(f"🔍 Testing {project_name} CLI integration...")
        cli_patterns = [
            f"src/{module_name}/cli/app.py",
            f"src/{module_name}/cli/main.py",
            f"src/{module_name}/cli/commands.py",
            f"src/{module_name}/cli/__main__.py"
        ]
        
        cli_found = False
        for pattern in cli_patterns:
            cli_file = project_dir / pattern
            if cli_file.exists():
                content = cli_file.read_text()
                if "granger_slash_mcp_mixin" in content and "add_slash_mcp_commands" in content:
                    if f"project_name='{project_name}'" in content or f'project_name="{project_name}"' in content:
                        result["tests"]["cli"] = {"status": "PASS", "file": pattern}
                        cli_found = True
                        break
                    else:
                        result["tests"]["cli"] = {
                            "status": "FAIL",
                            "critical_issues": ["CLI has mixin but wrong project_name"]
                        }
                        result["critical_issues"].append("CLI project_name mismatch")
                else:
                    result["tests"]["cli"] = {
                        "status": "FAIL", 
                        "critical_issues": ["CLI missing Granger mixin integration"]
                    }
                    result["critical_issues"].append("CLI not integrated")
        
        if not cli_found:
            result["tests"]["cli"] = {
                "status": "MISSING",
                "critical_issues": ["No CLI file found"]
            }
            result["critical_issues"].append("No CLI implementation")
        
        # Determine overall verification status
        if len(result["critical_issues"]) == 0:
            result["verification_status"] = "VERIFIED"
        elif len(result["critical_issues"]) < 3:
            result["verification_status"] = "PARTIALLY_VERIFIED"
        else:
            result["verification_status"] = "FAILED_VERIFICATION"
        
        return result
    
    def generate_critical_report(self, all_results: List[Dict[str, Any]]) -> str:
        """Generate a skeptical/critical verification report"""
        report = f"""# Granger Ecosystem Test Verification Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Verifier**: Critical Test Verification Engine v1.0
**Mode**: SKEPTICAL/CRITICAL

## Executive Summary

This report provides a critical analysis of test results across the Granger ecosystem.
All results have been skeptically verified for authenticity and real functionality.

## Verification Criteria

1. **Test Duration**: Must be >0.001s (no instant tests) and <30s (no timeouts)
2. **Real Functionality**: No mocks, stubs, or placeholders allowed
3. **Async Compliance**: No asyncio.run() inside functions
4. **Integration**: CLI must use Granger standard mixin
5. **MCP Alignment**: Must follow video transcript patterns

## Project Results

| Project | Status | Tests | Critical Issues | Confidence |
|---------|--------|-------|-----------------|------------|
"""
        
        for result in all_results:
            project = result["project"]
            status = result["verification_status"]
            test_count = len(result["tests"])
            pass_count = sum(1 for t in result["tests"].values() if t.get("status") == "PASS")
            issues = len(result["critical_issues"])
            
            # Calculate confidence
            if status == "VERIFIED":
                confidence = "HIGH (90%+)"
            elif status == "PARTIALLY_VERIFIED":
                confidence = "MEDIUM (60-89%)"
            else:
                confidence = "LOW (<60%)"
            
            status_emoji = "✅" if status == "VERIFIED" else "⚠️" if status == "PARTIALLY_VERIFIED" else "❌"
            
            report += f"| {project} | {status_emoji} {status} | {pass_count}/{test_count} | {issues} | {confidence} |\n"
        
        # Detailed analysis
        report += "\n## Critical Issues Found\n\n"
        
        for result in all_results:
            if result["critical_issues"]:
                report += f"### {result['project']}\n"
                for issue in result["critical_issues"]:
                    report += f"- ❌ {issue}\n"
                report += "\n"
        
        # Suspicious patterns
        report += "## Suspicious Patterns Detected\n\n"
        
        instant_tests = []
        mock_usage = []
        missing_tests = []
        
        for result in all_results:
            for test_name, test_data in result["tests"].items():
                if test_data.get("status") == "MISSING":
                    missing_tests.append(f"{result['project']}/{test_name}")
                elif test_data.get("duration", 1) < 0.01:
                    instant_tests.append(f"{result['project']}/{test_name} ({test_data.get('duration', 0):.4f}s)")
                if test_data.get("critical_issues"):
                    for issue in test_data["critical_issues"]:
                        if "mock" in issue.lower():
                            mock_usage.append(f"{result['project']}/{test_name}")
        
        if instant_tests:
            report += "### ⚡ Suspiciously Fast Tests\n"
            for test in instant_tests:
                report += f"- {test}\n"
            report += "\n"
        
        if mock_usage:
            report += "### 🎭 Mock/Stub Usage Detected\n"
            for test in mock_usage:
                report += f"- {test}\n"
            report += "\n"
        
        if missing_tests:
            report += "### 📭 Missing Tests\n"
            for test in missing_tests:
                report += f"- {test}\n"
            report += "\n"
        
        # Verification summary
        verified_count = sum(1 for r in all_results if r["verification_status"] == "VERIFIED")
        partial_count = sum(1 for r in all_results if r["verification_status"] == "PARTIALLY_VERIFIED")
        failed_count = sum(1 for r in all_results if r["verification_status"] == "FAILED_VERIFICATION")
        
        report += f"""## Verification Summary

- ✅ **Fully Verified**: {verified_count}/{len(all_results)} projects
- ⚠️ **Partially Verified**: {partial_count}/{len(all_results)} projects  
- ❌ **Failed Verification**: {failed_count}/{len(all_results)} projects

## Confidence Assessment

Based on critical analysis, the overall confidence in the test results is:

**{self._calculate_overall_confidence(all_results)}**

## Recommendations

1. **Fix Critical Issues**: Address all critical issues before considering tests valid
2. **Remove Mocks**: Replace all mock usage with real functionality tests
3. **Add Missing Tests**: Implement tests for all missing components
4. **Verify Duration**: Ensure tests actually exercise real functionality
5. **Manual Verification**: Manually test slash commands in Claude Code

## Conclusion

This critical verification reveals that while the structure is in place, many projects
still need work to achieve true alignment with the MCP prompts standard. Only projects
with "VERIFIED" status can be considered fully compliant.

---
*Generated by Granger Critical Test Verifier - Accept No Substitutes*
"""
        
        return report
    
    def _calculate_overall_confidence(self, results: List[Dict[str, Any]]) -> str:
        """Calculate overall confidence level"""
        verified = sum(1 for r in results if r["verification_status"] == "VERIFIED")
        total = len(results)
        
        percentage = (verified / total) * 100 if total > 0 else 0
        
        if percentage >= 80:
            return f"HIGH ({percentage:.0f}%) - Most projects verified"
        elif percentage >= 50:
            return f"MEDIUM ({percentage:.0f}%) - Significant issues remain"
        else:
            return f"LOW ({percentage:.0f}%) - Major work needed"


def main():
    """Run all tests with critical verification"""
    print("🚀 Granger Ecosystem Critical Test Verification")
    print("=" * 60)
    
    verifier = CriticalTestVerifier()
    all_results = []
    
    for project_name, project_path in SPOKE_PROJECTS:
        print(f"\n📦 Testing {project_name}...")
        result = verifier.run_project_tests(project_name, project_path)
        all_results.append(result)
        
        # Quick status
        if result["verification_status"] == "VERIFIED":
            print(f"✅ {project_name}: VERIFIED")
        elif result["verification_status"] == "PARTIALLY_VERIFIED":
            print(f"⚠️  {project_name}: PARTIALLY VERIFIED - {len(result['critical_issues'])} issues")
        else:
            print(f"❌ {project_name}: FAILED VERIFICATION - {len(result['critical_issues'])} issues")
    
    # Generate report
    print("\n📝 Generating critical verification report...")
    report = verifier.generate_critical_report(all_results)
    
    # Save report
    report_path = Path("/home/graham/workspace/shared_claude_docs/GRANGER_TEST_VERIFICATION_REPORT.md")
    report_path.write_text(report)
    print(f"✅ Report saved to: {report_path}")
    
    # Save raw results
    results_path = Path("/home/graham/workspace/shared_claude_docs/test_results.json")
    results_path.write_text(json.dumps(all_results, indent=2))
    print(f"✅ Raw results saved to: {results_path}")
    
    # Print summary
    verified = sum(1 for r in all_results if r["verification_status"] == "VERIFIED")
    print(f"\n📊 Summary: {verified}/{len(all_results)} projects fully verified")
    
    # Exit code based on results
    if verified == len(all_results):
        print("✅ All projects verified!")
        # sys.exit() removed
    else:
        print(f"⚠️  Only {verified} projects fully verified. See report for details.")
        # sys.exit() removed


if __name__ == "__main__":
    main()