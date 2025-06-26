#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: bug_fix_plan.py
Description: Generate a prioritized bug fixing plan based on verified bugs

External Dependencies:
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> planner = BugFixPlanner()
>>> plan = planner.generate_fix_plan("bug_hunt_report_20250608_090853.json")

Expected Output:
>>> print(plan)
{
    "high_priority_fixes": [
        {"module": "arangodb", "fix": "Add request handling interface", "effort": 2}
    ],
    "medium_priority_fixes": [...],
    "low_priority_fixes": [...]
}
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict
from datetime import datetime
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)


class BugFixPlanner:
    """Generate prioritized bug fixing plans"""
    
    def __init__(self):
        self.bugs_by_priority = defaultdict(list)
        self.fixes_by_module = defaultdict(list)
        
    def generate_fix_plan(self, report_file: str) -> Dict[str, Any]:
        """Generate a comprehensive fix plan"""
        logger.info(f"📋 Generating fix plan from {report_file}")
        
        # Load bug report
        with open(report_file) as f:
            report = json.load(f)
            
        # Extract and categorize bugs
        bugs = report.get('detailed_bugs', [])
        self._categorize_bugs(bugs)
        
        # Generate fixes
        fixes = self._generate_fixes()
        
        # Create implementation plan
        plan = self._create_implementation_plan(fixes)
        
        return plan
        
    def _categorize_bugs(self, bugs: List[Dict[str, Any]]):
        """Categorize bugs by priority and module"""
        for bug in bugs:
            severity = bug.get('severity', 'unknown')
            modules = bug.get('modules_affected', ['unknown'])
            
            # Group by severity
            self.bugs_by_priority[severity].append(bug)
            
            # Group by module
            for module in modules:
                self.fixes_by_module[module].append(bug)
                
        logger.info(f"Categorized {len(bugs)} bugs")
        
    def _generate_fixes(self) -> List[Dict[str, Any]]:
        """Generate specific fixes for each bug pattern"""
        fixes = []
        
        # Pattern-based fixes
        fix_patterns = {
            'missing_auth': {
                'fix': 'Implement request handling interface with authentication',
                'effort': 2,
                'template': 'add_request_handler.py'
            },
            'test_validity': {
                'fix': 'Add realistic delays and actual operations to tests',
                'effort': 1,
                'template': 'improve_test_timing.py'
            },
            'connection': {
                'fix': 'Improve error messages and connection handling',
                'effort': 1,
                'template': 'improve_error_handling.py'
            },
            'state_management': {
                'fix': 'Implement proper state recovery mechanisms',
                'effort': 3,
                'template': 'add_state_recovery.py'
            },
            'test_coverage': {
                'fix': 'Add comprehensive test implementation',
                'effort': 2,
                'template': 'expand_test_coverage.py'
            }
        }
        
        # Generate fixes for each module
        for module, bugs in self.fixes_by_module.items():
            module_fixes = set()
            
            for bug in bugs:
                bug_type = bug.get('type', 'unknown')
                if bug_type in fix_patterns:
                    fix_info = fix_patterns[bug_type]
                    module_fixes.add((
                        fix_info['fix'],
                        fix_info['effort'],
                        fix_info['template'],
                        bug.get('severity', 'unknown')
                    ))
                    
            for fix, effort, template, severity in module_fixes:
                fixes.append({
                    'module': module,
                    'fix': fix,
                    'effort': effort,
                    'template': template,
                    'severity': severity,
                    'bugs_addressed': len([b for b in bugs if b.get('type') == bug_type])
                })
                
        return fixes
        
    def _create_implementation_plan(self, fixes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a prioritized implementation plan"""
        # Sort by severity and effort
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'unknown': 4}
        fixes.sort(key=lambda x: (priority_order.get(x['severity'], 4), x['effort']))
        
        plan = {
            'total_bugs': sum(len(bugs) for bugs in self.bugs_by_priority.values()),
            'total_fixes': len(fixes),
            'estimated_effort': sum(f['effort'] for f in fixes),
            'high_priority_fixes': [f for f in fixes if f['severity'] in ['critical', 'high']],
            'medium_priority_fixes': [f for f in fixes if f['severity'] == 'medium'],
            'low_priority_fixes': [f for f in fixes if f['severity'] in ['low', 'unknown']],
            'module_summary': self._generate_module_summary(),
            'implementation_order': self._generate_implementation_order(fixes)
        }
        
        return plan
        
    def _generate_module_summary(self) -> Dict[str, Any]:
        """Generate summary by module"""
        summary = {}
        
        for module, bugs in self.fixes_by_module.items():
            severity_counts = defaultdict(int)
            for bug in bugs:
                severity_counts[bug.get('severity', 'unknown')] += 1
                
            summary[module] = {
                'total_bugs': len(bugs),
                'by_severity': dict(severity_counts),
                'health_score': self._calculate_health_score(severity_counts)
            }
            
        return summary
        
    def _calculate_health_score(self, severity_counts: Dict[str, int]) -> float:
        """Calculate module health score (0-100)"""
        weights = {'critical': 10, 'high': 5, 'medium': 2, 'low': 1}
        
        total_weight = sum(
            weights.get(sev, 1) * count 
            for sev, count in severity_counts.items()
        )
        
        # Inverse score - more bugs = lower health
        return max(0, 100 - (total_weight * 10))
        
    def _generate_implementation_order(self, fixes: List[Dict[str, Any]]) -> List[str]:
        """Generate recommended implementation order"""
        order = []
        
        # Group by effort for batching
        effort_groups = defaultdict(list)
        for fix in fixes:
            effort_groups[fix['effort']].append(fix)
            
        # Start with low effort, high impact
        for effort in sorted(effort_groups.keys()):
            group = effort_groups[effort]
            # Sort by severity within effort group
            group.sort(key=lambda x: x['severity'])
            
            for fix in group:
                order.append(f"{fix['module']}: {fix['fix']} (effort: {fix['effort']})")
                
        return order


def generate_fix_report(plan: Dict[str, Any], output_file: str):
    """Generate a markdown fix report"""
    report = f"""# Bug Fix Implementation Plan

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Total Bugs**: {plan['total_bugs']}  
**Total Fixes**: {plan['total_fixes']}  
**Estimated Effort**: {plan['estimated_effort']} days

## Priority Summary

- **High Priority**: {len(plan['high_priority_fixes'])} fixes
- **Medium Priority**: {len(plan['medium_priority_fixes'])} fixes  
- **Low Priority**: {len(plan['low_priority_fixes'])} fixes

## Module Health Status

| Module | Bugs | Critical | High | Medium | Low | Health Score |
|--------|------|----------|------|--------|-----|--------------|
"""
    
    for module, stats in plan['module_summary'].items():
        by_sev = stats['by_severity']
        report += f"| {module} | {stats['total_bugs']} | "
        report += f"{by_sev.get('critical', 0)} | {by_sev.get('high', 0)} | "
        report += f"{by_sev.get('medium', 0)} | {by_sev.get('low', 0)} | "
        report += f"{stats['health_score']:.0f}% |\n"
        
    report += "\n## High Priority Fixes\n\n"
    
    for i, fix in enumerate(plan['high_priority_fixes'], 1):
        report += f"{i}. **{fix['module']}**: {fix['fix']}\n"
        report += f"   - Severity: {fix['severity']}\n"
        report += f"   - Effort: {fix['effort']} days\n"
        report += f"   - Bugs addressed: {fix['bugs_addressed']}\n"
        report += f"   - Template: `{fix['template']}`\n\n"
        
    report += "## Implementation Order\n\n"
    
    for i, step in enumerate(plan['implementation_order'], 1):
        report += f"{i}. {step}\n"
        
    # Save report
    with open(output_file, 'w') as f:
        f.write(report)
        
    logger.info(f"📄 Fix plan saved to: {output_file}")
    
    return report


def main():
    """Generate fix plan for the latest bug report"""
    # Find the latest bug report
    reports = list(Path('.').glob('bug_hunt_report_*.json'))
    if not reports:
        logger.error("No bug reports found")
        return 1
        
    latest_report = max(reports, key=lambda p: p.stat().st_mtime)
    logger.info(f"Analyzing report: {latest_report}")
    
    # Generate fix plan
    planner = BugFixPlanner()
    plan = planner.generate_fix_plan(str(latest_report))
    
    # Generate report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'bug_fix_plan_{timestamp}.md'
    generate_fix_report(plan, report_file)
    
    # Summary
    logger.info(f"""
🔧 Fix Plan Complete
Total Fixes: {plan['total_fixes']}
High Priority: {len(plan['high_priority_fixes'])}
Estimated Effort: {plan['estimated_effort']} days
    """)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())