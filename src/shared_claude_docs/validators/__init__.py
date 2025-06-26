"""Project validation utilities."""

from pathlib import Path
import json
import os

def validate_project(project_path: Path) -> dict:
    """Validate a single project against standards."""
    issues = []
    
    # Check required files
    required_files = ["README.md", "pyproject.toml", ".gitignore"]
    for file in required_files:
        if not (project_path / file).exists():
            issues.append(f"Missing required file: {file}")
    
    # Check CLAUDE.md
    if not (project_path / "CLAUDE.md").exists():
        issues.append("Missing CLAUDE.md - AI interaction guidelines required")
    
    # Check project structure
    src_dir = project_path / "src"
    if not src_dir.exists():
        issues.append("Missing src/ directory")
    
    tests_dir = project_path / "tests"
    if not tests_dir.exists():
        issues.append("Missing tests/ directory")
    
    # Check for stray Python files in root
    stray_files = list(project_path.glob("*.py"))
    if stray_files:
        issues.append(f"Stray Python files in root: {[f.name for f in stray_files]}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "path": str(project_path)
    }

def validate_all(base_path: str = ".") -> dict:
    """Validate all projects in a directory."""
    base = Path(base_path)
    results = {}
    
    # Get experiments directory from env or use default
    if base_path == ".":
        base = Path(os.getenv("EXPERIMENTS_DIR", "/home/graham/workspace/experiments"))
    
    for project_dir in base.iterdir():
        if project_dir.is_dir() and not project_dir.name.startswith("."):
            results[project_dir.name] = validate_project(project_dir)
    
    return results
