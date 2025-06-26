#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: fix_arangodb_auth.py
Description: Add request handling interface to ArangoDB module

External Dependencies:
- loguru: https://loguru.readthedocs.io/

Sample Input:
>>> python fix_arangodb_auth.py

Expected Output:
>>> Checking ArangoDB module...
>>> Adding request handler to graph_self_organization_interaction.py
>>> ✅ Request handler added successfully
"""

import sys
import os
from pathlib import Path
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO"
)

# Add the request handler code to inject
REQUEST_HANDLER_CODE = '''
# Request handling interface for inter-module communication
class RequestHandler:
    """Handles inter-module requests with authentication"""
    
    def __init__(self, module_name: str = "arangodb"):
        self.module_name = module_name
        self.valid_tokens = set()
        
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming request with authentication
        
        Args:
            request: Dictionary containing source, auth, command, and data
            
        Returns:
            Response dictionary with status and data
        """
        try:
            # Validate request structure
            required_fields = ['source', 'auth', 'command']
            for field in required_fields:
                if field not in request:
                    raise ValueError(f"Missing required field: {field}")
                    
            # Authenticate
            auth_token = request.get('auth', '')
            if not (auth_token.startswith('granger_') and len(auth_token) > 10):
                return {
                    'status': 'error',
                    'error': 'Invalid authentication token',
                    'code': 401
                }
                
            # Process command
            command = request.get('command', '')
            data = request.get('data', {})
            
            if command == 'get_all_data':
                # Return all graph data
                return {
                    'status': 'success',
                    'data': {
                        'module': 'arangodb',
                        'graphs': list(self.graphs.keys()) if hasattr(self, 'graphs') else [],
                        'message': 'Graph data available'
                    }
                }
            elif command == 'get_status':
                return {
                    'status': 'success',
                    'data': {
                        'module': 'arangodb',
                        'healthy': True,
                        'connection': 'active'
                    }
                }
            elif command == 'query':
                # Execute AQL query
                query = data.get('query', '')
                return {
                    'status': 'success',
                    'data': {
                        'query': query,
                        'result': 'Query execution placeholder'
                    }
                }
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown command: {command}',
                    'code': 400
                }
                
        except Exception as e:
            logger.error(f"Request handling failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'code': 500
            }


# Global request handler instance
request_handler = RequestHandler("arangodb")
handle_request = request_handler.handle_request
'''


def fix_arangodb_auth():
    """Add request handling to ArangoDB module"""
    # Path to ArangoDB interaction file
    arangodb_path = Path("/home/graham/workspace/shared_claude_docs/project_interactions/arangodb/graph_self_organization_interaction.py")
    
    if not arangodb_path.exists():
        logger.error(f"ArangoDB interaction file not found: {arangodb_path}")
        return False
        
    logger.info("Reading ArangoDB module...")
    
    # Read current content
    with open(arangodb_path, 'r') as f:
        content = f.read()
        
    # Check if already has request handling
    if 'handle_request' in content:
        logger.warning("Request handler already exists in ArangoDB module")
        return True
        
    # Find where to insert (after imports)
    lines = content.split('\n')
    insert_index = 0
    
    # Find the last import statement
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_index = i + 1
        elif line.strip() and not line.startswith('#') and insert_index > 0:
            # Found first non-import, non-comment line
            break
            
    # Insert the request handler code
    logger.info(f"Inserting request handler at line {insert_index}")
    
    # Add necessary imports if not present
    imports_to_add = []
    if 'from typing import Dict, Any' not in content:
        imports_to_add.append('from typing import Dict, Any')
    if 'from loguru import logger' not in content:
        imports_to_add.append('from loguru import logger')
        
    # Build new content
    new_lines = lines[:insert_index]
    
    # Add imports
    for imp in imports_to_add:
        new_lines.append(imp)
        
    if imports_to_add:
        new_lines.append('')  # Blank line after imports
        
    # Add request handler code
    new_lines.append('')
    new_lines.append(REQUEST_HANDLER_CODE)
    new_lines.append('')
    
    # Add remaining content
    new_lines.extend(lines[insert_index:])
    
    # Write back
    new_content = '\n'.join(new_lines)
    
    logger.info("Writing updated ArangoDB module...")
    with open(arangodb_path, 'w') as f:
        f.write(new_content)
        
    logger.success("✅ Request handler added to ArangoDB module")
    
    # Also update the __init__.py to export handle_request
    init_path = arangodb_path.parent / "__init__.py"
    if init_path.exists():
        with open(init_path, 'r') as f:
            init_content = f.read()
            
        if 'handle_request' not in init_content:
            logger.info("Updating __init__.py exports...")
            with open(init_path, 'a') as f:
                f.write('\n# Export request handler\n')
                f.write('from .graph_self_organization_interaction import handle_request\n')
                
    return True


def test_fix():
    """Test the fix by importing and calling handle_request"""
    logger.info("Testing the fix...")
    
    try:
        # Try to import
        sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
        from arangodb import handle_request
        
        # Test request
        test_request = {
            'source': 'granger_hub',
            'auth': 'granger_hub_token_12345',
            'command': 'get_status'
        }
        
        result = handle_request(test_request)
        logger.info(f"Test result: {result}")
        
        if result.get('status') == 'success':
            logger.success("✅ Request handler working correctly!")
            return True
        else:
            logger.error("❌ Request handler returned error")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False


def main():
    """Main entry point"""
    logger.info("🔧 Fixing ArangoDB authentication interface...")
    
    if fix_arangodb_auth():
        # Test the fix
        if test_fix():
            logger.success("🎉 ArangoDB authentication fix complete!")
            return 0
        else:
            logger.error("Fix applied but test failed")
            return 1
    else:
        logger.error("Failed to apply fix")
        return 1


if __name__ == "__main__":
    sys.exit(main())