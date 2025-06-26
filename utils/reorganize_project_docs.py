#!/usr/bin/env python3
"""
Reorganize documentation for all projects to ensure clarity and consistency.

This script:
1. Creates a standard docs structure for each project
2. Archives deprecated/confusing documentation
3. Creates clear README indexes
4. Ensures no contradictory documents remain

External Dependencies:
- pathlib: Built-in path handling
- shutil: Built-in file operations

Example Usage:
>>> python reorganize_project_docs.py
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime

# Projects to reorganize (from PROJECTS.md)
PROJECTS = [
    "/home/graham/workspace/experiments/rl_commons/",
    "/home/graham/workspace/experiments/aider-daemon/",
    "/home/graham/workspace/experiments/sparta/",
    "/home/graham/workspace/experiments/marker/",
    "/home/graham/workspace/experiments/arangodb/",
    "/home/graham/workspace/experiments/chat/",
    "/home/graham/workspace/experiments/youtube_transcripts/",
    "/home/graham/workspace/experiments/claude_max_proxy/",
    "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
    "/home/graham/workspace/experiments/claude-module-communicator/",
    "/home/graham/workspace/experiments/claude-test-reporter/",
    "/home/graham/workspace/experiments/fine_tuning/",
    "/home/graham/workspace/experiments/marker-ground-truth/",
    "/home/graham/workspace/experiments/mcp-screenshot/"
]

# Standard directory structure
STANDARD_STRUCTURE = [
    "docs/01_overview",
    "docs/02_api",
    "docs/03_usage",
    "docs/04_development",
    "docs/archive"
]

# Patterns that indicate deprecated or temporary docs
DEPRECATED_PATTERNS = [
    "*_old.*", "*_backup.*", "*_deprecated.*", "*_temp.*",
    "GEMINI_*", "gemini_*", "*_OBSOLETE*", "TODO_*",
    "*_v1.*", "*_draft.*", "test_*", "old_*"
]

# Files that should be in archive
ARCHIVE_PATTERNS = [
    "correspondence", "gemini", "obsolete", "deprecated",
    "backup", "old", "legacy", "v1", "draft"
]


class ProjectDocsReorganizer:
    """Reorganize project documentation for clarity"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        self.docs_path = self.project_path / "docs"
        self.report = {
            "project": self.project_name,
            "path": str(self.project_path),
            "changes": [],
            "archived_files": [],
            "created_structure": False,
            "errors": []
        }
        
    def reorganize(self) -> Dict:
        """Main reorganization process"""
        print(f"\n{'='*60}")
        print(f"Reorganizing: {self.project_name}")
        print(f"Path: {self.project_path}")
        print(f"{'='*60}")
        
        try:
            # Check if project exists
            if not self.project_path.exists():
                self.report["errors"].append(f"Project path does not exist: {self.project_path}")
                return self.report
                
            # Check if docs directory exists
            if not self.docs_path.exists():
                print(f"No docs directory found. Creating minimal structure...")
                self.create_minimal_docs()
                return self.report
                
            # Analyze current structure
            self.analyze_current_docs()
            
            # Create standard structure
            self.create_standard_structure()
            
            # Archive deprecated docs
            self.archive_deprecated_docs()
            
            # Reorganize existing docs
            self.reorganize_existing_docs()
            
            # Create index README
            self.create_docs_index()
            
        except Exception as e:
            self.report["errors"].append(f"Error: {str(e)}")
            print(f"❌ Error reorganizing {self.project_name}: {e}")
            
        return self.report
        
    def analyze_current_docs(self):
        """Analyze current documentation structure"""
        print("\n📊 Analyzing current docs structure...")
        
        all_files = list(self.docs_path.rglob("*"))
        md_files = [f for f in all_files if f.suffix == ".md"]
        
        print(f"  Total files: {len(all_files)}")
        print(f"  Markdown files: {len(md_files)}")
        
        # Check for common patterns
        has_api_docs = any("api" in str(f).lower() for f in all_files)
        has_examples = any("example" in str(f).lower() for f in all_files)
        has_archive = (self.docs_path / "archive").exists()
        
        self.report["analysis"] = {
            "total_files": len(all_files),
            "markdown_files": len(md_files),
            "has_api_docs": has_api_docs,
            "has_examples": has_examples,
            "has_archive": has_archive
        }
        
    def create_standard_structure(self):
        """Create standard directory structure"""
        print("\n📁 Creating standard structure...")
        
        for dir_path in STANDARD_STRUCTURE:
            full_path = self.project_path / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                self.report["changes"].append(f"Created: {dir_path}")
                print(f"  ✅ Created: {dir_path}")
                
        self.report["created_structure"] = True
        
    def archive_deprecated_docs(self):
        """Move deprecated docs to archive"""
        print("\n🗄️ Archiving deprecated docs...")
        
        archive_path = self.docs_path / "archive"
        archive_path.mkdir(exist_ok=True)
        
        # Find files to archive
        for pattern in DEPRECATED_PATTERNS:
            for file in self.docs_path.rglob(pattern):
                if file.is_file() and "archive" not in str(file):
                    self.archive_file(file, archive_path)
                    
        # Archive directories with deprecated names
        for dir_name in ["correspondence", "gemini", "old", "backup", "legacy"]:
            dir_path = self.docs_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                dest = archive_path / dir_name
                shutil.move(str(dir_path), str(dest))
                self.report["archived_files"].append(f"Directory: {dir_name}")
                print(f"  📦 Archived directory: {dir_name}")
                
    def archive_file(self, file: Path, archive_path: Path):
        """Archive a single file"""
        relative_path = file.relative_to(self.docs_path)
        dest = archive_path / relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.move(str(file), str(dest))
        self.report["archived_files"].append(str(relative_path))
        print(f"  📦 Archived: {relative_path}")
        
    def reorganize_existing_docs(self):
        """Reorganize existing documentation into standard structure"""
        print("\n🔧 Reorganizing existing docs...")
        
        # Map common file patterns to new locations
        mappings = [
            ("README.md", "01_overview/README.md"),
            ("index.md", "01_overview/index.md"),
            ("overview.md", "01_overview/overview.md"),
            ("architecture.md", "01_overview/architecture.md"),
            
            ("api.md", "02_api/api.md"),
            ("API.md", "02_api/API.md"),
            ("endpoints.md", "02_api/endpoints.md"),
            ("reference.md", "02_api/reference.md"),
            
            ("usage.md", "03_usage/usage.md"),
            ("examples.md", "03_usage/examples.md"),
            ("tutorial.md", "03_usage/tutorial.md"),
            ("quickstart.md", "03_usage/quickstart.md"),
            
            ("development.md", "04_development/development.md"),
            ("contributing.md", "04_development/contributing.md"),
            ("testing.md", "04_development/testing.md"),
            ("setup.md", "04_development/setup.md")
        ]
        
        for pattern, new_location in mappings:
            files = list(self.docs_path.glob(pattern))
            for file in files:
                if file.is_file() and file.exists():
                    dest = self.docs_path / new_location
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    
                    if not dest.exists():
                        shutil.move(str(file), str(dest))
                        self.report["changes"].append(f"Moved {pattern} to {new_location}")
                        print(f"  ✅ Moved: {pattern} → {new_location}")
                        
    def create_docs_index(self):
        """Create a clear index README for docs"""
        print("\n📝 Creating docs index...")
        
        index_content = f"""# {self.project_name} Documentation

This documentation is organized for quick access and clarity.

## 📁 Directory Structure

```
docs/
├── 01_overview/     # Project overview and architecture
├── 02_api/          # API documentation and reference
├── 03_usage/        # Usage guides and examples
├── 04_development/  # Development and contribution guides
└── archive/         # Deprecated/historical docs
```

## 🚀 Quick Navigation

### Getting Started
- [Project Overview](./01_overview/README.md)
- [Quick Start Guide](./03_usage/quickstart.md)
- [API Reference](./02_api/api.md)

### For Developers
- [Development Setup](./04_development/setup.md)
- [Testing Guide](./04_development/testing.md)
- [Contributing](./04_development/contributing.md)

## 📚 Section Details

### 01_overview/
High-level project information:
- Project description and goals
- Architecture overview
- Key concepts and terminology

### 02_api/
Technical API documentation:
- Endpoint reference
- Request/response schemas
- Authentication and security

### 03_usage/
Practical usage information:
- Installation instructions
- Usage examples
- Common workflows
- Troubleshooting

### 04_development/
Development resources:
- Setting up development environment
- Running tests
- Code structure
- Contribution guidelines

## 🗂️ Archive
Historical or deprecated documentation is in `archive/` for reference only.

---

*Documentation last reorganized: {datetime.now().strftime('%Y-%m-%d')}*
"""
        
        index_path = self.docs_path / "README.md"
        index_path.write_text(index_content)
        self.report["changes"].append("Created docs/README.md index")
        print(f"  ✅ Created: docs/README.md")
        
    def create_minimal_docs(self):
        """Create minimal docs structure for projects without docs"""
        print("\n📄 Creating minimal docs structure...")
        
        # Create docs directory
        self.docs_path.mkdir(exist_ok=True)
        
        # Create minimal README
        readme_content = f"""# {self.project_name} Documentation

This project currently has minimal documentation.

## Overview
See the main [README.md](../README.md) for project information.

## Structure
```
docs/
├── 01_overview/     # Project overview (to be added)
├── 02_api/          # API documentation (to be added)
├── 03_usage/        # Usage guides (to be added)
└── 04_development/  # Development guides (to be added)
```

## Contributing
Please help improve the documentation by adding content to the appropriate sections.
"""
        
        readme_path = self.docs_path / "README.md"
        readme_path.write_text(readme_content)
        
        # Create directory structure
        for dir_path in ["01_overview", "02_api", "03_usage", "04_development"]:
            (self.docs_path / dir_path).mkdir(exist_ok=True)
            
        self.report["changes"].append("Created minimal docs structure")
        print(f"  ✅ Created minimal docs structure")


