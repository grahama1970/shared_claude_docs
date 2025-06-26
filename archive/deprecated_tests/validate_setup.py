"""
Validate the setup for Task #001 tests.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import sys
from pathlib import Path
import importlib.util


def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return Path(filepath).exists()


def check_import(module_path: str) -> bool:
    """Check if a module can be imported."""
    try:
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False
    return False


def main():
    """Run validation checks."""
    print("Validating Task #001 Setup")
    print("=" * 60)
    
    checks = [
        ("Self-evolution module", "self_evolution_interaction.py"),
        ("Test suite", "tests/interactions/test_self_evolution.py"),
        ("Honeypot tests", "tests/test_honeypot.py"),
        ("Test runner", "run_task_001_tests.py"),
        ("Requirements", "requirements.txt"),
        ("README", "README.md"),
    ]
    
    all_good = True
    
    print("\nFile Existence Checks:")
    for name, filepath in checks:
        exists = check_file_exists(filepath)
        status = "✅" if exists else "❌"
        print(f"  {status} {name}: {filepath}")
        all_good &= exists
    
    print("\nModule Import Checks:")
    modules = [
        ("Self-evolution", "self_evolution_interaction.py"),
        ("Tests", "tests/interactions/test_self_evolution.py"),
    ]
    
    for name, filepath in modules:
        can_import = check_import(filepath)
        status = "✅" if can_import else "❌"
        print(f"  {status} {name} imports correctly")
        all_good &= can_import
    
    print("\nPython Package Checks:")
    packages = ["arxiv", "pytest"]
    for package in packages:
        try:
            __import__(package)
            print(f"  ✅ {package} is installed")
        except ImportError:
            print(f"  ❌ {package} is NOT installed")
            print(f"     Run: pip install -r requirements.txt")
            all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All checks passed! Ready to run Task #001 tests.")
        print("\nRun tests with: python run_task_001_tests.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())