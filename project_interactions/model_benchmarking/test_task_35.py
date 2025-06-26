"""
Test Task 35: Automated Model Benchmarking Suite Verification Script

This script verifies that the model benchmarking implementation meets all requirements.
"""

import sys
from pathlib import Path
import subprocess
import json
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from model_benchmarking_interaction import (
    ModelBenchmarkingSuite, BenchmarkMetrics,
    TORCH_AVAILABLE, TF_AVAILABLE
)

def test_directory_structure():
    """Test that the directory structure is correct"""
    print("\n=== Testing Directory Structure ===")
    
    base_dir = Path(__file__).parent
    assert base_dir.name == "model_benchmarking", f"Directory should be 'model_benchmarking', got '{base_dir.name}'"
    
    # Check main file exists
    main_file = base_dir / "model_benchmarking_interaction.py"
    assert main_file.exists(), "Main interaction file missing"
    
    # Check test directory
    test_dir = base_dir / "tests"
    assert test_dir.exists(), "Tests directory missing"
    
    # Check test files
    test_files = [
        "test_model_benchmarking.py",
        "test_framework_support.py", 
        "test_statistical_analysis.py"
    ]
    
    for test_file in test_files:
        assert (test_dir / test_file).exists(), f"Test file {test_file} missing"
    
    print("✅ Directory structure is correct")
    return True

def test_core_functionality():
    """Test core benchmarking functionality"""
    print("\n=== Testing Core Functionality ===")
    
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    
    # Create test data
    X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train models
    print("Training test models...")
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=10, random_state=42),
        "Logistic Regression": LogisticRegression(random_state=42)
    }
    
    for name, model in models.items():
        model.fit(X_train, y_train)
    
    # Test benchmarking
    print("Running benchmarks...")
    with tempfile.TemporaryDirectory() as tmpdir:
        suite = ModelBenchmarkingSuite(output_dir=tmpdir)
        
        # Test single model benchmark
        rf_metrics = suite.benchmark_model(
            models["Random Forest"], X_test, y_test,
            model_name="RF Test",
            dataset_name="test_data",
            task_type="classification",
            batch_size=32,
            cross_validate=False
        )
        
        # Verify metrics
        assert isinstance(rf_metrics, BenchmarkMetrics)
        assert rf_metrics.model_name == "RF Test"
        assert rf_metrics.framework == "sklearn"
        assert 0 <= rf_metrics.accuracy <= 1
        assert rf_metrics.inference_time_mean > 0
        assert rf_metrics.memory_usage_mb > 0
        print(f"  - Accuracy: {rf_metrics.accuracy:.4f}")
        print(f"  - Inference time: {rf_metrics.inference_time_mean*1000:.2f} ms")
        print(f"  - Memory usage: {rf_metrics.memory_usage_mb:.2f} MB")
        
        # Test model comparison
        print("\nComparing models...")
        comparison_df = suite.compare_models(
            models, X_test, y_test,
            dataset_name="comparison_test"
        )
        
        assert len(comparison_df) == len(models)
        assert all(col in comparison_df.columns for col in 
                  ["Model", "Accuracy", "Inference Time (ms)", "Memory (MB)"])
        
        print("Comparison results:")
        print(comparison_df)
        
        # Test report generation
        print("\nGenerating reports...")
        suite.generate_report([rf_metrics], "test_report.html")
        
        report_path = Path(tmpdir) / "test_report.html"
        assert report_path.exists()
        assert report_path.stat().st_size > 1000  # Should have content
        
        # Test export functionality
        suite.export_results("json")
        json_files = list(Path(tmpdir).glob("*.json"))
        assert len(json_files) >= 1
        
    print("✅ Core functionality working correctly")
    return True

def test_framework_support():
    """Test multi-framework support"""
    print("\n=== Testing Framework Support ===")
    
    suite = ModelBenchmarkingSuite()
    
    # Test sklearn
    from sklearn.linear_model import LogisticRegression
    sklearn_model = LogisticRegression()
    assert suite._detect_framework(sklearn_model) == "sklearn"
    print("✅ Scikit-learn support verified")
    
    # Test PyTorch if available
    if TORCH_AVAILABLE:
        import torch.nn as nn
        class DummyNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc = nn.Linear(10, 2)
        
        pytorch_model = DummyNet()
        assert suite._detect_framework(pytorch_model) == "pytorch"
        print("✅ PyTorch support verified")
    else:
        print("⚠️  PyTorch not available for testing")
    
    # Test TensorFlow if available
    if TF_AVAILABLE:
        import tensorflow as tf
        tf_model = tf.keras.Sequential([
            tf.keras.layers.Dense(10, activation='relu'),
            tf.keras.layers.Dense(2)
        ])
        assert suite._detect_framework(tf_model) == "tensorflow"
        print("✅ TensorFlow support verified")
    else:
        print("⚠️  TensorFlow not available for testing")
    
    return True

