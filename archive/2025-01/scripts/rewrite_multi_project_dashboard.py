#!/usr/bin/env python3
"""Rewrite the problematic sections of multi_project_dashboard.py"""

from pathlib import Path

def rewrite_dashboard():
    """Rewrite the dashboard to avoid f-string percentage issues"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/multi_project_dashboard.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find the _generate_html method and replace the problematic f-string
    # We'll replace the entire project card generation with a version that uses str.format()
    
    # Find the start of the project_cards_html f-string
    start_marker = 'project_cards_html += f"""'
    end_marker = '"""'
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find start marker")
        return
    
    # Find the matching end
    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        print("Could not find end marker")
        return
    
    # Extract the before and after parts
    before = content[:start_idx]
    after = content[end_idx + len(end_marker):]
    
    # Create a new version that uses % formatting for percentages
    new_project_card = '''project_cards_html += """
            <div class="project-card" data-health="{health}">
                <div class="project-header" style="border-left: 4px solid {health_color}">
                    <h3>{project_name}</h3>
                    <span class="health-badge" style="background: {health_color}">
                        {health_upper}
                    </span>
                </div>
                <div class="project-metrics">
                    <div class="metric">
                        <span class="metric-value">{total}</span>
                        <span class="metric-label">Total Tests</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value" style="color: #10b981">{passed}</span>
                        <span class="metric-label">Passed</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value" style="color: #ef4444">{failed}</span>
                        <span class="metric-label">Failed</span>
                    </div>
                    <div class="metric">
                        <span class="metric-value">{success_rate_str}</span>
                        <span class="metric-label">Success Rate</span>
                    </div>
                </div>
                <div class="project-progress">
                    <div class="progress-bar">
                        <div class="progress-fill passed" style="width: {passed_percent}%"></div>
                        <div class="progress-fill failed" style="width: {failed_percent}%"></div>
                        <div class="progress-fill skipped" style="width: {skipped_percent}%"></div>
                    </div>
                </div>
                {failed_tests_html}
                <div class="project-footer">
                    <span class="timestamp">Updated: {timestamp}</span>
                    {report_link}
                </div>
            </div>
            """.format(
                health=results.get('health', 'unknown'),
                health_color=health_color,
                project_name=project_name,
                health_upper=results.get('health', 'unknown').upper(),
                total=results.get('total', 0),
                passed=results.get('passed', 0),
                failed=results.get('failed', 0),
                success_rate_str=f"{results.get('success_rate', 0):.1f}%",
                passed_percent=results.get('passed', 0) / max(results.get('total', 1), 1) * 100,
                failed_percent=results.get('failed', 0) / max(results.get('total', 1), 1) * 100,
                skipped_percent=results.get('skipped', 0) / max(results.get('total', 1), 1) * 100,
                failed_tests_html=failed_tests_html,
                timestamp=datetime.fromisoformat(project_data['added_at']).strftime('%Y-%m-%d %H:%M'),
                report_link=f'<a href="{project_data["report_url"]}" class="view-report">View Full Report →</a>' if project_data.get("report_url") else ''
            )'''
    
    # Also fix the summary cards
    summary_start = 'summary_cards_html = f"""'
    summary_end = '"""'
    
    summary_start_idx = content.find(summary_start)
    if summary_start_idx != -1:
        summary_end_idx = content.find(summary_end, summary_start_idx + len(summary_start))
        if summary_end_idx != -1:
            # Replace the summary cards f-string too
            new_summary = '''summary_cards_html = """
        <div class="summary-card">
            <div class="summary-value">{total_projects}</div>
            <div class="summary-label">Total Projects</div>
        </div>
        <div class="summary-card">
            <div class="summary-value">{total_tests}</div>
            <div class="summary-label">Total Tests</div>
        </div>
        <div class="summary-card">
            <div class="summary-value" style="color: #10b981">{success_rate_str}</div>
            <div class="summary-label">Overall Success Rate</div>
        </div>
        <div class="summary-card">
            <div class="summary-value">{duration_str}</div>
            <div class="summary-label">Total Duration</div>
        </div>
        """.format(
            total_projects=aggregate['total_projects'],
            total_tests=aggregate['total_tests'],
            success_rate_str=f"{aggregate['overall_success_rate']:.1f}%",
            duration_str=f"{aggregate['total_duration']:.1f}s"
        )'''
            
            # Rebuild the content
            content = (content[:summary_start_idx] + 
                      new_summary + 
                      content[summary_end_idx + len(summary_end):])
    
    # Now replace the project cards part
    start_idx = content.find(start_marker)
    if start_idx != -1:
        end_idx = content.find(end_marker, start_idx + len(start_marker))
        if end_idx != -1:
            content = before + new_project_card + after
    
    # Write back
    file_path.write_text(content)
    print(f"Rewrote {file_path}")
    
    # Verify it compiles
    import subprocess
    result = subprocess.run(
        ['python', '-m', 'py_compile', str(file_path)],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ File compiles successfully!")
    else:
        print(f"❌ Still has errors:\n{result.stderr}")

if __name__ == "__main__":
    rewrite_dashboard()