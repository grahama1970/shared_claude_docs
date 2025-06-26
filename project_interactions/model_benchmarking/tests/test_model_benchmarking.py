"""
Test module for core model benchmarking functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- numpy: https://numpy.org/doc/stable/
- scikit-learn: https://scikit-learn.org/stable/
"""

import pytest
import numpy as np
from pathlib import Path
import json
import tempfile
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import sys
sys.path.append(str(Path(__file__).parent.parent))

from model_benchmarking_interaction import (
    ModelBenchmarkingSuite, BenchmarkMetrics
)


class TestModelBenchmarking:
    """Test core benchmarking functionality"""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample classification data"""
        X, y = make_classification(
            n_samples=1000, n_features=10, n_informative=8,
            n_redundant=2, n_classes=2, random_state=42
        )
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    @pytest.fixture
    def trained_models(self, sample_data):
        """Train sample models"""
        X_train, X_test, y_train, y_test = sample_data
        
        rf = RandomForestClassifier(n_estimators=10, random_state=42)
        rf.fit(X_train, y_train)
        
        lr = LogisticRegression(random_state=42)
        lr.fit(X_train, y_train)
        
        return {"Random Forest": rf, "Logistic Regression": lr}
    
    @pytest.fixture
    def benchmarking_suite(self):
        """Create benchmarking suite with temp directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            suite = ModelBenchmarkingSuite(output_dir=tmpdir)
            yield suite
    
    def test_benchmark_metrics_creation(self):
        """Test BenchmarkMetrics dataclass creation"""
        metrics = BenchmarkMetrics(
            model_name="test_model",
            framework="sklearn",
            dataset_name="test_dataset"
        )
        
        assert metrics.model_name == "test_model"
        assert metrics.framework == "sklearn"
        assert metrics.dataset_name == "test_dataset"
        assert metrics.timestamp is not None
        assert isinstance(metrics.hyperparameters, dict)
        assert isinstance(metrics.cross_val_scores, list)
    
    def test_framework_detection(self, benchmarking_suite, trained_models):
        """Test ML framework detection"""
        for model in trained_models.values():
            framework = benchmarking_suite._detect_framework(model)
            assert framework == "sklearn"
    
    def test_hardware_info_collection(self, benchmarking_suite):
        """Test hardware information collection"""
        info = benchmarking_suite._get_hardware_info()
        
        assert "cpu_count" in info
        assert "cpu_freq" in info
        assert "total_memory" in info
        assert "platform" in info
        assert isinstance(info["cpu_count"], int)
        assert info["cpu_count"] > 0
    
    def test_model_size_calculation(self, benchmarking_suite, trained_models):
        """Test model size calculation"""
        for name, model in trained_models.items():
            size = benchmarking_suite._get_model_size(model, "sklearn")
            assert size > 0
            assert isinstance(size, float)
            print(f"{name} size: {size:.2f} MB")
    
    def test_inference_benchmarking(self, benchmarking_suite, trained_models, sample_data):
        """Test inference benchmarking"""
        X_train, X_test, y_train, y_test = sample_data
        
        model = trained_models["Random Forest"]
        results = benchmarking_suite.benchmark_inference(
            model, X_test, batch_size=32, num_runs=10, warmup_runs=2
        )
        
        assert "mean_time" in results
        assert "std_time" in results
        assert "throughput" in results
        assert "cpu_usage" in results
        
        assert results["mean_time"] > 0
        assert results["throughput"] > 0
        # CPU usage can exceed 100% on multi-core systems
        assert results["cpu_usage"] >= 0
    
    def test_full_model_benchmark(self, benchmarking_suite, trained_models, sample_data):
        """Test full model benchmarking"""
        X_train, X_test, y_train, y_test = sample_data
        
        model = trained_models["Random Forest"]
        metrics = benchmarking_suite.benchmark_model(
            model, X_test, y_test,
            model_name="RF Test",
            dataset_name="test_classification",
            task_type="classification",
            batch_size=32,
            cross_validate=False  # Skip for speed
        )
        
        # Check performance metrics
        assert 0 <= metrics.accuracy <= 1
        assert 0 <= metrics.precision <= 1
        assert 0 <= metrics.recall <= 1
        assert 0 <= metrics.f1_score <= 1
        
        # Check resource metrics
        assert metrics.memory_usage_mb > 0
        assert metrics.model_size_mb > 0
        assert metrics.inference_time_mean > 0
        assert metrics.inference_throughput > 0
        
        # Check metadata
        assert metrics.hardware_info
        assert metrics.dataset_info["num_samples"] == len(X_test)
        assert metrics.dataset_info["num_features"] == X_test.shape[1]
    
    def test_model_comparison(self, benchmarking_suite, trained_models, sample_data):
        """Test comparing multiple models"""
        X_train, X_test, y_train, y_test = sample_data
        
        comparison_df = benchmarking_suite.compare_models(
            trained_models, X_test, y_test,
            dataset_name="test_comparison",
            task_type="classification"
        )
        
        assert len(comparison_df) == len(trained_models)
        assert "Model" in comparison_df.columns
        assert "Accuracy" in comparison_df.columns
        assert "Inference Time (ms)" in comparison_df.columns
        assert "Memory (MB)" in comparison_df.columns
        
        # Check that values are reasonable
        assert all(0 <= acc <= 1 for acc in comparison_df["Accuracy"])
        assert all(t > 0 for t in comparison_df["Inference Time (ms)"])
    
    def test_regression_detection(self, benchmarking_suite):
        """Test performance regression detection"""
        # Create baseline metrics
        baseline = BenchmarkMetrics(
            model_name="baseline",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.95,
            inference_time_mean=0.01,
            memory_usage_mb=100
        )
        
        # Create current metrics with regression
        current = BenchmarkMetrics(
            model_name="current",
            framework="sklearn",
            dataset_name="test",
            accuracy=0.85,  # 10% drop
            inference_time_mean=0.02,  # 100% increase
            memory_usage_mb=150  # 50% increase
        )
        
        regressions = benchmarking_suite.detect_performance_regression(
            current, baseline, threshold=0.05
        )
        
        assert regressions['accuracy'] == True  # >5% regression
        assert regressions['speed'] == True  # >5% regression
        assert regressions['memory'] == True  # >5% regression
    
    def test_report_generation(self, benchmarking_suite, trained_models, sample_data):
        """Test report generation"""
        X_train, X_test, y_train, y_test = sample_data
        
        # Benchmark a model
        model = trained_models["Random Forest"]
        metrics = benchmarking_suite.benchmark_model(
            model, X_test, y_test,
            model_name="Test Model",
            dataset_name="test_data"
        )
        
        # Generate report
        benchmarking_suite.generate_report(metrics, "test_report.html")
        
        # Check that files were created
        report_path = benchmarking_suite.output_dir / "test_report.html"
        json_path = benchmarking_suite.output_dir / "test_report.json"
        
        assert report_path.exists()
        assert json_path.exists()
        
        # Verify HTML content
        html_content = report_path.read_text()
        assert "Model Benchmark Report" in html_content
        assert "Test Model" in html_content
        assert "sklearn" in html_content
        
        # Verify JSON content
        with open(json_path) as f:
            json_data = json.load(f)
        assert len(json_data) == 1
        assert json_data[0]["model_name"] == "Test Model"
    
    def test_results_export(self, benchmarking_suite, trained_models, sample_data):
        """Test exporting results to different formats"""
        X_train, X_test, y_train, y_test = sample_data
        
        # Benchmark models
        for name, model in trained_models.items():
            benchmarking_suite.benchmark_model(
                model, X_test, y_test, name, "test_export"
            )
        
        # Test CSV export
        benchmarking_suite.export_results("csv")
        csv_files = list(benchmarking_suite.output_dir.glob("*.csv"))
        assert len(csv_files) == 1
        
        # Test JSON export
        benchmarking_suite.export_results("json")
        json_files = list(benchmarking_suite.output_dir.glob("benchmark_results_*.json"))
        assert len(json_files) == 1
        
        # Verify JSON content
        with open(json_files[0]) as f:
            data = json.load(f)
        assert len(data) == len(trained_models)
        assert all("model_name" in item for item in data)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])