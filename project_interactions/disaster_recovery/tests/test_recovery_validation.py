"""
Module: test_recovery_validation.py
Purpose: Test recovery validation and optimization

Tests disaster recovery validation, health checks, and
recovery time optimization capabilities.

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://github.com/pytest-dev/pytest-asyncio

Example Usage:
>>> pytest test_recovery_validation.py -v
"""

import pytest
import asyncio
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from disaster_recovery_interaction import (
    DisasterRecoveryOrchestrator,
    RegionStatus,
    ServiceType,
    ServiceHealth
)


@pytest.fixture
async def orchestrator():
    """Create a disaster recovery orchestrator instance"""
    return DisasterRecoveryOrchestrator()


@pytest.mark.asyncio
async def test_region_health_monitoring(orchestrator):
    """Test comprehensive region health monitoring"""
    region_id = "us-east-1"
    status = await orchestrator.monitor_region_health(region_id)
    
    assert isinstance(status, RegionStatus)
    assert status in [RegionStatus.HEALTHY, RegionStatus.DEGRADED, 
                     RegionStatus.CRITICAL, RegionStatus.FAILED]
    
    region = orchestrator.regions[region_id]
    assert region.last_health_check is not None
    assert "availability" in region.metrics
    assert "avg_response_time" in region.metrics
    assert "avg_error_rate" in region.metrics
    assert region.metrics["availability"] >= 0
    assert region.metrics["availability"] <= 100


@pytest.mark.asyncio
async def test_service_health_checks(orchestrator):
    """Test individual service health monitoring"""
    region_id = "us-west-2"
    await orchestrator.monitor_region_health(region_id)
    
    region = orchestrator.regions[region_id]
    
    # Check each service type
    for service_type in ServiceType:
        assert service_type in region.services
        health = region.services[service_type]
        
        assert isinstance(health, ServiceHealth)
        assert health.response_time_ms >= 0
        assert health.error_rate >= 0
        assert health.throughput >= 0
        assert health.throughput <= 100
        assert isinstance(health.last_check, datetime)


@pytest.mark.asyncio
async def test_disaster_recovery_validation(orchestrator):
    """Test comprehensive DR validation"""
    dr_test = await orchestrator.test_disaster_recovery("us-east-1", "us-west-2")
    
    assert "source_region" in dr_test
    assert "target_region" in dr_test
    assert "timestamp" in dr_test
    assert "tests" in dr_test
    assert "overall_ready" in dr_test
    assert "readiness_score" in dr_test
    
    # Check individual test results
    expected_tests = ["region_health", "replication", "backup", "network", "dependencies"]
    for test_name in expected_tests:
        assert test_name in dr_test["tests"]
        assert "passed" in dr_test["tests"][test_name]
    
    assert 0 <= dr_test["readiness_score"] <= 100


@pytest.mark.asyncio
async def test_network_connectivity_validation(orchestrator):
    """Test network connectivity checks"""
    network_test = await orchestrator._test_network_connectivity("us-east-1", "eu-west-1")
    
    assert "latency_ms" in network_test
    assert "packet_loss" in network_test
    assert "bandwidth_mbps" in network_test
    assert "passed" in network_test
    
    assert network_test["latency_ms"] > 0
    assert network_test["packet_loss"] >= 0
    assert network_test["bandwidth_mbps"] > 0


@pytest.mark.asyncio
async def test_service_dependency_validation(orchestrator):
    """Test service dependency checks"""
    dep_test = await orchestrator._test_service_dependencies("us-west-2")
    
    assert "total_services" in dep_test
    assert "available_services" in dep_test
    assert "critical_services_ok" in dep_test
    assert "passed" in dep_test
    
    assert dep_test["total_services"] > 0
    assert dep_test["available_services"] <= dep_test["total_services"]


@pytest.mark.asyncio
async def test_recovery_time_optimization(orchestrator):
    """Test recovery time optimization suggestions"""
    optimization = await orchestrator.optimize_recovery_time("us-east-1")
    
    assert "region" in optimization
    assert "timestamp" in optimization
    assert "improvements" in optimization
    assert "status" in optimization
    
    assert optimization["region"] == "us-east-1"
    assert optimization["status"] in ["applied", "no_improvements_needed"]
    
    if optimization["improvements"]:
        for improvement in optimization["improvements"]:
            assert "type" in improvement
            assert "action" in improvement
            assert "impact" in improvement


@pytest.mark.asyncio
async def test_health_threshold_enforcement(orchestrator):
    """Test health threshold enforcement"""
    region_id = "us-east-1"
    await orchestrator.monitor_region_health(region_id)
    
    region = orchestrator.regions[region_id]
    
    # Check if status aligns with thresholds
    availability = region.metrics["availability"]
    
    if availability >= orchestrator.health_thresholds["availability"]:
        assert region.status == RegionStatus.HEALTHY
    elif availability >= 80:
        assert region.status == RegionStatus.DEGRADED
    elif availability >= 50:
        assert region.status == RegionStatus.CRITICAL
    else:
        assert region.status == RegionStatus.FAILED


@pytest.mark.asyncio
async def test_multi_region_health_comparison(orchestrator):
    """Test health comparison across regions"""
    health_statuses = {}
    
    for region_id in orchestrator.regions:
        status = await orchestrator.monitor_region_health(region_id)
        health_statuses[region_id] = status
    
    # At least one region should be healthy
    healthy_regions = [r for r, s in health_statuses.items() 
                      if s == RegionStatus.HEALTHY]
    assert len(healthy_regions) > 0


