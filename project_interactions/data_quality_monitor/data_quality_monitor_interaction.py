
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: data_quality_monitor_interaction.py
Purpose: Comprehensive data quality monitoring system with real-time checks and anomaly detection

External Dependencies:
- pandas: https://pandas.pydata.org/docs/
- numpy: https://numpy.org/doc/stable/
- scipy: https://docs.scipy.org/doc/scipy/
- loguru: https://loguru.readthedocs.io/

Example Usage:
>>> from data_quality_monitor_interaction import DataQualityMonitor
>>> monitor = DataQualityMonitor()
>>> results = monitor.check_data_quality({'values': [1, 2, 3, 4, 5]})
>>> print(f"Quality score: {results['quality_score']}")
Quality score: 100.0
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats


class DataQualityMonitor:
    """Comprehensive data quality monitoring system"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize data quality monitor with configuration"""
        self.config = config or self._default_config()
        self.quality_rules = {}
        self.historical_metrics = []
        self.alert_thresholds = self.config.get('alert_thresholds', {})
        self._setup_logging()
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for data quality monitoring"""
        return {
            'completeness_threshold': 0.95,
            'anomaly_detection': {
                'method': 'isolation_forest',
                'contamination': 0.1
            },
            'drift_detection': {
                'method': 'kolmogorov_smirnov',
                'threshold': 0.05
            },
            'alert_thresholds': {
                'quality_score': 80.0,
                'completeness': 90.0,
                'anomaly_rate': 5.0
            },
            'formats': {
                'date': r'^\d{4}-\d{2}-\d{2}$',
                'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'phone': r'^\+?\d{10,15}$'
            }
        }
        
    def _setup_logging(self):
        """Configure logging for data quality monitoring"""
        logger.remove()
        logger.add(
            "logs/data_quality_{time}.log",
            rotation="1 day",
            retention="7 days",
            level="INFO",
            format="{time} | {level} | {message}"
        )
        
    def ingest_data(self, source: Union[str, pd.DataFrame, Dict], 
                   source_type: Optional[str] = None) -> pd.DataFrame:
        """Ingest data from various sources"""
        logger.info(f"Ingesting data from source type: {source_type}")
        
        if isinstance(source, pd.DataFrame):
            return source
            
        if source_type == 'csv' or (isinstance(source, str) and source.endswith('.csv')):
            return pd.read_csv(source)
        elif source_type == 'json' or (isinstance(source, str) and source.endswith('.json')):
            with open(source, 'r') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        elif source_type == 'parquet' or (isinstance(source, str) and source.endswith('.parquet')):
            return pd.read_parquet(source)
        elif source_type == 'database':
            conn = sqlite3.connect(source)
            query = "SELECT * FROM data_table"  # Customize as needed
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        elif isinstance(source, dict):
            return pd.DataFrame(source)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
            
    def check_data_quality(self, data: Union[pd.DataFrame, Dict, str],
                          source_type: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive data quality checks"""
        logger.info("Starting comprehensive data quality check")
        
        # Ingest data if needed
        if not isinstance(data, pd.DataFrame):
            df = self.ingest_data(data, source_type)
        else:
            df = data
            
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'total_columns': len(df.columns),
            'quality_checks': {},
            'alerts': []
        }
        
        # Run all quality checks
        results['quality_checks']['schema'] = self.validate_schema(df)
        results['quality_checks']['completeness'] = self.check_completeness(df)
        results['quality_checks']['duplicates'] = self.detect_duplicates(df)
        results['quality_checks']['anomalies'] = self.detect_anomalies(df)
        results['quality_checks']['format'] = self.validate_formats(df)
        results['quality_checks']['constraints'] = self.check_constraints(df)
        results['quality_checks']['drift'] = self.detect_data_drift(df)
        
        # Calculate overall quality score
        results['quality_score'] = self._calculate_quality_score(results['quality_checks'])
        
        # Generate alerts
        results['alerts'] = self._generate_alerts(results)
        
        # Store historical metrics
        self.historical_metrics.append(results)
        
        logger.info(f"Data quality check completed. Score: {results['quality_score']:.2f}")
        return results
        
    def validate_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data schema against expected types"""
        logger.debug("Validating data schema")
        
        schema_issues = []
        expected_types = self.config.get('expected_schema', {})
        
        for column in df.columns:
            actual_type = str(df[column].dtype)
            if column in expected_types:
                expected = expected_types[column]
                if actual_type != expected:
                    schema_issues.append({
                        'column': column,
                        'expected': expected,
                        'actual': actual_type
                    })
                    
        return {
            'valid': len(schema_issues) == 0,
            'issues': schema_issues,
            'score': 100.0 if not schema_issues else 
                    100.0 * (1 - len(schema_issues) / len(expected_types))
        }
        
    def check_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data completeness and missing values"""
        logger.debug("Checking data completeness")
        
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        completeness_ratio = 1 - (missing_cells / total_cells) if total_cells > 0 else 0
        
        column_completeness = {}
        for column in df.columns:
            missing = df[column].isnull().sum()
            total = len(df)
            column_completeness[column] = {
                'missing_count': int(missing),
                'missing_percentage': (missing / total * 100) if total > 0 else 0,
                'completeness': ((total - missing) / total * 100) if total > 0 else 0
            }
            
        return {
            'overall_completeness': completeness_ratio * 100,
            'missing_cells': int(missing_cells),
            'total_cells': int(total_cells),
            'column_completeness': column_completeness,
            'score': completeness_ratio * 100
        }
        
    def detect_duplicates(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect duplicate records in the data"""
        logger.debug("Detecting duplicate records")
        
        duplicates = df.duplicated()
        duplicate_count = duplicates.sum()
        
        # Find duplicate groups
        duplicate_groups = []
        if duplicate_count > 0:
            for idx, row in df[duplicates].iterrows():
                matching_rows = df[(df == row).all(axis=1)]
                duplicate_groups.append({
                    'indices': matching_rows.index.tolist(),
                    'count': len(matching_rows)
                })
                
        return {
            'has_duplicates': duplicate_count > 0,
            'duplicate_count': int(duplicate_count),
            'duplicate_percentage': (duplicate_count / len(df) * 100) if len(df) > 0 else 0,
            'duplicate_groups': duplicate_groups[:10],  # Limit to first 10 groups
            'score': 100.0 * (1 - duplicate_count / len(df)) if len(df) > 0 else 100.0
        }
        
    def detect_anomalies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect anomalies in numerical columns"""
        logger.debug("Detecting anomalies in data")
        
        anomalies = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            col_data = df[column].dropna()
            if len(col_data) < 10:  # Skip if too few values
                continue
                
            # Statistical outlier detection (IQR method)
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            # Z-score method
            z_scores = np.abs(stats.zscore(col_data))
            z_outliers = col_data[z_scores > 3]
            
            anomalies[column] = {
                'iqr_outliers': len(outliers),
                'iqr_outlier_percentage': (len(outliers) / len(col_data) * 100),
                'z_score_outliers': len(z_outliers),
                'bounds': {
                    'lower': float(lower_bound),
                    'upper': float(upper_bound)
                },
                'statistics': {
                    'mean': float(col_data.mean()),
                    'std': float(col_data.std()),
                    'min': float(col_data.min()),
                    'max': float(col_data.max())
                }
            }
            
        total_anomalies = sum(a['iqr_outliers'] for a in anomalies.values())
        total_numeric_values = sum(len(df[col].dropna()) for col in numeric_columns)
        
        return {
            'column_anomalies': anomalies,
            'total_anomalies': total_anomalies,
            'anomaly_rate': (total_anomalies / total_numeric_values * 100) 
                           if total_numeric_values > 0 else 0,
            'score': 100.0 * (1 - total_anomalies / total_numeric_values) 
                    if total_numeric_values > 0 else 100.0
        }
        
    def validate_formats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate data formats against expected patterns"""
        logger.debug("Validating data formats")
        
        format_issues = {}
        formats = self.config.get('formats', {})
        
        for column in df.columns:
            if column in self.config.get('format_columns', {}):
                format_type = self.config['format_columns'][column]
                if format_type in formats:
                    pattern = formats[format_type]
                    
                    # Check format for non-null string values
                    string_data = df[column].dropna().astype(str)
                    matches = string_data.str.match(pattern)
                    invalid_count = (~matches).sum()
                    
                    format_issues[column] = {
                        'format_type': format_type,
                        'invalid_count': int(invalid_count),
                        'invalid_percentage': (invalid_count / len(string_data) * 100) 
                                            if len(string_data) > 0 else 0,
                        'valid_percentage': (matches.sum() / len(string_data) * 100) 
                                          if len(string_data) > 0 else 100.0
                    }
                    
        total_format_checks = sum(1 for col in format_issues)
        valid_formats = sum(1 for col, issues in format_issues.items() 
                          if issues['invalid_count'] == 0)
        
        return {
            'format_issues': format_issues,
            'total_checks': total_format_checks,
            'valid_formats': valid_formats,
            'score': (valid_formats / total_format_checks * 100) 
                    if total_format_checks > 0 else 100.0
        }
        
    def check_constraints(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Check data constraints and business rules"""
        logger.debug("Checking data constraints")
        
        constraint_violations = []
        constraints = self.config.get('constraints', {})
        
        for column, rules in constraints.items():
            if column not in df.columns:
                continue
                
            col_data = df[column].dropna()
            
            # Range constraints
            if 'min' in rules:
                violations = col_data[col_data < rules['min']]
                if len(violations) > 0:
                    constraint_violations.append({
                        'column': column,
                        'rule': f"minimum value {rules['min']}",
                        'violations': len(violations),
                        'violation_rate': len(violations) / len(col_data) * 100
                    })
                    
            if 'max' in rules:
                violations = col_data[col_data > rules['max']]
                if len(violations) > 0:
                    constraint_violations.append({
                        'column': column,
                        'rule': f"maximum value {rules['max']}",
                        'violations': len(violations),
                        'violation_rate': len(violations) / len(col_data) * 100
                    })
                    
            # Unique constraint
            if rules.get('unique', False):
                duplicates = col_data.duplicated().sum()
                if duplicates > 0:
                    constraint_violations.append({
                        'column': column,
                        'rule': 'unique values',
                        'violations': int(duplicates),
                        'violation_rate': duplicates / len(col_data) * 100
                    })
                    
        return {
            'violations': constraint_violations,
            'total_violations': sum(v['violations'] for v in constraint_violations),
            'score': 100.0 if not constraint_violations else 
                    100.0 * (1 - len(constraint_violations) / len(constraints))
        }
        
    def detect_data_drift(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Detect data drift compared to historical data"""
        logger.debug("Detecting data drift")
        
        if len(self.historical_metrics) < 2:
            return {
                'drift_detected': False,
                'message': 'Insufficient historical data',
                'score': 100.0
            }
            
        drift_results = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        # Compare with last period's data
        for column in numeric_columns:
            current_data = df[column].dropna()
            
            # Statistical tests for drift
            if len(current_data) > 30:  # Need sufficient data
                # Kolmogorov-Smirnov test
                historical_mean = np.mean([m['quality_checks'].get('drift', {})
                                         .get('column_stats', {})
                                         .get(column, {})
                                         .get('mean', current_data.mean()) 
                                         for m in self.historical_metrics[-5:]])
                
                historical_std = np.mean([m['quality_checks'].get('drift', {})
                                        .get('column_stats', {})
                                        .get(column, {})
                                        .get('std', current_data.std()) 
                                        for m in self.historical_metrics[-5:]])
                
                # Simple drift detection based on mean/std shift
                mean_shift = abs(current_data.mean() - historical_mean) / historical_std \
                            if historical_std > 0 else 0
                
                drift_results[column] = {
                    'current_mean': float(current_data.mean()),
                    'historical_mean': float(historical_mean),
                    'mean_shift': float(mean_shift),
                    'drift_detected': mean_shift > 2.0  # 2 std deviations
                }
                
        total_columns = len(drift_results)
        drifted_columns = sum(1 for r in drift_results.values() if r['drift_detected'])
        
        return {
            'column_drift': drift_results,
            'total_columns_checked': total_columns,
            'drifted_columns': drifted_columns,
            'drift_rate': (drifted_columns / total_columns * 100) if total_columns > 0 else 0,
            'score': 100.0 * (1 - drifted_columns / total_columns) if total_columns > 0 else 100.0
        }
        
    def profile_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data profile"""
        logger.info("Generating data profile")
        
        profile = {
            'shape': {
                'rows': len(df),
                'columns': len(df.columns)
            },
            'memory_usage': df.memory_usage(deep=True).to_dict(),
            'column_types': df.dtypes.astype(str).to_dict(),
            'numeric_summary': {},
            'categorical_summary': {}
        }
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            profile['numeric_summary'][col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q25': float(df[col].quantile(0.25)),
                'q50': float(df[col].quantile(0.50)),
                'q75': float(df[col].quantile(0.75)),
                'null_count': int(df[col].isnull().sum()),
                'unique_count': int(df[col].nunique())
            }
            
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            profile['categorical_summary'][col] = {
                'unique_count': int(df[col].nunique()),
                'null_count': int(df[col].isnull().sum()),
                'top_values': value_counts.head(10).to_dict(),
                'mode': str(df[col].mode()[0]) if not df[col].mode().empty else None
            }
            
        return profile
        
    def add_custom_rule(self, rule_name: str, rule_function: callable, 
                       description: str = "") -> None:
        """Add custom quality rule"""
        logger.info(f"Adding custom rule: {rule_name}")
        
        self.quality_rules[rule_name] = {
            'function': rule_function,
            'description': description
        }
        
    def generate_quality_report(self, results: Dict[str, Any], 
                              format: str = 'markdown') -> str:
        """Generate quality report in specified format"""
        logger.info(f"Generating quality report in {format} format")
        
        if format == 'markdown':
            return self._generate_markdown_report(results)
        elif format == 'html':
            return self._generate_html_report(results)
        else:
            return json.dumps(results, indent=2)
            
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown format quality report"""
        report = f"""# Data Quality Report

**Generated:** {results['timestamp']}

## Summary
- **Total Records:** {results['total_records']:,}
- **Total Columns:** {results['total_columns']}
- **Overall Quality Score:** {results['quality_score']:.2f}%

## Quality Checks

### Schema Validation
- **Valid:** {'✅' if results['quality_checks']['schema']['valid'] else '❌'}
- **Score:** {results['quality_checks']['schema']['score']:.2f}%
- **Issues:** {len(results['quality_checks']['schema']['issues'])}

### Data Completeness
- **Overall Completeness:** {results['quality_checks']['completeness']['overall_completeness']:.2f}%
- **Missing Cells:** {results['quality_checks']['completeness']['missing_cells']:,}
- **Total Cells:** {results['quality_checks']['completeness']['total_cells']:,}

### Duplicate Detection
- **Has Duplicates:** {'Yes' if results['quality_checks']['duplicates']['has_duplicates'] else 'No'}
- **Duplicate Count:** {results['quality_checks']['duplicates']['duplicate_count']}
- **Duplicate Rate:** {results['quality_checks']['duplicates']['duplicate_percentage']:.2f}%

### Anomaly Detection
- **Total Anomalies:** {results['quality_checks']['anomalies']['total_anomalies']}
- **Anomaly Rate:** {results['quality_checks']['anomalies']['anomaly_rate']:.2f}%

### Data Drift
- **Drift Rate:** {results['quality_checks']['drift'].get('drift_rate', 0.0):.2f}%
- **Drifted Columns:** {results['quality_checks']['drift'].get('drifted_columns', 0)}

## Alerts
"""
        
        if results['alerts']:
            for alert in results['alerts']:
                report += f"- ⚠️ {alert['message']} (Severity: {alert['severity']})\n"
        else:
            report += "No alerts generated.\n"
            
        return report
        
    def _generate_html_report(self, results: Dict[str, Any]) -> str:
        """Generate HTML format quality report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Data Quality Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .metric {{ margin: 10px 0; }}
        .alert {{ color: #d9534f; font-weight: bold; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>Data Quality Report</h1>
    <div class="summary">
        <p><strong>Generated:</strong> {results['timestamp']}</p>
        <p><strong>Overall Quality Score:</strong> {results['quality_score']:.2f}%</p>
        <p><strong>Total Records:</strong> {results['total_records']:,}</p>
        <p><strong>Total Columns:</strong> {results['total_columns']}</p>
    </div>
"""
        
        # Add quality check details
        for check_name, check_results in results['quality_checks'].items():
            html += f"<h2>{check_name.title()}</h2>"
            html += f"<p>Score: {check_results.get('score', 'N/A'):.2f}%</p>"
            
        # Add alerts
        if results['alerts']:
            html += "<h2>Alerts</h2><ul>"
            for alert in results['alerts']:
                html += f"<li class='alert'>{alert['message']}</li>"
            html += "</ul>"
            
        html += "</body></html>"
        return html
        
    def _calculate_quality_score(self, quality_checks: Dict[str, Any]) -> float:
        """Calculate overall quality score from individual checks"""
        weights = {
            'schema': 0.20,
            'completeness': 0.25,
            'duplicates': 0.15,
            'anomalies': 0.15,
            'format': 0.10,
            'constraints': 0.10,
            'drift': 0.05
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for check, weight in weights.items():
            if check in quality_checks and 'score' in quality_checks[check]:
                total_score += quality_checks[check]['score'] * weight
                total_weight += weight
                
        return (total_score / total_weight) if total_weight > 0 else 0.0
        
    def _generate_alerts(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate alerts based on quality check results"""
        alerts = []
        
        # Quality score alert
        if results['quality_score'] < self.alert_thresholds.get('quality_score', 80):
            alerts.append({
                'type': 'quality_score',
                'severity': 'high',
                'message': f"Overall quality score ({results['quality_score']:.2f}%) "
                          f"below threshold ({self.alert_thresholds.get('quality_score', 80)}%)"
            })
            
        # Completeness alert
        completeness = results['quality_checks']['completeness']['overall_completeness']
        if completeness < self.alert_thresholds.get('completeness', 90):
            alerts.append({
                'type': 'completeness',
                'severity': 'medium',
                'message': f"Data completeness ({completeness:.2f}%) "
                          f"below threshold ({self.alert_thresholds.get('completeness', 90)}%)"
            })
            
        # Anomaly rate alert
        anomaly_rate = results['quality_checks']['anomalies']['anomaly_rate']
        if anomaly_rate > self.alert_thresholds.get('anomaly_rate', 5):
            alerts.append({
                'type': 'anomalies',
                'severity': 'medium',
                'message': f"Anomaly rate ({anomaly_rate:.2f}%) "
                          f"above threshold ({self.alert_thresholds.get('anomaly_rate', 5)}%)"
            })
            
        return alerts
        
    def get_historical_trends(self, metric: str, periods: int = 10) -> Dict[str, Any]:
        """Get historical trends for specific metrics"""
        if not self.historical_metrics:
            return {'error': 'No historical data available'}
            
        recent_metrics = self.historical_metrics[-periods:]
        
        trend_data = {
            'timestamps': [],
            'values': [],
            'metric': metric
        }
        
        for m in recent_metrics:
            trend_data['timestamps'].append(m['timestamp'])
            
            if metric == 'quality_score':
                trend_data['values'].append(m['quality_score'])
            elif metric in m['quality_checks']:
                trend_data['values'].append(m['quality_checks'][metric].get('score', 0))
                
        return trend_data


def demonstrate_data_quality_monitoring():
    """Demonstrate data quality monitoring capabilities"""
    logger.info("Starting data quality monitoring demonstration")
    
    # Create sample dataset with various quality issues
    np.random.seed(42)
    n_records = 1000
    
    # Generate data with intentional quality issues
    data = {
        'id': list(range(n_records)),
        'name': ['User ' + str(i) for i in range(n_records)],
        'age': list(np.random.normal(35, 15, n_records).astype(int)),
        'email': ['user{}@example.com'.format(i) if i % 20 != 0 else 'invalid_email' 
                  for i in range(n_records)],
        'salary': list(np.random.normal(50000, 20000, n_records)),
        'department': list(np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR', None], 
                                     n_records, p=[0.3, 0.3, 0.2, 0.15, 0.05])),
        'join_date': list(pd.date_range('2020-01-01', periods=n_records, freq='D').astype(str)),
        'status': list(np.random.choice(['Active', 'Inactive'], n_records, p=[0.9, 0.1]))
    }
    
    # Add some duplicates
    for i in range(10):
        idx = np.random.randint(0, n_records)
        data['id'].append(data['id'][idx])
        data['name'].append(data['name'][idx])
        data['age'].append(data['age'][idx])
        data['email'].append(data['email'][idx])
        data['salary'].append(data['salary'][idx])
        data['department'].append(data['department'][idx])
        data['join_date'].append(data['join_date'][idx])
        data['status'].append(data['status'][idx])
        
    # Create DataFrame first to add anomalies
    df = pd.DataFrame(data)
    
    # Add some anomalies
    df.loc[50:54, 'age'] = [150, 200, -10, 0, 999]
    df.loc[100:104, 'salary'] = [1000000, 2000000, -50000, 0, 999999]
    
    # Add missing values
    for i in range(50):
        df.loc[np.random.randint(0, len(df)), 'email'] = None
        df.loc[np.random.randint(0, len(df)), 'department'] = None
    
    # Configure monitor
    config = {
        'expected_schema': {
            'id': 'int64',
            'name': 'object',
            'age': 'int64',
            'email': 'object',
            'salary': 'float64',
            'department': 'object',
            'join_date': 'object',
            'status': 'object'
        },
        'format_columns': {
            'email': 'email',
            'join_date': 'date'
        },
        'constraints': {
            'age': {'min': 18, 'max': 100},
            'salary': {'min': 0, 'max': 500000},
            'id': {'unique': True}
        }
    }
    
    # Create monitor instance
    monitor = DataQualityMonitor(config)
    
    # Run quality checks
    print("\n🔍 Running comprehensive data quality checks...")
    results = monitor.check_data_quality(df)
    
    # Display results
    print(f"\n📊 Data Quality Summary:")
    print(f"   Total Records: {results['total_records']:,}")
    print(f"   Total Columns: {results['total_columns']}")
    print(f"   Overall Quality Score: {results['quality_score']:.2f}%")
    
    print(f"\n✅ Quality Check Results:")
    for check_name, check_results in results['quality_checks'].items():
        score = check_results.get('score', 'N/A')
        print(f"   {check_name.title()}: {score:.2f}%")
        
    # Show alerts
    if results['alerts']:
        print(f"\n⚠️  Alerts Generated:")
        for alert in results['alerts']:
            print(f"   - {alert['message']} (Severity: {alert['severity']})")
            
    # Generate data profile
    print("\n📈 Generating data profile...")
    profile = monitor.profile_data(df)
    print(f"   Numeric columns: {len(profile['numeric_summary'])}")
    print(f"   Categorical columns: {len(profile['categorical_summary'])}")
    
    # Generate report
    print("\n📄 Generating quality report...")
    report = monitor.generate_quality_report(results, format='markdown')
    report_path = Path('docs/reports/data_quality_report.md')
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)
    print(f"   Report saved to: {report_path}")
    
    # Test custom rule
    def check_business_rule(df: pd.DataFrame) -> Dict[str, Any]:
        """Custom business rule: Senior employees (age > 50) should have salary > 60000"""
        seniors = df[df['age'] > 50]
        violations = seniors[seniors['salary'] < 60000]
        return {
            'violations': len(violations),
            'total_seniors': len(seniors),
            'score': 100.0 * (1 - len(violations) / len(seniors)) if len(seniors) > 0 else 100.0
        }
        
    monitor.add_custom_rule('senior_salary_rule', check_business_rule,
                           'Senior employees should have higher salaries')
    
    # Test different data sources
    print("\n🔄 Testing data source ingestion...")
    
    # Save to different formats
    df.to_csv('temp_data.csv', index=False)
    df.to_json('temp_data.json', orient='records')
    df.to_parquet('temp_data.parquet', index=False)
    
    # Test CSV ingestion
    csv_results = monitor.check_data_quality('temp_data.csv', source_type='csv')
    print(f"   CSV Quality Score: {csv_results['quality_score']:.2f}%")
    
    # Test JSON ingestion
    json_results = monitor.check_data_quality('temp_data.json', source_type='json')
    print(f"   JSON Quality Score: {json_results['quality_score']:.2f}%")
    
    # Test Parquet ingestion
    parquet_results = monitor.check_data_quality('temp_data.parquet', source_type='parquet')
    print(f"   Parquet Quality Score: {parquet_results['quality_score']:.2f}%")
    
    # Clean up temp files
    Path('temp_data.csv').unlink(missing_ok=True)
    Path('temp_data.json').unlink(missing_ok=True)
    Path('temp_data.parquet').unlink(missing_ok=True)
    
    return results


if __name__ == "__main__":
    # Run demonstration with real data
    results = demonstrate_data_quality_monitoring()
    
    # Validation
    assert results is not None, "Results should not be None"
    assert 'quality_score' in results, "Results should contain quality_score"
    assert results['quality_score'] > 0, "Quality score should be positive"
    assert len(results['quality_checks']) == 7, "Should have 7 quality checks"
    assert all(check in results['quality_checks'] for check in 
              ['schema', 'completeness', 'duplicates', 'anomalies', 
               'format', 'constraints', 'drift']), "All checks should be present"
    
    print("\n✅ Module validation passed")