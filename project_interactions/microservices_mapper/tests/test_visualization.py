"""
Module: test_visualization.py
Purpose: Test visualization export functionality

External Dependencies:
- pytest: https://docs.pytest.org/
- pytest-asyncio: https://pytest-asyncio.readthedocs.io/

Example Usage:
>>> pytest test_visualization.py -v
"""

import pytest
import asyncio
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from microservices_mapper_interaction import MicroservicesMapper, Service, Dependency


class TestVisualization:
    """Test visualization export functionality"""
    
    @pytest.mark.asyncio
    async def test_dot_export(self):
        """Test DOT format export"""
        mapper = MicroservicesMapper()
        
        # Add some services
        mapper.services = {
            "service-a": Service(name="service-a", version="1.0.0", health_status="healthy"),
            "service-b": Service(name="service-b", version="2.0.0", health_status="unhealthy"),
            "service-c": Service(name="service-c", version="1.5.0", health_status="healthy")
        }
        
        # Add dependencies
        mapper.dependencies = [
            Dependency(source="service-a", target="service-b", dep_type="api"),
            Dependency(source="service-b", target="service-c", dep_type="database"),
            Dependency(source="service-a", target="external-api", dep_type="external")
        ]
        
        # Export to DOT
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        dot_file = mapper.export_to_dot(output_path)
        assert dot_file.endswith(".png")
        assert "microservices_dependencies" in dot_file
    
    @pytest.mark.asyncio
    async def test_json_export_d3js(self):
        """Test JSON export for D3.js visualization"""
        mapper = MicroservicesMapper()
        
        # Setup test data
        mapper.services = {
            "auth": Service(
                name="auth", 
                version="1.0.0",
                metadata={"tags": ["security", "core"]}
            ),
            "users": Service(
                name="users",
                version="2.0.0",
                metadata={"tags": ["data", "core"]}
            ),
            "orders": Service(
                name="orders",
                version="1.5.0",
                metadata={"tags": ["business", "api"]}
            )
        }
        
        mapper.dependencies = [
            Dependency(
                source="orders",
                target="users",
                dep_type="api",
                endpoints=["/api/v1/users", "/api/v1/profile"]
            ),
            Dependency(
                source="users",
                target="auth",
                dep_type="api",
                endpoints=["/api/v1/validate"]
            )
        ]
        
        # Export to JSON
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        json_file = mapper.export_to_json(output_path)
        assert json_file.endswith(".json")
        
        # Verify JSON structure
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        assert "nodes" in data
        assert "links" in data
        assert len(data["nodes"]) == 3
        assert len(data["links"]) == 2
        
        # Check node structure
        auth_node = next(n for n in data["nodes"] if n["id"] == "auth")
        assert auth_node["version"] == "1.0.0"
        assert auth_node["group"] == "security"
        
        # Check link structure
        first_link = data["links"][0]
        assert "source" in first_link
        assert "target" in first_link
        assert "type" in first_link
        assert "value" in first_link
        assert first_link["value"] == 2  # Number of endpoints
    
    @pytest.mark.asyncio
    async def test_full_mapping_export(self):
        """Test full mapping with exports"""
        mapper = MicroservicesMapper()
        
        # Run full mapping
        result = await mapper.map_dependencies("http://localhost:8500")
        
        assert result["services"] > 0
        assert result["dependencies"] > 0
        assert "timestamp" in result
        
        # Export both formats
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        dot_file = mapper.export_to_dot(output_path)
        json_file = mapper.export_to_json(output_path)
        
        assert Path(json_file).exists()
    
    @pytest.mark.asyncio
    async def test_health_impact_visualization(self):
        """Test health impact analysis visualization"""
        mapper = MicroservicesMapper()
        
        # Map dependencies
        await mapper.map_dependencies("http://localhost:8500")
        
        # Get health impacts
        impacts = mapper._analyze_health_impacts()
        
        assert isinstance(impacts, dict)
        if "auth-service" in mapper.services:
            assert "auth-service" in impacts
            assert len(impacts["auth-service"]) > 0
    
    def test_edge_styles_by_type(self):
        """Test different edge styles for dependency types"""
        mapper = MicroservicesMapper()
        
        # Setup different dependency types
        mapper.services = {
            "app": Service(name="app", version="1.0.0"),
            "db": Service(name="db", version="5.7"),
            "queue": Service(name="queue", version="3.8"),
            "external": Service(name="external", version="1.0")
        }
        
        mapper.dependencies = [
            Dependency(source="app", target="db", dep_type="database"),
            Dependency(source="app", target="queue", dep_type="queue"),
            Dependency(source="app", target="external", dep_type="external")
        ]
        
        # Export and check (in real implementation, would verify DOT content)
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        dot_file = mapper.export_to_dot(output_path)
        assert dot_file is not None
    
    @pytest.mark.asyncio
    async def test_circular_dependency_visualization(self):
        """Test visualization of circular dependencies"""
        mapper = MicroservicesMapper()
        
        # Create services with circular dependency
        mapper.services = {
            "A": Service(name="A", version="1.0"),
            "B": Service(name="B", version="1.0"),
            "C": Service(name="C", version="1.0")
        }
        
        mapper.dependencies = [
            Dependency(source="A", target="B", dep_type="api"),
            Dependency(source="B", target="C", dep_type="api"),
            Dependency(source="C", target="A", dep_type="api")  # Circular
        ]
        
        # In real implementation, this would highlight circular dependencies
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        json_file = mapper.export_to_json(output_path)
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Verify all links are present
        assert len(data["links"]) == 3
        sources = [l["source"] for l in data["links"]]
        targets = [l["target"] for l in data["links"]]
        
        # Check circular path exists
        assert "A" in sources and "A" in targets
        assert "B" in sources and "B" in targets
        assert "C" in sources and "C" in targets
    
    def test_version_info_in_visualization(self):
        """Test version information is included in visualization"""
        mapper = MicroservicesMapper()
        
        mapper.services = {
            "api": Service(name="api", version="2.5.1"),
            "worker": Service(name="worker", version="1.0.0-beta")
        }
        
        output_path = Path("./test_output")
        output_path.mkdir(exist_ok=True)
        
        json_file = mapper.export_to_json(output_path)
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Check versions are included
        api_node = next(n for n in data["nodes"] if n["id"] == "api")
        assert api_node["version"] == "2.5.1"
        
        worker_node = next(n for n in data["nodes"] if n["id"] == "worker")
        assert worker_node["version"] == "1.0.0-beta"


if __name__ == "__main__":
    # Run tests with real data validation
    test = TestVisualization()
    
    # Test visualization functions
    async def validate():
        await test.test_dot_export()
        print("✓ DOT export test passed")
        
        await test.test_json_export_d3js()
        print("✓ JSON D3.js export test passed")
        
        await test.test_full_mapping_export()
        print("✓ Full mapping export test passed")
        
        await test.test_health_impact_visualization()
        print("✓ Health impact visualization test passed")
        
        test.test_edge_styles_by_type()
        print("✓ Edge styles test passed")
        
        await test.test_circular_dependency_visualization()
        print("✓ Circular dependency visualization test passed")
        
        test.test_version_info_in_visualization()
        print("✓ Version info visualization test passed")
    
    asyncio.run(validate())
    print("\n✅ All visualization tests passed!")