@pytest.mark.asyncio
async def test_recovery_validation_edge_cases(orchestrator):
    """Test edge cases in recovery validation"""
    # Test with same source and target
    with pytest.raises(ValueError):
        await orchestrator.execute_failover("us-east-1", "us-east-1")
    
    # Test with non-existent regions
    with pytest.raises(ValueError):
        await orchestrator.execute_failover("us-east-1", "non-existent")


@pytest.mark.asyncio
async def test_optimization_impact_tracking(orchestrator):
    """Test tracking of optimization impacts"""
    optimization = await orchestrator.optimize_recovery_time("us-west-2")
    
    if optimization["improvements"]:
        assert "expected_improvement" in optimization
        assert "rto_reduction_percent" in optimization["expected_improvement"]
        assert "rpo_reduction_percent" in optimization["expected_improvement"]
        
        # Improvements should be positive
        assert optimization["expected_improvement"]["rto_reduction_percent"] > 0
        assert optimization["expected_improvement"]["rpo_reduction_percent"] > 0


# Validation function
if __name__ == "__main__":
    async def validate_tests():
        """Run tests with real test data"""
        print("=" * 80)
        print("RECOVERY VALIDATION TEST VALIDATION")
        print("=" * 80)
        
        orchestrator = DisasterRecoveryOrchestrator()
        test_results = []
        
        # Test 1: Region Health Monitoring
        print("\n🏥 Testing Region Health Monitoring...")
        try:
            health_data = {}
            for region_id in ["us-east-1", "us-west-2", "eu-west-1"]:
                status = await orchestrator.monitor_region_health(region_id)
                region = orchestrator.regions[region_id]
                health_data[region_id] = {
                    "status": status,
                    "availability": region.metrics.get("availability", 0)
                }
            
            all_monitored = all(d["status"] is not None for d in health_data.values())
            test_results.append({
                "test": "Region Health Monitoring",
                "expected": "All regions monitored successfully",
                "actual": f"Monitored {len(health_data)} regions",
                "passed": all_monitored
            })
            
            for region_id, data in health_data.items():
                print(f"  ✓ {region_id}: {data['status'].value} ({data['availability']:.1f}% available)")
        except Exception as e:
            test_results.append({
                "test": "Region Health Monitoring",
                "expected": "Successful monitoring",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 2: DR Validation
        print("\n🧪 Testing Disaster Recovery Validation...")
        try:
            dr_test = await orchestrator.test_disaster_recovery("us-east-1", "us-west-2")
            test_results.append({
                "test": "DR Validation",
                "expected": "Complete DR readiness assessment",
                "actual": f"Readiness: {dr_test['readiness_score']:.1f}%, Ready: {dr_test['overall_ready']}",
                "passed": "readiness_score" in dr_test and dr_test["readiness_score"] >= 0
            })
            
            print(f"  ✓ Overall readiness: {dr_test['readiness_score']:.1f}%")
            print("  ✓ Test results:")
            for test_name, result in dr_test["tests"].items():
                print(f"    - {test_name}: {'✓ Pass' if result['passed'] else '✗ Fail'}")
        except Exception as e:
            test_results.append({
                "test": "DR Validation",
                "expected": "Complete assessment",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 3: Recovery Optimization
        print("\n🔧 Testing Recovery Time Optimization...")
        try:
            optimization = await orchestrator.optimize_recovery_time("us-west-2")
            has_improvements = len(optimization["improvements"]) > 0
            
            test_results.append({
                "test": "Recovery Optimization",
                "expected": "Optimization analysis completed",
                "actual": f"Status: {optimization['status']}, Improvements: {len(optimization['improvements'])}",
                "passed": optimization["status"] in ["applied", "no_improvements_needed"]
            })
            
            print(f"  ✓ Optimization status: {optimization['status']}")
            if has_improvements:
                print(f"  ✓ Found {len(optimization['improvements'])} improvements:")
                for imp in optimization["improvements"]:
                    print(f"    - {imp['type']}: {imp['action']} ({imp['impact']})")
        except Exception as e:
            test_results.append({
                "test": "Recovery Optimization",
                "expected": "Optimization analysis",
                "actual": f"Exception: {str(e)}",
                "passed": False
            })
        
        # Test 4: Service Health Checks
        print("\n💊 Testing Service Health Checks...")
        try:
            await orchestrator.monitor_region_health("us-east-1")
            region = orchestrator.regions["us-east-1"]
            
            all_services_checked = all(
                hasattr(health, 'last_check') and health.last_check is not None
                for health in region.services.values()
            )
            
            healthy_services = sum(1 for h in region.services.values() if h.healthy)
            
            test_results.append({
                "test": "Service Health Checks",
                "expected": "All services checked",
                "actual": f"Checked {len(region.services)} services, {healthy_services} healthy",
                "passed": all_services_checked
            })
            
            print(f"  ✓ Services checked: {len(region.services)}")
            print(f"  ✓ Healthy services: {healthy_services}")
            for service_type, health in region.services.items():
                status = "✓" if health.healthy else "✗"
                print(f"    {status} {service_type.value}: {health.response_time_ms:.1f}ms")
        except Exception as e:
            test_results.append({
                "test": "Service Health Checks",
                "expected": "All services checked",
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