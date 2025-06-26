#!/usr/bin/env python3
"""
Module: fix_critical_test_issues.py
Description: Fix critical test issues systematically

External Dependencies:
- None

Example Usage:
>>> python fix_critical_test_issues.py
"""

import os
import sys
import subprocess
import re
import ast
from pathlib import Path
from datetime import datetime


def fix_indentation_errors(file_path):
    """Fix indentation errors in Python files."""
    try:
        content = file_path.read_text()
        
        # Try to parse to find indentation issues
        try:
            ast.parse(content)
            return False  # No syntax errors
        except IndentationError as e:
            lines = content.split('\n')
            line_num = e.lineno - 1
            
            if line_num > 0 and line_num < len(lines):
                # Check if the previous line ends with a colon
                prev_line = lines[line_num - 1].strip()
                current_line = lines[line_num]
                
                if prev_line.endswith(':'):
                    # Add proper indentation
                    indent = len(lines[line_num - 1]) - len(lines[line_num - 1].lstrip())
                    lines[line_num] = ' ' * (indent + 4) + current_line.lstrip()
                    
                    content = '\n'.join(lines)
                    file_path.write_text(content)
                    return True
        except SyntaxError as e:
            # Handle specific syntax errors
            if "from __future__" in str(e):
                # Fix __future__ import position
                lines = content.split('\n')
                future_imports = []
                other_lines = []
                
                for line in lines:
                    if line.strip().startswith('from __future__ import'):
                        future_imports.append(line)
                    else:
                        other_lines.append(line)
                
                if future_imports:
                    # Put __future__ imports at the very top
                    new_content = '\n'.join(future_imports) + '\n' + '\n'.join(other_lines)
                    file_path.write_text(new_content)
                    return True
                    
            elif "invalid syntax" in str(e) and "# REMOVED:" in content:
                # Fix broken mock removal
                content = re.sub(r'for \w+ in # REMOVED: .*', 'pass  # Mock loop removed', content)
                file_path.write_text(content)
                return True
                
    except Exception:
        pass
    
    return False


def fix_missing_dependencies(project_path):
    """Install missing dependencies."""
    deps_to_install = {
        "numpy": "numpy",
        "playwright": "playwright",
        "transformers": "transformers",
        "torch": "torch",
    }
    
    installed = []
    
    for module, package in deps_to_install.items():
        try:
            # Check if module can be imported
            cmd = ['bash', '-c', f'cd {project_path} && source .venv/bin/activate && python -c "import {module}" 2>&1']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                # Install the package
                install_cmd = ['bash', '-c', f'cd {project_path} && source .venv/bin/activate && uv pip install {package}']
                subprocess.run(install_cmd)
                installed.append(package)
        except:
            pass
            
    return installed


def fix_import_paths(file_path):
    """Fix incorrect import paths."""
    try:
        content = file_path.read_text()
        
        # Fix relative imports from analyzers
        if "from analyzers." in content:
            content = content.replace("from analyzers.", "from claude_test_reporter.analyzers.")
            file_path.write_text(content)
            return True
            
        # Fix missing module prefix
        if "from core." in content and "claude_test_reporter" not in content:
            content = re.sub(r'from core\.', 'from claude_test_reporter.core.', content)
            file_path.write_text(content)
            return True
            
    except:
        pass
        
    return False


def create_missing_files(project_path):
    """Create missing required files."""
    created = []
    
    # Create .env.example if missing
    env_example = project_path / ".env.example"
    if not env_example.exists():
        env_example.write_text("""PYTHONPATH=./src

# API Keys (optional)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
ARANGO_HOST=http://localhost:8529
ARANGO_USER=root
ARANGO_PASSWORD=openSesame

# Service URLs
GRANGER_HUB_URL=http://localhost:8000
LLM_CALL_URL=http://localhost:8001
TEST_REPORTER_URL=http://localhost:8002
""")
        created.append(".env.example")
        
    # Copy to .env if missing
    env_file = project_path / ".env"
    if not env_file.exists() and env_example.exists():
        env_file.write_text(env_example.read_text())
        created.append(".env")
        
    return created


def fix_specific_project_critical_issues(project_name, project_path):
    """Fix critical issues for specific projects."""
    fixes = []
    
    if project_name == "granger_hub":
        # Fix test file with indentation error
        test_file = project_path / "tests/core/adapters/test_adapter_framework.py"
        if test_file.exists() and fix_indentation_errors(test_file):
            fixes.append("Fixed indentation in test_adapter_framework.py")
            
    elif project_name == "sparta":
        # Fix syntax error in honeypot test
        test_file = project_path / "tests/sparta/integration/test_honeypot.py"
        if test_file.exists():
            try:
                content = test_file.read_text()
                content = re.sub(r'for module in # REMOVED:.*', 'pass  # Mock loop removed', content)
                test_file.write_text(content)
                fixes.append("Fixed syntax error in honeypot test")
            except:
                pass
                
    elif project_name == "claude-test-reporter":
        # Fix import path
        monitor_file = project_path / "src/claude_test_reporter/monitoring/hallucination_monitor.py"
        if monitor_file.exists() and fix_import_paths(monitor_file):
            fixes.append("Fixed import paths in hallucination_monitor.py")
            
    elif project_name == "world_model":
        # Create missing .env.example
        created = create_missing_files(project_path)
        if created:
            fixes.extend([f"Created {f}" for f in created])
            
    return fixes


