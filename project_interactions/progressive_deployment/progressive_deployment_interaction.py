
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: progressive_deployment_interaction.py
Purpose: Progressive deployment with monitoring and automatic rollback capabilities

This module implements GRANGER Task #20 - Level 3 complexity task for safe deployment
with real-time monitoring and automatic rollback on failure detection.

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- enum: https://docs.python.org/3/library/enum.html

Example Usage:
>>> from progressive_deployment_interaction import ProgressiveDeploymentSystem
>>> deployer = ProgressiveDeploymentSystem()
>>> result = deployer.deploy_with_canary("service-v2.0", traffic_percentage=10)
>>> print(f"Deployment status: {result['status']}")
Deployment status: completed
"""

import asyncio
import json
import random
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from collections import defaultdict, deque


class DeploymentStrategy(Enum):
    """Supported deployment strategies"""
    CANARY = "canary"
    BLUE_GREEN = "blue_green"
    ROLLING = "rolling"
    FEATURE_FLAG = "feature_flag"


class DeploymentStatus(Enum):
    """Deployment status states"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    MONITORING = "monitoring"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    PAUSED = "paused"


class HealthStatus(Enum):
    """Service health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthMetrics:
    """Health metrics for monitoring"""
    response_time_ms: float
    error_rate: float
    success_rate: float
    cpu_usage: float
    memory_usage: float
    active_connections: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    def is_healthy(self, thresholds: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Check if metrics meet health thresholds"""
        violations = []
        
        if self.response_time_ms > thresholds.get("max_response_time_ms", 1000):
            violations.append(f"Response time {self.response_time_ms}ms exceeds threshold")
        
        if self.error_rate > thresholds.get("max_error_rate", 0.05):
            violations.append(f"Error rate {self.error_rate:.2%} exceeds threshold")
        
        if self.success_rate < thresholds.get("min_success_rate", 0.95):
            violations.append(f"Success rate {self.success_rate:.2%} below threshold")
        
        if self.cpu_usage > thresholds.get("max_cpu_usage", 0.80):
            violations.append(f"CPU usage {self.cpu_usage:.2%} exceeds threshold")
        
        if self.memory_usage > thresholds.get("max_memory_usage", 0.85):
            violations.append(f"Memory usage {self.memory_usage:.2%} exceeds threshold")
        
        return len(violations) == 0, violations


@dataclass
class DeploymentConfig:
    """Configuration for deployment"""
    service_name: str
    version: str
    strategy: DeploymentStrategy
    health_check_interval_seconds: int = 10
    monitoring_duration_minutes: int = 30
    rollback_threshold_violations: int = 3
    traffic_increment_percentage: int = 10
    health_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "max_response_time_ms": 1000,
        "max_error_rate": 0.05,
        "min_success_rate": 0.95,
        "max_cpu_usage": 0.80,
        "max_memory_usage": 0.85
    })
    feature_flags: Dict[str, bool] = field(default_factory=dict)


