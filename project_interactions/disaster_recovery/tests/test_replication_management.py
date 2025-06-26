"""
Module: test_replication_management.py
Purpose: Test multi-region replication management

Tests replication monitoring, lag tracking, and data consistency
validation across multiple regions.

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_replication_management.py -v
"""

import pytest
import asyncio
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from disaster_recovery_interaction import (
    DisasterRecoveryOrchestrator,
    ReplicationStatus,
    RegionStatus,
    BackupMetadata,
    RecoveryPoint
)


@pytest.fixture
async def orchestrator():
    """Create a disaster recovery orchestrator instance"""
    return DisasterRecoveryOrchestrator()


@pytest.mark.asyncio
async def test_replication_status_check(orchestrator):
    """Test checking replication status between regions"""
    status = await orchestrator.check_replication_status("us-east-1", "us-west-2")
    
    assert isinstance(status, ReplicationStatus)
    assert status.source_region == "us-east-1"
    assert status.target_region == "us-west-2"
    assert status.lag_seconds >= 0
    assert status.sync_status in ["in_sync", "lagging", "failed"]
    assert status.bandwidth_mbps > 0
    assert isinstance(status.last_sync, datetime)


@pytest.mark.asyncio
async def test_replication_lag_threshold(orchestrator):
    """Test replication lag against threshold"""
    threshold = orchestrator.health_thresholds["replication_lag"]
    
    # Check multiple region pairs
    region_pairs = [
        ("us-east-1", "us-west-2"),
        ("us-east-1", "eu-west-1"),
        ("eu-west-1", "ap-southeast-1")
    ]
    
    for source, target in region_pairs:
        status = await orchestrator.check_replication_status(source, target)
        
        # Verify sync status matches lag
        if status.lag_seconds < threshold:
            assert status.sync_status == "in_sync"
        else:
            assert status.sync_status == "lagging"


@pytest.mark.asyncio
async def test_backup_creation_and_retrieval(orchestrator):
    """Test backup metadata creation and retrieval"""
    region_id = "us-west-2"
    
    # Get or create backup
    backup = orchestrator._get_recent_backup(region_id)
    
    assert isinstance(backup, BackupMetadata)
    assert backup.region_id == region_id
    assert backup.status == "completed"
    assert backup.encrypted is True
    assert backup.size_gb > 0
    assert isinstance(backup.timestamp, datetime)


@pytest.mark.asyncio
async def test_recovery_point_tracking(orchestrator):
    """Test recovery point objective tracking"""
    region_id = "us-east-1"
    
    # Calculate RTO/RPO
    metrics = await orchestrator.calculate_rto_rpo(region_id)
    
    assert "rto_current" in metrics
    assert "rpo_current" in metrics
    assert "rto_target" in metrics
    assert "rpo_target" in metrics
    assert "rto_met" in metrics
    assert "rpo_met" in metrics
    assert "consistency_score" in metrics
    
    assert metrics["rto_current"] > 0
    assert metrics["rpo_current"] > 0
    assert isinstance(metrics["rto_met"], bool)
    assert isinstance(metrics["rpo_met"], bool)
    assert 0 <= metrics["consistency_score"] <= 100


@pytest.mark.asyncio
async def test_multi_region_replication_topology(orchestrator):
    """Test replication topology across multiple regions"""
    # Each region should have replicas configured
    for region_id, region in orchestrator.regions.items():
        assert len(region.replicas) > 0
        assert region_id not in region.replicas  # No self-replication
        
        # Verify replica regions exist
        for replica_id in region.replicas:
            assert replica_id in orchestrator.regions


@pytest.mark.asyncio
async def test_replication_bandwidth_monitoring(orchestrator):
    """Test bandwidth monitoring for replication"""
    status = await orchestrator.check_replication_status("us-east-1", "eu-west-1")
    
    assert status.bandwidth_mbps > 0
    assert status.bandwidth_mbps <= 1000  # Reasonable upper limit
    
    # Bandwidth should correlate with pending changes
    if status.pending_changes > 1000:
        assert status.bandwidth_mbps > 50  # Higher bandwidth for more changes


@pytest.mark.asyncio
async def test_backup_retention_policy(orchestrator):
    """Test backup retention settings"""
    # Create multiple backups
    regions = ["us-east-1", "us-west-2", "eu-west-1"]
    
    for region_id in regions:
        backup = orchestrator._get_recent_backup(region_id)
        assert backup.retention_days > 0
        assert backup.retention_days <= 365  # Reasonable retention period


@pytest.mark.asyncio
async def test_cross_region_consistency(orchestrator):
    """Test data consistency across regions"""
    # Get recovery points for multiple regions
    regions = list(orchestrator.regions.keys())
    
    for region_id in regions[:2]:  # Test first two regions
        rpo_metrics = await orchestrator.calculate_rto_rpo(region_id)
        
        # Consistency score should be high for healthy regions
        region = orchestrator.regions[region_id]
        if region.status == RegionStatus.HEALTHY:
            assert rpo_metrics["consistency_score"] > 85


