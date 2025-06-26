#!/usr/bin/env python3
"""Final fix for universal report generator - replace all %% with proper escaping"""

from pathlib import Path

def fix_generator():
    """Fix the universal report generator by using a different approach"""
    file_path = Path("/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/universal_report_generator.py")
    
    # Read the file
    content = file_path.read_text()
    
    # Find the _generate_html method and replace the entire HTML generation
    # We'll use a different approach - build the CSS separately
    
    # Find where the problematic return statement starts
    start_idx = content.find('# Using string template to avoid f-string issues with CSS')
    if start_idx == -1:
        print("Could not find the marker comment")
        return
    
    # Find the end of the method (the line after the .format() call)
    end_marker = '        )\n\n    def _get_cell_class'
    end_idx = content.find(end_marker)
    if end_idx == -1:
        print("Could not find the end marker")
        return
    
    # Extract the before and after parts
    before = content[:start_idx]
    after = content[end_idx:]
    
    # Create a new implementation that avoids the percentage issue
    new_implementation = '''# Using string template to avoid f-string issues with CSS
        # Build CSS separately to avoid percentage issues
        css_content = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif; background: #f4f7f6; color: #333; line-height: 1.6; }
        .container { max-width: 95%; margin: 20px auto; padding: 20px; background: #fff; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
        header { background: """ + self.theme_color + """; color: white; padding: 30px 20px; border-radius: 8px 8px 0 0; text-align: center; }
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
        .btn-primary { background: """ + self.theme_color + """; color: white; }
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
        .cell-url a { color: """ + self.theme_color + """; text-decoration: none; } .cell-url a:hover { text-decoration: underline; }
        .card-success { color: #28a745; } .card-error { color: #dc3545; } .card-warning { color: #ffc107; } .card-info { color: #17a2b8; }
        .group-summary { background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 25px; border: 1px solid #e7eaf3;}
        .group-summary h3 { margin-bottom: 15px; font-size: 1.3em; color: #444; }
        .group-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
        .group-item { padding: 12px; background: #f9fafd; border-radius: 6px; border: 1px solid #e7eaf3; }
        .group-name { font-weight: 500; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .group-stats { display: flex; justify-content: space-between; font-size: 0.85em; color: #666; margin-bottom: 6px; }
        .group-bar { height: 5px; background: #e9ecef; border-radius: 2.5px; overflow: hidden; }
        .group-bar-fill { height: 100%; background: """ + self.theme_color + """; transition: width 0.3s; }
        .more-groups-note { font-size: 0.85em; color: #777; margin-top: 10px; text-align: center; }
        .info-bar { margin-top: 20px; padding: 10px; background: #f9fafd; border-radius: 6px; text-align: center; font-size: 0.9em; color: #666; border: 1px solid #e7eaf3; }
        .highlight { background-color: #fff3cd; font-weight: bold; }
        @media (max-width: 768px) { .controls { flex-direction: column; align-items: stretch; } .btn { width: 100%; margin-bottom: 5px; } }
        """
        
        # Build the HTML using string concatenation instead of format
        html_parts = []
        html_parts.append('<!DOCTYPE html>\\n<html lang="en">\\n<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{self.title}</title>')
        html_parts.append('    <style>')
        html_parts.append(css_content)
        html_parts.append('    </style>')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('    <div class="container">')
        html_parts.append(f'        <header><h1>{self.logo} {self.title}</h1><p class="subtitle">Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p></header>')
        html_parts.append(f'        <div class="stats-grid">{summary_cards_html}</div>')
        html_parts.append(group_summary_html)
        html_parts.append('        <div class="controls">')
        html_parts.append('            <div class="search-box"><input type="text" id="searchInput" class="search-input" placeholder="Search all fields..." onkeyup="searchTable()"><span class="search-icon">🔍</span></div>')
        html_parts.append('            <button class="btn btn-secondary" onclick="clearSearch()">Clear</button>')
        html_parts.append('            <button class="btn btn-secondary" onclick="exportToCSV()">📥 Export CSV</button>')
        html_parts.append('            <button class="btn btn-primary" onclick="window.print()">🖨️ Print</button>')
        html_parts.append('        </div>')
        html_parts.append('        <div class="table-container">')
        html_parts.append(f'            <table id="dataTable"><thead><tr>{column_headers_html}</tr></thead><tbody>{table_rows_html}</tbody></table>')
        html_parts.append('        </div>')
        html_parts.append(f'        <div class="info-bar"><span id="recordCount">{len(data)}</span> records shown. Click headers to sort.</div>')
        html_parts.append('    </div>')
        
        # JavaScript part
        js_content = """
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
            const headers = """ + json.dumps(columns) + """;
            let csvContent = headers.join(',') + '\\\\n';
            const visibleRowIndexes = Array.from(tbody.rows).filter(r => !r.classList.contains('hidden')).map(r => parseInt(r.dataset.index));
            visibleRowIndexes.forEach(idx => {
                const rowData = initialRows[idx].data;
                csvContent += rowData.map(val => `"${val.replace(/"/g, '""')}"`).join(',') + '\\\\n';
            });
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '""" + self.title.replace(" ", "_").lower() + """_report.csv';
            link.style.visibility = 'hidden'; document.body.appendChild(link); link.click(); document.body.removeChild(link);
        }
        document.addEventListener('DOMContentLoaded', () => {
            initialRows.forEach((row, index) => row.originalIndex = index);
            if (initialRows.length === 0) { document.getElementById('recordCount').textContent = 0; }
        });
        """
        
        html_parts.append('    <script>')
        html_parts.append(js_content)
        html_parts.append('    </script>')
        html_parts.append('</body></html>')
        
        return '\\n'.join(html_parts)'''
    
    # Combine the parts
    final_content = before + new_implementation + after
    
    # Write back
    file_path.write_text(final_content)
    print(f"Fixed {file_path}")
    
    # Verify the fix
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
    fix_generator()