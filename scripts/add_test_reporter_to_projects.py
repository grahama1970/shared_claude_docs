#!/usr/bin/env python3
"""
Add claude-test-reporter to all projects that are missing it.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


import os
import re
from pathlib import Path
import subprocess
import sys

def backup_file(file_path):
    """Create a backup of the file."""
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    import shutil
    shutil.copy2(file_path, backup_path)
    return backup_path

def add_test_reporter_to_pyproject(pyproject_path):
    """Add claude-test-reporter to dependencies in pyproject.toml."""
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    # Check if already has claude-test-reporter
    if 'claude-test-reporter' in content:
        print(f"  ✓ Already has claude-test-reporter")
        return False
    
    # Find dependencies section
    dependencies_match = re.search(r'(dependencies = \[.*?\])', content, re.DOTALL)
    if not dependencies_match:
        print(f"  ✗ Could not find dependencies section")
        return False
    
    dependencies_section = dependencies_match.group(1)
    
    # Add claude-test-reporter before the closing bracket
    reporter_line = '    "claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main",\n'
    
    # Find the last dependency line
    lines = dependencies_section.split('\n')
    insert_pos = -1
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() and lines[i].strip() != ']':
            insert_pos = i + 1
            break
    
    if insert_pos == -1:
        print(f"  ✗ Could not find insertion point")
        return False
    
    # Insert the new dependency
    lines.insert(insert_pos, reporter_line.rstrip())
    new_dependencies = '\n'.join(lines)
    
    # Replace in content
    new_content = content.replace(dependencies_match.group(1), new_dependencies)
    
    # Backup and write
    backup_file(pyproject_path)
    with open(pyproject_path, 'w') as f:
        f.write(new_content)
    
    print(f"  ✓ Added claude-test-reporter")
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
        dry_run = True
        print("DRY RUN MODE - No changes will be made\n")
    else:
        dry_run = False
    
    experiments_dir = Path('/home/graham/workspace/experiments')
    
    # List of projects to update
    projects_to_update = [
        'agent_tools',
        'arangodb',
        'bubblewrap',
        'claude-code-mcp',
        'claude_comms',
        'claude_max_proxy',
        'code-index-mcp',
        'comms',
        'complexity',
        'docker-mcp',
        'fetch-page',
        'gitget',
        'llm-summarizer',
        'marker',
        'mcp-screenshot',
        'mcp-server-arangodb',
        'mcp_natrium_orchestrator',
        'mcp_tools',
        'pdf_extractor',
        'student_teacher',
        'unsloth_wip'
    ]
    
    print(f"Updating {len(projects_to_update)} projects with claude-test-reporter...\n")
    
    updated = 0
    failed = 0
    
    for project_name in projects_to_update:
        project_path = experiments_dir / project_name
        pyproject_path = project_path / 'pyproject.toml'
        
        print(f"Processing {project_name}...")
        
        if not pyproject_path.exists():
            print(f"  ✗ pyproject.toml not found")
            failed += 1
            continue
        
        if dry_run:
            print(f"  [DRY RUN] Would update {pyproject_path}")
            updated += 1
        else:
            if add_test_reporter_to_pyproject(pyproject_path):
                updated += 1
            else:
                failed += 1
    
    print(f"\n✅ Summary:")
    print(f"   Updated: {updated} projects")
    print(f"   Failed: {failed} projects")
    
    if not dry_run and updated > 0:
        print(f"\n📝 Note: Backup files created with .bak extension")
        print(f"   To restore: mv pyproject.toml.bak pyproject.toml")

if __name__ == '__main__':
    main()
