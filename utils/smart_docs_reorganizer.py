#!/usr/bin/env python3
"""
Smart documentation reorganizer that preserves good content while improving organization.

This script:
1. Analyzes existing documentation structure
2. Preserves well-organized content
3. Archives only truly deprecated/confusing docs
4. Creates a clear navigation index

External Dependencies:
- pathlib: Built-in path handling
- shutil: Built-in file operations

Example Usage:
>>> python smart_docs_reorganizer.py --project /path/to/project
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Set
import argparse
from datetime import datetime

# Files/patterns that should definitely be archived
ARCHIVE_PATTERNS = {
    "gemini": ["*GEMINI*", "*gemini*", "gemini_*"],
    "old_versions": ["*_old.*", "*_backup.*", "*_v1.*", "*_OBSOLETE*"],
    "temporary": ["*_temp.*", "*_draft.*", "TODO_*", "DEPRECATED_*"],
    "test_artifacts": ["test_report_*", "*_test_output.*"],
}

# Good patterns that should be kept and organized
KEEP_PATTERNS = {
    "architecture": ["architecture", "design", "schema", "pipeline"],
    "api": ["api", "reference", "endpoints"],
    "guides": ["guide", "tutorial", "setup", "quickstart"],
    "integration": ["integration", "mcp", "module"],
}


class SmartDocsReorganizer:
    """Intelligently reorganize project documentation"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.project_name = self.project_path.name
        self.docs_path = self.project_path / "docs"
        self.changes = []
        self.archived = []
        
    def reorganize(self):
        """Main reorganization process"""
        print(f"\n{'='*60}")
        print(f"📚 Smart Reorganization: {self.project_name}")
        print(f"📁 Path: {self.project_path}")
        print(f"{'='*60}")
        
        if not self.docs_path.exists():
            print("❌ No docs directory found.")
            return
            
        # Step 1: Archive deprecated content
        self.archive_deprecated()
        
        # Step 2: Create organized structure
        self.create_organized_structure()
        
        # Step 3: Create navigation index
        self.create_navigation_index()
        
        # Summary
        print(f"\n✅ Reorganization complete!")
        print(f"  - Archived: {len(self.archived)} files")
        print(f"  - Changes: {len(self.changes)} modifications")
        
    def archive_deprecated(self):
        """Archive only truly deprecated content"""
        print("\n🗄️ Archiving deprecated content...")
        
        archive_path = self.docs_path / "archive"
        archived_count = 0
        
        for category, patterns in ARCHIVE_PATTERNS.items():
            for pattern in patterns:
                files = list(self.docs_path.rglob(pattern))
                for file in files:
                    if file.is_file() and "archive" not in str(file):
                        # Create archive subdirectory
                        category_path = archive_path / category
                        category_path.mkdir(parents=True, exist_ok=True)
                        
                        # Move file
                        dest = category_path / file.name
                        if not dest.exists():
                            shutil.move(str(file), str(dest))
                            self.archived.append(file.name)
                            archived_count += 1
                            print(f"  📦 Archived: {file.name} → archive/{category}/")
                            
        if archived_count == 0:
            print("  ✓ No deprecated files found")
            
    def create_organized_structure(self):
        """Create a better organized structure while preserving content"""
        print("\n🔧 Organizing documentation structure...")
        
        # Define the ideal structure
        structure = {
            "00_quick_start": ["README.md", "quickstart", "getting_started"],
            "01_architecture": ["architecture", "design", "schema", "models"],
            "02_api_reference": ["api", "reference", "endpoints", "python_api"],
            "03_guides": ["guide", "tutorial", "setup", "usage"],
            "04_integration": ["integration", "mcp", "modules", "external"],
            "05_development": ["development", "contributing", "testing"],
            "06_reports": ["reports", "analysis", "validation"],
            "99_tasks": ["tasks", "TODO", "planning"]
        }
        
        # Create directories
        for dir_name in structure.keys():
            (self.docs_path / dir_name).mkdir(exist_ok=True)
            
        # Move files to appropriate directories
        for dir_name, keywords in structure.items():
            for keyword in keywords:
                # Find matching files
                files = list(self.docs_path.glob(f"*{keyword}*"))
                dirs = list(self.docs_path.glob(f"{keyword}*/"))
                
                # Move files
                for file in files:
                    if file.is_file() and file.parent == self.docs_path:
                        dest = self.docs_path / dir_name / file.name
                        if not dest.exists():
                            shutil.move(str(file), str(dest))
                            self.changes.append(f"Moved {file.name} to {dir_name}/")
                            print(f"  ✓ Organized: {file.name} → {dir_name}/")
                            
                # Move directories
                for dir_item in dirs:
                    if dir_item.is_dir() and dir_item.name not in structure:
                        dest = self.docs_path / dir_name / dir_item.name
                        if not dest.exists():
                            shutil.move(str(dir_item), str(dest))
                            self.changes.append(f"Moved {dir_item.name}/ to {dir_name}/")
                            print(f"  ✓ Organized: {dir_item.name}/ → {dir_name}/")
                            
    def create_navigation_index(self):
        """Create a clear navigation index"""
        print("\n📝 Creating navigation index...")
        
        # Scan the organized structure
        sections = []
        for dir_path in sorted(self.docs_path.iterdir()):
            if dir_path.is_dir() and not dir_path.name.startswith('.'):
                files = list(dir_path.glob("**/*.md"))
                if files:
                    sections.append({
                        "name": dir_path.name,
                        "files": [f.relative_to(self.docs_path) for f in files[:10]]  # First 10
                    })
                    
        # Create index content
        index_content = f"""# {self.project_name} Documentation

> 📚 Organized documentation for easy navigation

## 🗺️ Quick Navigation

| Section | Description | Key Documents |
|---------|-------------|---------------|
| [00_quick_start](./00_quick_start/) | Get started quickly | README, quickstart guides |
| [01_architecture](./01_architecture/) | System design & architecture | Architecture docs, schemas |
| [02_api_reference](./02_api_reference/) | API documentation | API reference, endpoints |
| [03_guides](./03_guides/) | How-to guides | Setup, usage, tutorials |
| [04_integration](./04_integration/) | Integration with other modules | MCP, module integration |
| [05_development](./05_development/) | Development resources | Contributing, testing |
| [06_reports](./06_reports/) | Analysis and reports | Test reports, validations |
| [99_tasks](./99_tasks/) | Task tracking | TODO lists, planning |

## 📁 Directory Structure

```
docs/
├── 00_quick_start/      # Start here!
├── 01_architecture/     # System design
├── 02_api_reference/    # API docs
├── 03_guides/           # How-to guides
├── 04_integration/      # Integration docs
├── 05_development/      # Dev resources
├── 06_reports/          # Reports & analysis
├── 99_tasks/            # Task tracking
└── archive/             # Deprecated docs
```

## 📚 Document Index
"""
        
        # Add file listings
        for section in sections:
            if section["files"]:
                index_content += f"\n### {section['name'].replace('_', ' ').title()}\n"
                for file in section["files"][:5]:  # Show first 5 files
                    index_content += f"- [{file.stem}](./{file})\n"
                if len(section["files"]) > 5:
                    index_content += f"- *...and {len(section['files']) - 5} more*\n"
                    
        index_content += f"""
## 🔍 Finding Information

- **New to the project?** Start with [00_quick_start](./00_quick_start/)
- **Need API details?** Check [02_api_reference](./02_api_reference/)
- **Integration help?** See [04_integration](./04_integration/)
- **Contributing?** Read [05_development](./05_development/)

## 🗄️ Archive

Deprecated or historical documentation has been moved to [archive](./archive/) for reference.

---

*Documentation reorganized on {datetime.now().strftime('%Y-%m-%d')} for clarity and easy navigation.*
"""
        
        # Write index
        index_path = self.docs_path / "README.md"
        index_path.write_text(index_content)
        print(f"  ✅ Created: docs/README.md navigation index")
        
        # Create section READMEs if they don't exist
        section_descriptions = {
            "00_quick_start": "Quick start guides and project overview",
            "01_architecture": "System architecture and design documentation",
            "02_api_reference": "API reference and technical documentation",
            "03_guides": "User guides and tutorials",
            "04_integration": "Integration with other modules and systems",
            "05_development": "Development setup and contribution guidelines",
            "06_reports": "Test reports and analysis documents",
            "99_tasks": "Task lists and project planning"
        }
        
        for dir_name, description in section_descriptions.items():
            section_path = self.docs_path / dir_name
            if section_path.exists() and not (section_path / "README.md").exists():
                readme_content = f"""# {dir_name.replace('_', ' ').title()}

> {description}

## Contents

"""
                # List files in this section
                files = list(section_path.glob("**/*.md"))
                for file in sorted(files):
                    if file.name != "README.md":
                        rel_path = file.relative_to(section_path)
                        readme_content += f"- [{file.stem}](./{rel_path})\n"
                        
                (section_path / "README.md").write_text(readme_content)
                print(f"  ✅ Created: {dir_name}/README.md")


