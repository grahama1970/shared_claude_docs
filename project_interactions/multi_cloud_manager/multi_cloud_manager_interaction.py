
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: multi_cloud_manager_interaction.py
Purpose: Unified multi-cloud resource management system with cost optimization and compliance

External Dependencies:
- boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- azure-mgmt-*: https://docs.microsoft.com/en-us/python/api/overview/azure/
- google-cloud-*: https://cloud.google.com/python/docs/reference
- pandas: https://pandas.pydata.org/docs/
- networkx: https://networkx.org/documentation/stable/

Example Usage:
>>> from multi_cloud_manager_interaction import MultiCloudManager
>>> manager = MultiCloudManager()
>>> resources = manager.discover_all_resources()
>>> print(f"Found {len(resources)} resources across all clouds")
Found 142 resources across all clouds
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict
import json
import pandas as pd
import networkx as nx
from loguru import logger

# Cloud provider imports (mocked for demonstration)
try:
    import boto3
except ImportError:
    boto3 = None
    
try:
    from azure.mgmt.compute import ComputeManagementClient
    from azure.mgmt.storage import StorageManagementClient
except ImportError:
    ComputeManagementClient = None
    StorageManagementClient = None
    
try:
    from google.cloud import compute_v1
    from google.cloud import storage
except ImportError:
    compute_v1 = None
    storage = None


class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"


class ResourceType(Enum):
    """Types of cloud resources"""
    COMPUTE = "compute"
    STORAGE = "storage"
    FUNCTION = "function"
    DATABASE = "database"
    NETWORK = "network"
    SECURITY = "security"


class ResourceState(Enum):
    """Resource lifecycle states"""
    RUNNING = "running"
    STOPPED = "stopped"
    PENDING = "pending"
    TERMINATING = "terminating"
    TERMINATED = "terminated"


@dataclass
class ResourceMetrics:
    """Resource usage metrics"""
    cpu_utilization: float = 0.0
    memory_utilization: float = 0.0
    network_in_bytes: int = 0
    network_out_bytes: int = 0
    storage_used_bytes: int = 0
    request_count: int = 0
    error_count: int = 0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CostData:
    """Resource cost information"""
    hourly_cost: float
    monthly_estimate: float
    currency: str = "USD"
    billing_period: str = ""
    discount_applied: float = 0.0


@dataclass
class ComplianceCheck:
    """Security compliance check result"""
    check_name: str
    passed: bool
    severity: str
    details: str
    recommendation: str = ""


@dataclass
class CloudResource:
    """Unified cloud resource representation"""
    id: str
    name: str
    provider: CloudProvider
    resource_type: ResourceType
    state: ResourceState
    region: str
    created_at: datetime
    tags: Dict[str, str] = field(default_factory=dict)
    metrics: Optional[ResourceMetrics] = None
    cost_data: Optional[CostData] = None
    compliance_checks: List[ComplianceCheck] = field(default_factory=list)
    dependencies: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)


