#!/usr/bin/env python3
"""
Module: check_and_fix_all_granger_projects.py
Description: Systematically check and fix pyproject.toml files across all Granger projects

External Dependencies:
- toml: https://pypi.org/project/toml/
- GitPython: https://github.com/gitpython-developers/GitPython

Sample Input:
>>> projects = [
>>>     {"name": "granger_hub", "path": "/home/graham/workspace/experiments/granger_hub/", "github": "git+https://github.com/grahama1970/granger_hub.git"}
>>> ]

Expected Output:
>>> Checking granger_hub...
>>> ✅ pyproject.toml is valid
>>> 
>>> Summary: 1 checked, 0 fixed, 0 errors

Example Usage:
>>> python check_and_fix_all_granger_projects.py
"""

import os
import sys
import subprocess
import toml
from pathlib import Path
import json
from datetime import datetime

# Define all Granger projects based on GRANGER_PROJECTS.md
GRANGER_PROJECTS = [
    # Core Infrastructure
    {"name": "granger_hub", "path": "/home/graham/workspace/experiments/granger_hub/", "github": "git+https://github.com/grahama1970/granger_hub.git"},
    {"name": "rl_commons", "path": "/home/graham/workspace/experiments/rl_commons/", "github": "git+https://github.com/grahama1970/rl-commons.git"},
    {"name": "claude-test-reporter", "path": "/home/graham/workspace/experiments/claude-test-reporter/", "github": "git+https://github.com/grahama1970/claude-test-reporter.git"},
    {"name": "world_model", "path": "/home/graham/workspace/experiments/world_model/", "github": None},
    
    # Infrastructure Services
    {"name": "runpod_ops", "path": "/home/graham/workspace/experiments/runpod_ops/", "github": None},
    
    # Processing Spokes
    {"name": "sparta", "path": "/home/graham/workspace/experiments/sparta/", "github": "git+https://github.com/grahama1970/SPARTA.git"},
    {"name": "marker", "path": "/home/graham/workspace/experiments/marker/", "github": "git+https://github.com/grahama1970/marker.git"},
    {"name": "arangodb", "path": "/home/graham/workspace/experiments/arangodb/", "github": "git+https://github.com/grahama1970/arangodb.git"},
    {"name": "youtube_transcripts", "path": "/home/graham/workspace/experiments/youtube_transcripts/", "github": "git+https://github.com/grahama1970/youtube-transcripts-search.git"},
    {"name": "memvid", "path": "/home/graham/workspace/experiments/memvid/", "github": "git+https://github.com/grahama1970/memvid.git"},
    {"name": "llm_call", "path": "/home/graham/workspace/experiments/llm_call/", "github": "git+https://github.com/grahama1970/llm_call.git"},
    {"name": "unsloth_wip", "path": "/home/graham/workspace/experiments/fine_tuning/", "github": "git+https://github.com/grahama1970/fine_tuning.git"},
    {"name": "darpa_crawl", "path": "/home/graham/workspace/experiments/darpa_crawl/", "github": None},
    {"name": "gitget", "path": "/home/graham/workspace/experiments/gitget/", "github": None},
    {"name": "ppt", "path": "/home/graham/workspace/experiments/ppt/", "github": None},
    
    # MCP Services
    {"name": "arxiv-mcp-server", "path": "/home/graham/workspace/mcp-servers/arxiv-mcp-server/", "github": "git+https://github.com/blazickjp/arxiv-mcp-server.git"},
    {"name": "mcp-screenshot", "path": "/home/graham/workspace/experiments/mcp-screenshot/", "github": "git+https://github.com/grahama1970/mcp-screenshot.git"},
    
    # User Interfaces
    {"name": "annotator", "path": "/home/graham/workspace/experiments/annotator/", "github": "git+https://github.com/grahama1970/marker-ground-truth.git"},
    {"name": "chat", "path": "/home/graham/workspace/experiments/chat/", "github": None},
    {"name": "aider-daemon", "path": "/home/graham/workspace/experiments/aider-daemon/", "github": "git+https://github.com/grahama1970/aider-daemon.git"},
]

def fix_toml_syntax(content: str) -> tuple[str, list[str]]:
    """Fix common TOML syntax errors."""
    lines = content.splitlines()
    fixes = []
    
    for i, line in enumerate(lines):
        # Fix stray quotes after section headers
        if line.strip().startswith('[') and line.strip().endswith('"]'):
            original = line
            # Remove the extra quote
            line = line.rstrip()[:-1] + ']'
            lines[i] = line
            fixes.append(f"Line {i+1}: Fixed stray quote in section header")
        elif '[' in line and ']"' in line:
            # Another pattern: [section]"
            original = line
            line = line.replace(']"', ']')
            lines[i] = line
            if original != line:
                fixes.append(f"Line {i+1}: Fixed stray quote after section header")
    
    return '\n'.join(lines), fixes

