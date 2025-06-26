#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: granger_full_integration_test.py
Description: Comprehensive test of ALL Granger modules to find integration bugs

This script tests EVERY module in the Granger ecosystem to find real bugs.
NO SIMULATIONS - real module calls only.

External Dependencies:
- All Granger modules installed
"""

import asyncio
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add paths for imports
sys.path.insert(0, '/home/graham/workspace/experiments')
sys.path.insert(0, '/home/graham/workspace/mcp-servers')

async def main():
    """Test ALL Granger modules to find bugs"""
    
    print("🚀 COMPREHENSIVE GRANGER MODULE INTEGRATION TEST")
    print("=" * 60)
    print("📍 Testing ALL modules to find real integration bugs")
    print("=" * 60)
    
    results = {
        "tested_modules": [],
        "successful_imports": [],
        "failed_imports": [],
        "successful_operations": [],
        "failed_operations": [],
        "bugs_found": []
    }
    
    # Test 1: Core Infrastructure Modules
    print("\n📦 Testing Core Infrastructure Modules...")
    await test_granger_hub(results)
    await test_rl_commons(results)
    await test_world_model(results)
    await test_claude_test_reporter(results)
    
    # Test 2: Processing Spokes
    print("\n🔧 Testing Processing Spoke Modules...")
    await test_sparta(results)
    await test_marker(results)
    await test_arangodb_module(results)
    await test_unsloth(results)
    await test_darpa_crawl(results)
    
    # Test 3: MCP Services
    print("\n🌐 Testing MCP Service Modules...")
    await test_arxiv_mcp_server(results)
    await test_mcp_screenshot(results)
    await test_gitget(results)
    
    # Test 4: UI Projects
    print("\n🖼️ Testing UI Modules...")
    await test_chat(results)
    await test_annotator(results)
    await test_aider_daemon(results)
    
    # Test 5: Cross-Module Integration
    print("\n🔗 Testing Cross-Module Integration...")
    await test_full_pipeline(results)
    
    # Summary
    print_summary(results)
    
    # Create comprehensive bug report
    create_bug_report(results)


async def test_granger_hub(results: dict):
    """Test granger_hub module"""
    module_name = "granger_hub"
    results["tested_modules"].append(module_name)
    
    try:
        from granger_hub import GrangerHub
        results["successful_imports"].append(f"{module_name}: GrangerHub imported")
        
        # Try to create instance
        try:
            hub = GrangerHub()
            results["successful_operations"].append(f"{module_name}: Instance created")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Instance creation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "Cannot instantiate GrangerHub",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")
        results["bugs_found"].append({
            "module": module_name,
            "bug": "Import failure",
            "error": str(e)
        })


async def test_rl_commons(results: dict):
    """Test rl_commons module"""
    module_name = "rl_commons"
    results["tested_modules"].append(module_name)
    
    try:
        from rl_commons import ContextualBandit
        results["successful_imports"].append(f"{module_name}: ContextualBandit imported")
        
        # Try to use it
        try:
            bandit = ContextualBandit(
                actions=["option1", "option2"],
                context_features=["feature1"],
                exploration_rate=0.1
            )
            action = bandit.select_action({"feature1": 0.5})
            results["successful_operations"].append(f"{module_name}: Bandit action selected")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Bandit usage failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "ContextualBandit usage error",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_world_model(results: dict):
    """Test world_model module"""
    module_name = "world_model"
    results["tested_modules"].append(module_name)
    
    try:
        from world_model import WorldModel
        results["successful_imports"].append(f"{module_name}: WorldModel imported")
        
        # Try to use it
        try:
            model = WorldModel()
            results["successful_operations"].append(f"{module_name}: Instance created")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Instance creation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "Cannot instantiate WorldModel",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_claude_test_reporter(results: dict):
    """Test claude-test-reporter module"""
    module_name = "claude-test-reporter"
    results["tested_modules"].append(module_name)
    
    try:
        from claude_test_reporter import TestReporter
        results["successful_imports"].append(f"{module_name}: TestReporter imported")
        
        # Try to use it
        try:
            reporter = TestReporter()
            results["successful_operations"].append(f"{module_name}: Instance created")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Instance creation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "Cannot instantiate TestReporter",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_sparta(results: dict):
    """Test sparta module"""
    module_name = "sparta"
    results["tested_modules"].append(module_name)
    
    try:
        from sparta import SpartaClient
        results["successful_imports"].append(f"{module_name}: SpartaClient imported")
        
        # Try to use it
        try:
            client = SpartaClient()
            # Try a search
            search_results = await client.search("CVE-2024")
            results["successful_operations"].append(f"{module_name}: Search completed")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Operation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "SpartaClient operation error",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_marker(results: dict):
    """Test marker module"""
    module_name = "marker"
    results["tested_modules"].append(module_name)
    
    try:
        from marker import process_document
        results["successful_imports"].append(f"{module_name}: process_document imported")
        
        # Try to use it
        try:
            # Test with a simple text
            result = process_document("Test document content")
            results["successful_operations"].append(f"{module_name}: Document processed")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Processing failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "Document processing error",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_arangodb_module(results: dict):
    """Test arangodb module"""
    module_name = "arangodb"
    results["tested_modules"].append(module_name)
    
    try:
        from arangodb import ArangoDBClient
        results["successful_imports"].append(f"{module_name}: ArangoDBClient imported")
        
        # Try to connect
        try:
            client = ArangoDBClient()
            # Try to list databases
            dbs = client.list_databases()
            results["successful_operations"].append(f"{module_name}: Listed databases")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Operation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "ArangoDB connection/operation error",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_unsloth(results: dict):
    """Test unsloth module"""
    module_name = "unsloth_wip"
    results["tested_modules"].append(module_name)
    
    try:
        from fine_tuning import FastLanguageModel
        results["successful_imports"].append(f"{module_name}: FastLanguageModel imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")
        results["bugs_found"].append({
            "module": module_name,
            "bug": "FastLanguageModel not available",
            "error": str(e)
        })


async def test_darpa_crawl(results: dict):
    """Test darpa_crawl module"""
    module_name = "darpa_crawl"
    results["tested_modules"].append(module_name)
    
    try:
        from darpa_crawl import DARPACrawler
        results["successful_imports"].append(f"{module_name}: DARPACrawler imported")
        
        # Try to use it
        try:
            crawler = DARPACrawler()
            results["successful_operations"].append(f"{module_name}: Instance created")
        except Exception as e:
            results["failed_operations"].append(f"{module_name}: Instance creation failed: {e}")
            results["bugs_found"].append({
                "module": module_name,
                "bug": "Cannot instantiate DARPACrawler",
                "error": str(e)
            })
            
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_arxiv_mcp_server(results: dict):
    """Test arxiv-mcp-server module"""
    module_name = "arxiv-mcp-server"
    results["tested_modules"].append(module_name)
    
    try:
        from arxiv_mcp_server import ArxivServer
        results["successful_imports"].append(f"{module_name}: ArxivServer imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_mcp_screenshot(results: dict):
    """Test mcp-screenshot module"""
    module_name = "mcp-screenshot"
    results["tested_modules"].append(module_name)
    
    try:
        from mcp_screenshot import ScreenshotServer
        results["successful_imports"].append(f"{module_name}: ScreenshotServer imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_gitget(results: dict):
    """Test gitget module"""
    module_name = "gitget"
    results["tested_modules"].append(module_name)
    
    try:
        from gitget import GitGetClient
        results["successful_imports"].append(f"{module_name}: GitGetClient imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_chat(results: dict):
    """Test chat module"""
    module_name = "chat"
    results["tested_modules"].append(module_name)
    
    try:
        from chat import ChatServer
        results["successful_imports"].append(f"{module_name}: ChatServer imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_annotator(results: dict):
    """Test annotator module"""
    module_name = "annotator"
    results["tested_modules"].append(module_name)
    
    try:
        from annotator import AnnotatorUI
        results["successful_imports"].append(f"{module_name}: AnnotatorUI imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_aider_daemon(results: dict):
    """Test aider-daemon module"""
    module_name = "aider-daemon"
    results["tested_modules"].append(module_name)
    
    try:
        from aider_daemon import AiderDaemon
        results["successful_imports"].append(f"{module_name}: AiderDaemon imported")
        
    except ImportError as e:
        results["failed_imports"].append(f"{module_name}: {str(e)}")


async def test_full_pipeline(results: dict):
    """Test a full pipeline integration"""
    print("\n   Testing YouTube → ArXiv → LLM → ArangoDB pipeline...")
    
    pipeline_bugs = []
    
    # Step 1: YouTube search
    try:
        from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig
        config = UnifiedSearchConfig()
        yt_client = UnifiedYouTubeSearch(config)
        
        # Search for content
        yt_results = yt_client.search("Python design patterns", limit=1)
        
        if yt_results and 'results' in yt_results:
            results["successful_operations"].append("Pipeline: YouTube search succeeded")
        else:
            pipeline_bugs.append("YouTube search returned no results")
            
    except Exception as e:
        pipeline_bugs.append(f"YouTube search failed: {e}")
    
    # Step 2: ArXiv search
    try:
        import arxiv
        search = arxiv.Search(
            query="Python software engineering",
            max_results=1
        )
        papers = list(search.results())
        
        if papers:
            results["successful_operations"].append("Pipeline: ArXiv search succeeded")
        else:
            pipeline_bugs.append("ArXiv search returned no results")
            
    except Exception as e:
        pipeline_bugs.append(f"ArXiv search failed: {e}")
    
    # Step 3: LLM synthesis
    try:
        from llm_call import call
        
        config = {
            "messages": [{"role": "user", "content": "Synthesize findings about Python patterns"}],
            "max_tokens": 50
        }
        
        llm_response = await call(config)
        
        if llm_response:
            results["successful_operations"].append("Pipeline: LLM synthesis succeeded")
        else:
            pipeline_bugs.append("LLM returned empty response")
            
    except Exception as e:
        pipeline_bugs.append(f"LLM synthesis failed: {e}")
    
    # Step 4: Store in ArangoDB
    try:
        from arango import ArangoClient
        client = ArangoClient(hosts='http://localhost:8529')
        
        # Try to connect
        try:
            sys_db = client.db('_system', username='root', password='')
            results["successful_operations"].append("Pipeline: ArangoDB connection succeeded")
        except Exception as e:
            pipeline_bugs.append(f"ArangoDB connection failed: {e}")
            
    except Exception as e:
        pipeline_bugs.append(f"ArangoDB client error: {e}")
    
    # Record pipeline bugs
    if pipeline_bugs:
        results["bugs_found"].append({
            "module": "Full Pipeline Integration",
            "bug": "Pipeline integration failures",
            "errors": pipeline_bugs
        })


def print_summary(results: dict):
    """Print test summary"""
    print("\n" + "=" * 60)
    print("📊 GRANGER INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    print(f"\nModules Tested: {len(results['tested_modules'])}")
    print(f"Successful Imports: {len(results['successful_imports'])}")
    print(f"Failed Imports: {len(results['failed_imports'])}")
    print(f"Successful Operations: {len(results['successful_operations'])}")
    print(f"Failed Operations: {len(results['failed_operations'])}")
    print(f"Total Bugs Found: {len(results['bugs_found'])}")
    
    if results['failed_imports']:
        print("\n❌ Failed Imports:")
        for failure in results['failed_imports']:
            print(f"   - {failure}")
    
    if results['failed_operations']:
        print("\n❌ Failed Operations:")
        for failure in results['failed_operations']:
            print(f"   - {failure}")
    
    if results['bugs_found']:
        print("\n🐛 Bugs Found:")
        for bug in results['bugs_found']:
            print(f"   - {bug['module']}: {bug['bug']}")


def create_bug_report(results: dict):
    """Create comprehensive bug report"""
    report_path = Path("/home/graham/workspace/shared_claude_docs/project_interactions/GRANGER_COMPREHENSIVE_BUG_REPORT.md")
    
    content = [
        "# Granger Comprehensive Integration Bug Report",
        "",
        f"*Generated: {datetime.now().isoformat()}*",
        "",
        "## Executive Summary",
        "",
        f"- **Modules Tested**: {len(results['tested_modules'])}",
        f"- **Import Failures**: {len(results['failed_imports'])}",
        f"- **Operation Failures**: {len(results['failed_operations'])}",
        f"- **Total Bugs Found**: {len(results['bugs_found'])}",
        "",
        "## Detailed Bug Report",
        ""
    ]
    
    # Group bugs by severity
    critical_bugs = []
    major_bugs = []
    minor_bugs = []
    
    for bug in results['bugs_found']:
        if "Import failure" in bug['bug'] or "not available" in bug['bug']:
            critical_bugs.append(bug)
        elif "operation error" in bug['bug'] or "connection" in bug['bug']:
            major_bugs.append(bug)
        else:
            minor_bugs.append(bug)
    
    if critical_bugs:
        content.extend([
            "### 🔴 Critical Bugs (Import/Module Failures)",
            ""
        ])
        for bug in critical_bugs:
            content.extend([
                f"#### {bug['module']}",
                f"**Issue**: {bug['bug']}",
                f"**Error**: `{bug.get('error', 'N/A')}`",
                ""
            ])
    
    if major_bugs:
        content.extend([
            "### 🟠 Major Bugs (Operation Failures)",
            ""
        ])
        for bug in major_bugs:
            content.extend([
                f"#### {bug['module']}",
                f"**Issue**: {bug['bug']}",
                f"**Error**: `{bug['error']}`" if 'error' in bug else f"**Errors**: {bug.get('errors', [])}",
                ""
            ])
    
    if minor_bugs:
        content.extend([
            "### 🟡 Minor Bugs",
            ""
        ])
        for bug in minor_bugs:
            content.extend([
                f"#### {bug['module']}",
                f"**Issue**: {bug['bug']}",
                f"**Error**: `{bug.get('error', 'N/A')}`",
                ""
            ])
    
    # Add recommendations
    content.extend([
        "## Recommendations",
        "",
        "### Immediate Actions Required",
        ""
    ])
    
    if any("Import failure" in bug['bug'] for bug in results['bugs_found']):
        content.append("1. **Fix module imports**: Many modules cannot be imported due to missing exports or incorrect package structure")
    
    if any("connection" in str(bug) for bug in results['bugs_found']):
        content.append("2. **Service dependencies**: Ensure all required services (ArangoDB, etc.) are running")
    
    if any("Instance creation failed" in bug['bug'] for bug in results['bugs_found']):
        content.append("3. **Constructor issues**: Many modules fail at instantiation - check required parameters")
    
    content.extend([
        "",
        "### Module Health Status",
        "",
        "| Module | Import | Operations | Status |",
        "|--------|--------|------------|--------|"
    ])
    
    for module in results['tested_modules']:
        import_ok = any(module in s for s in results['successful_imports'])
        ops_ok = any(module in s for s in results['successful_operations'])
        has_bugs = any(module == bug['module'] for bug in results['bugs_found'])
        
        status = "❌ Critical" if not import_ok else ("⚠️ Issues" if has_bugs else "✅ OK")
        
        content.append(f"| {module} | {'✅' if import_ok else '❌'} | {'✅' if ops_ok else '❌'} | {status} |")
    
    report_path.write_text("\n".join(content))
    print(f"\n📄 Comprehensive bug report created: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())