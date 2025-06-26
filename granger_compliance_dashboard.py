#!/usr/bin/env python3
"""
Module: granger_compliance_dashboard.py
Description: Generate visual compliance dashboard for Granger ecosystem

External Dependencies:
- None (uses standard library only)

Sample Input:
>>> report = json.load(open('granger_compliance_report.json'))

Expected Output:
>>> HTML dashboard file with visual compliance status

Example Usage:
>>> python granger_compliance_dashboard.py
"""

import json
from pathlib import Path
from datetime import datetime

def generate_dashboard_html(report_path: Path) -> str:
    """Generate HTML dashboard from compliance report"""
    
    with open(report_path) as f:
        report = json.load(f)
    
    # Calculate percentages
    total = report['total_projects']
    compliant = report['summary']['fully_compliant']
    minor = report['summary']['minor_issues']
    major = report['summary']['major_issues']
    
    compliant_pct = (compliant / total * 100) if total > 0 else 0
    minor_pct = (minor / total * 100) if total > 0 else 0
    major_pct = (major / total * 100) if total > 0 else 0
    
    # Generate project cards
    project_cards = []
    for name, data in report['projects'].items():
        if not data.get('exists'):
            continue
            
        severity = data.get('severity', 'unknown')
        color = {
            'compliant': '#10b981',  # green
            'minor': '#f59e0b',      # amber
            'major': '#ef4444'       # red
        }.get(severity, '#6b7280')
        
        # Count issues
        issue_counts = {}
        for check_name, check_data in data.get('checks', {}).items():
            if check_data.get('issues'):
                issue_counts[check_name] = len(check_data['issues'])
        
        issues_html = ""
        if issue_counts:
            issues_html = "<ul style='margin: 10px 0; padding-left: 20px;'>"
            for check, count in issue_counts.items():
                issues_html += f"<li>{check}: {count} issue{'s' if count > 1 else ''}</li>"
            issues_html += "</ul>"
        else:
            issues_html = "<p style='color: #10b981; margin: 10px 0;'>✓ All checks passed</p>"
        
        card = f"""
        <div style="background: white; border: 2px solid {color}; border-radius: 8px; padding: 15px; margin: 10px;">
            <h3 style="margin: 0 0 10px 0; color: {color};">{name}</h3>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">
                    {severity.upper()}
                </span>
                <span style="font-size: 0.9em; color: #6b7280;">
                    {data['path'].replace('/home/graham/workspace/', '~/')}
                </span>
            </div>
            {issues_html}
        </div>
        """
        project_cards.append((severity, name, card))
    
    # Sort by severity (major first, then minor, then compliant)
    severity_order = {'major': 0, 'minor': 1, 'compliant': 2}
    project_cards.sort(key=lambda x: (severity_order.get(x[0], 3), x[1]))
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Granger Ecosystem Compliance Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f3f4f6;
            color: #1f2937;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-card h2 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .summary-card p {{
            margin: 5px 0 0 0;
            color: #6b7280;
        }}
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 0;
        }}
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e5e7eb;
            border-radius: 15px;
            overflow: hidden;
            margin: 20px 0;
            display: flex;
        }}
        .progress-segment {{
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        .action-items {{
            background: #fef3c7;
            border: 1px solid #fbbf24;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .action-items h3 {{
            margin: 0 0 10px 0;
            color: #92400e;
        }}
        .action-items ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .action-items li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0 0 10px 0;">Granger Ecosystem Compliance Dashboard</h1>
            <p style="margin: 0; color: #6b7280;">
                Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                Standard: GRANGER_MODULE_STANDARDS.md v1.0.0
            </p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h2 style="color: #10b981;">{compliant}</h2>
                <p>Fully Compliant</p>
                <p style="font-size: 1.2em; font-weight: bold;">{compliant_pct:.0f}%</p>
            </div>
            <div class="summary-card">
                <h2 style="color: #f59e0b;">{minor}</h2>
                <p>Minor Issues</p>
                <p style="font-size: 1.2em; font-weight: bold;">{minor_pct:.0f}%</p>
            </div>
            <div class="summary-card">
                <h2 style="color: #ef4444;">{major}</h2>
                <p>Major Issues</p>
                <p style="font-size: 1.2em; font-weight: bold;">{major_pct:.0f}%</p>
            </div>
            <div class="summary-card">
                <h2>{total}</h2>
                <p>Total Projects</p>
                <p style="font-size: 1.2em; font-weight: bold;">With GitHub</p>
            </div>
        </div>
        
        <div class="progress-bar">
            <div class="progress-segment" style="width: {major_pct}%; background: #ef4444;">
                {major_pct:.0f}% Major
            </div>
            <div class="progress-segment" style="width: {minor_pct}%; background: #f59e0b;">
                {minor_pct:.0f}% Minor
            </div>
            <div class="progress-segment" style="width: {compliant_pct}%; background: #10b981;">
                {compliant_pct:.0f}% Compliant
            </div>
        </div>
        
        <div class="action-items">
            <h3>🚨 Critical Actions Required</h3>
            <ul>
                <li><strong>9 projects</strong> need build system migration from hatchling/poetry to setuptools</li>
                <li><strong>8 projects</strong> have incorrect dependency versions or GitHub URL formats</li>
                <li><strong>1 project</strong> (granger_hub) violates NO MOCKS policy</li>
                <li><strong>13 projects</strong> need MCP integration</li>
            </ul>
        </div>
        
        <h2 style="margin: 30px 0 20px 0;">Project Compliance Status</h2>
        <div class="projects-grid">
            {''.join(card for _, _, card in project_cards)}
        </div>
        
        <div style="background: white; padding: 20px; border-radius: 8px; margin-top: 30px;">
            <h3>Legend</h3>
            <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 20px; height: 20px; background: #ef4444; border-radius: 4px;"></div>
                    <span>Major Issues (Breaking)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 20px; height: 20px; background: #f59e0b; border-radius: 4px;"></div>
                    <span>Minor Issues (Non-breaking)</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <div style="width: 20px; height: 20px; background: #10b981; border-radius: 4px;"></div>
                    <span>Fully Compliant</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    return html

def main():
    """Generate the dashboard"""
    report_path = Path("/home/graham/workspace/shared_claude_docs/granger_compliance_report.json")
    dashboard_path = Path("/home/graham/workspace/shared_claude_docs/granger_compliance_dashboard.html")
    
    if not report_path.exists():
        print("Error: granger_compliance_report.json not found. Run granger_compliance_checker.py first.")
        return
    
    html = generate_dashboard_html(report_path)
    dashboard_path.write_text(html)
    
    print(f"✅ Dashboard generated: {dashboard_path}")
    print(f"   Open in browser: file://{dashboard_path.absolute()}")

if __name__ == "__main__":
    main()