def run_quick_test(project_path):
    """Run a quick test to check if basics work."""
    cmd = [
        'bash', '-c',
        f'cd {project_path} && source .venv/bin/activate && '
        f'python -m pytest --collect-only -q 2>&1 | head -20'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        # Check for collection success
        if "collected" in result.stdout and "error" not in result.stdout.lower():
            # Extract number of tests collected
            import re
            match = re.search(r'collected (\d+) items?', result.stdout)
            if match:
                return int(match.group(1)), None
        
        # Return error if present
        if "error" in result.stdout.lower() or result.returncode != 0:
            return 0, result.stdout + result.stderr
            
    except:
        pass
        
    return 0, "Unknown error"


def main():
    """Fix critical test issues."""
    projects = [
        ("granger_hub", "/home/graham/workspace/experiments/granger_hub"),
        ("rl_commons", "/home/graham/workspace/experiments/rl_commons"),
        ("world_model", "/home/graham/workspace/experiments/world_model"),
        ("claude-test-reporter", "/home/graham/workspace/experiments/claude-test-reporter"),
        ("sparta", "/home/graham/workspace/experiments/sparta"),
        ("marker", "/home/graham/workspace/experiments/marker"),
        ("arangodb", "/home/graham/workspace/experiments/arangodb"),
        ("llm_call", "/home/graham/workspace/experiments/llm_call"),
        ("unsloth_wip", "/home/graham/workspace/experiments/unsloth_wip"),
        ("youtube_transcripts", "/home/graham/workspace/experiments/youtube_transcripts"),
        ("darpa_crawl", "/home/graham/workspace/experiments/darpa_crawl"),
        ("gitget", "/home/graham/workspace/experiments/gitget"),
        ("arxiv-mcp-server", "/home/graham/workspace/mcp-servers/arxiv-mcp-server"),
        ("mcp-screenshot", "/home/graham/workspace/experiments/mcp-screenshot"),
        ("chat", "/home/graham/workspace/experiments/chat"),
        ("annotator", "/home/graham/workspace/experiments/annotator"),
        ("aider-daemon", "/home/graham/workspace/experiments/aider-daemon"),
        ("runpod_ops", "/home/graham/workspace/experiments/runpod_ops"),
    ]
    
    print("🔧 Fixing Critical Test Issues")
    print("=" * 60)
    
    working_projects = 0
    
    for project_name, project_path in projects:
        project_path = Path(project_path)
        if not project_path.exists():
            continue
            
        print(f"\n📦 {project_name}")
        print("-" * 40)
        
        all_fixes = []
        
        # 1. Fix Python syntax issues in all test files
        for test_file in project_path.rglob("test_*.py"):
            if ".venv" in str(test_file) or "archive" in str(test_file):
                continue
                
            if fix_indentation_errors(test_file):
                all_fixes.append(f"Fixed indentation in {test_file.name}")
                
            if fix_import_paths(test_file):
                all_fixes.append(f"Fixed imports in {test_file.name}")
                
        # 2. Fix project-specific critical issues
        specific_fixes = fix_specific_project_critical_issues(project_name, project_path)
        all_fixes.extend(specific_fixes)
        
        # 3. Install missing dependencies
        installed = fix_missing_dependencies(project_path)
        if installed:
            all_fixes.append(f"Installed: {', '.join(installed)}")
            
        # 4. Create missing files
        created = create_missing_files(project_path)
        if created:
            all_fixes.extend([f"Created {f}" for f in created])
            
        # Print fixes
        if all_fixes:
            for fix in all_fixes:
                print(f"  ✓ {fix}")
        else:
            print("  ℹ️  No critical issues found")
            
        # 5. Quick test
        print("  🧪 Quick test...")
        tests_collected, error = run_quick_test(project_path)
        
        if tests_collected > 0:
            print(f"  ✅ Can collect {tests_collected} tests")
            working_projects += 1
        elif error:
            # Show first error line
            first_error = error.split('\n')[0]
            print(f"  ❌ Collection failed: {first_error}")
        else:
            print(f"  ⚠️  No tests collected")
            
    print(f"\n{'='*60}")
    print(f"Summary: {working_projects}/{len(projects)} projects can collect tests")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())