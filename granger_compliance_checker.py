#!/usr/bin/env python3
"""
Module: granger_compliance_checker.py
Description: Comprehensive compliance assessment for Granger projects against module standards

External Dependencies:
- None (uses standard library only)

Sample Input:
>>> projects = get_projects_with_github()
>>> compliance_report = check_all_projects(projects)

Expected Output:
>>> print(compliance_report['summary'])
{'total_projects': 14, 'fully_compliant': 5, 'minor_issues': 6, 'major_issues': 3}

Example Usage:
>>> python granger_compliance_checker.py
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re
from datetime import datetime

# Projects with GitHub repositories from GRANGER_PROJECTS.md
GITHUB_PROJECTS = {
    "granger_hub": {
        "path": "/home/graham/workspace/experiments/granger_hub/",
        "github": "git+https://github.com/grahama1970/granger_hub.git"
    },
    "rl_commons": {
        "path": "/home/graham/workspace/experiments/rl_commons/",
        "github": "git+https://github.com/grahama1970/rl-commons.git"
    },
    "claude-test-reporter": {
        "path": "/home/graham/workspace/experiments/claude-test-reporter/",
        "github": "git+https://github.com/grahama1970/claude-test-reporter.git"
    },
    "sparta": {
        "path": "/home/graham/workspace/experiments/sparta/",
        "github": "git+https://github.com/grahama1970/SPARTA.git"
    },
    "marker": {
        "path": "/home/graham/workspace/experiments/marker/",
        "github": "git+https://github.com/grahama1970/marker.git"
    },
    "arangodb": {
        "path": "/home/graham/workspace/experiments/arangodb/",
        "github": "git+https://github.com/grahama1970/arangodb.git"
    },
    "youtube_transcripts": {
        "path": "/home/graham/workspace/experiments/youtube_transcripts/",
        "github": "git+https://github.com/grahama1970/youtube-transcripts-search.git"
    },
    "llm_call": {
        "path": "/home/graham/workspace/experiments/llm_call/",
        "github": "git+https://github.com/grahama1970/llm_call.git"
    },
    "unsloth_wip": {
        "path": "/home/graham/workspace/experiments/fine_tuning/",
        "github": "git+https://github.com/grahama1970/fine_tuning.git"
    },
    "arxiv-mcp-server": {
        "path": "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
        "github": "git+https://github.com/blazickjp/arxiv-mcp-server.git"
    },
    "mcp-screenshot": {
        "path": "/home/graham/workspace/experiments/mcp-screenshot/",
        "github": "git+https://github.com/grahama1970/mcp-screenshot.git"
    },
    "annotator": {
        "path": "/home/graham/workspace/experiments/annotator/",
        "github": "git+https://github.com/grahama1970/marker-ground-truth.git"
    },
    "aider-daemon": {
        "path": "/home/graham/workspace/experiments/aider-daemon/",
        "github": "git+https://github.com/grahama1970/aider-daemon.git"
    }
}

# Add memvid which was mentioned but not in the main list
GITHUB_PROJECTS["memvid"] = {
    "path": "/home/graham/workspace/experiments/memvid/",
    "github": "git+https://github.com/grahama1970/memvid.git"
}


class ComplianceChecker:
    def __init__(self):
        self.results = {}
        
    def check_project(self, name: str, info: dict) -> dict:
        """Check a single project for compliance"""
        project_path = Path(info['path'])
        
        if not project_path.exists():
            return {
                "exists": False,
                "error": f"Project path does not exist: {project_path}"
            }
            
        result = {
            "name": name,
            "path": str(project_path),
            "github": info['github'],
            "exists": True,
            "checks": {},
            "issues": [],
            "severity": "compliant"  # compliant, minor, major
        }
        
        # 1. Check pyproject.toml
        pyproject_check = self.check_pyproject_toml(project_path)
        result["checks"]["pyproject"] = pyproject_check
        
        # 2. Check .env.example
        env_check = self.check_env_example(project_path)
        result["checks"]["env_example"] = env_check
        
        # 3. Check project structure
        structure_check = self.check_project_structure(project_path)
        result["checks"]["structure"] = structure_check
        
        # 4. Check for UV usage
        uv_check = self.check_uv_usage(project_path)
        result["checks"]["uv_usage"] = uv_check
        
        # 5. Check for NO MOCKS policy
        mocks_check = self.check_no_mocks(project_path)
        result["checks"]["no_mocks"] = mocks_check
        
        # 6. Check MCP integration
        mcp_check = self.check_mcp_integration(project_path)
        result["checks"]["mcp_integration"] = mcp_check
        
        # Determine overall severity
        result["severity"] = self.determine_severity(result["checks"])
        
        return result
    
    def check_pyproject_toml(self, project_path: Path) -> dict:
        """Check pyproject.toml compliance"""
        pyproject_path = project_path / "pyproject.toml"
        
        if not pyproject_path.exists():
            return {
                "exists": False,
                "issues": ["pyproject.toml not found"],
                "severity": "major"
            }
            
        try:
            content = pyproject_path.read_text()
            issues = []
            
            # Check Python version
            python_match = re.search(r'requires-python\s*=\s*"([^"]+)"', content)
            if python_match:
                python_version = python_match.group(1)
                if not python_version.startswith(">=3.10"):
                    issues.append(f"Python version {python_version} does not meet >=3.10.11 requirement")
            else:
                issues.append("requires-python not found")
            
            # Check build system
            if "[build-system]" in content:
                if "setuptools" not in content:
                    if "hatchling" in content or "poetry" in content:
                        issues.append("Using hatchling/poetry instead of setuptools")
            else:
                issues.append("[build-system] section not found")
            
            # Check critical dependencies
            if "dependencies" in content:
                # Check numpy version
                if "numpy" in content:
                    numpy_match = re.search(r'numpy==([0-9.]+)', content)
                    if numpy_match:
                        if numpy_match.group(1) != "1.26.4":
                            issues.append(f"numpy version {numpy_match.group(1)} != 1.26.4")
                    else:
                        issues.append("numpy version not locked to 1.26.4")
                
                # Check pandas constraint
                if "pandas" in content and "pandas>=2.2.3,<2.3.0" not in content:
                    issues.append("pandas not constrained to >=2.2.3,<2.3.0")
                
                # Check pyarrow constraint
                if "pyarrow" in content:
                    if not re.search(r'pyarrow[>=<,0-9.]+,<20', content):
                        issues.append("pyarrow not constrained to <20")
                
                # Check pillow constraint
                if "pillow" in content and "pillow>=10.1.0,<11.0.0" not in content:
                    issues.append("pillow not constrained to >=10.1.0,<11.0.0")
            
            # Check GitHub dependency format
            git_deps = re.findall(r'(git\+https://[^"]+|https://github[^"]+)', content)
            for dep in git_deps:
                if not dep.startswith("git+https://"):
                    issues.append(f"GitHub dependency missing git+ prefix: {dep}")
            
            return {
                "exists": True,
                "issues": issues,
                "severity": "major" if issues else "compliant"
            }
            
        except Exception as e:
            return {
                "exists": True,
                "issues": [f"Error reading pyproject.toml: {str(e)}"],
                "severity": "major"
            }
    
    def check_env_example(self, project_path: Path) -> dict:
        """Check .env.example compliance"""
        env_path = project_path / ".env.example"
        
        if not env_path.exists():
            return {
                "exists": False,
                "issues": [".env.example not found"],
                "severity": "minor"
            }
            
        try:
            content = env_path.read_text()
            lines = content.strip().split('\n')
            issues = []
            
            # Check first line
            if not lines or not lines[0].strip().startswith("PYTHONPATH="):
                issues.append(".env.example does not start with PYTHONPATH=./src")
            elif lines[0].strip() != "PYTHONPATH=./src":
                issues.append(f"First line is '{lines[0].strip()}' not 'PYTHONPATH=./src'")
            
            return {
                "exists": True,
                "issues": issues,
                "severity": "minor" if issues else "compliant"
            }
            
        except Exception as e:
            return {
                "exists": True,
                "issues": [f"Error reading .env.example: {str(e)}"],
                "severity": "minor"
            }
    
    def check_project_structure(self, project_path: Path) -> dict:
        """Check project structure compliance"""
        issues = []
        
        # Required directories
        required_dirs = ["src", "tests", "docs", "examples"]
        for dir_name in required_dirs:
            if not (project_path / dir_name).exists():
                issues.append(f"Missing required directory: {dir_name}/")
        
        # Check for src/project_name structure
        src_path = project_path / "src"
        if src_path.exists():
            subdirs = [d for d in src_path.iterdir() if d.is_dir()]
            if not subdirs:
                issues.append("src/ directory has no subdirectories")
        
        return {
            "exists": True,
            "issues": issues,
            "severity": "minor" if issues else "compliant"
        }
    
    def check_uv_usage(self, project_path: Path) -> dict:
        """Check for UV usage documentation"""
        issues = []
        
        # Check for uv.lock
        if not (project_path / "uv.lock").exists():
            issues.append("uv.lock file not found")
        
        # Check README for UV mentions
        readme_path = project_path / "README.md"
        if readme_path.exists():
            content = readme_path.read_text().lower()
            if "uv " not in content and "uv add" not in content:
                issues.append("README.md does not mention UV usage")
        
        return {
            "exists": True,
            "issues": issues,
            "severity": "minor" if issues else "compliant"
        }
    
    def check_no_mocks(self, project_path: Path) -> dict:
        """Check for NO MOCKS policy compliance"""
        issues = []
        mock_patterns = [
            "from unittest.mock import",
            "from mock import",
            "@patch(",
            "Mock(",
            "MagicMock(",
            "@mock.",
        ]
        
        # Check test files
        test_dirs = [project_path / "tests", project_path / "test"]
        for test_dir in test_dirs:
            if test_dir.exists():
                for py_file in test_dir.rglob("*.py"):
                    try:
                        content = py_file.read_text()
                        for pattern in mock_patterns:
                            if pattern in content:
                                issues.append(f"Mock usage found in {py_file.relative_to(project_path)}")
                                break
                    except:
                        pass
        
        return {
            "exists": True,
            "issues": issues[:5],  # Limit to first 5 to avoid spam
            "total_mock_issues": len(issues),
            "severity": "major" if issues else "compliant"
        }
    
    def check_mcp_integration(self, project_path: Path) -> dict:
        """Check for MCP integration"""
        issues = []
        
        # Check for mcp.json
        if not (project_path / "mcp.json").exists():
            issues.append("mcp.json not found")
        
        # Check for MCP directory structure
        mcp_dir = project_path / "src" / "*" / "mcp"
        mcp_dirs = list(project_path.glob("src/*/mcp"))
        if not mcp_dirs:
            issues.append("No mcp/ directory found in src/")
        
        return {
            "exists": True,
            "issues": issues,
            "severity": "minor" if issues else "compliant"
        }
    
    def determine_severity(self, checks: dict) -> str:
        """Determine overall severity based on individual checks"""
        severities = []
        for check in checks.values():
            if isinstance(check, dict) and "severity" in check:
                severities.append(check["severity"])
        
        if "major" in severities:
            return "major"
        elif "minor" in severities:
            return "minor"
        else:
            return "compliant"
    
    def generate_report(self, results: List[dict]) -> dict:
        """Generate comprehensive compliance report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_projects": len(results),
            "summary": {
                "fully_compliant": 0,
                "minor_issues": 0,
                "major_issues": 0,
                "not_found": 0
            },
            "projects": {},
            "action_plan": []
        }
        
        # Process results
        for result in results:
            if not result.get("exists"):
                report["summary"]["not_found"] += 1
            elif result["severity"] == "compliant":
                report["summary"]["fully_compliant"] += 1
            elif result["severity"] == "minor":
                report["summary"]["minor_issues"] += 1
            elif result["severity"] == "major":
                report["summary"]["major_issues"] += 1
            
            report["projects"][result.get("name", "unknown")] = result
        
        # Generate action plan
        report["action_plan"] = self.generate_action_plan(results)
        
        return report
    
    def generate_action_plan(self, results: List[dict]) -> List[dict]:
        """Generate prioritized action plan"""
        actions = []
        
        # Priority 1: Major issues
        for result in results:
            if result.get("severity") == "major" and result.get("exists"):
                project_name = result["name"]
                for check_name, check_result in result["checks"].items():
                    if check_result.get("severity") == "major":
                        actions.append({
                            "priority": 1,
                            "project": project_name,
                            "category": check_name,
                            "issues": check_result.get("issues", []),
                            "action": self.get_action_for_issue(check_name, check_result)
                        })
        
        # Priority 2: Minor issues
        for result in results:
            if result.get("severity") == "minor" and result.get("exists"):
                project_name = result["name"]
                for check_name, check_result in result["checks"].items():
                    if check_result.get("severity") == "minor":
                        actions.append({
                            "priority": 2,
                            "project": project_name,
                            "category": check_name,
                            "issues": check_result.get("issues", []),
                            "action": self.get_action_for_issue(check_name, check_result)
                        })
        
        return sorted(actions, key=lambda x: (x["priority"], x["project"]))
    
    def get_action_for_issue(self, category: str, check_result: dict) -> str:
        """Get recommended action for specific issue category"""
        actions = {
            "pyproject": "Update pyproject.toml to use setuptools and correct dependency versions",
            "env_example": "Create/update .env.example with PYTHONPATH=./src as first line",
            "structure": "Create missing directories (src/, tests/, docs/, examples/)",
            "uv_usage": "Run 'uv init' and update README.md with UV instructions",
            "no_mocks": "Replace mock usage with real service connections in tests",
            "mcp_integration": "Add MCP integration following the standards guide"
        }
        return actions.get(category, "Review and fix according to standards")


def main():
    """Run compliance check on all projects"""
    checker = ComplianceChecker()
    results = []
    
    print("🔍 Granger Ecosystem Compliance Check")
    print("=" * 80)
    
    for name, info in GITHUB_PROJECTS.items():
        print(f"\nChecking {name}...")
        result = checker.check_project(name, info)
        results.append(result)
        
        if result.get("exists"):
            print(f"  ✓ Found at {info['path']}")
            print(f"  Severity: {result['severity']}")
        else:
            print(f"  ✗ Not found at {info['path']}")
    
    # Generate report
    report = checker.generate_report(results)
    
    # Save detailed report
    report_path = Path("/home/graham/workspace/shared_claude_docs/granger_compliance_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 80)
    print("📊 Compliance Summary")
    print(f"Total Projects: {report['total_projects']}")
    print(f"✅ Fully Compliant: {report['summary']['fully_compliant']}")
    print(f"⚠️  Minor Issues: {report['summary']['minor_issues']}")
    print(f"❌ Major Issues: {report['summary']['major_issues']}")
    print(f"🔍 Not Found: {report['summary']['not_found']}")
    
    print(f"\n📄 Detailed report saved to: {report_path}")
    
    return report


if __name__ == "__main__":
    report = main()