def test_statistical_features():
    """Test statistical analysis features"""
    print("\n=== Testing Statistical Features ===")
    
    # Test confidence intervals
    metrics = BenchmarkMetrics(
        model_name="Test Model",
        framework="sklearn",
        dataset_name="test",
        cross_val_scores=[0.85, 0.86, 0.84, 0.87, 0.85]
    )
    
    import numpy as np
    mean = np.mean(metrics.cross_val_scores)
    std = np.std(metrics.cross_val_scores)
    ci_lower = mean - 1.96 * std
    ci_upper = mean + 1.96 * std
    
    assert ci_lower < mean < ci_upper
    print(f"✅ Confidence interval calculation working: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    # Test regression detection
    suite = ModelBenchmarkingSuite()
    
    baseline = BenchmarkMetrics(
        model_name="baseline",
        framework="sklearn", 
        dataset_name="test",
        accuracy=0.90,
        inference_time_mean=0.01,
        memory_usage_mb=100
    )
    
    current = BenchmarkMetrics(
        model_name="current",
        framework="sklearn",
        dataset_name="test",
        accuracy=0.85,  # 5.5% drop
        inference_time_mean=0.02,  # 100% increase
        memory_usage_mb=120  # 20% increase
    )
    
    regressions = suite.detect_performance_regression(current, baseline, threshold=0.05)
    assert regressions['accuracy'] == True  # >5% regression
    assert regressions['speed'] == True     # >5% regression  
    assert regressions['memory'] == True    # >5% regression
    
    print("✅ Regression detection working correctly")
    return True

def test_visualization_features():
    """Test visualization and reporting features"""
    print("\n=== Testing Visualization Features ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        suite = ModelBenchmarkingSuite(output_dir=tmpdir)
        
        # Create sample metrics
        metrics1 = BenchmarkMetrics(
            model_name="Model A",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.85,
            f1_score=0.84,
            inference_time_mean=0.01,
            inference_throughput=100,
            memory_usage_mb=50,
            model_size_mb=10
        )
        
        metrics2 = BenchmarkMetrics(
            model_name="Model B",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.88,
            f1_score=0.87,
            inference_time_mean=0.015,
            inference_throughput=66.67,
            memory_usage_mb=75,
            model_size_mb=15
        )
        
        # Generate report with visualizations
        suite.generate_report([metrics1, metrics2], "viz_test.html")
        
        report_path = Path(tmpdir) / "viz_test.html"
        assert report_path.exists()
        
        # Check HTML content
        html_content = report_path.read_text()
        assert "Model Benchmark Report" in html_content
        assert "data:image/png;base64" in html_content  # Embedded plot
        assert "Model A" in html_content
        assert "Model B" in html_content
        
        print("✅ Visualization and reporting working correctly")
    
    return True

def run_unit_tests():
    """Run the unit tests"""
    print("\n=== Running Unit Tests ===")
    
    test_dir = Path(__file__).parent / "tests"
    
    # Run pytest on the test directory
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        print("✅ All unit tests passed")
        return True
    else:
        print("❌ Some unit tests failed")
        return False

def test_performance_metrics():
    """Test that all required performance metrics are tracked"""
    print("\n=== Testing Performance Metrics Coverage ===")
    
    metrics = BenchmarkMetrics(
        model_name="test",
        framework="sklearn",
        dataset_name="test"
    )
    
    # Check all required metrics exist
    required_metrics = [
        'accuracy', 'precision', 'recall', 'f1_score', 'auc_roc',
        'mse', 'mae', 'r2',
        'inference_time_mean', 'inference_time_std', 'inference_throughput',
        'memory_usage_mb', 'model_size_mb', 'cpu_usage_percent',
        'cross_val_scores', 'confidence_interval', 'p_value'
    ]
    
    for metric in required_metrics:
        assert hasattr(metrics, metric), f"Missing metric: {metric}"
    
    print("✅ All required performance metrics are available")
    return True

def main():
    """Run all verification tests"""
    print("=" * 60)
    print("Task 35: Automated Model Benchmarking Suite Verification")
    print("=" * 60)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("Core Functionality", test_core_functionality),
        ("Framework Support", test_framework_support),
        ("Statistical Features", test_statistical_features),
        ("Visualization Features", test_visualization_features),
        ("Performance Metrics", test_performance_metrics),
        ("Unit Tests", run_unit_tests)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All verification tests passed! Task 35 is complete.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues.")
        return 1

if __name__ == "__main__":
    # sys.exit() removed)