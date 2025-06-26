"""
Module: test_data_cleaning.py
Purpose: Test data cleaning and normalization capabilities

Tests data quality validation, cleaning operations, and error handling.
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
    TransformationType
)


class TestDataCleaning:
    """Test data cleaning and quality validation functionality"""
    
    @pytest.fixture
    def transformer(self):
        """Create a data transformer instance"""
        return DataTransformerInteraction()
    
    @pytest.fixture
    def dirty_data(self):
        """Sample data with quality issues"""
        return [
            {
                "id": 1,
                "name": "  John Doe  ",
                "email": "JOHN@EXAMPLE.COM",
                "phone": "123-456-7890!!!",
                "age": "25",
                "salary": None
            },
            {
                "id": 2,
                "name": "Jane Smith   ",
                "email": "jane@test.com  ",
                "phone": "(098) 765-4321",
                "age": "invalid",
                "salary": "50000"
            },
            {
                "id": 3,
                "name": None,
                "email": "bob@",
                "phone": "",
                "age": "30",
                "salary": "75000.50"
            }
        ]
    
    def test_string_cleaning(self, transformer):
        """Test string cleaning operations"""
        data = [
            {"text": "  Hello World  ", "code": "ABC123!!!"},
            {"text": "  Python  Programming  ", "code": "XYZ@#$789"}
        ]
        
        transformations = [
            {"type": "clean", "field": "text", "parameters": {"operation": "trim"}},
            {"type": "clean", "field": "code", "parameters": {"operation": "remove_special"}}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        cleaned = json.loads(result.transformed_data)
        assert cleaned[0]["text"] == "Hello World"
        assert cleaned[0]["code"] == "ABC123"
        assert cleaned[1]["text"] == "Python  Programming"
        assert cleaned[1]["code"] == "XYZ789"
    
    def test_custom_cleaning_functions(self, transformer):
        """Test custom cleaning transformations"""
        # Register custom cleaners
        transformer.register_custom_transformer(
            "clean_phone",
            lambda x: ''.join(filter(str.isdigit, str(x))) if x else ""
        )
        
        transformer.register_custom_transformer(
            "validate_email",
            lambda x: x if "@" in str(x) and "." in str(x).split("@")[1] else None
        )
        
        data = [
            {"phone": "(123) 456-7890", "email": "test@example.com"},
            {"phone": "555.123.4567", "email": "invalid@"},
            {"phone": None, "email": "valid@email.org"}
        ]
        
        transformations = [
            {
                "type": "custom",
                "field": "phone",
                "custom_func": transformer.custom_transformers["clean_phone"]
            },
            {
                "type": "custom",
                "field": "email",
                "custom_func": transformer.custom_transformers["validate_email"]
            }
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        cleaned = json.loads(result.transformed_data)
        assert cleaned[0]["phone"] == "1234567890"
        assert cleaned[0]["email"] == "test@example.com"
        assert cleaned[1]["phone"] == "5551234567"
        assert cleaned[1]["email"] is None
        assert cleaned[2]["phone"] == ""
        assert cleaned[2]["email"] == "valid@email.org"
    
    def test_data_quality_validation(self, transformer, dirty_data):
        """Test data quality metrics collection"""
        result = transformer.transform_data(
            input_data=dirty_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            validate_quality=True
        )
        
        assert result.success
        metrics = result.quality_metrics
        
        # Check null field detection
        assert "name" in metrics.null_fields
        assert metrics.null_fields["name"] == 1
        assert "salary" in metrics.null_fields
        assert metrics.null_fields["salary"] == 1
        
        # Check record counts
        assert metrics.total_records == 3
        assert metrics.invalid_records > 0
        
        # Check warnings
        assert len(result.warnings) > 0
        assert any("null values" in w for w in result.warnings)
    
    def test_normalization(self, transformer):
        """Test data normalization"""
        data = [
            {"id": 1, "score": 10, "value": 100},
            {"id": 2, "score": 50, "value": 200},
            {"id": 3, "score": 90, "value": 300}
        ]
        
        transformations = [
            {"type": "normalize", "field": "score"},
            {"type": "normalize", "field": "value"}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        normalized = json.loads(result.transformed_data)
        
        # Check score normalization (10-90 range -> 0-1)
        assert normalized[0]["score"] == 0.0  # (10-10)/(90-10) = 0
        assert normalized[2]["score"] == 1.0  # (90-10)/(90-10) = 1
        assert 0 <= normalized[1]["score"] <= 1
        
        # Check value normalization
        assert normalized[0]["value"] == 0.0
        assert normalized[2]["value"] == 1.0
    
    def test_filtering_invalid_records(self, transformer, dirty_data):
        """Test filtering out invalid records"""
        transformations = [
            # First try to cast age to int - will fail for "invalid"
            {"type": "type_cast", "field": "age", "target_type": "float"},
            # Filter out records where age conversion failed
            {"type": "filter", "condition": "age > 0"}
        ]
        
        result = transformer.transform_data(
            input_data=dirty_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        filtered = json.loads(result.transformed_data)
        assert len(filtered) == 2  # Should have filtered out the invalid age record
    
    def test_aggregation_cleaning(self, transformer):
        """Test aggregation as a form of data cleaning"""
        data = [
            {"category": "A", "value": 10, "valid": True},
            {"category": "A", "value": 20, "valid": True},
            {"category": "B", "value": 15, "valid": False},
            {"category": "B", "value": 25, "valid": True}
        ]
        
        # Filter and aggregate
        transformations = [
            {"type": "filter", "condition": "valid == True"},
            {"type": "aggregate", "aggregation": "sum"}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        assert result.success
        aggregated = json.loads(result.transformed_data)
        assert len(aggregated) == 1
        assert aggregated[0]["value"] == 55  # 10 + 20 + 25 (15 filtered out)
    
    def test_error_handling_with_fallbacks(self, transformer):
        """Test error handling during cleaning operations"""
        data = [
            {"id": 1, "date": "2023-01-15", "amount": "100.50"},
            {"id": 2, "date": "invalid-date", "amount": "invalid"},
            {"id": 3, "date": "2023-02-20", "amount": "200.75"}
        ]
        
        # Register a custom transformer with error handling
        def safe_date_parse(x):
            try:
                return datetime.fromisoformat(x).timestamp()
            except:
                return None
        
        transformer.register_custom_transformer("safe_date_parse", safe_date_parse)
        
        transformations = [
            {
                "type": "custom",
                "field": "date",
                "custom_func": transformer.custom_transformers["safe_date_parse"]
            },
            {"type": "type_cast", "field": "amount", "target_type": "float"}
        ]
        
        result = transformer.transform_data(
            input_data=data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            transformations=transformations
        )
        
        # Should succeed even with errors
        assert result.success
        cleaned = json.loads(result.transformed_data)
        assert cleaned[0]["date"] is not None  # Valid date converted
        assert cleaned[1]["date"] is None  # Invalid date -> None
        assert cleaned[2]["date"] is not None  # Valid date converted
    
    def test_streaming_data_cleaning(self, transformer):
        """Test cleaning large datasets with streaming"""
        # Generate data with issues
        def generate_dirty_data():
            for i in range(2000):
                yield {
                    "id": i,
                    "name": f"  User {i}  " if i % 2 == 0 else f"USER{i}",
                    "email": f"user{i}@test.com" if i % 3 != 0 else "invalid",
                    "value": str(i * 10) if i % 5 != 0 else None
                }
        
        # Use streaming transformation
        stream_results = list(transformer.stream_transform(
            input_stream=generate_dirty_data(),
            source_format=DataFormat.DICT,
            target_format=DataFormat.JSON,
            transformations=[
                {"type": "clean", "field": "name", "parameters": {"operation": "trim"}},
                {"type": "filter", "condition": "value is not None"},
                {"type": "type_cast", "field": "value", "target_type": "float"}
            ],
            buffer_size=500
        ))
        
        assert len(stream_results) > 0
        
        # Check first batch
        first_batch = json.loads(stream_results[0])
        assert all("value" in record for record in first_batch)
        assert all(isinstance(record["value"], (int, float)) for record in first_batch)
    
    def test_chained_cleaning_operations(self, transformer):
        """Test chaining multiple cleaning operations"""
        data = {"records": [
            {"raw_data": "  ABC123@#$  ", "status": "ACTIVE"},
            {"raw_data": "XYZ789!!!", "status": "inactive"}
        ]}
        
        # Define a chain of transformations
        chain = [
            {
                "source_format": DataFormat.DICT,
                "target_format": DataFormat.JSON,
                "transformations": [
                    {"type": "clean", "field": "raw_data", "parameters": {"operation": "trim"}}
                ]
            },
            {
                "source_format": DataFormat.JSON,
                "target_format": DataFormat.JSON,
                "transformations": [
                    {"type": "clean", "field": "raw_data", "parameters": {"operation": "remove_special"}}
                ]
            },
            {
                "source_format": DataFormat.JSON,
                "target_format": DataFormat.DICT,
                "transformations": [
                    {
                        "type": "custom",
                        "field": "status",
                        "custom_func": transformer.custom_transformers["lowercase"]
                    }
                ]
            }
        ]
        
        result = transformer.chain_transformations(data["records"], chain)
        
        assert result[0]["raw_data"] == "ABC123"
        assert result[0]["status"] == "active"
        assert result[1]["raw_data"] == "XYZ789"
        assert result[1]["status"] == "inactive"
    
    def test_data_quality_report(self, transformer, dirty_data):
        """Test comprehensive data quality reporting"""
        # Add more issues to the data
        dirty_data.append({
            "id": "not_a_number",
            "name": "",
            "email": None,
            "phone": None,
            "age": None,
            "salary": "not_a_salary"
        })
        
        result = transformer.transform_data(
            input_data=dirty_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.JSON,
            validate_quality=True,
            transformations=[
                {"type": "type_cast", "field": "salary", "target_type": "float"}
            ]
        )
        
        # Check quality metrics
        metrics = result.quality_metrics
        assert metrics.total_records == 4
        assert metrics.invalid_records > 0
        assert len(metrics.null_fields) > 0
        
        # Check audit trail for failures
        assert any(not audit.success for audit in result.audit_trail)


if __name__ == "__main__":
    # Run basic cleaning test
    transformer = DataTransformerInteraction()
    
    dirty = [
        {"name": "  Test  ", "value": "123abc!!!", "email": "TEST@EXAMPLE.COM"}
    ]
    
    result = transformer.transform_data(
        input_data=dirty,
        source_format=DataFormat.JSON,
        target_format=DataFormat.JSON,
        transformations=[
            {"type": "clean", "field": "name", "parameters": {"operation": "trim"}},
            {"type": "clean", "field": "value", "parameters": {"operation": "remove_special"}},
            {"type": "custom", "field": "email", "custom_func": transformer.custom_transformers["lowercase"]}
        ]
    )
    
    assert result.success
    cleaned = json.loads(result.transformed_data)
    assert cleaned[0]["name"] == "Test"
    assert cleaned[0]["value"] == "123abc"
    assert cleaned[0]["email"] == "test@example.com"
    print("✅ Data cleaning tests passed!")