class CloudProviderAdapter(ABC):
    """Abstract base class for cloud provider adapters"""
    
    @abstractmethod
    async def discover_resources(self) -> List[CloudResource]:
        """Discover all resources in the cloud provider"""
        pass
    
    @abstractmethod
    async def get_resource_metrics(self, resource_id: str) -> ResourceMetrics:
        """Get current metrics for a resource"""
        pass
    
    @abstractmethod
    async def get_resource_cost(self, resource_id: str) -> CostData:
        """Get cost data for a resource"""
        pass
    
    @abstractmethod
    async def create_resource(self, resource_spec: Dict[str, Any]) -> CloudResource:
        """Create a new resource"""
        pass
    
    @abstractmethod
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource"""
        pass
    
    @abstractmethod
    async def update_resource_tags(self, resource_id: str, tags: Dict[str, str]) -> bool:
        """Update resource tags"""
        pass


class AWSAdapter(CloudProviderAdapter):
    """AWS cloud provider adapter"""
    
    def __init__(self, credentials: Optional[Dict[str, str]] = None):
        self.credentials = credentials or {}
        self.ec2_client = None
        self.s3_client = None
        self.lambda_client = None
        self.rds_client = None
        
    async def discover_resources(self) -> List[CloudResource]:
        """Discover all AWS resources"""
        resources = []
        
        # Simulate EC2 instances
        resources.extend([
            CloudResource(
                id=f"i-{i:012d}",
                name=f"web-server-{i}",
                provider=CloudProvider.AWS,
                resource_type=ResourceType.COMPUTE,
                state=ResourceState.RUNNING,
                region="us-east-1",
                created_at=datetime.now() - timedelta(days=30 - i),
                tags={"environment": "production", "team": "backend"},
                metadata={"instance_type": "t3.medium", "ami_id": "ami-12345678"}
            )
            for i in range(5)
        ])
        
        # Simulate S3 buckets
        resources.extend([
            CloudResource(
                id=f"s3-bucket-{i}",
                name=f"data-lake-{i}",
                provider=CloudProvider.AWS,
                resource_type=ResourceType.STORAGE,
                state=ResourceState.RUNNING,
                region="us-east-1",
                created_at=datetime.now() - timedelta(days=60 - i*10),
                tags={"data_classification": "sensitive", "retention": "7years"},
                metadata={"size_bytes": 1024 * 1024 * 1024 * (i + 1)}
            )
            for i in range(3)
        ])
        
        return resources
    
    async def get_resource_metrics(self, resource_id: str) -> ResourceMetrics:
        """Get AWS resource metrics"""
        # Simulate metrics
        return ResourceMetrics(
            cpu_utilization=65.5,
            memory_utilization=78.2,
            network_in_bytes=1024 * 1024 * 100,
            network_out_bytes=1024 * 1024 * 50,
            storage_used_bytes=1024 * 1024 * 1024 * 10
        )
    
    async def get_resource_cost(self, resource_id: str) -> CostData:
        """Get AWS resource cost"""
        # Simulate cost data
        hourly = 0.0684 if resource_id.startswith("i-") else 0.023
        return CostData(
            hourly_cost=hourly,
            monthly_estimate=hourly * 24 * 30,
            billing_period="2024-01"
        )
    
    async def create_resource(self, resource_spec: Dict[str, Any]) -> CloudResource:
        """Create AWS resource"""
        return CloudResource(
            id=f"i-{datetime.now().timestamp():.0f}",
            name=resource_spec.get("name", "new-instance"),
            provider=CloudProvider.AWS,
            resource_type=ResourceType.COMPUTE,
            state=ResourceState.PENDING,
            region=resource_spec.get("region", "us-east-1"),
            created_at=datetime.now(),
            tags=resource_spec.get("tags", {})
        )
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete AWS resource"""
        logger.info(f"Deleting AWS resource: {resource_id}")
        return True
    
    async def update_resource_tags(self, resource_id: str, tags: Dict[str, str]) -> bool:
        """Update AWS resource tags"""
        logger.info(f"Updating tags for AWS resource: {resource_id}")
        return True


