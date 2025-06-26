"""
Test Task #54: Performance Profiler Integration
Tests comprehensive performance profiling capabilities
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import subprocess
import sys
from pathlib import Path

def run_test(test_name: str, file_path: str) -> bool:
    """Run a test file and return success status"""
    print(f"\n{'='*60}")
    print(f"Running {test_name}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            cwd=str(Path(file_path).parent.parent)
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Failed to run {test_name}: {e}")
        return False

def main():
    """Run all tests for Task #54"""
    base_dir = Path(__file__).parent / "performance-profiler"
    
    # Define test files
    tests = [
        ("Main Module Validation", base_dir / "performance_profiler_interaction.py"),
        ("CPU Profiling Tests", base_dir / "tests" / "test_cpu_profiling.py"),
        ("Memory Profiling Tests", base_dir / "tests" / "test_memory_profiling.py"),
        ("Bottleneck Detection Tests", base_dir / "tests" / "test_bottleneck_detection.py"),
    ]
    
    # Track results
    results = []
    
    # Run each test
    for test_name, test_file in tests:
        if not test_file.exists():
            print(f"ERROR: {test_file} not found!")
            results.append((test_name, False))
            continue
            
        success = run_test(test_name, test_file)
        results.append((test_name, success))
    
    # Summary
    print("\n" + "="*60)
    print("TASK #54 TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    # Check if directory should be renamed
    if base_dir.name == "performance-profiler" and passed_tests == total_tests:
        new_name = base_dir.parent / "performance_profiler"
        print(f"\n✅ All tests passed! Ready to rename {base_dir.name} to {new_name.name}")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    # sys.exit() removed