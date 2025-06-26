"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Module: test_example_generation.py
Purpose: Test code example generation for API endpoints

External Dependencies:
- pytest: https://docs.pytest.org/ - Testing framework

Example Usage:
>>> pytest tests/test_example_generation.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
from typing import Dict, List

import pytest
from loguru import logger

from api_doc_generator_interaction import (
    APIEndpoint,
    ExampleGenerator,
    DocumentationRenderer
)


class TestExampleGeneration:
    """Test code example generation"""
    
    @pytest.fixture
    def sample_endpoints(self) -> List[APIEndpoint]:
        """Create sample endpoints for testing"""
        return [
            APIEndpoint(
                path="/users",
                method="GET",
                summary="List users",
                parameters=[
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer"}
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer"}
                    }
                ]
            ),
            APIEndpoint(
                path="/users",
                method="POST",
                summary="Create user",
                request_body={
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            ),
            APIEndpoint(
                path="/users/{user_id}",
                method="GET",
                summary="Get user by ID",
                parameters=[
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ]
            ),
            APIEndpoint(
                path="/protected/data",
                method="GET",
                summary="Get protected data",
                security=[{"bearerAuth": []}]
            ),
            APIEndpoint(
                path="/users/{user_id}",
                method="PUT",
                summary="Update user",
                parameters=[
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                request_body={
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string"}
                                }
                            }
                        }
                    }
                },
                security=[{"bearerAuth": []}]
            )
        ]
    
    @pytest.fixture
    def example_generator(self) -> ExampleGenerator:
        """Create example generator instance"""
        return ExampleGenerator(base_url="https://api.example.com")
    
    def test_python_example_generation(self, example_generator: ExampleGenerator,
                                     sample_endpoints: List[APIEndpoint]):
        """Test Python code example generation"""
        # Test GET with query parameters
        get_endpoint = sample_endpoints[0]
        examples = example_generator.generate_examples(get_endpoint, ["python"])
        
        assert "python" in examples
        python_code = examples["python"]
        
        # Check basic structure
        assert "import requests" in python_code
        assert 'url = "https://api.example.com/users"' in python_code
        assert "params = {" in python_code
        assert '"page": "value"' in python_code
        assert '"limit": "value"' in python_code
        assert "response = requests.get(" in python_code
        assert "params=params" in python_code
        
        logger.info("✅ Python GET example generated")
        
        # Test POST with body
        post_endpoint = sample_endpoints[1]
        examples = example_generator.generate_examples(post_endpoint, ["python"])
        
        python_code = examples["python"]
        assert "data = {" in python_code
        assert "response = requests.post(" in python_code
        assert "json=data" in python_code
        
        logger.info("✅ Python POST example generated")
        
        # Test authenticated request
        auth_endpoint = sample_endpoints[3]
        examples = example_generator.generate_examples(auth_endpoint, ["python"])
        
        python_code = examples["python"]
        assert "headers = {" in python_code
        assert '"Authorization": "Bearer <token>"' in python_code
        assert "headers=headers" in python_code
        
        logger.info("✅ Python authenticated example generated")
    
    def test_javascript_example_generation(self, example_generator: ExampleGenerator,
                                         sample_endpoints: List[APIEndpoint]):
        """Test JavaScript code example generation"""
        # Test GET with query parameters
        get_endpoint = sample_endpoints[0]
        examples = example_generator.generate_examples(get_endpoint, ["javascript"])
        
        assert "javascript" in examples
        js_code = examples["javascript"]
        
        # Check basic structure
        assert "const url = 'https://api.example.com/users'" in js_code
        assert "const params = new URLSearchParams({" in js_code
        assert "page: 'value'" in js_code
        assert "limit: 'value'" in js_code
        assert "fetch(url + '?' + params" in js_code
        assert "method: 'GET'" in js_code
        
        logger.info("✅ JavaScript GET example generated")
        
        # Test POST with body
        post_endpoint = sample_endpoints[1]
        examples = example_generator.generate_examples(post_endpoint, ["javascript"])
        
        js_code = examples["javascript"]
        assert "const data = {" in js_code
        assert "method: 'POST'" in js_code
        assert "body: JSON.stringify(data)" in js_code
        assert "'Content-Type': 'application/json'" in js_code
        
        logger.info("✅ JavaScript POST example generated")
        
        # Test authenticated request
        auth_endpoint = sample_endpoints[3]
        examples = example_generator.generate_examples(auth_endpoint, ["javascript"])
        
        js_code = examples["javascript"]
        assert "'Authorization': 'Bearer <token>'" in js_code
        
        logger.info("✅ JavaScript authenticated example generated")
    
    def test_curl_example_generation(self, example_generator: ExampleGenerator,
                                   sample_endpoints: List[APIEndpoint]):
        """Test cURL command example generation"""
        # Test GET with query parameters
        get_endpoint = sample_endpoints[0]
        examples = example_generator.generate_examples(get_endpoint, ["curl"])
        
        assert "curl" in examples
        curl_cmd = examples["curl"]
        
        # Check basic structure
        assert 'curl -X GET "https://api.example.com/users?' in curl_cmd
        assert "page=value" in curl_cmd
        assert "limit=value" in curl_cmd
        
        logger.info("✅ cURL GET example generated")
        
        # Test POST with body
        post_endpoint = sample_endpoints[1]
        examples = example_generator.generate_examples(post_endpoint, ["curl"])
        
        curl_cmd = examples["curl"]
        assert "curl -X POST" in curl_cmd
        assert '-H "Content-Type: application/json"' in curl_cmd
        assert "-d '{" in curl_cmd
        
        logger.info("✅ cURL POST example generated")
        
        # Test authenticated request
        auth_endpoint = sample_endpoints[3]
        examples = example_generator.generate_examples(auth_endpoint, ["curl"])
        
        curl_cmd = examples["curl"]
        assert '-H "Authorization: Bearer <token>"' in curl_cmd
        
        logger.info("✅ cURL authenticated example generated")
    
    def test_multiple_language_generation(self, example_generator: ExampleGenerator,
                                        sample_endpoints: List[APIEndpoint]):
        """Test generating examples for multiple languages"""
        endpoint = sample_endpoints[4]  # PUT with auth and body
        
        # Generate for all languages
        examples = example_generator.generate_examples(endpoint)
        
        assert "python" in examples
        assert "javascript" in examples
        assert "curl" in examples
        
        # Check all have authentication
        for lang, code in examples.items():
            assert "Bearer <token>" in code, f"Missing auth in {lang} example"
        
        # Check all have request body
        assert "data = {" in examples["python"]
        assert "const data = {" in examples["javascript"]
        assert "-d '{" in examples["curl"]
        
        logger.info("✅ Multi-language example generation successful")
    
    def test_custom_base_url(self):
        """Test example generation with custom base URL"""
        custom_generator = ExampleGenerator(base_url="http://localhost:8000")
        
        endpoint = APIEndpoint(
            path="/test",
            method="GET",
            summary="Test endpoint"
        )
        
        examples = custom_generator.generate_examples(endpoint)
        
        # Check base URL in all examples
        assert 'url = "http://localhost:8000/test"' in examples["python"]
        assert "const url = 'http://localhost:8000/test'" in examples["javascript"]
        assert 'curl -X GET "http://localhost:8000/test"' in examples["curl"]
        
        logger.info("✅ Custom base URL handling validated")
    
    def test_documentation_rendering(self, sample_endpoints: List[APIEndpoint]):
        """Test documentation rendering with examples"""
        renderer = DocumentationRenderer()
        
        # Create mock spec
        spec = {
            "info": {
                "title": "Test API",
                "version": "1.0.0",
                "description": "Test API for example generation"
            },
            "servers": [{"url": "https://api.example.com"}],
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            }
        }
        
        # Generate examples
        example_gen = ExampleGenerator(base_url="https://api.example.com")
        examples = {}
        for endpoint in sample_endpoints:
            key = endpoint.path + endpoint.method
            examples[key] = example_gen.generate_examples(endpoint)
        
        # Render markdown
        markdown = renderer.render_markdown(spec, sample_endpoints, examples)
        
        # Check content
        assert "# Test API" in markdown
        assert "## Endpoints" in markdown
        assert "**Example Request:**" in markdown
        assert "```python" in markdown
        assert "import requests" in markdown
        
        logger.info("✅ Documentation rendering with examples successful")
    
    def test_html_rendering(self, sample_endpoints: List[APIEndpoint]):
        """Test HTML documentation rendering"""
        renderer = DocumentationRenderer()
        
        # Create simple markdown
        markdown = """# Test API

## Endpoints

### GET /users

Get list of users.

**Example Request:**

```python
import requests
response = requests.get("https://api.example.com/users")
```
"""
        
        # Render HTML
        html = renderer.render_html(markdown)
        
        # Check HTML structure
        assert "<!DOCTYPE html>" in html
        assert "<title>API Documentation</title>" in html
        assert "<h1>Test API</h1>" in html
        assert "<h2>Endpoints</h2>" in html
        assert "<pre>" in html
        assert "import requests" in html
        
        # Check styling
        assert "font-family:" in html
        assert "background-color:" in html
        
        logger.info("✅ HTML rendering successful")
    
    def test_error_code_documentation(self):
        """Test error code documentation generation"""
        renderer = DocumentationRenderer()
        
        # Get error codes section
        error_codes = renderer._render_error_codes()
        
        # Check content
        assert "| Code | Description |" in error_codes
        assert "| 400 | Bad Request" in error_codes
        assert "| 401 | Unauthorized" in error_codes
        assert "| 404 | Not Found" in error_codes
        assert "| 500 | Internal Server Error" in error_codes
        
        logger.info("✅ Error code documentation generated")
    
    def test_empty_parameters(self, example_generator: ExampleGenerator):
        """Test example generation with no parameters"""
        endpoint = APIEndpoint(
            path="/health",
            method="GET",
            summary="Health check",
            parameters=[]
        )
        
        examples = example_generator.generate_examples(endpoint)
        
        # Check no parameters in examples
        python_code = examples["python"]
        assert "params = {" not in python_code
        assert "response = requests.get(\n    url\n)" in python_code
        
        js_code = examples["javascript"]
        assert "const params" not in js_code
        assert "fetch(url, {" in js_code
        
        curl_code = examples["curl"]
        assert "?" not in curl_code
        assert 'curl -X GET "https://api.example.com/health"' in curl_code
        
        logger.info("✅ Empty parameters handling validated")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])