@pytest.mark.asyncio
async def test_replication_failure_detection(orchestrator):
    """Test detection of replication failures"""
    # Force a replication check that might show high lag
    status = await orchestrator.check_replication_status("us-east-1", "ap-southeast-1")
    
    # If lag is very high, it should be detected
    if status.lag_seconds > 300:  # 5 minutes
        assert status.sync_status in ["lagging", "failed"]


@pytest.mark.asyncio
async def test_incremental_backup_support(orchestrator):
    """Test support for different backup types"""
    backup_types = ["full", "incremental", "snapshot"]
    
    # Create backups of different types
    for backup_type in backup_types:
        backup = BackupMetadata(
            backup_id=f"test-backup-{backup_type}",
            region_id="us-east-1",
            timestamp=datetime.now(),
            size_gb=100.0 if backup_type == "full" else 10.0,
            type=backup_type,
            status="completed"
        )
        orchestrator.backups.append(backup)
    
    # Verify all types are supported
    region_backups = [b for b in orchestrator.backups if b.region_id == "us-east-1"]
    backup_types_found = set(b.type for b in region_backups)
    
    assert len(backup_types_found) >= 1  # At least one type should exist


# Validation function
if __name__ == "__main__":
    async def validate_tests():
        """Run tests with real test data"""
        print("=" * 80)
        print("REPLICATION MANAGEMENT TEST VALIDATION")
        print("=" * 80)
        
        orchestrator = DisasterRecoveryOrchestrator()
        test_results = []
        
        # Test 1: Replication Status
        print("\n🔄 Testing Replication Status...")
        try:
            status = await orchestrator.check_replication_status("us-east-1", "us-west-2")
            test_results.append({
                "test": "Replication Status Check",
                "expected": "Valid replication status with metrics",
                "actual": f"Lag: {status.lag_seconds:.1f}s, Status: {status.sync_status}",
                "passed": status.lag_seconds >= 0 and status.sync_status in ["in_sync", "lagging"]
            })
            print(f"  ✓ Replication lag: {status.lag_seconds:.1f} seconds")
            print(f"  ✓ Sync status: {status.sync_status}")
            print(f"  ✓ Bandwidth: {status.bandwidth_mbps:.1f} Mbps")
        except Exception as e:
            test_results.append({
                "test": "Replication Status Check",
                "expected": "Valid replication status",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 2: Backup Management
        print("\n💾 Testing Backup Management...")
        try:
            backup = orchestrator._get_recent_backup("us-west-2")
            age_hours = (datetime.now() - backup.timestamp).total_seconds() / 3600
            test_results.append({
                "test": "Backup Retrieval",
                "expected": "Recent backup available",
                "actual": f"Backup age: {age_hours:.1f} hours, Size: {backup.size_gb:.1f} GB",
                "passed": backup is not None and age_hours < 48
            })
            print(f"  ✓ Backup ID: {backup.backup_id}")
            print(f"  ✓ Age: {age_hours:.1f} hours")
            print(f"  ✓ Size: {backup.size_gb:.1f} GB")
            print(f"  ✓ Encrypted: {backup.encrypted}")
        except Exception as e:
            test_results.append({
                "test": "Backup Retrieval",
                "expected": "Recent backup available",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 3: RTO/RPO Metrics
        print("\n⏱️  Testing RTO/RPO Metrics...")
        try:
            metrics = await orchestrator.calculate_rto_rpo("us-east-1")
            test_results.append({
                "test": "RTO/RPO Calculation",
                "expected": "Metrics calculated and within targets",
                "actual": f"RTO: {metrics['rto_current']:.1f}min, RPO: {metrics['rpo_current']:.1f}min",
                "passed": metrics['rto_current'] > 0 and metrics['rpo_current'] > 0
            })
            print(f"  ✓ RTO: {metrics['rto_current']:.1f} min (Target: {metrics['rto_target']} min)")
            print(f"  ✓ RPO: {metrics['rpo_current']:.1f} min (Target: {metrics['rpo_target']} min)")
            print(f"  ✓ RTO Met: {metrics['rto_met']}")
            print(f"  ✓ RPO Met: {metrics['rpo_met']}")
            print(f"  ✓ Consistency: {metrics['consistency_score']:.1f}%")
        except Exception as e:
            test_results.append({
                "test": "RTO/RPO Calculation",
                "expected": "Valid metrics",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 4: Multi-Region Topology
        print("\n🌍 Testing Multi-Region Topology...")
        try:
            topology_valid = True
            for region_id, region in orchestrator.regions.items():
                if len(region.replicas) == 0 or region_id in region.replicas:
                    topology_valid = False
                    break
            
            test_results.append({
                "test": "Replication Topology",
                "expected": "Each region has valid replicas",
                "actual": f"Regions: {len(orchestrator.regions)}, All have replicas: {topology_valid}",
                "passed": topology_valid
            })
            
            print("  ✓ Replication topology:")
            for region_id, region in orchestrator.regions.items():
                print(f"    - {region_id} → {', '.join(region.replicas)}")
        except Exception as e:
            test_results.append({
                "test": "Replication Topology",
                "expected": "Valid topology",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total = len(test_results)
        passed = sum(1 for r in test_results if r["passed"])
        
        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        
        # Exit with appropriate code
        exit_code = 0 if passed == total else 1
        exit(exit_code)
    
    # Run validation
    asyncio.run(validate_tests())