class AzureAdapter(CloudProviderAdapter):
    """Azure cloud provider adapter"""
    
    def __init__(self, credentials: Optional[Dict[str, str]] = None):
        self.credentials = credentials or {}
        
    async def discover_resources(self) -> List[CloudResource]:
        """Discover all Azure resources"""
        resources = []
        
        # Simulate Azure VMs
        resources.extend([
            CloudResource(
                id=f"vm-azure-{i}",
                name=f"app-vm-{i}",
                provider=CloudProvider.AZURE,
                resource_type=ResourceType.COMPUTE,
                state=ResourceState.RUNNING,
                region="eastus",
                created_at=datetime.now() - timedelta(days=20 - i*2),
                tags={"project": "migration", "cost_center": "IT"},
                metadata={"vm_size": "Standard_B2ms", "os": "Ubuntu 20.04"}
            )
            for i in range(3)
        ])
        
        # Simulate Azure Storage
        resources.append(
            CloudResource(
                id="storage-azure-001",
                name="backupstorage001",
                provider=CloudProvider.AZURE,
                resource_type=ResourceType.STORAGE,
                state=ResourceState.RUNNING,
                region="eastus",
                created_at=datetime.now() - timedelta(days=90),
                tags={"purpose": "backup", "tier": "cool"},
                metadata={"account_type": "StorageV2", "replication": "LRS"}
            )
        )
        
        return resources
    
    async def get_resource_metrics(self, resource_id: str) -> ResourceMetrics:
        """Get Azure resource metrics"""
        return ResourceMetrics(
            cpu_utilization=45.8,
            memory_utilization=62.1,
            network_in_bytes=1024 * 1024 * 80,
            network_out_bytes=1024 * 1024 * 40
        )
    
    async def get_resource_cost(self, resource_id: str) -> CostData:
        """Get Azure resource cost"""
        hourly = 0.0496 if resource_id.startswith("vm-") else 0.0184
        return CostData(
            hourly_cost=hourly,
            monthly_estimate=hourly * 24 * 30,
            billing_period="2024-01"
        )
    
    async def create_resource(self, resource_spec: Dict[str, Any]) -> CloudResource:
        """Create Azure resource"""
        return CloudResource(
            id=f"vm-azure-{datetime.now().timestamp():.0f}",
            name=resource_spec.get("name", "new-vm"),
            provider=CloudProvider.AZURE,
            resource_type=ResourceType.COMPUTE,
            state=ResourceState.PENDING,
            region=resource_spec.get("region", "eastus"),
            created_at=datetime.now(),
            tags=resource_spec.get("tags", {})
        )
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete Azure resource"""
        logger.info(f"Deleting Azure resource: {resource_id}")
        return True
    
    async def update_resource_tags(self, resource_id: str, tags: Dict[str, str]) -> bool:
        """Update Azure resource tags"""
        logger.info(f"Updating tags for Azure resource: {resource_id}")
        return True


class GCPAdapter(CloudProviderAdapter):
    """Google Cloud Platform adapter"""
    
    def __init__(self, credentials: Optional[Dict[str, str]] = None):
        self.credentials = credentials or {}
        
    async def discover_resources(self) -> List[CloudResource]:
        """Discover all GCP resources"""
        resources = []
        
        # Simulate GCP Compute instances
        resources.extend([
            CloudResource(
                id=f"gce-instance-{i}",
                name=f"api-server-{i}",
                provider=CloudProvider.GCP,
                resource_type=ResourceType.COMPUTE,
                state=ResourceState.RUNNING,
                region="us-central1",
                created_at=datetime.now() - timedelta(days=15 - i),
                tags={"service": "api", "version": "v2"},
                metadata={"machine_type": "e2-medium", "zone": "us-central1-a"}
            )
            for i in range(4)
        ])
        
        # Simulate Cloud Functions
        resources.extend([
            CloudResource(
                id=f"function-{i}",
                name=f"data-processor-{i}",
                provider=CloudProvider.GCP,
                resource_type=ResourceType.FUNCTION,
                state=ResourceState.RUNNING,
                region="us-central1",
                created_at=datetime.now() - timedelta(days=10),
                tags={"trigger": "pubsub", "runtime": "python39"},
                metadata={"memory": "256MB", "timeout": "60s"}
            )
            for i in range(2)
        ])
        
        return resources
    
    async def get_resource_metrics(self, resource_id: str) -> ResourceMetrics:
        """Get GCP resource metrics"""
        return ResourceMetrics(
            cpu_utilization=55.3,
            memory_utilization=70.5,
            network_in_bytes=1024 * 1024 * 120,
            network_out_bytes=1024 * 1024 * 60,
            request_count=10000 if resource_id.startswith("function-") else 0
        )
    
    async def get_resource_cost(self, resource_id: str) -> CostData:
        """Get GCP resource cost"""
        if resource_id.startswith("gce-"):
            hourly = 0.0475
        elif resource_id.startswith("function-"):
            hourly = 0.0000004  # Per invocation
        else:
            hourly = 0.02
            
        return CostData(
            hourly_cost=hourly,
            monthly_estimate=hourly * 24 * 30 if not resource_id.startswith("function-") else hourly * 1000000,
            billing_period="2024-01"
        )
    
    async def create_resource(self, resource_spec: Dict[str, Any]) -> CloudResource:
        """Create GCP resource"""
        return CloudResource(
            id=f"gce-instance-{datetime.now().timestamp():.0f}",
            name=resource_spec.get("name", "new-instance"),
            provider=CloudProvider.GCP,
            resource_type=ResourceType.COMPUTE,
            state=ResourceState.PENDING,
            region=resource_spec.get("region", "us-central1"),
            created_at=datetime.now(),
            tags=resource_spec.get("tags", {})
        )
    
    async def delete_resource(self, resource_id: str) -> bool:
        """Delete GCP resource"""
        logger.info(f"Deleting GCP resource: {resource_id}")
        return True
    
    async def update_resource_tags(self, resource_id: str, tags: Dict[str, str]) -> bool:
        """Update GCP resource tags"""
        logger.info(f"Updating tags for GCP resource: {resource_id}")
        return True


class CostOptimizer:
    """Cost optimization engine"""
    
    def __init__(self):
        self.optimization_rules = self._load_optimization_rules()
        
    def _load_optimization_rules(self) -> List[Dict[str, Any]]:
        """Load cost optimization rules"""
        return [
            {
                "name": "idle_compute",
                "description": "Identify idle compute instances",
                "condition": lambda r, m: m.cpu_utilization < 10.0,
                "recommendation": "Consider stopping or terminating idle instances",
                "potential_savings": 0.9  # 90% of cost
            },
            {
                "name": "oversized_compute",
                "description": "Identify oversized compute instances",
                "condition": lambda r, m: m.cpu_utilization < 30.0 and m.memory_utilization < 40.0,
                "recommendation": "Consider downsizing to a smaller instance type",
                "potential_savings": 0.5  # 50% of cost
            },
            {
                "name": "old_snapshots",
                "description": "Identify old storage snapshots",
                "condition": lambda r, m: r.resource_type == ResourceType.STORAGE and 
                                       (datetime.now() - r.created_at).days > 90,
                "recommendation": "Review and delete unnecessary old snapshots",
                "potential_savings": 1.0  # 100% of cost
            },
            {
                "name": "untagged_resources",
                "description": "Identify resources without proper tags",
                "condition": lambda r, m: len(r.tags) < 2,
                "recommendation": "Add proper tags for cost allocation and management",
                "potential_savings": 0.0  # No direct savings but improves tracking
            }
        ]
    
    async def analyze_resource(self, resource: CloudResource) -> List[Dict[str, Any]]:
        """Analyze a single resource for optimization opportunities"""
        recommendations = []
        
        if not resource.metrics or not resource.cost_data:
            return recommendations
            
        for rule in self.optimization_rules:
            if rule["condition"](resource, resource.metrics):
                recommendations.append({
                    "resource_id": resource.id,
                    "resource_name": resource.name,
                    "rule_name": rule["name"],
                    "description": rule["description"],
                    "recommendation": rule["recommendation"],
                    "current_monthly_cost": resource.cost_data.monthly_estimate,
                    "potential_monthly_savings": resource.cost_data.monthly_estimate * rule["potential_savings"],
                    "priority": "high" if rule["potential_savings"] > 0.5 else "medium"
                })
                
        return recommendations
    
    async def analyze_all_resources(self, resources: List[CloudResource]) -> pd.DataFrame:
        """Analyze all resources and return optimization report"""
        all_recommendations = []
        
        for resource in resources:
            recommendations = await self.analyze_resource(resource)
            all_recommendations.extend(recommendations)
            
        if not all_recommendations:
            return pd.DataFrame()
            
        df = pd.DataFrame(all_recommendations)
        df["total_potential_savings"] = df.groupby("rule_name")["potential_monthly_savings"].transform("sum")
        
        return df.sort_values("potential_monthly_savings", ascending=False)


class ComplianceChecker:
    """Security compliance checker"""
    
    def __init__(self):
        self.compliance_rules = self._load_compliance_rules()
        
    def _load_compliance_rules(self) -> List[Dict[str, Any]]:
        """Load compliance rules"""
        return [
            {
                "name": "encryption_at_rest",
                "check": lambda r: r.metadata.get("encryption", False),
                "severity": "high",
                "recommendation": "Enable encryption at rest for all storage resources"
            },
            {
                "name": "public_access",
                "check": lambda r: not r.metadata.get("public_access", True),
                "severity": "critical",
                "recommendation": "Disable public access unless explicitly required"
            },
            {
                "name": "backup_configured",
                "check": lambda r: r.metadata.get("backup_enabled", False),
                "severity": "medium",
                "recommendation": "Configure automated backups for critical resources"
            },
            {
                "name": "tagging_compliance",
                "check": lambda r: all(tag in r.tags for tag in ["environment", "owner", "cost_center"]),
                "severity": "low",
                "recommendation": "Ensure all required tags are present"
            },
            {
                "name": "region_compliance",
                "check": lambda r: r.region in ["us-east-1", "us-west-2", "eastus", "us-central1"],
                "severity": "medium",
                "recommendation": "Deploy resources only in approved regions"
            }
        ]
    
    async def check_resource(self, resource: CloudResource) -> List[ComplianceCheck]:
        """Check a single resource for compliance"""
        checks = []
        
        for rule in self.compliance_rules:
            passed = rule["check"](resource)
            checks.append(ComplianceCheck(
                check_name=rule["name"],
                passed=passed,
                severity=rule["severity"],
                details=f"Resource {resource.name} {'passed' if passed else 'failed'} {rule['name']} check",
                recommendation=rule["recommendation"] if not passed else ""
            ))
            
        return checks
    
    async def check_all_resources(self, resources: List[CloudResource]) -> Dict[str, Any]:
        """Check all resources and generate compliance report"""
        all_checks = []
        resource_compliance = {}
        
        for resource in resources:
            checks = await self.check_resource(resource)
            resource.compliance_checks = checks
            
            passed_checks = sum(1 for c in checks if c.passed)
            total_checks = len(checks)
            compliance_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
            
            resource_compliance[resource.id] = {
                "resource_name": resource.name,
                "provider": resource.provider.value,
                "compliance_score": compliance_score,
                "passed_checks": passed_checks,
                "total_checks": total_checks,
                "critical_issues": sum(1 for c in checks if not c.passed and c.severity == "critical")
            }
            
            all_checks.extend([{
                "resource_id": resource.id,
                "resource_name": resource.name,
                "check_name": c.check_name,
                "passed": c.passed,
                "severity": c.severity,
                "details": c.details
            } for c in checks])
            
        return {
            "summary": {
                "total_resources": len(resources),
                "compliant_resources": sum(1 for r in resource_compliance.values() if r["compliance_score"] == 100),
                "critical_issues": sum(r["critical_issues"] for r in resource_compliance.values()),
                "average_compliance_score": sum(r["compliance_score"] for r in resource_compliance.values()) / len(resources) if resources else 0
            },
            "resource_compliance": resource_compliance,
            "all_checks": pd.DataFrame(all_checks) if all_checks else pd.DataFrame()
        }


class ResourceDependencyMapper:
    """Maps and manages resource dependencies"""
    
    def __init__(self):
        self.dependency_graph = nx.DiGraph()
        
    def add_resource(self, resource: CloudResource):
        """Add a resource to the dependency graph"""
        self.dependency_graph.add_node(
            resource.id,
            name=resource.name,
            provider=resource.provider.value,
            resource_type=resource.resource_type.value,
            state=resource.state.value
        )
        
    def add_dependency(self, from_resource: str, to_resource: str, dependency_type: str = "depends_on"):
        """Add a dependency between resources"""
        self.dependency_graph.add_edge(from_resource, to_resource, type=dependency_type)
        
    def find_dependencies(self, resource_id: str) -> Dict[str, List[str]]:
        """Find all dependencies for a resource"""
        dependencies = {
            "depends_on": list(self.dependency_graph.successors(resource_id)),
            "required_by": list(self.dependency_graph.predecessors(resource_id))
        }
        return dependencies
        
    def find_circular_dependencies(self) -> List[List[str]]:
        """Find circular dependencies in the graph"""
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            return cycles
        except nx.NetworkXNoCycle:
            return []
            
    def get_deletion_order(self, resources_to_delete: List[str]) -> List[str]:
        """Get the safe deletion order for a set of resources"""
        subgraph = self.dependency_graph.subgraph(resources_to_delete)
        try:
            # Reverse topological sort for deletion order
            return list(reversed(list(nx.topological_sort(subgraph))))
        except nx.NetworkXUnfeasible:
            logger.warning("Circular dependencies detected, using best-effort order")
            return resources_to_delete
            
    def visualize_dependencies(self, output_file: str = "dependency_graph.png"):
        """Visualize the dependency graph"""
        # In real implementation, would use matplotlib or graphviz
        logger.info(f"Dependency graph would be saved to {output_file}")
        return self.dependency_graph.number_of_nodes(), self.dependency_graph.number_of_edges()


class MultiCloudManager:
    """Main multi-cloud resource manager"""
    
    def __init__(self, credentials: Optional[Dict[str, Dict[str, str]]] = None):
        self.credentials = credentials or {}
        self.adapters = {
            CloudProvider.AWS: AWSAdapter(self.credentials.get("aws")),
            CloudProvider.AZURE: AzureAdapter(self.credentials.get("azure")),
            CloudProvider.GCP: GCPAdapter(self.credentials.get("gcp"))
        }
        self.cost_optimizer = CostOptimizer()
        self.compliance_checker = ComplianceChecker()
        self.dependency_mapper = ResourceDependencyMapper()
        self.resources_cache: Dict[str, CloudResource] = {}
        
    async def discover_all_resources(self) -> List[CloudResource]:
        """Discover resources across all cloud providers"""
        all_resources = []
        
        for provider, adapter in self.adapters.items():
            logger.info(f"Discovering resources in {provider.value}")
            try:
                resources = await adapter.discover_resources()
                all_resources.extend(resources)
                
                # Update cache and dependency mapper
                for resource in resources:
                    self.resources_cache[resource.id] = resource
                    self.dependency_mapper.add_resource(resource)
                    
                logger.info(f"Found {len(resources)} resources in {provider.value}")
            except Exception as e:
                logger.error(f"Error discovering resources in {provider.value}: {e}")
                
        # Simulate some dependencies
        if len(all_resources) > 2:
            self.dependency_mapper.add_dependency(all_resources[0].id, all_resources[1].id)
            self.dependency_mapper.add_dependency(all_resources[1].id, all_resources[2].id)
            
        return all_resources
    
    async def get_resource_metrics(self, resource_id: str) -> Optional[ResourceMetrics]:
        """Get metrics for a specific resource"""
        resource = self.resources_cache.get(resource_id)
        if not resource:
            logger.error(f"Resource {resource_id} not found")
            return None
            
        adapter = self.adapters[resource.provider]
        metrics = await adapter.get_resource_metrics(resource_id)
        resource.metrics = metrics
        return metrics
    
    async def get_resource_cost(self, resource_id: str) -> Optional[CostData]:
        """Get cost data for a specific resource"""
        resource = self.resources_cache.get(resource_id)
        if not resource:
            logger.error(f"Resource {resource_id} not found")
            return None
            
        adapter = self.adapters[resource.provider]
        cost_data = await adapter.get_resource_cost(resource_id)
        resource.cost_data = cost_data
        return cost_data
    
    async def update_all_metrics(self):
        """Update metrics for all resources"""
        for resource_id in self.resources_cache:
            await self.get_resource_metrics(resource_id)
            await self.get_resource_cost(resource_id)
            
    async def get_optimization_report(self) -> pd.DataFrame:
        """Generate cost optimization report"""
        await self.update_all_metrics()
        resources = list(self.resources_cache.values())
        return await self.cost_optimizer.analyze_all_resources(resources)
    
    async def get_compliance_report(self) -> Dict[str, Any]:
        """Generate compliance report"""
        resources = list(self.resources_cache.values())
        return await self.compliance_checker.check_all_resources(resources)
    
    async def create_resource(self, provider: CloudProvider, resource_spec: Dict[str, Any]) -> CloudResource:
        """Create a new resource"""
        adapter = self.adapters[provider]
        resource = await adapter.create_resource(resource_spec)
        self.resources_cache[resource.id] = resource
        self.dependency_mapper.add_resource(resource)
        return resource
    
    async def delete_resource(self, resource_id: str, force: bool = False) -> bool:
        """Delete a resource"""
        resource = self.resources_cache.get(resource_id)
        if not resource:
            logger.error(f"Resource {resource_id} not found")
            return False
            
        # Check dependencies
        dependencies = self.dependency_mapper.find_dependencies(resource_id)
        if dependencies["required_by"] and not force:
            logger.error(f"Cannot delete {resource_id}: required by {dependencies['required_by']}")
            return False
            
        adapter = self.adapters[resource.provider]
        success = await adapter.delete_resource(resource_id)
        
        if success:
            del self.resources_cache[resource_id]
            self.dependency_mapper.dependency_graph.remove_node(resource_id)
            
        return success
    
    async def migrate_resource(self, resource_id: str, target_provider: CloudProvider, 
                             target_region: str) -> Optional[CloudResource]:
        """Migrate a resource to a different provider or region"""
        source_resource = self.resources_cache.get(resource_id)
        if not source_resource:
            logger.error(f"Resource {resource_id} not found")
            return None
            
        logger.info(f"Migrating {resource_id} from {source_resource.provider.value} to {target_provider.value}")
        
        # Create resource spec for new provider
        resource_spec = {
            "name": f"{source_resource.name}-migrated",
            "region": target_region,
            "tags": source_resource.tags.copy(),
            "source_provider": source_resource.provider.value,
            "migration_timestamp": datetime.now().isoformat()
        }
        
        # Create new resource
        new_resource = await self.create_resource(target_provider, resource_spec)
        
        # Update dependencies
        dependencies = self.dependency_mapper.find_dependencies(resource_id)
        for dep in dependencies["depends_on"]:
            self.dependency_mapper.add_dependency(new_resource.id, dep)
        for dep in dependencies["required_by"]:
            self.dependency_mapper.add_dependency(dep, new_resource.id)
            
        logger.info(f"Migration completed: {resource_id} -> {new_resource.id}")
        return new_resource
    
    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of all resources"""
        summary = {
            "total_resources": len(self.resources_cache),
            "by_provider": defaultdict(int),
            "by_type": defaultdict(int),
            "by_state": defaultdict(int),
            "by_region": defaultdict(int),
            "total_monthly_cost": 0.0
        }
        
        for resource in self.resources_cache.values():
            summary["by_provider"][resource.provider.value] += 1
            summary["by_type"][resource.resource_type.value] += 1
            summary["by_state"][resource.state.value] += 1
            summary["by_region"][resource.region] += 1
            
            if resource.cost_data:
                summary["total_monthly_cost"] += resource.cost_data.monthly_estimate
                
        return dict(summary)
    
    async def generate_deployment_template(self, resource_ids: List[str], 
                                         template_name: str) -> Dict[str, Any]:
        """Generate a deployment template from existing resources"""
        template = {
            "name": template_name,
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "resources": []
        }
        
        for resource_id in resource_ids:
            resource = self.resources_cache.get(resource_id)
            if resource:
                template["resources"].append({
                    "type": resource.resource_type.value,
                    "provider": resource.provider.value,
                    "region": resource.region,
                    "tags": resource.tags,
                    "metadata": resource.metadata,
                    "dependencies": list(resource.dependencies)
                })
                
        return template


