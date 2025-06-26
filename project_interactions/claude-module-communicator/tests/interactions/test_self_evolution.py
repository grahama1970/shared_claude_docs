"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test module for claude-module-communicator self-evolution capabilities.

These tests validate GRANGER Task #001 requirements:
- Self-evolution discovers improvement (Test 001.1)
- Approval gate blocks unapproved changes (Test 001.2)  
- Rollback failed evolution (Test 001.3)
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import pytest
import time
import json
from pathlib import Path
# REMOVED: # REMOVED: from unittest.mock import patch, MagicMock

from .self_evolution_interaction import SelfEvolutionScenario


class TestSelfEvolution:
    """Test suite for self-evolution capabilities."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary file paths."""
        scenario = SelfEvolutionScenario()
        scenario.evolution_history_file = tmp_path / "evolution_history.json"
        scenario.approval_queue_file = tmp_path / "approval_queue.json"
        return scenario
    
    def test_discovers_improvement(self, scenario):
        """
        Test 001.1: Self-evolution discovers improvement.
        Expected duration: 2.0s-10.0s
        """
        start_time = time.time()
        
        # Execute discovery with real ArXiv API
        result = scenario.discover_improvement("multi-agent coordination")
        
        duration = time.time() - start_time
        
        # Assertions
        assert result.success, f"Discovery failed: {result.error}"
        assert 2.0 <= duration <= 10.0, f"Duration {duration}s outside expected range"
        assert len(result.output_data.get("papers", [])) > 0, "No papers found"
        assert len(result.output_data.get("proposed_improvements", [])) > 0, "No improvements proposed"
        
        # Validate paper structure
        for paper in result.output_data["papers"]:
            assert "id" in paper
            assert "title" in paper
            assert "summary" in paper
            assert "authors" in paper
            assert len(paper["summary"]) <= 500  # Truncated as expected
        
        # Validate improvement structure
        for improvement in result.output_data["proposed_improvements"]:
            assert "paper_id" in improvement
            assert "technique" in improvement
            assert "confidence" in improvement
            assert 0.5 <= improvement["confidence"] <= 1.0  # Realistic confidence
            assert "proposed_changes" in improvement
            assert len(improvement["proposed_changes"]) > 0
    
    def test_approval_gate(self, scenario):
        """
        Test 001.2: Approval gate blocks unapproved changes.
        Expected duration: 0.1s-2.0s
        """
        start_time = time.time()
        
        # Create a proposal
        improvements = [{
            "paper_id": "test_paper_001",
            "technique": "Test Technique",
            "confidence": 0.85,
            "proposed_changes": ["Change 1", "Change 2"]
        }]
        
        proposal_result = scenario.create_evolution_proposal(improvements)
        assert proposal_result.success
        
        proposal_id = proposal_result.output_data["proposal"]["id"]
        
        # Try to implement without approval (should fail)
        implementation_result = scenario.implement_evolution(proposal_id)
        
        duration = time.time() - start_time
        
        # Assertions
        assert not implementation_result.success, "Should not implement unapproved proposal"
        assert implementation_result.error == "Proposal not approved"
        assert 0.1 <= duration <= 2.0, f"Duration {duration}s outside expected range"
        
        # Verify proposal is still pending
        status_result = scenario.check_approval_status(proposal_id)
        assert status_result.success
        assert status_result.output_data["status"] == "pending_approval"
        
        # Wait for auto-approval
        time.sleep(11)
        
        # Now implementation should succeed
        implementation_result = scenario.implement_evolution(proposal_id)
        assert implementation_result.success, "Should implement approved proposal"
    
    def test_rollback(self, scenario):
        """
        Test 001.3: Rollback failed evolution.
        Expected duration: 0.5s-3.0s
        """
        # First, create and implement an evolution
        improvements = [{
            "paper_id": "test_paper_002",
            "technique": "Risky Technique",
            "confidence": 0.75,
            "proposed_changes": [
                "Update core algorithm",
                "Modify consensus mechanism",
                "Change coordinator logic"
            ]
        }]
        
        proposal_result = scenario.create_evolution_proposal(improvements)
        assert proposal_result.success
        
        proposal_id = proposal_result.output_data["proposal"]["id"]
        
        # Wait for auto-approval
        time.sleep(11)
        
        # Implement the evolution
        implementation_result = scenario.implement_evolution(proposal_id)
        assert implementation_result.success
        
        # Now test rollback
        start_time = time.time()
        
        rollback_result = scenario.rollback_evolution(proposal_id)
        
        duration = time.time() - start_time
        
        # Assertions
        assert rollback_result.success, f"Rollback failed: {rollback_result.error}"
        assert 0.5 <= duration <= 3.0, f"Duration {duration}s outside expected range"
        assert rollback_result.output_data["files_restored"] > 0
        assert "config_restored" in rollback_result.output_data
        assert len(rollback_result.output_data["rollback_log"]) > 0
        
        # Verify rollback is recorded in history
        history = scenario._load_evolution_history()
        evolution = next((h for h in history if h["proposal_id"] == proposal_id), None)
        assert evolution is not None
        assert evolution["rollback_performed"]
        assert not evolution["rollback_available"]  # Can't rollback twice
        
        # Verify second rollback fails
        second_rollback = scenario.rollback_evolution(proposal_id)
        assert not second_rollback.success
        assert "not available" in second_rollback.error


class TestHoneypot:
    """Honeypot tests designed to catch fake test implementations."""
    
    @pytest.fixture
    def scenario(self, tmp_path):
        """Create a scenario with temporary file paths."""
        scenario = SelfEvolutionScenario()
        scenario.evolution_history_file = tmp_path / "evolution_history.json"
        scenario.approval_queue_file = tmp_path / "approval_queue.json"
        return scenario
    
    def test_evolution_without_research(self, scenario):
        """
        Test 001.H: HONEYPOT - Evolution without research.
        This test SHOULD FAIL - attempting evolution without discovery.
        """
        # Try to create proposal without any improvements (no research)
        empty_improvements = []
        
        proposal_result = scenario.create_evolution_proposal(empty_improvements)
        
        # This should succeed (creating empty proposal)
        assert proposal_result.success
        
        # But the proposal should have high risk and no real changes
        proposal = proposal_result.output_data["proposal"]
        assert proposal["risk_assessment"]["score"] == 0  # No changes = no risk
        assert len(proposal["improvements"]) == 0
        
        # Now let's create a fake improvement without research
        fake_improvements = [{
            "paper_id": None,  # No paper!
            "technique": "Made Up Technique",
            "confidence": 1.0,  # Suspiciously high
            "proposed_changes": ["Random change without research"]
        }]
        
        # This should raise concerns in a real system
        # For testing, we'll check that the system handles this poorly
        with pytest.raises(Exception) as exc_info:
            # In a proper implementation, this would validate paper_id exists
            # For now, it will fail when trying to implement without valid research
            proposal_result = scenario.create_evolution_proposal(fake_improvements)
            proposal_id = proposal_result.output_data["proposal"]["id"]
            
            # Force approval (bypass gate)
            queue = scenario._load_approval_queue()
            for p in queue:
                if p["id"] == proposal_id:
                    p["status"] = "approved"
            scenario._save_approval_queue(queue)
            
            # This should fail spectacularly
            scenario.implement_evolution(proposal_id)
        
        # The test "passes" by failing - this is the honeypot
        assert False, "Honeypot test should have detected evolution without research"


if __name__ == "__main__":
    # Run tests with detailed output
    pytest.main([__file__, "-v", "--tb=short"])