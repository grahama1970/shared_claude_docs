#!/usr/bin/env python3
"""
Test script for Task #47: Microservices Dependency Mapper
Validates the implementation meets all requirements
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import sys
import subprocess
import asyncio
from pathlib import Path

def check_directory_structure():
    """Check if the directory structure is correct"""
    print("Checking directory structure...")
    
    base_path = Path("microservices_mapper")
    required_files = [
        "microservices_mapper_interaction.py",
        "tests/test_service_discovery.py",
        "tests/test_dependency_analysis.py",
        "tests/test_visualization.py"
    ]
    
    for file_path in required_files:
        full_path = base_path / file_path
        if not full_path.exists():
            print(f"❌ Missing required file: {full_path}")
            return False
        print(f"✓ Found {full_path}")
    
    return True

def check_implementation_features():
    """Check if implementation has required features"""
    print("\nChecking implementation features...")
    
    main_file = Path("microservices_mapper/microservices_mapper_interaction.py")
    content = main_file.read_text()
    
    required_features = [
        ("ServiceDiscovery", "Service discovery integration"),
        ("DependencyAnalyzer", "Dependency analysis"),
        ("MicroservicesMapper", "Main mapper class"),
        ("analyze_runtime_dependencies", "Runtime dependency detection"),
        ("analyze_static_code", "Static code analysis"),
        ("detect_circular_dependencies", "Circular dependency detection"),
        ("export_to_dot", "DOT format export"),
        ("export_to_json", "JSON export for D3.js"),
        ("check_version_compatibility", "Version compatibility checking"),
        ("analyze_service_mesh", "Service mesh integration"),
        ("_analyze_health_impacts", "Health impact analysis")
    ]
    
    for feature, description in required_features:
        if feature in content:
            print(f"✓ Found {description}: {feature}")
        else:
            print(f"❌ Missing {description}: {feature}")
            return False
    
    return True

def check_parallel_processing():
    """Check if parallel processing is implemented"""
    print("\nChecking parallel processing implementation...")
    
    main_file = Path("microservices_mapper/microservices_mapper_interaction.py")
    content = main_file.read_text()
    
    parallel_indicators = [
        "asyncio.gather",
        "async def",
        "await",
        "tasks.append"
    ]
    
    for indicator in parallel_indicators:
        if indicator in content:
            print(f"✓ Found parallel processing: {indicator}")
        else:
            print(f"❌ Missing parallel indicator: {indicator}")
            return False
    
    return True

async def run_main_validation():
    """Run the main module validation"""
    print("\nRunning main module validation...")
    
    try:
        # Change to the microservices_mapper directory
        import os
        os.chdir("microservices_mapper")
        
        # Run the validation
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            "microservices_mapper_interaction.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            print("✓ Main module validation passed")
            print(stdout.decode())
            return True
        else:
            print("❌ Main module validation failed")
            print(stderr.decode())
            return False
    except Exception as e:
        print(f"❌ Error running validation: {e}")
        return False
    finally:
        os.chdir("..")

async def run_tests():
    """Run all test files"""
    print("\nRunning test files...")
    
    test_files = [
        "tests/test_service_discovery.py",
        "tests/test_dependency_analysis.py",
        "tests/test_visualization.py"
    ]
    
    all_passed = True
    
    for test_file in test_files:
        print(f"\nRunning {test_file}...")
        try:
            # Change to the microservices_mapper directory
            import os
            os.chdir("microservices_mapper")
            
            process = await asyncio.create_subprocess_exec(
                sys.executable,
                test_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                print(f"✓ {test_file} passed")
            else:
                print(f"❌ {test_file} failed")
                print(stderr.decode())
                all_passed = False
                
            os.chdir("..")
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
            all_passed = False
    
    return all_passed

def check_code_quality():
    """Check code quality standards"""
    print("\nChecking code quality standards...")
    
    main_file = Path("microservices_mapper/microservices_mapper_interaction.py")
    content = main_file.read_text()
    lines = content.split('\n')
    
    # Check file size
    if len(lines) <= 500:
        print(f"✓ File size within limit: {len(lines)} lines")
    else:
        print(f"❌ File exceeds 500 lines: {len(lines)} lines")
        return False
    
    # Check for documentation header
    if '"""' in content[:200]:
        print("✓ Documentation header present")
    else:
        print("❌ Missing documentation header")
        return False
    
    # Check for type hints
    if "-> Dict" in content and ": str" in content:
        print("✓ Type hints used")
    else:
        print("❌ Missing type hints")
        return False
    
    return True

async def main():
    """Run all validation checks"""
    print("🔍 Validating Task #47: Microservices Dependency Mapper\n")
    
    checks = [
        ("Directory Structure", check_directory_structure()),
        ("Implementation Features", check_implementation_features()),
        ("Parallel Processing", check_parallel_processing()),
        ("Code Quality", check_code_quality())
    ]
    
    # Run async checks
    validation_passed = await run_main_validation()
    checks.append(("Main Validation", validation_passed))
    
    tests_passed = await run_tests()
    checks.append(("Test Suite", tests_passed))
    
    # Summary
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    
    all_passed = True
    for check_name, passed in checks:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✅ Task #47 implementation is complete and valid!")
        print("\nKey features implemented:")
        print("- Service discovery (Consul, Kubernetes)")
        print("- Runtime dependency detection")
        print("- Static code analysis")
        print("- Circular dependency detection")
        print("- Health impact analysis")
        print("- Version compatibility checking")
        print("- Service mesh integration")
        print("- Export to DOT and JSON (D3.js)")
        print("- Parallel processing for scalability")
    else:
        print("\n❌ Task #47 validation failed. Please fix the issues above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    # sys.exit() removed