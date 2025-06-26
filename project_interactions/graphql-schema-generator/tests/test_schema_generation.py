"""
Module: test_schema_generation.py
Purpose: Test GraphQL schema generation functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- graphql-core: https://graphql-core-3.readthedocs.io/

Example Usage:
>>> pytest test_schema_generation.py -v
"""

import pytest
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from graphql import GraphQLSchema, GraphQLObjectType, GraphQLString, print_schema

from graphql_schema_generator_interaction import (
    GraphQLSchemaGenerator, FieldMetadata, SchemaVersion
)


@dataclass
class TestUser:
    """Test user model"""
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True
    bio: Optional[str] = None


@dataclass
class TestPost:
    """Test post model"""
    id: int
    title: str
    content: str
    author_id: int
    tags: List[str]
    published_at: Optional[datetime] = None


@dataclass
class TestComment:
    """Test comment model"""
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime


class TestSchemaGeneration:
    """Test schema generation functionality"""
    
    def test_single_model_generation(self):
        """Test generating schema from single model"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([TestUser])
        
        assert schema is not None
        assert isinstance(schema, GraphQLSchema)
        assert "User" in generator.generated_types
        
        user_type = generator.generated_types["User"]
        assert "id" in user_type.fields
        assert "username" in user_type.fields
        assert "email" in user_type.fields
        
    def test_multiple_models_generation(self):
        """Test generating schema from multiple models"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([TestUser, TestPost, TestComment])
        
        assert len(generator.generated_types) == 3
        assert "User" in generator.generated_types
        assert "Post" in generator.generated_types
        assert "Comment" in generator.generated_types
        
    def test_query_type_generation(self):
        """Test automatic Query type generation"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([TestUser])
        
        query_type = schema.query_type
        assert query_type is not None
        assert "getUser" in query_type.fields
        assert "listUsers" in query_type.fields
        
    def test_mutation_type_generation(self):
        """Test automatic Mutation type generation"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([TestUser])
        
        mutation_type = schema.mutation_type
        assert mutation_type is not None
        assert "createUser" in mutation_type.fields
        assert "updateUser" in mutation_type.fields
        assert "deleteUser" in mutation_type.fields
        
    def test_subscription_type_generation(self):
        """Test automatic Subscription type generation"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([TestUser])
        
        subscription_type = schema.subscription_type
        assert subscription_type is not None
        assert "userCreated" in subscription_type.fields
        assert "userUpdated" in subscription_type.fields
        
    def test_sdl_export(self):
        """Test SDL export functionality"""
        generator = GraphQLSchemaGenerator()
        generator.generate_from_models([TestUser])
        
        sdl = generator.to_sdl()
        assert sdl is not None
        assert "type User" in sdl
        assert "type Query" in sdl
        
    def test_schema_versioning(self):
        """Test schema versioning functionality"""
        generator = GraphQLSchemaGenerator()
        
        # Initial version
        assert generator.version.version == "1.0.0"
        
        # Add change and bump version
        generator.version.add_change("add_field", "Added field", ["User.newField"])
        generator.version.bump_version("minor")
        assert generator.version.version == "1.1.0"
        assert len(generator.version.changelog) == 1
        
    def test_empty_model_list(self):
        """Test handling empty model list"""
        generator = GraphQLSchemaGenerator()
        schema = generator.generate_from_models([])
        
        assert schema is not None
        assert len(generator.generated_types) == 0
        
    def test_documentation_generation(self):
        """Test documentation generation"""
        generator = GraphQLSchemaGenerator()
        generator.generate_from_models([TestUser, TestPost])
        
        docs = generator.generate_documentation()
        assert docs is not None
        assert "# GraphQL Schema" in docs
        assert "## Types" in docs
        assert "### User" in docs
        assert "### Post" in docs
        
    def test_schema_validation(self):
        """Test schema validation"""
        generator = GraphQLSchemaGenerator()
        generator.generate_from_models([TestUser])
        
        errors = generator.validate_schema()
        assert isinstance(errors, list)
        # Schema should be valid for simple models
        assert len(errors) == 0


def run_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("Schema Generation Tests")
    print("=" * 60)
    
    test_class = TestSchemaGeneration()
    test_methods = [
        method for method in dir(test_class) 
        if method.startswith('test_')
    ]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        try:
            method = getattr(test_class, method_name)
            method()
            print(f"✅ {method_name}")
            passed += 1
        except Exception as e:
            print(f"❌ {method_name}: {str(e)}")
            failed += 1
            
    print("\n" + "=" * 60)
    print(f"Tests passed: {passed}/{passed + failed}")
    if failed > 0:
        print(f"Tests failed: {failed}")
        return 1
    else:
        print("All tests passed!")
        return 0


if __name__ == "__main__":
    exit(run_tests())