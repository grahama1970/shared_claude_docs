#!/usr/bin/env python3
"""
Module: cleanup_project_structure.py
Description: Organize and clean up the shared_claude_docs project structure

External Dependencies:
- pathlib: https://docs.python.org/3/library/pathlib.html
- shutil: https://docs.python.org/3/library/shutil.html

Sample Input:
>>> python cleanup_project_structure.py

Expected Output:
>>> Creating directories...
>>> Moving Python scripts to archive/scripts/...
>>> Moving log files to logs/...
>>> Organizing test files...
>>> ✅ Project cleanup complete!

Example Usage:
>>> python cleanup_project_structure.py --dry-run  # Preview changes
>>> python cleanup_project_structure.py            # Execute cleanup
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

# Define project root
PROJECT_ROOT = Path(".")

# Define directory structure
DIRECTORIES = {
    "logs": PROJECT_ROOT / "logs",
    "archive": PROJECT_ROOT / "archive",
    "archive_scripts": PROJECT_ROOT / "archive" / "2025-01" / "scripts",
    "archive_fix_scripts": PROJECT_ROOT / "archive" / "2025-01" / "fix_scripts",
    "archive_reports": PROJECT_ROOT / "archive" / "2025-01" / "reports",
    "archive_temp": PROJECT_ROOT / "archive" / "2025-01" / "temp_files",
    "tests_integration": PROJECT_ROOT / "tests" / "integration",
    "tests_unit": PROJECT_ROOT / "tests" / "unit",
}

# Define file movement rules
FILE_RULES = {
    # Fix scripts to archive
    "fix_*.py": "archive_fix_scripts",
    "remove_*.py": "archive_fix_scripts",
    "restore_*.py": "archive_fix_scripts",
    "rewrite_*.py": "archive_fix_scripts",
    
    # Test and verification scripts
    "test_*.py": "archive_scripts",
    "verify_*.py": "archive_scripts",
    "run_*.py": "archive_scripts",
    
    # Bug hunter scripts
    "bug_hunter*.py": "archive_scripts",
    "*_bug_hunter*.py": "archive_scripts",
    
    # Implementation scripts
    "implement_*.py": "archive_scripts",
    "create_*.py": "archive_scripts",
    "setup_*.py": "archive_scripts",
    "deploy_*.py": "archive_scripts",
    "prepare_*.py": "archive_scripts",
    
    # Other utility scripts
    "check_*.py": "archive_scripts",
    "comprehensive_*.py": "archive_scripts",
    "complete_*.py": "archive_scripts",
    "find_*.py": "archive_scripts",
    "load_*.py": "archive_scripts",
    "multi_project_*.py": "archive_scripts",
    "universal_*.py": "archive_scripts",
    "final_*.py": "archive_scripts",
    
    # Specific one-off scripts
    "ai_verifier.py": "archive_scripts",
    "all_scenarios.py": "archive_scripts",
    "arxiv_mcp_server.py": "archive_scripts",
    "gitget.py": "archive_scripts",
    "python_arango.py": "archive_scripts",
    "python312_fstring_fixes.py": "archive_scripts",
    "world_model.py": "archive_scripts",
    
    # Log files
    "*.log": "logs",
    
    # Report markdown files
    "*_report_*.md": "archive_reports",
    "*_REPORT.md": "archive_reports",
    "*_SUMMARY.md": "archive_reports",
    "*_STATUS.md": "archive_reports",
    "*_COMPLETE.md": "archive_reports",
    "*_FIX_*.md": "archive_reports",
    "*_PLAN.md": "archive_reports",
    "ecosystem_test_*.md": "archive_reports",
    "integration_test_*.md": "archive_reports",
    
    # Deprecated/old markdown files
    "ARXIV_API_FIX_SUMMARY.md": "archive_reports",
    "BUG_FIXES_COMPLETE_REPORT.md": "archive_reports",
    "BUG_HUNT_SESSION_COMPLETE.md": "archive_reports",
    "DEPENDENCIES_STATUS.md": "archive_reports",
    "DEPENDENCY_CONFLICTS_SUMMARY.md": "archive_reports",
    "FINAL_ECOSYSTEM_STATUS_REPORT.md": "archive_reports",
    "GRANGER_ACTION_PLAN.md": "archive_reports",
    "GRANGER_AUTHENTICATION_SUMMARY.md": "archive_reports",
    "GRANGER_BUG_FIX_COMPLETE_REPORT.md": "archive_reports",
    "GRANGER_BUG_HUNT_FINAL_REPORT.md": "archive_reports",
    "GRANGER_CLEANUP_FINAL_REPORT.md": "archive_reports",
    "GRANGER_COMMANDS_CLEANUP_REPORT.md": "archive_reports",
    "GRANGER_CONFLICTS_TO_RESOLVE.md": "archive_reports",
    "GRANGER_CWE_SECURITY_ORCHESTRATION_EXAMPLE.md": "archive_reports",
    "GRANGER_ECOSYSTEM_FIX_SUMMARY.md": "archive_reports",
    "GRANGER_ECOSYSTEM_NUMPY_COMPATIBILITY_COMPLETE.md": "archive_reports",
    "GRANGER_ECOSYSTEM_STATUS_REPORT.md": "archive_reports",
    "GRANGER_FINAL_STATUS.md": "archive_reports",
    "GRANGER_FIX_INSTRUCTIONS.md": "archive_reports",
    "GRANGER_HUB_ORCHESTRATION_DEMO.md": "archive_reports",
    "GRANGER_HUB_ORCHESTRATION_UNDERSTANDING.md": "archive_reports",
    "GRANGER_PRODUCTION_DEPLOYMENT_CHECKLIST.md": "archive_reports",
    "GRANGER_PROGRESS_REPORT.md": "archive_reports",
    "GRANGER_PROTOTYPE_CONVERSION_DIRECTIVE.md": "archive_reports",
    "GRANGER_SETUP_COMPLETE.md": "archive_reports",
    "GRANGER_SYNC_SUCCESS.md": "archive_reports",
    "GRANGER_VERIFICATION_COMPLETE.md": "archive_reports",
    "HONEYPOT_FIX_SUMMARY.md": "archive_reports",
    "MOCK_REPLACEMENT_GUIDE.md": "archive_reports",
    "NUMPY_COMPATIBILITY_PLAN.md": "archive_reports",
    "PYTHON_PACKAGING_FIX_SUMMARY.md": "archive_reports",
    "RESTRUCTURE_COMPLETE.md": "archive_reports",
    "test_granger_verification.md": "archive_reports",
    "bug_hunter_baseline.md": "archive_reports",
    "critical_fixes_report.md": "archive_reports",
    "granger_dependencies_installed.md": "archive_reports",
    "granger_force_fix_report.md": "archive_reports",
    "granger_infrastructure_readiness_report.md": "archive_reports",
    "granger_phase1_fixed_report.md": "archive_reports",
    "granger_phase1_report.md": "archive_reports",
    "granger_phase2_fixes.md": "archive_reports",
    "python312_fstring_quick_reference.md": "archive_reports",
    
    # JSON files
    "*_results*.json": "archive_reports",
    "*_report*.json": "archive_reports",
    "test_*.json": "archive_reports",
    "granger_*.json": "archive_reports",
    "module_*.json": "archive_reports",
    "critical_*.json": "archive_reports",
    "mock_*.json": "archive_reports",
    "slash_commands_*.json": "archive_reports",
    "gemini_test_results.json": "archive_reports",
}

# Files to keep in root
KEEP_IN_ROOT = {
    "README.md",
    "CLAUDE.md",
    "pyproject.toml",
    "uv.lock",
    "setup.sh",
    "setup_venv.sh",
    "pytest.ini",
    ".gitignore",
    ".python-version",
    ".pre-commit-config.yaml",
    "vertex_ai_service_account.json",  # Keep credentials in root
}

# Special handling for certain files
SPECIAL_MOVES = {
    "cleanup_project_structure.py": None,  # Keep this script
    "fix_all_granger_compliance.py": None,  # Keep recent compliance fix
    "remove_all_mocks_from_granger.py": None,  # Keep recent mock removal
}


def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    for name, path in DIRECTORIES.items():
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {path}")


def should_move_file(file_path: Path) -> Tuple[bool, str]:
    """Determine if a file should be moved and where"""
    filename = file_path.name
    
    # Check if file should stay
    if filename in KEEP_IN_ROOT:
        return False, ""
    
    # Check special moves
    if filename in SPECIAL_MOVES:
        if SPECIAL_MOVES[filename] is None:
            return False, ""
        return True, SPECIAL_MOVES[filename]
    
    # Check against rules
    for pattern, destination in FILE_RULES.items():
        if "*" in pattern:
            # Handle wildcards
            if pattern.startswith("*") and pattern.endswith("*"):
                # *text* pattern
                if pattern[1:-1] in filename:
                    return True, destination
            elif pattern.startswith("*"):
                # *suffix pattern
                if filename.endswith(pattern[1:]):
                    return True, destination
            elif pattern.endswith("*"):
                # prefix* pattern
                if filename.startswith(pattern[:-1]):
                    return True, destination
        else:
            # Exact match
            if filename == pattern:
                return True, destination
    
    return False, ""


def move_files(dry_run: bool = False):
    """Move files according to rules"""
    moved_files = []
    
    # Process files in root directory
    for file_path in PROJECT_ROOT.iterdir():
        if not file_path.is_file():
            continue
            
        should_move, destination = should_move_file(file_path)
        
        if should_move:
            dest_dir = DIRECTORIES[destination]
            dest_path = dest_dir / file_path.name
            
            if dry_run:
                print(f"Would move: {file_path} -> {dest_path}")
            else:
                shutil.move(str(file_path), str(dest_path))
                print(f"Moved: {file_path} -> {dest_path}")
            
            moved_files.append((file_path, dest_path))
    
    return moved_files


def organize_tests():
    """Organize test files in tests directory"""
    print("\nOrganizing test files...")
    
    tests_dir = PROJECT_ROOT / "tests"
    
    # Move granger_interaction_tests to integration
    granger_tests = tests_dir / "granger_interaction_tests"
    if granger_tests.exists():
        dest = tests_dir / "integration" / "granger_interaction_tests"
        shutil.move(str(granger_tests), str(dest))
        print(f"  Moved granger_interaction_tests to integration/")
    
    # Keep basic tests in tests root
    # test_basic.py, conftest.py, __init__.py stay in tests/


def create_tests_readme():
    """Create comprehensive README for tests directory"""
    readme_content = """# Shared Claude Docs - Test Suite

