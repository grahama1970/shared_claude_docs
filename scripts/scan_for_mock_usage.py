#!/usr/bin/env python3
"""
Module: scan_for_mock_usage.py
Description: Scan all Granger projects for any remaining mock usage

External Dependencies:
- None

Example Usage:
>>> python scan_for_mock_usage.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def scan_file_for_mocks(file_path: Path) -> list[tuple[int, str]]:
    """Scan a file for mock usage patterns. Returns list of (line_number, line_content)."""
    mock_patterns = [
        r'\bMock\b',
        r'\bMagicMock\b',
        r'\bpatch\b',
        r'\bmonkeypatch\b',
        r'\.return_value\s*=',
        r'\.side_effect\s*=',
        r'@mock\.',
        r'unittest\.mock',
        r'pytest_mock',
        r'mock\.Mock',
        r'mock\.MagicMock',
    ]
    
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Skip comments and removed lines
                if '# REMOVED' in line or '# AUTOFIX' in line:
                    continue
                    
                for pattern in mock_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append((line_num, line.strip()))
                        break
    except Exception as e:
        pass
    
    return findings


def main():
    """Scan all projects for mock usage."""
    print("🔍 Scanning for Mock Usage in Granger Ecosystem")
    print("=" * 60)
    
    projects = [
        '/home/graham/workspace/experiments/granger_hub',
        '/home/graham/workspace/experiments/rl_commons',
        '/home/graham/workspace/experiments/claude-test-reporter',
        '/home/graham/workspace/experiments/world_model',
        '/home/graham/workspace/experiments/sparta',
        '/home/graham/workspace/experiments/marker',
        '/home/graham/workspace/experiments/arangodb',
        '/home/graham/workspace/experiments/llm_call',
        '/home/graham/workspace/experiments/unsloth_wip',
        '/home/graham/workspace/experiments/youtube_transcripts',
        '/home/graham/workspace/experiments/darpa_crawl',
        '/home/graham/workspace/experiments/gitget',
        '/home/graham/workspace/mcp-servers/arxiv-mcp-server',
        '/home/graham/workspace/experiments/mcp-screenshot',
        '/home/graham/workspace/experiments/chat',
        '/home/graham/workspace/experiments/annotator',
        '/home/graham/workspace/experiments/aider-daemon',
        '/home/graham/workspace/experiments/runpod_ops',
        '/home/graham/workspace/granger-ui',
    ]
    
    all_findings = defaultdict(list)
    
    for project_path in projects:
        project_name = Path(project_path).name
        
        if not Path(project_path).exists():
            continue
        
        # Find test files
        test_files = []
        for pattern in ['test_*.py', '*_test.py', 'tests/*.py']:
            test_files.extend(Path(project_path).rglob(pattern))
        
        # Also check src files for any mock usage
        src_files = list(Path(project_path).rglob('*.py'))
        
        for file_path in src_files:
            # Skip __pycache__ and .venv
            if '__pycache__' in str(file_path) or '.venv' in str(file_path):
                continue
            
            findings = scan_file_for_mocks(file_path)
            if findings:
                all_findings[project_name].append((file_path, findings))
    
    # Report findings
    if not all_findings:
        print("\n✅ No mock usage found in any project!")
    else:
        print(f"\n❌ Mock usage found in {len(all_findings)} projects:\n")
        
        for project_name, files in all_findings.items():
            print(f"\n📁 {project_name}:")
            for file_path, findings in files:
                relative_path = file_path.relative_to(file_path.parent.parent)
                print(f"  📄 {relative_path}:")
                for line_num, line_content in findings[:3]:  # Show first 3
                    print(f"    Line {line_num}: {line_content[:80]}...")
                if len(findings) > 3:
                    print(f"    ... and {len(findings) - 3} more occurrences")
    
    return 0 if not all_findings else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())