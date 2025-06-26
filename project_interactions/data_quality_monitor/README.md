# Data Quality Monitoring System

A comprehensive data quality monitoring system that implements real-time quality checks, anomaly detection, and data profiling with multi-source ingestion capabilities.

## Features

### Data Quality Checks
- **Schema Validation**: Validates data types against expected schema
- **Completeness Checking**: Detects missing values and calculates completeness metrics
- **Duplicate Detection**: Identifies duplicate records with grouping
- **Anomaly Detection**: Statistical outlier detection using IQR and Z-score methods
- **Format Validation**: Validates data formats (email, date, phone, etc.)
- **Constraint Checking**: Validates business rules and data constraints
- **Data Drift Detection**: Monitors changes in data distribution over time

### Data Sources
- CSV files
- JSON files
- Parquet files
- Pandas DataFrames
- Python dictionaries
- SQLite databases

### Additional Features
- **Real-time Quality Metrics**: Live quality score calculation
- **Historical Trend Analysis**: Track quality metrics over time
- **Alert System**: Configurable thresholds with severity levels
- **Data Profiling**: Comprehensive statistical summaries
- **Custom Rule Engine**: Add domain-specific quality rules
- **Report Generation**: Markdown and HTML report formats

## Installation

```bash
# Install dependencies
uv add pandas numpy scipy loguru pyarrow
```

## Usage

```python
from data_quality_monitor_interaction import DataQualityMonitor

# Create monitor with configuration
monitor = DataQualityMonitor({
    'alert_thresholds': {
        'quality_score': 85.0,
        'completeness': 95.0,
        'anomaly_rate': 3.0
    }
})

# Check data quality
results = monitor.check_data_quality('data.csv')

# Generate report
report = monitor.generate_quality_report(results, format='markdown')
```

## Configuration

```python
config = {
    'expected_schema': {
        'column_name': 'expected_dtype'
    },
    'format_columns': {
        'email_col': 'email',
        'date_col': 'date'
    },
    'constraints': {
        'age': {'min': 0, 'max': 150},
        'id': {'unique': True}
    },
    'alert_thresholds': {
        'quality_score': 80.0,
        'completeness': 90.0,
        'anomaly_rate': 5.0
    }
}
```

## Custom Rules

```python
def custom_rule(df: pd.DataFrame) -> dict:
    """Custom quality check"""
    # Implement custom logic
    violations = 0
    # ... check logic ...
    return {
        'violations': violations,
        'score': 100.0 * (1 - violations / len(df))
    }

monitor.add_custom_rule('custom_check', custom_rule, 'Description')
```

## Testing

Run the test suite:

```bash
# Run verification script
python test_task_34.py

# Run individual test files
python tests/test_quality_checks.py
python tests/test_anomaly_detection.py
python tests/test_data_profiling.py
```

## Architecture

The system follows a modular architecture:

1. **DataQualityMonitor**: Main orchestrator class
2. **Quality Checks**: Individual check methods (schema, completeness, etc.)
3. **Alert System**: Threshold-based alert generation
4. **Report Generator**: Multiple format support
5. **Historical Tracking**: Trend analysis capabilities

## Performance Considerations

- Uses vectorized operations for efficiency
- Supports batch processing for large datasets
- Configurable sampling for very large files
- Memory-efficient profiling

## License

MIT License