## Overview

This directory contains all tests for the shared_claude_docs project. Tests are organized to mirror the src/ directory structure for easy navigation.

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py          # Shared pytest fixtures
├── test_basic.py        # Basic smoke tests
├── README.md           # This file
├── unit/               # Fast, isolated unit tests
│   └── (mirrors src/ structure)
└── integration/        # Integration tests requiring services
    └── granger_interaction_tests/  # Granger ecosystem tests
```

## Running Tests

### Run All Tests
```bash
# From project root
pytest

# With coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Basic smoke tests
pytest tests/test_basic.py
```

### Run Tests by Marker
```bash
# Fast tests only
pytest -m "not slow"

# Specific module tests
pytest -k "test_cli"
```

## Test Categories

1. **Unit Tests** (`tests/unit/`)
   - No external dependencies
   - No file I/O or network calls
   - Fast execution (< 1 second each)
   - Test individual functions/classes

2. **Integration Tests** (`tests/integration/`)
   - May require external services
   - Test module interactions
   - Can use real file I/O
   - May be slower

3. **Smoke Tests** (`tests/test_basic.py`)
   - Basic sanity checks
   - Verify installation works
   - Import tests

## Writing Tests

### Test File Naming
- Test files: `test_*.py`
- Test classes: `TestClassName`
- Test functions: `test_should_do_something_when_condition()`

### Example Test Structure
```python
import pytest
from shared_claude_docs.module import function_to_test