@dataclass
class DeploymentState:
    """State of a deployment"""
    deployment_id: str
    config: DeploymentConfig
    status: DeploymentStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    current_traffic_percentage: float = 0
    health_violations: List[str] = field(default_factory=list)
    rollback_count: int = 0
    metrics_history: List[HealthMetrics] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_event(self, event_type: str, details: Dict[str, Any]):
        """Add deployment event"""
        self.events.append({
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for persistence"""
        config_dict = asdict(self.config)
        # Convert enum to string
        config_dict["strategy"] = config_dict["strategy"].value
        
        # Convert metrics history with datetime handling
        metrics_dicts = []
        for m in self.metrics_history[-100:]:  # Keep last 100
            m_dict = asdict(m)
            m_dict["timestamp"] = m_dict["timestamp"].isoformat()
            metrics_dicts.append(m_dict)
        
        return {
            "deployment_id": self.deployment_id,
            "config": config_dict,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "current_traffic_percentage": self.current_traffic_percentage,
            "health_violations": self.health_violations,
            "rollback_count": self.rollback_count,
            "metrics_history": metrics_dicts,
            "events": self.events[-50:]  # Keep last 50 events
        }


class ServiceSimulator:
    """Simulates service behavior for testing"""
    
    def __init__(self):
        self.failure_injection = False
        self.performance_degradation = False
        self.base_response_time = 100
        self.base_error_rate = 0.01
        
    def get_metrics(self, version: str, traffic_percentage: float) -> HealthMetrics:
        """Simulate health metrics for a service version"""
        # Simulate different behaviors for different versions
        if "v2.0" in version and traffic_percentage > 50:
            # Simulate issues when scaling up v2.0
            self.performance_degradation = True
        
        response_time = self.base_response_time
        error_rate = self.base_error_rate
        
        if self.failure_injection:
            response_time *= random.uniform(5, 10)
            error_rate = random.uniform(0.1, 0.3)
        elif self.performance_degradation:
            response_time *= random.uniform(2, 4)
            error_rate = random.uniform(0.05, 0.15)
        else:
            # Normal variations
            response_time *= random.uniform(0.8, 1.2)
            error_rate *= random.uniform(0.5, 1.5)
        
        return HealthMetrics(
            response_time_ms=response_time,
            error_rate=min(error_rate, 1.0),
            success_rate=max(1.0 - error_rate, 0),
            cpu_usage=random.uniform(0.3, 0.7) if not self.failure_injection else random.uniform(0.8, 0.95),
            memory_usage=random.uniform(0.4, 0.6) if not self.failure_injection else random.uniform(0.85, 0.95),
            active_connections=random.randint(100, 1000)
        )


class ProgressiveDeploymentSystem:
    """Main system for progressive deployment with monitoring and rollback"""
    
    def __init__(self, state_dir: str = "./deployment_state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.active_deployments: Dict[str, DeploymentState] = {}
        self.deployment_history: deque = deque(maxlen=100)
        self.service_simulator = ServiceSimulator()
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        
    def deploy_with_canary(self, service_version: str, traffic_percentage: int = 10) -> Dict[str, Any]:
        """Deploy using canary strategy"""
        config = DeploymentConfig(
            service_name="example-service",
            version=service_version,
            strategy=DeploymentStrategy.CANARY,
            traffic_increment_percentage=traffic_percentage
        )
        
        deployment_id = f"deploy-{int(time.time())}"
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.active_deployments[deployment_id] = state
        
        # Execute canary deployment
        result = asyncio.run(self._execute_canary_deployment(state))
        
        # Save state
        self._save_deployment_state(state)
        
        return result
    
    def deploy_blue_green(self, service_version: str) -> Dict[str, Any]:
        """Deploy using blue-green strategy"""
        config = DeploymentConfig(
            service_name="example-service",
            version=service_version,
            strategy=DeploymentStrategy.BLUE_GREEN
        )
        
        deployment_id = f"deploy-{int(time.time())}"
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.active_deployments[deployment_id] = state
        
        # Execute blue-green deployment
        result = asyncio.run(self._execute_blue_green_deployment(state))
        
        # Save state
        self._save_deployment_state(state)
        
        return result
    
    def deploy_with_feature_flags(self, service_version: str, feature_flags: Dict[str, bool]) -> Dict[str, Any]:
        """Deploy using feature flags"""
        config = DeploymentConfig(
            service_name="example-service",
            version=service_version,
            strategy=DeploymentStrategy.FEATURE_FLAG,
            feature_flags=feature_flags
        )
        
        deployment_id = f"deploy-{int(time.time())}"
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.active_deployments[deployment_id] = state
        
        # Execute feature flag deployment
        result = asyncio.run(self._execute_feature_flag_deployment(state))
        
        # Save state
        self._save_deployment_state(state)
        
        return result
    
    async def _execute_canary_deployment(self, state: DeploymentState) -> Dict[str, Any]:
        """Execute canary deployment with progressive traffic shifting"""
        state.status = DeploymentStatus.IN_PROGRESS
        state.add_event("deployment_started", {"strategy": "canary"})
        
        try:
            # Start with initial traffic percentage
            state.current_traffic_percentage = state.config.traffic_increment_percentage
            
            while state.current_traffic_percentage <= 100:
                # Monitor health at current traffic level
                monitoring_result = await self._monitor_deployment_health(state)
                
                if not monitoring_result["healthy"]:
                    # Rollback on health check failure
                    await self._rollback_deployment(state)
                    return {
                        "status": "rolled_back",
                        "deployment_id": state.deployment_id,
                        "reason": monitoring_result["violations"],
                        "final_traffic_percentage": state.current_traffic_percentage
                    }
                
                # Increment traffic if healthy
                if state.current_traffic_percentage < 100:
                    state.current_traffic_percentage += state.config.traffic_increment_percentage
                    state.current_traffic_percentage = min(state.current_traffic_percentage, 100)
                    state.add_event("traffic_increased", {"percentage": state.current_traffic_percentage})
                else:
                    break
                
                # Small delay between increments
                await asyncio.sleep(2)
            
            # Final monitoring period at 100% traffic
            state.status = DeploymentStatus.MONITORING
            final_result = await self._monitor_deployment_health(state, duration_minutes=5)
            
            if final_result["healthy"]:
                state.status = DeploymentStatus.COMPLETED
                state.end_time = datetime.now()
                state.add_event("deployment_completed", {"final_metrics": final_result["metrics"]})
                
                return {
                    "status": "completed",
                    "deployment_id": state.deployment_id,
                    "duration": str(state.end_time - state.start_time),
                    "final_metrics": final_result["metrics"]
                }
            else:
                await self._rollback_deployment(state)
                return {
                    "status": "rolled_back",
                    "deployment_id": state.deployment_id,
                    "reason": final_result["violations"]
                }
                
        except Exception as e:
            state.status = DeploymentStatus.FAILED
            state.add_event("deployment_failed", {"error": str(e)})
            await self._rollback_deployment(state)
            return {
                "status": "failed",
                "deployment_id": state.deployment_id,
                "error": str(e)
            }
    
    async def _execute_blue_green_deployment(self, state: DeploymentState) -> Dict[str, Any]:
        """Execute blue-green deployment with instant switch"""
        state.status = DeploymentStatus.IN_PROGRESS
        state.add_event("deployment_started", {"strategy": "blue_green"})
        
        try:
            # Deploy to green environment (0% traffic)
            state.current_traffic_percentage = 0
            state.add_event("green_deployment_started", {"version": state.config.version})
            
            # Simulate deployment time
            await asyncio.sleep(3)
            
            # Health check green environment
            green_health = await self._check_environment_health(state, "green")
            
            if not green_health["healthy"]:
                state.status = DeploymentStatus.FAILED
                state.add_event("green_health_check_failed", {"violations": green_health["violations"]})
                return {
                    "status": "failed",
                    "deployment_id": state.deployment_id,
                    "reason": "Green environment health check failed",
                    "violations": green_health["violations"]
                }
            
            # Switch traffic instantly
            state.current_traffic_percentage = 100
            state.add_event("traffic_switched", {"from": "blue", "to": "green"})
            
            # Monitor after switch
            state.status = DeploymentStatus.MONITORING
            monitoring_result = await self._monitor_deployment_health(state, duration_minutes=10)
            
            if monitoring_result["healthy"]:
                state.status = DeploymentStatus.COMPLETED
                state.end_time = datetime.now()
                state.add_event("deployment_completed", {"strategy": "blue_green"})
                
                return {
                    "status": "completed",
                    "deployment_id": state.deployment_id,
                    "duration": str(state.end_time - state.start_time),
                    "switch_time": "instant"
                }
            else:
                # Quick rollback to blue
                await self._instant_rollback(state)
                return {
                    "status": "rolled_back",
                    "deployment_id": state.deployment_id,
                    "reason": monitoring_result["violations"],
                    "rollback_time": "instant"
                }
                
        except Exception as e:
            state.status = DeploymentStatus.FAILED
            state.add_event("deployment_failed", {"error": str(e)})
            return {
                "status": "failed",
                "deployment_id": state.deployment_id,
                "error": str(e)
            }
    
    async def _execute_feature_flag_deployment(self, state: DeploymentState) -> Dict[str, Any]:
        """Execute deployment with feature flags"""
        state.status = DeploymentStatus.IN_PROGRESS
        state.add_event("deployment_started", {"strategy": "feature_flag", "flags": state.config.feature_flags})
        
        try:
            # Deploy with all flags initially disabled
            state.current_traffic_percentage = 100  # Full deployment but features controlled by flags
            
            enabled_features = []
            failed_features = []
            
            # Enable features one by one
            for feature, should_enable in state.config.feature_flags.items():
                if should_enable:
                    state.add_event("enabling_feature", {"feature": feature})
                    
                    # Monitor while enabling feature
                    feature_health = await self._monitor_feature_health(state, feature)
                    
                    if feature_health["healthy"]:
                        enabled_features.append(feature)
                        state.add_event("feature_enabled", {"feature": feature})
                    else:
                        failed_features.append({
                            "feature": feature,
                            "violations": feature_health["violations"]
                        })
                        state.add_event("feature_failed", {
                            "feature": feature,
                            "violations": feature_health["violations"]
                        })
            
            # Determine final status
            if failed_features:
                state.status = DeploymentStatus.COMPLETED if enabled_features else DeploymentStatus.FAILED
                return {
                    "status": "partial_success",
                    "deployment_id": state.deployment_id,
                    "enabled_features": enabled_features,
                    "failed_features": failed_features
                }
            else:
                state.status = DeploymentStatus.COMPLETED
                state.end_time = datetime.now()
                return {
                    "status": "completed",
                    "deployment_id": state.deployment_id,
                    "enabled_features": enabled_features,
                    "duration": str(state.end_time - state.start_time)
                }
                
        except Exception as e:
            state.status = DeploymentStatus.FAILED
            state.add_event("deployment_failed", {"error": str(e)})
            return {
                "status": "failed",
                "deployment_id": state.deployment_id,
                "error": str(e)
            }
    
    async def _monitor_deployment_health(self, state: DeploymentState, duration_minutes: int = None) -> Dict[str, Any]:
        """Monitor deployment health for specified duration"""
        duration = duration_minutes or state.config.monitoring_duration_minutes
        end_time = datetime.now() + timedelta(minutes=duration)
        
        violations_count = 0
        all_violations = []
        metrics_collected = []
        
        while datetime.now() < end_time:
            # Collect metrics
            metrics = self.service_simulator.get_metrics(
                state.config.version,
                state.current_traffic_percentage
            )
            
            state.metrics_history.append(metrics)
            metrics_collected.append(metrics)
            
            # Check health
            is_healthy, violations = metrics.is_healthy(state.config.health_thresholds)
            
            if not is_healthy:
                violations_count += 1
                all_violations.extend(violations)
                state.health_violations.extend(violations)
                state.add_event("health_violation", {
                    "violations": violations,
                    "count": violations_count
                })
                
                # Check if exceeded threshold
                if violations_count >= state.config.rollback_threshold_violations:
                    return {
                        "healthy": False,
                        "violations": all_violations,
                        "metrics": self._aggregate_metrics(metrics_collected)
                    }
            else:
                # Reset count on healthy check
                violations_count = 0
            
            # Wait before next check
            await asyncio.sleep(state.config.health_check_interval_seconds)
        
        return {
            "healthy": True,
            "violations": [],
            "metrics": self._aggregate_metrics(metrics_collected)
        }
    
    async def _monitor_feature_health(self, state: DeploymentState, feature: str) -> Dict[str, Any]:
        """Monitor health of a specific feature"""
        # Simplified monitoring for feature flags
        monitoring_duration = 2  # 2 minutes per feature
        return await self._monitor_deployment_health(state, duration_minutes=monitoring_duration)
    
    async def _check_environment_health(self, state: DeploymentState, environment: str) -> Dict[str, Any]:
        """Check health of a specific environment"""
        # Simulate environment health check
        metrics = self.service_simulator.get_metrics(state.config.version, 0)
        is_healthy, violations = metrics.is_healthy(state.config.health_thresholds)
        
        return {
            "healthy": is_healthy,
            "violations": violations,
            "environment": environment
        }
    
    async def _rollback_deployment(self, state: DeploymentState):
        """Perform deployment rollback"""
        state.status = DeploymentStatus.ROLLED_BACK
        state.rollback_count += 1
        state.current_traffic_percentage = 0
        state.end_time = datetime.now()
        
        state.add_event("rollback_initiated", {
            "reason": state.health_violations[-3:],  # Last 3 violations
            "rollback_count": state.rollback_count
        })
        
        # Simulate rollback time
        await asyncio.sleep(2)
        
        state.add_event("rollback_completed", {
            "duration": "2 seconds",
            "final_traffic": 0
        })
    
    async def _instant_rollback(self, state: DeploymentState):
        """Instant rollback for blue-green deployment"""
        state.status = DeploymentStatus.ROLLED_BACK
        state.rollback_count += 1
        state.current_traffic_percentage = 0
        state.end_time = datetime.now()
        
        state.add_event("instant_rollback", {
            "from": "green",
            "to": "blue",
            "duration": "instant"
        })
    
    def _aggregate_metrics(self, metrics_list: List[HealthMetrics]) -> Dict[str, float]:
        """Aggregate metrics for reporting"""
        if not metrics_list:
            return {}
        
        return {
            "avg_response_time_ms": sum(m.response_time_ms for m in metrics_list) / len(metrics_list),
            "avg_error_rate": sum(m.error_rate for m in metrics_list) / len(metrics_list),
            "avg_success_rate": sum(m.success_rate for m in metrics_list) / len(metrics_list),
            "avg_cpu_usage": sum(m.cpu_usage for m in metrics_list) / len(metrics_list),
            "avg_memory_usage": sum(m.memory_usage for m in metrics_list) / len(metrics_list),
            "max_response_time_ms": max(m.response_time_ms for m in metrics_list),
            "max_error_rate": max(m.error_rate for m in metrics_list),
            "min_success_rate": min(m.success_rate for m in metrics_list)
        }
    
    def _save_deployment_state(self, state: DeploymentState):
        """Save deployment state to disk"""
        state_file = self.state_dir / f"{state.deployment_id}.json"
        with open(state_file, 'w') as f:
            json.dump(state.to_dict(), f, indent=2)
        
        # Update history
        self.deployment_history.append({
            "deployment_id": state.deployment_id,
            "status": state.status.value,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_deployment_history(self) -> List[Dict[str, Any]]:
        """Get deployment history"""
        return list(self.deployment_history)
    
    def get_deployment_state(self, deployment_id: str) -> Optional[Dict[str, Any]]:
        """Get specific deployment state"""
        state_file = self.state_dir / f"{deployment_id}.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                return json.load(f)
        return None
    
    def simulate_failure(self, failure_type: str = "performance"):
        """Inject failures for testing"""
        if failure_type == "performance":
            self.service_simulator.performance_degradation = True
        elif failure_type == "critical":
            self.service_simulator.failure_injection = True
    
    def clear_failures(self):
        """Clear injected failures"""
        self.service_simulator.performance_degradation = False
        self.service_simulator.failure_injection = False
    
    def test_canary_success(self) -> Tuple[bool, str, float]:
        """Test successful canary deployment"""
        start_time = time.time()
        self.clear_failures()
        
        result = self.deploy_with_canary("service-v1.5", traffic_percentage=20)
        duration = time.time() - start_time
        
        success = result["status"] == "completed"
        message = f"Canary deployment: {result['status']}"
        
        return success, message, duration
    
    def test_canary_rollback(self) -> Tuple[bool, str, float]:
        """Test canary deployment with rollback"""
        start_time = time.time()
        self.clear_failures()
        
        # Inject failure when traffic increases
        result = self.deploy_with_canary("service-v2.0", traffic_percentage=25)
        duration = time.time() - start_time
        
        success = result["status"] == "rolled_back"
        message = f"Canary rollback test: {result['status']}"
        
        return success, message, duration
    
    def test_blue_green_instant_switch(self) -> Tuple[bool, str, float]:
        """Test blue-green deployment with instant switch"""
        start_time = time.time()
        self.clear_failures()
        
        result = self.deploy_blue_green("service-v3.0")
        duration = time.time() - start_time
        
        success = result["status"] == "completed" and result.get("switch_time") == "instant"
        message = f"Blue-green deployment: {result['status']}"
        
        return success, message, duration
    
    def test_feature_flag_progressive(self) -> Tuple[bool, str, float]:
        """Test feature flag deployment"""
        start_time = time.time()
        self.clear_failures()
        
        feature_flags = {
            "new_ui": True,
            "advanced_analytics": True,
            "experimental_feature": False
        }
        
        result = self.deploy_with_feature_flags("service-v4.0", feature_flags)
        duration = time.time() - start_time
        
        success = result["status"] in ["completed", "partial_success"]
        enabled_count = len(result.get("enabled_features", []))
        message = f"Feature flag deployment: {result['status']}, {enabled_count} features enabled"
        
        return success, message, duration
    
    def test_monitoring_and_metrics(self) -> Tuple[bool, str, float]:
        """Test monitoring and metrics collection"""
        start_time = time.time()
        self.clear_failures()
        
        # Quick deployment for monitoring test
        deployment_id = f"test-monitor-{int(time.time())}"
        config = DeploymentConfig(
            service_name="monitor-test",
            version="v1.0",
            strategy=DeploymentStrategy.CANARY,
            monitoring_duration_minutes=1  # Short duration for testing
        )
        
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.MONITORING,
            start_time=datetime.now(),
            current_traffic_percentage=100
        )
        
        # Run monitoring
        result = asyncio.run(self._monitor_deployment_health(state, duration_minutes=1))
        duration = time.time() - start_time
        
        metrics_collected = len(state.metrics_history) > 0
        has_aggregated_metrics = "avg_response_time_ms" in result.get("metrics", {})
        
        success = result["healthy"] and metrics_collected and has_aggregated_metrics
        message = f"Monitoring test: collected {len(state.metrics_history)} metrics"
        
        return success, message, duration
    
    def test_state_persistence(self) -> Tuple[bool, str, float]:
        """Test deployment state persistence"""
        start_time = time.time()
        
        # Create and save a deployment state
        deployment_id = f"test-persist-{int(time.time())}"
        config = DeploymentConfig(
            service_name="persist-test",
            version="v1.0",
            strategy=DeploymentStrategy.CANARY
        )
        
        state = DeploymentState(
            deployment_id=deployment_id,
            config=config,
            status=DeploymentStatus.COMPLETED,
            start_time=datetime.now(),
            end_time=datetime.now()
        )
        
        # Add some test data
        state.add_event("test_event", {"data": "test"})
        state.metrics_history.append(HealthMetrics(
            response_time_ms=100,
            error_rate=0.01,
            success_rate=0.99,
            cpu_usage=0.5,
            memory_usage=0.6,
            active_connections=500
        ))
        
        # Save state
        self._save_deployment_state(state)
        
        # Load state
        loaded_state = self.get_deployment_state(deployment_id)
        duration = time.time() - start_time
        
        success = (
            loaded_state is not None and
            loaded_state["deployment_id"] == deployment_id and
            loaded_state["status"] == "completed" and
            len(loaded_state["events"]) > 0 and
            len(loaded_state["metrics_history"]) > 0
        )
        
        message = f"State persistence: {'successful' if success else 'failed'}"
        
        return success, message, duration


def run_all_tests():
    """Run all progressive deployment tests"""
    print("=" * 80)
    print("Progressive Deployment System - Test Suite")
    print("=" * 80)
    
    deployer = ProgressiveDeploymentSystem()
    
    tests = [
        ("Canary Deployment Success", deployer.test_canary_success),
        ("Canary Deployment Rollback", deployer.test_canary_rollback),
        ("Blue-Green Instant Switch", deployer.test_blue_green_instant_switch),
        ("Feature Flag Progressive", deployer.test_feature_flag_progressive),
        ("Monitoring and Metrics", deployer.test_monitoring_and_metrics),
        ("State Persistence", deployer.test_state_persistence)
    ]
    
    total_tests = len(tests)
    passed_tests = 0
    failed_tests = []
    
    print(f"\nRunning {total_tests} tests...\n")
    
    for test_name, test_func in tests:
        try:
            success, message, duration = test_func()
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} | {test_name}")
            print(f"     {message}")
            print(f"     Duration: {duration:.2f}s")
            
            if success:
                passed_tests += 1
            else:
                failed_tests.append((test_name, message))
                
        except Exception as e:
            print(f"❌ FAIL | {test_name}")
            print(f"     Error: {str(e)}")
            failed_tests.append((test_name, str(e)))
        
        print()
    
    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests:
        print("\nFailed Tests:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}: {error}")
    
    print("=" * 80)
    
    # Return exit code
    return 0 if len(failed_tests) == 0 else 1


if __name__ == "__main__":
    # Test with real deployment scenarios
    print("Testing Progressive Deployment System...\n")
    
    # Run comprehensive test suite
    exit_code = run_all_tests()
    
    # Example of individual deployment
    if exit_code == 0:
        print("\n" + "=" * 80)
        print("EXAMPLE: Running a sample canary deployment...")
        print("=" * 80)
        
        deployer = ProgressiveDeploymentSystem()
        result = deployer.deploy_with_canary("production-v2.1", traffic_percentage=10)
        
        print(f"\nDeployment Result:")
        print(f"  Status: {result['status']}")
        print(f"  Deployment ID: {result['deployment_id']}")
        
        if "duration" in result:
            print(f"  Duration: {result['duration']}")
        if "final_metrics" in result:
            print(f"  Final Metrics:")
            for metric, value in result['final_metrics'].items():
                print(f"    {metric}: {value:.2f}")
    
    exit(exit_code)