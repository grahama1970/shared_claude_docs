#!/usr/bin/env python3
"""
Module: fix_arxiv_all_issues.py
Description: Comprehensive fix for all 141 issues in arxiv_mcp project

This script fixes:
1. Module header syntax errors (28 files)
2. Relative imports (109 instances)
3. Missing dependencies (4 packages)
4. Test honeypot indentation error

External Dependencies:
- ast: Built-in Python AST module
- pathlib: Built-in path handling
"""

import ast
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Set

class ArxivIssueFixer:
    """Fix all issues in arxiv_mcp project."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_root = project_root / "src" / "arxiv_mcp_server"
        self.fixes_applied = {
            "headers": 0,
            "imports": 0,
            "deps": 0,
            "indentation": 0
        }
    
    def fix_module_headers(self) -> int:
        """Fix module header syntax errors."""
        print("\n🔧 Fixing module headers...")
        
        # Pattern to match incorrect headers
        pattern = re.compile(
            r'^("""[^"]+"""\s*)\nModule: ([^\n]+)\nDescription: ([^\n]+)\n',
            re.MULTILINE
        )
        
        files_to_fix = [
            self.src_root / "config_improved.py",
            self.src_root / "logging_config.py", 
            self.src_root / "__main__.py",
            self.src_root / "prompts" / "conversion_guide_prompt.py",
            self.src_root / "prompts" / "handlers.py",
            self.src_root / "prompts" / "prompt_manager.py",
            self.src_root / "prompts" / "__init__.py",
            self.src_root / "prompts" / "deep_research_analysis_prompt.py",
            self.src_root / "prompts" / "comprehensive_research_guide.py",
            self.src_root / "prompts" / "code_analysis_prompt.py",
            self.src_root / "prompts" / "content_description_prompt.py",
            self.src_root / "prompts" / "prompts.py",
            self.src_root / "utils" / "__init__.py",
            self.src_root / "tools" / "summarize_paper.py",
            self.src_root / "tools" / "describe_content.py",
            self.src_root / "tools" / "system_stats.py",
            self.src_root / "tools" / "conversion_options.py",
            self.src_root / "tools" / "search_enhanced.py",
            self.src_root / "tools" / "semantic_search.py",
            self.src_root / "tools" / "analyze_code.py",
            self.src_root / "tools" / "read_paper.py",
            self.src_root / "tools" / "list_papers.py",
            self.src_root / "resources" / "__init__.py",
            self.project_root / "src" / "arxiv_mcp" / "integrations" / "__init__.py",
            self.project_root / "archive" / "deprecated_tests" / "run_tests.py",
            self.project_root / "archive" / "scripts" / "update_search_tqdm.py",
            self.project_root / "archive" / "scripts" / "fix_hardware_display.py"
        ]
        
        fixed = 0
        for file_path in files_to_fix:
            if not file_path.exists():
                print(f"  ⚠️  File not found: {file_path}")
                continue
                
            try:
                content = file_path.read_text()
                
                # Fix the header format
                def replacement(match):
                    docstring = match.group(1).strip()
                    module = match.group(2)
                    description = match.group(3)
                    return f'"""\nModule: {module}\nDescription: {description}\n\n{docstring[3:-3].strip()}\n"""'
                
                new_content = pattern.sub(replacement, content)
                
                if new_content != content:
                    file_path.write_text(new_content)
                    fixed += 1
                    print(f"  ✅ Fixed: {file_path.name}")
                    
            except Exception as e:
                print(f"  ❌ Error fixing {file_path}: {e}")
        
        self.fixes_applied["headers"] = fixed
        return fixed
    
    def fix_relative_imports(self) -> int:
        """Convert relative imports to absolute."""
        print("\n🔧 Converting relative imports...")
        
        # Map of file paths to their module paths
        def get_module_path(file_path: Path) -> str:
            """Get the module path for a file."""
            rel_path = file_path.relative_to(self.project_root / "src")
            parts = list(rel_path.parts)
            if parts[-1].endswith('.py'):
                parts[-1] = parts[-1][:-3]
            if parts[-1] == '__init__':
                parts.pop()
            return '.'.join(parts)
        
        fixed = 0
        for py_file in self.src_root.rglob("*.py"):
            try:
                content = py_file.read_text()
                module_path = get_module_path(py_file)
                module_parts = module_path.split('.')
                
                lines = content.split('\n')
                new_lines = []
                
                for line in lines:
                    # Handle various relative import patterns
                    if line.strip().startswith('from .'):
                        # Extract the relative import
                        match = re.match(r'from (\.+)(\w+(?:\.\w+)*)?(.*)$', line)
                        if match:
                            dots = match.group(1)
                            relative_module = match.group(2) or ''
                            rest = match.group(3)
                            
                            # Calculate absolute path
                            level = len(dots)
                            if level <= len(module_parts):
                                base_parts = module_parts[:-level] if level > 0 else module_parts
                                if relative_module:
                                    absolute_module = '.'.join(base_parts + [relative_module])
                                else:
                                    absolute_module = '.'.join(base_parts)
                                
                                new_line = f'from {absolute_module}{rest}'
                                new_lines.append(new_line)
                                fixed += 1
                                continue
                    
                    new_lines.append(line)
                
                if new_lines != lines:
                    py_file.write_text('\n'.join(new_lines))
                    
            except Exception as e:
                print(f"  ❌ Error processing {py_file}: {e}")
        
        self.fixes_applied["imports"] = fixed
        return fixed
    
    def install_missing_deps(self) -> int:
        """Install missing dependencies."""
        print("\n🔧 Installing missing dependencies...")
        
        deps = [
            "scikit-learn>=1.3.0",
            "sentence-transformers>=4.0.0",
            "git+https://github.com/grahama1970/claude-test-reporter.git@main",
            "pytest-json-report>=1.5.0"
        ]
        
        installed = 0
        for dep in deps:
            print(f"  📦 Installing {dep}...")
            try:
                result = subprocess.run(
                    ["uv", "add", dep],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    installed += 1
                    print(f"  ✅ Installed: {dep}")
                else:
                    print(f"  ❌ Failed to install {dep}: {result.stderr}")
            except Exception as e:
                print(f"  ❌ Error installing {dep}: {e}")
        
        self.fixes_applied["deps"] = installed
        return installed
    
    def fix_honeypot_indentation(self) -> int:
        """Fix honeypot test indentation error."""
        print("\n🔧 Fixing honeypot test indentation...")
        
        honeypot_file = self.project_root / "tests" / "test_honeypot.py"
        if not honeypot_file.exists():
            print(f"  ⚠️  Honeypot file not found: {honeypot_file}")
            return 0
            
        try:
            content = honeypot_file.read_text()
            lines = content.split('\n')
            
            # Find and fix the duplicate decorator issue
            new_lines = []
            skip_next = False
            
            for i, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                    
                # Check for duplicate @pytest.mark.asyncio
                if (i > 0 and 
                    lines[i-1].strip() == "@pytest.mark.asyncio" and 
                    line.strip() == "@pytest.mark.asyncio"):
                    # Skip this duplicate line and fix indentation of next line
                    skip_next = False
                    continue
                    
                # Fix the indentation of the method after duplicate decorator
                if (i > 1 and 
                    lines[i-2].strip() == "@pytest.mark.asyncio" and
                    lines[i-1].strip() == "@pytest.mark.asyncio" and
                    line.startswith("async def")):
                    # Add proper indentation
                    new_lines.append("    " + line)
                else:
                    new_lines.append(line)
            
            honeypot_file.write_text('\n'.join(new_lines))
            self.fixes_applied["indentation"] = 1
            print("  ✅ Fixed honeypot test indentation")
            return 1
            
        except Exception as e:
            print(f"  ❌ Error fixing honeypot: {e}")
            return 0
    
    def run_all_fixes(self):
        """Run all fixes."""
        print("🚀 Starting comprehensive ArXiv fixes...")
        print(f"📁 Project root: {self.project_root}")
        
        # Apply all fixes
        self.fix_module_headers()
        self.fix_relative_imports()
        self.install_missing_deps()
        self.fix_honeypot_indentation()
        
        # Print summary
        print("\n📊 Fix Summary:")
        print(f"  Module headers fixed: {self.fixes_applied['headers']}")
        print(f"  Imports converted: {self.fixes_applied['imports']}")
        print(f"  Dependencies installed: {self.fixes_applied['deps']}")
        print(f"  Indentation fixes: {self.fixes_applied['indentation']}")
        
        total = sum(self.fixes_applied.values())
        print(f"\n✅ Total fixes applied: {total}")


def main():
    """Main function."""
    arxiv_root = Path("/home/graham/workspace/mcp-servers/arxiv-mcp-server")
    
    if not arxiv_root.exists():
        print(f"❌ ArXiv project not found at: {arxiv_root}")
        return 1
        
    fixer = ArxivIssueFixer(arxiv_root)
    fixer.run_all_fixes()
    
    print("\n🔍 Verifying fixes with granger-verify...")
    result = subprocess.run(
        ["/home/graham/.claude/commands/granger-verify", "--project", "arxiv_mcp", "--test"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())