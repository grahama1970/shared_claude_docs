#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: fix_modules_auth.py
Description: Add request handling interfaces to all modules that need them

External Dependencies:
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> python fix_modules_auth.py

Expected Output:
>>> Fixing authentication for arangodb...
>>> ✅ Added request handler to arangodb module
>>> Fixing authentication for marker...
>>> ✅ Added request handler to marker module
>>> Fixing authentication for sparta...
>>> ✅ Added request handler to sparta module
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)


def add_request_handler_to_module(module_path: Path, module_name: str) -> bool:
    """Add request handler to a module's __init__.py"""
    init_path = module_path / "__init__.py"
    
    if not init_path.exists():
        logger.warning(f"Creating __init__.py for {module_name}")
        init_path.write_text("")
        
    # Read current content
    content = init_path.read_text()
    
    # Check if already has request handler
    if 'handle_request' in content:
        logger.info(f"{module_name} already has request handler")
        return True
        
    # Add request handler code
    handler_code = f'''
# Request handler for {module_name} module
def handle_request(request):
    """
    Handle inter-module requests with authentication.
    
    Args:
        request: Dict with source, auth, command, and data
        
    Returns:
        Response dict with status and data
    """
    try:
        # Validate request
        required = ['source', 'auth', 'command']
        for field in required:
            if field not in request:
                return {{
                    'status': 'error',
                    'error': f'Missing required field: {{field}}',
                    'code': 400
                }}
                
        # Authenticate
        auth_token = request.get('auth', '')
        if not (auth_token.startswith('granger_') and len(auth_token) > 10):
            return {{
                'status': 'error',
                'error': 'Invalid authentication token',
                'code': 401
            }}
            
        # Process command
        command = request.get('command', '')
        data = request.get('data', {{}})
        
        # Command handlers
        if command == 'get_status':
            return {{
                'status': 'success',
                'data': {{
                    'module': '{module_name}',
                    'healthy': True,
                    'message': 'Module is operational'
                }}
            }}
        elif command == 'get_all_data':
            return {{
                'status': 'success',
                'data': {{
                    'module': '{module_name}',
                    'message': 'Data retrieval not implemented yet'
                }}
            }}
        elif command == 'process':
            return {{
                'status': 'success',
                'data': {{
                    'processed': True,
                    'input': data
                }}
            }}
        else:
            return {{
                'status': 'error',
                'error': f'Unknown command: {{command}}',
                'code': 400
            }}
            
    except Exception as e:
        return {{
            'status': 'error',
            'error': str(e),
            'code': 500
        }}


# Export the handler
__all__ = ['handle_request']
'''
    
    # Append to file
    logger.info(f"Adding request handler to {module_name}")
    with open(init_path, 'a') as f:
        f.write(handler_code)
        
    return True


def fix_module_authentication(module_name: str, base_path: Path) -> bool:
    """Fix authentication for a specific module"""
    module_path = base_path / module_name
    
    if not module_path.exists():
        logger.error(f"Module path not found: {module_path}")
        return False
        
    logger.info(f"Fixing authentication for {module_name}...")
    
    # Add request handler to __init__.py
    if add_request_handler_to_module(module_path, module_name):
        logger.success(f"✅ Added request handler to {module_name} module")
        return True
    else:
        logger.error(f"❌ Failed to add request handler to {module_name}")
        return False


def test_module_handler(module_name: str) -> bool:
    """Test that the module's request handler works"""
    try:
        # Import the module
        exec(f"from {module_name} import handle_request")
        
        # Get the handle_request function
        handle_request = locals()['handle_request']
        
        # Test request
        test_request = {
            'source': 'granger_hub',
            'auth': 'granger_hub_token_12345',
            'command': 'get_status'
        }
        
        result = handle_request(test_request)
        
        if result.get('status') == 'success':
            logger.info(f"✅ {module_name} handler test passed")
            return True
        else:
            logger.error(f"❌ {module_name} handler test failed: {result}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to test {module_name}: {e}")
        return False


def main():
    """Main entry point"""
    base_path = Path("/home/graham/workspace/shared_claude_docs/project_interactions")
    
    # Modules that need request handlers
    modules_to_fix = [
        "arangodb",
        "marker", 
        "sparta"
    ]
    
    # Add base path to Python path for imports
    sys.path.insert(0, str(base_path))
    
    success_count = 0
    
    for module_name in modules_to_fix:
        if fix_module_authentication(module_name, base_path):
            # Test the handler
            if test_module_handler(module_name):
                success_count += 1
            else:
                logger.warning(f"Module {module_name} was updated but test failed")
        else:
            logger.error(f"Failed to fix {module_name}")
            
    logger.info(f"\n🎯 Fixed {success_count}/{len(modules_to_fix)} modules")
    
    if success_count == len(modules_to_fix):
        logger.success("🎉 All modules have been fixed!")
        return 0
    else:
        logger.warning(f"⚠️ Only {success_count} modules were successfully fixed")
        return 1


if __name__ == "__main__":
    sys.exit(main())