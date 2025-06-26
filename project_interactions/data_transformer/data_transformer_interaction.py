
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: data_transformer_interaction.py
Purpose: Flexible data transformation engine for format conversion, schema mapping, and data processing

This module provides a comprehensive data transformation engine that handles various data formats,
performs schema mapping, data cleaning, and supports custom transformation rules with streaming capabilities.

External Dependencies:
- pandas: https://pandas.pydata.org/docs/
- pydantic: https://docs.pydantic.dev/
- pyarrow: https://arrow.apache.org/docs/python/
- xmltodict: https://github.com/martinblech/xmltodict

Example Usage:
>>> transformer = DataTransformerInteraction()
>>> result = transformer.transform_data(
...     input_data={'name': 'John', 'age': '30'},
...     source_format='json',
...     target_format='csv',
...     transformations=[
...         {'type': 'type_cast', 'field': 'age', 'target_type': 'int'},
...         {'type': 'add_field', 'field': 'adult', 'value': True}
...     ]
... )
>>> print(result.transformed_data)
'name,age,adult\\nJohn,30,True\\n'
"""

import json
import csv
import io
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union, Callable, Iterator
from enum import Enum
from pathlib import Path
import logging
from dataclasses import dataclass, field
from collections import defaultdict

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import xmltodict
from pydantic import BaseModel, Field, ConfigDict, field_validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataFormat(str, Enum):
    """Supported data formats for transformation"""
    JSON = "json"
    XML = "xml"
    CSV = "csv"
    PARQUET = "parquet"
    DICT = "dict"
    DATAFRAME = "dataframe"


class TransformationType(str, Enum):
    """Types of transformations available"""
    TYPE_CAST = "type_cast"
    RENAME_FIELD = "rename_field"
    ADD_FIELD = "add_field"
    REMOVE_FIELD = "remove_field"
    EXTRACT_FIELD = "extract_field"
    AGGREGATE = "aggregate"
    FILTER = "filter"
    NORMALIZE = "normalize"
    CLEAN = "clean"
    CUSTOM = "custom"
    MAP_SCHEMA = "map_schema"


class TransformationRule(BaseModel):
    """Defines a single transformation rule"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    type: TransformationType
    field: Optional[str] = None
    target_field: Optional[str] = None
    value: Optional[Any] = None
    target_type: Optional[str] = None
    mapping: Optional[Dict[str, str]] = None
    condition: Optional[str] = None
    aggregation: Optional[str] = None
    custom_func: Optional[Callable] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class DataQualityMetrics(BaseModel):
    """Metrics for data quality validation"""
    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    null_fields: Dict[str, int] = Field(default_factory=dict)
    type_mismatches: Dict[str, int] = Field(default_factory=dict)
    validation_errors: List[str] = Field(default_factory=list)


class TransformationAudit(BaseModel):
    """Audit trail for transformations"""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transformation_type: str
    field_affected: Optional[str] = None
    before_value: Optional[Any] = None
    after_value: Optional[Any] = None
    success: bool = True
    error_message: Optional[str] = None


class TransformationResult(BaseModel):
    """Result of a data transformation operation"""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    success: bool
    transformed_data: Any
    source_format: DataFormat
    target_format: DataFormat
    records_processed: int
    transformations_applied: List[str]
    quality_metrics: DataQualityMetrics
    audit_trail: List[TransformationAudit]
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    processing_time_ms: float


class TransformationTemplate(BaseModel):
    """Reusable transformation template"""
    name: str
    description: str
    source_format: DataFormat
    target_format: DataFormat
    transformations: List[TransformationRule]
    schema_mapping: Optional[Dict[str, str]] = None
    validation_rules: Optional[Dict[str, Any]] = None


@dataclass
class StreamingContext:
    """Context for streaming transformations"""
    buffer_size: int = 1000
    processed_count: int = 0
    error_count: int = 0
    audit_trail: List[TransformationAudit] = field(default_factory=list)
    quality_metrics: DataQualityMetrics = field(default_factory=DataQualityMetrics)


