#!/usr/bin/env python3
"""
Simplified Project Cleanup Utility
A more manageable version of the cleanup utility
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SimpleCleanupUtility:
    def __init__(self, config_file='cleanup_config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.report_dir = Path('cleanup_reports')
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
    def run_command(self, cmd, cwd=None):
        """Run a command and return output"""
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, 
                text=True, cwd=cwd, timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return '', str(e), -1
    
    def analyze_project(self, project_path):
        """Analyze a single project"""
        project_path = Path(project_path)
        project_name = project_path.name
        
        print(f"\n{'='*60}")
        print(f"Processing: {project_path}")
        print(f"{'='*60}")
        
        if not project_path.exists():
            print(f"Error: Project directory not found")
            return {'status': 'not_found'}
        
        results = {
            'project': str(project_path),
            'name': project_name,
            'issues': [],
            'status': 'analyzing'
        }
        
        # Change to project directory
        os.chdir(project_path)
        
        # Check for README.md
        if (project_path / 'README.md').exists():
            print("  ✅ README.md found")
        else:
            print("  ⚠️  No README.md found")
            results['issues'].append('Missing README.md')
        
        # Check for pyproject.toml and claude-test-reporter
        pyproject_path = project_path / 'pyproject.toml'
        if pyproject_path.exists():
            with open(pyproject_path, 'r') as f:
                content = f.read()
            if 'claude-test-reporter' in content:
                print("  ✅ claude-test-reporter configured")
            else:
                print("  ❌ claude-test-reporter missing")
                results['issues'].append('Missing claude-test-reporter in pyproject.toml')
                self.add_test_reporter(pyproject_path)
        else:
            print("  ⚠️  No pyproject.toml found")
            results['issues'].append('Missing pyproject.toml')
        
        # Check for Claude-related features
        if (project_path / 'CLAUDE.md').exists() or self.is_claude_project(project_path):
            print("  🔍 Checking slash commands...")
            # Check documentation
            stdout, _, _ = self.run_command('grep -E "/[a-zA-Z]+" README.md CLAUDE.md 2>/dev/null || true')
            if stdout.strip():
                print("    ✅ Slash commands documented")
            else:
                print("    ⚠️  No slash commands documented")
                results['issues'].append('Missing slash command documentation')
            
            # Check implementation
            stdout, _, _ = self.run_command('find . -name "*.py" -type f | xargs grep -l "handle_command\|command_handler" 2>/dev/null || true')
            if stdout.strip():
                print("    ✅ Command handlers found")
            else:
                print("    ❌ No command handlers found")
                results['issues'].append('Missing command handler implementation')
        
        # Check for MCP implementation
        if 'mcp' in project_name.lower() or self.is_mcp_project(project_path):
            print("  🔍 Checking MCP implementation...")
            
            # Check config
            config_files = ['mcp.json', 'server.json', '.mcp/config.json']
            has_config = any((project_path / cf).exists() for cf in config_files)
            if has_config:
                print("    ✅ MCP configuration found")
            else:
                print("    ❌ No MCP configuration file")
                results['issues'].append('Missing MCP configuration file')
            
            # Check required methods
            required_methods = ['handle_request', 'handle_response', 'get_capabilities', 'initialize']
            for method in required_methods:
                stdout, _, returncode = self.run_command(f'find . -name "*.py" | xargs grep -q "def {method}" 2>/dev/null')
                if returncode == 0:
                    print(f"    ✅ Method {method} found")
                else:
                    print(f"    ❌ Method {method} missing")
                    results['issues'].append(f'Missing MCP method: {method}')
        
        # Run tests if available
        if (project_path / 'tests').exists():
            print("  🧪 Running tests...")
            stdout, stderr, returncode = self.run_command('pytest -v tests/ 2>&1 || true')
            if returncode == 0:
                print("    ✅ Tests passed")
                results['tests_passed'] = True
            else:
                print("    ❌ Tests failed")
                results['tests_passed'] = False
                results['issues'].append('Tests failed')
        else:
            print("  ⚠️  No tests directory")
            results['tests_passed'] = None
        
        # Determine final status
        if not results['issues']:
            results['status'] = 'success'
        elif results.get('tests_passed') == False:
            results['status'] = 'failed'
        else:
            results['status'] = 'issues'
        
        return results
    
    def is_claude_project(self, project_path):
        """Check if this is a Claude-related project"""
        readme_path = project_path / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read().lower()
            return any(kw in content for kw in ['claude', 'assistant', 'cli', 'command'])
        return False
    
    def is_mcp_project(self, project_path):
        """Check if this is an MCP project"""
        for file in ['README.md', 'pyproject.toml']:
            file_path = project_path / file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                if any(term in content for term in ['mcp', 'model context protocol', 'mcp-server']):
                    return True
        return False
    
    def add_test_reporter(self, pyproject_path):
        """Add claude-test-reporter to pyproject.toml"""
        try:
            import toml
            with open(pyproject_path, 'r') as f:
                data = toml.load(f)
            
            # Add to dev-dependencies
            if 'tool' not in data:
                data['tool'] = {}
            if 'poetry' not in data['tool']:
                data['tool']['poetry'] = {}
            if 'dev-dependencies' not in data['tool']['poetry']:
                data['tool']['poetry']['dev-dependencies'] = {}
            
            data['tool']['poetry']['dev-dependencies']['claude-test-reporter'] = {
                'git': 'https://github.com/grahama1970/claude-test-reporter.git',
                'branch': 'main'
            }
            
            with open(pyproject_path, 'w') as f:
                toml.dump(data, f)
            
            print("    📦 Added claude-test-reporter to pyproject.toml")
            return True
        except Exception as e:
            print(f"    ❌ Failed to add claude-test-reporter: {e}")
            return False
    
    def run(self):
        """Run cleanup on all projects"""
        print("Enhanced Project Cleanup Utility")
        print(f"Timestamp: {self.timestamp}")
        print(f"Projects to process: {len(self.config['projects'])}")
        
        all_results = []
        
        for project in self.config['projects']:
            results = self.analyze_project(project)
            all_results.append(results)
            
            # Save individual report
            project_name = Path(project).name
            report_file = self.report_dir / f"{self.timestamp}-{project_name}.json"
            with open(report_file, 'w') as f:
                json.dump(results, f, indent=2)
        
        # Generate summary
        self.generate_summary(all_results)
        
        return all_results
    
    def generate_summary(self, all_results):
        """Generate a markdown summary report"""
        summary_file = self.report_dir / f"summary_{self.timestamp}.md"
        
        with open(summary_file, 'w') as f:
            f.write(f"# Project Cleanup Summary\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Statistics
            total = len(all_results)
            successful = sum(1 for r in all_results if r.get('status') == 'success')
            failed = sum(1 for r in all_results if r.get('status') == 'failed')
            issues = sum(1 for r in all_results if r.get('status') == 'issues')
            not_found = sum(1 for r in all_results if r.get('status') == 'not_found')
            
            f.write(f"## Summary\n")
            f.write(f"- Total projects: {total}\n")
            f.write(f"- Successful: {successful}\n")
            f.write(f"- Failed tests: {failed}\n")
            f.write(f"- Has issues: {issues}\n")
            f.write(f"- Not found: {not_found}\n\n")
            
            # Detailed results
            f.write(f"## Project Details\n\n")
            for result in all_results:
                status_icon = {
                    'success': '✅',
                    'failed': '❌',
                    'issues': '⚠️',
                    'not_found': '🚫'
                }.get(result.get('status', 'unknown'), '❓')
                
                f.write(f"### {status_icon} {result.get('name', 'Unknown')}\n")
                f.write(f"- Path: {result.get('project', 'Unknown')}\n")
                f.write(f"- Status: {result.get('status', 'unknown')}\n")
                
                if result.get('issues'):
                    f.write(f"- Issues:\n")
                    for issue in result['issues']:
                        f.write(f"  - {issue}\n")
                f.write("\n")
        
        print(f"\nSummary report saved to: {summary_file}")
        
        # Also print summary to console
        print(f"\n{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Total projects: {total}")
        print(f"Successful: {successful}")
        print(f"Failed tests: {failed}")
        print(f"Has issues: {issues}")
        print(f"Not found: {not_found}")


if __name__ == '__main__':
    utility = SimpleCleanupUtility()
    utility.run()
