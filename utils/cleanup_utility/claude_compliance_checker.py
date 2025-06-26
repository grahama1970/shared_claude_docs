#!/usr/bin/env python3
"""
CLAUDE.md Compliance Checker
Analyzes code compliance with CLAUDE.md rules without auto-refactoring
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ClaudeRule:
    """Represents a rule extracted from CLAUDE.md"""
    category: str
    rule: str
    pattern: str = None
    severity: str = 'warning'  # warning, error, info
    auto_fixable: bool = False

class ClaudeComplianceChecker:
    """Check code compliance with CLAUDE.md rules"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.claude_md_path = self.project_path / 'CLAUDE.md'
        self.rules: List[ClaudeRule] = []
        self.violations: List[Dict[str, Any]] = []
        
    def extract_rules_from_claude_md(self) -> List[ClaudeRule]:
        """Extract coding rules from CLAUDE.md"""
        if not self.claude_md_path.exists():
            return []
        
        with open(self.claude_md_path, 'r') as f:
            content = f.read()
        
        rules = []
        
        # Common patterns in CLAUDE.md files
        rule_patterns = [
            # Style rules
            (r'follow pep[\s-]?8', ClaudeRule('style', 'Follow PEP 8', severity='error')),
            (r'use (type hints|typing)', ClaudeRule('typing', 'Use type hints', severity='error')),
            (r'no hardcoded (secrets|credentials|keys)', ClaudeRule('security', 'No hardcoded secrets', severity='error')),
            
            # Documentation rules  
            (r'document all public (apis|functions|methods)', ClaudeRule('docs', 'Document public APIs', severity='warning')),
            (r'maintain.*docstring', ClaudeRule('docs', 'Maintain docstrings', severity='warning')),
            
            # Testing rules
            (r'maintain.*test coverage.*(\d+)%', ClaudeRule('testing', 'Maintain test coverage', severity='warning')),
            (r'write tests for', ClaudeRule('testing', 'Write tests', severity='warning')),
            
            # Import rules
            (r'prefer relative imports', ClaudeRule('imports', 'Use relative imports', severity='info')),
            (r'avoid circular imports', ClaudeRule('imports', 'No circular imports', severity='error')),
            
            # Naming conventions
            (r'use snake_case for', ClaudeRule('naming', 'Use snake_case', severity='warning')),
            (r'class names.*CamelCase', ClaudeRule('naming', 'Classes use CamelCase', severity='warning')),
            
            # Code organization
            (r'keep functions.*(\d+) lines', ClaudeRule('structure', 'Function length limit', severity='info')),
            (r'single responsibility', ClaudeRule('structure', 'Single responsibility', severity='info')),
        ]
        
        content_lower = content.lower()
        for pattern, rule_template in rule_patterns:
            if re.search(pattern, content_lower):
                rules.append(rule_template)
        
        # Extract custom rules from bullet points
        custom_rules = re.findall(r'[-*]\s+(Always|Never|Must|Should|Don\'t)\s+([^\n]+)', content, re.IGNORECASE)
        for directive, rule_text in custom_rules:
            severity = 'error' if directive.lower() in ['always', 'never', 'must'] else 'warning'
            rules.append(ClaudeRule('custom', f"{directive} {rule_text}", severity=severity))
        
        self.rules = rules
        return rules
    
    def check_file_compliance(self, file_path: Path) -> List[Dict[str, Any]]:
        """Check a single file for CLAUDE.md compliance"""
        violations = []
        
        if not file_path.suffix == '.py':
            return violations
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except:
            return violations
        
        # Check for common violations
        for i, line in enumerate(lines, 1):
            # PEP 8: Line length
            if len(line) > 120:  # Being lenient (PEP 8 says 79)
                violations.append({
                    'file': str(file_path),
                    'line': i,
                    'rule': 'Line too long',
                    'severity': 'info',
                    'message': f'Line {i} has {len(line)} characters (max 120)'
                })
            
            # Security: Hardcoded secrets
            secret_patterns = [
                r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
                r'password\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']'
            ]
            for pattern in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    violations.append({
                        'file': str(file_path),
                        'line': i,
                        'rule': 'Potential hardcoded secret',
                        'severity': 'error',
                        'message': f'Line {i} may contain hardcoded credentials'
                    })
        
        # Check file-level issues
        # Missing docstrings
        if 'def ' in content or 'class ' in content:
            if '"""' not in content and "'''" not in content:
                violations.append({
                    'file': str(file_path),
                    'line': 0,
                    'rule': 'Missing docstrings',
                    'severity': 'warning',
                    'message': 'File contains functions/classes but no docstrings'
                })
        
        # Check for type hints (basic check)
        function_matches = re.findall(r'def\s+(\w+)\s*\(([^)]*)\)', content)
        for func_name, params in function_matches:
            if params and '->' not in content[content.find(f'def {func_name}'):content.find('\n', content.find(f'def {func_name}'))]:
                violations.append({
                    'file': str(file_path),
                    'line': 0,
                    'rule': 'Missing return type hint',
                    'severity': 'info',
                    'message': f'Function {func_name} missing return type hint'
                })
        
        return violations
    
    def check_project_compliance(self) -> Dict[str, Any]:
        """Check entire project for CLAUDE.md compliance"""
        print(f"\n🔍 Checking CLAUDE.md compliance for {self.project_path.name}")
        
        # Extract rules
        self.extract_rules_from_claude_md()
        if not self.rules:
            print("  ⚠️  No CLAUDE.md found or no rules extracted")
            return {
                'project': str(self.project_path),
                'has_claude_md': False,
                'rules_found': 0,
                'files_checked': 0,
                'total_violations': 0,
                'violations': []
            }
        
        print(f"  Found {len(self.rules)} rules in CLAUDE.md")
        
        # Find all Python files
        py_files = list(self.project_path.rglob('*.py'))
        py_files = [f for f in py_files if '.venv' not in str(f) and 'venv' not in str(f)]
        
        print(f"  Checking {len(py_files)} Python files...")
        
        all_violations = []
        for py_file in py_files:
            violations = self.check_file_compliance(py_file)
            all_violations.extend(violations)
        
        # Summary by severity
        severity_counts = {'error': 0, 'warning': 0, 'info': 0}
        for v in all_violations:
            severity_counts[v.get('severity', 'info')] += 1
        
        print(f"  Found {len(all_violations)} total violations:")
        print(f"    ❌ Errors: {severity_counts['error']}")
        print(f"    ⚠️  Warnings: {severity_counts['warning']}")
        print(f"    ℹ️  Info: {severity_counts['info']}")
        
        return {
            'project': str(self.project_path),
            'has_claude_md': True,
            'rules_found': len(self.rules),
            'files_checked': len(py_files),
            'total_violations': len(all_violations),
            'severity_counts': severity_counts,
            'violations': all_violations[:100],  # First 100 violations
            'rules': [{'category': r.category, 'rule': r.rule, 'severity': r.severity} for r in self.rules]
        }

