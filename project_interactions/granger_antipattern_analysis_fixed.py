#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: granger_antipattern_analysis_fixed.py
Description: FIXED Granger ecosystem interaction using correct imports

This uses the ACTUAL module structures discovered through investigation.
NO SIMULATIONS - real module calls only.

External Dependencies:
- youtube_transcripts: Unified search functionality
- llm_call: Package-based LLM interface
- python-arango: ArangoDB client
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add paths for imports
sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/src')
sys.path.insert(0, '/home/graham/workspace/experiments')

async def main():
    """Execute FIXED anti-pattern analysis workflow"""
    
    print("🚀 Starting FIXED Granger Anti-Pattern Analysis")
    print("=" * 60)
    print("📍 Using correct module imports discovered through investigation")
    print("=" * 60)
    
    workflow_start = time.time()
    results = {
        "module_successes": [],
        "module_failures": [],
        "data_extracted": {}
    }
    
    # Step 1: Use youtube_transcripts with CORRECT imports
    print("\n📹 Step 1: YouTube Search with Correct Imports...")
    video_data = search_youtube_correctly(results)
    
    # Step 2: Try LLM with correct import pattern
    print("\n🤖 Step 2: LLM Call with Correct Import...")
    synthesis = await try_llm_correctly(results)
    
    # Step 3: Try ArangoDB with proper client
    print("\n💾 Step 3: ArangoDB with python-arango...")
    db_result = try_arangodb_correctly(results)
    
    # Step 4: Analyze real codebases
    print("\n🔬 Step 4: Real Codebase Analysis...")
    violations = analyze_granger_codebases()
    
    workflow_duration = time.time() - workflow_start
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FIXED Workflow Results")
    print("=" * 60)
    print(f"Duration: {workflow_duration:.2f}s")
    print(f"\nSuccessful Operations: {len(results['module_successes'])}")
    for success in results['module_successes']:
        print(f"   ✅ {success}")
    
    print(f"\nFailed Operations: {len(results['module_failures'])}")
    for failure in results['module_failures']:
        print(f"   ❌ {failure}")
    
    # Create bug fix documentation
    create_fix_documentation(results)


def search_youtube_correctly(results: dict) -> Optional[Dict[str, Any]]:
    """Use youtube_transcripts with CORRECT imports"""
    try:
        # CORRECT import based on examples/level0_demo.py
        from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig
        results['module_successes'].append("youtube_transcripts.unified_search imported successfully")
        
        # Initialize with config
        config = UnifiedSearchConfig()
        client = UnifiedYouTubeSearch(config)
        results['module_successes'].append("UnifiedYouTubeSearch client created")
        
        # Perform search
        print("   Searching for Python anti-patterns...")
        search_results = client.search("Python anti-patterns ArjanCodes", limit=5)
        
        if search_results and 'results' in search_results:
            results['module_successes'].append(f"Found {len(search_results['results'])} videos")
            results['data_extracted']['videos'] = search_results['results']
            return search_results
        else:
            results['module_failures'].append("Search returned no results")
            
    except ImportError as e:
        results['module_failures'].append(f"youtube_transcripts import still failed: {str(e)}")
    except Exception as e:
        results['module_failures'].append(f"YouTube search error: {str(e)}")
    
    return None


async def try_llm_correctly(results: dict) -> Optional[str]:
    """Try LLM with correct import pattern"""
    try:
        # First check what's in llm_call package
        import llm_call
        print(f"   llm_call package location: {llm_call.__file__}")
        
        # Try to find the correct function/class
        if hasattr(llm_call, 'call'):
            llm_function = llm_call.call
        elif hasattr(llm_call, 'llm_call'):
            llm_function = llm_call.llm_call
        else:
            # Explore the package structure
            import inspect
            members = inspect.getmembers(llm_call)
            callable_members = [name for name, obj in members if callable(obj)]
            results['module_failures'].append(f"llm_call has no 'call' or 'llm_call'. Available: {callable_members[:5]}")
            
            # Try importing from submodules
            try:
                from llm_call.core import call as llm_function
                results['module_successes'].append("Found llm_call.core.call")
            except:
                try:
                    from llm_call.api import call as llm_function
                    results['module_successes'].append("Found llm_call.api.call")
                except:
                    results['module_failures'].append("Could not find LLM call function in package")
                    return None
        
        # If we found a function, try to use it
        if 'llm_function' in locals():
            # Check if it's async
            import asyncio
            import inspect
            
            # Check if it's the 'call' function which needs special handling
            if llm_function.__name__ == 'call':
                # call() expects a config dict, not a plain string
                config = {
                    "messages": [{"role": "user", "content": "List 3 Python anti-patterns"}],
                    "max_tokens": 100
                }
                response = await llm_function(config)
            elif inspect.iscoroutinefunction(llm_function):
                response = await llm_function("List 3 Python anti-patterns", max_tokens=100)
            else:
                response = llm_function("List 3 Python anti-patterns", max_tokens=100)
            if response:
                results['module_successes'].append("LLM call succeeded")
                results['data_extracted']['llm_response'] = response
                return response
                
    except ImportError as e:
        results['module_failures'].append(f"llm_call import failed: {str(e)}")
    except Exception as e:
        results['module_failures'].append(f"LLM call error: {str(e)}")
    
    return None


