#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Fix all imports to use absolute paths as required by CLAUDE.md standards.
"""

from pathlib import Path

def fix_imports_in_file(file_path: Path):
    """Fix imports in a single file to use absolute imports."""
    content = file_path.read_text()
    
    # Replace relative imports with absolute imports
    replacements = [
        # The fixed one
        ("from shared_claude_docs.templates.interaction_framework import (", 
         "from templates.interaction_framework import ("),
        # The original relative import
        ("from ...templates.interaction_framework import (",
         "from templates.interaction_framework import ("),
        # Test file imports
        ("from ..claude_max_proxy_interaction import",
         "from project_interactions.claude_max_proxy.claude_max_proxy_interaction import"),
        ("from ..unsloth_interaction import",
         "from project_interactions.unsloth.unsloth_interaction import"),
        ("from ..test_reporter_interaction import",
         "from project_interactions.test_reporter.test_reporter_interaction import"),
        ("from ..arxiv_marker_pipeline_interaction import",
         "from project_interactions.arxiv_marker_pipeline.arxiv_marker_pipeline_interaction import"),
        ("from ..marker_arangodb_pipeline_interaction import",
         "from project_interactions.marker_arangodb_pipeline.marker_arangodb_pipeline_interaction import"),
    ]
    
    modified = False
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            modified = True
    
    if modified:
        file_path.write_text(content)
        print(f"✅ Fixed imports in: {file_path.name}")
        return True
    return False

def main():
    """Fix imports in all generated files."""
    base_dir = Path("/home/graham/workspace/shared_claude_docs/project_interactions")
    
    # Files to fix
    files_to_fix = [
        # Interaction files
        "claude-max-proxy/claude_max_proxy_interaction.py",
        "unsloth/unsloth_interaction.py",
        "test-reporter/test_reporter_interaction.py",
        "arxiv-marker-pipeline/arxiv_marker_pipeline_interaction.py",
        "marker-arangodb-pipeline/marker_arangodb_pipeline_interaction.py",
        # Test files
        "claude-max-proxy/tests/test_claude_max_proxy.py",
        "unsloth/tests/test_unsloth.py",
        "test-reporter/tests/test_test_reporter.py",
        "arxiv-marker-pipeline/tests/test_arxiv_marker_pipeline.py",
        "marker-arangodb-pipeline/tests/test_marker_arangodb_pipeline.py",
    ]
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        full_path = base_dir / file_path
        if full_path.exists():
            if fix_imports_in_file(full_path):
                fixed_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Fixed {fixed_count} files to use absolute imports (per CLAUDE.md)")
    print("\nReminder from CLAUDE.md:")
    print("- No Conditional Imports: Never use try/except blocks for required package imports")
    print("- Always use absolute imports, not relative imports")

if __name__ == "__main__":
    main()