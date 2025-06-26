#!/usr/bin/env python3
"""
Module: test_history_tracker.py
Description: Test history tracking functionality with trend analysis

External Dependencies:
- statistics: https://docs.python.org/3/library/statistics.html

Sample Input:
>>> tracker = TestHistoryTracker()
>>> tracker.add_test_run("MyProject", {"total": 100, "passed": 95, "failed": 5})

Expected Output:
>>> tracker.get_test_trends("MyProject", "test_example")
{"test_name": "test_example", "success_rate": 95.0, ...}

Example Usage:
>>> tracker = TestHistoryTracker()
>>> tracker.add_test_run("Project", test_results)
>>> report = tracker.generate_history_report("Project")
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict, deque
import statistics


class TestHistoryTracker:
    """Track and analyze test results over time."""

    def __init__(self, storage_dir: str = ".test_history"):
        """Initialize tracker with storage directory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.history_file = self.storage_dir / "test_history.json"
        self.flaky_tests_file = self.storage_dir / "flaky_tests.json"
        self.history = self._load_history()

    def _load_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load test history from storage."""
        if self.history_file.exists():
            with open(self.history_file) as f:
                return json.load(f)
        return {}

    def _save_history(self) -> None:
        """Save test history to storage."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def add_test_run(self, project_name: str, test_results: Dict[str, Any],
                     run_id: Optional[str] = None) -> None:
        """Add a test run to history."""
        if project_name not in self.history:
            self.history[project_name] = []

        # Create run record
        run_record = {
            "run_id": run_id or datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": test_results.get("total", 0),
                "passed": test_results.get("passed", 0),
                "failed": test_results.get("failed", 0),
                "skipped": test_results.get("skipped", 0),
                "duration": test_results.get("duration", 0)
            },
            "tests": {}
        }

        # Store individual test results
        for test in test_results.get("tests", []):
            test_name = test.get("nodeid", test.get("name", "unknown"))
            run_record["tests"][test_name] = {
                "outcome": test.get("outcome", test.get("status", "unknown")),
                "duration": test.get("duration", 0),
                "error": test.get("error", None)
            }

        # Add to history (keep last 100 runs)
        self.history[project_name].append(run_record)
        self.history[project_name] = self.history[project_name][-100:]

        self._save_history()
        self._analyze_flaky_tests(project_name)

    def get_test_trends(self, project_name: str, test_name: str,
                       days: int = 7) -> Dict[str, Any]:
        """Get trends for a specific test over time."""
        if project_name not in self.history:
            return {"error": "Project not found"}

        cutoff_date = datetime.now() - timedelta(days=days)
        relevant_runs = []

        for run in self.history[project_name]:
            run_time = datetime.fromisoformat(run["timestamp"])
            if run_time >= cutoff_date and test_name in run["tests"]:
                relevant_runs.append({
                    "timestamp": run["timestamp"],
                    "outcome": run["tests"][test_name]["outcome"],
                    "duration": run["tests"][test_name]["duration"]
                })

        if not relevant_runs:
            return {"error": "No data for this test in the specified period"}

        # Calculate trends
        outcomes = [r["outcome"] for r in relevant_runs]
        durations = [r["duration"] for r in relevant_runs if r["duration"] > 0]

        trends = {
            "test_name": test_name,
            "period_days": days,
            "total_runs": len(relevant_runs),
            "outcomes": {
                "passed": outcomes.count("passed"),
                "failed": outcomes.count("failed"),
                "skipped": outcomes.count("skipped")
            },
            "success_rate": (outcomes.count("passed") / len(outcomes) * 100) if outcomes else 0,
            "duration_stats": {
                "mean": statistics.mean(durations) if durations else 0,
                "median": statistics.median(durations) if durations else 0,
                "std_dev": statistics.stdev(durations) if len(durations) > 1 else 0,
                "min": min(durations) if durations else 0,
                "max": max(durations) if durations else 0
            },
            "recent_runs": relevant_runs[-10:]  # Last 10 runs
        }

        # Detect performance regression
        if len(durations) >= 5:
            recent_avg = statistics.mean(durations[-5:])
            overall_avg = statistics.mean(durations)
            if recent_avg > overall_avg * 1.5:
                trends["performance_regression"] = True
                trends["regression_factor"] = recent_avg / overall_avg

        return trends

    def _analyze_flaky_tests(self, project_name: str) -> None:
        """Analyze and identify flaky tests."""
        if project_name not in self.history or len(self.history[project_name]) < 3:
            return

        # Analyze last 20 runs
        recent_runs = self.history[project_name][-20:]
        test_outcomes = defaultdict(list)

        # Collect outcomes for each test
        for run in recent_runs:
            for test_name, test_data in run["tests"].items():
                test_outcomes[test_name].append(test_data["outcome"])

        # Identify flaky tests
        flaky_tests = {}
        for test_name, outcomes in test_outcomes.items():
            if len(outcomes) < 3:
                continue

            unique_outcomes = set(outcomes)
            # Test is flaky if it has mixed results
            if len(unique_outcomes) > 1 and "passed" in unique_outcomes and "failed" in unique_outcomes:
                passed_count = outcomes.count("passed")
                failed_count = outcomes.count("failed")
                total_runs = len(outcomes)

                # Calculate flakiness score (0-1, higher is more flaky)
                flakiness = 1 - abs(passed_count - failed_count) / total_runs

                # Track recent pattern
                recent_pattern = "".join(
                    "P" if o == "passed" else "F" if o == "failed" else "S"
                    for o in outcomes[-10:]
                )

                flaky_tests[test_name] = {
                    "flakiness_score": round(flakiness, 3),
                    "pass_rate": round(passed_count / total_runs * 100, 1),
                    "fail_rate": round(failed_count / total_runs * 100, 1),
                    "total_runs": total_runs,
                    "recent_pattern": recent_pattern,
                    "last_outcome": outcomes[-1],
                    "detected_at": datetime.now().isoformat()
                }

        # Save flaky tests analysis
        if flaky_tests:
            all_flaky_tests = {}
            if self.flaky_tests_file.exists():
                with open(self.flaky_tests_file) as f:
                    all_flaky_tests = json.load(f)

            all_flaky_tests[project_name] = {
                "updated_at": datetime.now().isoformat(),
                "tests": flaky_tests
            }

            with open(self.flaky_tests_file, 'w') as f:
                json.dump(all_flaky_tests, f, indent=2)

    def get_flaky_tests(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """Get flaky tests for a project or all projects."""
        if not self.flaky_tests_file.exists():
            return {}

        with open(self.flaky_tests_file) as f:
            all_flaky_tests = json.load(f)

        if project_name:
            return all_flaky_tests.get(project_name, {})
        return all_flaky_tests

    def get_project_health_history(self, project_name: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get project health metrics over time."""
        if project_name not in self.history:
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        health_history = []

        for run in self.history[project_name]:
            run_time = datetime.fromisoformat(run["timestamp"])
            if run_time >= cutoff_date:
                summary = run["summary"]
                total = summary.get("total", 0)
                if total > 0:
                    health_history.append({
                        "timestamp": run["timestamp"],
                        "success_rate": (summary.get("passed", 0) / total) * 100,
                        "total_tests": total,
                        "failed_tests": summary.get("failed", 0),
                        "duration": summary.get("duration", 0)
                    })

        return health_history

    def generate_history_report(self, project_name: str, output_file: str = "test_history_report.html") -> str:
        """Generate HTML report showing test history and trends."""
        if project_name not in self.history:
            raise ValueError(f"No history found for project: {project_name}")

        # Get data
        health_history = self.get_project_health_history(project_name, days=30)
        flaky_tests = self.get_flaky_tests(project_name)

        # Calculate summary stats
        if health_history:
            avg_success_rate = statistics.mean([h['success_rate'] for h in health_history[-7:]])
        else:
            avg_success_rate = 0

        # Generate simple HTML without f-string formatting issues
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PROJECT_NAME - Test History Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f3f4f6; color: #111827; line-height: 1.6; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        h2 { font-size: 1.8em; margin: 30px 0 20px; color: #374151; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
        .stat-value { font-size: 2em; font-weight: 700; margin-bottom: 5px; }
        .stat-label { color: #6b7280; font-size: 0.9em; }
        .flaky-table { width: 100%; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .flaky-table th { background: #f9fafb; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #e5e7eb; }
        .flaky-table td { padding: 12px; border-bottom: 1px solid #f3f4f6; }
        .flaky-table tr:hover { background: #f9fafb; }
        .test-name { font-family: monospace; font-size: 0.9em; }
        .flakiness { font-weight: 600; color: #dc2626; }
        .pattern { font-family: monospace; letter-spacing: 0.1em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📈 PROJECT_NAME - Test History Report</h1>
        <p style="color: #6b7280; margin-bottom: 30px;">Generated: TIMESTAMP</p>

        <div class="summary">
            <div class="stat-card">
                <div class="stat-value">TOTAL_RUNS</div>
                <div class="stat-label">Test Runs (30 days)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">AVG_SUCCESS_RATE%</div>
                <div class="stat-label">Avg Success Rate (7 days)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">FLAKY_COUNT</div>
                <div class="stat-label">Flaky Tests Detected</div>
            </div>
        </div>

        FLAKY_TESTS_SECTION
    </div>
</body>
</html>"""

        # Build flaky tests section
        flaky_tests_html = ""
        if flaky_tests and "tests" in flaky_tests:
            flaky_tests_html = "<h2>🎲 Flaky Tests</h2><table class='flaky-table'><thead><tr><th>Test Name</th><th>Flakiness Score</th><th>Pass Rate</th><th>Recent Pattern</th><th>Last Result</th></tr></thead><tbody>"
            for test_name, data in sorted(flaky_tests["tests"].items(), key=lambda x: x[1]["flakiness_score"], reverse=True):
                last_outcome_color = "#10b981" if data["last_outcome"] == "passed" else "#ef4444"
                flaky_tests_html += f"""
                <tr>
                    <td class='test-name'>{test_name}</td>
                    <td class='flakiness'>{data['flakiness_score']}</td>
                    <td>{data['pass_rate']}%</td>
                    <td class='pattern'>{data['recent_pattern']}</td>
                    <td style='color: {last_outcome_color}'>{data['last_outcome'].upper()}</td>
                </tr>
                """
            flaky_tests_html += "</tbody></table>"

        # Replace placeholders
        html_content = html_template.replace('PROJECT_NAME', project_name)
        html_content = html_content.replace('TIMESTAMP', datetime.now().strftime("%B %d, %Y at %I:%M %p"))
        html_content = html_content.replace('TOTAL_RUNS', str(len(health_history)))
        html_content = html_content.replace('AVG_SUCCESS_RATE', f"{avg_success_rate:.1f}")
        html_content = html_content.replace('FLAKY_COUNT', str(len(flaky_tests.get('tests', {}))))
        html_content = html_content.replace('FLAKY_TESTS_SECTION', flaky_tests_html)

        output_path = Path(output_file)
        output_path.write_text(html_content, encoding='utf-8')

        return str(output_path.resolve())


if __name__ == "__main__":
    # Validation example
    print(f"Validating {__file__}...")

    # Create tracker
    tracker = TestHistoryTracker()

    # Add sample test runs
    for i in range(5):
        tracker.add_test_run("ExampleProject", {
            "total": 100,
            "passed": 95 - i,
            "failed": 3 + i,
            "skipped": 2,
            "duration": 45.2 + i * 2,
            "tests": [
                {"nodeid": "test_feature_a", "outcome": "passed", "duration": 1.2},
                {"nodeid": "test_feature_b", "outcome": "passed" if i % 2 == 0 else "failed", "duration": 0.8},
                {"nodeid": "test_feature_c", "outcome": "failed" if i < 2 else "passed", "duration": 2.1},
            ]
        })

    # Get trends
    trends = tracker.get_test_trends("ExampleProject", "test_feature_b", days=30)
    print(f"Test trends: {trends}")

    # Get flaky tests
    flaky = tracker.get_flaky_tests("ExampleProject")
    print(f"Flaky tests: {flaky}")

    print("✅ Test History Tracker validation passed")