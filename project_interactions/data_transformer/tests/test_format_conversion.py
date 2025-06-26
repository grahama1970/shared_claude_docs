"""
Module: test_format_conversion.py
Purpose: Test format conversion capabilities of the data transformer

Tests various data format conversions including JSON, CSV, XML, and Parquet.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import json
import io
import pytest
import pandas as pd
import pyarrow.parquet as pq
from datetime import datetime

from data_transformer_interaction import (
    DataTransformerInteraction,
    DataFormat
)


class TestFormatConversion:
    """Test format conversion functionality"""
    
    @pytest.fixture
    def transformer(self):
        """Create a data transformer instance"""
        return DataTransformerInteraction()
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for testing"""
        return [
            {"id": 1, "name": "Alice", "score": 95.5, "active": True},
            {"id": 2, "name": "Bob", "score": 87.3, "active": False},
            {"id": 3, "name": "Charlie", "score": 92.1, "active": True}
        ]
    
    def test_json_to_csv_conversion(self, transformer, sample_data):
        """Test JSON to CSV conversion"""
        result = transformer.transform_data(
            input_data=sample_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.CSV
        )
        
        assert result.success
        assert isinstance(result.transformed_data, str)
        assert "id,name,score,active" in result.transformed_data
        assert "Alice" in result.transformed_data
        assert "95.5" in result.transformed_data
        assert result.records_processed == 3
    
    def test_csv_to_json_conversion(self, transformer):
        """Test CSV to JSON conversion"""
        csv_data = """id,name,score,active
1,Alice,95.5,True
2,Bob,87.3,False
3,Charlie,92.1,True"""
        
        result = transformer.transform_data(
            input_data=csv_data,
            source_format=DataFormat.CSV,
            target_format=DataFormat.JSON
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert len(data) == 3
        assert data[0]["name"] == "Alice"
        assert data[1]["score"] == 87.3
    
    def test_json_to_xml_conversion(self, transformer, sample_data):
        """Test JSON to XML conversion"""
        result = transformer.transform_data(
            input_data=sample_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.XML
        )
        
        assert result.success
        assert isinstance(result.transformed_data, str)
        assert "<?xml version" in result.transformed_data
        assert "<name>Alice</name>" in result.transformed_data
        assert "<score>95.5</score>" in result.transformed_data
    
    def test_xml_to_json_conversion(self, transformer):
        """Test XML to JSON conversion"""
        xml_data = """<?xml version="1.0"?>
        <root>
            <record>
                <id>1</id>
                <name>Alice</name>
                <score>95.5</score>
                <active>true</active>
            </record>
            <record>
                <id>2</id>
                <name>Bob</name>
                <score>87.3</score>
                <active>false</active>
            </record>
        </root>"""
        
        result = transformer.transform_data(
            input_data=xml_data,
            source_format=DataFormat.XML,
            target_format=DataFormat.JSON
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert len(data) == 2
        assert data[0]["name"] == "Alice"
    
    def test_dataframe_to_parquet_conversion(self, transformer, sample_data):
        """Test DataFrame to Parquet conversion"""
        df = pd.DataFrame(sample_data)
        
        result = transformer.transform_data(
            input_data=df,
            source_format=DataFormat.DATAFRAME,
            target_format=DataFormat.PARQUET
        )
        
        assert result.success
        assert isinstance(result.transformed_data, bytes)
        
        # Verify parquet data
        table = pq.read_table(io.BytesIO(result.transformed_data))
        df_back = table.to_pandas()
        assert len(df_back) == 3
        assert df_back["name"].tolist() == ["Alice", "Bob", "Charlie"]
    
    def test_parquet_to_csv_conversion(self, transformer, sample_data):
        """Test Parquet to CSV conversion"""
        # First convert to parquet
        df = pd.DataFrame(sample_data)
        buffer = io.BytesIO()
        df.to_parquet(buffer)
        parquet_data = buffer.getvalue()
        
        # Then convert to CSV
        result = transformer.transform_data(
            input_data=parquet_data,
            source_format=DataFormat.PARQUET,
            target_format=DataFormat.CSV
        )
        
        assert result.success
        assert "Alice" in result.transformed_data
        assert "95.5" in result.transformed_data
    
    def test_dict_to_json_single_record(self, transformer):
        """Test single dictionary to JSON conversion"""
        single_record = {"id": 1, "name": "Test", "value": 100}
        
        result = transformer.transform_data(
            input_data=single_record,
            source_format=DataFormat.DICT,
            target_format=DataFormat.JSON
        )
        
        assert result.success
        data = json.loads(result.transformed_data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Test"
    
    def test_mixed_type_conversion(self, transformer):
        """Test conversion with mixed data types"""
        mixed_data = [
            {
                "id": 1,
                "timestamp": datetime.now().isoformat(),
                "values": [1, 2, 3],
                "metadata": {"key": "value"},
                "nullable": None
            }
        ]
        
        # JSON to CSV (should handle complex types)
        result = transformer.transform_data(
            input_data=mixed_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.CSV
        )
        
        assert result.success
        assert result.warnings  # Should have warnings about complex types
    
    def test_empty_data_conversion(self, transformer):
        """Test conversion with empty data"""
        result = transformer.transform_data(
            input_data=[],
            source_format=DataFormat.JSON,
            target_format=DataFormat.CSV
        )
        
        assert result.success
        assert result.records_processed == 0
    
    def test_large_dataset_conversion(self, transformer):
        """Test conversion with larger dataset"""
        large_data = [
            {"id": i, "value": i * 2, "name": f"Record_{i}"}
            for i in range(1000)
        ]
        
        result = transformer.transform_data(
            input_data=large_data,
            source_format=DataFormat.JSON,
            target_format=DataFormat.CSV,
            streaming=True,
            buffer_size=100
        )
        
        assert result.success
        assert result.records_processed == 1000
        assert "Record_999" in result.transformed_data
    
    def test_unsupported_format_error(self, transformer):
        """Test error handling for unsupported formats"""
        result = transformer.transform_data(
            input_data={"test": "data"},
            source_format="invalid_format",
            target_format=DataFormat.JSON
        )
        
        assert not result.success
        assert len(result.errors) > 0


if __name__ == "__main__":
    # Run basic tests
    transformer = DataTransformerInteraction()
    
    # Test JSON to CSV
    test_data = [
        {"name": "Test1", "value": 100},
        {"name": "Test2", "value": 200}
    ]
    
    result = transformer.transform_data(
        input_data=test_data,
        source_format=DataFormat.JSON,
        target_format=DataFormat.CSV
    )
    
    assert result.success
    assert "Test1" in result.transformed_data
    print("✅ Format conversion tests passed!")