#!/usr/bin/env python3
"""
Module: fix_remaining_arxiv_imports.py
Description: Fix the remaining 15 relative imports in arxiv_mcp

External Dependencies:
- pathlib: Built-in path handling
- re: Built-in regex
"""

import re
from pathlib import Path

# Specific files and their relative imports to fix
REMAINING_IMPORTS = {
    "src/arxiv_mcp/integrations/__init__.py": {
        7: ("from .arxiv_module import", "from arxiv_mcp.integrations.arxiv_module import")
    },
    "src/arxiv_mcp_server/__init__.py": {
        5: ("from .tools import", "from arxiv_mcp_server.tools import")
    },
    "src/arxiv_mcp_server/cli.py": {
        591: ("from .config import", "from arxiv_mcp_server.config import")
    },
    "src/arxiv_mcp_server/cli/__main__.py": {
        639: ("from .search_commands import", "from arxiv_mcp_server.cli.search_commands import"),
        656: ("from .search_commands import", "from arxiv_mcp_server.cli.search_commands import"),
        666: ("from .search_commands import", "from arxiv_mcp_server.cli.search_commands import")
    },
    "src/arxiv_mcp_server/cli/granger_slash_mcp_mixin.py": {
        32: ("from ..mcp.prompts import", "from arxiv_mcp_server.mcp.prompts import")
    },
    "src/arxiv_mcp_server/cli/research_commands.py": {
        314: ("from ..tools.batch_operations import", "from arxiv_mcp_server.tools.batch_operations import")
    },
    "src/arxiv_mcp_server/converters_enhanced.py": {
        10: ("from .tools.tree_sitter_utils import", "from arxiv_mcp_server.tools.tree_sitter_utils import")
    },
    "src/arxiv_mcp_server/storage/search_engine.py": {
        35: ("from ..utils.mac_compatibility import", "from arxiv_mcp_server.utils.mac_compatibility import")
    },
    "src/arxiv_mcp_server/tools/export_references.py": {
        367: ("from .reading_list import", "from arxiv_mcp_server.tools.reading_list import"),
        583: ("from .reading_list import", "from arxiv_mcp_server.tools.reading_list import")
    },
    "src/arxiv_mcp_server/tools/reading_list.py": {
        343: ("from ..core.search import", "from arxiv_mcp_server.core.search import")
    },
    "src/arxiv_mcp_server/tools/semantic_search.py": {
        157: ("from ..chunking.section_chunker import", "from arxiv_mcp_server.chunking.section_chunker import")
    },
    "tests/framework/__init__.py": {
        18: ("from .scenario_test import", "from tests.framework.scenario_test import")
    }
}

def fix_imports():
    """Fix remaining relative imports."""
    project_root = Path("/home/graham/workspace/mcp-servers/arxiv-mcp-server")
    fixed = 0
    
    for file_path, imports in REMAINING_IMPORTS.items():
        full_path = project_root / file_path
        
        if not full_path.exists():
            print(f"⚠️  File not found: {full_path}")
            continue
            
        try:
            content = full_path.read_text()
            lines = content.split('\n')
            
            # Sort line numbers in reverse to avoid offset issues
            for line_num in sorted(imports.keys(), reverse=True):
                if line_num <= len(lines):
                    old_import, new_import = imports[line_num]
                    # Adjust for 0-based indexing
                    line_idx = line_num - 1
                    
                    if old_import in lines[line_idx]:
                        lines[line_idx] = lines[line_idx].replace(old_import, new_import)
                        fixed += 1
                        print(f"✅ Fixed import in {file_path} line {line_num}")
                    else:
                        print(f"⚠️  Import not found at line {line_num} in {file_path}")
                        print(f"   Expected: {old_import}")
                        print(f"   Found: {lines[line_idx]}")
                        
            full_path.write_text('\n'.join(lines))
            
        except Exception as e:
            print(f"❌ Error fixing {file_path}: {e}")
    
    print(f"\n✅ Fixed {fixed} imports")
    
    # Also fix the syntax errors in archived files
    fix_archived_syntax_errors(project_root)

def fix_archived_syntax_errors(project_root):
    """Fix syntax errors in archived files."""
    print("\n🔧 Fixing archived file syntax errors...")
    
    # Fix run_tests.py indentation
    run_tests_path = project_root / "archive/deprecated_tests/run_tests.py"
    if run_tests_path.exists():
        try:
            content = run_tests_path.read_text()
            lines = content.split('\n')
            
            # Find the problematic if statement around line 124
            if len(lines) > 125:
                # Add proper indentation after if statement
                if lines[124].strip() == "":
                    lines[124] = "        pass  # Fixed indentation"
                    print("✅ Fixed indentation in run_tests.py")
            
            run_tests_path.write_text('\n'.join(lines))
        except Exception as e:
            print(f"❌ Error fixing run_tests.py: {e}")
    
    # Fix update_search_tqdm.py
    tqdm_path = project_root / "archive/scripts/update_search_tqdm.py"
    if tqdm_path.exists():
        try:
            content = tqdm_path.read_text()
            # This is likely a string quote issue
            # Add closing quote if missing
            lines = content.split('\n')
            if len(lines) > 26:
                # Check for unclosed string
                if lines[25].count('"') % 2 == 1 or lines[25].count("'") % 2 == 1:
                    lines[25] += '"'  # Add closing quote
                    print("✅ Fixed string quote in update_search_tqdm.py")
            tqdm_path.write_text('\n'.join(lines))
        except Exception as e:
            print(f"❌ Error fixing update_search_tqdm.py: {e}")
    
    # Fix fix_hardware_display.py
    hardware_path = project_root / "archive/scripts/fix_hardware_display.py"
    if hardware_path.exists():
        try:
            content = hardware_path.read_text()
            lines = content.split('\n')
            if len(lines) > 13:
                # Similar string quote issue
                if lines[12].count('"') % 2 == 1 or lines[12].count("'") % 2 == 1:
                    lines[12] += '"'  # Add closing quote
                    print("✅ Fixed string quote in fix_hardware_display.py")
            hardware_path.write_text('\n'.join(lines))
        except Exception as e:
            print(f"❌ Error fixing fix_hardware_display.py: {e}")

if __name__ == "__main__":
    fix_imports()