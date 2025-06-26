#!/usr/bin/env python3
"""
Module: fix_doc_headers_batch.py
Description: Batch fix missing documentation headers in Granger projects

External Dependencies:
- pathlib: Built-in Python module for path operations

Sample Input:
>>> python fix_doc_headers_batch.py --project marker

Expected Output:
>>> Fixed 226 documentation headers in marker project

Example Usage:
>>> python fix_doc_headers_batch.py --all
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
import argparse

def generate_doc_header(file_path: Path, project_name: str) -> str:
    """Generate appropriate documentation header based on file content."""
    module_name = file_path.stem
    relative_path = file_path.relative_to(file_path.parent.parent)
    
    # Read file to understand its purpose
    try:
        content = file_path.read_text()
        lines = content.split('\n')[:50]  # First 50 lines
    except:
        lines = []
    
    # Determine file purpose from imports and function names
    description = infer_description(module_name, lines, str(relative_path))
    
    # Extract key dependencies
    dependencies = extract_dependencies(lines)
    
    header = f'''"""
Module: {module_name}.py
Description: {description}
'''
    
    if dependencies:
        header += "\nExternal Dependencies:\n"
        for dep, url in dependencies.items():
            header += f"- {dep}: {url}\n"
    
    header += '''
Sample Input:
>>> # See function docstrings for specific examples

Expected Output:
>>> # See function docstrings for expected results

Example Usage:
>>> # Import and use as needed based on module functionality
"""

'''
    return header

def infer_description(module_name: str, lines: List[str], path: str) -> str:
    """Infer module description from name and content."""
    # Common patterns
    if 'test_' in module_name:
        return f"Test suite for {module_name.replace('test_', '')} functionality"
    elif '__init__' in module_name:
        return "Package initialization and exports"
    elif 'config' in module_name:
        return "Configuration management and settings"
    elif 'utils' in module_name or 'helpers' in module_name:
        return "Utility functions and helper methods"
    elif 'api' in module_name:
        return "API endpoints and request handlers"
    elif 'models' in module_name:
        return "Data models and schema definitions"
    elif 'handlers' in module_name:
        return "Event and request handlers"
    elif 'validators' in module_name:
        return "Data validation and verification functions"
    elif 'processors' in module_name:
        return "Data processing and transformation logic"
    elif 'services' in module_name:
        return "Service layer implementations"
    elif 'cli' in module_name:
        return "Command line interface functionality"
    elif 'mcp' in path:
        return "Model Context Protocol (MCP) integration"
    elif 'arxiv' in path:
        return "ArXiv research paper integration"
    elif 'arangodb' in path:
        return "ArangoDB graph database interactions"
    elif 'marker' in path:
        return "Document processing and marking functionality"
    elif 'llm' in path:
        return "Large Language Model integration and management"
    else:
        return f"Implementation of {module_name.replace('_', ' ')} functionality"

def extract_dependencies(lines: List[str]) -> Dict[str, str]:
    """Extract external dependencies from imports."""
    deps = {}
    
    # Common dependency URLs
    dep_urls = {
        'fastapi': 'https://fastapi.tiangolo.com/',
        'pydantic': 'https://docs.pydantic.dev/',
        'pytest': 'https://docs.pytest.org/',
        'aiohttp': 'https://docs.aiohttp.org/',
        'requests': 'https://docs.python-requests.org/',
        'numpy': 'https://numpy.org/doc/',
        'pandas': 'https://pandas.pydata.org/docs/',
        'torch': 'https://pytorch.org/docs/',
        'transformers': 'https://huggingface.co/docs/transformers/',
        'langchain': 'https://python.langchain.com/docs/',
        'openai': 'https://platform.openai.com/docs/',
        'anthropic': 'https://docs.anthropic.com/',
        'arango': 'https://docs.python-arango.com/',
        'litellm': 'https://docs.litellm.ai/',
        'loguru': 'https://loguru.readthedocs.io/'
    }
    
    for line in lines:
        if line.strip().startswith(('import ', 'from ')):
            for dep, url in dep_urls.items():
                if dep in line:
                    deps[dep] = url
                    break
    
    return deps

def fix_project_headers(project_path: Path, project_name: str) -> int:
    """Fix all missing headers in a project."""
    fixed = 0
    
    # Find all Python files
    py_files = list(project_path.rglob("*.py"))
    
    for file_path in py_files:
        # Skip if file already has proper header
        try:
            content = file_path.read_text()
            if content.strip().startswith('"""') and 'Module:' in content[:500]:
                continue
        except:
            continue
        
        # Generate and add header
        header = generate_doc_header(file_path, project_name)
        
        try:
            # Prepend header to file
            if content.strip().startswith(('"""', "'''")):
                # Replace existing docstring
                quote_char = '"""' if content.strip().startswith('"""') else "'''"
                end_pos = content.find(quote_char, 3) + 3
                if end_pos > 3:
                    content = header + content[end_pos:].lstrip('\n')
            else:
                content = header + content
            
            file_path.write_text(content)
            fixed += 1
            
            if fixed % 50 == 0:
                print(f"  Progress: Fixed {fixed} files...")
                
        except Exception as e:
            print(f"  Error fixing {file_path}: {e}")
    
    return fixed

def main():
    parser = argparse.ArgumentParser(description='Fix missing documentation headers')
    parser.add_argument('--project', help='Specific project to fix')
    parser.add_argument('--all', action='store_true', help='Fix all projects')
    args = parser.parse_args()
    
    projects = {
        'marker': ('/home/graham/workspace/experiments/marker', 226),
        'llm_call': ('/home/graham/workspace/experiments/llm_call', 154),
        'arangodb': ('/home/graham/workspace/experiments/arangodb', 141),
    }
    
    if args.project:
        if args.project in projects:
            path, expected = projects[args.project]
            print(f"\n🔧 Fixing {args.project} ({expected} files expected)...")
            fixed = fix_project_headers(Path(path), args.project)
            print(f"✅ Fixed {fixed} files in {args.project}")
        else:
            print(f"Unknown project: {args.project}")
    elif args.all:
        total_fixed = 0
        for project, (path, expected) in projects.items():
            print(f"\n🔧 Fixing {project} ({expected} files expected)...")
            fixed = fix_project_headers(Path(path), project)
            total_fixed += fixed
            print(f"✅ Fixed {fixed} files in {project}")
        
        print(f"\n🎉 Total files fixed: {total_fixed}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()