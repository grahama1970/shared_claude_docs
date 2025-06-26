"""
Module: test_openapi_spec.py
Purpose: Test OpenAPI specification generation and validation

External Dependencies:
- pytest: https://docs.pytest.org/ - Testing framework
- jsonschema: https://python-jsonschema.readthedocs.io/ - JSON schema validation

Example Usage:
>>> pytest tests/test_openapi_spec.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



from typing import Dict, List

import pytest
from loguru import logger

from api_doc_generator_interaction import (
    APIEndpoint,
    DocumentationConfig,
    OpenAPIGenerator
)


class TestOpenAPISpecification:
    """Test OpenAPI specification generation"""
    
    @pytest.fixture
    def sample_endpoints(self) -> List[APIEndpoint]:
        """Create sample API endpoints"""
        return [
            APIEndpoint(
                path="/",
                method="GET",
                summary="Get API info",
                description="Returns API information",
                responses={
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    }
                },
                tags=["General"]
            ),
            APIEndpoint(
                path="/users",
                method="GET",
                summary="List users",
                description="Get paginated list of users",
                parameters=[
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "default": 1}
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "default": 10}
                    }
                ],
                responses={
                    "200": {
                        "description": "List of users",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "users": {"type": "array"},
                                        "total": {"type": "integer"}
                                    }
                                }
                            }
                        }
                    }
                },
                tags=["Users"]
            ),
            APIEndpoint(
                path="/users",
                method="POST",
                summary="Create user",
                description="Create a new user",
                request_body={
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "email": {"type": "string", "format": "email"}
                                },
                                "required": ["name", "email"]
                            }
                        }
                    }
                },
                responses={
                    "201": {
                        "description": "User created",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    }
                },
                tags=["Users"]
            ),
            APIEndpoint(
                path="/users/{user_id}",
                method="GET",
                summary="Get user",
                description="Get user by ID",
                parameters=[
                    {
                        "name": "user_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"}
                    }
                ],
                responses={
                    "200": {
                        "description": "User details",
                        "content": {
                            "application/json": {
                                "schema": {"type": "object"}
                            }
                        }
                    },
                    "404": {
                        "description": "User not found"
                    }
                },
                tags=["Users"]
            ),
            APIEndpoint(
                path="/auth/login",
                method="POST",
                summary="User login",
                description="Authenticate user and get token",
                request_body={
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "username": {"type": "string"},
                                    "password": {"type": "string"}
                                },
                                "required": ["username", "password"]
                            }
                        }
                    }
                },
                responses={
                    "200": {
                        "description": "Login successful",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "token": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "401": {
                        "description": "Invalid credentials"
                    }
                },
                tags=["Authentication"]
            ),
            APIEndpoint(
                path="/protected",
                method="GET",
                summary="Protected endpoint",
                description="Requires authentication",
                security=[{"bearerAuth": []}],
                responses={
                    "200": {
                        "description": "Success"
                    },
                    "401": {
                        "description": "Unauthorized"
                    }
                },
                tags=["Protected"]
            )
        ]
    
    @pytest.fixture
    def generator_config(self) -> DocumentationConfig:
        """Create generator configuration"""
        return DocumentationConfig(
            title="Test API",
            version="2.0.0",
            description="API for testing OpenAPI generation",
            base_url="https://api.example.com",
            contact={
                "name": "API Support",
                "email": "support@example.com",
                "url": "https://example.com/support"
            },
            license={
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            },
            servers=[
                {"url": "https://api.example.com", "description": "Production"},
                {"url": "https://staging-api.example.com", "description": "Staging"},
                {"url": "http://localhost:8000", "description": "Development"}
            ],
            security_schemes={
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                },
                "apiKey": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key"
                }
            }
        )
    
    def test_basic_spec_generation(self, sample_endpoints: List[APIEndpoint],
                                  generator_config: DocumentationConfig):
        """Test basic OpenAPI specification generation"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check required fields
        assert spec["openapi"] == "3.0.3"
        assert spec["info"]["title"] == "Test API"
        assert spec["info"]["version"] == "2.0.0"
        assert spec["info"]["description"] == "API for testing OpenAPI generation"
        
        # Check servers
        assert len(spec["servers"]) == 3
        assert spec["servers"][0]["url"] == "https://api.example.com"
        assert spec["servers"][1]["description"] == "Staging"
        
        # Check paths
        assert "paths" in spec
        assert "/" in spec["paths"]
        assert "/users" in spec["paths"]
        assert "/users/{user_id}" in spec["paths"]
        assert "/auth/login" in spec["paths"]
        assert "/protected" in spec["paths"]
        
        logger.info("✅ Basic OpenAPI spec generation successful")
    
    def test_endpoint_methods(self, sample_endpoints: List[APIEndpoint],
                             generator_config: DocumentationConfig):
        """Test endpoint method handling"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check multiple methods on same path
        assert "get" in spec["paths"]["/users"]
        assert "post" in spec["paths"]["/users"]
        
        # Check single method paths
        assert "get" in spec["paths"]["/"]
        assert "post" not in spec["paths"]["/"]
        
        # Check method details
        users_get = spec["paths"]["/users"]["get"]
        assert users_get["summary"] == "List users"
        assert len(users_get["parameters"]) == 2
        
        users_post = spec["paths"]["/users"]["post"]
        assert users_post["summary"] == "Create user"
        assert "requestBody" in users_post
        
        logger.info("✅ Endpoint method handling validated")
    
    def test_parameters_handling(self, sample_endpoints: List[APIEndpoint],
                                generator_config: DocumentationConfig):
        """Test parameter handling in spec"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check query parameters
        users_params = spec["paths"]["/users"]["get"]["parameters"]
        assert len(users_params) == 2
        
        page_param = next(p for p in users_params if p["name"] == "page")
        assert page_param["in"] == "query"
        assert not page_param["required"]
        assert page_param["schema"]["type"] == "integer"
        assert page_param["schema"]["default"] == 1
        
        # Check path parameters
        user_detail_params = spec["paths"]["/users/{user_id}"]["get"]["parameters"]
        assert len(user_detail_params) == 1
        
        user_id_param = user_detail_params[0]
        assert user_id_param["name"] == "user_id"
        assert user_id_param["in"] == "path"
        assert user_id_param["required"]
        
        logger.info("✅ Parameter handling validated")
    
    def test_request_body_handling(self, sample_endpoints: List[APIEndpoint],
                                   generator_config: DocumentationConfig):
        """Test request body handling"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check POST /users request body
        create_user = spec["paths"]["/users"]["post"]
        assert "requestBody" in create_user
        assert create_user["requestBody"]["required"]
        
        content = create_user["requestBody"]["content"]["application/json"]
        assert "schema" in content
        assert content["schema"]["type"] == "object"
        assert "properties" in content["schema"]
        assert "name" in content["schema"]["properties"]
        assert "email" in content["schema"]["properties"]
        
        # Check login request body
        login = spec["paths"]["/auth/login"]["post"]
        assert "requestBody" in login
        
        logger.info("✅ Request body handling validated")
    
    def test_response_handling(self, sample_endpoints: List[APIEndpoint],
                              generator_config: DocumentationConfig):
        """Test response handling"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check multiple responses
        create_user_responses = spec["paths"]["/users"]["post"]["responses"]
        assert "201" in create_user_responses
        assert "400" in create_user_responses
        assert create_user_responses["201"]["description"] == "User created"
        assert create_user_responses["400"]["description"] == "Invalid input"
        
        # Check response content
        list_users_response = spec["paths"]["/users"]["get"]["responses"]["200"]
        assert "content" in list_users_response
        schema = list_users_response["content"]["application/json"]["schema"]
        assert schema["type"] == "object"
        assert "users" in schema["properties"]
        assert "total" in schema["properties"]
        
        logger.info("✅ Response handling validated")
    
    def test_security_handling(self, sample_endpoints: List[APIEndpoint],
                              generator_config: DocumentationConfig):
        """Test security scheme handling"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check security schemes in components
        assert "components" in spec
        assert "securitySchemes" in spec["components"]
        assert "bearerAuth" in spec["components"]["securitySchemes"]
        assert "apiKey" in spec["components"]["securitySchemes"]
        
        # Check bearer auth details
        bearer = spec["components"]["securitySchemes"]["bearerAuth"]
        assert bearer["type"] == "http"
        assert bearer["scheme"] == "bearer"
        assert bearer["bearerFormat"] == "JWT"
        
        # Check endpoint security
        protected = spec["paths"]["/protected"]["get"]
        assert "security" in protected
        assert protected["security"] == [{"bearerAuth": []}]
        
        logger.info("✅ Security handling validated")
    
    def test_tags_handling(self, sample_endpoints: List[APIEndpoint],
                          generator_config: DocumentationConfig):
        """Test tags handling"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check tags collection
        assert "tags" in spec
        tag_names = [tag["name"] for tag in spec["tags"]]
        assert "General" in tag_names
        assert "Users" in tag_names
        assert "Authentication" in tag_names
        assert "Protected" in tag_names
        
        # Check endpoint tags
        assert spec["paths"]["/"]["get"]["tags"] == ["General"]
        assert spec["paths"]["/users"]["get"]["tags"] == ["Users"]
        assert spec["paths"]["/auth/login"]["post"]["tags"] == ["Authentication"]
        
        logger.info("✅ Tags handling validated")
    
    def test_spec_validation(self, sample_endpoints: List[APIEndpoint],
                            generator_config: DocumentationConfig):
        """Test OpenAPI spec validation"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Validate generated spec
        is_valid, errors = generator.validate_spec(spec)
        assert is_valid, f"Spec validation failed: {errors}"
        assert len(errors) == 0
        
        # Test invalid spec
        invalid_spec = {"info": {"title": "Test"}}  # Missing required fields
        is_valid, errors = generator.validate_spec(invalid_spec)
        assert not is_valid
        assert "Missing 'openapi' field" in errors
        assert "Missing 'paths' field" in errors
        
        # Test invalid path
        invalid_spec = {
            "openapi": "3.0.3",
            "info": {"title": "Test", "version": "1.0.0"},
            "paths": {
                "users": {}  # Path doesn't start with /
            }
        }
        is_valid, errors = generator.validate_spec(invalid_spec)
        assert not is_valid
        assert any("must start with '/'" in error for error in errors)
        
        logger.info("✅ Spec validation tested")
    
    def test_postman_conversion(self, sample_endpoints: List[APIEndpoint],
                               generator_config: DocumentationConfig):
        """Test Postman collection conversion"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Convert to Postman collection
        collection = generator.export_postman_collection(spec)
        
        # Check collection structure
        assert collection["info"]["name"] == "Test API"
        assert collection["info"]["description"] == "API for testing OpenAPI generation"
        assert "schema" in collection["info"]
        
        # Check items
        assert "item" in collection
        assert len(collection["item"]) == len(spec["paths"])
        
        # Check request structure
        first_item = collection["item"][0]
        assert "name" in first_item
        assert "item" in first_item  # Folder for path
        
        # Check individual request
        if first_item["item"]:
            request = first_item["item"][0]
            assert "name" in request
            assert "request" in request
            assert "method" in request["request"]
            assert "url" in request["request"]
        
        logger.info("✅ Postman collection conversion successful")
    
    def test_contact_and_license(self, sample_endpoints: List[APIEndpoint],
                                generator_config: DocumentationConfig):
        """Test contact and license information"""
        generator = OpenAPIGenerator(generator_config)
        spec = generator.generate_spec(sample_endpoints)
        
        # Check contact info
        assert "contact" in spec["info"]
        assert spec["info"]["contact"]["name"] == "API Support"
        assert spec["info"]["contact"]["email"] == "support@example.com"
        assert spec["info"]["contact"]["url"] == "https://example.com/support"
        
        # Check license info
        assert "license" in spec["info"]
        assert spec["info"]["license"]["name"] == "MIT"
        assert spec["info"]["license"]["url"] == "https://opensource.org/licenses/MIT"
        
        logger.info("✅ Contact and license information validated")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])