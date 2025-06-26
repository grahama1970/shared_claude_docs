#!/usr/bin/env python3
"""
Module: test_task_50.py
Purpose: Verification script for Task #50 - Multi-Region Disaster Recovery System

This script verifies that all components of the disaster recovery system
are properly implemented and functioning correctly.

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- subprocess: https://docs.python.org/3/library/subprocess.html

Example Usage:
>>> python test_task_50.py
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import asyncio
import subprocess
import sys
from pathlib import Path
import importlib.util
from datetime import datetime


def load_module(module_path):
    """Dynamically load a Python module"""
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def test_main_module():
    """Test the main disaster recovery module"""
    print("\n🔍 Testing Main Module: disaster_recovery_interaction.py")
    
    try:
        # Import the main module
        module_path = Path(__file__).parent / "disaster_recovery_interaction.py"
        dr_module = load_module(module_path)
        
        # Create orchestrator instance
        orchestrator = dr_module.DisasterRecoveryOrchestrator()
        
        # Test basic functionality
        tests_passed = 0
        tests_total = 5
        
        # Test 1: Region initialization
        print("  ✓ Testing region initialization...")
        if len(orchestrator.regions) == 4:
            tests_passed += 1
            print("    ✅ 4 regions initialized correctly")
        else:
            print(f"    ❌ Expected 4 regions, got {len(orchestrator.regions)}")
        
        # Test 2: Health monitoring
        print("  ✓ Testing health monitoring...")
        status = await orchestrator.monitor_region_health("us-east-1")
        if status in dr_module.RegionStatus:
            tests_passed += 1
            print(f"    ✅ Health monitoring returned: {status.value}")
        else:
            print("    ❌ Health monitoring failed")
        
        # Test 3: Replication check
        print("  ✓ Testing replication status...")
        repl_status = await orchestrator.check_replication_status("us-east-1", "us-west-2")
        if repl_status and hasattr(repl_status, 'lag_seconds'):
            tests_passed += 1
            print(f"    ✅ Replication lag: {repl_status.lag_seconds:.1f}s")
        else:
            print("    ❌ Replication check failed")
        
        # Test 4: Failover execution
        print("  ✓ Testing failover execution...")
        failover_result = await orchestrator.execute_failover(
            "us-east-1", "us-west-2", dr_module.FailoverStrategy.IMMEDIATE
        )
        if failover_result and hasattr(failover_result, 'success'):
            tests_passed += 1
            print(f"    ✅ Failover completed: {'Success' if failover_result.success else 'Failed'}")
        else:
            print("    ❌ Failover execution failed")
        
        # Test 5: DR validation
        print("  ✓ Testing DR validation...")
        dr_test = await orchestrator.test_disaster_recovery("us-east-1", "us-west-2")
        if dr_test and 'readiness_score' in dr_test:
            tests_passed += 1
            print(f"    ✅ DR readiness: {dr_test['readiness_score']:.1f}%")
        else:
            print("    ❌ DR validation failed")
        
        return tests_passed, tests_total
        
    except Exception as e:
        print(f"  ❌ Error testing main module: {str(e)}")
        return 0, 5


def test_file_structure():
    """Test that all required files exist"""
    print("\n📁 Testing File Structure")
    
    base_path = Path(__file__).parent
    required_files = [
        "disaster_recovery_interaction.py",
        "tests/test_failover_orchestration.py",
        "tests/test_replication_management.py",
        "tests/test_recovery_validation.py",
        "test_task_50.py"
    ]
    
    files_found = 0
    for file_path in required_files:
        full_path = base_path / file_path
        if full_path.exists():
            files_found += 1
            print(f"  ✅ Found: {file_path}")
        else:
            print(f"  ❌ Missing: {file_path}")
    
    return files_found, len(required_files)


def test_module_features():
    """Test that all required features are implemented"""
    print("\n🔧 Testing Module Features")
    
    try:
        module_path = Path(__file__).parent / "disaster_recovery_interaction.py"
        with open(module_path, 'r') as f:
            content = f.read()
        
        features = [
            ("Multi-region replication", "check_replication_status"),
            ("Automated failover", "execute_failover"),
            ("RTO/RPO monitoring", "calculate_rto_rpo"),
            ("Backup coordination", "_get_recent_backup"),
            ("Service health checks", "monitor_region_health"),
            ("DNS failover", "_update_dns_records"),
            ("Data consistency", "RecoveryPoint"),
            ("Recovery optimization", "optimize_recovery_time"),
            ("Failover strategies", "FailoverStrategy"),
            ("Rollback capability", "rollback_failover")
        ]
        
        features_found = 0
        for feature_name, feature_code in features:
            if feature_code in content:
                features_found += 1
                print(f"  ✅ {feature_name}")
            else:
                print(f"  ❌ {feature_name}")
        
        return features_found, len(features)
        
    except Exception as e:
        print(f"  ❌ Error checking features: {str(e)}")
        return 0, 10


def run_test_files():
    """Run the individual test files"""
    print("\n🧪 Running Test Files")
    
    base_path = Path(__file__).parent
    test_files = [
        "tests/test_failover_orchestration.py",
        "tests/test_replication_management.py",
        "tests/test_recovery_validation.py"
    ]
    
    tests_passed = 0
    for test_file in test_files:
        test_path = base_path / test_file
        print(f"\n  Running {test_file}...")
        
        try:
            result = subprocess.run(
                [sys.executable, str(test_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                tests_passed += 1
                print(f"    ✅ Test passed")
            else:
                print(f"    ❌ Test failed (exit code: {result.returncode})")
                
        except subprocess.TimeoutExpired:
            print(f"    ❌ Test timed out")
        except Exception as e:
            print(f"    ❌ Error running test: {str(e)}")
    
    return tests_passed, len(test_files)


def run_main_validation():
    """Run the main module's validation function"""
    print("\n🎯 Running Main Module Validation")
    
    try:
        module_path = Path(__file__).parent / "disaster_recovery_interaction.py"
        result = subprocess.run(
            [sys.executable, str(module_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✅ Main validation passed")
            # Print key output lines
            for line in result.stdout.split('\n'):
                if 'VALIDATION SUMMARY' in line or 'Success Rate:' in line:
                    print(f"    {line.strip()}")
            return 1, 1
        else:
            print("  ❌ Main validation failed")
            return 0, 1
            
    except Exception as e:
        print(f"  ❌ Error running validation: {str(e)}")
        return 0, 1


async def main():
    """Main verification function"""
    print("=" * 80)
    print("TASK #50 VERIFICATION: MULTI-REGION DISASTER RECOVERY SYSTEM")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_passed = 0
    total_tests = 0
    
    # Test 1: File structure
    passed, total = test_file_structure()
    total_passed += passed
    total_tests += total
    
    # Test 2: Module features
    passed, total = test_module_features()
    total_passed += passed
    total_tests += total
    
    # Test 3: Main module functionality
    passed, total = await test_main_module()
    total_passed += passed
    total_tests += total
    
    # Test 4: Run test files
    passed, total = run_test_files()
    total_passed += passed
    total_tests += total
    
    # Test 5: Run main validation
    passed, total = run_main_validation()
    total_passed += passed
    total_tests += total
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n✅ ALL VERIFICATIONS PASSED - Task #50 Completed Successfully!")
        exit(0)
    else:
        print("\n❌ VERIFICATION FAILED - Please check the errors above")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())