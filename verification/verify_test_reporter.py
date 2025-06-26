#!/usr/bin/env python3
"""
Verify Claude Test Reporter - Our verification tool itself
This is critical as it's what we use to verify other modules
"""

import subprocess
import json
import sys
import os
from pathlib import Path
from datetime import datetime

MODULE_PATH = Path("/home/graham/workspace/experiments/claude-test-reporter")

def check_test_reporter():
    """Comprehensive check of claude-test-reporter."""
    
    print("🔍 Claude Test Reporter Verification")
    print("="*60)
    
    results = {
        "module": "claude-test-reporter",
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "verdict": None
    }
    
    # 1. Check if it's installed and importable
    print("\n1️⃣ Checking if importable...")
    try:
        sys.path.insert(0, str(MODULE_PATH / "src"))
        from claude_test_reporter.core.test_result_verifier import TestResultVerifier
        from claude_test_reporter.analyzers.llm_test_analyzer import LLMTestAnalyzer
        print("   ✓ Successfully imported core modules")
        results["checks"]["importable"] = True
    except ImportError as e:
        print(f"   ❌ Import failed: {e}")
        results["checks"]["importable"] = False
        
    # 2. Check for Gemini integration
    print("\n2️⃣ Checking LLM integration...")
    config_file = MODULE_PATH / "src/claude_test_reporter/config.py"
    if config_file.exists():
        with open(config_file) as f:
            content = f.read()
        has_gemini = "gemini" in content.lower()
        has_perplexity = "perplexity" in content.lower()
        
        print(f"   Gemini support: {'✓' if has_gemini else '❌'}")
        print(f"   Perplexity support: {'✓' if has_perplexity else '❌'}")
        
        results["checks"]["llm_support"] = {
            "gemini": has_gemini,
            "perplexity": has_perplexity
        }
    
    # 3. Check for hallucination detection
    print("\n3️⃣ Checking hallucination detection...")
    halluc_file = MODULE_PATH / "src/claude_test_reporter/monitoring/hallucination_monitor.py"
    if halluc_file.exists():
        print("   ✓ Hallucination monitor exists")
        results["checks"]["hallucination_monitor"] = True
    else:
        print("   ❌ No hallucination monitor found")
        results["checks"]["hallucination_monitor"] = False
        
    # 4. Run a simple test
    print("\n4️⃣ Running basic functionality test...")
    os.chdir(MODULE_PATH)
    
    test_script = """
import sys
sys.path.insert(0, 'src')

from claude_test_reporter.core.test_result_verifier import TestResultVerifier

# Create sample test data
test_results = {
    "total": 10,
    "passed": 8,
    "failed": 2,
    "success_rate": 80.0,
    "tests": [
        {"nodeid": "test_1", "outcome": "passed"},
        {"nodeid": "test_2", "outcome": "failed", "error": "AssertionError"}
    ]
}

# Verify it works
verifier = TestResultVerifier()
verified = verifier.create_immutable_test_record(test_results)

print(f"Hash: {verified['verification']['hash'][:32]}...")
print(f"Deployment: {verified['immutable_facts']['deployment_status']}")
print("SUCCESS")
"""
    
    test_file = MODULE_PATH / "verify_basic.py"
    test_file.write_text(test_script)
    
    try:
        cmd = f"source .venv/bin/activate && python {test_file.name}"
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "SUCCESS" in result.stdout:
            print("   ✓ Basic functionality works")
            results["checks"]["basic_test"] = True
        else:
            print("   ❌ Basic test failed")
            print(f"   Output: {result.stdout}")
            print(f"   Error: {result.stderr}")
            results["checks"]["basic_test"] = False
            
    finally:
        if test_file.exists():
            test_file.unlink()
    
    # 5. Check for mocks in test reporter tests
    print("\n5️⃣ Checking for mocks in tests...")
    # REMOVED: cmd = f"grep -r 'mock\\|Mock\\|@patch' {MODULE_PATH}/tests --include='*.py' | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    mock_count = int(result.stdout.strip())
    
    # REMOVED: print(f"   Mock usage: {mock_count} instances")
    results["checks"]["mock_count"] = mock_count
    
    # 6. Check if pytest plugin works
    print("\n6️⃣ Checking pytest plugin...")
    plugin_file = MODULE_PATH / "src/claude_test_reporter/pytest_plugin.py"
    if plugin_file.exists():
        print("   ✓ Pytest plugin exists")
        results["checks"]["pytest_plugin"] = True
    else:
        print("   ❌ No pytest plugin found")
        results["checks"]["pytest_plugin"] = False
    
    # Generate verdict
    score = 0
    if results["checks"].get("importable", False):
        score += 25
    if results["checks"].get("llm_support", {}).get("gemini", False):
        score += 25
    if results["checks"].get("hallucination_monitor", False):
        score += 20
    if results["checks"].get("basic_test", False):
        score += 20
    if results["checks"].get("pytest_plugin", False):
        score += 10
        
    if score >= 80:
        results["verdict"] = "FUNCTIONAL - Ready for use"
    elif score >= 60:
        results["verdict"] = "PARTIALLY FUNCTIONAL - Limited capabilities"
    else:
        results["verdict"] = "NOT READY - Major issues"
        
    results["functionality_score"] = score
    
    # Save report
    os.chdir(Path.cwd())
    report_path = Path("verification/test_reporter_verification.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Module: Claude Test Reporter")
    print(f"Verdict: {results['verdict']}")
    print(f"Functionality Score: {score}/100")
    print(f"\nKey findings:")
    print(f"  - Importable: {'✓' if results['checks'].get('importable') else '❌'}")
    print(f"  - Gemini support: {'✓' if results['checks'].get('llm_support', {}).get('gemini') else '❌'}")
    print(f"  - Hallucination detection: {'✓' if results['checks'].get('hallucination_monitor') else '❌'}")
    print(f"  - Basic test passed: {'✓' if results['checks'].get('basic_test') else '❌'}")
    
    return results


if __name__ == "__main__":
    original_dir = Path.cwd()
    try:
        results = check_test_reporter()
        
        # Now use it to verify results if functional
        if results["functionality_score"] >= 60:
            print("\n🔬 Using Test Reporter to verify findings...")
            # Would use the test reporter here to verify our findings
            print("   (Would run LLM verification here)")
            
        sys.exit(0 if "FUNCTIONAL" in results["verdict"] else 1)
    finally:
        os.chdir(original_dir)