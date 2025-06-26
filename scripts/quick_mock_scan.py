#!/usr/bin/env python3
"""Quick scan to identify projects with remaining mocks."""

import os
import re
from pathlib import Path

# Projects to check
projects = [
    # Already cleaned (9 projects):
    # '/home/graham/workspace/experiments/granger_hub',
    # '/home/graham/workspace/experiments/rl_commons', 
    # '/home/graham/workspace/experiments/claude-test-reporter',
    # '/home/graham/workspace/experiments/world_model',
    # '/home/graham/workspace/experiments/sparta',
    # '/home/graham/workspace/experiments/marker',
    # '/home/graham/workspace/experiments/arangodb',
    # '/home/graham/workspace/experiments/youtube_transcripts',
    # '/home/graham/workspace/mcp-servers/arxiv-mcp-server',
    
    # Need to check (13 projects):
    '/home/graham/workspace/experiments/llm_call',
    '/home/graham/workspace/experiments/unsloth_wip',
    '/home/graham/workspace/experiments/darpa_crawl',
    '/home/graham/workspace/experiments/gitget',
    '/home/graham/workspace/experiments/mcp-screenshot',
    '/home/graham/workspace/experiments/chat',
    '/home/graham/workspace/experiments/annotator',
    '/home/graham/workspace/experiments/aider-daemon',
    '/home/graham/workspace/experiments/runpod_ops',
    '/home/graham/workspace/granger-ui',
    '/home/graham/workspace/experiments/marker-ground-truth',
    '/home/graham/workspace/experiments/memvid',
    '/home/graham/workspace/shared_claude_docs',
]

mock_patterns = [
    r'from unittest\.mock',
    r'from mock import',
    r'import mock',
    r'\.Mock\(',
    r'\.MagicMock\(',
    r'@patch',
    r'@mock\.',
]

for project in projects:
    if not Path(project).exists():
        print(f"❌ Not found: {project}")
        continue
        
    mock_count = 0
    files_with_mocks = []
    
    for py_file in Path(project).rglob('*.py'):
        if '.venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            content = py_file.read_text()
            for pattern in mock_patterns:
                if re.search(pattern, content):
                    mock_count += len(re.findall(pattern, content))
                    files_with_mocks.append(str(py_file))
                    break
        except:
            pass
    
    if mock_count > 0:
        project_name = Path(project).name
        print(f"\n📁 {project_name}: {mock_count} mocks in {len(files_with_mocks)} files")
        for f in files_with_mocks[:5]:  # Show first 5
            print(f"   - {Path(f).relative_to(project)}")
        if len(files_with_mocks) > 5:
            print(f"   ... and {len(files_with_mocks) - 5} more files")