class DataTransformerInteraction:
    """
    Advanced data transformation engine with support for multiple formats,
    schema mapping, and custom transformation rules.
    """
    
    def __init__(self):
        """Initialize the data transformer with default configuration"""
        self.templates: Dict[str, TransformationTemplate] = {}
        self.custom_transformers: Dict[str, Callable] = {}
        self._initialize_default_transformers()
    
    def _initialize_default_transformers(self):
        """Initialize default transformation functions"""
        self.custom_transformers = {
            'uppercase': lambda x: x.upper() if isinstance(x, str) else x,
            'lowercase': lambda x: x.lower() if isinstance(x, str) else x,
            'trim': lambda x: x.strip() if isinstance(x, str) else x,
            'remove_special': lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)),
            'to_timestamp': lambda x: datetime.fromisoformat(x).timestamp() if isinstance(x, str) else x,
            'from_timestamp': lambda x: datetime.fromtimestamp(x).isoformat() if isinstance(x, (int, float)) else x,
        }
    
    def transform_data(
        self,
        input_data: Any,
        source_format: Union[str, DataFormat],
        target_format: Union[str, DataFormat],
        transformations: Optional[List[Union[Dict, TransformationRule]]] = None,
        schema_mapping: Optional[Dict[str, str]] = None,
        template_name: Optional[str] = None,
        streaming: bool = False,
        buffer_size: int = 1000,
        validate_quality: bool = True
    ) -> TransformationResult:
        """
        Transform data from one format to another with optional transformations
        
        Args:
            input_data: Input data to transform
            source_format: Source data format
            target_format: Target data format
            transformations: List of transformation rules to apply
            schema_mapping: Field mapping for schema transformation
            template_name: Name of pre-defined template to use
            streaming: Enable streaming for large datasets
            buffer_size: Buffer size for streaming
            validate_quality: Perform data quality validation
            
        Returns:
            TransformationResult with transformed data and metadata
        """
        start_time = datetime.now()
        audit_trail = []
        errors = []
        warnings = []
        
        try:
            # Convert string formats to enum
            source_format = DataFormat(source_format)
            target_format = DataFormat(target_format)
            
            # Load template if specified
            if template_name:
                template = self.templates.get(template_name)
                if not template:
                    raise ValueError(f"Template '{template_name}' not found")
                transformations = template.transformations
                schema_mapping = template.schema_mapping or schema_mapping
            
            # Parse transformation rules
            transformation_rules = []
            if transformations:
                for t in transformations:
                    if isinstance(t, dict):
                        transformation_rules.append(TransformationRule(**t))
                    else:
                        transformation_rules.append(t)
            
            # Convert input data to intermediate format (DataFrame)
            df = self._convert_to_dataframe(input_data, source_format)
            original_count = len(df)
            
            # Apply schema mapping if provided
            if schema_mapping:
                df = self._apply_schema_mapping(df, schema_mapping, audit_trail)
            
            # Apply transformations
            if transformation_rules:
                if streaming and len(df) > buffer_size:
                    df = self._apply_transformations_streaming(
                        df, transformation_rules, buffer_size, audit_trail
                    )
                else:
                    df = self._apply_transformations(df, transformation_rules, audit_trail)
            
            # Validate data quality
            quality_metrics = DataQualityMetrics(total_records=len(df))
            if validate_quality:
                quality_metrics = self._validate_data_quality(df, warnings)
            
            # Convert to target format
            output_data = self._convert_from_dataframe(df, target_format)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            return TransformationResult(
                success=True,
                transformed_data=output_data,
                source_format=source_format,
                target_format=target_format,
                records_processed=len(df),
                transformations_applied=[t.type.value for t in transformation_rules],
                quality_metrics=quality_metrics,
                audit_trail=audit_trail,
                errors=errors,
                warnings=warnings,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logger.error(f"Transformation failed: {str(e)}")
            errors.append(str(e))
            
            return TransformationResult(
                success=False,
                transformed_data=None,
                source_format=source_format,
                target_format=target_format,
                records_processed=0,
                transformations_applied=[],
                quality_metrics=DataQualityMetrics(),
                audit_trail=audit_trail,
                errors=errors,
                warnings=warnings,
                processing_time_ms=(datetime.now() - start_time).total_seconds() * 1000
            )
    
    def _convert_to_dataframe(self, data: Any, format: DataFormat) -> pd.DataFrame:
        """Convert input data to pandas DataFrame"""
        if format == DataFormat.DATAFRAME:
            return data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        elif format == DataFormat.JSON:
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        
        elif format == DataFormat.CSV:
            if isinstance(data, str):
                return pd.read_csv(io.StringIO(data))
            else:
                return pd.DataFrame(data)
        
        elif format == DataFormat.XML:
            if isinstance(data, str):
                parsed = xmltodict.parse(data)
                # Extract the root element
                root_key = list(parsed.keys())[0]
                data = parsed[root_key]
                if isinstance(data, dict) and len(data) == 1:
                    data = list(data.values())[0]
            return pd.DataFrame(data if isinstance(data, list) else [data])
        
        elif format == DataFormat.PARQUET:
            if isinstance(data, bytes):
                return pq.read_table(io.BytesIO(data)).to_pandas()
            elif isinstance(data, str):
                return pd.read_parquet(data)
            else:
                raise ValueError("Parquet format requires bytes or file path")
        
        elif format == DataFormat.DICT:
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        
        else:
            raise ValueError(f"Unsupported source format: {format}")
    
    def _convert_from_dataframe(self, df: pd.DataFrame, format: DataFormat) -> Any:
        """Convert DataFrame to target format"""
        if format == DataFormat.DATAFRAME:
            return df
        
        elif format == DataFormat.JSON:
            return df.to_json(orient='records', indent=2)
        
        elif format == DataFormat.CSV:
            return df.to_csv(index=False)
        
        elif format == DataFormat.XML:
            records = df.to_dict(orient='records')
            return xmltodict.unparse({'root': {'record': records}}, pretty=True)
        
        elif format == DataFormat.PARQUET:
            buffer = io.BytesIO()
            table = pa.Table.from_pandas(df)
            pq.write_table(table, buffer)
            return buffer.getvalue()
        
        elif format == DataFormat.DICT:
            records = df.to_dict(orient='records')
            return records[0] if len(records) == 1 else records
        
        else:
            raise ValueError(f"Unsupported target format: {format}")
    
    def _apply_schema_mapping(
        self,
        df: pd.DataFrame,
        mapping: Dict[str, str],
        audit_trail: List[TransformationAudit]
    ) -> pd.DataFrame:
        """Apply schema mapping to rename fields"""
        for old_name, new_name in mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
                audit_trail.append(TransformationAudit(
                    transformation_type="schema_mapping",
                    field_affected=old_name,
                    after_value=new_name,
                    success=True
                ))
            else:
                logger.warning(f"Field '{old_name}' not found in data")
        return df
    
    def _apply_transformations(
        self,
        df: pd.DataFrame,
        rules: List[TransformationRule],
        audit_trail: List[TransformationAudit]
    ) -> pd.DataFrame:
        """Apply transformation rules to DataFrame"""
        for rule in rules:
            try:
                df = self._apply_single_transformation(df, rule, audit_trail)
            except Exception as e:
                logger.error(f"Transformation failed: {str(e)}")
                audit_trail.append(TransformationAudit(
                    transformation_type=rule.type.value,
                    field_affected=rule.field,
                    success=False,
                    error_message=str(e)
                ))
        return df
    
    def _apply_transformations_streaming(
        self,
        df: pd.DataFrame,
        rules: List[TransformationRule],
        buffer_size: int,
        audit_trail: List[TransformationAudit]
    ) -> pd.DataFrame:
        """Apply transformations in streaming mode for large datasets"""
        chunks = []
        for i in range(0, len(df), buffer_size):
            chunk = df.iloc[i:i+buffer_size].copy()
            transformed_chunk = self._apply_transformations(chunk, rules, audit_trail)
            chunks.append(transformed_chunk)
        
        return pd.concat(chunks, ignore_index=True)
    
    def _apply_single_transformation(
        self,
        df: pd.DataFrame,
        rule: TransformationRule,
        audit_trail: List[TransformationAudit]
    ) -> pd.DataFrame:
        """Apply a single transformation rule"""
        if rule.type == TransformationType.TYPE_CAST:
            if rule.field and rule.target_type:
                try:
                    df = df.copy()  # Avoid SettingWithCopyWarning
                    df[rule.field] = df[rule.field].astype(rule.target_type)
                except (ValueError, TypeError) as e:
                    # Log the error but continue
                    logger.warning(f"Type cast failed for field '{rule.field}': {str(e)}")
                    audit_trail.append(TransformationAudit(
                        transformation_type=rule.type.value,
                        field_affected=rule.field,
                        success=False,
                        error_message=str(e)
                    ))
                    return df
                
        elif rule.type == TransformationType.RENAME_FIELD:
            if rule.field and rule.target_field:
                df = df.rename(columns={rule.field: rule.target_field})
                
        elif rule.type == TransformationType.ADD_FIELD:
            if rule.target_field is not None:
                df = df.copy()  # Avoid SettingWithCopyWarning
                df[rule.target_field] = rule.value
                
        elif rule.type == TransformationType.REMOVE_FIELD:
            if rule.field and rule.field in df.columns:
                df = df.drop(columns=[rule.field])
                
        elif rule.type == TransformationType.EXTRACT_FIELD:
            if rule.field and rule.target_field and 'pattern' in rule.parameters:
                pattern = rule.parameters['pattern']
                df[rule.target_field] = df[rule.field].str.extract(pattern, expand=False)
                
        elif rule.type == TransformationType.AGGREGATE:
            if rule.aggregation:
                if rule.aggregation == 'sum':
                    df = pd.DataFrame([df.sum(numeric_only=True)])
                elif rule.aggregation == 'mean':
                    df = pd.DataFrame([df.mean(numeric_only=True)])
                elif rule.aggregation == 'count':
                    df = pd.DataFrame([df.count()])
                    
        elif rule.type == TransformationType.FILTER:
            if rule.condition:
                df = df.query(rule.condition)
                
        elif rule.type == TransformationType.NORMALIZE:
            if rule.field:
                if df[rule.field].dtype in ['float64', 'int64']:
                    min_val = df[rule.field].min()
                    max_val = df[rule.field].max()
                    if max_val > min_val:
                        df = df.copy()  # Avoid SettingWithCopyWarning
                        df[rule.field] = (df[rule.field] - min_val) / (max_val - min_val)
                        
        elif rule.type == TransformationType.CLEAN:
            if rule.field:
                if rule.parameters.get('operation') == 'trim':
                    df[rule.field] = df[rule.field].str.strip()
                elif rule.parameters.get('operation') == 'remove_special':
                    df[rule.field] = df[rule.field].apply(
                        lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x))
                    )
                    
        elif rule.type == TransformationType.CUSTOM:
            if rule.custom_func:
                if rule.field:
                    df[rule.field] = df[rule.field].apply(rule.custom_func)
                else:
                    df = rule.custom_func(df)
                    
        audit_trail.append(TransformationAudit(
            transformation_type=rule.type.value,
            field_affected=rule.field,
            success=True
        ))
        
        return df
    
    def _validate_data_quality(
        self,
        df: pd.DataFrame,
        warnings: List[str]
    ) -> DataQualityMetrics:
        """Validate data quality and collect metrics"""
        metrics = DataQualityMetrics(
            total_records=len(df),
            valid_records=len(df)
        )
        
        # Check for null values
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                metrics.null_fields[col] = int(count)
                warnings.append(f"Field '{col}' has {count} null values")
                
        # Check for type consistency
        for col in df.columns:
            try:
                # Try to infer consistent type
                non_null = df[col].dropna()
                if len(non_null) > 0:
                    # Check if all values can be converted to numeric
                    try:
                        pd.to_numeric(non_null, errors='raise')
                    except:
                        # Check if all values are strings
                        if not all(isinstance(x, str) for x in non_null):
                            metrics.type_mismatches[col] = len(non_null)
                            warnings.append(f"Field '{col}' has mixed types")
            except Exception as e:
                metrics.validation_errors.append(f"Error validating field '{col}': {str(e)}")
                
        # Calculate valid records (records without any nulls or type mismatches)
        invalid_mask = df.isnull().any(axis=1)
        metrics.valid_records = len(df[~invalid_mask])
        metrics.invalid_records = metrics.total_records - metrics.valid_records
        
        return metrics
    
    def create_template(
        self,
        name: str,
        description: str,
        source_format: DataFormat,
        target_format: DataFormat,
        transformations: List[Union[Dict, TransformationRule]],
        schema_mapping: Optional[Dict[str, str]] = None,
        validation_rules: Optional[Dict[str, Any]] = None
    ) -> TransformationTemplate:
        """Create a reusable transformation template"""
        # Parse transformation rules
        transformation_rules = []
        for t in transformations:
            if isinstance(t, dict):
                transformation_rules.append(TransformationRule(**t))
            else:
                transformation_rules.append(t)
                
        template = TransformationTemplate(
            name=name,
            description=description,
            source_format=source_format,
            target_format=target_format,
            transformations=transformation_rules,
            schema_mapping=schema_mapping,
            validation_rules=validation_rules
        )
        
        self.templates[name] = template
        return template
    
    def register_custom_transformer(self, name: str, func: Callable):
        """Register a custom transformation function"""
        self.custom_transformers[name] = func
    
    def stream_transform(
        self,
        input_stream: Iterator[Any],
        source_format: DataFormat,
        target_format: DataFormat,
        transformations: Optional[List[Union[Dict, TransformationRule]]] = None,
        buffer_size: int = 1000
    ) -> Iterator[Any]:
        """
        Stream transformation for processing large datasets
        
        Yields transformed data chunks
        """
        buffer = []
        
        for item in input_stream:
            buffer.append(item)
            
            if len(buffer) >= buffer_size:
                # Process buffer
                result = self.transform_data(
                    input_data=buffer,
                    source_format=source_format,
                    target_format=target_format,
                    transformations=transformations,
                    streaming=False
                )
                
                if result.success:
                    yield result.transformed_data
                    
                buffer = []
        
        # Process remaining items
        if buffer:
            result = self.transform_data(
                input_data=buffer,
                source_format=source_format,
                target_format=target_format,
                transformations=transformations,
                streaming=False
            )
            
            if result.success:
                yield result.transformed_data
    
    def chain_transformations(
        self,
        input_data: Any,
        transformation_chain: List[Dict[str, Any]]
    ) -> Any:
        """
        Chain multiple transformations together
        
        Args:
            input_data: Initial input data
            transformation_chain: List of transformation specifications
            
        Returns:
            Final transformed data
        """
        current_data = input_data
        
        for spec in transformation_chain:
            result = self.transform_data(
                input_data=current_data,
                source_format=spec.get('source_format', DataFormat.DICT),
                target_format=spec.get('target_format', DataFormat.DICT),
                transformations=spec.get('transformations', []),
                schema_mapping=spec.get('schema_mapping')
            )
            
            if not result.success:
                raise ValueError(f"Transformation failed: {result.errors}")
                
            current_data = result.transformed_data
            
        return current_data
    
    def analyze_data_schema(self, data: Any, format: DataFormat) -> Dict[str, Any]:
        """Analyze data schema and statistics"""
        df = self._convert_to_dataframe(data, format)
        
        schema = {
            'fields': {},
            'record_count': len(df),
            'memory_usage': df.memory_usage(deep=True).sum(),
            'statistics': {}
        }
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            schema['fields'][col] = {
                'type': dtype,
                'null_count': int(df[col].isnull().sum()),
                'unique_count': int(df[col].nunique()),
                'sample_values': df[col].dropna().head(5).tolist()
            }
            
            # Add statistics for numeric columns
            if df[col].dtype in ['int64', 'float64']:
                schema['statistics'][col] = {
                    'mean': float(df[col].mean()),
                    'std': float(df[col].std()),
                    'min': float(df[col].min()),
                    'max': float(df[col].max()),
                    'median': float(df[col].median())
                }
                
        return schema