def generate_compliance_report(results: List[Dict[str, Any]], output_path: str):
    """Generate a compliance report"""
    with open(output_path, 'w') as f:
        f.write("# CLAUDE.md Compliance Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary
        total_violations = sum(r['total_violations'] for r in results)
        total_errors = sum(r['severity_counts']['error'] for r in results if 'severity_counts' in r)
        
        f.write("## Summary\n")
        f.write(f"- Projects checked: {len(results)}\n")
        f.write(f"- Total violations: {total_violations}\n")
        f.write(f"- Critical errors: {total_errors}\n\n")
        
        # Detailed results
        f.write("## Project Details\n\n")
        for result in results:
            project_name = Path(result['project']).name
            f.write(f"### {project_name}\n")
            
            if not result['has_claude_md']:
                f.write("- ⚠️  No CLAUDE.md file found\n\n")
                continue
            
            f.write(f"- Rules in CLAUDE.md: {result['rules_found']}\n")
            f.write(f"- Files checked: {result['files_checked']}\n")
            f.write(f"- Total violations: {result['total_violations']}\n")
            
            if result['total_violations'] > 0:
                f.write(f"  - ❌ Errors: {result['severity_counts']['error']}\n")
                f.write(f"  - ⚠️  Warnings: {result['severity_counts']['warning']}\n")
                f.write(f"  - ℹ️  Info: {result['severity_counts']['info']}\n")
                
                # Show first few violations
                f.write("\n#### Sample Violations:\n")
                for v in result['violations'][:5]:
                    f.write(f"- {v['severity'].upper()}: {v['rule']} - {v['message']}\n")
                    if v['line'] > 0:
                        f.write(f"  File: {v['file']}:{v['line']}\n")
            
            f.write("\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("1. **DO NOT auto-refactor** based on these violations\n")
        f.write("2. Review CLAUDE.md rules for practicality\n")
        f.write("3. Address critical errors (security, type safety) first\n")
        f.write("4. Consider updating CLAUDE.md if rules are too strict\n")
        f.write("5. Use this report for manual code review guidance\n")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python claude_compliance_checker.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    checker = ClaudeComplianceChecker(project_path)
    result = checker.check_project_compliance()
    
    # Save report
    report_path = f"claude_compliance_{Path(project_path).name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")