def check_project(project: dict) -> dict:
    """Check a single project's pyproject.toml."""
    result = {
        "name": project["name"],
        "path": project["path"],
        "status": "unknown",
        "error": None,
        "fixes": [],
        "has_github": project["github"] is not None
    }
    
    pyproject_path = Path(project["path"]) / "pyproject.toml"
    
    # Check if project directory exists
    if not Path(project["path"]).exists():
        result["status"] = "missing_directory"
        result["error"] = f"Directory not found: {project['path']}"
        return result
    
    # Check if pyproject.toml exists
    if not pyproject_path.exists():
        result["status"] = "missing_pyproject"
        result["error"] = "No pyproject.toml found"
        return result
    
    # Read and check TOML syntax
    try:
        with open(pyproject_path, 'r') as f:
            content = f.read()
        
        # Try to parse as-is
        try:
            toml.loads(content)
            result["status"] = "valid"
        except toml.TomlDecodeError as e:
            # Try to fix common issues
            fixed_content, fixes = fix_toml_syntax(content)
            result["fixes"] = fixes
            
            # Try parsing fixed content
            try:
                toml.loads(fixed_content)
                # If it parses, write the fixed content
                with open(pyproject_path, 'w') as f:
                    f.write(fixed_content)
                result["status"] = "fixed"
                result["error"] = f"Fixed TOML syntax errors: {str(e)}"
            except toml.TomlDecodeError as e2:
                result["status"] = "invalid"
                result["error"] = f"Could not fix TOML: {str(e2)}"
    
    except Exception as e:
        result["status"] = "error"
        result["error"] = f"Failed to read file: {str(e)}"
    
    return result

def commit_and_push_fixes(project: dict, result: dict) -> bool:
    """Commit and push fixes if the project has a GitHub repo."""
    if not project["github"] or result["status"] != "fixed":
        return False
    
    try:
        # Change to project directory
        original_dir = os.getcwd()
        os.chdir(project["path"])
        
        # Check if there are changes
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            os.chdir(original_dir)
            return False
        
        # Add and commit
        subprocess.run(["git", "add", "pyproject.toml"], check=True)
        commit_msg = f"fix: correct pyproject.toml syntax errors\n\n" + "\n".join(result["fixes"])
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Try to push
        push_result = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        os.chdir(original_dir)
        
        if push_result.returncode == 0:
            return True
        else:
            print(f"  ⚠️  Push failed for {project['name']}: {push_result.stderr}")
            return False
            
    except Exception as e:
        os.chdir(original_dir)
        print(f"  ❌ Git operation failed for {project['name']}: {str(e)}")
        return False

def main():
    """Check all Granger projects."""
    print("=" * 80)
    print("GRANGER ECOSYSTEM PYPROJECT.TOML VERIFICATION")
    print("=" * 80)
    print(f"Checking {len(GRANGER_PROJECTS)} projects...\n")
    
    results = []
    summary = {
        "total": len(GRANGER_PROJECTS),
        "valid": 0,
        "fixed": 0,
        "invalid": 0,
        "missing_directory": 0,
        "missing_pyproject": 0,
        "error": 0,
        "pushed": 0
    }
    
    for project in GRANGER_PROJECTS:
        print(f"\n{'='*60}")
        print(f"Checking {project['name']}...")
        print(f"Path: {project['path']}")
        if project['github']:
            print(f"GitHub: {project['github']}")
        else:
            print("GitHub: ❌ No repository")
        
        result = check_project(project)
        results.append(result)
        
        # Update summary
        summary[result["status"]] = summary.get(result["status"], 0) + 1
        
        # Print result
        if result["status"] == "valid":
            print("✅ pyproject.toml is valid")
        elif result["status"] == "fixed":
            print("🔧 Fixed pyproject.toml issues:")
            for fix in result["fixes"]:
                print(f"   - {fix}")
            
            # Try to commit and push if GitHub repo exists
            if project["github"]:
                print("📤 Attempting to commit and push fixes...")
                if commit_and_push_fixes(project, result):
                    print("✅ Successfully pushed fixes to GitHub")
                    summary["pushed"] += 1
                else:
                    print("⚠️  Could not push fixes (may need manual intervention)")
        else:
            print(f"❌ {result['status']}: {result['error']}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total projects checked: {summary['total']}")
    print(f"✅ Valid: {summary['valid']}")
    print(f"🔧 Fixed: {summary['fixed']} (Pushed: {summary['pushed']})")
    print(f"❌ Invalid (unfixable): {summary['invalid']}")
    print(f"📁 Missing directory: {summary['missing_directory']}")
    print(f"📄 Missing pyproject.toml: {summary['missing_pyproject']}")
    print(f"⚠️  Errors: {summary['error']}")
    
    # Write detailed report
    report_path = Path("granger_pyproject_verification_report.json")
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "results": results
    }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Detailed report saved to: {report_path}")
    
    # Return exit code based on results
    if summary['invalid'] > 0 or summary['error'] > 0:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())