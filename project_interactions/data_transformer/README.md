# Data Transformation Engine

A flexible and powerful data transformation engine that handles format conversion, schema mapping, data cleaning, and custom transformations with streaming support for large datasets.

## Features

### Format Conversion
- **Supported Formats**: JSON, CSV, XML, Parquet, DataFrame, Dictionary
- **Bidirectional Conversion**: Convert between any supported formats
- **Automatic Type Detection**: Intelligently handles different data structures
- **Preserves Data Integrity**: Maintains data types and relationships during conversion

### Schema Mapping & Transformation
- **Field Renaming**: Map old field names to new ones
- **Type Casting**: Convert data types (string to int, float, bool, etc.)
- **Field Extraction**: Extract data using regex patterns
- **Field Addition/Removal**: Add new fields or remove existing ones
- **Complex Transformations**: Chain multiple operations together

### Data Cleaning & Normalization
- **String Cleaning**: Trim whitespace, remove special characters
- **Data Normalization**: Scale numeric values to 0-1 range
- **Custom Cleaning Functions**: Register your own cleaning logic
- **Null Value Handling**: Track and manage missing data
- **Data Validation**: Comprehensive quality metrics

### Advanced Features
- **Streaming Support**: Process large datasets in chunks
- **Transformation Templates**: Create reusable transformation pipelines
- **Audit Trail**: Complete history of all transformations
- **Error Recovery**: Graceful handling of transformation errors
- **Performance Optimization**: Efficient processing with minimal memory usage

## Usage Examples

### Basic Format Conversion
```python
from data_transformer_interaction import DataTransformerInteraction, DataFormat

transformer = DataTransformerInteraction()

# Convert JSON to CSV
json_data = [
    {"name": "John", "age": 30, "city": "NYC"},
    {"name": "Jane", "age": 25, "city": "LA"}
]

result = transformer.transform_data(
    input_data=json_data,
    source_format=DataFormat.JSON,
    target_format=DataFormat.CSV
)

print(result.transformed_data)
# Output: name,age,city\nJohn,30,NYC\nJane,25,LA\n
```

### Schema Mapping
```python
# Map old field names to new ones
schema_mapping = {
    "firstName": "first_name",
    "lastName": "last_name",
    "emailAddress": "email"
}

result = transformer.transform_data(
    input_data=old_data,
    source_format=DataFormat.JSON,
    target_format=DataFormat.JSON,
    schema_mapping=schema_mapping
)
```

### Data Cleaning
```python
# Clean messy data
transformations = [
    {"type": "clean", "field": "name", "parameters": {"operation": "trim"}},
    {"type": "type_cast", "field": "age", "target_type": "int"},
    {"type": "normalize", "field": "score"},
    {"type": "filter", "condition": "age > 18"}
]

result = transformer.transform_data(
    input_data=dirty_data,
    source_format=DataFormat.JSON,
    target_format=DataFormat.CSV,
    transformations=transformations,
    validate_quality=True
)

# Check quality metrics
print(f"Valid records: {result.quality_metrics.valid_records}")
print(f"Null fields: {result.quality_metrics.null_fields}")
```

### Streaming Large Datasets
```python
# Process large datasets in chunks
def generate_large_dataset():
    for i in range(1000000):
        yield {"id": i, "value": i * 2}

# Stream transform with buffer
for batch in transformer.stream_transform(
    input_stream=generate_large_dataset(),
    source_format=DataFormat.DICT,
    target_format=DataFormat.JSON,
    transformations=[{"type": "filter", "condition": "value > 1000"}],
    buffer_size=5000
):
    process_batch(batch)
```

### Creating Reusable Templates
```python
# Create a template for customer data processing
template = transformer.create_template(
    name="customer_cleanup",
    description="Standard customer data processing",
    source_format=DataFormat.JSON,
    target_format=DataFormat.CSV,
    transformations=[
        {"type": "clean", "field": "email", "parameters": {"operation": "trim"}},
        {"type": "type_cast", "field": "age", "target_type": "int"},
        {"type": "add_field", "target_field": "processed_date", "value": datetime.now()}
    ]
)

# Use the template
result = transformer.transform_data(
    input_data=customer_data,
    source_format=DataFormat.JSON,
    target_format=DataFormat.CSV,
    template_name="customer_cleanup"
)
```

## Transformation Types

| Type | Description | Parameters |
|------|-------------|------------|
| `type_cast` | Convert field to different type | `field`, `target_type` |
| `rename_field` | Rename a field | `field`, `target_field` |
| `add_field` | Add new field with value | `target_field`, `value` |
| `remove_field` | Remove a field | `field` |
| `extract_field` | Extract data using regex | `field`, `target_field`, `pattern` |
| `aggregate` | Aggregate data (sum, mean, count) | `aggregation` |
| `filter` | Filter records by condition | `condition` |
| `normalize` | Normalize numeric values to 0-1 | `field` |
| `clean` | Clean string data | `field`, `operation` |
| `custom` | Apply custom function | `field`, `custom_func` |

## Quality Metrics

The transformer provides comprehensive quality metrics:
- Total records processed
- Valid vs invalid record counts
- Null field tracking
- Type mismatch detection
- Validation errors and warnings

## Performance Considerations

- Use streaming for datasets > 10,000 records
- Enable buffering for optimal memory usage
- Chain transformations to minimize passes over data
- Use templates for frequently repeated operations

## Integration with Other Modules

The Data Transformer can be integrated with:
- **ArXiv MCP Server**: Transform research paper metadata
- **Marker**: Prepare documents for PDF processing
- **ArangoDB**: Format data for graph storage
- **Log Analyzer**: Transform log formats
- **API Gateway**: Format conversion for API responses