#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Visual Report Generator for Level 4 UI Tests

Generates HTML reports with screenshots and visual diffs for UI validation.

External Dependencies:
- jinja2: https://jinja.palletsprojects.com/
- pillow: https://python-pillow.org/

Example Usage:
    >>> python generate_visual_report.py test_results.json --output-html reports/visual_report.html
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import base64
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GRANGER Level 4 UI Test Report - {{ timestamp }}</title>
    <style>
        :root {
            --color-primary-start: #4F46E5;
            --color-primary-end: #6366F1;
            --color-secondary: #6B7280;
            --color-background: #F9FAFB;
            --color-accent: #10B981;
            --color-error: #EF4444;
            --color-warning: #F59E0B;
            --color-success: #10B981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: var(--color-background);
            color: #1F2937;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, var(--color-primary-start), var(--color-primary-end));
            color: white;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }
        
        .summary-card {
            background: white;
            padding: 24px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .summary-card h3 {
            color: var(--color-secondary);
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 8px;
        }
        
        .summary-card .value {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--color-primary-start), var(--color-primary-end));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .test-result {
            background: white;
            border-radius: 8px;
            margin-bottom: 24px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .test-header {
            padding: 16px 24px;
            border-bottom: 1px solid #E5E7EB;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .test-title {
            font-size: 18px;
            font-weight: 600;
        }
        
        .test-status {
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
        }
        
        .status-real {
            background: var(--color-success);
            color: white;
        }
        
        .status-fake {
            background: var(--color-error);
            color: white;
        }
        
        .status-suspicious {
            background: var(--color-warning);
            color: white;
        }
        
        .test-body {
            padding: 24px;
        }
        
        .screenshot-section {
            margin-bottom: 24px;
        }
        
        .screenshot-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 16px;
        }
        
        .screenshot-item {
            text-align: center;
        }
        
        .screenshot-item img {
            max-width: 100%;
            border: 1px solid #E5E7EB;
            border-radius: 4px;
        }
        
        .screenshot-label {
            font-size: 14px;
            color: var(--color-secondary);
            margin-top: 8px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }
        
        .metric-item {
            padding: 16px;
            background: var(--color-background);
            border-radius: 4px;
        }
        
        .metric-label {
            font-size: 12px;
            color: var(--color-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 600;
            margin-top: 4px;
        }
        
        .style-compliance {
            margin-top: 24px;
        }
        
        .compliance-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 8px;
            margin-top: 12px;
        }
        
        .compliance-item {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px;
            background: var(--color-background);
            border-radius: 4px;
        }
        
        .compliance-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: white;
        }
        
        .compliance-pass {
            background: var(--color-success);
        }
        
        .compliance-fail {
            background: var(--color-error);
        }
        
        .footer {
            text-align: center;
            padding: 32px;
            color: var(--color-secondary);
            font-size: 14px;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1>GRANGER Level 4 UI Test Report</h1>
            <p>Generated: {{ timestamp }}</p>
        </div>
    </header>
    
    <main class="container">
        <!-- Summary Statistics -->
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Tests</h3>
                <div class="value">{{ total_tests }}</div>
            </div>
            <div class="summary-card">
                <h3>Passed (REAL)</h3>
                <div class="value">{{ passed_tests }}</div>
            </div>
            <div class="summary-card">
                <h3>Failed (FAKE)</h3>
                <div class="value">{{ failed_tests }}</div>
            </div>
            <div class="summary-card">
                <h3>Average Confidence</h3>
                <div class="value">{{ avg_confidence }}%</div>
            </div>
        </div>
        
        <!-- Test Results -->
        {% for test in tests %}
        <div class="test-result">
            <div class="test-header">
                <h2 class="test-title">Test {{ test.test_id }}: {{ test.description }}</h2>
                <span class="test-status status-{{ test.verdict|lower }}">{{ test.verdict }}</span>
            </div>
            
            <div class="test-body">
                <!-- Screenshots -->
                {% if test.visual_evidence %}
                <div class="screenshot-section">
                    <h3>Visual Evidence</h3>
                    <div class="screenshot-container">
                        <div class="screenshot-item">
                            <img src="{{ test.visual_evidence }}" alt="Test Screenshot">
                            <div class="screenshot-label">Actual Result</div>
                        </div>
                        {% if test.baseline_screenshot %}
                        <div class="screenshot-item">
                            <img src="{{ test.baseline_screenshot }}" alt="Baseline Screenshot">
                            <div class="screenshot-label">Expected (Baseline)</div>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endif %}
                
                <!-- Performance Metrics -->
                {% if test.performance %}
                <div class="metrics-section">
                    <h3>Performance Metrics</h3>
                    <div class="metrics-grid">
                        <div class="metric-item">
                            <div class="metric-label">Duration</div>
                            <div class="metric-value">{{ test.duration|round(2) }}s</div>
                        </div>
                        {% if test.performance.fps %}
                        <div class="metric-item">
                            <div class="metric-label">FPS</div>
                            <div class="metric-value">{{ test.performance.fps }}</div>
                        </div>
                        {% endif %}
                        {% if test.performance.latency_ms %}
                        <div class="metric-item">
                            <div class="metric-label">Latency</div>
                            <div class="metric-value">{{ test.performance.latency_ms|round(0) }}ms</div>
                        </div>
                        {% endif %}
                        <div class="metric-item">
                            <div class="metric-label">Confidence</div>
                            <div class="metric-value">{{ test.confidence }}%</div>
                        </div>
                    </div>
                </div>
                {% endif %}
                
                <!-- Style Compliance -->
                {% if test.style_compliance %}
                <div class="style-compliance">
                    <h3>Style Guide Compliance</h3>
                    <div class="compliance-grid">
                        {% for check, result in test.style_compliance.items() %}
                        <div class="compliance-item">
                            <div class="compliance-icon {{ 'compliance-pass' if result else 'compliance-fail' }}">
                                {{ '✓' if result else '✗' }}
                            </div>
                            <span>{{ check|replace('_', ' ')|title }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
                
                <!-- Failure Reason -->
                {% if test.reason %}
                <div class="failure-reason">
                    <h3>Details</h3>
                    <p>{{ test.reason }}</p>
                </div>
                {% endif %}
            </div>
        </div>
        {% endfor %}
    </main>
    
    <footer class="footer">
        <p>GRANGER UI Testing Infrastructure v1.0 | Powered by Playwright</p>
    </footer>
</body>
</html>
"""


def generate_visual_report(test_results_file: str, output_html: str):
    """Generate HTML report from test results JSON"""
    
    # Load test results
    with open(test_results_file, 'r') as f:
        results = json.load(f)
    
    # If results is a single test, wrap in array
    if isinstance(results, dict) and 'test_id' in results:
        results = [results]
    
    # Calculate summary statistics
    total_tests = len(results)
    passed_tests = sum(1 for t in results if t.get('verdict') == 'REAL')
    failed_tests = sum(1 for t in results if t.get('verdict') == 'FAKE')
    avg_confidence = sum(t.get('confidence', 0) for t in results) / total_tests if total_tests > 0 else 0
    
    # Add descriptions based on test IDs
    test_descriptions = {
        "001.1": "Chat UI Load Validation",
        "001.2": "Annotator Style Compliance",
        "001.3": "Terminal Performance",
        "001.H": "Honeypot - Headless Mode Detection"
    }
    
    for test in results:
        test['description'] = test_descriptions.get(test['test_id'], 'Unknown Test')
    
    # Render template
    template = Template(HTML_TEMPLATE)
    html_content = template.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_tests=total_tests,
        passed_tests=passed_tests,
        failed_tests=failed_tests,
        avg_confidence=round(avg_confidence, 1),
        tests=results
    )
    
    # Write output
    output_path = Path(output_html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)
    
    print(f"Visual report generated: {output_html}")
    print(f"Total: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}")
    print(f"Average confidence: {avg_confidence:.1f}%")


def main():
    parser = argparse.ArgumentParser(description="Generate visual test reports")
    parser.add_argument("test_results", help="JSON file with test results")
    parser.add_argument("--output-html", required=True, help="Output HTML file path")
    
    args = parser.parse_args()
    
    generate_visual_report(args.test_results, args.output_html)


if __name__ == "__main__":
    main()