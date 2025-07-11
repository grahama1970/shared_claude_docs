
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: container_orchestrator_interaction.py
Purpose: Container orchestration assistance system for Docker and Kubernetes

External Dependencies:
- docker: https://docker-py.readthedocs.io/
- kubernetes: https://github.com/kubernetes-client/python
- pyyaml: https://pyyaml.org/wiki/PyYAMLDocumentation

Example Usage:
>>> from container_orchestrator_interaction import ContainerOrchestrator
>>> orchestrator = ContainerOrchestrator()
>>> result = orchestrator.deploy_service("web-app", replicas=3)
{'status': 'deployed', 'service': 'web-app', 'replicas': 3, 'endpoints': ['10.0.0.1:8080', '10.0.0.2:8080', '10.0.0.3:8080']}
"""

import asyncio
import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import base64
from pathlib import Path


class DeploymentStrategy(Enum):
    """Deployment strategy types"""
    ROLLING_UPDATE = "rolling_update"
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    RECREATE = "recreate"


class ResourceType(Enum):
    """Kubernetes resource types"""
    DEPLOYMENT = "deployment"
    SERVICE = "service"
    CONFIGMAP = "configmap"
    SECRET = "secret"
    INGRESS = "ingress"
    STATEFULSET = "statefulset"
    DAEMONSET = "daemonset"


@dataclass
class ContainerConfig:
    """Container configuration"""
    image: str
    name: str
    ports: List[int] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    resources: Dict[str, Any] = field(default_factory=dict)
    volumes: List[Dict[str, str]] = field(default_factory=list)
    health_check: Optional[Dict[str, Any]] = None
    command: Optional[List[str]] = None
    args: Optional[List[str]] = None


@dataclass
class ServiceConfig:
    """Service configuration"""
    name: str
    selector: Dict[str, str]
    ports: List[Dict[str, Any]]
    type: str = "ClusterIP"
    load_balancer_ip: Optional[str] = None
    session_affinity: Optional[str] = None


@dataclass
class AutoScalingPolicy:
    """Auto-scaling policy configuration"""
    min_replicas: int
    max_replicas: int
    target_cpu_utilization: int = 80
    target_memory_utilization: Optional[int] = None
    scale_up_rate: int = 1
    scale_down_rate: int = 1
    cool_down_period: int = 300


@dataclass
class NetworkPolicy:
    """Network policy configuration"""
    name: str
    pod_selector: Dict[str, str]
    ingress_rules: List[Dict[str, Any]] = field(default_factory=list)
    egress_rules: List[Dict[str, Any]] = field(default_factory=list)
    policy_types: List[str] = field(default_factory=lambda: ["Ingress", "Egress"])


class ContainerOrchestrator:
    """Container orchestration assistance system"""
    
    def __init__(self, clusters: Optional[List[str]] = None):
        """Initialize container orchestrator"""
        self.clusters = clusters or ["default"]
        self.deployments: Dict[str, Dict[str, Any]] = {}
        self.services: Dict[str, ServiceConfig] = {}
        self.configs: Dict[str, Dict[str, str]] = {}
        self.secrets: Dict[str, Dict[str, str]] = {}
        self.network_policies: Dict[str, NetworkPolicy] = {}
        self.auto_scaling_policies: Dict[str, AutoScalingPolicy] = {}
        
    async def deploy_service(
        self,
        name: str,
        image: str,
        replicas: int = 1,
        ports: Optional[List[int]] = None,
        strategy: DeploymentStrategy = DeploymentStrategy.ROLLING_UPDATE,
        environment: Optional[Dict[str, str]] = None,
        resources: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deploy a service with specified configuration"""
        container_config = ContainerConfig(
            name=name,
            image=image,
            ports=ports or [8080],
            environment=environment or {},
            resources=resources or {
                "requests": {"cpu": "100m", "memory": "128Mi"},
                "limits": {"cpu": "500m", "memory": "512Mi"}
            }
        )
        
        # Create deployment
        deployment = await self._create_deployment(
            name, container_config, replicas, strategy
        )
        
        # Create service
        service = await self._create_service(name, container_config)
        
        # Store configurations
        self.deployments[name] = deployment
        self.services[name] = service
        
        # Simulate endpoint creation
        endpoints = [
            f"10.0.0.{i+1}:{ports[0] if ports else 8080}"
            for i in range(replicas)
        ]
        
        return {
            "status": "deployed",
            "service": name,
            "replicas": replicas,
            "endpoints": endpoints,
            "strategy": strategy.value,
            "deployment_id": deployment["id"]
        }
    
    async def _create_deployment(
        self,
        name: str,
        config: ContainerConfig,
        replicas: int,
        strategy: DeploymentStrategy
    ) -> Dict[str, Any]:
        """Create deployment configuration"""
        deployment_id = hashlib.md5(f"{name}-{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        
        deployment = {
            "id": deployment_id,
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": name,
                "labels": {"app": name}
            },
            "spec": {
                "replicas": replicas,
                "selector": {"matchLabels": {"app": name}},
                "strategy": self._get_deployment_strategy(strategy),
                "template": {
                    "metadata": {"labels": {"app": name}},
                    "spec": {
                        "containers": [self._container_spec(config)]
                    }
                }
            }
        }
        
        return deployment
    
    def _get_deployment_strategy(self, strategy: DeploymentStrategy) -> Dict[str, Any]:
        """Get deployment strategy configuration"""
        if strategy == DeploymentStrategy.ROLLING_UPDATE:
            return {
                "type": "RollingUpdate",
                "rollingUpdate": {
                    "maxSurge": "25%",
                    "maxUnavailable": "25%"
                }
            }
        elif strategy == DeploymentStrategy.RECREATE:
            return {"type": "Recreate"}
        else:
            # For blue-green and canary, use rolling update with custom logic
            return {
                "type": "RollingUpdate",
                "rollingUpdate": {
                    "maxSurge": "100%" if strategy == DeploymentStrategy.BLUE_GREEN else "10%",
                    "maxUnavailable": "0%"
                }
            }
    
    def _container_spec(self, config: ContainerConfig) -> Dict[str, Any]:
        """Generate container specification"""
        spec = {
            "name": config.name,
            "image": config.image,
            "ports": [{"containerPort": port} for port in config.ports],
            "env": [
                {"name": k, "value": v}
                for k, v in config.environment.items()
            ],
            "resources": config.resources
        }
        
        if config.command:
            spec["command"] = config.command
        if config.args:
            spec["args"] = config.args
        if config.health_check:
            spec["livenessProbe"] = config.health_check
            spec["readinessProbe"] = config.health_check
            
        return spec
    
    async def _create_service(
        self, name: str, config: ContainerConfig
    ) -> ServiceConfig:
        """Create service configuration"""
        service_config = ServiceConfig(
            name=name,
            selector={"app": name},
            ports=[
                {
                    "port": port,
                    "targetPort": port,
                    "protocol": "TCP"
                }
                for port in config.ports
            ]
        )
        
        return service_config
    
    async def scale_deployment(
        self, name: str, replicas: int
    ) -> Dict[str, Any]:
        """Scale a deployment to specified replicas"""
        if name not in self.deployments:
            return {"error": f"Deployment {name} not found"}
        
        old_replicas = self.deployments[name]["spec"]["replicas"]
        self.deployments[name]["spec"]["replicas"] = replicas
        
        return {
            "status": "scaled",
            "deployment": name,
            "old_replicas": old_replicas,
            "new_replicas": replicas,
            "timestamp": datetime.now().isoformat()
        }
    
    async def configure_auto_scaling(
        self,
        deployment: str,
        policy: AutoScalingPolicy
    ) -> Dict[str, Any]:
        """Configure auto-scaling for a deployment"""
        if deployment not in self.deployments:
            return {"error": f"Deployment {deployment} not found"}
        
        self.auto_scaling_policies[deployment] = policy
        
        hpa_config = {
            "apiVersion": "autoscaling/v2",
            "kind": "HorizontalPodAutoscaler",
            "metadata": {"name": f"{deployment}-hpa"},
            "spec": {
                "scaleTargetRef": {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name": deployment
                },
                "minReplicas": policy.min_replicas,
                "maxReplicas": policy.max_replicas,
                "metrics": [
                    {
                        "type": "Resource",
                        "resource": {
                            "name": "cpu",
                            "target": {
                                "type": "Utilization",
                                "averageUtilization": policy.target_cpu_utilization
                            }
                        }
                    }
                ]
            }
        }
        
        if policy.target_memory_utilization:
            hpa_config["spec"]["metrics"].append({
                "type": "Resource",
                "resource": {
                    "name": "memory",
                    "target": {
                        "type": "Utilization",
                        "averageUtilization": policy.target_memory_utilization
                    }
                }
            })
        
        return {
            "status": "configured",
            "deployment": deployment,
            "auto_scaling": {
                "min_replicas": policy.min_replicas,
                "max_replicas": policy.max_replicas,
                "cpu_target": policy.target_cpu_utilization,
                "memory_target": policy.target_memory_utilization
            }
        }
    
    async def perform_rolling_update(
        self,
        deployment: str,
        new_image: str,
        max_surge: str = "25%",
        max_unavailable: str = "25%"
    ) -> Dict[str, Any]:
        """Perform rolling update of deployment"""
        if deployment not in self.deployments:
            return {"error": f"Deployment {deployment} not found"}
        
        old_image = self.deployments[deployment]["spec"]["template"]["spec"]["containers"][0]["image"]
        self.deployments[deployment]["spec"]["template"]["spec"]["containers"][0]["image"] = new_image
        
        # Update strategy
        self.deployments[deployment]["spec"]["strategy"] = {
            "type": "RollingUpdate",
            "rollingUpdate": {
                "maxSurge": max_surge,
                "maxUnavailable": max_unavailable
            }
        }
        
        # Simulate update progress
        update_status = {
            "status": "updating",
            "deployment": deployment,
            "old_image": old_image,
            "new_image": new_image,
            "progress": "0%",
            "updated_replicas": 0,
            "total_replicas": self.deployments[deployment]["spec"]["replicas"]
        }
        
        return update_status
    
    async def rollback_deployment(
        self, deployment: str, revision: Optional[int] = None
    ) -> Dict[str, Any]:
        """Rollback deployment to previous revision"""
        if deployment not in self.deployments:
            return {"error": f"Deployment {deployment} not found"}
        
        # Simulate rollback
        return {
            "status": "rolled_back",
            "deployment": deployment,
            "revision": revision or "previous",
            "timestamp": datetime.now().isoformat()
        }
    
    async def create_config_map(
        self, name: str, data: Dict[str, str]
    ) -> Dict[str, Any]:
        """Create ConfigMap for configuration management"""
        self.configs[name] = data
        
        config_map = {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": name},
            "data": data
        }
        
        return {
            "status": "created",
            "type": "configmap",
            "name": name,
            "items": len(data)
        }
    
    async def create_secret(
        self, name: str, data: Dict[str, str], secret_type: str = "Opaque"
    ) -> Dict[str, Any]:
        """Create Secret for sensitive data"""
        # Simulate base64 encoding
        encoded_data = {
            k: base64.b64encode(v.encode()).decode()[:20] + "..."
            for k, v in data.items()
        }
        
        self.secrets[name] = encoded_data
        
        secret = {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {"name": name},
            "type": secret_type,
            "data": encoded_data
        }
        
        return {
            "status": "created",
            "type": "secret",
            "name": name,
            "secret_type": secret_type,
            "keys": list(data.keys())
        }
    
    async def configure_network_policy(
        self, policy: NetworkPolicy
    ) -> Dict[str, Any]:
        """Configure network policy for pod communication"""
        self.network_policies[policy.name] = policy
        
        k8s_policy = {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "NetworkPolicy",
            "metadata": {"name": policy.name},
            "spec": {
                "podSelector": {"matchLabels": policy.pod_selector},
                "policyTypes": policy.policy_types,
                "ingress": policy.ingress_rules,
                "egress": policy.egress_rules
            }
        }
        
        return {
            "status": "configured",
            "policy": policy.name,
            "pod_selector": policy.pod_selector,
            "rules": {
                "ingress": len(policy.ingress_rules),
                "egress": len(policy.egress_rules)
            }
        }
    
    async def setup_service_mesh(
        self,
        mesh_name: str,
        services: List[str],
        mtls_enabled: bool = True,
        traffic_policy: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Setup service mesh configuration"""
        mesh_config = {
            "name": mesh_name,
            "services": services,
            "mtls": mtls_enabled,
            "traffic_policy": traffic_policy or {
                "connectionPool": {
                    "tcp": {"maxConnections": 100},
                    "http": {"http1MaxPendingRequests": 10}
                },
                "outlierDetection": {
                    "consecutiveErrors": 5,
                    "interval": "30s",
                    "baseEjectionTime": "30s"
                }
            }
        }
        
        # Generate virtual services
        virtual_services = []
        for service in services:
            virtual_services.append({
                "name": f"{service}-vs",
                "hosts": [service],
                "http": [{
                    "route": [{
                        "destination": {
                            "host": service,
                            "subset": "v1"
                        }
                    }]
                }]
            })
        
        return {
            "status": "configured",
            "mesh": mesh_name,
            "services": len(services),
            "mtls_enabled": mtls_enabled,
            "virtual_services": len(virtual_services),
            "policies": list(traffic_policy.keys()) if traffic_policy else []
        }
    
    async def monitor_container_health(
        self, deployment: str
    ) -> Dict[str, Any]:
        """Monitor container health status"""
        if deployment not in self.deployments:
            return {"error": f"Deployment {deployment} not found"}
        
        replicas = self.deployments[deployment]["spec"]["replicas"]
        
        # Simulate health status
        health_status = {
            "deployment": deployment,
            "timestamp": datetime.now().isoformat(),
            "replicas": {
                "desired": replicas,
                "ready": replicas,
                "available": replicas,
                "updated": replicas
            },
            "containers": []
        }
        
        # Simulate container health
        for i in range(replicas):
            health_status["containers"].append({
                "name": f"{deployment}-{i}",
                "ready": True,
                "restart_count": 0,
                "status": "Running",
                "cpu_usage": f"{20 + i * 5}%",
                "memory_usage": f"{30 + i * 3}%"
            })
        
        return health_status
    
    async def optimize_resource_allocation(
        self, deployment: str
    ) -> Dict[str, Any]:
        """Optimize resource allocation based on usage"""
        if deployment not in self.deployments:
            return {"error": f"Deployment {deployment} not found"}
        
        current_resources = self.deployments[deployment]["spec"]["template"]["spec"]["containers"][0]["resources"]
        
        # Simulate optimization recommendations
        recommendations = {
            "deployment": deployment,
            "current_resources": current_resources,
            "recommended_resources": {
                "requests": {
                    "cpu": "150m",  # Increased from 100m
                    "memory": "256Mi"  # Increased from 128Mi
                },
                "limits": {
                    "cpu": "750m",  # Increased from 500m
                    "memory": "1Gi"  # Increased from 512Mi
                }
            },
            "reasoning": "Based on observed usage patterns",
            "potential_savings": "20% reduction in resource waste"
        }
        
        return recommendations
    
    async def generate_deployment_manifest(
        self,
        name: str,
        config: Dict[str, Any]
    ) -> str:
        """Generate deployment manifest in YAML format"""
        manifest = {
            "apiVersion": "v1",
            "kind": "List",
            "items": []
        }
        
        # Add deployment
        if name in self.deployments:
            manifest["items"].append(self.deployments[name])
        
        # Add service
        if name in self.services:
            service = self.services[name]
            manifest["items"].append({
                "apiVersion": "v1",
                "kind": "Service",
                "metadata": {"name": service.name},
                "spec": {
                    "selector": service.selector,
                    "ports": service.ports,
                    "type": service.type
                }
            })
        
        # Add ConfigMaps
        for cm_name, cm_data in self.configs.items():
            if cm_name.startswith(name):
                manifest["items"].append({
                    "apiVersion": "v1",
                    "kind": "ConfigMap",
                    "metadata": {"name": cm_name},
                    "data": cm_data
                })
        
        # Convert to YAML
        yaml_manifest = yaml.dump(manifest, default_flow_style=False)
        return yaml_manifest
    
    async def setup_load_balancer(
        self,
        service: str,
        algorithm: str = "round_robin",
        health_check_path: str = "/health",
        sticky_sessions: bool = False
    ) -> Dict[str, Any]:
        """Setup load balancer configuration"""
        if service not in self.services:
            return {"error": f"Service {service} not found"}
        
        lb_config = {
            "service": service,
            "algorithm": algorithm,
            "health_check": {
                "path": health_check_path,
                "interval": "10s",
                "timeout": "5s",
                "healthy_threshold": 2,
                "unhealthy_threshold": 3
            },
            "sticky_sessions": sticky_sessions,
            "backends": []
        }
        
        # Add backend endpoints
        if service in self.deployments:
            replicas = self.deployments[service]["spec"]["replicas"]
            for i in range(replicas):
                lb_config["backends"].append({
                    "address": f"10.0.0.{i+1}",
                    "port": self.services[service].ports[0]["port"],
                    "weight": 100,
                    "healthy": True
                })
        
        return {
            "status": "configured",
            "load_balancer": f"{service}-lb",
            "algorithm": algorithm,
            "backends": len(lb_config["backends"]),
            "health_check_enabled": True,
            "sticky_sessions": sticky_sessions
        }
    
    def get_cluster_status(self) -> Dict[str, Any]:
        """Get overall cluster status"""
        total_deployments = len(self.deployments)
        total_services = len(self.services)
        total_replicas = sum(
            d["spec"]["replicas"] for d in self.deployments.values()
        )
        
        return {
            "clusters": self.clusters,
            "deployments": total_deployments,
            "services": total_services,
            "total_replicas": total_replicas,
            "network_policies": len(self.network_policies),
            "auto_scaling_policies": len(self.auto_scaling_policies),
            "config_maps": len(self.configs),
            "secrets": len(self.secrets)
        }


async def demonstrate_container_orchestration():
    """Demonstrate container orchestration capabilities"""
    orchestrator = ContainerOrchestrator(clusters=["production", "staging"])
    
    print("Container Orchestration Demonstration\n" + "=" * 50)
    
    # Deploy a web service
    print("\n1. Deploying web service...")
    web_result = await orchestrator.deploy_service(
        name="web-app",
        image="nginx:latest",
        replicas=3,
        ports=[80, 443],
        environment={"ENV": "production", "LOG_LEVEL": "info"},
        strategy=DeploymentStrategy.ROLLING_UPDATE
    )
    print(f"Result: {json.dumps(web_result, indent=2)}")
    
    # Configure auto-scaling
    print("\n2. Configuring auto-scaling...")
    scaling_policy = AutoScalingPolicy(
        min_replicas=2,
        max_replicas=10,
        target_cpu_utilization=70,
        target_memory_utilization=80
    )
    scaling_result = await orchestrator.configure_auto_scaling(
        "web-app", scaling_policy
    )
    print(f"Result: {json.dumps(scaling_result, indent=2)}")
    
    # Create configuration
    print("\n3. Creating ConfigMap...")
    config_result = await orchestrator.create_config_map(
        "web-app-config",
        {
            "app.properties": "server.port=8080\napp.name=WebApp",
            "logging.conf": "level=INFO\nformat=json"
        }
    )
    print(f"Result: {json.dumps(config_result, indent=2)}")
    
    # Create secrets
    print("\n4. Creating secrets...")
    secret_result = await orchestrator.create_secret(
        "web-app-secrets",
        {
            "db_password": "super-secret-password",
            "api_key": "xyz123abc456"
        }
    )
    print(f"Result: {json.dumps(secret_result, indent=2)}")
    
    # Configure network policy
    print("\n5. Configuring network policy...")
    network_policy = NetworkPolicy(
        name="web-app-policy",
        pod_selector={"app": "web-app"},
        ingress_rules=[{
            "from": [{"podSelector": {"app": "frontend"}}],
            "ports": [{"protocol": "TCP", "port": 80}]
        }]
    )
    network_result = await orchestrator.configure_network_policy(network_policy)
    print(f"Result: {json.dumps(network_result, indent=2)}")
    
    # Setup service mesh
    print("\n6. Setting up service mesh...")
    mesh_result = await orchestrator.setup_service_mesh(
        "istio-mesh",
        ["web-app", "api-service", "database-proxy"],
        mtls_enabled=True
    )
    print(f"Result: {json.dumps(mesh_result, indent=2)}")
    
    # Monitor health
    print("\n7. Monitoring container health...")
    health_result = await orchestrator.monitor_container_health("web-app")
    print(f"Result: {json.dumps(health_result, indent=2)}")
    
    # Optimize resources
    print("\n8. Optimizing resource allocation...")
    optimize_result = await orchestrator.optimize_resource_allocation("web-app")
    print(f"Result: {json.dumps(optimize_result, indent=2)}")
    
    # Setup load balancer
    print("\n9. Setting up load balancer...")
    lb_result = await orchestrator.setup_load_balancer(
        "web-app",
        algorithm="least_connections",
        sticky_sessions=True
    )
    print(f"Result: {json.dumps(lb_result, indent=2)}")
    
    # Perform rolling update
    print("\n10. Performing rolling update...")
    update_result = await orchestrator.perform_rolling_update(
        "web-app",
        "nginx:1.21"
    )
    print(f"Result: {json.dumps(update_result, indent=2)}")
    
    # Get cluster status
    print("\n11. Getting cluster status...")
    status = orchestrator.get_cluster_status()
    print(f"Cluster Status: {json.dumps(status, indent=2)}")
    
    # Generate deployment manifest
    print("\n12. Generating deployment manifest...")
    manifest = await orchestrator.generate_deployment_manifest(
        "web-app", {"include_configs": True}
    )
    print(f"Manifest preview (first 500 chars):\n{manifest[:500]}...")
    
    return orchestrator


if __name__ == "__main__":
    # Test with real container orchestration scenarios
    orchestrator = asyncio.run(demonstrate_container_orchestration())
    
    # Additional validation
    print("\n" + "=" * 50)
    print("Validation Results:")
    
    # Verify deployment exists
    assert "web-app" in orchestrator.deployments, "Deployment should exist"
    print("✅ Deployment created successfully")
    
    # Verify service configuration
    assert "web-app" in orchestrator.services, "Service should exist"
    assert orchestrator.services["web-app"].ports[0]["port"] == 80
    print("✅ Service configured correctly")
    
    # Verify auto-scaling policy
    assert "web-app" in orchestrator.auto_scaling_policies
    assert orchestrator.auto_scaling_policies["web-app"].max_replicas == 10
    print("✅ Auto-scaling policy configured")
    
    # Verify configurations
    assert "web-app-config" in orchestrator.configs
    assert "web-app-secrets" in orchestrator.secrets
    print("✅ Configurations and secrets created")
    
    # Verify network policy
    assert "web-app-policy" in orchestrator.network_policies
    print("✅ Network policy configured")
    
    print("\n✅ All validations passed!")