#!/usr/bin/env python3
"""
Enhanced Project Cleanup Utility for Claude Code
Comprehensive validation and cleanup for all companion projects
"""

import json
import os
import subprocess
import sys
import re
import asyncio
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import argparse
from typing import Dict, List, Any, Optional, Tuple
import traceback

# Try to import optional dependencies
try:
    import toml
    HAS_TOML = True
except ImportError:
    HAS_TOML = False
    print("Warning: toml not installed. Some features will be limited.")

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Warning: tqdm not installed. Progress bars disabled.")


class EnhancedCleanupUtility:
    """Enhanced cleanup utility with comprehensive project validation"""
    
    def __init__(self, config_file='cleanup_config.json', verbose=False, dry_run=False):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        self.verbose = verbose
        self.dry_run = dry_run
        self.report_dir = Path('cleanup_reports')
        self.report_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        
        # Project-specific configurations
        self.project_configs = {
            'sparta': {
                'type': 'framework',
                'requires_tests': True,
                'requires_docs': True,
                'check_imports': ['torch', 'transformers']
            },
            'marker': {
                'type': 'tool',
                'requires_cli': True,
                'requires_tests': True,
                'check_commands': True
            },
            'arangodb': {
                'type': 'database',
                'requires_config': True,
                'check_connection': True
            },
            'youtube_transcripts': {
                'type': 'tool',
                'requires_api_keys': True,
                'check_imports': ['youtube_dl', 'whisper']
            },
            'claude_max_proxy': {
                'type': 'proxy',
                'requires_config': True,
                'check_endpoints': True
            },
            'arxiv-mcp-server': {
                'type': 'mcp',
                'requires_mcp': True,
                'check_mcp_methods': True
            },
            'granger_hub': {
                'type': 'hub',
                'requires_tests': True,
                'check_inter_project': True
            },
            'claude-test-reporter': {
                'type': 'testing',
                'requires_tests': True,
                'is_dependency': True
            },
            'unsloth_wip': {
                'type': 'experimental',
                'wip': True,
                'check_imports': ['unsloth', 'torch']
            },
            'marker-ground-truth': {
                'type': 'dataset',
                'requires_data': True,
                'check_structure': True
            },
            'mcp-screenshot': {
                'type': 'mcp',
                'requires_mcp': True,
                'check_mcp_methods': True,
                'check_imports': ['PIL', 'screenshot']
            }
        }
        
    def run_command(self, cmd: str, cwd: Optional[str] = None, timeout: int = 30) -> Tuple[str, str, int]:
        """Run a command and return output"""
        if self.verbose:
            print(f"  Running: {cmd}")
        
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, 
                text=True, cwd=cwd, timeout=timeout
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return '', f'Command timed out after {timeout}s', -1
        except Exception as e:
            return '', str(e), -1
    
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Comprehensive project analysis"""
        project_path = Path(project_path)
        project_name = project_path.name
        
        print(f"\n{'='*60}")
        print(f"Processing: {project_path}")
        print(f"{'='*60}")
        
        if not project_path.exists():
            print(f"Error: Project directory not found")
            return {'status': 'not_found', 'project': str(project_path)}
        
        # Get project-specific config
        project_config = self.project_configs.get(project_name, {})
        
        results = {
            'project': str(project_path),
            'name': project_name,
            'type': project_config.get('type', 'unknown'),
            'timestamp': self.timestamp,
            'issues': [],
            'warnings': [],
            'suggestions': [],
            'validations': {},
            'status': 'analyzing'
        }
        
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project_path)
        
        try:
            # Run all validations
            self._validate_documentation(project_path, results)
            self._validate_dependencies(project_path, results, project_config)
            self._validate_code_structure(project_path, results, project_config)
            self._validate_tests(project_path, results, project_config)
            self._validate_slash_commands(project_path, results)
            self._validate_mcp_implementation(project_path, results, project_config)
            self._validate_readme_features(project_path, results)
            self._check_security(project_path, results)
            self._check_code_quality(project_path, results)
            
            # Project-specific validations
            if project_config.get('requires_cli'):
                self._validate_cli_interface(project_path, results)
            
            if project_config.get('check_imports'):
                self._validate_required_imports(project_path, results, project_config['check_imports'])
            
            if project_config.get('check_inter_project'):
                self._validate_inter_project_communication(project_path, results)
            
            # Determine final status
            if not results['issues']:
                results['status'] = 'success'
            elif any('test' in issue.lower() and 'fail' in issue.lower() for issue in results['issues']):
                results['status'] = 'failed'
            else:
                results['status'] = 'issues'
                
        finally:
            os.chdir(original_dir)
        
        return results
    
    def _validate_documentation(self, project_path: Path, results: Dict[str, Any]):
        """Validate project documentation"""
        print("📚 Checking documentation...")
        
        # Check README.md
        readme_path = project_path / 'README.md'
        if readme_path.exists():
            print("  ✅ README.md found")
            results['validations']['readme'] = True
            
            # Check README content quality
            with open(readme_path, 'r') as f:
                content = f.read()
                
            # Check for essential sections
            essential_sections = ['installation', 'usage', 'requirements']
            missing_sections = []
            for section in essential_sections:
                if section not in content.lower():
                    missing_sections.append(section)
            
            if missing_sections:
                results['warnings'].append(f"README.md missing sections: {', '.join(missing_sections)}")
                
        else:
            print("  ❌ No README.md found")
            results['issues'].append('Missing README.md')
            results['validations']['readme'] = False
        
        # Check CLAUDE.md
        claude_path = project_path / 'CLAUDE.md'
        if claude_path.exists():
            print("  ✅ CLAUDE.md found")
            results['validations']['claude_md'] = True
        else:
            print("  ⚠️  No CLAUDE.md found")
            results['suggestions'].append('Consider adding CLAUDE.md for AI interaction guidelines')
            results['validations']['claude_md'] = False
    
    def _validate_dependencies(self, project_path: Path, results: Dict[str, Any], config: Dict[str, Any]):
        """Validate project dependencies"""
        print("📦 Checking dependencies...")
        
        # Check pyproject.toml
        pyproject_path = project_path / 'pyproject.toml'
        if pyproject_path.exists():
            results['validations']['pyproject'] = True
            
            # Check for claude-test-reporter
            with open(pyproject_path, 'r') as f:
                content = f.read()
            
            if 'claude-test-reporter' in content:
                print("  ✅ claude-test-reporter configured")
                results['validations']['claude_test_reporter'] = True
            else:
                print("  ❌ claude-test-reporter missing")
                results['issues'].append('Missing claude-test-reporter in pyproject.toml')
                results['validations']['claude_test_reporter'] = False
                
                # Add it if not in dry-run mode
                if not self.dry_run and HAS_TOML:
                    self._add_test_reporter(pyproject_path)
            
            # Check for security vulnerabilities
            if not config.get('wip', False):
                stdout, _, _ = self.run_command('pip-audit --desc 2>/dev/null || true')
                if 'vulnerabilit' in stdout.lower():
                    results['warnings'].append('Security vulnerabilities found in dependencies')
                    
        else:
            print("  ⚠️  No pyproject.toml found")
            results['issues'].append('Missing pyproject.toml')
            results['validations']['pyproject'] = False
        
        # Check requirements.txt as fallback
        requirements_path = project_path / 'requirements.txt'
        if requirements_path.exists() and not pyproject_path.exists():
            print("  ⚠️  Using requirements.txt (consider migrating to pyproject.toml)")
            results['suggestions'].append('Consider migrating from requirements.txt to pyproject.toml')
    
    def _validate_code_structure(self, project_path: Path, results: Dict[str, Any], config: Dict[str, Any]):
        """Validate code structure and organization"""
        print("🏗️  Checking code structure...")
        
        # Check for proper package structure
        src_dir = project_path / 'src'
        if src_dir.exists():
            print("  ✅ src/ directory found")
            results['validations']['src_structure'] = True
        else:
            # Check for alternative structures
            module_dir = project_path / project_path.name.replace('-', '_')
            if module_dir.exists():
                print(f"  ✅ {module_dir.name}/ directory found")
                results['validations']['src_structure'] = True
            else:
                print("  ⚠️  No standard package structure found")
                results['warnings'].append('Non-standard package structure')
                results['validations']['src_structure'] = False
        
        # Check for misplaced files
        stdout, _, _ = self.run_command('find . -name "*.py" -not -path "./src/*" -not -path "./tests/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./build/*" -not -path "./dist/*" -not -name "setup.py" -not -name "conf*.py" -type f')
        misplaced_files = [f for f in stdout.strip().split('\n') if f and not f.startswith('./')]
        
        if misplaced_files:
            print(f"  ⚠️  Found {len(misplaced_files)} potentially misplaced Python files")
            results['warnings'].append(f"Potentially misplaced Python files: {len(misplaced_files)}")
            results['validations']['file_organization'] = False
        else:
            results['validations']['file_organization'] = True
    
    def _validate_tests(self, project_path: Path, results: Dict[str, Any], config: Dict[str, Any]):
        """Validate and run tests"""
        print("🧪 Checking tests...")
        
        tests_dir = project_path / 'tests'
        if not tests_dir.exists():
            if config.get('requires_tests', True) and not config.get('wip', False):
                print("  ❌ No tests directory found")
                results['issues'].append('Missing tests directory')
                results['validations']['has_tests'] = False
            else:
                print("  ⚠️  No tests directory (acceptable for this project type)")
                results['validations']['has_tests'] = False
            return
        
        print("  ✅ tests/ directory found")
        results['validations']['has_tests'] = True
        
        # Count test files
        test_files = list(tests_dir.glob('test_*.py'))
        if not test_files:
            print("  ⚠️  No test files found")
            results['warnings'].append('Tests directory exists but contains no test files')
            return
        
        print(f"  Found {len(test_files)} test files")
        
        # Run tests if not in dry-run mode
        if not self.dry_run:
            print("  Running tests...")
            # First check if pytest is available
            _, _, pytest_check = self.run_command('which pytest', timeout=5)
            if pytest_check != 0:
                print("    ⚠️  pytest not available, skipping test execution")
                results['warnings'].append('pytest not installed')
                return
                
            stdout, stderr, returncode = self.run_command(
                'pytest -v tests/ --tb=short 2>&1 || true',
                timeout=120
            )
            
            if 'error' in stderr.lower() and returncode == -1:
                print("    ⚠️  Test execution error")
                results['warnings'].append('Test execution failed - check test environment')
                return
            
            if returncode == 0:
                print("    ✅ All tests passed")
                results['validations']['tests_pass'] = True
                
                # Extract test statistics
                import re
                match = re.search(r'(\d+) passed', stdout)
                if match:
                    results['test_count'] = int(match.group(1))
                    
            else:
                print("    ❌ Tests failed")
                results['issues'].append('Tests failed')
                results['validations']['tests_pass'] = False
                
                # Extract failure information
                failures = re.findall(r'FAILED (.*?) -', stdout)
                if failures:
                    results['test_failures'] = failures[:5]  # First 5 failures
    
    def _validate_slash_commands(self, project_path: Path, results: Dict[str, Any]):
        """Validate slash command implementations"""
        # Check if this is a Claude-related project
        is_claude_project = False
        
        readme_path = project_path / 'README.md'
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read().lower()
            if any(kw in content for kw in ['claude', 'assistant', 'cli', 'command', 'slash']):
                is_claude_project = True
        
        if (project_path / 'CLAUDE.md').exists():
            is_claude_project = True
        
        if not is_claude_project:
            return
        
        print("🔧 Checking slash commands...")
        results['validations']['slash_commands'] = {}
        
        # Check for slash command documentation
        stdout, _, _ = self.run_command('grep -E "^/[a-zA-Z]+" README.md CLAUDE.md 2>/dev/null || true')
        documented_commands = re.findall(r'/[a-zA-Z]+', stdout)
        
        if documented_commands:
            print(f"  ✅ Found {len(documented_commands)} documented slash commands")
            results['validations']['slash_commands']['documented'] = documented_commands
        else:
            print("  ⚠️  No slash commands documented")
            results['warnings'].append('No slash commands documented for Claude project')
        
        # Check for implementation
        stdout, _, _ = self.run_command('find . -name "*.py" | xargs grep -l "handle_command\\|command_handler\\|slash_command\\|@command" 2>/dev/null || true')
        if stdout.strip():
            print("  ✅ Command handler implementation found")
            results['validations']['slash_commands']['implemented'] = True
        else:
            print("  ❌ No command handler implementation found")
            if documented_commands:
                results['issues'].append('Slash commands documented but not implemented')
            results['validations']['slash_commands']['implemented'] = False
    
    def _validate_mcp_implementation(self, project_path: Path, results: Dict[str, Any], config: Dict[str, Any]):
        """Validate MCP (Model Context Protocol) implementation"""
        # Check if this is an MCP project
        is_mcp = config.get('type') == 'mcp' or 'mcp' in project_path.name.lower()
        
        if not is_mcp and project_path.joinpath('README.md').exists():
            with open(project_path / 'README.md', 'r') as f:
                content = f.read().lower()
            if any(term in content for term in ['mcp', 'model context protocol']):
                is_mcp = True
        
        if not is_mcp:
            return
        
        print("🔌 Checking MCP implementation...")
        results['validations']['mcp'] = {}
        
        # Check for MCP configuration
        config_files = ['mcp.json', 'server.json', '.mcp/config.json']
        config_found = False
        for cf in config_files:
            if (project_path / cf).exists():
                print(f"  ✅ MCP configuration found: {cf}")
                results['validations']['mcp']['config'] = cf
                config_found = True
                break
        
        if not config_found:
            print("  ❌ No MCP configuration file found")
            results['issues'].append('Missing MCP configuration file')
            results['validations']['mcp']['config'] = None
        
        # Check for required MCP methods
        required_methods = ['handle_request', 'handle_response', 'get_capabilities', 'initialize']
        missing_methods = []
        
        for method in required_methods:
            stdout, _, returncode = self.run_command(f'find . -name "*.py" | xargs grep -q "def {method}" 2>/dev/null')
            if returncode != 0:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"  ❌ Missing MCP methods: {', '.join(missing_methods)}")
            results['issues'].append(f"Missing MCP methods: {', '.join(missing_methods)}")
            results['validations']['mcp']['methods'] = False
        else:
            print("  ✅ All required MCP methods found")
            results['validations']['mcp']['methods'] = True
        
        # Check MCP dependencies
        if (project_path / 'pyproject.toml').exists():
            with open(project_path / 'pyproject.toml', 'r') as f:
                content = f.read()
            if not re.search(r'mcp|model-context-protocol', content, re.IGNORECASE):
                print("  ⚠️  MCP dependencies not found in pyproject.toml")
                results['warnings'].append('MCP dependencies not declared in pyproject.toml')
    
    def _validate_readme_features(self, project_path: Path, results: Dict[str, Any]):
        """Validate that README claims match actual implementation"""
        readme_path = project_path / 'README.md'
        if not readme_path.exists():
            return
        
        print("📋 Validating README claims...")
        
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        
        # Extract feature claims
        feature_patterns = [
            r'[*-]\s+(.*?(?:feature|capability|support|provide|implement).*?)(?:\n|$)',
            r'##\s+Features?\s*\n(.*?)(?:\n##|\Z)',
        ]
        
        claimed_features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, readme_content, re.IGNORECASE | re.DOTALL | re.MULTILINE)
            claimed_features.extend(matches)
        
        if not claimed_features:
            return
        
        # Check for implementations
        unimplemented = []
        for feature in claimed_features[:10]:  # Check first 10 features
            # Extract potential class/function names
            key_terms = re.findall(r'\b[A-Z][a-zA-Z]+\b|\b[a-z]+_[a-z]+\b', feature)
            
            implemented = False
            for term in key_terms[:3]:  # Check first 3 terms
                stdout, _, returncode = self.run_command(
                    f'find . -name "*.py" | xargs grep -l "class {term}\\|def {term}" 2>/dev/null | head -1'
                )
                if stdout.strip():
                    implemented = True
                    break
            
            if not implemented and key_terms:
                unimplemented.append(feature[:100])
        
        if unimplemented:
            print(f"  ⚠️  {len(unimplemented)} claimed features may lack implementation")
            results['warnings'].append(f"Some README features may lack implementation")
        else:
            print("  ✅ README features appear to be implemented")
    
    def _validate_cli_interface(self, project_path: Path, results: Dict[str, Any]):
        """Validate CLI interface for tools"""
        print("🖥️  Checking CLI interface...")
        
        # Check for CLI entry points
        cli_indicators = [
            '__main__.py',
            'cli.py',
            'main.py',
            'console_scripts'  # in setup.py or pyproject.toml
        ]
        
        cli_found = False
        for indicator in cli_indicators:
            if indicator == 'console_scripts':
                # Check in pyproject.toml
                if (project_path / 'pyproject.toml').exists():
                    with open(project_path / 'pyproject.toml', 'r') as f:
                        if 'console_scripts' in f.read():
                            cli_found = True
                            break
            else:
                # Check for files
                stdout, _, _ = self.run_command(f'find . -name "{indicator}" -type f | head -1')
                if stdout.strip():
                    cli_found = True
                    break
        
        if cli_found:
            print("  ✅ CLI interface found")
            results['validations']['cli'] = True
        else:
            print("  ❌ No CLI interface found")
            results['issues'].append('No CLI interface found for tool project')
            results['validations']['cli'] = False
    
    def _validate_required_imports(self, project_path: Path, results: Dict[str, Any], required_imports: List[str]):
        """Check for required imports in the project"""
        print(f"📥 Checking required imports: {', '.join(required_imports)}...")
        
        missing_imports = []
        for import_name in required_imports:
            stdout, _, returncode = self.run_command(
                f'find . -name "*.py" | xargs grep -l "import {import_name}\\|from {import_name}" 2>/dev/null | head -1'
            )
            if not stdout.strip():
                missing_imports.append(import_name)
        
        if missing_imports:
            print(f"  ⚠️  Missing imports: {', '.join(missing_imports)}")
            results['warnings'].append(f"Expected imports not found: {', '.join(missing_imports)}")
        else:
            print("  ✅ All required imports found")
    
    def _validate_inter_project_communication(self, project_path: Path, results: Dict[str, Any]):
        """Validate inter-project communication capabilities"""
        print("🔗 Checking inter-project communication...")
        
        # Check for imports from other projects
        other_projects = [
            'sparta', 'marker', 'arangodb', 'youtube_transcripts',
            'claude_max_proxy', 'arxiv-mcp-server', 'granger_hub',
            'claude-test-reporter', 'unsloth_wip', 'marker-ground-truth', 'mcp-screenshot'
        ]
        
        imports_found = []
        for project in other_projects:
            stdout, _, _ = self.run_command(
                f'find . -name "*.py" | xargs grep -l "from {project}\\|import {project}" 2>/dev/null || true'
            )
            if stdout.strip():
                imports_found.append(project)
        
        if imports_found:
            print(f"  ✅ Communicates with: {', '.join(imports_found)}")
            results['validations']['inter_project'] = imports_found
        else:
            print("  ⚠️  No inter-project imports found")
            results['validations']['inter_project'] = []
    
    def _check_security(self, project_path: Path, results: Dict[str, Any]):
        """Basic security checks"""
        print("🔒 Running security checks...")
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            stdout, _, _ = self.run_command(
                f'find . -name "*.py" | xargs grep -E "{pattern}" 2>/dev/null || true'
            )
            if stdout.strip():
                print("  ⚠️  Potential hardcoded secrets found")
                results['warnings'].append('Potential hardcoded secrets detected')
                break
        else:
            print("  ✅ No obvious hardcoded secrets")
    
    def _check_code_quality(self, project_path: Path, results: Dict[str, Any]):
        """Basic code quality checks"""
        print("📊 Checking code quality...")
        
        # Count TODO/FIXME comments
        stdout, _, _ = self.run_command(
            'find . -name "*.py" | xargs grep -E "TODO|FIXME|HACK|XXX" 2>/dev/null | wc -l || echo 0'
        )
        todo_count = int(stdout.strip() or 0)
        
        if todo_count > 0:
            print(f"  ⚠️  Found {todo_count} TODO/FIXME comments")
            if todo_count > 10:
                results['warnings'].append(f'High technical debt: {todo_count} TODO/FIXME comments')
        else:
            print("  ✅ No TODO/FIXME comments")
        
        # Check for very long files
        stdout, _, _ = self.run_command(
            'find . -name "*.py" -exec wc -l {} + | sort -rn | head -5'
        )
        long_files = []
        for line in stdout.strip().split('\n'):
            if line and not line.endswith('total'):
                parts = line.strip().split()
                if len(parts) >= 2 and parts[0].isdigit():
                    line_count = int(parts[0])
                    if line_count > 500:
                        long_files.append(f"{parts[1]} ({line_count} lines)")
        
        if long_files:
            print(f"  ⚠️  Found {len(long_files)} files over 500 lines")
            results['suggestions'].append('Consider refactoring large files')
    
    def _add_test_reporter(self, pyproject_path: Path):
        """Add claude-test-reporter to pyproject.toml"""
        if not HAS_TOML:
            print("    ⚠️  Cannot add claude-test-reporter (toml package not installed)")
            return False
        
        try:
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
    
    async def test_inter_project_communication(self, projects: List[str]) -> Dict[str, Any]:
        """Test communication between projects"""
        results = {}
        
        # Test a few key communication paths
        key_paths = [
            ('granger_hub', 'sparta'),
            ('granger_hub', 'marker'),
            ('marker', 'marker-ground-truth'),
            ('claude-test-reporter', 'sparta')
        ]
        
        for proj1_name, proj2_name in key_paths:
            proj1 = next((p for p in projects if proj1_name in p), None)
            proj2 = next((p for p in projects if proj2_name in p), None)
            
            if proj1 and proj2:
                # Simple import test
                test_cmd = f'''cd {proj2} && python -c "
import sys
sys.path.insert(0, '{proj1}')
try:
    import importlib
    # Try to import the main module
    module_name = '{Path(proj1).name}'.replace('-', '_')
    importlib.import_module(module_name)
    print('SUCCESS')
except Exception as e:
    print(f'FAILED: {{e}}')"
'''
                stdout, _, _ = self.run_command(test_cmd)
                
                key = f"{proj1_name} -> {proj2_name}"
                results[key] = 'SUCCESS' in stdout
        
        return results
    
    def run(self, parallel: bool = True) -> List[Dict[str, Any]]:
        """Run cleanup on all projects"""
        print("🚀 Enhanced Project Cleanup Utility")
        print(f"Timestamp: {self.timestamp}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print(f"Projects to process: {len(self.config['projects'])}")
        print("")
        
        all_results = []
        
        if parallel and len(self.config['projects']) > 1:
            # Process projects in parallel using ThreadPoolExecutor instead of ProcessPoolExecutor
            # to avoid pickling issues with instance methods
            with ThreadPoolExecutor(max_workers=self.config.get('parallel_workers', 4)) as executor:
                if HAS_TQDM:
                    from tqdm import tqdm
                    futures = []
                    for project in self.config['projects']:
                        future = executor.submit(self.analyze_project, project)
                        futures.append((project, future))
                    
                    with tqdm(total=len(futures), desc="Processing projects") as pbar:
                        for project, future in futures:
                            try:
                                result = future.result(timeout=300)  # 5 minute timeout per project
                                all_results.append(result)
                            except Exception as e:
                                print(f"\n❌ Error processing {project}: {e}")
                                all_results.append({
                                    'project': project,
                                    'name': Path(project).name,
                                    'status': 'error',
                                    'error': str(e),
                                    'issues': [f'Processing error: {e}']
                                })
                            pbar.update(1)
                else:
                    futures = []
                    for project in self.config['projects']:
                        future = executor.submit(self.analyze_project, project)
                        futures.append((project, future))
                    
                    for i, (project, future) in enumerate(futures):
                        print(f"Processing {i+1}/{len(futures)}: {Path(project).name}")
                        try:
                            result = future.result(timeout=300)
                            all_results.append(result)
                        except Exception as e:
                            print(f"❌ Error: {e}")
                            all_results.append({
                                'project': project,
                                'name': Path(project).name,
                                'status': 'error',
                                'error': str(e),
                                'issues': [f'Processing error: {e}']
                            })
        else:
            # Process sequentially
            for i, project in enumerate(self.config['projects']):
                if len(self.config['projects']) > 1:
                    print(f"\nProcessing {i+1}/{len(self.config['projects'])}: {Path(project).name}")
                try:
                    result = self.analyze_project(project)
                    all_results.append(result)
                except Exception as e:
                    print(f"❌ Error processing {project}: {e}")
                    if self.verbose:
                        traceback.print_exc()
                    all_results.append({
                        'project': project,
                        'name': Path(project).name,
                        'status': 'error', 
                        'error': str(e),
                        'issues': [f'Processing error: {e}']
                    })
        
        # Test inter-project communication
        print("\n🔗 Testing inter-project communication...")
        comm_results = asyncio.run(
            self.test_inter_project_communication(self.config['projects'])
        )
        
        # Save individual reports
        for result in all_results:
            project_name = result.get('name', 'unknown')
            report_file = self.report_dir / f"{self.timestamp}-{project_name}.json"
            with open(report_file, 'w') as f:
                json.dump(result, f, indent=2)
        
        # Generate comprehensive report
        self.generate_comprehensive_report(all_results, comm_results)
        
        return all_results
    
    def generate_comprehensive_report(self, all_results: List[Dict[str, Any]], comm_results: Dict[str, bool]):
        """Generate a comprehensive markdown report"""
        report_file = self.report_dir / f"comprehensive_report_{self.timestamp}.md"
        
        with open(report_file, 'w') as f:
            f.write("# 🚀 Enhanced Project Cleanup Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}\n\n")
            
            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            
            total = len(all_results)
            successful = sum(1 for r in all_results if r.get('status') == 'success')
            failed = sum(1 for r in all_results if r.get('status') == 'failed')
            issues = sum(1 for r in all_results if r.get('status') == 'issues')
            not_found = sum(1 for r in all_results if r.get('status') == 'not_found')
            
            f.write(f"- **Total Projects**: {total}\n")
            f.write(f"- **✅ Successful**: {successful} ({successful/total*100:.1f}%)\n")
            f.write(f"- **❌ Failed**: {failed} ({failed/total*100:.1f}%)\n")
            f.write(f"- **⚠️  Has Issues**: {issues} ({issues/total*100:.1f}%)\n")
            f.write(f"- **🚫 Not Found**: {not_found}\n\n")
            
            # Project Matrix
            f.write("## 📋 Project Status Matrix\n\n")
            f.write("| Project | Type | Status | Tests | Docs | Dependencies | Issues |\n")
            f.write("|---------|------|--------|-------|------|--------------|--------|\n")
            
            for result in sorted(all_results, key=lambda x: x.get('name', '')):
                status_icon = {
                    'success': '✅',
                    'failed': '❌',
                    'issues': '⚠️',
                    'not_found': '🚫'
                }.get(result.get('status', 'unknown'), '❓')
                
                tests_icon = '✅' if result.get('validations', {}).get('tests_pass') else '❌'
                docs_icon = '✅' if result.get('validations', {}).get('readme') else '❌'
                deps_icon = '✅' if result.get('validations', {}).get('claude_test_reporter') else '❌'
                issue_count = len(result.get('issues', []))
                
                f.write(f"| {result.get('name', 'Unknown')} | {result.get('type', 'unknown')} | "
                       f"{status_icon} | {tests_icon} | {docs_icon} | {deps_icon} | {issue_count} |\n")
            
            # Inter-project Communication
            f.write("\n## 🔗 Inter-Project Communication\n\n")
            if comm_results:
                f.write("| From | To | Status |\n")
                f.write("|------|-----|--------|\n")
                for path, success in comm_results.items():
                    status = '✅' if success else '❌'
                    from_proj, to_proj = path.split(' -> ')
                    f.write(f"| {from_proj} | {to_proj} | {status} |\n")
            else:
                f.write("No inter-project communication tests performed.\n")
            
            # Detailed Results
            f.write("\n## 📝 Detailed Project Reports\n\n")
            
            for result in sorted(all_results, key=lambda x: x.get('name', '')):
                if result.get('status') == 'not_found':
                    continue
                    
                f.write(f"### {result.get('name', 'Unknown')}\n\n")
                f.write(f"- **Type**: {result.get('type', 'unknown')}\n")
                f.write(f"- **Status**: {result.get('status', 'unknown')}\n")
                
                # Issues
                if result.get('issues'):
                    f.write(f"\n#### 🔴 Issues ({len(result['issues'])})\n")
                    for issue in result['issues']:
                        f.write(f"- {issue}\n")
                
                # Warnings
                if result.get('warnings'):
                    f.write(f"\n#### 🟡 Warnings ({len(result['warnings'])})\n")
                    for warning in result['warnings']:
                        f.write(f"- {warning}\n")
                
                # Suggestions
                if result.get('suggestions'):
                    f.write(f"\n#### 💡 Suggestions ({len(result['suggestions'])})\n")
                    for suggestion in result['suggestions']:
                        f.write(f"- {suggestion}\n")
                
                # Validations summary
                validations = result.get('validations', {})
                if validations:
                    f.write("\n#### ✅ Validations\n")
                    for key, value in validations.items():
                        if isinstance(value, bool):
                            icon = '✅' if value else '❌'
                            f.write(f"- {icon} {key.replace('_', ' ').title()}\n")
                
                f.write("\n---\n\n")
            
            # Recommendations
            f.write("## 🎯 Recommendations\n\n")
            
            # Critical issues
            critical_projects = [r for r in all_results if r.get('status') == 'failed']
            if critical_projects:
                f.write("### 🚨 Critical - Fix Immediately\n")
                for proj in critical_projects:
                    f.write(f"- **{proj['name']}**: {', '.join(proj.get('issues', ['Test failures']))}\n")
                f.write("\n")
            
            # Missing documentation
            no_docs = [r for r in all_results if not r.get('validations', {}).get('readme')]
            if no_docs:
                f.write("### 📚 Documentation Needed\n")
                for proj in no_docs:
                    f.write(f"- {proj['name']}: Add README.md\n")
                f.write("\n")
            
            # Missing tests
            no_tests = [r for r in all_results if not r.get('validations', {}).get('has_tests')]
            if no_tests:
                f.write("### 🧪 Tests Needed\n")
                for proj in no_tests:
                    f.write(f"- {proj['name']}: Add test suite\n")
                f.write("\n")
            
            f.write("\n## 🏁 Next Steps\n\n")
            f.write("1. Address all critical issues (failed tests)\n")
            f.write("2. Add missing documentation (README.md, CLAUDE.md)\n")
            f.write("3. Ensure all projects have claude-test-reporter configured\n")
            f.write("4. Implement missing slash commands for Claude projects\n")
            f.write("5. Complete MCP implementations where required\n")
            f.write("6. Add test suites for projects lacking tests\n")
            f.write("7. Review and address security warnings\n")
            
        print(f"\n📄 Comprehensive report saved to: {report_file}")
        
        # Also save a quick summary
        summary_file = self.report_dir / f"summary_{self.timestamp}.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Enhanced Cleanup Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n")
            f.write(f"Total: {total} | Success: {successful} | Failed: {failed} | Issues: {issues}\n")
            f.write(f"{'='*50}\n")
            for result in all_results:
                status = result.get('status', 'unknown')
                issues = len(result.get('issues', []))
                f.write(f"{result.get('name', 'Unknown'):.<30} {status:.<15} {issues} issues\n")
        
        print(f"📄 Quick summary saved to: {summary_file}")


def main():
    parser = argparse.ArgumentParser(description='Enhanced Project Cleanup Utility')
    parser.add_argument('--config', default='cleanup_config.json', help='Configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--dry-run', action='store_true', help='Perform dry run without making changes')
    parser.add_argument('--sequential', action='store_true', help='Process projects sequentially')
    
    args = parser.parse_args()
    
    # Update config for localhost
    if Path(args.config).exists():
        with open(args.config, 'r') as f:
            config = json.load(f)
        
        # Remove SSH-related config for localhost
        if 'connection_command' in config:
            del config['connection_command']
        
        # Save updated config
        with open(args.config, 'w') as f:
            json.dump(config, f, indent=2)
    
    utility = EnhancedCleanupUtility(
        config_file=args.config,
        verbose=args.verbose,
        dry_run=args.dry_run
    )
    
    results = utility.run(parallel=not args.sequential)
    
    # Print quick summary
    print("\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
    
    total = len(results)
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    print(f"Total projects: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {successful/total*100:.1f}%")
    
    if failed > 0:
        print("\n⚠️  Some projects have critical issues that need attention!")
        sys.exit(1)
    else:
        print("\n✅ All projects processed successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()