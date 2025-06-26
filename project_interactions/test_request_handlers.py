#!/usr/bin/env python3
"""
Module: test_request_handlers.py  
Description: Test request handlers for all modules

External Dependencies:
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> python test_request_handlers.py

Expected Output:
>>> Testing marker handler... ✅ Success
>>> Testing sparta handler... ✅ Success  
>>> Testing arangodb handler... ✅ Success
"""

import sys
from pathlib import Path
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)


def test_module_handler(module_name: str):
    """Test a module's request handler"""
    try:
        # Import the handler
        if module_name == "marker":
            from marker import handle_request
        elif module_name == "sparta":
            from sparta import handle_request
        elif module_name == "arangodb":
            from arangodb import handle_request
        else:
            logger.error(f"Unknown module: {module_name}")
            return False
            
        # Test request
        test_request = {
            'source': 'granger_hub',
            'auth': 'granger_hub_token_12345',
            'command': 'get_status'
        }
        
        result = handle_request(test_request)
        
        if result.get('status') == 'success':
            logger.success(f"✅ {module_name} handler test passed")
            logger.info(f"Response: {result.get('data', {})}")
            return True
        else:
            logger.error(f"❌ {module_name} handler test failed: {result}")
            return False
            
    except ImportError as e:
        logger.error(f"❌ Failed to import {module_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to test {module_name}: {e}")
        return False


def main():
    """Main entry point"""
    # Add project to path
    sys.path.insert(0, str(Path(__file__).parent))
    
    modules_to_test = ["marker", "sparta", "arangodb"]
    success_count = 0
    
    for module_name in modules_to_test:
        logger.info(f"Testing {module_name} handler...")
        if test_module_handler(module_name):
            success_count += 1
            
    logger.info(f"\n🎯 {success_count}/{len(modules_to_test)} modules passed")
    
    if success_count == len(modules_to_test):
        logger.success("🎉 All request handlers working!")
        return 0
    else:
        logger.warning(f"⚠️ Only {success_count} modules passed")
        return 1


if __name__ == "__main__":
    sys.exit(main())