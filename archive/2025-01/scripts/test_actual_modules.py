#!/usr/bin/env python3
"""
Module: test_actual_modules.py
Description: Test importing actual Granger modules from their real locations

External Dependencies:
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> # No input required

Expected Output:
>>> # Shows which modules can be imported successfully

Example Usage:
>>> python test_actual_modules.py
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Configure logging
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>", level="INFO")

def setup_paths():
    """Set up Python paths for all modules"""
    paths = [
        "/home/graham/workspace/experiments/sparta/src",
        "/home/graham/workspace/experiments/marker/src",
        "/home/graham/workspace/experiments/arangodb/src",
        "/home/graham/workspace/experiments/youtube_transcripts/src",
        "/home/graham/workspace/experiments/rl_commons/src",
        "/home/graham/workspace/experiments/world_model/src",
        "/home/graham/workspace/experiments/claude-test-reporter/src",
        "/home/graham/workspace/experiments/llm_call/src",
        "/home/graham/workspace/experiments/gitget/src",
        "/home/graham/workspace/mcp-servers/arxiv-mcp-server/src",
    ]
    
    # Insert at beginning to take precedence
    for path in reversed(paths):
        if path not in sys.path:
            sys.path.insert(0, path)
    
    logger.info(f"Added {len(paths)} module paths to sys.path")

def test_module_imports():
    """Test importing each module"""
    logger.info("Testing module imports from actual locations...")
    
    test_cases = [
        # Module, Import statement, Expected class/function
        ("SPARTA", "from sparta.integrations.sparta_module import SPARTAModule", "SPARTAModule"),
        ("Marker", "from marker import convert_single_pdf", "convert_single_pdf"),
        ("YouTube", "from youtube_transcripts import YouTubeTranscripts", "YouTubeTranscripts"),
        ("RL Commons", "from rl_commons import ContextualBandit", "ContextualBandit"),
        ("World Model", "from world_model import WorldModel", "WorldModel"),
        ("GitGet", "from gitget import RepositoryAnalyzerInteraction", "RepositoryAnalyzerInteraction"),
        ("ArangoDB", "from arangodb import ArangoDBClient", "ArangoDBClient"),
        ("Test Reporter", "from claude_test_reporter import GrangerTestReporter", "GrangerTestReporter"),
        ("LLM Call", "from llm_call import llm_call", "llm_call"),
    ]
    
    results = []
    
    for module_name, import_stmt, expected_obj in test_cases:
        try:
            # Clear any cached imports
            if '.' in import_stmt:
                base_module = import_stmt.split()[1].split('.')[0]
                if base_module in sys.modules:
                    del sys.modules[base_module]
            
            # Try the import
            exec(import_stmt, globals())
            
            # Check if object exists
            if expected_obj in globals():
                logger.success(f"✅ {module_name}: Successfully imported {expected_obj}")
                results.append((module_name, True, "Success"))
            else:
                logger.error(f"❌ {module_name}: Import succeeded but {expected_obj} not found")
                results.append((module_name, False, f"{expected_obj} not found"))
        except ImportError as e:
            logger.error(f"❌ {module_name}: Import failed - {str(e)}")
            results.append((module_name, False, str(e)))
        except Exception as e:
            logger.error(f"❌ {module_name}: Unexpected error - {type(e).__name__}: {str(e)}")
            results.append((module_name, False, f"{type(e).__name__}: {str(e)}"))
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("IMPORT TEST SUMMARY")
    logger.info("="*60)
    
    success_count = sum(1 for _, success, _ in results if success)
    total_count = len(results)
    
    logger.info(f"Total: {total_count}")
    logger.info(f"Success: {success_count}")
    logger.info(f"Failed: {total_count - success_count}")
    logger.info(f"Success Rate: {success_count/total_count*100:.1f}%")
    
    # Show failed imports
    if success_count < total_count:
        logger.info("\nFailed Imports:")
        for module, success, error in results:
            if not success:
                logger.info(f"  - {module}: {error}")
    
    return success_count == total_count

def check_module_structure():
    """Check the actual structure of key modules"""
    logger.info("\n" + "="*60)
    logger.info("MODULE STRUCTURE CHECK")
    logger.info("="*60)
    
    modules_to_check = [
        ("/home/graham/workspace/experiments/sparta/src/sparta", ["integrations", "handlers", "core"]),
        ("/home/graham/workspace/experiments/marker/src/marker", ["core", "cli", "processors"]),
        ("/home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts", ["__init__.py"]),
        ("/home/graham/workspace/experiments/rl_commons/src/rl_commons", ["__init__.py"]),
    ]
    
    for module_path, expected_items in modules_to_check:
        path = Path(module_path)
        if path.exists():
            logger.info(f"\n{path.name}:")
            items = sorted([item.name for item in path.iterdir() if not item.name.startswith('.')])
            for item in items[:10]:  # Show first 10 items
                logger.info(f"  - {item}")
            if len(items) > 10:
                logger.info(f"  ... and {len(items) - 10} more")
            
            # Check for expected items
            missing = [item for item in expected_items if item not in items]
            if missing:
                logger.warning(f"  Missing expected items: {missing}")
        else:
            logger.error(f"\n{module_path} does not exist!")

def main():
    """Run all tests"""
    logger.info("🔍 Testing Actual Module Imports")
    
    setup_paths()
    test_module_imports()
    check_module_structure()
    
    logger.info("\n✅ Module import test complete")

if __name__ == "__main__":
    main()