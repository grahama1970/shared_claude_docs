#!/usr/bin/env python3
"""
Module: verify_module_implementation.py
Description: Comprehensive check of module implementation status

External Dependencies:
- None (uses standard library only)

Example Usage:
>>> python verify_module_implementation.py
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
import sys

def run_module_test(module_path: str, test_file: str) -> dict:
    """Run a specific test file and capture results."""
    result = {
        'test_file': test_file,
        'passed': False,
        'error': None,
        'output': None
    }
    
    try:
        # Run pytest on the specific test
        cmd = [sys.executable, '-m', 'pytest', test_file, '-v', '--tb=short']
        
        process = subprocess.run(
            cmd,
            cwd=module_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        result['output'] = process.stdout[:1000]  # First 1000 chars
        result['return_code'] = process.returncode
        result['passed'] = process.returncode == 0
        
        if process.stderr:
            result['error'] = process.stderr[:500]
            
    except subprocess.TimeoutExpired:
        result['error'] = 'Test timed out after 30 seconds'
    except Exception as e:
        result['error'] = str(e)
    
    return result

def analyze_module(module_path: str, module_name: str) -> dict:
    """Analyze a module in detail."""
    print(f"\n🔍 Analyzing {module_name}...")
    
    module_dir = Path(module_path)
    analysis = {
        'module': module_name,
        'path': module_path,
        'has_venv': False,
        'has_requirements': False,
        'has_pyproject': False,
        'main_files': [],
        'test_results': [],
        'import_test': False
    }
    
    # Check for virtual environment
    venv_path = module_dir / '.venv'
    analysis['has_venv'] = venv_path.exists()
    
    # Check for requirements
    requirements = module_dir / 'requirements.txt'
    pyproject = module_dir / 'pyproject.toml'
    analysis['has_requirements'] = requirements.exists()
    analysis['has_pyproject'] = pyproject.exists()
    
    # Find main implementation files
    src_dir = module_dir / 'src'
    if src_dir.exists():
        for py_file in src_dir.rglob('*.py'):
            if '.venv' not in str(py_file) and '__pycache__' not in str(py_file):
                analysis['main_files'].append(str(py_file.relative_to(module_dir)))
    
    # Test simple import
    src_path = module_dir / 'src'
    if src_path.exists():
        sys.path.insert(0, str(src_path))
        try:
            module_import_name = module_name.lower().replace('-', '_').replace(' ', '_')
            exec(f"import {module_import_name}")
            analysis['import_test'] = True
            print(f"  ✅ Can import {module_import_name}")
        except Exception as e:
            print(f"  ❌ Cannot import: {e}")
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))
    
    # Run a simple test
    test_dir = module_dir / 'tests'
    if test_dir.exists():
        # Find a simple test file
        test_files = list(test_dir.glob('test_*.py'))
        if test_files:
            # Pick the first non-honeypot test
            for test_file in test_files[:3]:  # Try up to 3 tests
                if 'honeypot' not in str(test_file):
                    print(f"  🧪 Running {test_file.name}...")
                    result = run_module_test(str(module_dir), str(test_file))
                    analysis['test_results'].append(result)
                    if result['passed']:
                        print(f"    ✅ Test passed!")
                        break
                    else:
                        print(f"    ❌ Test failed")
    
    return analysis

def main():
    """Verify module implementations."""
    modules = [
        ('/home/graham/workspace/experiments/sparta', 'SPARTA'),
        ('/home/graham/workspace/experiments/youtube_transcripts', 'YouTube Transcripts'),
        ('/home/graham/workspace/experiments/claude-test-reporter', 'Claude Test Reporter'),
    ]
    
    print("🚀 Granger Module Implementation Verification")
    print("=" * 80)
    print(f"Timestamp: {datetime.now()}")
    
    all_results = []
    
    for module_path, module_name in modules:
        analysis = analyze_module(module_path, module_name)
        all_results.append(analysis)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    
    working_modules = []
    for result in all_results:
        status = "❌"
        if result['import_test']:
            status = "✅"
            if any(tr['passed'] for tr in result['test_results']):
                status = "✅✅"
                working_modules.append(result)
        
        print(f"\n{status} {result['module']}:")
        print(f"   - Can import: {'Yes' if result['import_test'] else 'No'}")
        print(f"   - Has .venv: {'Yes' if result['has_venv'] else 'No'}")
        print(f"   - Tests run: {len(result['test_results'])}")
        print(f"   - Tests passed: {sum(1 for tr in result['test_results'] if tr['passed'])}")
        print(f"   - Main files: {len(result['main_files'])}")
    
    print("\n🎯 RECOMMENDATION:")
    if working_modules:
        best = working_modules[0]
        print(f"✅ Start with {best['module']} - it has working imports and passing tests")
        print(f"   Path: {best['path']}")
        print("\n   Next steps:")
        print("   1. cd to the module directory")
        print("   2. Activate its virtual environment: source .venv/bin/activate")
        print("   3. Run its test suite: pytest tests/")
    else:
        print("⚠️  No modules have both working imports and passing tests")
        print("   Manual investigation needed")
    
    # Save detailed results
    output_file = Path('module_verification_report.json')
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': str(datetime.now()),
            'modules': all_results,
            'working_count': len(working_modules)
        }, f, indent=2)
    print(f"\n📄 Detailed report saved to: {output_file}")

if __name__ == "__main__":
    main()