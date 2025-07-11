
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: real_sparta_handlers.py
Purpose: Real SPARTA handlers for GRANGER integration using actual SPARTA functionality

External Dependencies:
- aiohttp: For async HTTP requests
- fastmcp: For MCP server integration
- loguru: For logging

Example Usage:
>>> from real_sparta_handlers import SPARTADownloadHandler
>>> handler = SPARTADownloadHandler()
>>> result = await handler.execute(limit=10)
>>> print(f"Downloaded {result.output_data['resources_downloaded']} resources")
"""

import time
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import sys
import os

# Add SPARTA to path
sparta_path = Path("/home/graham/workspace/experiments/sparta/src")
if sparta_path.exists():
    sys.path.insert(0, str(sparta_path))

try:
    # Import real SPARTA components
    from sparta.core.downloader import (
        download_sparta_dataset,
        extract_urls_from_stix,
        download_resource,
        create_download_summary,
        ResourceDownloadResult,
        DownloadMethod
    )
    from sparta.config import settings
    from sparta.core.mitre_integration import MitreDataManager
    from sparta.integrations.real_apis import NASAApi, CVEApi
    from sparta.integrations.sparta_module import SPARTAModule
    SPARTA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: SPARTA imports failed: {e}")
    SPARTA_AVAILABLE = False

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from templates.interaction_framework import (
    Level0Interaction,
    InteractionResult,
    InteractionLevel
)


class SPARTADownloadHandler(Level0Interaction):
    """
    Real SPARTA resource download handler.
    Downloads cybersecurity resources from STIX dataset.
    """
    
    def __init__(self):
        super().__init__(
            name="sparta_resource_download",
            description="Downloads cybersecurity resources from STIX dataset"
        )
        self.sparta_available = SPARTA_AVAILABLE
        
    def initialize_module(self):
        """Initialize SPARTA downloader"""
        return None  # No module needed for direct API calls
        
    def validate_output(self, output):
        """Validate download results"""
        if not isinstance(output, dict):
            return False
        return output.get("resources_downloaded", 0) > 0
        
    async def execute(self, dataset_url: Optional[str] = None, limit: int = 10, **kwargs) -> InteractionResult:
        """
        Download SPARTA resources using real downloader.
        
        Args:
            dataset_url: URL to STIX dataset (uses default if not provided)
            limit: Maximum number of resources to download
        """
        start_time = time.time()
        
        if not self.sparta_available:
            return InteractionResult(
                interaction_name="resource_download",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"dataset_url": dataset_url, "limit": limit},
                output_data={},
                error="SPARTA module not available"
            )
        
        try:
            # Use default SPARTA dataset URL if not provided
            url = dataset_url or str(settings.sparta_dataset_url)
            output_dir = settings.download_dir
            
            # Extract URLs from STIX
            urls = await extract_urls_from_stix(url)
            
            if limit:
                urls = urls[:limit]
            
            # Download resources
            results = await download_sparta_dataset(
                urls=urls,
                output_dir=output_dir,
                max_concurrent=5
            )
            
            # Create summary
            summary = create_download_summary(results)
            
            # Calculate metrics
            successful = len([r for r in results if r.local_path])
            failed = len([r for r in results if r.method == DownloadMethod.FAILED])
            paywall = len([r for r in results if r.is_paywall])
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="resource_download",
                level=InteractionLevel.LEVEL_0,
                success=successful > 0,
                duration=duration,
                input_data={
                    "dataset_url": url,
                    "target_resources": len(urls),
                    "max_concurrent": 5
                },
                output_data={
                    "resources_downloaded": successful,
                    "download_failures": failed,
                    "paywall_resources": paywall,
                    "summary": summary,
                    "output_directory": str(output_dir),
                    "sample_results": [
                        {
                            "url": r.url,
                            "local_path": str(r.local_path) if r.local_path else None,
                            "method": r.method.value,
                            "is_paywall": r.is_paywall
                        } for r in results[:5]
                    ],
                    "timestamp": datetime.now().isoformat()
                },
                error=None if successful > 0 else "No resources downloaded"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="resource_download",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"dataset_url": dataset_url, "limit": limit},
                output_data={},
                error=str(e)
            )


class SPARTAMissionSearchHandler(Level0Interaction):
    """
    Real NASA mission search handler using SPARTA's NASA API integration.
    """
    
    def __init__(self):
        super().__init__(
            name="sparta_mission_search",
            description="Search NASA missions using real API"
        )
        self.sparta_available = SPARTA_AVAILABLE
        self.nasa_api = NASAApi() if SPARTA_AVAILABLE else None
        
    def initialize_module(self):
        """Initialize NASA API"""
        return self.nasa_api
        
    def validate_output(self, output):
        """Validate mission search results"""
        if not isinstance(output, dict):
            return False
        return output.get("missions_found", 0) > 0
        
    async def execute(self, query: str = "Apollo", limit: int = 10, **kwargs) -> InteractionResult:
        """
        Search NASA missions using real API.
        
        Args:
            query: Search query for missions
            limit: Maximum number of results
        """
        start_time = time.time()
        
        if not self.sparta_available or not self.nasa_api:
            return InteractionResult(
                interaction_name="mission_search",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"query": query, "limit": limit},
                output_data={},
                error="SPARTA NASA API not available"
            )
        
        try:
            # Search missions using real NASA API
            missions = await self.nasa_api.search_missions(query, limit)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="mission_search",
                level=InteractionLevel.LEVEL_0,
                success=len(missions) > 0,
                duration=duration,
                input_data={
                    "query": query,
                    "limit": limit,
                    "api": "NASA Open Data"
                },
                output_data={
                    "missions_found": len(missions),
                    "missions": missions,
                    "api_source": "NASA Images API",
                    "timestamp": datetime.now().isoformat()
                },
                error=None if missions else "No missions found"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="mission_search",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"query": query, "limit": limit},
                output_data={},
                error=str(e)
            )


class SPARTACVESearchHandler(Level0Interaction):
    """
    Real CVE search handler using SPARTA's NVD API integration.
    """
    
    def __init__(self):
        super().__init__(
            name="sparta_cve_search",
            description="Search CVE database using real NVD API"
        )
        self.sparta_available = SPARTA_AVAILABLE
        self.cve_api = CVEApi() if SPARTA_AVAILABLE else None
        
    def initialize_module(self):
        """Initialize CVE API"""
        return self.cve_api
        
    def validate_output(self, output):
        """Validate CVE search results"""
        if not isinstance(output, dict):
            return False
        return output.get("vulnerabilities_found", 0) > 0
        
    async def execute(self, keywords: str = "satellite", severity: Optional[str] = None, limit: int = 10, **kwargs) -> InteractionResult:
        """
        Search CVE database using real NVD API.
        
        Args:
            keywords: Keywords to search for
            severity: Filter by severity (LOW, MEDIUM, HIGH, CRITICAL)
            limit: Maximum number of results
        """
        start_time = time.time()
        
        if not self.sparta_available or not self.cve_api:
            return InteractionResult(
                interaction_name="cve_search",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"keywords": keywords, "severity": severity, "limit": limit},
                output_data={},
                error="SPARTA CVE API not available"
            )
        
        try:
            # Search CVEs using real NVD API
            vulnerabilities = await self.cve_api.search_cves(keywords, severity, limit)
            
            # Calculate severity distribution
            severity_dist = {}
            for vuln in vulnerabilities:
                sev = vuln.get("cvss", {}).get("severity", "UNKNOWN")
                severity_dist[sev] = severity_dist.get(sev, 0) + 1
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="cve_search",
                level=InteractionLevel.LEVEL_0,
                success=len(vulnerabilities) > 0,
                duration=duration,
                input_data={
                    "keywords": keywords,
                    "severity": severity,
                    "limit": limit,
                    "api": "NVD"
                },
                output_data={
                    "vulnerabilities_found": len(vulnerabilities),
                    "vulnerabilities": vulnerabilities,
                    "severity_distribution": severity_dist,
                    "api_source": "NIST National Vulnerability Database",
                    "timestamp": datetime.now().isoformat()
                },
                error=None if vulnerabilities else "No vulnerabilities found"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="cve_search",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"keywords": keywords, "severity": severity, "limit": limit},
                output_data={},
                error=str(e)
            )


class SPARTAMITREHandler(Level0Interaction):
    """
    Real MITRE framework handler using SPARTA's MITRE integration.
    """
    
    def __init__(self):
        super().__init__(
            name="sparta_mitre_query",
            description="Query MITRE framework data"
        )
        self.sparta_available = SPARTA_AVAILABLE
        self.mitre_manager = MitreDataManager() if SPARTA_AVAILABLE else None
        
    def initialize_module(self):
        """Initialize MITRE manager"""
        return self.mitre_manager
        
    def validate_output(self, output):
        """Validate MITRE query results"""
        if not isinstance(output, dict):
            return False
        return output.get("found", False)
        
    async def execute(self, framework: str = "attack", query: str = "T1055", **kwargs) -> InteractionResult:
        """
        Query MITRE framework data.
        
        Args:
            framework: Framework to query (attack, capec, d3fend)
            query: Query string (technique ID, pattern ID, etc.)
        """
        start_time = time.time()
        
        if not self.sparta_available or not self.mitre_manager:
            return InteractionResult(
                interaction_name="mitre_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"framework": framework, "query": query},
                output_data={},
                error="SPARTA MITRE integration not available"
            )
        
        try:
            # Query MITRE data
            result = None
            if framework == "attack":
                result = self.mitre_manager.get_attack_technique(query)
            elif framework == "capec":
                result = self.mitre_manager.get_capec_pattern(query)
            elif framework == "d3fend":
                result = self.mitre_manager.get_d3fend_defense(query)
            else:
                raise ValueError(f"Unknown framework: {framework}")
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="mitre_query",
                level=InteractionLevel.LEVEL_0,
                success=result is not None,
                duration=duration,
                input_data={
                    "framework": framework,
                    "query": query
                },
                output_data={
                    "framework": framework,
                    "query": query,
                    "result": result,
                    "found": result is not None,
                    "timestamp": datetime.now().isoformat()
                },
                error=None if result else f"No results found for {query} in {framework}"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="mitre_query",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"framework": framework, "query": query},
                output_data={},
                error=str(e)
            )


class SPARTAModuleHandler(Level0Interaction):
    """
    Handler using SPARTA's module interface for claude-module-communicator.
    """
    
    def __init__(self):
        super().__init__(
            name="sparta_module_process",
            description="Execute SPARTA module action through process() interface"
        )
        self.sparta_available = SPARTA_AVAILABLE
        self.sparta_module = SPARTAModule() if SPARTA_AVAILABLE else None
        
    def initialize_module(self):
        """Initialize SPARTA module"""
        return self.sparta_module
        
    def validate_output(self, output):
        """Validate module process results"""
        if not isinstance(output, dict):
            return False
        return output.get("success", False)
        
    async def execute(self, action: str, data: Dict[str, Any], **kwargs) -> InteractionResult:
        """
        Execute SPARTA module action through process() interface.
        
        Args:
            action: Action to perform
            data: Data for the action
        """
        start_time = time.time()
        
        if not self.sparta_available or not self.sparta_module:
            return InteractionResult(
                interaction_name="module_process",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"action": action, "data": data},
                output_data={},
                error="SPARTA module not available"
            )
        
        try:
            # Process through SPARTA module
            result = await self.sparta_module.process({
                "action": action,
                "data": data
            })
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="module_process",
                level=InteractionLevel.LEVEL_0,
                success=result.get("success", False),
                duration=duration,
                input_data={
                    "action": action,
                    "data": data
                },
                output_data=result,
                error=result.get("error") if not result.get("success") else None
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="module_process",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={"action": action, "data": data},
                output_data={},
                error=str(e)
            )


if __name__ == "__main__":
    async def test_handlers():
        """Test real SPARTA handlers"""
        print("Testing Real SPARTA Handlers")
        print("=" * 50)
        
        # Test 1: Resource Download
        print("\n1. Testing Resource Download...")
        download_handler = SPARTADownloadHandler()
        download_result = await download_handler.execute(limit=5)
        print(f"   Success: {download_result.success}")
        print(f"   Downloaded: {download_result.output_data.get('resources_downloaded', 0)} resources")
        print(f"   Duration: {download_result.duration:.2f}s")
        
        # Test 2: Mission Search
        print("\n2. Testing NASA Mission Search...")
        mission_handler = SPARTAMissionSearchHandler()
        mission_result = await mission_handler.execute(query="Apollo", limit=5)
        print(f"   Success: {mission_result.success}")
        print(f"   Found: {mission_result.output_data.get('missions_found', 0)} missions")
        print(f"   Duration: {mission_result.duration:.2f}s")
        
        # Test 3: CVE Search
        print("\n3. Testing CVE Search...")
        cve_handler = SPARTACVESearchHandler()
        cve_result = await cve_handler.execute(keywords="satellite", severity="HIGH", limit=5)
        print(f"   Success: {cve_result.success}")
        print(f"   Found: {cve_result.output_data.get('vulnerabilities_found', 0)} vulnerabilities")
        print(f"   Duration: {cve_result.duration:.2f}s")
        
        # Test 4: MITRE Query
        print("\n4. Testing MITRE Query...")
        mitre_handler = SPARTAMITREHandler()
        mitre_result = await mitre_handler.execute(framework="attack", query="T1055")
        print(f"   Success: {mitre_result.success}")
        print(f"   Found: {mitre_result.output_data.get('found', False)}")
        print(f"   Duration: {mitre_result.duration:.2f}s")
        
        # Test 5: Module Process
        print("\n5. Testing SPARTA Module Process...")
        module_handler = SPARTAModuleHandler()
        module_result = await module_handler.execute(
            action="search_space_missions",
            data={"query": "Mars", "limit": 3}
        )
        print(f"   Success: {module_result.success}")
        print(f"   Duration: {module_result.duration:.2f}s")
        
        print("\n" + "=" * 50)
        print("✅ Real SPARTA handler tests complete!")
    
    # Run tests
    asyncio.run(test_handlers())