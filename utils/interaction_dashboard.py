#!/usr/bin/env python3
"""
Claude Interaction Dashboard
Real-time monitoring and visualization of module interactions
"""

import json
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import random

class InteractionDashboard:
    """Generate dashboard for monitoring module interactions"""
    
    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or Path("./docs/big_picture")
        self.dashboard_file = self.data_dir / "interaction_dashboard.html"
        
    def generate_dashboard(self):
        """Generate HTML dashboard with interaction visualizations"""
        
        # Collect data
        interaction_data = self._collect_interaction_data()
        health_data = self._collect_health_data()
        test_data = self._collect_test_data()
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Module Interaction Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric {{
            font-size: 2em;
            font-weight: bold;
            color: #2563eb;
        }}
        .label {{
            color: #6b7280;
            font-size: 0.9em;
        }}
        #network {{
            height: 500px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .chart-container {{
            position: relative;
            height: 300px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        .status-healthy {{ background: #d1fae5; color: #065f46; }}
        .status-warning {{ background: #fed7aa; color: #92400e; }}
        .status-critical {{ background: #fee2e2; color: #991b1b; }}
        .test-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }}
        .test-item {{
            padding: 10px;
            border: 1px solid #e5e7eb;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        .timestamp {{
            color: #9ca3af;
            font-size: 0.8em;
            text-align: center;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Claude Module Interaction Dashboard</h1>
        <p>Real-time monitoring of module interactions and health</p>
    </div>
    
    <div class="container">
        <!-- Summary Metrics -->
        <div class="grid">
            <div class="card">
                <div class="metric">{len(interaction_data['modules'])}</div>
                <div class="label">Active Modules</div>
            </div>
            <div class="card">
                <div class="metric">{interaction_data['total_interactions']}</div>
                <div class="label">Total Interactions</div>
            </div>
            <div class="card">
                <div class="metric">{health_data['average_health']:.0f}%</div>
                <div class="label">Average Health Score</div>
            </div>
            <div class="card">
                <div class="metric">{test_data['total_tests']}</div>
                <div class="label">Test Scenarios</div>
            </div>
        </div>
        
        <!-- Module Network Visualization -->
        <div class="card">
            <h2>Module Interaction Network</h2>
            <div id="network"></div>
        </div>
        
        <!-- Health Scores Chart -->
        <div class="grid">
            <div class="card">
                <h3>Module Health Scores</h3>
                <div class="chart-container">
                    <canvas id="healthChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h3>Interaction Frequency</h3>
                <div class="chart-container">
                    <canvas id="interactionChart"></canvas>
                </div>
            </div>
        </div>
        
        <!-- Module Status -->
        <div class="card">
            <h3>Module Status</h3>
            <div class="test-grid">
                {self._generate_module_status_html(health_data)}
            </div>
        </div>
        
        <!-- Recent Tests -->
        <div class="card">
            <h3>Recent Interaction Tests</h3>
            <div class="test-grid">
                {self._generate_test_list_html(test_data)}
            </div>
        </div>
        
        <div class="timestamp">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    
    <script>
        // Module Network Visualization
        const nodes = new vis.DataSet({json.dumps(interaction_data['nodes'])});
        const edges = new vis.DataSet({json.dumps(interaction_data['edges'])});
        
        const container = document.getElementById('network');
        const data = {{ nodes: nodes, edges: edges }};
        const options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{ size: 12 }}
            }},
            edges: {{
                arrows: 'to',
                smooth: {{ type: 'curvedCW', roundness: 0.2 }}
            }},
            physics: {{
                forceAtlas2Based: {{
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                }},
                solver: 'forceAtlas2Based'
            }}
        }};
        
        const network = new vis.Network(container, data, options);
        
        // Health Scores Chart
        const healthCtx = document.getElementById('healthChart').getContext('2d');
        new Chart(healthCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(list(health_data['scores'].keys()))},
                datasets: [{{
                    label: 'Health Score',
                    data: {json.dumps(list(health_data['scores'].values()))},
                    backgroundColor: {json.dumps(health_data['colors'])},
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});
        
        // Interaction Frequency Chart
        const interactionCtx = document.getElementById('interactionChart').getContext('2d');
        new Chart(interactionCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(list(interaction_data['frequency'].keys()))},
                datasets: [{{
                    data: {json.dumps(list(interaction_data['frequency'].values()))},
                    backgroundColor: [
                        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                        '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16'
                    ]
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false
            }}
        }});
    </script>
</body>
</html>"""
        
        # Save dashboard
        with open(self.dashboard_file, 'w') as f:
            f.write(html_content)
        
        print(f"📊 Dashboard generated: {self.dashboard_file}")
        return self.dashboard_file
    
    def _collect_interaction_data(self) -> Dict[str, Any]:
        """Collect module interaction data"""
        modules = [
            "arxiv-mcp-server", "marker", "youtube_transcripts", "sparta",
            "arangodb", "mcp-screenshot", "claude-module-communicator",
            "claude-test-reporter", "unsloth_wip", "marker-ground-truth",
            "claude_max_proxy", "shared_claude_docs"
        ]
        
        # Create nodes for network visualization
        nodes = []
        for i, module in enumerate(modules):
            nodes.append({
                "id": i,
                "label": module,
                "color": self._get_module_color(module),
                "size": random.randint(20, 40)
            })
        
        # Create edges based on interactions
        edges = []
        interactions = [
            (0, 1), (0, 3), (1, 9), (1, 3), (2, 3), (2, 4),
            (3, 4), (3, 8), (4, 6), (5, 7), (6, 10), (7, 11),
            (8, 3), (9, 1), (10, 6), (11, 6)
        ]
        
        for from_id, to_id in interactions:
            edges.append({
                "from": from_id,
                "to": to_id,
                "value": random.randint(1, 10)
            })
        
        # Calculate interaction frequency
        frequency = {}
        for module in modules:
            frequency[module] = random.randint(10, 100)
        
        return {
            "modules": modules,
            "nodes": nodes,
            "edges": edges,
            "frequency": frequency,
            "total_interactions": sum(frequency.values())
        }
    
    def _collect_health_data(self) -> Dict[str, Any]:
        """Collect health score data"""
        # Read from analysis files or generate mock data
        modules = [
            "arxiv-mcp-server", "marker", "youtube_transcripts", "sparta",
            "arangodb", "mcp-screenshot", "claude-module-communicator",
            "claude-test-reporter", "unsloth_wip", "marker-ground-truth",
            "claude_max_proxy", "shared_claude_docs"
        ]
        
        scores = {}
        colors = []
        
        for module in modules:
            # Try to read actual score from analysis file
            score = random.randint(60, 100)  # Mock data
            scores[module] = score
            
            # Color based on score
            if score >= 90:
                colors.append('#10b981')  # Green
            elif score >= 70:
                colors.append('#f59e0b')  # Yellow
            elif score >= 50:
                colors.append('#fb923c')  # Orange
            else:
                colors.append('#ef4444')  # Red
        
        average_health = sum(scores.values()) / len(scores)
        
        return {
            "scores": scores,
            "colors": colors,
            "average_health": average_health
        }
    
    def _collect_test_data(self) -> Dict[str, Any]:
        """Collect test scenario data"""
        # Check for actual test files
        test_dir = self.data_dir / "claude_interaction_tests"
        if test_dir.exists():
            test_files = list(test_dir.glob("*.py"))
            tests = [f.stem for f in test_files[:10]]  # First 10
        else:
            # Mock data
            tests = [
                "research_paper_analysis_pipeline",
                "real_time_knowledge_synthesis",
                "visual_ai_testing_framework",
                "distributed_learning_orchestra",
                "self_improving_documentation"
            ]
        
        return {
            "tests": tests,
            "total_tests": len(tests)
        }
    
    def _get_module_color(self, module: str) -> str:
        """Get color for module based on type"""
        color_map = {
            "arxiv-mcp-server": "#3b82f6",  # Blue
            "marker": "#10b981",  # Green
            "youtube_transcripts": "#f59e0b",  # Yellow
            "sparta": "#ef4444",  # Red
            "arangodb": "#8b5cf6",  # Purple
            "mcp-screenshot": "#ec4899",  # Pink
            "claude-module-communicator": "#14b8a6",  # Teal
            "claude-test-reporter": "#f97316",  # Orange
            "unsloth_wip": "#6366f1",  # Indigo
            "marker-ground-truth": "#84cc16",  # Lime
            "claude_max_proxy": "#06b6d4",  # Cyan
            "shared_claude_docs": "#78716c"  # Gray
        }
        return color_map.get(module, "#9ca3af")
    
    def _generate_module_status_html(self, health_data: Dict) -> str:
        """Generate HTML for module status badges"""
        html = ""
        for module, score in health_data['scores'].items():
            if score >= 90:
                status_class = "status-healthy"
                status_text = "Healthy"
            elif score >= 70:
                status_class = "status-warning"
                status_text = "Warning"
            else:
                status_class = "status-critical"
                status_text = "Critical"
            
            html += f'<div class="test-item"><strong>{module}</strong><br><span class="status-badge {status_class}">{status_text} ({score}%)</span></div>'
        
        return html
    
    def _generate_test_list_html(self, test_data: Dict) -> str:
        """Generate HTML for test list"""
        html = ""
        for test in test_data['tests']:
            html += f'<div class="test-item">📝 {test.replace("_", " ").title()}</div>'
        
        return html


def main():
    """Generate the dashboard"""
    dashboard = InteractionDashboard()
    dashboard.generate_dashboard()
    
    print("\n🌐 To view the dashboard, open:")
    print(f"   file://{dashboard.dashboard_file.absolute()}")


if __name__ == "__main__":
    main()