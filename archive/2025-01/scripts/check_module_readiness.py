#!/usr/bin/env python3
"""
Module: check_module_readiness.py
Description: Check readiness of Granger modules by analyzing test infrastructure

External Dependencies:
- None (uses standard library only)

Example Usage:
>>> python check_module_readiness.py
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def check_module_tests(module_path: str, module_name: str) -> dict:
    """Check if a module has real tests."""
    results = {
        'module': module_name,
        'path': module_path,
        'has_tests': False,
        'test_count': 0,
        'skeleton_count': 0,
        'has_pytest': False,
        'has_src': False,
        'real_implementation': False
    }
    
    module_dir = Path(module_path)
    if not module_dir.exists():
        results['error'] = 'Module directory not found'
        return results
    
    # Check for tests
    test_files = list(module_dir.rglob('test_*.py'))
    test_files = [f for f in test_files if '.venv' not in str(f)]
    results['test_count'] = len(test_files)
    results['has_tests'] = len(test_files) > 0
    
    # Check for pytest
    pyproject = module_dir / 'pyproject.toml'
    pytest_ini = module_dir / 'pytest.ini'
    results['has_pytest'] = pyproject.exists() or pytest_ini.exists()
    
    # Check for src directory
    src_dir = module_dir / 'src'
    results['has_src'] = src_dir.exists()
    
    # Count skeleton code indicators
    if src_dir.exists():
        skeleton_count = 0
        for py_file in src_dir.rglob('*.py'):
            if '.venv' in str(py_file):
                continue
            try:
                content = py_file.read_text()
                skeleton_count += content.count('NotImplementedError')
                skeleton_count += len([line for line in content.splitlines() 
                                     if line.strip() == 'pass'])
            except:
                pass
        results['skeleton_count'] = skeleton_count
        results['real_implementation'] = skeleton_count < 20  # Threshold for real code
    
    return results

def main():
    """Check readiness of key Granger modules."""
    modules = [
        ('/home/graham/workspace/experiments/sparta', 'SPARTA'),
        ('/home/graham/workspace/experiments/marker', 'Marker'),
        ('/home/graham/workspace/experiments/arangodb', 'ArangoDB'),
        ('/home/graham/workspace/experiments/youtube_transcripts', 'YouTube Transcripts'),
        ('/home/graham/workspace/experiments/claude-test-reporter', 'Claude Test Reporter'),
    ]
    
    print("🔍 Granger Module Readiness Check")
    print("=" * 80)
    print(f"Timestamp: {datetime.now()}")
    print()
    
    all_results = []
    
    for module_path, module_name in modules:
        print(f"\n📦 Checking {module_name}...")
        results = check_module_tests(module_path, module_name)
        all_results.append(results)
        
        if results.get('error'):
            print(f"  ❌ Error: {results['error']}")
            continue
            
        status_icon = "✅" if results['real_implementation'] else "⚠️"
        print(f"  {status_icon} Implementation: {'Real' if results['real_implementation'] else 'Skeleton'}")
        print(f"  📊 Test files: {results['test_count']}")
        print(f"  🔧 Skeleton indicators: {results['skeleton_count']}")
        print(f"  📁 Has src/: {'Yes' if results['has_src'] else 'No'}")
        print(f"  🧪 Has pytest config: {'Yes' if results['has_pytest'] else 'No'}")
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    ready_modules = [r for r in all_results if r['real_implementation'] and r['has_tests']]
    print(f"\n✅ Modules ready for testing ({len(ready_modules)}):")
    for r in sorted(ready_modules, key=lambda x: x['skeleton_count']):
        print(f"  - {r['module']} (skeleton count: {r['skeleton_count']}, tests: {r['test_count']})")
    
    not_ready = [r for r in all_results if not r['real_implementation']]
    print(f"\n⚠️  Modules not ready ({len(not_ready)}):")
    for r in not_ready:
        print(f"  - {r['module']} (skeleton count: {r['skeleton_count']})")
    
    # Recommendation
    print("\n🎯 RECOMMENDATION:")
    if ready_modules:
        best = ready_modules[0]
        print(f"Start with {best['module']} - it has the most real implementation")
        print(f"Path: {best['path']}")
    else:
        print("No modules appear ready for testing. Manual inspection needed.")
    
    # Save results
    output_file = Path('module_readiness_report.json')
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': str(datetime.now()),
            'modules': all_results,
            'summary': {
                'total': len(all_results),
                'ready': len(ready_modules),
                'not_ready': len(not_ready)
            }
        }, f, indent=2)
    print(f"\n📄 Full report saved to: {output_file}")

if __name__ == "__main__":
    main()