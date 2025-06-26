"""
Module: test_type_inference.py
Purpose: Test GraphQL type inference functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- graphql-core: https://graphql-core-3.readthedocs.io/

Example Usage:
>>> pytest test_type_inference.py -v
"""

import pytest
from typing import Optional, List, Union, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from graphql import (
    GraphQLString, GraphQLInt, GraphQLFloat, GraphQLBoolean,
    GraphQLList, GraphQLNonNull, GraphQLScalarType
)

from graphql_schema_generator_interaction import TypeInferenceEngine


class TestTypeInference:
    """Test type inference functionality"""
    
    def test_basic_type_inference(self):
        """Test inference of basic Python types"""
        engine = TypeInferenceEngine()
        
        # Test string
        assert engine.infer_graphql_type(str) == GraphQLString
        
        # Test int
        assert engine.infer_graphql_type(int) == GraphQLInt
        
        # Test float
        assert engine.infer_graphql_type(float) == GraphQLFloat
        
        # Test bool
        assert engine.infer_graphql_type(bool) == GraphQLBoolean
        
    def test_none_type_inference(self):
        """Test handling of None type"""
        engine = TypeInferenceEngine()
        
        # None should default to String
        assert engine.infer_graphql_type(None) == GraphQLString
        assert engine.infer_graphql_type(type(None)) == GraphQLString
        
    def test_datetime_type_inference(self):
        """Test datetime and date type inference"""
        engine = TypeInferenceEngine()
        
        # Test datetime
        datetime_type = engine.infer_graphql_type(datetime)
        assert isinstance(datetime_type, GraphQLScalarType)
        assert datetime_type.name == "DateTime"
        
        # Test date
        date_type = engine.infer_graphql_type(date)
        assert isinstance(date_type, GraphQLScalarType)
        assert date_type.name == "Date"
        
    def test_decimal_type_inference(self):
        """Test Decimal type inference"""
        engine = TypeInferenceEngine()
        
        # Decimal should map to Float
        assert engine.infer_graphql_type(Decimal) == GraphQLFloat
        
    def test_json_type_inference(self):
        """Test dict and list inference to JSON"""
        engine = TypeInferenceEngine()
        
        # Dict should map to JSON
        json_type = engine.infer_graphql_type(dict)
        assert isinstance(json_type, GraphQLScalarType)
        assert json_type.name == "JSON"
        
        # List should also map to JSON
        list_json_type = engine.infer_graphql_type(list)
        assert isinstance(list_json_type, GraphQLScalarType)
        assert list_json_type.name == "JSON"
        
    def test_optional_type_inference(self):
        """Test Optional type inference"""
        engine = TypeInferenceEngine()
        
        # Optional[str] should be nullable String
        optional_str_type = engine.infer_graphql_type(Optional[str])
        assert optional_str_type == GraphQLString
        
        # Optional[int] should be nullable Int
        optional_int_type = engine.infer_graphql_type(Optional[int])
        assert optional_int_type == GraphQLInt
        
    def test_list_type_inference(self):
        """Test List type inference"""
        engine = TypeInferenceEngine()
        
        # List[str] should be GraphQLList of String
        list_type = engine.infer_graphql_type(List[str])
        assert isinstance(list_type, GraphQLList)
        assert isinstance(list_type.of_type, GraphQLNonNull)
        assert list_type.of_type.of_type == GraphQLString
        
        # List[int] should be GraphQLList of Int
        list_int_type = engine.infer_graphql_type(List[int])
        assert isinstance(list_int_type, GraphQLList)
        assert isinstance(list_int_type.of_type, GraphQLNonNull)
        assert list_int_type.of_type.of_type == GraphQLInt
        
    def test_nullable_parameter(self):
        """Test nullable parameter handling"""
        engine = TypeInferenceEngine()
        
        # Non-nullable string
        non_null_str = engine.infer_graphql_type(str, nullable=False)
        assert isinstance(non_null_str, GraphQLNonNull)
        assert non_null_str.of_type == GraphQLString
        
        # Nullable string (default)
        nullable_str = engine.infer_graphql_type(str, nullable=True)
        assert nullable_str == GraphQLString
        
    def test_unknown_type_inference(self):
        """Test handling of unknown types"""
        engine = TypeInferenceEngine()
        
        # Custom class should default to String
        class CustomClass:
            pass
            
        assert engine.infer_graphql_type(CustomClass) == GraphQLString
        
    def test_custom_scalar_serialization(self):
        """Test custom scalar serialization"""
        engine = TypeInferenceEngine()
        
        # Test DateTime serialization
        dt = datetime(2023, 12, 25, 12, 0, 0)
        datetime_scalar = engine.custom_scalars["DateTime"]
        serialized = datetime_scalar.serialize(dt)
        assert serialized == dt.isoformat()
        
        # Test Date serialization
        d = date(2023, 12, 25)
        date_scalar = engine.custom_scalars["Date"]
        serialized = date_scalar.serialize(d)
        assert serialized == d.isoformat()
        
        # Test JSON serialization
        json_data = {"key": "value", "number": 42}
        json_scalar = engine.custom_scalars["JSON"]
        serialized = json_scalar.serialize(json_data)
        assert serialized == '{"key": "value", "number": 42}'
        
    def test_custom_scalar_parsing(self):
        """Test custom scalar parsing"""
        engine = TypeInferenceEngine()
        
        # Test DateTime parsing
        datetime_scalar = engine.custom_scalars["DateTime"]
        parsed = datetime_scalar.parse_value("2023-12-25T12:00:00")
        assert isinstance(parsed, datetime)
        assert parsed.year == 2023
        assert parsed.month == 12
        assert parsed.day == 25
        
        # Test Date parsing
        date_scalar = engine.custom_scalars["Date"]
        parsed = date_scalar.parse_value("2023-12-25")
        assert isinstance(parsed, date)
        assert parsed.year == 2023
        assert parsed.month == 12
        assert parsed.day == 25
        
        # Test JSON parsing
        json_scalar = engine.custom_scalars["JSON"]
        parsed = json_scalar.parse_value('{"key": "value"}')
        assert isinstance(parsed, dict)
        assert parsed["key"] == "value"


def run_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("Type Inference Tests")
    print("=" * 60)
    
    test_class = TestTypeInference()
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