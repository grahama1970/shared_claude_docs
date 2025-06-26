#!/usr/bin/env python3
"""
Simple Project Health Check
Focuses on basic validation without complex Git operations
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

class ProjectHealthChecker:
    """Simple health checker for all projects"""
    
    def __init__(self, config_file='cleanup_config_localhost.json'):
        config_path = Path(__file__).parent / config_file
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.report_dir = Path(__file__).parent / 'health_reports' / self.timestamp
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def run_command(self, cmd: str, cwd: Path) -> Tuple[str, str, int]:
        """Run a command safely"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, 
                text=True, cwd=str(cwd), timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return '', str(e), -1
    
    def check_project(self, project_path: Path) -> Dict[str, Any]:
        """Run basic health checks on a project"""
        project_name = project_path.name
        print(f"\n🔍 Checking: {project_name}")
        
        result = {
            'project': project_name,
            'path': str(project_path),
            'checks': {},
            'issues': [],
            'warnings': []
        }
        
        # Check 1: Project exists
        if not project_path.exists():
            result['checks']['exists'] = False
            result['issues'].append('Project directory not found')
            return result
        result['checks']['exists'] = True
        
        # Check 2: Essential files
        essential_files = {
            'README.md': project_path / 'README.md',
            'pyproject.toml': project_path / 'pyproject.toml',
            '.gitignore': project_path / '.gitignore'
        }
        
        for name, path in essential_files.items():
            result['checks'][f'has_{name}'] = path.exists()
            if not path.exists():
                result['warnings'].append(f'Missing {name}')
        
        # Check 3: Project structure
        src_variations = [
            project_path / 'src',
            project_path / project_name.replace('-', '_'),
            project_path / 'src' / project_name.replace('-', '_')
        ]
        
        has_src = any(d.exists() for d in src_variations)
        result['checks']['has_src'] = has_src
        if not has_src:
            result['issues'].append('No source code directory found')
        
        # Check 4: Tests
        tests_dir = project_path / 'tests'
        result['checks']['has_tests'] = tests_dir.exists()
        if tests_dir.exists():
            test_files = list(tests_dir.glob('test_*.py')) + list(tests_dir.glob('*_test.py'))
            result['checks']['test_count'] = len(test_files)
        else:
            result['warnings'].append('No tests directory')
            result['checks']['test_count'] = 0
        
        # Check 5: Git repository
        git_dir = project_path / '.git'
        result['checks']['has_git'] = git_dir.exists()
        if not git_dir.exists():
            result['warnings'].append('Not a Git repository')
        
        # Check 6: Virtual environment
        venv_paths = [project_path / '.venv', project_path / 'venv']
        result['checks']['has_venv'] = any(p.exists() for p in venv_paths)
        if not result['checks']['has_venv']:
            result['warnings'].append('No virtual environment')
        
        # Check 7: Basic pyproject.toml validation
        pyproject_path = project_path / 'pyproject.toml'
        if pyproject_path.exists():
            try:
                # Just check if it's valid TOML
                import toml
                with open(pyproject_path, 'r') as f:
                    data = toml.load(f)
                result['checks']['valid_toml'] = True
                
                # Check for claude-test-reporter
                deps_str = str(data)
                result['checks']['has_test_reporter'] = 'claude-test-reporter' in deps_str
                if not result['checks']['has_test_reporter']:
                    result['warnings'].append('Missing claude-test-reporter dependency')
                    
            except Exception as e:
                result['checks']['valid_toml'] = False
                result['issues'].append(f'Invalid pyproject.toml: {str(e)[:100]}')
        
        # Check 8: Code quality indicators
        if has_src:
            # Count Python files
            py_files = list(project_path.rglob('*.py'))
            result['checks']['python_files'] = len(py_files)
            
            # Check for TODO/FIXME
            todo_count = 0
            for py_file in py_files[:20]:  # Check first 20 files
                try:
                    with open(py_file, 'r') as f:
                        content = f.read()
                        todo_count += content.count('TODO') + content.count('FIXME')
                except:
                    pass
            result['checks']['todo_count'] = todo_count
            if todo_count > 50:
                result['warnings'].append(f'High technical debt: {todo_count} TODOs')
        
        # Calculate health score
        critical_checks = ['exists', 'has_src', 'valid_toml']
        important_checks = ['has_README.md', 'has_tests', 'has_git', 'has_test_reporter']
        
        critical_pass = all(result['checks'].get(c, False) for c in critical_checks)
        important_pass = sum(result['checks'].get(c, False) for c in important_checks)
        
        if not critical_pass:
            result['health'] = 'critical'
        elif important_pass >= 3:
            result['health'] = 'good'
        elif important_pass >= 2:
            result['health'] = 'fair'
        else:
            result['health'] = 'poor'
        
        # Print summary
        health_emoji = {
            'good': '✅',
            'fair': '⚠️',
            'poor': '❌',
            'critical': '💀'
        }.get(result['health'], '❓')
        
        print(f"  {health_emoji} Health: {result['health']}")
        print(f"  📊 Issues: {len(result['issues'])}, Warnings: {len(result['warnings'])}")
        
        return result
    
    def generate_report(self, results: List[Dict[str, Any]]):
        """Generate health report"""
        print(f"\n\n{'='*70}")
        print("📊 PROJECT HEALTH SUMMARY")
        print(f"{'='*70}")
        
        # Count by health status
        health_counts = {}
        for r in results:
            health = r.get('health', 'unknown')
            health_counts[health] = health_counts.get(health, 0) + 1
        
        print(f"\nProjects analyzed: {len(results)}")
        for health, count in sorted(health_counts.items()):
            emoji = {'good': '✅', 'fair': '⚠️', 'poor': '❌', 'critical': '💀'}.get(health, '❓')
            print(f"  {emoji} {health}: {count}")
        
        # Projects needing attention
        critical = [r for r in results if r['health'] in ['critical', 'poor']]
        if critical:
            print(f"\n⚠️  Projects needing immediate attention:")
            for project in critical:
                print(f"  - {project['project']}: {', '.join(project['issues'][:2])}")
        
        # Common issues
        all_issues = []
        all_warnings = []
        for r in results:
            all_issues.extend(r['issues'])
            all_warnings.extend(r['warnings'])
        
        if all_issues:
            print(f"\n❌ Most common issues:")
            from collections import Counter
            for issue, count in Counter(all_issues).most_common(5):
                print(f"  - {issue}: {count} projects")
        
        if all_warnings:
            print(f"\n⚠️  Most common warnings:")
            from collections import Counter
            for warning, count in Counter(all_warnings).most_common(5):
                print(f"  - {warning}: {count} projects")
        
        # Save detailed report
        report_file = self.report_dir / 'health_report.json'
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': self.timestamp,
                'summary': health_counts,
                'results': results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Create markdown report
        md_file = self.report_dir / 'health_report.md'
        with open(md_file, 'w') as f:
            f.write(f"# Project Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"Total projects: {len(results)}\n\n")
            f.write("| Health | Count |\n")
            f.write("|--------|-------|\n")
            for health, count in sorted(health_counts.items()):
                f.write(f"| {health} | {count} |\n")
            
            f.write("\n## Project Details\n\n")
            f.write("| Project | Health | Tests | Git | Venv | Issues | Warnings |\n")
            f.write("|---------|--------|-------|-----|------|--------|----------|\n")
            
            for r in sorted(results, key=lambda x: x['project']):
                f.write(f"| {r['project']} | {r['health']} | "
                       f"{r['checks'].get('test_count', '-')} | "
                       f"{'✓' if r['checks'].get('has_git') else '✗'} | "
                       f"{'✓' if r['checks'].get('has_venv') else '✗'} | "
                       f"{len(r['issues'])} | {len(r['warnings'])} |\n")
        
        print(f"📄 Markdown report saved to: {md_file}")
        
        # Quick fixes script
        self.generate_quick_fixes_script(results)
    
    def generate_quick_fixes_script(self, results: List[Dict[str, Any]]):
        """Generate a script with quick fixes for common issues"""
        script_file = self.report_dir / 'quick_fixes.sh'
        
        with open(script_file, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# Quick fixes for common project issues\n\n")
            
            for r in results:
                if r['issues'] or r['warnings']:
                    f.write(f"\n# {r['project']}\n")
                    project_path = r['path']
                    
                    if not r['checks'].get('has_git'):
                        f.write(f"cd {project_path} && git init\n")
                    
                    if not r['checks'].get('has_venv'):
                        f.write(f"cd {project_path} && python -m venv .venv\n")
                    
                    if not r['checks'].get('has_README.md'):
                        f.write(f"touch {project_path}/README.md\n")
                    
                    if not r['checks'].get('has_.gitignore'):
                        f.write(f"cp /path/to/template/.gitignore {project_path}/\n")
        
        os.chmod(script_file, 0o755)
        print(f"\n🔧 Quick fixes script saved to: {script_file}")
    
    def run(self):
        """Run health check on all projects"""
        results = []
        
        for project_path in self.config['projects']:
            project_path = Path(project_path)
            try:
                result = self.check_project(project_path)
                results.append(result)
            except Exception as e:
                print(f"❌ Error checking {project_path.name}: {e}")
                results.append({
                    'project': project_path.name,
                    'path': str(project_path),
                    'health': 'error',
                    'issues': [str(e)]
                })
        
        self.generate_report(results)
        
        # Return exit code based on critical issues
        critical_count = sum(1 for r in results if r.get('health') == 'critical')
        return 1 if critical_count > 0 else 0

def main():
    """Run project health check"""
    try:
        # Check if toml is available
        try:
            import toml
        except ImportError:
            print("Installing toml package...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'toml'])
            import toml
        
        checker = ProjectHealthChecker()
        exit_code = checker.run()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()