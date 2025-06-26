"""
Module: test_anomaly_detection.py
Purpose: Test anomaly detection functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pandas: https://pandas.pydata.org/docs/
- numpy: https://numpy.org/doc/stable/

Example Usage:
>>> pytest test_anomaly_detection.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_quality_monitor_interaction import DataQualityMonitor


class TestAnomalyDetection:
    """Test suite for anomaly detection functionality"""
    
    @pytest.fixture
    def normal_data(self):
        """Create normally distributed data"""
        np.random.seed(42)
        return pd.DataFrame({
            'value': np.random.normal(100, 10, 1000),
            'count': np.random.poisson(50, 1000),
            'ratio': np.random.uniform(0.4, 0.6, 1000)
        })
        
    @pytest.fixture
    def data_with_outliers(self):
        """Create data with intentional outliers"""
        np.random.seed(42)
        values = np.random.normal(100, 10, 1000)
        
        # Add outliers
        values[50:55] = [200, 250, -50, 300, 400]  # Extreme values
        values[100:103] = [150, 160, 170]  # Moderate outliers
        
        return pd.DataFrame({
            'value': values,
            'count': np.random.poisson(50, 1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000)
        })
        
    @pytest.fixture
    def monitor(self):
        """Create monitor instance"""
        return DataQualityMonitor()
        
    def test_anomaly_detection_normal_data(self, monitor, normal_data):
        """Test anomaly detection on normal data"""
        results = monitor.detect_anomalies(normal_data)
        
        assert 'column_anomalies' in results
        assert 'total_anomalies' in results
        assert 'anomaly_rate' in results
        
        # Should have low anomaly rate for normal data
        assert results['anomaly_rate'] < 5.0
        
    def test_anomaly_detection_with_outliers(self, monitor, data_with_outliers):
        """Test anomaly detection with outliers"""
        results = monitor.detect_anomalies(data_with_outliers)
        
        # Should detect anomalies in value column
        assert 'value' in results['column_anomalies']
        value_anomalies = results['column_anomalies']['value']
        
        assert value_anomalies['iqr_outliers'] > 0
        assert value_anomalies['z_score_outliers'] > 0
        
    def test_iqr_method(self, monitor):
        """Test IQR outlier detection method"""
        # Create data with clear outliers
        data = pd.DataFrame({
            'values': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100]  # 100 is outlier
        })
        
        results = monitor.detect_anomalies(data)
        assert results['total_anomalies'] >= 1
        
    def test_z_score_method(self, monitor):
        """Test z-score outlier detection"""
        # Create data where last value is > 3 std deviations away
        values = list(range(1, 100))
        values.append(1000)  # Extreme outlier
        
        data = pd.DataFrame({'values': values})
        results = monitor.detect_anomalies(data)
        
        z_outliers = results['column_anomalies']['values']['z_score_outliers']
        assert z_outliers >= 1
        
    def test_anomaly_bounds(self, monitor, normal_data):
        """Test anomaly detection bounds calculation"""
        results = monitor.detect_anomalies(normal_data)
        
        for col, anomalies in results['column_anomalies'].items():
            bounds = anomalies['bounds']
            stats = anomalies['statistics']
            
            # Bounds should be reasonable
            assert bounds['lower'] < stats['mean']
            assert bounds['upper'] > stats['mean']
            assert bounds['lower'] < bounds['upper']
            
    def test_non_numeric_columns(self, monitor):
        """Test handling of non-numeric columns"""
        data = pd.DataFrame({
            'text': ['a', 'b', 'c', 'd', 'e'],
            'numbers': [1, 2, 3, 4, 5],
            'mixed': ['1', '2', '3', '4', 'text']
        })
        
        results = monitor.detect_anomalies(data)
        
        # Should only analyze numeric columns
        assert 'numbers' in results['column_anomalies']
        assert 'text' not in results['column_anomalies']
        assert 'mixed' not in results['column_anomalies']
        
    def test_insufficient_data(self, monitor):
        """Test handling of insufficient data"""
        # Less than 10 values
        small_data = pd.DataFrame({
            'values': [1, 2, 3, 4, 5]
        })
        
        results = monitor.detect_anomalies(small_data)
        
        # Should skip column with insufficient data
        assert 'values' not in results['column_anomalies']
        
    def test_anomaly_statistics(self, monitor, data_with_outliers):
        """Test anomaly statistics calculation"""
        results = monitor.detect_anomalies(data_with_outliers)
        
        value_stats = results['column_anomalies']['value']['statistics']
        
        # Verify statistics are calculated
        assert 'mean' in value_stats
        assert 'std' in value_stats
        assert 'min' in value_stats
        assert 'max' in value_stats
        
        # Statistics should be reasonable
        assert value_stats['std'] > 0
        assert value_stats['min'] < value_stats['max']
        
    def test_anomaly_percentage_calculation(self, monitor):
        """Test anomaly percentage calculation"""
        # Create data with known outliers
        values = list(range(1, 96))  # 95 normal values
        values.extend([200, 300, 400, 500, 600])  # 5 outliers
        
        data = pd.DataFrame({'values': values})
        results = monitor.detect_anomalies(data)
        
        anomaly_percentage = results['column_anomalies']['values']['iqr_outlier_percentage']
        
        # Should be approximately 5%
        assert 4 <= anomaly_percentage <= 6
        
    def test_multiple_column_anomalies(self, monitor):
        """Test anomaly detection across multiple columns"""
        np.random.seed(42)
        data = pd.DataFrame({
            'col1': np.random.normal(0, 1, 100),
            'col2': np.random.normal(100, 20, 100),
            'col3': np.random.exponential(2, 100),
            'col4': np.random.uniform(0, 1, 100)
        })
        
        # Add anomalies to different columns
        data.loc[0, 'col1'] = 10
        data.loc[1, 'col2'] = 500
        data.loc[2, 'col3'] = 50
        
        results = monitor.detect_anomalies(data)
        
        # Should detect anomalies in multiple columns
        assert len(results['column_anomalies']) >= 3
        assert results['total_anomalies'] >= 3


def run_anomaly_detection_tests():
    """Run anomaly detection tests and report results"""
    print("🔍 Running anomaly detection tests...\n")
    
    # Create test instance
    test_instance = TestAnomalyDetection()
    
    # Create fixtures manually (not using pytest fixtures directly)
    monitor = DataQualityMonitor()
    
    # Normal data
    np.random.seed(42)
    normal_data = pd.DataFrame({
        'value': np.random.normal(100, 10, 1000),
        'count': np.random.poisson(50, 1000),
        'ratio': np.random.uniform(0.4, 0.6, 1000)
    })
    
    # Data with outliers
    np.random.seed(42)
    values = np.random.normal(100, 10, 1000)
    values[50:55] = [200, 250, -50, 300, 400]  # Extreme values
    values[100:103] = [150, 160, 170]  # Moderate outliers
    
    data_with_outliers = pd.DataFrame({
        'value': values,
        'count': np.random.poisson(50, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000)
    })
    
    # Run tests
    test_results = []
    
    # Test 1: Normal data
    try:
        test_instance.test_anomaly_detection_normal_data(monitor, normal_data)
        test_results.append(('Normal Data Detection', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Normal Data Detection', 'Fail', f'❌ {str(e)}'))
        
    # Test 2: Data with outliers
    try:
        test_instance.test_anomaly_detection_with_outliers(monitor, data_with_outliers)
        test_results.append(('Outlier Detection', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Outlier Detection', 'Fail', f'❌ {str(e)}'))
        
    # Test 3: IQR method
    try:
        test_instance.test_iqr_method(monitor)
        test_results.append(('IQR Method', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('IQR Method', 'Fail', f'❌ {str(e)}'))
        
    # Test 4: Z-score method
    try:
        test_instance.test_z_score_method(monitor)
        test_results.append(('Z-Score Method', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Z-Score Method', 'Fail', f'❌ {str(e)}'))
        
    # Test 5: Anomaly bounds
    try:
        test_instance.test_anomaly_bounds(monitor, normal_data)
        test_results.append(('Anomaly Bounds', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Anomaly Bounds', 'Fail', f'❌ {str(e)}'))
        
    # Test 6: Non-numeric columns
    try:
        test_instance.test_non_numeric_columns(monitor)
        test_results.append(('Non-Numeric Handling', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Non-Numeric Handling', 'Fail', f'❌ {str(e)}'))
        
    # Test 7: Statistics
    try:
        test_instance.test_anomaly_statistics(monitor, data_with_outliers)
        test_results.append(('Anomaly Statistics', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Anomaly Statistics', 'Fail', f'❌ {str(e)}'))
        
    # Test 8: Multiple columns
    try:
        test_instance.test_multiple_column_anomalies(monitor)
        test_results.append(('Multi-Column Anomalies', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Multi-Column Anomalies', 'Fail', f'❌ {str(e)}'))
        
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
    success = run_anomaly_detection_tests()
    
    # Validation
    assert success, "Not all tests passed"
    
    print("\n✅ Anomaly detection tests validation passed")