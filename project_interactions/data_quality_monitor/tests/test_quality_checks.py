"""
Module: test_quality_checks.py
Purpose: Test data quality check functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pandas: https://pandas.pydata.org/docs/
- numpy: https://numpy.org/doc/stable/

Example Usage:
>>> pytest test_quality_checks.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_quality_monitor_interaction import DataQualityMonitor


class TestQualityChecks:
    """Test suite for data quality checks"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5, 5],  # Duplicate
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Eve'],
            'age': [25, 30, 35, 40, 45, 45],
            'email': ['alice@example.com', 'invalid', 'charlie@example.com', 
                     None, 'eve@example.com', 'eve@example.com'],
            'salary': [50000, 60000, 70000, 80000, 90000, 90000],
            'department': ['Sales', 'Engineering', None, 'Marketing', 'HR', 'HR']
        })
        
    @pytest.fixture
    def monitor(self):
        """Create monitor instance with test configuration"""
        config = {
            'expected_schema': {
                'id': 'int64',
                'name': 'object',
                'age': 'int64',
                'email': 'object',
                'salary': 'int64',
                'department': 'object'
            },
            'format_columns': {
                'email': 'email'
            },
            'constraints': {
                'age': {'min': 0, 'max': 120},
                'salary': {'min': 0},
                'id': {'unique': True}
            }
        }
        return DataQualityMonitor(config)
        
    def test_schema_validation(self, monitor, sample_data):
        """Test schema validation functionality"""
        results = monitor.validate_schema(sample_data)
        
        assert 'valid' in results
        assert 'issues' in results
        assert 'score' in results
        assert results['valid'] is True
        assert results['score'] == 100.0
        assert len(results['issues']) == 0
        
    def test_completeness_check(self, monitor, sample_data):
        """Test completeness checking"""
        results = monitor.check_completeness(sample_data)
        
        assert 'overall_completeness' in results
        assert 'missing_cells' in results
        assert 'column_completeness' in results
        assert results['missing_cells'] == 2  # email and department nulls
        assert results['overall_completeness'] < 100.0
        
    def test_duplicate_detection(self, monitor, sample_data):
        """Test duplicate detection"""
        results = monitor.detect_duplicates(sample_data)
        
        assert 'has_duplicates' in results
        assert 'duplicate_count' in results
        assert results['has_duplicates'] is True
        assert results['duplicate_count'] == 1  # One duplicate row
        
    def test_format_validation(self, monitor, sample_data):
        """Test format validation"""
        results = monitor.validate_formats(sample_data)
        
        assert 'format_issues' in results
        assert 'email' in results['format_issues']
        assert results['format_issues']['email']['invalid_count'] > 0
        
    def test_constraint_checking(self, monitor, sample_data):
        """Test constraint validation"""
        results = monitor.check_constraints(sample_data)
        
        assert 'violations' in results
        assert 'total_violations' in results
        
        # Should find duplicate ID violation
        id_violations = [v for v in results['violations'] if v['column'] == 'id']
        assert len(id_violations) > 0
        
    def test_comprehensive_quality_check(self, monitor, sample_data):
        """Test comprehensive quality check"""
        results = monitor.check_data_quality(sample_data)
        
        assert 'quality_score' in results
        assert 'quality_checks' in results
        assert 'alerts' in results
        assert results['quality_score'] > 0
        assert results['quality_score'] < 100  # Should not be perfect due to issues
        
    def test_quality_score_calculation(self, monitor):
        """Test quality score calculation"""
        quality_checks = {
            'schema': {'score': 100.0},
            'completeness': {'score': 90.0},
            'duplicates': {'score': 95.0},
            'anomalies': {'score': 98.0},
            'format': {'score': 85.0},
            'constraints': {'score': 92.0},
            'drift': {'score': 100.0}
        }
        
        score = monitor._calculate_quality_score(quality_checks)
        assert score > 0
        assert score <= 100
        assert 90 < score < 96  # Weighted average should be in this range
        
    def test_alert_generation(self, monitor):
        """Test alert generation"""
        results = {
            'quality_score': 75.0,
            'quality_checks': {
                'completeness': {'overall_completeness': 85.0},
                'anomalies': {'anomaly_rate': 8.0}
            }
        }
        
        alerts = monitor._generate_alerts(results)
        assert len(alerts) > 0
        
        # Should have quality score alert
        quality_alerts = [a for a in alerts if a['type'] == 'quality_score']
        assert len(quality_alerts) > 0
        
    def test_empty_dataframe(self, monitor):
        """Test handling of empty dataframe"""
        empty_df = pd.DataFrame()
        results = monitor.check_data_quality(empty_df)
        
        assert results['total_records'] == 0
        assert results['total_columns'] == 0
        
    def test_perfect_data(self, monitor):
        """Test with perfect quality data"""
        perfect_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['A', 'B', 'C', 'D', 'E'],
            'value': [10, 20, 30, 40, 50]
        })
        
        results = monitor.check_data_quality(perfect_data)
        assert results['quality_checks']['completeness']['overall_completeness'] == 100.0
        assert results['quality_checks']['duplicates']['has_duplicates'] is False


