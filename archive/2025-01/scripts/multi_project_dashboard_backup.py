
"""
Module: multi_project_dashboard.py
Description: Implementation of multi project dashboard functionality
"""

External Dependencies:
- None (uses only standard library)

Sample Input:
>>> # Add specific examples based on module functionality

Expected Output:
>>> # Add expected output examples

Example Usage:
>>> # Add usage examples
"""

#!/usr/bin/env python3
"""
Multi-Project Dashboard Generator

Purpose: Create a unified dashboard showing test status across multiple projects
Features: Project health indicators, aggregated metrics, quick navigation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import re
from collections import defaultdict


class MultiProjectDashboard:
    """Generate dashboard showing test results across multiple projects."""

    def __init__(self, title: str = "Multi-Project Test Dashboard"):
        """Initialize dashboard generator."""
        self.title = title
        self.projects_data = {}

    def add_project(self, project_name: str, test_results: Dict[str, Any],
                   report_url: Optional[str] = None,
                   analyzer_results: Optional[Dict[str, Any]] = None) -> None:
        """Add project test results to dashboard."""
        self.projects_data[project_name] = {
            "results": test_results,
            "report_url": report_url,
            "analyzer_results": analyzer_results,
            "added_at": datetime.now().isoformat()
        }

    def load_project_from_json(self, project_name: str, json_path: Path) -> None:
        """Load project test results from pytest JSON report."""
        with open(json_path) as f:
            data = json.load(f)

        # Extract key metrics
        tests = data.get("tests", [])
        summary = {
            "total": len(tests),
            "passed": sum(1 for t in tests if t["outcome"] == "passed"),
            "failed": sum(1 for t in tests if t["outcome"] == "failed"),
            "skipped": sum(1 for t in tests if t["outcome"] == "skipped"),
            "duration": data.get("duration", 0),
            "created": data.get("created", datetime.now().timestamp())
        }

        # Calculate health score
        if summary["total"] > 0:
            summary["success_rate"] = (summary["passed"] / summary["total"]) * 100
            summary["health"] = self._calculate_health(summary)
        else:
            summary["success_rate"] = 0
            summary["health"] = "unknown"

        # Store failed test details
        summary["failed_tests"] = [
            {
                "name": t["nodeid"],
                "duration": t.get("duration", 0),
                "file": t["nodeid"].split("::")[0]
            }
            for t in tests if t["outcome"] == "failed"
        ]

        self.add_project(project_name, summary)

    def _calculate_health(self, summary: Dict[str, Any]) -> str:
        """Calculate project health status."""
        success_rate = summary["success_rate"]
        if success_rate >= 95:
            return "healthy"
        elif success_rate >= 80:
            return "warning"
        else:
            return "critical"

    def generate(self, output_file: str = "multi_project_dashboard.html") -> str:
        """Generate the multi-project dashboard."""
        if not self.projects_data:
            raise ValueError("No project data added to dashboard")

        # Calculate aggregate metrics
        aggregate = self._calculate_aggregate_metrics()

        # Generate HTML
        html_content = self._generate_html(aggregate)

        # Write file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')

        return str(output_path.resolve())

    def _calculate_aggregate_metrics(self) -> Dict[str, Any]:
        """Calculate metrics across all projects."""
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_skipped = 0
        total_duration = 0

        for project_name, project_data in self.projects_data.items():
            results = project_data["results"]
            total_tests += results.get("total", 0)
            total_passed += results.get("passed", 0)
            total_failed += results.get("failed", 0)
            total_skipped += results.get("skipped", 0)
            total_duration += results.get("duration", 0)

        return {
            "total_projects": len(self.projects_data),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_skipped": total_skipped,
            "total_duration": total_duration,
            "overall_success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "healthy_projects": sum(1 for p in self.projects_data.values()
                                  if p["results"].get("health") == "healthy"),
            "warning_projects": sum(1 for p in self.projects_data.values()
                                  if p["results"].get("health") == "warning"),
            "critical_projects": sum(1 for p in self.projects_data.values()
                                   if p["results"].get("health") == "critical")
        }

    def _generate_html(self, aggregate: Dict[str, Any]) -> str:
        """Generate the dashboard HTML."""
        # Build project cards
        project_cards_html = ""
        for project_name, project_data in sorted(self.projects_data.items()):
            results = project_data["results"]
            health_color = {
                "healthy": "#10b981",
                "warning": "#f59e0b",
                "critical": "#ef4444",
                "unknown": "#6b7280"
            }.get(results.get("health", "unknown"), "#6b7280")

            # Failed tests list
            failed_tests_html = ""
            if results.get("failed_tests"):
                failed_tests_html = "<div class='failed-tests'><strong>Failed Tests:</strong><ul>"
                for test in results["failed_tests"][:5]:  # Show top 5
                    failed_tests_html += f"<li>{test['name']}</li>"
                if len(results.get("failed_tests", [])) > 5:
                    failed_tests_html += f"<li>... and {len(results['failed_tests']) - 5} more</li>"
                failed_tests_html += "</ul></div>"

            # Project card
            project_cards_html += f"""
            <div class="project-card" data-health="{results.get('health', 'unknown')}">
                <div class="project-header" style="border-left: 4px solid {health_color}">
                    <h3>{project_name}</h3>
                    <span class="health-badge" style="background: {health_color}">
                        {results.get('health', 'unknown').upper()}
                    </span>
                </div>
                <div class="project-metrics">
                    <div class="metric">
                        <span class="metric-value">{results.get('total', 0)}</span>
                        <span class="metric-label">Total Tests</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value" style="color: #10b981">{results.get('passed', 0)}</span>
                        <span class="metric-label">Passed</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value" style="color: #ef4444">{results.get('failed', 0)}</span>
                        <span class="metric-label">Failed</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value">{results.get('success_rate', 0):.1f}%%%</span>
                        <span class="metric-label">Success Rate</span>
                    </div>
                </div>
                <div class="project-progress">
                    <div class="progress-bar">
                        <div class="progress-fill passed" style="width: {results.get('passed', 0) / max(results.get('total', 1), 1) * 100}%%"></div>
                        <div class="progress-fill failed" style="width: {results.get('failed', 0) / max(results.get('total', 1), 1) * 100}%%"></div>
                        <div class="progress-fill skipped" style="width: {results.get('skipped', 0) / max(results.get('total', 1), 1) * 100}%%"></div>
                    </div>
                </div>
                {failed_tests_html}
                <div class="project-footer">
                    <span class="timestamp">Updated: {datetime.fromisoformat(project_data['added_at']).strftime('%Y-%m-%d %H:%M')}</span>
                    {f'<a href="{project_data["report_url"]}" class="view-report">View Full Report →</a>' if project_data.get("report_url") else ''}
                </div>
            </div>
            """

        # Summary cards
        summary_cards_html = f"""
        <div class="summary-card">
            <div class="summary-value">{aggregate['total_projects']}</div>
            <div class="summary-label">Total Projects</div>
        </div>
        <div class="summary-card">
            <div class="summary-value">{aggregate['total_tests']}</div>
            <div class="summary-label">Total Tests</div>
        </div>
        <div class="summary-card">
            <div class="summary-value" style="color: #10b981">{aggregate['overall_success_rate']:.1f}%%%</div>
            <div class="summary-label">Overall Success Rate</div>
        </div>
        <div class="summary-card">
            <div class="summary-value">{aggregate['total_duration']:.1f}s</div>
            <div class="summary-label">Total Duration</div>
        </div>
        """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f3f4f6;
            color: #111827;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #111827;
        }}
        .subtitle {{
            color: #6b7280;
            font-size: 1.1em;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .summary-value {{
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        .summary-label {{
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .filters {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }}
        .filter-btn {{
            padding: 8px 16px;
            border: 1px solid #e5e7eb;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9em;
        }}
        .filter-btn:hover {{
            background: #f9fafb;
        }}
        .filter-btn.active {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
        }}
        .project-card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .project-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .project-header {{
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e5e7eb;
        }}
        .project-header h3 {{
            font-size: 1.3em;
            color: #111827;
        }}
        .health-badge {{
            padding: 4px 12px;
            border-radius: 20px;
            color: white;
            font-size: 0.75em;
            font-weight: 600;
            letter-spacing: 0.05em;
        }}
        .project-metrics {{
            padding: 20px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            text-align: center;
            border-bottom: 1px solid #e5e7eb;
        }}
        .metric {{
            display: flex;
            flex-direction: column;
        }}
        .metric-value {{
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 2px;
        }}
        .metric-label {{
            font-size: 0.75em;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        .project-progress {{
            padding: 0 20px 20px;
        }}
        .progress-bar {{
            height: 10px;
            background: #e5e7eb;
            border-radius: 5px;
            overflow: hidden;
            display: flex;
        }}
        .progress-fill {{
            height: 100%;
            transition: width 0.3s;
        }}
        .progress-fill.passed {{ background: #10b981; }}
        .progress-fill.failed {{ background: #ef4444; }}
        .progress-fill.skipped {{ background: #f59e0b; }}
        .failed-tests {{
            padding: 0 20px 20px;
            font-size: 0.85em;
            color: #6b7280;
        }}
        .failed-tests ul {{
            margin-top: 5px;
            padding-left: 20px;
        }}
        .failed-tests li {{
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #ef4444;
        }}
        .project-footer {{
            padding: 15px 20px;
            background: #f9fafb;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
        }}
        .timestamp {{
            color: #6b7280;
        }}
        .view-report {{
            color: #3b82f6;
            text-decoration: none;
            font-weight: 500;
        }}
        .view-report:hover {{
            text-decoration: underline;
        }}
        .hidden {{ display: none !important; }}
        @media (max-width: 768px) {{
            .projects-grid {{ grid-template-columns: 1fr; }}
            .summary-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 {self.title}</h1>
            <p class="subtitle">Last updated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
        </header>

        <div class="summary-grid">
            {summary_cards_html}
        </div>

        <div class="filters">
            <span style="font-weight: 600; margin-right: 10px;">Filter by health:</span>
            <button class="filter-btn active" onclick="filterProjects('all')">All Projects</button>
            <button class="filter-btn" onclick="filterProjects('healthy')">Healthy ({aggregate['healthy_projects']})</button>
            <button class="filter-btn" onclick="filterProjects('warning')">Warning ({aggregate['warning_projects']})</button>
            <button class="filter-btn" onclick="filterProjects('critical')">Critical ({aggregate['critical_projects']})</button>
        </div>

        <div class="projects-grid">
            {project_cards_html}
        </div>
    </div>

    <script>
        function filterProjects(health) {{
            const cards = document.querySelectorAll('.project-card');
            const buttons = document.querySelectorAll('.filter-btn');

            // Update active button
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // Filter cards
            cards.forEach(card => {{
                if (health === 'all' || card.dataset.health === health) {{
                    card.classList.remove('hidden');
                }} else {{
                    card.classList.add('hidden');
                }}
            }});
        }}

        // Auto-refresh every 30 seconds
        setInterval(() => {{
            const subtitle = document.querySelector('.subtitle');
            subtitle.textContent = 'Last updated: ' + new Date().toLocaleString('en-US', {{
                month: 'long', day: 'numeric', year: 'numeric',
                hour: 'numeric', minute: '2-digit', hour12: true
            }});
        }}, 30000);
    </script>
</body>
</html>"""


if __name__ == "__main__":
    # Validation example
    print(f"Validating {__file__}...")

    # Create dashboard
    dashboard = MultiProjectDashboard()

    # Add sample projects
    dashboard.add_project("SPARTA", {
        "total": 100,
        "passed": 95,
        "failed": 3,
        "skipped": 2,
        "duration": 45.2,
        "success_rate": 95.0,
        "health": "healthy",
        "failed_tests": [
            {"name": "test_download_pdf", "duration": 1.2, "file": "tests/test_download.py"},
            {"name": "test_parse_html", "duration": 0.5, "file": "tests/test_parse.py"}
        ]
    }, "sparta_report.html")

    dashboard.add_project("Marker", {
        "total": 50,
        "passed": 42,
        "failed": 8,
        "skipped": 0,
        "duration": 23.1,
        "success_rate": 84.0,
        "health": "warning",
        "failed_tests": [
            {"name": "test_extract_tables", "duration": 2.1, "file": "tests/test_extract.py"}
        ]
    }, "marker_report.html")

    dashboard.add_project("ArangoDB", {
        "total": 75,
        "passed": 45,
        "failed": 30,
        "skipped": 0,
        "duration": 67.8,
        "success_rate": 60.0,
        "health": "critical",
        "failed_tests": [
            {"name": "test_graph_query", "duration": 3.2, "file": "tests/test_graph.py"},
            {"name": "test_connection", "duration": 0.1, "file": "tests/test_connection.py"}
        ]
    })

    # Generate dashboard
    output_file = dashboard.generate("example_multi_project_dashboard.html")
    print(f"✅ Multi-project dashboard generated: {output_file}")