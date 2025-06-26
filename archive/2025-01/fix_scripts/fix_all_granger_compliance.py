#!/usr/bin/env python3
"""
Module: fix_all_granger_compliance.py
Description: Fix all Granger projects to comply with mandatory standards

External Dependencies:
- toml: https://pypi.org/project/toml/

Sample Input:
>>> # Run from shared_claude_docs directory
>>> python fix_all_granger_compliance.py

Expected Output:
>>> Fixed Python version for rl_commons: >=3.10 -> >=3.10.11
>>> Fixed numpy version for granger_hub: >=1.24.0 -> ==1.26.4
>>> ... (more fixes)
>>> ✅ All projects fixed successfully

Example Usage:
>>> python fix_all_granger_compliance.py
"""

import os
import sys
from pathlib import Path
import toml
from typing import Dict, List, Tuple

# Define all projects and their locations (excluding llm_call)
PROJECTS = {
    # Core Infrastructure
    "granger_hub": "/home/graham/workspace/experiments/granger_hub",
    "rl_commons": "/home/graham/workspace/experiments/rl_commons",
    "world_model": "/home/graham/workspace/experiments/world_model",
    "claude-test-reporter": "/home/graham/workspace/experiments/claude-test-reporter",
    
    # Processing Spokes
    "sparta": "/home/graham/workspace/experiments/sparta",
    "marker": "/home/graham/workspace/experiments/marker",
    "arangodb": "/home/graham/workspace/experiments/arangodb",
    "youtube_transcripts": "/home/graham/workspace/experiments/youtube_transcripts",
    # "llm_call": EXCLUDED - being converted to Docker
    "unsloth_wip": "/home/graham/workspace/experiments/unsloth_wip",
    
    # User Interfaces
    "chat": "/home/graham/workspace/experiments/chat",
    "annotator": "/home/graham/workspace/experiments/annotator",
    "aider-daemon": "/home/graham/workspace/experiments/aider-daemon",
    
    # MCP Services
    "arxiv-mcp-server": "/home/graham/workspace/mcp-servers/arxiv-mcp-server",
    "mcp-screenshot": "/home/graham/workspace/experiments/mcp-screenshot",
    
    # Support Projects
    "gitget": "/home/graham/workspace/experiments/gitget",
    "darpa_crawl": "/home/graham/workspace/experiments/darpa_crawl",
}

# Standard versions per GRANGER_MODULE_STANDARDS.md
STANDARD_VERSIONS = {
    "python": ">=3.10.11",
    "numpy": "numpy==1.26.4",
    "pandas": "pandas>=2.2.3,<2.3.0",
    "pillow": "pillow>=10.1.0,<11.0.0",
    "pyarrow": "pyarrow>=4.0.0,<20",
}


