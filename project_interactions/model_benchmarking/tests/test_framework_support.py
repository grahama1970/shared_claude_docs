"""
Test module for multi-framework support

External Dependencies:
- pytest: https://docs.pytest.org/
- numpy: https://numpy.org/doc/stable/
- scikit-learn: https://scikit-learn.org/stable/
- torch: https://pytorch.org/docs/ (optional)
- tensorflow: https://www.tensorflow.org/api_docs (optional)
"""

import pytest
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from model_benchmarking_interaction import (
    ModelBenchmarkingSuite, BenchmarkMetrics,
    TORCH_AVAILABLE, TF_AVAILABLE
)

# Optional imports
if TORCH_AVAILABLE:
    import torch
    import torch.nn as nn
    
if TF_AVAILABLE:
    import tensorflow as tf


class TestFrameworkSupport:
    """Test support for multiple ML frameworks"""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data"""
        np.random.seed(42)
        X = np.random.randn(1000, 10).astype(np.float32)
        y = (X[:, 0] + X[:, 1] > 0).astype(np.int64)
        
        # One-hot encode for multi-class compatibility
        y_onehot = np.zeros((len(y), 2))
        y_onehot[np.arange(len(y)), y] = 1
        
        return X[:800], X[800:], y[:800], y[800:], y_onehot[:800], y_onehot[800:]
    
    @pytest.fixture
    def pytorch_model(self, sample_data):
        """Create and train a PyTorch model"""
        if not TORCH_AVAILABLE:
            pytest.skip("PyTorch not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        class SimpleNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc1 = nn.Linear(10, 32)
                self.fc2 = nn.Linear(32, 16)
                self.fc3 = nn.Linear(16, 2)
                self.relu = nn.ReLU()
                self.softmax = nn.Softmax(dim=1)
                
            def forward(self, x):
                x = self.relu(self.fc1(x))
                x = self.relu(self.fc2(x))
                x = self.fc3(x)
                return self.softmax(x)
        
        model = SimpleNet()
        
        # Simple training
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.CrossEntropyLoss()
        
        X_train_t = torch.FloatTensor(X_train)
        y_train_t = torch.LongTensor(y_train)
        
        model.train()
        for epoch in range(20):
            optimizer.zero_grad()
            outputs = model(X_train_t)
            loss = criterion(outputs, y_train_t)
            loss.backward()
            optimizer.step()
            
        model.eval()
        return model
    
    @pytest.fixture
    def tensorflow_model(self, sample_data):
        """Create and train a TensorFlow model"""
        if not TF_AVAILABLE:
            pytest.skip("TensorFlow not available")
            
        X_train, X_test, y_train, y_test, y_train_oh, y_test_oh = sample_data
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(2, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        model.fit(
            X_train, y_train_oh,
            epochs=20,
            batch_size=32,
            verbose=0
        )
        
        return model
    
    @pytest.fixture
    def sklearn_model(self, sample_data):
        """Create and train a scikit-learn model"""
        from sklearn.neural_network import MLPClassifier
        
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        model = MLPClassifier(
            hidden_layer_sizes=(32, 16),
            activation='relu',
            max_iter=500,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        return model
    
    def test_pytorch_framework_detection(self, pytorch_model):
        """Test PyTorch framework detection"""
        if not TORCH_AVAILABLE:
            pytest.skip("PyTorch not available")
            
        suite = ModelBenchmarkingSuite()
        framework = suite._detect_framework(pytorch_model)
        assert framework == "pytorch"
    
    def test_tensorflow_framework_detection(self, tensorflow_model):
        """Test TensorFlow framework detection"""
        if not TF_AVAILABLE:
            pytest.skip("TensorFlow not available")
            
        suite = ModelBenchmarkingSuite()
        framework = suite._detect_framework(tensorflow_model)
        assert framework == "tensorflow"
    
    def test_sklearn_framework_detection(self, sklearn_model):
        """Test scikit-learn framework detection"""
        suite = ModelBenchmarkingSuite()
        framework = suite._detect_framework(sklearn_model)
        assert framework == "sklearn"
    
    def test_pytorch_model_size(self, pytorch_model):
        """Test PyTorch model size calculation"""
        if not TORCH_AVAILABLE:
            pytest.skip("PyTorch not available")
            
        suite = ModelBenchmarkingSuite()
        size = suite._get_model_size(pytorch_model, "pytorch")
        
        assert size > 0
        assert isinstance(size, float)
        
        # Verify it's reasonable (simple model should be < 1MB)
        assert size < 1.0
    
    def test_tensorflow_model_size(self, tensorflow_model):
        """Test TensorFlow model size calculation"""
        if not TF_AVAILABLE:
            pytest.skip("TensorFlow not available")
            
        suite = ModelBenchmarkingSuite()
        size = suite._get_model_size(tensorflow_model, "tensorflow")
        
        assert size > 0
        assert isinstance(size, float)
        assert size < 1.0  # Simple model
    
    def test_pytorch_inference(self, pytorch_model, sample_data):
        """Test PyTorch model inference"""
        if not TORCH_AVAILABLE:
            pytest.skip("PyTorch not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        suite = ModelBenchmarkingSuite()
        predictions = suite._run_inference(pytorch_model, X_test[:32], "pytorch")
        
        assert predictions.shape == (32, 2)
        assert np.allclose(predictions.sum(axis=1), 1.0)  # Softmax outputs
    
    def test_tensorflow_inference(self, tensorflow_model, sample_data):
        """Test TensorFlow model inference"""
        if not TF_AVAILABLE:
            pytest.skip("TensorFlow not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        suite = ModelBenchmarkingSuite()
        predictions = suite._run_inference(tensorflow_model, X_test[:32], "tensorflow")
        
        assert predictions.shape == (32, 2)
        assert np.allclose(predictions.sum(axis=1), 1.0, atol=1e-6)
    
    def test_pytorch_benchmarking(self, pytorch_model, sample_data):
        """Test full PyTorch model benchmarking"""
        if not TORCH_AVAILABLE:
            pytest.skip("PyTorch not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        suite = ModelBenchmarkingSuite()
        metrics = suite.benchmark_model(
            pytorch_model, X_test, y_test,
            model_name="PyTorch Test",
            dataset_name="binary_classification",
            task_type="classification",
            batch_size=32,
            cross_validate=False
        )
        
        assert metrics.framework == "pytorch"
        assert 0 <= metrics.accuracy <= 1
        assert metrics.inference_time_mean > 0
        assert metrics.memory_usage_mb > 0
        assert metrics.model_size_mb > 0
    
    def test_tensorflow_benchmarking(self, tensorflow_model, sample_data):
        """Test full TensorFlow model benchmarking"""
        if not TF_AVAILABLE:
            pytest.skip("TensorFlow not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        suite = ModelBenchmarkingSuite()
        metrics = suite.benchmark_model(
            tensorflow_model, X_test, y_test,
            model_name="TensorFlow Test",
            dataset_name="binary_classification",
            task_type="classification",
            batch_size=32,
            cross_validate=False
        )
        
        assert metrics.framework == "tensorflow"
        assert 0 <= metrics.accuracy <= 1
        assert metrics.inference_time_mean > 0
        assert metrics.memory_usage_mb > 0
    
    def test_cross_framework_comparison(self, pytorch_model, tensorflow_model, sklearn_model, sample_data):
        """Test comparing models across frameworks"""
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        models = {"sklearn": sklearn_model}
        
        if TORCH_AVAILABLE:
            models["pytorch"] = pytorch_model
        if TF_AVAILABLE:
            models["tensorflow"] = tensorflow_model
            
        if len(models) < 2:
            pytest.skip("Need at least 2 frameworks for comparison")
        
        suite = ModelBenchmarkingSuite()
        comparison_df = suite.compare_models(
            models, X_test, y_test,
            dataset_name="cross_framework_test"
        )
        
        assert len(comparison_df) == len(models)
        assert all(framework in comparison_df["Framework"].values for framework in models.keys())
        
        # All models should have reasonable accuracy on this simple task
        assert all(0.5 <= acc <= 1.0 for acc in comparison_df["Accuracy"])
    
    def test_gpu_metrics_collection(self, pytorch_model, sample_data):
        """Test GPU metrics collection if available"""
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            pytest.skip("PyTorch GPU not available")
            
        X_train, X_test, y_train, y_test, _, _ = sample_data
        
        # Move model to GPU
        pytorch_model = pytorch_model.cuda()
        
        suite = ModelBenchmarkingSuite()
        
        # Note: Actual GPU metrics collection would require nvidia-ml-py
        # This test just verifies the structure is in place
        # Keep data on CPU for this test as our _run_inference handles device placement
        metrics = suite.benchmark_model(
            pytorch_model, X_test, y_test,
            model_name="GPU Test",
            dataset_name="gpu_test",
            cross_validate=False
        )
        
        assert metrics.framework == "pytorch"
        assert hasattr(metrics, 'gpu_usage_percent')
        assert hasattr(metrics, 'gpu_memory_mb')


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])