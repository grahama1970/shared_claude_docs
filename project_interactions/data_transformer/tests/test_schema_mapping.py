"""
Module: test_schema_mapping.py
Purpose: Test schema mapping and transformation capabilities

Tests field renaming, type conversion, and complex schema transformations.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
import pytest
from datetime import datetime

from data_transformer_interaction import (
    DataTransformerInteraction,
    DataFormat,
    TransformationType,
    TransformationRule
)


class TestSchemaMapping:
    """Test schema mapping and transformation functionality"""
    
    @pytest.fixture
    def transformer(self):
        """Create a data transformer instance"""
        return DataTransformerInteraction()
    
    @pytest.fixture
    def user_data(self):
        """Sample user data with inconsistent schema"""
        return [
            {
                "firstName": "John",
                "lastName": "Doe",
                "emailAddress": "john@example.com",
                "phoneNumber": "123-456-7890",
                "dateOfBirth": "1990-01-15"
            },
            {
                "firstName": "Jane",
                "lastName": "Smith",
                "emailAddress": "jane@example.com",
                "phoneNumber": "098-765-4321",
                "dateOfBirth": "1985-06-20"
            }
        ]
    
    def test_simple_field_renaming(self, transformer, user_data):
        """Test basic field renaming through schema mapping"""
        schema_mapping = {
            "firstName": "first_name",
            "lastName": "last_name",
            "emailAddress": "email",
            "phoneNumber": "phone",
            "dateOfBirth": "dob"
        }
        
        result = transformer.transform_data(
            input_data=user_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            schema_mapping=schema_mapping
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert "first_name" in data[0]
        assert "email" in data[0]
        assert data[0]["first_name"] == "John"
        assert data[1]["email"] == "jane@example.com"
    
    def test_field_extraction(self, transformer):
        """Test extracting fields from complex values"""
        data = [
            {"full_name": "John Doe", "contact": "john@example.com (Primary)"},
            {"full_name": "Jane Smith", "contact": "jane@example.com (Work)"}
        ]
        
        transformations = [
            {
                "type": "extract_field",
                "field": "full_name",
                "target_field": "first_name",
                "parameters": {"pattern": r"(\w+)\s"}
            },
            {
                "type": "extract_field",
                "field": "full_name",
                "target_field": "last_name",
                "parameters": {"pattern": r"\w+\s(\w+)"}
            },
            {
                "type": "extract_field",
                "field": "contact",
                "target_field": "email",
                "parameters": {"pattern": r"([\w.]+@[\w.]+)"}
            }
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert data[0]["first_name"] == "John"
        assert data[0]["last_name"] == "Doe"
        assert data[0]["email"] == "john@example.com"
    
    def test_nested_to_flat_schema(self, transformer):
        """Test flattening nested data structures"""
        nested_data = [
            {
                "id": 1,
                "user": {
                    "name": "John Doe",
                    "email": "john@example.com"
                },
                "address": {
                    "street": "123 Main St",
                    "city": "Anytown",
                    "zip": "12345"
                }
            }
        ]
        
        # Convert to DataFrame which automatically flattens
        result = transformer.transform_data(
            input_data=nested_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.CSV
        )
        
        assert result.success
        assert "123 Main St" in result.transformed_data
        assert "john@example.com" in result.transformed_data
    
    def test_type_casting_with_schema(self, transformer):
        """Test type conversion during transformation"""
        data = [
            {"id": "1", "price": "19.99", "quantity": "5", "in_stock": "true"},
            {"id": "2", "price": "29.99", "quantity": "0", "in_stock": "false"}
        ]
        
        transformations = [
            {"type": "type_cast", "field": "id", "target_type": "int"},
            {"type": "type_cast", "field": "price", "target_type": "float"},
            {"type": "type_cast", "field": "quantity", "target_type": "int"},
            {"type": "type_cast", "field": "in_stock", "target_type": "bool"}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert isinstance(data[0]["id"], int)
        assert isinstance(data[0]["price"], float)
        assert data[0]["price"] == 19.99
        assert isinstance(data[0]["in_stock"], bool)
    
    def test_conditional_field_mapping(self, transformer):
        """Test adding fields based on conditions"""
        data = [
            {"name": "Product A", "price": 150},
            {"name": "Product B", "price": 50},
            {"name": "Product C", "price": 250}
        ]
        
        transformations = [
            {
                "type": "add_field",
                "target_field": "category",
                "value": "Standard"  # Default value
            },
            {
                "type": "filter",
                "condition": "price < 100"
            }
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert len(data) == 1  # Only one product under $100
        assert data[0]["name"] == "Product B"
        assert data[0]["category"] == "Standard"
    
    def test_complex_schema_transformation(self, transformer):
        """Test complex transformation with multiple operations"""
        data = [
            {
                "customer_id": "CUST001",
                "full_name": "John Michael Doe",
                "email": "  john.doe@example.com  ",
                "registration_date": "2023-01-15",
                "total_purchases": "1250.50"
            }
        ]
        
        transformations = [
            # Clean email
            {"type": "clean", "field": "email", "parameters": {"operation": "trim"}},
            # Extract first name
            {
                "type": "extract_field",
                "field": "full_name",
                "target_field": "first_name",
                "parameters": {"pattern": r"^(\w+)"}
            },
            # Type conversion
            {"type": "type_cast", "field": "total_purchases", "target_type": "float"},
            # Add calculated field
            {"type": "add_field", "target_field": "vip_customer", "value": True},
            # Rename field
            {"type": "rename_field", "field": "customer_id", "target_field": "id"}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert data[0]["email"] == "john.doe@example.com"  # Trimmed
        assert data[0]["first_name"] == "John"
        assert isinstance(data[0]["total_purchases"], float)
        assert data[0]["vip_customer"] is True
        assert "id" in data[0] and "customer_id" not in data[0]
    
    def test_template_based_schema_transformation(self, transformer):
        """Test using templates for consistent transformations"""
        # Create a customer data standardization template
        template = transformer.create_template(
            name="customer_standardization",
            description="Standardize customer data format",
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=[
                {"type": "clean", "field": "email", "parameters": {"operation": "trim"}},
                {"type": "rename_field", "field": "customerID", "target_field": "customer_id"},
                {"type": "rename_field", "field": "firstName", "target_field": "first_name"},
                {"type": "rename_field", "field": "lastName", "target_field": "last_name"},
                {"type": "type_cast", "field": "age", "target_type": "int"},
                {"type": "add_field", "target_field": "processed_at", "value": datetime.now().isoformat()}
            ],
            schema_mapping={
                "Phone": "phone_number",
                "Email": "email_address"
            }
        )
        
        # Apply template to data
        data = [
            {
                "customerID": "C001",
                "firstName": "Alice",
                "lastName": "Johnson",
                "email": " alice@example.com ",
                "age": "28",
                "Phone": "555-1234"
            }
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            template_name="customer_standardization"
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert data[0]["customer_id"] == "C001"
        assert data[0]["first_name"] == "Alice"
        assert data[0]["email"] == "alice@example.com"
        assert isinstance(data[0]["age"], int)
        assert "processed_at" in data[0]
        assert data[0]["phone_number"] == "555-1234"
    
    def test_audit_trail(self, transformer, user_data):
        """Test that transformations are properly audited"""
        transformations = [
            {"type": "rename_field", "field": "firstName", "target_field": "first_name"},
            {"type": "add_field", "target_field": "source", "value": "api"}
        ]
        
        result = transformer.transform_data(
            input_data=user_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        assert len(result.audit_trail) >= 2
        assert any(audit.transformation_type == "rename_field" for audit in result.audit_trail)
        assert any(audit.transformation_type == "add_field" for audit in result.audit_trail)
        assert all(audit.success for audit in result.audit_trail)
    
    def test_schema_analysis(self, transformer):
        """Test schema analysis functionality"""
        data = [
            {"id": 1, "name": "Item 1", "price": 10.5, "quantity": 100},
            {"id": 2, "name": "Item 2", "price": 20.0, "quantity": 50},
            {"id": 3, "name": "Item 3", "price": 15.5, "quantity": 75}
        ]
        
        schema = transformer.analyze_data_schema(data, DataFormat.JSON)
        
        assert "fields" in schema
        assert "id" in schema["fields"]
        assert schema["fields"]["id"]["type"] == "int64"
        assert schema["record_count"] == 3
        assert "statistics" in schema
        assert "price" in schema["statistics"]
        assert schema["statistics"]["price"]["mean"] == 15.333333333333334


if __name__ == "__main__":
    # Run basic schema mapping test
    transformer = DataTransformerInteraction()
    
    data = [
        {"oldName": "Test", "oldValue": "100"}
    ]
    
    result = transformer.transform_data(
        input_data=data,
        source_format=DataFormat.JSON,
        target_format=DataFormat.JSON,
        schema_mapping={"oldName": "name", "oldValue": "value"},
        transformations=[
            {"type": "type_cast", "field": "value", "target_type": "int"}
        ]
    )
    
    assert result.success
    transformed = json.loads(result.transformed_data)
    assert transformed[0]["name"] == "Test"
    assert transformed[0]["value"] == 100
    print("✅ Schema mapping tests passed!")