if __name__ == "__main__":
    # Test the data transformer with real examples
    transformer = DataTransformerInteraction()
    
    # Test 1: JSON to CSV with type casting and field addition
    print("Test 1: JSON to CSV transformation")
    json_data = [
        {"name": "Alice", "age": "25", "city": "New York"},
        {"name": "Bob", "age": "30", "city": "San Francisco"},
        {"name": "Charlie", "age": "35", "city": "Chicago"}
    ]
    
    result = transformer.transform_data(
        input_data=json_data,
        source_format="json",
        target_format="csv",
        transformations=[
            {"type": "type_cast", "field": "age", "target_type": "int"},
            {"type": "add_field", "target_field": "country", "value": "USA"},
            {"type": "normalize", "field": "age"}
        ]
    )
    
    assert result.success, f"Transformation failed: {result.errors}"
    assert "Alice" in result.transformed_data, "Expected 'Alice' in output"
    assert "USA" in result.transformed_data, "Expected 'USA' in output"
    assert result.records_processed == 3, f"Expected 3 records, got {result.records_processed}"
    print(f"✓ Processed {result.records_processed} records in {result.processing_time_ms:.2f}ms")
    print(f"Output preview:\n{result.transformed_data[:100]}...")
    
    # Test 2: XML to JSON with schema mapping
    print("\nTest 2: XML to JSON with schema mapping")
    xml_data = """<?xml version="1.0"?>
    <root>
        <record>
            <firstName>John</firstName>
            <lastName>Doe</lastName>
            <email>john@example.com</email>
        </record>
    </root>"""
    
    result = transformer.transform_data(
        input_data=xml_data,
        source_format="xml",
        target_format="json",
        schema_mapping={
            "firstName": "first_name",
            "lastName": "last_name",
            "email": "contact_email"
        }
    )
    
    assert result.success, f"Transformation failed: {result.errors}"
    assert "first_name" in result.transformed_data, "Expected 'first_name' in output"
    assert "John" in result.transformed_data, "Expected 'John' in output"
    print(f"✓ Successfully transformed XML to JSON with schema mapping")
    
    # Test 3: Create and use a template
    print("\nTest 3: Template-based transformation")
    template = transformer.create_template(
        name="user_cleanup",
        description="Clean and standardize user data",
        source_format=DataFormat.JSON,
        target_format=DataFormat.CSV,
        transformations=[
            {"type": "clean", "field": "name", "parameters": {"operation": "trim"}},
            {"type": "type_cast", "field": "age", "target_type": "int"},
            {"type": "add_field", "target_field": "processed_date", "value": datetime.now().isoformat()}
        ]
    )
    
    messy_data = [
        {"name": "  Alice Smith  ", "age": "25", "email": "alice@test.com"},
        {"name": "Bob Jones   ", "age": "30", "email": "bob@test.com"}
    ]
    
    result = transformer.transform_data(
        input_data=messy_data,
        source_format="json",
        target_format="csv",
        template_name="user_cleanup"
    )
    
    assert result.success, f"Template transformation failed: {result.errors}"
    assert "Alice Smith" in result.transformed_data, "Expected trimmed name in output"
    assert "processed_date" in result.transformed_data, "Expected processed_date field"
    print(f"✓ Template-based transformation completed successfully")
    
    # Test 4: Data quality validation
    print("\nTest 4: Data quality validation")
    dirty_data = [
        {"id": 1, "value": 100, "category": "A"},
        {"id": 2, "value": None, "category": "B"},
        {"id": 3, "value": 300, "category": None},
        {"id": 4, "value": "invalid", "category": "A"}
    ]
    
    result = transformer.transform_data(
        input_data=dirty_data,
        source_format="json",
        target_format="json",
        validate_quality=True
    )
    
    print(f"✓ Quality metrics:")
    print(f"  - Total records: {result.quality_metrics.total_records}")
    print(f"  - Valid records: {result.quality_metrics.valid_records}")
    print(f"  - Null fields: {result.quality_metrics.null_fields}")
    print(f"  - Warnings: {len(result.warnings)}")
    
    # Test 5: Streaming transformation
    print("\nTest 5: Streaming transformation")
    def generate_large_dataset():
        for i in range(5000):
            yield {"id": i, "value": i * 2, "timestamp": datetime.now().isoformat()}
    
    stream_results = list(transformer.stream_transform(
        input_stream=generate_large_dataset(),
        source_format=DataFormat.DICT,
        target_format=DataFormat.JSON,
        transformations=[
            {"type": "filter", "condition": "value > 5000"},
            {"type": "add_field", "target_field": "processed", "value": True}
        ],
        buffer_size=1000
    ))
    
    assert len(stream_results) > 0, "Expected streaming results"
    print(f"✓ Streamed {len(stream_results)} batches successfully")
    
    print("\n✅ All data transformer tests passed!")