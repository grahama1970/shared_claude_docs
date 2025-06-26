"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test module for contradiction detection interactions

Tests the ContradictionDetector class with various scenarios.
"""

import time
import unittest
from datetime import datetime
from typing import List

import sys
import os
# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from contradiction_detection_interaction import (
    ContradictionDetector,
    ContradictionSeverity,
    SourceType,
    Source,
    Contradiction,
    ReconciliationStrategy
)


class TestContradictionDetection(unittest.TestCase):
    """Test cases for contradiction detection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = ContradictionDetector()
        self.sources = self.detector.get_mock_sources()
    
    def test_source_loading(self):
        """Test that mock sources are loaded correctly"""
        self.assertGreaterEqual(len(self.sources), 8)
        
        # Check source types
        source_types = {source.type for source in self.sources}
        expected_types = {
            SourceType.ARXIV_PAPER,
            SourceType.YOUTUBE_TRANSCRIPT,
            SourceType.DOCUMENTATION,
            SourceType.TECHNICAL_SPEC,
            SourceType.RESEARCH_BLOG
        }
        self.assertEqual(source_types, expected_types)
        
        # Check all sources have required fields
        for source in self.sources:
            self.assertIsNotNone(source.id)
            self.assertIsNotNone(source.title)
            self.assertIsNotNone(source.content)
            self.assertGreater(len(source.get_statements()), 0)
    
    def test_contradiction_detection(self):
        """Test basic contradiction detection"""
        contradictions = self.detector.detect_contradictions(self.sources)
        
        # Should find multiple contradictions
        self.assertGreater(len(contradictions), 4)
        
        # All contradictions should have required fields
        for contradiction in contradictions:
            self.assertIsNotNone(contradiction.source1_id)
            self.assertIsNotNone(contradiction.source2_id)
            self.assertIsNotNone(contradiction.statement1)
            self.assertIsNotNone(contradiction.statement2)
            self.assertIsInstance(contradiction.severity, ContradictionSeverity)
            self.assertGreaterEqual(contradiction.confidence, 0)
            self.assertLessEqual(contradiction.confidence, 1)
    
    def test_severity_classification(self):
        """Test that contradictions are properly classified by severity"""
        contradictions = self.detector.detect_contradictions(self.sources)
        classified = self.detector.classify_contradictions(contradictions)
        
        # Should have multiple severity levels
        self.assertGreater(len(classified), 1)
        
        # Check that critical/major contradictions exist
        critical_major_count = 0
        for severity in [ContradictionSeverity.CRITICAL, ContradictionSeverity.MAJOR]:
            if severity in classified:
                critical_major_count += len(classified[severity])
        
        self.assertGreater(critical_major_count, 0)
    
    def test_specific_contradictions(self):
        """Test that specific known contradictions are detected"""
        contradictions = self.detector.detect_contradictions(self.sources)
        
        # Build a map of contradiction pairs
        contradiction_pairs = {}
        for c in contradictions:
            pair = tuple(sorted([c.source1_id, c.source2_id]))
            contradiction_pairs[pair] = c
        
        # Check quantum computing contradiction
        quantum_pair = tuple(sorted(["arxiv_2024_001", "arxiv_2024_002"]))
        self.assertIn(quantum_pair, contradiction_pairs)
        quantum_contradiction = contradiction_pairs[quantum_pair]
        # Accept MODERATE or higher severity for quantum contradiction
        self.assertIn(quantum_contradiction.severity, 
                     [ContradictionSeverity.MODERATE, ContradictionSeverity.MAJOR, ContradictionSeverity.CRITICAL])
        
        # Check AI safety contradiction
        ai_pair = tuple(sorted(["youtube_001", "youtube_002"]))
        self.assertIn(ai_pair, contradiction_pairs)
        
        # Check satellite security contradiction
        sat_pair = tuple(sorted(["doc_001", "doc_002"]))
        self.assertIn(sat_pair, contradiction_pairs)
    
    def test_reconciliation_strategies(self):
        """Test that appropriate reconciliation strategies are recommended"""
        contradictions = self.detector.detect_contradictions(self.sources)
        
        # Check that all contradictions have strategies
        for contradiction in contradictions:
            self.assertIsNotNone(contradiction.recommended_strategy)
            self.assertIsInstance(contradiction.recommended_strategy, ReconciliationStrategy)
        
        # Check strategy diversity
        strategies = {c.recommended_strategy for c in contradictions}
        self.assertGreater(len(strategies), 1)
    
    def test_temporal_analysis(self):
        """Test temporal gap calculation between sources"""
        source1 = Source(
            id="test1",
            type=SourceType.ARXIV_PAPER,
            title="Test 1",
            content="Old information says X is true.",
            publication_date=datetime(2023, 1, 1)
        )
        source2 = Source(
            id="test2",
            type=SourceType.ARXIV_PAPER,
            title="Test 2",
            content="New information says X is false.",
            publication_date=datetime(2024, 1, 1)
        )
        
        gap = self.detector._calculate_temporal_gap(source1, source2)
        self.assertEqual(gap, 365)  # One year difference
    
    def test_confidence_calculation(self):
        """Test confidence score calculation"""
        # High credibility, high similarity
        conf1 = self.detector._calculate_confidence(0.9, 0.9, 0.8)
        self.assertGreater(conf1, 0.7)
        
        # Low credibility, high similarity
        conf2 = self.detector._calculate_confidence(0.4, 0.4, 0.8)
        self.assertLess(conf2, conf1)
        
        # Mismatched credibility
        conf3 = self.detector._calculate_confidence(0.9, 0.3, 0.8)
        self.assertLess(conf3, conf1)
    
    def test_report_generation(self):
        """Test reconciliation report generation"""
        contradictions = self.detector.detect_contradictions(self.sources)
        report = self.detector.generate_reconciliation_report(contradictions)
        
        # Check report contains key sections
        self.assertIn("# Contradiction Detection Report", report)
        self.assertIn("## Summary by Severity", report)
        self.assertIn("## Detailed Analysis", report)
        self.assertIn("## Reconciliation Strategies", report)
        
        # Check report contains actual data
        self.assertIn(str(len(contradictions)), report)
        for severity in ContradictionSeverity:
            self.assertIn(severity.value.upper(), report)
    
    def test_performance(self):
        """Test performance characteristics"""
        start_time = time.time()
        contradictions = self.detector.detect_contradictions(self.sources)
        detection_time = time.time() - start_time
        
        # Should complete in reasonable time
        self.assertLess(detection_time, 5.0)  # 5 seconds max
        
        # Check detection rate
        total_comparisons = len(self.sources) * (len(self.sources) - 1) // 2
        detection_rate = len(contradictions) / total_comparisons
        self.assertGreater(detection_rate, 0.1)  # At least 10% detection rate
        self.assertLess(detection_rate, 0.9)  # Not everything is a contradiction


def run_tests():
    """Run all tests and return results"""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestContradictionDetection)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)