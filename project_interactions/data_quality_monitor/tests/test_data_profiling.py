"""
Module: test_data_profiling.py
Purpose: Test data profiling functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pandas: https://pandas.pydata.org/docs/
- numpy: https://numpy.org/doc/stable/

Example Usage:
>>> pytest test_data_profiling.py -v
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_quality_monitor_interaction import DataQualityMonitor


class TestDataProfiling:
    """Test suite for data profiling functionality"""
    
    @pytest.fixture
    def mixed_data(self):
        """Create mixed type dataset for profiling"""
        np.random.seed(42)
        return pd.DataFrame({
            'id': range(1, 101),
            'name': [f'Person_{i}' for i in range(1, 101)],
            'age': np.random.randint(18, 80, 100),
            'salary': np.random.normal(50000, 15000, 100),
            'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 100),
            'is_active': np.random.choice([True, False], 100),
            'join_date': pd.date_range('2020-01-01', periods=100, freq='D'),
            'rating': np.random.uniform(1, 5, 100),
            'tags': [f'tag{i%5}' for i in range(100)]
        })
        
    @pytest.fixture
    def monitor(self):
        """Create monitor instance"""
        return DataQualityMonitor()
        
    def test_profile_structure(self, monitor, mixed_data):
        """Test profile structure and required fields"""
        profile = monitor.profile_data(mixed_data)
        
        # Check required sections
        assert 'shape' in profile
        assert 'memory_usage' in profile
        assert 'column_types' in profile
        assert 'numeric_summary' in profile
        assert 'categorical_summary' in profile
        
        # Check shape
        assert profile['shape']['rows'] == 100
        assert profile['shape']['columns'] == 9
        
    def test_numeric_profiling(self, monitor, mixed_data):
        """Test numeric column profiling"""
        profile = monitor.profile_data(mixed_data)
        numeric_summary = profile['numeric_summary']
        
        # Should profile numeric columns
        assert 'age' in numeric_summary
        assert 'salary' in numeric_summary
        assert 'rating' in numeric_summary
        assert 'id' in numeric_summary
        
        # Check age statistics
        age_stats = numeric_summary['age']
        assert 'mean' in age_stats
        assert 'std' in age_stats
        assert 'min' in age_stats
        assert 'max' in age_stats
        assert 'q25' in age_stats
        assert 'q50' in age_stats
        assert 'q75' in age_stats
        assert 'null_count' in age_stats
        assert 'unique_count' in age_stats
        
        # Validate statistics are reasonable
        assert 18 <= age_stats['min'] <= age_stats['max'] < 80
        assert age_stats['q25'] < age_stats['q50'] < age_stats['q75']
        
    def test_categorical_profiling(self, monitor, mixed_data):
        """Test categorical column profiling"""
        profile = monitor.profile_data(mixed_data)
        categorical_summary = profile['categorical_summary']
        
        # Should profile categorical columns
        assert 'name' in categorical_summary
        assert 'department' in categorical_summary
        assert 'tags' in categorical_summary
        
        # Check department statistics
        dept_stats = categorical_summary['department']
        assert 'unique_count' in dept_stats
        assert 'null_count' in dept_stats
        assert 'top_values' in dept_stats
        assert 'mode' in dept_stats
        
        # Validate department values
        assert dept_stats['unique_count'] <= 4  # Max 4 departments
        assert dept_stats['mode'] in ['Sales', 'Engineering', 'Marketing', 'HR']
        
    def test_memory_usage(self, monitor, mixed_data):
        """Test memory usage reporting"""
        profile = monitor.profile_data(mixed_data)
        memory_usage = profile['memory_usage']
        
        # Should have memory usage for each column
        assert len(memory_usage) == len(mixed_data.columns) + 1  # +1 for Index
        
        # Memory usage should be positive
        for col, usage in memory_usage.items():
            assert usage > 0
            
    def test_column_types(self, monitor, mixed_data):
        """Test column type detection"""
        profile = monitor.profile_data(mixed_data)
        column_types = profile['column_types']
        
        # Check detected types
        assert column_types['id'] in ['int64', 'int32']
        assert column_types['name'] == 'object'
        assert column_types['salary'] == 'float64'
        assert column_types['is_active'] == 'bool'
        
    def test_empty_dataframe_profiling(self, monitor):
        """Test profiling empty dataframe"""
        empty_df = pd.DataFrame()
        profile = monitor.profile_data(empty_df)
        
        assert profile['shape']['rows'] == 0
        assert profile['shape']['columns'] == 0
        assert len(profile['numeric_summary']) == 0
        assert len(profile['categorical_summary']) == 0
        
    def test_null_handling(self, monitor):
        """Test handling of null values in profiling"""
        data_with_nulls = pd.DataFrame({
            'complete': [1, 2, 3, 4, 5],
            'partial': [1, 2, None, 4, None],
            'all_null': [None, None, None, None, None]
        })
        
        profile = monitor.profile_data(data_with_nulls)
        
        # Check null counts
        assert profile['numeric_summary']['complete']['null_count'] == 0
        assert profile['numeric_summary']['partial']['null_count'] == 2
        
    def test_unique_value_counts(self, monitor):
        """Test unique value counting"""
        data = pd.DataFrame({
            'unique': [1, 2, 3, 4, 5],
            'duplicates': [1, 1, 2, 2, 3],
            'constant': [1, 1, 1, 1, 1]
        })
        
        profile = monitor.profile_data(data)
        
        assert profile['numeric_summary']['unique']['unique_count'] == 5
        assert profile['numeric_summary']['duplicates']['unique_count'] == 3
        assert profile['numeric_summary']['constant']['unique_count'] == 1
        
    def test_top_values_categorical(self, monitor):
        """Test top values for categorical columns"""
        data = pd.DataFrame({
            'category': ['A'] * 50 + ['B'] * 30 + ['C'] * 15 + ['D'] * 5
        })
        
        profile = monitor.profile_data(data)
        top_values = profile['categorical_summary']['category']['top_values']
        
        # Should be ordered by frequency
        values = list(top_values.keys())
        counts = list(top_values.values())
        
        assert values[0] == 'A'
        assert counts[0] == 50
        assert all(counts[i] >= counts[i+1] for i in range(len(counts)-1))
        
    def test_datetime_handling(self, monitor, mixed_data):
        """Test handling of datetime columns"""
        profile = monitor.profile_data(mixed_data)
        
        # Datetime columns should be in categorical summary
        assert 'join_date' in profile['categorical_summary']
        
    def test_boolean_handling(self, monitor, mixed_data):
        """Test handling of boolean columns"""
        profile = monitor.profile_data(mixed_data)
        
        # Boolean columns are treated as categorical
        assert 'is_active' in profile['categorical_summary']
        
        is_active_stats = profile['categorical_summary']['is_active']
        assert is_active_stats['unique_count'] <= 2


def run_data_profiling_tests():
    """Run data profiling tests and report results"""
    print("📊 Running data profiling tests...\n")
    
    # Create test instance
    test_instance = TestDataProfiling()
    
    # Create fixtures manually (not using pytest fixtures directly)
    monitor = DataQualityMonitor()
    
    # Mixed data
    np.random.seed(42)
    mixed_data = pd.DataFrame({
        'id': range(1, 101),
        'name': [f'Person_{i}' for i in range(1, 101)],
        'age': np.random.randint(18, 80, 100),
        'salary': np.random.normal(50000, 15000, 100),
        'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR'], 100),
        'is_active': np.random.choice([True, False], 100),
        'join_date': pd.date_range('2020-01-01', periods=100, freq='D'),
        'rating': np.random.uniform(1, 5, 100),
        'tags': [f'tag{i%5}' for i in range(100)]
    })
    
    # Run tests
    test_results = []
    
    # Test 1: Profile structure
    try:
        test_instance.test_profile_structure(monitor, mixed_data)
        test_results.append(('Profile Structure', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Profile Structure', 'Fail', f'❌ {str(e)}'))
        
    # Test 2: Numeric profiling
    try:
        test_instance.test_numeric_profiling(monitor, mixed_data)
        test_results.append(('Numeric Profiling', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Numeric Profiling', 'Fail', f'❌ {str(e)}'))
        
    # Test 3: Categorical profiling
    try:
        test_instance.test_categorical_profiling(monitor, mixed_data)
        test_results.append(('Categorical Profiling', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Categorical Profiling', 'Fail', f'❌ {str(e)}'))
        
    # Test 4: Memory usage
    try:
        test_instance.test_memory_usage(monitor, mixed_data)
        test_results.append(('Memory Usage', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Memory Usage', 'Fail', f'❌ {str(e)}'))
        
    # Test 5: Column types
    try:
        test_instance.test_column_types(monitor, mixed_data)
        test_results.append(('Column Types', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Column Types', 'Fail', f'❌ {str(e)}'))
        
    # Test 6: Empty dataframe
    try:
        test_instance.test_empty_dataframe_profiling(monitor)
        test_results.append(('Empty DataFrame', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Empty DataFrame', 'Fail', f'❌ {str(e)}'))
        
    # Test 7: Null handling
    try:
        test_instance.test_null_handling(monitor)
        test_results.append(('Null Handling', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Null Handling', 'Fail', f'❌ {str(e)}'))
        
    # Test 8: Unique values
    try:
        test_instance.test_unique_value_counts(monitor)
        test_results.append(('Unique Value Counts', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Unique Value Counts', 'Fail', f'❌ {str(e)}'))
        
    # Test 9: Top categorical values
    try:
        test_instance.test_top_values_categorical(monitor)
        test_results.append(('Top Categorical Values', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Top Categorical Values', 'Fail', f'❌ {str(e)}'))
        
    # Test 10: Boolean handling
    try:
        test_instance.test_boolean_handling(monitor, mixed_data)
        test_results.append(('Boolean Handling', 'Pass', '✅'))
    except AssertionError as e:
        test_results.append(('Boolean Handling', 'Fail', f'❌ {str(e)}'))
        
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
    success = run_data_profiling_tests()
    
    # Validation
    assert success, "Not all tests passed"
    
    print("\n✅ Data profiling tests validation passed")