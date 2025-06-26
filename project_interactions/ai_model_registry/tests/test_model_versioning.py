#!/usr/bin/env python3
"""Test model versioning functionality"""

import sys
import os
from datetime import datetime
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs")

from project_interactions.ai_model_registry.ai_model_registry_interaction import (
    AIModelRegistry, ModelVersion, ModelMetadata, ModelStatus, ModelType
)


def test_model_registration():
    """Test model registration"""
    registry = AIModelRegistry()
    
    # Register a model
    model_id = registry.register_model(
        name="sentiment-analyzer",
        model_type=ModelType.TEXT_CLASSIFICATION,
        framework="pytorch",
        description="BERT-based sentiment analysis model"
    )
    
    assert model_id is not None, "Model registration failed"
    assert model_id.startswith("sentiment-analyzer"), "Wrong model ID format"
    
    # Check model exists
    models = registry.list_models()
    assert len(models) > 0, "No models found"
    assert any(m.id == model_id for m in models), "Registered model not found"
    
    print("✓ Model registration test passed")


def test_version_creation():
    """Test model version creation"""
    registry = AIModelRegistry()
    
    # Register model
    model_id = registry.register_model(
        name="image-classifier",
        model_type=ModelType.IMAGE_CLASSIFICATION,
        framework="tensorflow"
    )
    
    # Create version
    version = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/image-classifier-v1.0.0.pb",
        metrics={"accuracy": 0.95, "f1_score": 0.93}
    )
    
    assert version is not None, "Version creation failed"
    assert version.version == "1.0.0", "Wrong version number"
    assert version.metrics["accuracy"] == 0.95, "Metrics not stored"
    
    print("✓ Version creation test passed")


def test_version_comparison():
    """Test version comparison and selection"""
    registry = AIModelRegistry()
    
    # Register model
    model_id = registry.register_model(
        name="test-model",
        model_type=ModelType.REGRESSION,
        framework="scikit-learn"
    )
    
    # Create multiple versions
    v1 = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/v1.pkl",
        metrics={"mse": 0.05, "r2": 0.85}
    )
    
    v2 = registry.create_version(
        model_id=model_id,
        version="1.1.0",
        path="/models/v2.pkl",
        metrics={"mse": 0.03, "r2": 0.92}
    )
    
    # Get latest version
    latest = registry.get_latest_version(model_id)
    assert latest.version == "1.1.0", "Wrong latest version"
    
    # Get best version by metric
    best = registry.get_best_version(model_id, metric="r2", higher_better=True)
    assert best.version == "1.1.0", "Wrong best version"
    
    print("✓ Version comparison test passed")


def test_version_tagging():
    """Test version tagging functionality"""
    registry = AIModelRegistry()
    
    # Register and version
    model_id = registry.register_model(
        name="nlp-model",
        model_type=ModelType.NLP,
        framework="transformers"
    )
    
    version = registry.create_version(
        model_id=model_id,
        version="2.0.0",
        path="/models/nlp-v2.pkl"
    )
    
    # Tag version
    registry.tag_version(model_id, "2.0.0", "production")
    registry.tag_version(model_id, "2.0.0", "stable")
    
    # Get by tag
    prod_version = registry.get_version_by_tag(model_id, "production")
    assert prod_version is not None, "Tagged version not found"
    assert prod_version.version == "2.0.0", "Wrong tagged version"
    
    print("✓ Version tagging test passed")


def test_metadata_management():
    """Test model metadata management"""
    registry = AIModelRegistry()
    
    # Register with metadata
    model_id = registry.register_model(
        name="custom-model",
        model_type=ModelType.CUSTOM,
        framework="custom",
        metadata={
            "author": "data-science-team",
            "training_data": "customer-reviews-2024",
            "hyperparameters": {"learning_rate": 0.001, "batch_size": 32}
        }
    )
    
    # Get model
    model = registry.get_model(model_id)
    assert model.metadata["author"] == "data-science-team", "Metadata not stored"
    
    # Update metadata
    registry.update_model_metadata(model_id, {"validated": True, "validator": "qa-team"})
    
    updated = registry.get_model(model_id)
    assert updated.metadata["validated"] is True, "Metadata not updated"
    assert updated.metadata["author"] == "data-science-team", "Original metadata lost"
    
    print("✓ Metadata management test passed")


def test_version_status_transitions():
    """Test version status transitions"""
    registry = AIModelRegistry()
    
    # Create model and version
    model_id = registry.register_model(
        name="status-test",
        model_type=ModelType.CLASSIFICATION,
        framework="pytorch"
    )
    
    version = registry.create_version(
        model_id=model_id,
        version="1.0.0",
        path="/models/test.pt"
    )
    
    # Check initial status
    assert version.status == ModelStatus.REGISTERED, "Wrong initial status"
    
    # Update status
    registry.update_version_status(model_id, "1.0.0", ModelStatus.VALIDATED)
    v = registry.get_version(model_id, "1.0.0")
    assert v.status == ModelStatus.VALIDATED, "Status not updated"
    
    # Deploy
    registry.update_version_status(model_id, "1.0.0", ModelStatus.DEPLOYED)
    v = registry.get_version(model_id, "1.0.0")
    assert v.status == ModelStatus.DEPLOYED, "Deployment status not set"
    
    print("✓ Version status transitions test passed")


if __name__ == "__main__":
    test_model_registration()
    test_version_creation()
    test_version_comparison()
    test_version_tagging()
    test_metadata_management()
    test_version_status_transitions()
    print("\n✅ All model versioning tests passed")