def fix_pyproject_toml(project_name: str, project_path: str) -> List[str]:
    """Fix a single project's pyproject.toml"""
    fixes = []
    pyproject_path = Path(project_path) / "pyproject.toml"
    
    if not pyproject_path.exists():
        return [f"❌ {project_name}: pyproject.toml not found"]
    
    try:
        # Read current pyproject.toml
        with open(pyproject_path, 'r') as f:
            data = toml.load(f)
        
        # Fix Python version
        if 'project' in data:
            current_python = data['project'].get('requires-python', 'None')
            if current_python != STANDARD_VERSIONS['python']:
                data['project']['requires-python'] = STANDARD_VERSIONS['python']
                fixes.append(f"Fixed Python version: {current_python} -> {STANDARD_VERSIONS['python']}")
        else:
            # Add project section if missing
            data['project'] = {'requires-python': STANDARD_VERSIONS['python']}
            fixes.append(f"Added Python version: {STANDARD_VERSIONS['python']}")
        
        # Fix dependencies
        if 'project' in data and 'dependencies' in data['project']:
            deps = data['project']['dependencies']
            new_deps = []
            
            for dep in deps:
                dep_lower = dep.lower()
                
                # Fix numpy
                if dep_lower.startswith('numpy'):
                    if dep != STANDARD_VERSIONS['numpy']:
                        fixes.append(f"Fixed numpy: {dep} -> {STANDARD_VERSIONS['numpy']}")
                        new_deps.append(STANDARD_VERSIONS['numpy'])
                    else:
                        new_deps.append(dep)
                
                # Fix pandas
                elif dep_lower.startswith('pandas'):
                    if dep != STANDARD_VERSIONS['pandas']:
                        fixes.append(f"Fixed pandas: {dep} -> {STANDARD_VERSIONS['pandas']}")
                        new_deps.append(STANDARD_VERSIONS['pandas'])
                    else:
                        new_deps.append(dep)
                
                # Fix pillow
                elif dep_lower.startswith('pillow'):
                    if dep != STANDARD_VERSIONS['pillow']:
                        fixes.append(f"Fixed pillow: {dep} -> {STANDARD_VERSIONS['pillow']}")
                        new_deps.append(STANDARD_VERSIONS['pillow'])
                    else:
                        new_deps.append(dep)
                
                # Fix pyarrow
                elif dep_lower.startswith('pyarrow'):
                    if dep != STANDARD_VERSIONS['pyarrow']:
                        fixes.append(f"Fixed pyarrow: {dep} -> {STANDARD_VERSIONS['pyarrow']}")
                        new_deps.append(STANDARD_VERSIONS['pyarrow'])
                    else:
                        new_deps.append(dep)
                
                # Keep other dependencies
                else:
                    new_deps.append(dep)
            
            # Add pyarrow if pandas is present but pyarrow is not
            has_pandas = any(d.startswith('pandas') for d in new_deps)
            has_pyarrow = any(d.startswith('pyarrow') for d in new_deps)
            if has_pandas and not has_pyarrow:
                new_deps.append(STANDARD_VERSIONS['pyarrow'])
                fixes.append(f"Added pyarrow for pandas compatibility")
            
            data['project']['dependencies'] = new_deps
        
        # Write back the fixed pyproject.toml
        if fixes:
            with open(pyproject_path, 'w') as f:
                toml.dump(data, f)
            
            return [f"✅ {project_name}: {fix}" for fix in fixes]
        else:
            return [f"✓ {project_name}: Already compliant"]
            
    except Exception as e:
        return [f"❌ {project_name}: Error - {str(e)}"]


def remove_mocks_from_project(project_name: str, project_path: str) -> List[str]:
    """Remove mock usage from a project's tests"""
    # This would be handled by /granger-verify --fix
    # For now, we'll just report that it needs to be done
    return [f"📋 {project_name}: Run '/granger-verify --fix --project {project_name}' to remove mocks"]


def main():
    """Fix all Granger projects for compliance"""
    print("🔧 Fixing Granger Projects for Standards Compliance")
    print("=" * 50)
    
    all_fixes = []
    
    # Phase 1: Fix dependency versions
    print("\n📦 Phase 1: Fixing Dependency Versions")
    print("-" * 40)
    
    for project_name, project_path in PROJECTS.items():
        fixes = fix_pyproject_toml(project_name, project_path)
        all_fixes.extend(fixes)
        for fix in fixes:
            print(fix)
    
    # Phase 2: Report mock removal needs
    print("\n🧪 Phase 2: Mock Removal Required")
    print("-" * 40)
    
    # Projects known to have mocks from audit
    mock_projects = ["granger_hub", "rl_commons", "arangodb", "marker", "sparta"]
    
    for project in mock_projects:
        if project in PROJECTS:
            fixes = remove_mocks_from_project(project, PROJECTS[project])
            all_fixes.extend(fixes)
            for fix in fixes:
                print(fix)
    
    # Summary
    print("\n📊 Summary")
    print("=" * 50)
    
    fixed_count = sum(1 for fix in all_fixes if "✅" in fix)
    already_compliant = sum(1 for fix in all_fixes if "✓" in fix)
    errors = sum(1 for fix in all_fixes if "❌" in fix)
    mock_removals = sum(1 for fix in all_fixes if "📋" in fix)
    
    print(f"✅ Fixed: {fixed_count} issues")
    print(f"✓ Already compliant: {already_compliant} projects")
    print(f"📋 Mock removal needed: {mock_removals} projects")
    print(f"❌ Errors: {errors}")
    
    print("\n🎯 Next Steps:")
    print("1. Run 'uv sync' to verify dependency fixes")
    print("2. Run mock removal for each project listed above")
    print("3. Run '/granger-verify --all' for full compliance check")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())