def main():
    """Run the smart reorganizer"""
    parser = argparse.ArgumentParser(description="Smart documentation reorganizer")
    parser.add_argument("--project", type=str, help="Specific project path")
    parser.add_argument("--all", action="store_true", help="Process all projects")
    args = parser.parse_args()
    
    projects = [
        "/home/graham/workspace/experiments/sparta/",
        "/home/graham/workspace/experiments/marker/",
        "/home/graham/workspace/experiments/arangodb/",
        "/home/graham/workspace/experiments/youtube_transcripts/",
        "/home/graham/workspace/experiments/claude_max_proxy/",
        "/home/graham/workspace/mcp-servers/arxiv-mcp-server/",
        "/home/graham/workspace/experiments/claude-test-reporter/",
        "/home/graham/workspace/experiments/marker-ground-truth/",
        "/home/graham/workspace/experiments/mcp-screenshot/",
    ]
    
    if args.project:
        reorganizer = SmartDocsReorganizer(args.project)
        reorganizer.reorganize()
    elif args.all:
        for project in projects:
            # Skip claude-module-communicator
            if "claude-module-communicator" not in project:
                reorganizer = SmartDocsReorganizer(project)
                reorganizer.reorganize()
    else:
        print("Usage: python smart_docs_reorganizer.py --project /path/to/project")
        print("   or: python smart_docs_reorganizer.py --all")
        

if __name__ == "__main__":
    main()