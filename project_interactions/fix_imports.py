#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Fix import paths in generated interaction files.
"""

import os
from pathlib import Path

def fix_imports_in_file(file_path: Path):
    """Fix import paths in a single file."""
    content = file_path.read_text()
    
    # Replace the incorrect relative import
    old_import = "from ...templates.interaction_framework import ("
    new_import = "from shared_claude_docs.templates.interaction_framework import ("
    
    if old_import in content:
        content = content.replace(old_import, new_import)
        file_path.write_text(content)
        print(f"✅ Fixed imports in: {file_path}")
        return True
    return False

def main():
    """Fix imports in all generated interaction files."""
    base_dir = Path("/home/graham/workspace/shared_claude_docs/project_interactions")
    
    # Modules to fix
    modules = [
        "claude-max-proxy",
        "unsloth", 
        "test-reporter",
        "arxiv-marker-pipeline",
        "marker-arangodb-pipeline"
    ]
    
    fixed_count = 0
    
    for module in modules:
        module_dir = base_dir / module
        if module_dir.exists():
            # Fix interaction file
            interaction_file = module_dir / f"{module.replace('-', '_')}_interaction.py"
            if interaction_file.exists():
                if fix_imports_in_file(interaction_file):
                    fixed_count += 1
    
    print(f"\n✅ Fixed {fixed_count} files")

if __name__ == "__main__":
    main()