def try_arangodb_correctly(results: dict) -> bool:
    """Try ArangoDB with correct package name"""
    try:
        # Check if python-arango is installed
        try:
            from arango import ArangoClient
            results['module_successes'].append("arango package imported (python-arango)")
        except ImportError:
            # Try alternate import
            from python_arango import ArangoClient
            results['module_successes'].append("python_arango imported")
        
        # Try to connect
        client = ArangoClient(hosts='http://localhost:8529')
        
        # Try to access database
        try:
            db = client.db('granger_test', username='root', password='')
            results['module_successes'].append("Connected to ArangoDB")
            
            # Try to create a test collection
            if not db.has_collection('antipattern_test'):
                db.create_collection('antipattern_test')
                results['module_successes'].append("Created test collection")
            
            return True
            
        except Exception as e:
            results['module_failures'].append(f"ArangoDB connection failed: {str(e)}")
            
    except ImportError as e:
        results['module_failures'].append(f"ArangoDB client not installed: {str(e)}")
    except Exception as e:
        results['module_failures'].append(f"ArangoDB error: {str(e)}")
    
    return False


def analyze_granger_codebases() -> Dict[str, List[Dict[str, Any]]]:
    """Analyze real Granger codebases for anti-patterns"""
    violations = {}
    
    # Simple anti-pattern checks
    antipatterns = {
        "bare_except": r"except\s*:",
        "mutable_default": r"def\s+\w+\([^)]*=\s*\[\]",
        "type_check_equality": r"type\s*\([^)]+\)\s*==",
    }
    
    # Check a few key projects
    projects = {
        "youtube_transcripts": "/home/graham/workspace/experiments/youtube_transcripts/src",
        "shared_claude_docs": "/home/graham/workspace/shared_claude_docs/src"
    }
    
    for project_name, project_path in projects.items():
        project_violations = []
        
        if Path(project_path).exists():
            py_files = list(Path(project_path).rglob("*.py"))[:10]  # Limit for demo
            
            for py_file in py_files:
                try:
                    content = py_file.read_text()
                    
                    for pattern_name, pattern in antipatterns.items():
                        import re
                        matches = re.finditer(pattern, content, re.MULTILINE)
                        
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            project_violations.append({
                                "file": str(py_file.relative_to(project_path)),
                                "line": line_num,
                                "pattern": pattern_name,
                                "code": match.group(0)
                            })
                            
                except Exception:
                    pass
        
        violations[project_name] = project_violations
    
    return violations


def create_fix_documentation(results: dict):
    """Create documentation of fixes discovered"""
    fix_doc = Path("/home/graham/workspace/shared_claude_docs/project_interactions/GRANGER_IMPORT_FIXES.md")
    
    content = [
        "# Granger Module Import Fixes",
        "",
        f"*Generated: {datetime.now().isoformat()}*",
        "",
        "## Correct Import Patterns Discovered",
        "",
        "### 1. YouTube Transcripts ✅",
        "```python",
        "# WRONG:",
        "from youtube_transcripts.technical_content_mining_interaction import TechnicalContentMiningScenario",
        "",
        "# CORRECT:",
        "from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig",
        "",
        "# Usage:",
        "config = UnifiedSearchConfig()",
        "client = UnifiedYouTubeSearch(config)",
        "results = client.search('query', limit=5)",
        "```",
        "",
        "### 2. LLM Call ❓",
        "```python",
        "# WRONG:",
        "from llm_call import llm_call",
        "",
        "# INVESTIGATING:",
        "# Package exists but function location unclear",
        "# Tried: llm_call.call, llm_call.llm_call, llm_call.core.call",
        "```",
        "",
        "### 3. ArangoDB ✅",
        "```python", 
        "# WRONG:",
        "from python_arango import ArangoClient",
        "",
        "# CORRECT (if python-arango is installed):",
        "from arango import ArangoClient",
        "```",
        "",
        "## Installation Commands Needed",
        "",
        "```bash",
        "# Install missing dependencies",
        "uv add python-arango",
        "",
        "# Install Granger modules in development mode",
        "cd /home/graham/workspace/experiments/youtube_transcripts",
        "uv pip install -e .",
        "```",
        "",
        "## Module Structure Findings",
        ""
    ]
    
    # Add actual findings
    for success in results.get('module_successes', []):
        content.append(f"- ✅ {success}")
    
    content.append("")
    content.append("## Remaining Issues")
    content.append("")
    
    for failure in results.get('module_failures', []):
        content.append(f"- ❌ {failure}")
    
    fix_doc.write_text("\n".join(content))
    print(f"\n📄 Fix documentation created: {fix_doc}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())