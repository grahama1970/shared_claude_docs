#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: add_request_handler_template.py
Description: Template for adding request handling interface to Granger modules

External Dependencies:
- None

Sample Input:
>>> handler = RequestHandler()
>>> result = handler.handle_request({'source': 'granger_hub', 'auth': 'token123', 'command': 'test'})

Expected Output:
>>> print(result)
{'status': 'success', 'data': 'Request handled'}
"""

from typing import Dict, Any, Optional
from functools import wraps
import hashlib
import time
from loguru import logger


class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass


class RequestHandler:
    """Handles inter-module requests with authentication"""
    
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.valid_tokens = set()
        self.request_log = []
        
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming request with authentication and validation
        
        Args:
            request: Dictionary containing:
                - source: Source module name
                - auth: Authentication token
                - command: Command to execute
                - data: Optional command data
                
        Returns:
            Response dictionary with status and data
        """
        try:
            # Log request
            self._log_request(request)
            
            # Validate request structure
            self._validate_request_structure(request)
            
            # Authenticate
            if not self._authenticate(request):
                raise AuthenticationError("Invalid authentication token")
                
            # Check authorization
            if not self._authorize(request):
                raise AuthenticationError("Unauthorized for this operation")
                
            # Process command
            response = self._process_command(request)
            
            # Log response
            self._log_response(response)
            
            return response
            
        except AuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'code': 401
            }
        except Exception as e:
            logger.error(f"Request handling failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'code': 500
            }
            
    def _validate_request_structure(self, request: Dict[str, Any]):
        """Validate request has required fields"""
        required_fields = ['source', 'auth', 'command']
        
        for field in required_fields:
            if field not in request:
                raise ValueError(f"Missing required field: {field}")
                
    def _authenticate(self, request: Dict[str, Any]) -> bool:
        """Authenticate the request"""
        auth_token = request.get('auth', '')
        
        # For testing, accept tokens that match pattern
        # In production, this would check against a secure token store
        if auth_token.startswith('granger_') and len(auth_token) > 10:
            return True
            
        # Check if it's a valid pre-registered token
        return auth_token in self.valid_tokens
        
    def _authorize(self, request: Dict[str, Any]) -> bool:
        """Check if source is authorized for the command"""
        source = request.get('source', '')
        command = request.get('command', '')
        
        # Define authorization rules
        auth_rules = {
            'granger_hub': ['*'],  # Hub can do anything
            'test_reporter': ['get_data', 'submit_test'],
            'marker': ['process_document', 'get_status'],
            'sparta': ['analyze_cve', 'get_vulnerabilities'],
            'arangodb': ['query', 'store', 'update', 'delete'],
        }
        
        # Check if source has permission
        allowed_commands = auth_rules.get(source, [])
        
        if '*' in allowed_commands:
            return True
            
        return command in allowed_commands
        
    def _process_command(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process the actual command"""
        command = request.get('command', '')
        data = request.get('data', {})
        
        # Command handlers
        handlers = {
            'get_all_data': self._handle_get_all_data,
            'get_status': self._handle_get_status,
            'process': self._handle_process,
            'test': self._handle_test,
        }
        
        handler = handlers.get(command, self._handle_unknown_command)
        return handler(data)
        
    def _handle_get_all_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_all_data command"""
        # This should be overridden in actual implementations
        return {
            'status': 'success',
            'data': {
                'module': self.module_name,
                'records': 0,
                'message': 'Override this method in module implementation'
            }
        }
        
    def _handle_get_status(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle status check"""
        return {
            'status': 'success',
            'data': {
                'module': self.module_name,
                'healthy': True,
                'uptime': time.time(),
                'requests_handled': len(self.request_log)
            }
        }
        
    def _handle_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generic process command"""
        return {
            'status': 'success',
            'data': {
                'processed': True,
                'input': data
            }
        }
        
    def _handle_test(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle test command"""
        return {
            'status': 'success',
            'data': 'Test successful'
        }
        
    def _handle_unknown_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle unknown commands"""
        return {
            'status': 'error',
            'error': 'Unknown command',
            'code': 400
        }
        
    def _log_request(self, request: Dict[str, Any]):
        """Log incoming request"""
        self.request_log.append({
            'timestamp': time.time(),
            'type': 'request',
            'data': request
        })
        
    def _log_response(self, response: Dict[str, Any]):
        """Log outgoing response"""
        self.request_log.append({
            'timestamp': time.time(),
            'type': 'response',
            'data': response
        })
        
    def register_token(self, token: str):
        """Register a valid authentication token"""
        self.valid_tokens.add(token)
        
    def revoke_token(self, token: str):
        """Revoke an authentication token"""
        self.valid_tokens.discard(token)


def secure_module(module_name: str):
    """
    Decorator to add request handling to a module
    
    Usage:
        @secure_module("my_module")
        class MyModule:
            def process(self, data):
                return "processed"
    """
    def decorator(cls):
        # Add request handler
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.request_handler = RequestHandler(module_name)
            self.handle_request = self.request_handler.handle_request
            
        cls.__init__ = new_init
        return cls
        
    return decorator


# Example usage
if __name__ == "__main__":
    # Create handler
    handler = RequestHandler("example_module")
    
    # Test valid request
    valid_request = {
        'source': 'granger_hub',
        'auth': 'granger_hub_token_12345',
        'command': 'get_status'
    }
    
    result = handler.handle_request(valid_request)
    print(f"✅ Valid request result: {result}")
    
    # Test invalid auth
    invalid_request = {
        'source': 'unknown',
        'auth': 'bad_token',
        'command': 'get_all_data'
    }
    
    result = handler.handle_request(invalid_request)
    print(f"❌ Invalid auth result: {result}")
    
    # Test missing fields
    bad_request = {
        'source': 'granger_hub',
        # Missing auth field
        'command': 'test'
    }
    
    result = handler.handle_request(bad_request)
    print(f"❌ Bad request result: {result}")