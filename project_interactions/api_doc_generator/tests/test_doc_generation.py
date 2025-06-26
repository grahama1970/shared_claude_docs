"""
Module: test_doc_generation.py
Purpose: Test documentation generation functionality

External Dependencies:
- pytest: https://docs.pytest.org/ - Testing framework
- pydantic: https://docs.pydantic.dev/ - Data validation

Example Usage:
>>> pytest tests/test_doc_generation.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from pathlib import Path
from typing import Dict, List

import pytest
from loguru import logger

from api_doc_generator_interaction import (
    APIDocGeneratorInteraction,
    APIEndpoint,
    DocumentationConfig,
    DocumentationExtractor
)


class TestDocumentationGeneration:
    """Test documentation generation capabilities"""
    
    @pytest.fixture
    def sample_fastapi_code(self, tmp_path: Path) -> Path:
        """Create sample FastAPI application code"""
        code = '''
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Sample API", version="1.0.0")

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class CreateProductRequest(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.get("/", tags=["General"])
async def root():
    """Get API information
    
    Returns basic information about the API.
    """
    return {"message": "Welcome to Sample API", "version": "1.0.0"}

@app.get("/products", response_model=List[Product], tags=["Products"])
async def get_products(skip: int = 0, limit: int = 10):
    """Get list of products
    
    Retrieve a paginated list of products from the catalog.
    """
    return []

@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product(product_id: int):
    """Get product by ID
    
    Retrieve detailed information about a specific product.
    """
    if product_id < 1:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(id=product_id, name="Sample Product", price=99.99)

@app.post("/products", response_model=Product, tags=["Products"])
async def create_product(product: CreateProductRequest):
    """Create new product
    
    Add a new product to the catalog.
    """
    return Product(id=1, name=product.name, price=product.price, description=product.description)

@app.put("/products/{product_id}", response_model=Product, tags=["Products"])
async def update_product(product_id: int, product: CreateProductRequest):
    """Update product
    
    Update an existing product's information.
    """
    return Product(id=product_id, name=product.name, price=product.price, description=product.description)

@app.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: int):
    """Delete product
    
    Remove a product from the catalog.
    """
    return {"message": f"Product {product_id} deleted"}
'''
        
        file_path = tmp_path / "sample_api.py"
        file_path.write_text(code)
        return file_path
    
    @pytest.fixture
    def sample_flask_code(self, tmp_path: Path) -> Path:
        """Create sample Flask application code"""
        code = '''
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    """Get API information"""
    return jsonify({"message": "Welcome to Flask API", "version": "1.0.0"})

@app.route('/users', methods=['GET', 'POST'])
def users():
    """Handle user operations
    
    GET: Retrieve list of users
    POST: Create new user
    """
    if request.method == 'GET':
        return jsonify({"users": []})
    else:
        return jsonify({"id": 1, "name": "New User"})

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    """Handle individual user operations"""
    if request.method == 'GET':
        return jsonify({"id": user_id, "name": "User"})
    elif request.method == 'PUT':
        return jsonify({"id": user_id, "name": "Updated User"})
    else:
        return jsonify({"message": f"User {user_id} deleted"})
'''
        
        file_path = tmp_path / "flask_api.py"
        file_path.write_text(code)
        return file_path
    
    @pytest.fixture
    def doc_generator(self) -> APIDocGeneratorInteraction:
        """Create documentation generator instance"""
        config = DocumentationConfig(
            title="Test API",
            version="1.0.0",
            description="API for testing documentation generation"
        )
        return APIDocGeneratorInteraction(config)
    
    def test_fastapi_extraction(self, sample_fastapi_code: Path):
        """Test FastAPI endpoint extraction"""
        extractor = DocumentationExtractor()
        endpoints = extractor.extract_from_fastapi(sample_fastapi_code)
        
        # Verify endpoints extracted
        assert len(endpoints) == 6, f"Expected 6 endpoints, got {len(endpoints)}"
        
        # Check endpoint details
        paths = {e.path for e in endpoints}
        assert "/" in paths, "Missing root endpoint"
        assert "/products" in paths, "Missing products endpoint"
        assert "/products/{product_id}" in paths, "Missing product detail endpoint"
        
        # Check methods
        methods = {e.method for e in endpoints}
        assert "GET" in methods, "Missing GET method"
        assert "POST" in methods, "Missing POST method"
        assert "PUT" in methods, "Missing PUT method"
        assert "DELETE" in methods, "Missing DELETE method"
        
        # Check documentation extraction
        root_endpoint = next(e for e in endpoints if e.path == "/" and e.method == "GET")
        assert "Get API information" in root_endpoint.summary
        assert "Returns basic information" in root_endpoint.description
        
        logger.info(f"✅ Extracted {len(endpoints)} FastAPI endpoints")
    
    def test_flask_extraction(self, sample_flask_code: Path):
        """Test Flask endpoint extraction"""
        extractor = DocumentationExtractor()
        endpoints = extractor.extract_from_flask(sample_flask_code)
        
        # Verify endpoints extracted
        assert len(endpoints) > 0, "No Flask endpoints extracted"
        
        # Check endpoint paths
        paths = {e.path for e in endpoints}
        assert "/" in paths, "Missing root endpoint"
        assert "/users" in paths, "Missing users endpoint"
        
        logger.info(f"✅ Extracted {len(endpoints)} Flask endpoints")
    
    def test_documentation_generation(self, doc_generator: APIDocGeneratorInteraction, 
                                    sample_fastapi_code: Path):
        """Test complete documentation generation"""
        docs = doc_generator.generate_documentation(
            sample_fastapi_code,
            framework="fastapi",
            output_formats=["openapi", "markdown", "html"]
        )
        
        # Verify all outputs generated
        assert "openapi" in docs, "OpenAPI spec not generated"
        assert "markdown" in docs, "Markdown not generated"
        assert "html" in docs, "HTML not generated"
        assert "endpoints" in docs, "Endpoints not included"
        assert "validation" in docs, "Validation results not included"
        
        # Check OpenAPI spec
        spec = docs["openapi"]
        assert spec["info"]["title"] == "Test API"
        assert spec["info"]["version"] == "1.0.0"
        assert "paths" in spec
        assert len(spec["paths"]) > 0
        
        # Check validation
        assert docs["validation"]["valid"], f"Validation failed: {docs['validation']['errors']}"
        
        # Check markdown content
        markdown = docs["markdown"]
        assert "# Test API" in markdown
        assert "## Endpoints" in markdown
        assert "GET /" in markdown
        assert "POST /products" in markdown
        
        # Check HTML content
        html = docs["html"]
        assert "<title>API Documentation</title>" in html
        assert "Test API" in html
        
        logger.info("✅ Documentation generation completed successfully")
    
    def test_postman_collection_export(self, doc_generator: APIDocGeneratorInteraction,
                                      sample_fastapi_code: Path):
        """Test Postman collection export"""
        docs = doc_generator.generate_documentation(
            sample_fastapi_code,
            framework="fastapi",
            output_formats=["openapi", "postman"]
        )
        
        assert "postman" in docs, "Postman collection not generated"
        
        collection = docs["postman"]
        assert collection["info"]["name"] == "Test API"
        assert "item" in collection
        assert len(collection["item"]) > 0
        
        # Check request structure
        first_item = collection["item"][0]
        assert "name" in first_item
        assert "item" in first_item  # Folder structure
        
        logger.info("✅ Postman collection export successful")
    
    def test_multi_framework_support(self, doc_generator: APIDocGeneratorInteraction,
                                    sample_fastapi_code: Path, sample_flask_code: Path):
        """Test support for multiple frameworks"""
        # Test FastAPI
        fastapi_docs = doc_generator.generate_documentation(
            sample_fastapi_code,
            framework="fastapi"
        )
        assert len(fastapi_docs["endpoints"]) > 0
        
        # Test Flask
        flask_docs = doc_generator.generate_documentation(
            sample_flask_code,
            framework="flask"
        )
        assert len(flask_docs["endpoints"]) > 0
        
        # Test unsupported framework
        with pytest.raises(ValueError, match="Unsupported framework"):
            doc_generator.generate_documentation(
                sample_fastapi_code,
                framework="express"
            )
        
        logger.info("✅ Multi-framework support validated")
    
    def test_documentation_update(self, doc_generator: APIDocGeneratorInteraction,
                                 sample_fastapi_code: Path):
        """Test documentation update with change detection"""
        # Generate initial documentation
        initial_docs = doc_generator.generate_documentation(
            sample_fastapi_code,
            framework="fastapi"
        )
        
        # Update documentation (simulating changes)
        result = doc_generator.update_documentation(
            sample_fastapi_code,
            initial_docs["openapi"],
            framework="fastapi"
        )
        
        assert "openapi" in result
        assert "changes" in result
        assert "change_count" in result
        
        # Check version increment
        assert result["openapi"]["info"]["version"] != initial_docs["openapi"]["info"]["version"]
        
        logger.info(f"✅ Documentation update detected {result['change_count']} changes")
    
    def test_sdk_hints_generation(self, doc_generator: APIDocGeneratorInteraction,
                                 sample_fastapi_code: Path):
        """Test SDK generation hints"""
        docs = doc_generator.generate_documentation(
            sample_fastapi_code,
            framework="fastapi"
        )
        
        # Test Python SDK hints
        python_hints = doc_generator.generate_sdk_hints(docs["openapi"], "python")
        assert "openapi-python-client" in python_hints
        assert "Generated SDK usage" in python_hints
        
        # Test TypeScript SDK hints
        ts_hints = doc_generator.generate_sdk_hints(docs["openapi"], "typescript")
        assert "openapi-typescript-codegen" in ts_hints
        
        # Test Go SDK hints
        go_hints = doc_generator.generate_sdk_hints(docs["openapi"], "go")
        assert "oapi-codegen" in go_hints
        
        logger.info("✅ SDK hints generation successful")
    
    def test_error_handling(self, doc_generator: APIDocGeneratorInteraction,
                           tmp_path: Path):
        """Test error handling"""
        # Test with non-existent file
        non_existent = tmp_path / "non_existent.py"
        docs = doc_generator.generate_documentation(
            non_existent,
            framework="fastapi"
        )
        assert len(docs["endpoints"]) == 0
        
        # Test with invalid Python code
        invalid_code = tmp_path / "invalid.py"
        invalid_code.write_text("This is not valid Python code {{{")
        docs = doc_generator.generate_documentation(
            invalid_code,
            framework="fastapi"
        )
        assert len(docs["endpoints"]) == 0
        
        logger.info("✅ Error handling validated")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])