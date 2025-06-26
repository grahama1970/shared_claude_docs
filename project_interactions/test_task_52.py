#!/usr/bin/env python3
"""
Test Task 52: Verify API Documentation Generator implementation

This script validates that the API Documentation Generator properly implements
documentation generation capabilities with multi-framework support.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from project_interactions.api_doc_generator.api_doc_generator_interaction import (
    APIDocGeneratorInteraction,
    DocumentationConfig,
    DocumentationExtractor,
    OpenAPIGenerator,
    ExampleGenerator,
    DocumentationRenderer,
    APIEndpoint
)


def test_module_structure() -> Tuple[bool, str]:
    """Test if all required modules and classes exist"""
    print("\n1. Testing module structure...")
    
    required_classes = [
        'APIDocGeneratorInteraction',
        'DocumentationExtractor',
        'OpenAPIGenerator',
        'ExampleGenerator',
        'DocumentationRenderer',
        'APIEndpoint',
        'DocumentationConfig'
    ]
    
    for class_name in required_classes:
        if class_name not in globals():
            return False, f"Missing required class: {class_name}"
    
    return True, "✅ All required classes found"


def test_documentation_extraction() -> Tuple[bool, str]:
    """Test documentation extraction from source code"""
    print("\n2. Testing documentation extraction...")
    
    # Create test FastAPI code
    test_code = '''
from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
async def test_endpoint():
    """Test endpoint for validation"""
    return {"status": "ok"}

@app.post("/items")
async def create_item(name: str):
    """Create a new item"""
    return {"name": name}
'''
    
    # Save test code
    test_file = Path("/tmp/test_fastapi.py")
    test_file.write_text(test_code)
    
    try:
        # Extract endpoints
        extractor = DocumentationExtractor()
        endpoints = extractor.extract_from_fastapi(test_file)
        
        if len(endpoints) != 2:
            return False, f"Expected 2 endpoints, got {len(endpoints)}"
        
        # Check endpoint details
        paths = [e.path for e in endpoints]
        if "/test" not in paths or "/items" not in paths:
            return False, f"Missing expected endpoints: {paths}"
        
        # Check methods
        methods = {e.method for e in endpoints}
        if "GET" not in methods or "POST" not in methods:
            return False, f"Missing expected methods: {methods}"
        
        # Check documentation
        test_endpoint = next(e for e in endpoints if e.path == "/test")
        if "Test endpoint" not in test_endpoint.summary:
            return False, "Documentation not extracted correctly"
        
        return True, "✅ Documentation extraction working"
    
    except Exception as e:
        return False, f"❌ Extraction failed: {str(e)}"
    
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def test_openapi_generation() -> Tuple[bool, str]:
    """Test OpenAPI specification generation"""
    print("\n3. Testing OpenAPI specification generation...")
    
    try:
        # Create sample endpoints
        endpoints = [
            APIEndpoint(
                path="/api/v1/users",
                method="GET",
                summary="List all users",
                description="Returns a paginated list of users",
                parameters=[
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "default": 1}
                    }
                ],
                responses={
                    "200": {
                        "description": "List of users",
                        "content": {
                            "application/json": {
                                "schema": {"type": "array"}
                            }
                        }
                    }
                },
                tags=["Users"]
            ),
            APIEndpoint(
                path="/api/v1/users",
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
                },
                responses={
                    "201": {"description": "User created"},
                    "400": {"description": "Invalid input"}
                },
                tags=["Users"]
            )
        ]
        
        # Generate OpenAPI spec
        config = DocumentationConfig(
            title="Test API",
            version="1.0.0",
            description="API for testing"
        )
        generator = OpenAPIGenerator(config)
        spec = generator.generate_spec(endpoints)
        
        # Validate spec structure
        if spec["openapi"] != "3.0.3":
            return False, f"Wrong OpenAPI version: {spec['openapi']}"
        
        if spec["info"]["title"] != "Test API":
            return False, "Wrong API title"
        
        if "/api/v1/users" not in spec["paths"]:
            return False, "Missing API path"
        
        # Check methods
        users_path = spec["paths"]["/api/v1/users"]
        if "get" not in users_path or "post" not in users_path:
            return False, "Missing HTTP methods"
        
        # Validate spec
        is_valid, errors = generator.validate_spec(spec)
        if not is_valid:
            return False, f"Invalid spec: {errors}"
        
        return True, "✅ OpenAPI generation working"
    
    except Exception as e:
        return False, f"❌ OpenAPI generation failed: {str(e)}"


def test_example_generation() -> Tuple[bool, str]:
    """Test code example generation"""
    print("\n4. Testing code example generation...")
    
    try:
        # Create test endpoint
        endpoint = APIEndpoint(
            path="/api/v1/data",
            method="POST",
            summary="Submit data",
            parameters=[
                {
                    "name": "format",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"}
                }
            ],
            request_body={
                "required": True,
                "content": {
                    "application/json": {
                        "schema": {"type": "object"}
                    }
                }
            },
            security=[{"bearerAuth": []}]
        )
        
        # Generate examples
        generator = ExampleGenerator(base_url="https://api.example.com")
        examples = generator.generate_examples(endpoint)
        
        # Check all languages generated
        required_langs = ["python", "javascript", "curl"]
        for lang in required_langs:
            if lang not in examples:
                return False, f"Missing {lang} example"
        
        # Check Python example
        python_code = examples["python"]
        if "import requests" not in python_code:
            return False, "Python example missing imports"
        if "https://api.example.com/api/v1/data" not in python_code:
            return False, "Python example missing URL"
        if "Bearer <token>" not in python_code:
            return False, "Python example missing authentication"
        if "requests.post" not in python_code:
            return False, "Python example using wrong method"
        
        # Check JavaScript example
        js_code = examples["javascript"]
        if "fetch(" not in js_code:
            return False, "JavaScript example missing fetch"
        if "method: 'POST'" not in js_code:
            return False, "JavaScript example missing method"
        if "Authorization" not in js_code:
            return False, "JavaScript example missing auth header"
        
        # Check cURL example
        curl_code = examples["curl"]
        if "curl -X POST" not in curl_code:
            return False, "cURL example missing command"
        if "-H \"Authorization: Bearer <token>\"" not in curl_code:
            return False, "cURL example missing auth header"
        
        return True, "✅ Example generation working"
    
    except Exception as e:
        return False, f"❌ Example generation failed: {str(e)}"


def test_full_documentation_generation() -> Tuple[bool, str]:
    """Test complete documentation generation workflow"""
    print("\n5. Testing full documentation generation...")
    
    # Create test API code
    test_code = '''
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Demo API", version="2.0.0", description="Demo API for testing")

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True

@app.get("/")
def read_root():
    """Get API status
    
    Returns the current API status and version information.
    """
    return {"status": "running", "version": "2.0.0"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """Get item by ID
    
    Retrieves a specific item by its ID with optional query filter.
    """
    if item_id < 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    """Create new item
    
    Creates a new item in the inventory.
    """
    return {"name": item.name, "price": item.price, "is_available": item.is_available}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """Update existing item
    
    Updates an existing item's information.
    """
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """Delete item
    
    Removes an item from the inventory.
    """
    return {"message": f"Item {item_id} deleted"}
'''
    
    # Save test code
    test_file = Path("/tmp/demo_api.py")
    test_file.write_text(test_code)
    
    try:
        # Generate documentation
        config = DocumentationConfig(
            title="Demo API",
            version="2.0.0",
            description="Demonstration API",
            base_url="https://demo.api.com",
            contact={"name": "API Support", "email": "support@demo.com"},
            license={"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
        )
        
        generator = APIDocGeneratorInteraction(config)
        docs = generator.generate_documentation(
            test_file,
            framework="fastapi",
            output_formats=["openapi", "markdown", "html", "postman"]
        )
        
        # Check all outputs generated
        required_outputs = ["openapi", "markdown", "html", "postman", "endpoints", "validation"]
        for output in required_outputs:
            if output not in docs:
                return False, f"Missing output: {output}"
        
        # Check endpoint count
        if len(docs["endpoints"]) != 5:
            return False, f"Expected 5 endpoints, got {len(docs['endpoints'])}"
        
        # Check OpenAPI spec
        spec = docs["openapi"]
        if spec["info"]["title"] != "Demo API":
            return False, "Wrong API title in spec"
        if len(spec["paths"]) != 3:  # /, /items/{item_id}, /items/
            return False, f"Expected 3 paths, got {len(spec['paths'])}"
        
        # Check markdown content
        markdown = docs["markdown"]
        if "# Demo API" not in markdown:
            return False, "Markdown missing title"
        if "## Endpoints" not in markdown:
            return False, "Markdown missing endpoints section"
        if "GET /" not in markdown:
            return False, "Markdown missing root endpoint"
        if "**Example Request:**" not in markdown:
            return False, "Markdown missing examples"
        
        # Check HTML content
        html = docs["html"]
        if "<title>API Documentation</title>" not in html:
            return False, "HTML missing title"
        if "Demo API" not in html:
            return False, "HTML missing API name"
        
        # Check Postman collection
        postman = docs["postman"]
        if postman["info"]["name"] != "Demo API":
            return False, "Wrong Postman collection name"
        if len(postman["item"]) == 0:
            return False, "Empty Postman collection"
        
        # Check validation
        if not docs["validation"]["valid"]:
            return False, f"Validation failed: {docs['validation']['errors']}"
        
        # Test update functionality
        print("   Testing documentation update...")
        updated_docs = generator.update_documentation(
            test_file,
            docs["openapi"],
            framework="fastapi"
        )
        
        if "changes" not in updated_docs:
            return False, "Update missing changes"
        if updated_docs["openapi"]["info"]["version"] == "2.0.0":
            return False, "Version not incremented"
        
        # Test SDK hints
        sdk_hints = generator.generate_sdk_hints(docs["openapi"], "python")
        if "openapi-python-client" not in sdk_hints:
            return False, "SDK hints missing generator info"
        
        return True, "✅ Full documentation generation working"
    
    except Exception as e:
        return False, f"❌ Full generation failed: {str(e)}"
    
    finally:
        # Cleanup
        if test_file.exists():
            test_file.unlink()


def test_multi_framework_support() -> Tuple[bool, str]:
    """Test support for multiple frameworks"""
    print("\n6. Testing multi-framework support...")
    
    # Test Flask code
    flask_code = '''
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/api/data', methods=['GET', 'POST'])
def data_endpoint():
    """Data management endpoint
    
    GET: Retrieve data
    POST: Submit new data
    """
    if request.method == 'GET':
        return jsonify({"data": []})
    return jsonify({"message": "Data received"})
'''
    
    flask_file = Path("/tmp/flask_test.py")
    flask_file.write_text(flask_code)
    
    try:
        # Test Flask extraction
        extractor = DocumentationExtractor()
        flask_endpoints = extractor.extract_from_flask(flask_file)
        
        if len(flask_endpoints) == 0:
            return False, "No Flask endpoints extracted"
        
        # Check Flask endpoints
        flask_paths = [e.path for e in flask_endpoints]
        if "/api/health" not in flask_paths:
            return False, "Missing Flask health endpoint"
        
        # Test Django URL patterns
        django_urls = '''
from django.urls import path
from . import views

urlpatterns = [
    path('api/users/', UserListView.as_view()),
    path('api/users/<int:pk>/', UserDetailView.as_view()),
    path('api/products/', ProductViewSet.as_view()),
]
'''
        
        django_file = Path("/tmp/django_urls.py")
        django_file.write_text(django_urls)
        
        # Test Django extraction
        django_endpoints = extractor.extract_from_django(django_file)
        
        if len(django_endpoints) != 3:
            return False, f"Expected 3 Django endpoints, got {len(django_endpoints)}"
        
        return True, "✅ Multi-framework support working"
    
    except Exception as e:
        return False, f"❌ Multi-framework test failed: {str(e)}"
    
    finally:
        # Cleanup
        for f in [flask_file, django_file]:
            if f.exists():
                f.unlink()


def test_error_handling() -> Tuple[bool, str]:
    """Test error handling capabilities"""
    print("\n7. Testing error handling...")
    
    try:
        generator = APIDocGeneratorInteraction()
        
        # Test with non-existent file
        non_existent = Path("/tmp/does_not_exist.py")
        docs = generator.generate_documentation(
            non_existent,
            framework="fastapi"
        )
        
        if len(docs["endpoints"]) != 0:
            return False, "Should handle non-existent file gracefully"
        
        # Test with invalid Python code
        invalid_file = Path("/tmp/invalid_python.py")
        invalid_file.write_text("This is not valid Python {{{ code")
        
        docs = generator.generate_documentation(
            invalid_file,
            framework="fastapi"
        )
        
        if len(docs["endpoints"]) != 0:
            return False, "Should handle invalid Python gracefully"
        
        # Test with unsupported framework
        try:
            generator.generate_documentation(
                invalid_file,
                framework="unsupported_framework"
            )
            return False, "Should raise error for unsupported framework"
        except ValueError:
            pass  # Expected
        
        return True, "✅ Error handling working"
    
    except Exception as e:
        return False, f"❌ Error handling test failed: {str(e)}"
    
    finally:
        # Cleanup
        if invalid_file.exists():
            invalid_file.unlink()


def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing Task 52: API Documentation Generator")
    print("=" * 60)
    
    tests = [
        test_module_structure,
        test_documentation_extraction,
        test_openapi_generation,
        test_example_generation,
        test_full_documentation_generation,
        test_multi_framework_support,
        test_error_handling
    ]
    
    all_passed = True
    results = []
    
    for test in tests:
        passed, message = test()
        results.append((test.__name__, passed, message))
        if not passed:
            all_passed = False
        print(f"   {message}")
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for test_name, passed, message in results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:<40} {status}")
    
    if all_passed:
        print("\n✅ All tests passed! API Documentation Generator is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    # sys.exit() removed)