def run_quality_check_tests():
    """Run quality check tests and report results"""
    print("🧪 Running quality check tests...\n")
    
    # Create test instance
    test_instance = TestQualityChecks()
    
    # Create fixtures manually (not using pytest fixtures directly)
    # Monitor with test configuration
    config = {
        'expected_schema': {
            'id': 'int64',
            'name': 'object',
            'age': 'int64',
            'email': 'object',
            'salary': 'int64',
            'department': 'object'
        },
        'format_columns': {
            'email': 'email'
        },
        'constraints': {
            'age': {'min': 0, 'max': 120},
            'salary': {'min': 0},
            'id': {'unique': True}
        }
    }
    monitor = DataQualityMonitor(config)
    
    # Sample data
    sample_data = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 5],  # Duplicate
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Eve'],
        'age': [25, 30, 35, 40, 45, 45],
        'email': ['alice@example.com', 'invalid', 'charlie@example.com', 
                 None, 'eve@example.com', 'eve@example.com'],
        'salary': [50000, 60000, 70000, 80000, 90000, 90000],
        'department': ['Sales', 'Engineering', None, 'Marketing', 'HR', 'HR']
    })
    
    # Run tests
    test_results = []
    
    # Test 1: Schema validation
    try:
        test_instance.test_schema_validation(monitor, sample_data)
        test_results.append(('Schema Validation', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Schema Validation', 'Fail', f'❌ {str(e)}'))
        
    # Test 2: Completeness check
    try:
        test_instance.test_completeness_check(monitor, sample_data)
        test_results.append(('Completeness Check', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Completeness Check', 'Fail', f'❌ {str(e)}'))
        
    # Test 3: Duplicate detection
    try:
        test_instance.test_duplicate_detection(monitor, sample_data)
        test_results.append(('Duplicate Detection', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Duplicate Detection', 'Fail', f'❌ {str(e)}'))
        
    # Test 4: Format validation
    try:
        test_instance.test_format_validation(monitor, sample_data)
        test_results.append(('Format Validation', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Format Validation', 'Fail', f'❌ {str(e)}'))
        
    # Test 5: Constraint checking
    try:
        test_instance.test_constraint_checking(monitor, sample_data)
        test_results.append(('Constraint Checking', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Constraint Checking', 'Fail', f'❌ {str(e)}'))
        
    # Test 6: Comprehensive check
    try:
        test_instance.test_comprehensive_quality_check(monitor, sample_data)
        test_results.append(('Comprehensive Check', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Comprehensive Check', 'Fail', f'❌ {str(e)}'))
        
    # Test 7: Empty dataframe
    try:
        test_instance.test_empty_dataframe(monitor)
        test_results.append(('Empty DataFrame', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Empty DataFrame', 'Fail', f'❌ {str(e)}'))
        
    # Test 8: Perfect data
    try:
        test_instance.test_perfect_data(monitor)
        test_results.append(('Perfect Data', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Perfect Data', 'Fail', f'❌ {str(e)}'))
        
    # Display results
    print("📊 Test Results:")
    print("-" * 50)
    for test_name, status, icon in test_results:
        print(f"{test_name:<25} {status:<6} {icon}")
    print("-" * 50)
    
    # Summary
    passed = sum(1 for _, status, _ in test_results if status == 'Pass')
    total = len(test_results)
    print(f"\nSummary: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    # Run tests with real data
    success = run_quality_check_tests()
    
    # Validation
    assert success, "Not all tests passed"
    
    print("\n✅ Quality check tests validation passed")