def main():
    """Run reorganization for all projects"""
    print("🚀 Starting documentation reorganization for all projects")
    print(f"Processing {len(PROJECTS)} projects...")
    
    reports = []
    summary = {
        "total_projects": len(PROJECTS),
        "successful": 0,
        "errors": 0,
        "total_archived": 0,
        "timestamp": datetime.now().isoformat()
    }
    
    for project_path in PROJECTS:
        # Skip claude-module-communicator as requested
        if "claude-module-communicator" in project_path:
            print(f"\n⏭️ Skipping claude-module-communicator (already well-organized)")
            continue
            
        reorganizer = ProjectDocsReorganizer(project_path)
        report = reorganizer.reorganize()
        reports.append(report)
        
        if report["errors"]:
            summary["errors"] += 1
        else:
            summary["successful"] += 1
            summary["total_archived"] += len(report.get("archived_files", []))
            
    # Save summary report
    summary["reports"] = reports
    report_path = Path("docs_reorganization_report.json")
    with open(report_path, "w") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n{'='*60}")
    print("📊 REORGANIZATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total projects: {summary['total_projects']}")
    print(f"Successful: {summary['successful']}")
    print(f"Errors: {summary['errors']}")
    print(f"Total files archived: {summary['total_archived']}")
    print(f"\nDetailed report saved to: {report_path}")
    
    return summary


if __name__ == "__main__":
    summary = main()
    
    # Exit with appropriate code
    exit_code = 0 if summary["errors"] == 0 else 1
    exit(exit_code)