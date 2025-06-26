#!/usr/bin/env python3
"""Create a simple working version of universal_report_generator.py"""

from pathlib import Path

def create_simple_generator():
    """Create a simplified version that avoids percentage issues"""
    
    content = '''"""
Module: universal_report_generator.py
Description: Implementation of universal report generator functionality

External Dependencies:
- webbrowser: https://docs.python.org/3/library/webbrowser.html
- socketserver: https://docs.python.org/3/library/socketserver.html
- threading: https://docs.python.org/3/library/threading.html

Sample Input:
>>> data = [{"name": "test", "value": 100}]
>>> generator = UniversalReportGenerator()
>>> generator.generate(data, "output.html")

Expected Output:
>>> # Creates output.html with formatted report

Example Usage:
>>> from claude_test_reporter.core.generators.universal_report_generator import UniversalReportGenerator
>>> gen = UniversalReportGenerator(title="Test Report")
>>> gen.generate(test_data, "report.html")
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
import webbrowser
import os
import urllib.parse
import re


class UniversalReportGenerator:
    """Generate beautiful HTML reports with sort, search, and export features."""

    def __init__(self,
                 title: str = "Data Report",
                 theme_color: str = "#667eea",
                 logo: str = "📊",
                 base_url: Optional[str] = None):
        """
        Initialize report generator.

        Args:
            title: Report title
            theme_color: Primary color for the report
            logo: Emoji or text logo
            base_url: Base URL for serving reports
        """
        self.title = title
        self.theme_color = theme_color
        self.logo = logo
        self.base_url = base_url

    def generate(self,
                 data: List[Dict[str, Any]],
                 output_file: str = "report.html",
                 summary_stats: Optional[Dict[str, Any]] = None,
                 group_by: Optional[str] = None,
                 column_order: Optional[List[str]] = None) -> str:
        """
        Generate HTML report from data.

        Args:
            data: List of dictionaries with your data
            output_file: Output HTML filename
            summary_stats: Optional summary statistics to display as cards
            group_by: Optional field to group data by
            column_order: Optional list to specify column order

        Returns:
            Path to generated HTML file
        """
        if not data:
            columns = []
        elif column_order:
            ordered_columns = [col for col in column_order if col in data[0]]
            remaining_columns = [col for col in data[0].keys() if col not in ordered_columns]
            columns = ordered_columns + remaining_columns
        else:
            columns = list(data[0].keys()) if data else []

        if not summary_stats:
            summary_stats = self._auto_generate_summary(data, group_by)

        grouped_data = {}
        if group_by and group_by in columns and data:
            grouped_data = self._group_data(data, group_by)

        html_content = self._generate_html(data, columns, summary_stats, grouped_data, group_by)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_content, encoding='utf-8')

        return str(output_path.resolve())

    def _auto_generate_summary(self, data: List[Dict[str, Any]], group_by: Optional[str]) -> Dict[str, Any]:
        summary = {
            "Total Records": len(data),
            "Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if group_by and data:
            unique_values = set(row.get(group_by, 'Unknown') for row in data)
            summary[f"Unique {group_by.replace('_',' ').title()}"] = len(unique_values)
        return summary

    def _group_data(self, data: List[Dict[str, Any]], group_by_field: str) -> Dict[str, List[Dict]]:
        grouped = {}
        for row in data:
            key = str(row.get(group_by_field, 'Unknown'))
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(row)
        return grouped

    def _generate_html(self,
                       data: List[Dict[str, Any]],
                       columns: List[str],
                       summary_stats: Dict[str, Any],
                       grouped_data: Dict[str, List[Dict]],
                       group_by_field: Optional[str]) -> str:
        
        # Generate table rows
        table_rows_html = ""
        if data:
            for i, row_data in enumerate(data):
                table_rows_html += f"<tr data-index='{i}'>\\n"
                for col_name in columns:
                    value = row_data.get(col_name, '')
                    cell_class = self._get_cell_class(col_name, value)
                    table_rows_html += f"  <td class='{cell_class}'>{self._format_value(value)}</td>\\n"
                table_rows_html += "</tr>\\n"

        # Generate summary cards
        summary_cards_html = ""
        for label_text, stat_value in summary_stats.items():
            card_class_str = self._get_card_class(label_text)
            summary_cards_html += f"""
            <div class="stat-card">
                <div class="stat-value {card_class_str}">{self._format_value(stat_value)}</div>
                <div class="stat-label">{label_text}</div>
            </div>
            """

        # Generate group summary
        group_summary_html = ""
        if grouped_data and data:
            group_summary_html = f"<div class='group-summary'><h3>Summary by {group_by_field.replace('_',' ').title() if group_by_field else 'Group'}</h3><div class='group-grid'>"
            sorted_groups = sorted(grouped_data.items(), key=lambda item: len(item[1]), reverse=True)
            for group_name_str, items_list in sorted_groups[:10]:
                percentage_val = (len(items_list) / len(data) * 100) if data else 0
                percent_str = f"{percentage_val:.1f}%"
                group_summary_html += '<div class="group-item">'
                group_summary_html += f'<div class="group-name">{self._format_value(group_name_str)}</div>'
                group_summary_html += '<div class="group-stats">'
                group_summary_html += f'<span class="group-count">{len(items_list)} items</span>'
                group_summary_html += f'<span class="group-percent">{percent_str}</span>'
                group_summary_html += '</div>'
                group_summary_html += '<div class="group-bar">'
                group_summary_html += f'<div class="group-bar-fill" style="width: {percent_str};"></div>'
                group_summary_html += '</div>'
                group_summary_html += '</div>'
            group_summary_html += "</div></div>"

        # Generate column headers
        column_headers_html = ""
        if columns:
            for i, col_name_str in enumerate(columns):
                column_headers_html += f'<th onclick="sortTable({i})" class="sortable">{col_name_str} <span class="sort-icon">⇅</span></th>\\n'
        else:
            column_headers_html = "<th>No data to display</th>"

        # Build the HTML - using a template with placeholders
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TITLE_PLACEHOLDER</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f4f7f6; color: #333; line-height: 1.6; }
        .container { max-width: 95%; margin: 20px auto; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
        header { background: THEME_COLOR_PLACEHOLDER; color: white; padding: 30px 20px; border-radius: 8px 8px 0 0; text-align: center; }
        header h1 { font-size: 2.2em; margin-bottom: 5px; }
        header .subtitle { font-size: 1em; opacity: 0.9; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 25px 0; }
        .stat-card { background: #fff; border: 1px solid #e7eaf3; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .stat-value { font-size: 1.8em; font-weight: 600; margin-bottom: 3px; }
        .stat-label { color: #555; font-size: 0.85em; text-transform: uppercase; letter-spacing: 0.5px; }
        .controls { display: flex; gap: 10px; margin-bottom: 20px; padding: 15px; background: #f9fafd; border-radius: 8px; border: 1px solid #e7eaf3; align-items: center; flex-wrap: wrap; }
        .search-box { flex-grow: 1; position: relative; }
        .search-input { width: 100%; padding: 10px 35px 10px 15px; border: 1px solid #ccc; border-radius: 6px; font-size: 1em; }
        .search-icon { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); color: #888; }
        .btn { padding: 10px 15px; border: none; border-radius: 6px; font-size: 0.9em; font-weight: 500; cursor: pointer; transition: background-color 0.2s; text-decoration: none; display: inline-flex; align-items: center; gap: 5px; }
        .btn-primary { background: THEME_COLOR_PLACEHOLDER; color: white; }
        .btn-primary:hover { background-color: #556bb0; }
        .btn-secondary { background: #e9ecef; color: #333; }
        .btn-secondary:hover { background: #ced4da; }
        .table-container { overflow-x: auto; border: 1px solid #e7eaf3; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        table { width: 100%; border-collapse: collapse; min-width: 600px; }
        th { background: #f9fafd; padding: 10px 12px; text-align: left; font-weight: 600; cursor: pointer; user-select: none; border-bottom: 2px solid #dee2e6; }
        th .sort-icon { float: right; color: #aaa; font-size: 0.8em; }
        td { padding: 10px 12px; border-bottom: 1px solid #f1f3f5; }
        tr:nth-child(even) td { background-color: #fdfdff; }
        tr:hover td { background-color: #f0f4ff; }
        tr.hidden { display: none; }
        .cell-success { color: #28a745; } .cell-error { color: #dc3545; } .cell-warning { color: #ffc107; } .cell-info { color: #17a2b8; }
        .cell-number { text-align: right; font-variant-numeric: tabular-nums; }
        .cell-url a { color: THEME_COLOR_PLACEHOLDER; text-decoration: none; } .cell-url a:hover { text-decoration: underline; }
        .card-success { color: #28a745; } .card-error { color: #dc3545; } .card-warning { color: #ffc107; } .card-info { color: #17a2b8; }
        .group-summary { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid #e7eaf3;}
        .group-summary h3 { margin-bottom: 15px; font-size: 1.3em; color: #444; }
        .group-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
        .group-item { padding: 12px; background: #f9fafd; border-radius: 6px; border: 1px solid #e7eaf3; }
        .group-name { font-weight: 500; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .group-stats { display: flex; justify-content: space-between; font-size: 0.85em; color: #666; margin-bottom: 6px; }
        .group-bar { height: 5px; background: #e9ecef; border-radius: 2.5px; overflow: hidden; }
        .group-bar-fill { height: 100%; background: THEME_COLOR_PLACEHOLDER; transition: width 0.3s; }
        .more-groups-note { font-size: 0.85em; color: #777; margin-top: 10px; text-align: center; }
        .info-bar { margin-top: 20px; padding: 10px; background: #f9fafd; border-radius: 6px; text-align: center; font-size: 0.9em; color: #666; border: 1px solid #e7eaf3; }
        .highlight { background-color: #fff3cd; font-weight: bold; }
        @media (max-width: 768px) { .controls { flex-direction: column; align-items: stretch; } .btn { width: 100%; margin-bottom: 5px; } }
    </style>
</head>
<body>
    <div class="container">
        <header><h1>LOGO_PLACEHOLDER TITLE_PLACEHOLDER</h1><p class="subtitle">Generated: DATETIME_PLACEHOLDER</p></header>
        <div class="stats-grid">SUMMARY_CARDS_PLACEHOLDER</div>
        GROUP_SUMMARY_PLACEHOLDER
        <div class="controls">
            <div class="search-box"><input type="text" id="searchInput" class="search-input" placeholder="Search all fields..." onkeyup="searchTable()"><span class="search-icon">🔍</span></div>
            <button class="btn btn-secondary" onclick="clearSearch()">Clear</button>
            <button class="btn btn-secondary" onclick="exportToCSV()">📥 Export CSV</button>
            <button class="btn btn-primary" onclick="window.print()">🖨️ Print</button>
        </div>
        <div class="table-container">
            <table id="dataTable"><thead><tr>COLUMN_HEADERS_PLACEHOLDER</tr></thead><tbody>TABLE_ROWS_PLACEHOLDER</tbody></table>
        </div>
        <div class="info-bar"><span id="recordCount">DATA_LENGTH_PLACEHOLDER</span> records shown. Click headers to sort.</div>
    </div>
    <script>
        let sortColumn = -1, sortAsc = true;
        const table = document.getElementById('dataTable'), tbody = table.tBodies[0];
        const initialRows = Array.from(tbody.rows).map(r => { return { html: r.innerHTML, data: Array.from(r.cells).map(c => c.textContent.trim()) } });
        function renderRows(rowsToRender) { tbody.innerHTML = rowsToRender.map(r => `<tr data-index="${r.originalIndex}">${r.html}</tr>`).join(''); }

        function sortTable(columnIndex) {
            const headers = table.tHead.rows[0].cells;
            Array.from(headers).forEach(th => th.querySelector('.sort-icon').textContent = '⇅');
            sortAsc = (sortColumn === columnIndex) ? !sortAsc : true;
            sortColumn = columnIndex;
            headers[columnIndex].querySelector('.sort-icon').textContent = sortAsc ? '▲' : '▼';

            const currentVisibleRows = Array.from(tbody.rows).map(r => initialRows[parseInt(r.dataset.index)]);
            currentVisibleRows.sort((a, b) => {
                const aVal = a.data[columnIndex], bVal = b.data[columnIndex];
                const aNum = parseFloat(aVal.replace(/[^0-9.-]+/g, '')), bNum = parseFloat(bVal.replace(/[^0-9.-]+/g, ''));
                let comparison = 0;
                if (!isNaN(aNum) && !isNaN(bNum)) { comparison = aNum - bNum; }
                else { comparison = aVal.localeCompare(bVal); }
                return sortAsc ? comparison : -comparison;
            });
            tbody.innerHTML = currentVisibleRows.map(r => `<tr data-index="${r.originalIndex}">${r.html}</tr>`).join('');
        }
        function searchTable() {
            const filter = document.getElementById('searchInput').value.toUpperCase();
            let visibleCount = 0;
            initialRows.forEach((rowObj, index) => {
                const tr = tbody.querySelector(`tr[data-index='${index}']`) || document.createElement('tr');
                if (!tbody.contains(tr)) { tr.innerHTML = rowObj.html; tr.dataset.index = index; }

                const isVisible = filter === '' || rowObj.data.some(text => text.toUpperCase().includes(filter));
                tr.classList.toggle('hidden', !isVisible);
                if (isVisible) {
                    visibleCount++;
                    if (filter) {
                        Array.from(tr.cells).forEach(cell => {
                            const regex = new RegExp(filter.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\\\\\$&'), 'gi');
                            cell.innerHTML = cell.textContent.replace(regex, match => `<span class="highlight">${match}</span>`);
                        });
                    } else {
                         Array.from(tr.cells).forEach(cell => { cell.innerHTML = cell.textContent; });
                    }
                }
            });
            if (filter === '') {
                tbody.innerHTML = initialRows.map((r, idx) => `<tr data-index="${idx}">${r.html}</tr>`).join('');
            }
            document.getElementById('recordCount').textContent = visibleCount;
        }
        function clearSearch() { document.getElementById('searchInput').value = ''; searchTable(); }
        function exportToCSV() {
            const headers = COLUMNS_JSON_PLACEHOLDER;
            let csvContent = headers.join(',') + '\\n';
            const visibleRowIndexes = Array.from(tbody.rows).filter(r => !r.classList.contains('hidden')).map(r => parseInt(r.dataset.index));
            visibleRowIndexes.forEach(idx => {
                const rowData = initialRows[idx].data;
                csvContent += rowData.map(val => `"${val.replace(/"/g, '""')}"`).join(',') + '\\n';
            });
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'FILENAME_PLACEHOLDER_report.csv';
            link.style.visibility = 'hidden'; document.body.appendChild(link); link.click(); document.body.removeChild(link);
        }
        document.addEventListener('DOMContentLoaded', () => {
            initialRows.forEach((row, index) => row.originalIndex = index);
            if (initialRows.length === 0) { document.getElementById('recordCount').textContent = 0; }
        });
    </script>
</body>
</html>"""

        # Replace placeholders
        html_template = html_template.replace('TITLE_PLACEHOLDER', self.title)
        html_template = html_template.replace('THEME_COLOR_PLACEHOLDER', self.theme_color)
        html_template = html_template.replace('LOGO_PLACEHOLDER', self.logo)
        html_template = html_template.replace('DATETIME_PLACEHOLDER', datetime.now().strftime("%B %d, %Y at %I:%M %p"))
        html_template = html_template.replace('SUMMARY_CARDS_PLACEHOLDER', summary_cards_html)
        html_template = html_template.replace('GROUP_SUMMARY_PLACEHOLDER', group_summary_html)
        html_template = html_template.replace('COLUMN_HEADERS_PLACEHOLDER', column_headers_html)
        html_template = html_template.replace('TABLE_ROWS_PLACEHOLDER', table_rows_html)
        html_template = html_template.replace('DATA_LENGTH_PLACEHOLDER', str(len(data)))
        html_template = html_template.replace('COLUMNS_JSON_PLACEHOLDER', json.dumps(columns))
        html_template = html_template.replace('FILENAME_PLACEHOLDER', self.title.replace(" ", "_").lower())
        
        return html_template

    def _get_cell_class(self, column_name: str, value: Any) -> str:
        """Determine CSS class for a cell based on column name or value patterns."""
        base_class = ""
        value_str = str(value).lower()

        # Type-based classes
        if isinstance(value, (int, float)): 
            base_class = "cell-number"
        elif value_str.startswith(('http://', 'https://')): 
            base_class = "cell-url"

        # Content-based classes
        status_keywords = {
            "success": ["success", "complete", "pass", "passed", "active", "true", "yes", "✅"],
            "error": ["error", "fail", "failed", "critical", "false", "no", "❌", "❗"],
            "warning": ["warning", "pending", "caution", "skipped", "⚠️"],
            "info": ["info", "note", "notice", "❓", "🔍"]
        }
        for status_type, keywords in status_keywords.items():
            if any(keyword in value_str for keyword in keywords):
                return f"{base_class} cell-{status_type}".strip()

        # Date-like patterns
        if re.search(r'\\d{4}-\\d{2}-\\d{2}|\\d{1,2}/\\d{1,2}/\\d{2,4}', value_str) and len(value_str) < 30:
            return f"{base_class} cell-date".strip()

        return base_class.strip()

    def _get_card_class(self, label: str) -> str:
        """Determine CSS class for a summary card based on its label."""
        label_lower = label.lower()
        if any(kw in label_lower for kw in ["success", "passed", "complete", "downloaded"]): 
            return "card-success"
        if any(kw in label_lower for kw in ["fail", "error", "critical"]): 
            return "card-error"
        if any(kw in label_lower for kw in ["warning", "skipped", "attention", "paywall"]): 
            return "card-warning"
        if any(kw in label_lower for kw in ["total", "count", "unique", "duration", "rate"]): 
            return "card-info"
        return ""

    def _format_value(self, value: Any) -> str:
        """Format value for HTML display, including making URLs clickable."""
        if value is None: 
            return ""
        str_value = str(value)
        if str_value.startswith(('http://', 'https://')):
            return f'<a href="{str_value}" target="_blank" rel="noopener noreferrer">{str_value}</a>'
        if isinstance(value, bool): 
            return "Yes" if value else "No"
        if isinstance(value, (int, float)):
            try:
                if isinstance(value, float) and not value.is_integer(): 
                    return f"{value:,.2f}"
                return f"{int(value):,}"
            except TypeError:
                return str_value
        return str_value

    def serve_report(self, report_file_path: str, port: Optional[int] = None) -> str:
        """Serve the report locally and return the URL."""
        import http.server
        import socketserver
        import threading

        report_abs_path = Path(report_file_path).resolve()
        report_dir = report_abs_path.parent
        report_filename = report_abs_path.name

        # Determine host and port
        parsed_url = urllib.parse.urlparse(self.base_url or "http://localhost:8000")
        host = parsed_url.hostname or "localhost"
        final_port = port if port is not None else parsed_url.port or 8000

        # Handler that serves files from the report's directory
        class ReportHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(report_dir), **kwargs)
            def log_message(self, format, *args):
                return

        httpd = None
        # Try to bind to the port
        for p_offset in range(10):
            current_port_try = final_port + p_offset
            try:
                httpd = socketserver.TCPServer((host, current_port_try), ReportHTTPRequestHandler)
                final_port = current_port_try
                break
            except OSError as e:
                if e.errno == 98:
                    print(f"Port {current_port_try} is in use, trying next...")
                else:
                    raise

        if httpd is None:
            print(f"Could not find an available port near {final_port}.")
            return f"file://{report_abs_path}"

        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()

        served_url = f"http://{host}:{final_port}/{report_filename}"

        print(f"\\n📊 Report server started. Access at: {served_url}")
        print(f"   Local file: {report_abs_path}")
        print("   Press Ctrl+C in this terminal to stop the server.")

        try:
            webbrowser.open(served_url)
        except Exception as e_browser:
            print(f"   Could not open browser automatically: {e_browser}")

        return served_url


# Example usage
if __name__ == "__main__":
    print("Module validation...")
    
    # Test with sample data
    test_data = [
        {"name": "Test Item 1", "status": "success", "value": 100},
        {"name": "Test Item 2", "status": "failed", "value": 200},
    ]
    
    generator = UniversalReportGenerator(title="Test Report")
    output_file = generator.generate(test_data, "test_output.html")
    
    assert Path(output_file).exists(), f"Expected output file {output_file} to exist"
    print("✅ Module validation passed")
'''
    
    # Write the new content
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    file_path.write_text(content)
    print(f"Created new {file_path}")
    
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
    create_simple_generator()