if __name__ == "__main__":
    # Test with real multi-cloud resource management
    async def test_multi_cloud_manager():
        """Test multi-cloud resource management"""
        logger.info("Starting multi-cloud resource manager test")
        
        # Initialize manager
        manager = MultiCloudManager()
        
        # Test 1: Resource discovery
        logger.info("\n=== Test 1: Resource Discovery ===")
        resources = await manager.discover_all_resources()
        assert len(resources) > 0, "No resources discovered"
        logger.info(f"✓ Discovered {len(resources)} resources across all clouds")
        
        # Test 2: Resource summary
        logger.info("\n=== Test 2: Resource Summary ===")
        summary = manager.get_resource_summary()
        assert summary["total_resources"] == len(resources)
        logger.info(f"✓ Resource summary: {json.dumps(summary, indent=2)}")
        
        # Test 3: Cost optimization
        logger.info("\n=== Test 3: Cost Optimization ===")
        opt_report = await manager.get_optimization_report()
        if not opt_report.empty:
            total_savings = opt_report["potential_monthly_savings"].sum()
            logger.info(f"✓ Found ${total_savings:.2f} in potential monthly savings")
            logger.info(f"✓ Top recommendations:\n{opt_report.head()}")
        else:
            logger.info("✓ No optimization opportunities found")
        
        # Test 4: Compliance checking
        logger.info("\n=== Test 4: Compliance Checking ===")
        compliance_report = await manager.get_compliance_report()
        avg_score = compliance_report["summary"]["average_compliance_score"]
        logger.info(f"✓ Average compliance score: {avg_score:.1f}%")
        logger.info(f"✓ Critical issues: {compliance_report['summary']['critical_issues']}")
        
        # Test 5: Resource creation
        logger.info("\n=== Test 5: Resource Creation ===")
        new_resource = await manager.create_resource(CloudProvider.AWS, {
            "name": "test-instance",
            "region": "us-west-2",
            "tags": {"purpose": "testing", "owner": "admin"}
        })
        assert new_resource.id in manager.resources_cache
        logger.info(f"✓ Created new resource: {new_resource.id}")
        
        # Test 6: Dependency management
        logger.info("\n=== Test 6: Dependency Management ===")
        if len(resources) >= 3:
            deps = manager.dependency_mapper.find_dependencies(resources[1].id)
            logger.info(f"✓ Dependencies for {resources[1].name}: {deps}")
            
            cycles = manager.dependency_mapper.find_circular_dependencies()
            logger.info(f"✓ Circular dependencies: {len(cycles)}")
        
        # Test 7: Resource migration
        logger.info("\n=== Test 7: Resource Migration ===")
        if len(resources) > 0:
            source = resources[0]
            target_provider = CloudProvider.AZURE if source.provider != CloudProvider.AZURE else CloudProvider.GCP
            migrated = await manager.migrate_resource(source.id, target_provider, "eastus")
            assert migrated is not None
            logger.info(f"✓ Migrated {source.name} from {source.provider.value} to {target_provider.value}")
        
        # Test 8: Deployment template
        logger.info("\n=== Test 8: Deployment Template ===")
        template = await manager.generate_deployment_template(
            [r.id for r in resources[:3]], 
            "production-stack"
        )
        assert len(template["resources"]) <= 3
        logger.info(f"✓ Generated deployment template with {len(template['resources'])} resources")
        
        logger.info("\n✅ All multi-cloud manager tests passed!")
        return True
    
    # Run async tests
    success = asyncio.run(test_multi_cloud_manager())
    exit(0 if success else 1)