class TestModuleName:
    def test_function_returns_expected_value(self):
        # Arrange
        input_data = {"key": "value"}
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == {"processed": True}
    
    def test_function_raises_on_invalid_input(self):
        with pytest.raises(ValueError):
            function_to_test(None)
```

## Fixtures

Common fixtures are defined in `conftest.py`:
- `tmp_workspace`: Temporary directory for file operations
- `mock_config`: Test configuration

## Coverage Requirements

- Minimum coverage: 80%
- New code must include tests
- Critical paths require 100% coverage

## CI/CD Integration

Tests run automatically on:
- Pull requests
- Push to main branch
- Daily scheduled runs

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure PYTHONPATH is set
   export PYTHONPATH=./src
   ```

2. **Missing Dependencies**
   ```bash
   # Install test dependencies
   uv sync --dev
   ```

3. **Slow Tests**
   ```bash
   # Skip slow tests
   pytest -m "not slow"
   ```

## Contributing

1. Write tests for new features
2. Ensure all tests pass locally
3. Update this README if adding new test categories
4. Follow the project's coding standards
"""
    
    readme_path = PROJECT_ROOT / "tests" / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f"Created: {readme_path}")


def create_cleanup_report(moved_files: List[Tuple[Path, Path]]):
    """Create a report of cleanup actions"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = PROJECT_ROOT / "archive" / "2025-01" / f"cleanup_report_{timestamp}.md"
    
    report_content = f"""# Project Cleanup Report

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Files Moved**: {len(moved_files)}

## Summary

Cleaned up shared_claude_docs project root by:
1. Moving fix/utility scripts to archive
2. Organizing log files
3. Archiving temporary reports and JSON files
4. Organizing test directory structure

## Files Moved

| Original Location | New Location | Category |
|------------------|--------------|----------|
"""
    
    for src, dest in moved_files:
        category = dest.parent.name
        report_content += f"| {src.name} | {dest.relative_to(PROJECT_ROOT)} | {category} |\n"
    
    report_content += f"""

## Directories Created/Updated

- `logs/` - Centralized log storage
- `archive/2025-01/scripts/` - Archived utility scripts
- `archive/2025-01/fix_scripts/` - Fix and migration scripts
- `archive/2025-01/reports/` - Old reports and JSON files
- `tests/integration/` - Integration test organization

## Next Steps

1. Review archived files and delete if no longer needed
2. Update any scripts that reference moved files
3. Commit the cleaned structure
"""
    
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    print(f"\nCreated cleanup report: {report_path}")


def main():
    """Main cleanup function"""
    print("🧹 Cleaning up shared_claude_docs project structure")
    print("=" * 50)
    
    # Check for dry run
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("DRY RUN MODE - No files will be moved")
        print("-" * 50)
    
    # Create directories
    create_directories()
    
    # Move files
    print("\nMoving files...")
    moved_files = move_files(dry_run)
    
    if not dry_run:
        # Organize tests
        organize_tests()
        
        # Create tests README
        create_tests_readme()
        
        # Create cleanup report
        create_cleanup_report(moved_files)
    
    print("\n✅ Project cleanup complete!")
    print(f"   Files moved: {len(moved_files)}")
    
    if dry_run:
        print("\nRun without --dry-run to execute these changes")


if __name__ == "__main__":
    main()