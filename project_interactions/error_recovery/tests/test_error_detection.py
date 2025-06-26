"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test Error Detection Capabilities
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from error_recovery_interaction import (
    ErrorRecoveryInteraction,
    ErrorPattern,
    ErrorSeverity,
    ErrorClassifier
)


class TestErrorDetection:
    """Test error detection and classification"""
    
    @pytest.fixture
    def recovery_system(self):
        """Create recovery system instance"""
        return ErrorRecoveryInteraction()
    
    @pytest.fixture
    def error_classifier(self):
        """Create error classifier instance"""
        return ErrorClassifier()
    
    @pytest.mark.asyncio
    async def test_error_pattern_creation(self, recovery_system):
        """Test error pattern creation and analysis"""
        # Create test error
        error = ValueError("Test error")
        context = {"service": "api", "endpoint": "/users"}
        
        # Analyze error
        pattern = recovery_system._analyze_error(error, context)
        
        assert pattern.error_type == "ValueError"
        assert pattern.frequency == 1
        assert pattern.context_features == context
        assert isinstance(pattern.last_occurrence, datetime)
    
    @pytest.mark.asyncio
    async def test_error_frequency_tracking(self, recovery_system):
        """Test error frequency tracking"""
        error = ConnectionError("Connection failed")
        context = {"service": "database"}
        
        # Analyze same error multiple times
        for i in range(5):
            pattern = recovery_system._analyze_error(error, context)
        
        assert pattern.frequency == 5
        assert pattern.error_type == "ConnectionError"
    
    @pytest.mark.asyncio
    async def test_severity_assessment(self, recovery_system):
        """Test error severity assessment"""
        # Test critical error
        critical_error = SystemError("System failure")
        pattern = ErrorPattern(
            error_type="SystemError",
            frequency=1,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.5,
            avg_recovery_time=1.0
        )
        severity = recovery_system._assess_severity(critical_error, pattern)
        assert severity == ErrorSeverity.CRITICAL
        
        # Test high frequency error
        freq_error = ValueError("Frequent error")
        freq_pattern = ErrorPattern(
            error_type="ValueError",
            frequency=15,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.8,
            avg_recovery_time=0.5
        )
        severity = recovery_system._assess_severity(freq_error, freq_pattern)
        assert severity == ErrorSeverity.HIGH
        
        # Test low success rate error
        low_success_error = RuntimeError("Hard to recover")
        low_pattern = ErrorPattern(
            error_type="RuntimeError",
            frequency=3,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.2,
            avg_recovery_time=5.0
        )
        severity = recovery_system._assess_severity(low_success_error, low_pattern)
        assert severity == ErrorSeverity.MEDIUM
    
    @pytest.mark.asyncio
    async def test_error_pattern_features(self):
        """Test error pattern feature extraction"""
        pattern = ErrorPattern(
            error_type="TestError",
            frequency=10,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.75,
            avg_recovery_time=2.5,
            context_features={"key": "value"}
        )
        
        features = pattern.to_feature_vector()
        
        assert len(features) == 6
        assert features[1] == 10  # frequency
        assert features[3] == 0.75  # recovery success rate
        assert features[4] == 2.5  # avg recovery time
    
    @pytest.mark.asyncio
    async def test_ml_classifier_training(self, error_classifier):
        """Test ML classifier training"""
        # Create training data
        patterns = []
        labels = []
        
        # Generate synthetic training data
        from error_recovery_interaction import RecoveryAction
        
        for i in range(50):
            pattern = ErrorPattern(
                error_type=f"Error{i % 5}",
                frequency=i % 10,
                last_occurrence=datetime.now(),
                recovery_success_rate=(i % 100) / 100,
                avg_recovery_time=i % 5
            )
            patterns.append(pattern)
            
            # Simple rule for labels
            if i % 5 == 0:
                labels.append(RecoveryAction.RETRY)
            elif i % 5 == 1:
                labels.append(RecoveryAction.RETRY_WITH_BACKOFF)
            else:
                labels.append(RecoveryAction.FALLBACK)
        
        # Train classifier
        error_classifier.train(patterns, labels)
        
        assert error_classifier.is_trained
        
        # Test prediction
        test_pattern = ErrorPattern(
            error_type="TestError",
            frequency=5,
            last_occurrence=datetime.now(),
            recovery_success_rate=0.5,
            avg_recovery_time=1.0
        )
        
        prediction = error_classifier.predict_recovery(test_pattern)
        assert isinstance(prediction, RecoveryAction)
    
    @pytest.mark.asyncio
    async def test_error_correlation(self, recovery_system):
        """Test error correlation detection"""
        # Simulate correlated errors
        errors = [
            (ConnectionError("DB connection failed"), {"service": "api", "db": "primary"}),
            (TimeoutError("Query timeout"), {"service": "api", "db": "primary"}),
            (ConnectionError("DB connection failed"), {"service": "worker", "db": "primary"})
        ]
        
        patterns = []
        for error, context in errors:
            pattern = recovery_system._analyze_error(error, context)
            patterns.append(pattern)
        
        # Check that errors are tracked
        assert len(recovery_system.error_patterns) > 0
        
        # Verify context features are preserved
        for pattern in patterns:
            assert "service" in pattern.context_features
            assert "db" in pattern.context_features
    
    @pytest.mark.asyncio
    async def test_concurrent_error_detection(self, recovery_system):
        """Test concurrent error detection"""
        async def generate_error(error_type: str, delay: float):
            await asyncio.sleep(delay)
            error = Exception(f"{error_type} error")
            return recovery_system._analyze_error(error, {"type": error_type})
        
        # Generate concurrent errors
        tasks = [
            generate_error("TypeA", 0.1),
            generate_error("TypeB", 0.1),
            generate_error("TypeA", 0.2),
            generate_error("TypeC", 0.1)
        ]
        
        patterns = await asyncio.gather(*tasks)
        
        # Verify all patterns were created
        assert len(patterns) == 4
        
        # Check frequency tracking for TypeA
        type_a_patterns = [p for p in patterns if "TypeA" in p.error_type]
        assert len(type_a_patterns) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])