"""
Module: test_security_policies.py
Purpose: Test security policy features of service mesh manager

External Dependencies:
- pytest: https://docs.pytest.org/
- typing: https://docs.python.org/3/library/typing.html

Example Usage:
>>> pytest test_security_policies.py -v
test_mtls_configuration PASSED
test_authorization_policies PASSED
"""

import pytest
from typing import Dict, List, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from service_mesh_manager_interaction import (
    ServiceMeshManager, MeshProvider, ServiceEndpoint,
    MutualTLSConfig, AuthorizationPolicy, RateLimitConfig
)


class TestSecurityPolicies:
    """Test security policy configurations"""
    
    @pytest.fixture
    def manager(self):
        """Create service mesh manager instance"""
        return ServiceMeshManager(MeshProvider.ISTIO)
    
    @pytest.fixture
    def secure_service(self):
        """Create secure service endpoint"""
        return ServiceEndpoint(
            name="secure-api",
            namespace="secure",
            port=443,
            protocol="https",
            labels={"security": "high", "compliance": "pci"}
        )
    
    def test_mtls_configuration(self, manager):
        """Test mutual TLS configuration"""
        # Test strict mode
        strict_mtls = manager.configure_mtls(
            namespace="production",
            mode="STRICT"
        )
        
        assert strict_mtls["kind"] == "PeerAuthentication"
        assert strict_mtls["spec"]["mtls"]["mode"] == "STRICT"
        assert strict_mtls["metadata"]["namespace"] == "production"
        
        # Test with port exclusions
        mtls_with_exclusions = manager.configure_mtls(
            namespace="mixed",
            mode="STRICT",
            exclude_ports=[8080, 8081]  # Health check ports
        )
        
        assert "portLevelMtls" in mtls_with_exclusions["spec"]
        assert "8080" in mtls_with_exclusions["spec"]["portLevelMtls"]
        assert mtls_with_exclusions["spec"]["portLevelMtls"]["8080"]["mode"] == "DISABLE"
        
        print("✅ mTLS configuration test passed")
    
    def test_mtls_modes(self, manager):
        """Test different mTLS modes"""
        modes = ["DISABLE", "PERMISSIVE", "STRICT"]
        
        for mode in modes:
            config = manager.configure_mtls(
                namespace=f"test-{mode.lower()}",
                mode=mode
            )
            
            assert config["spec"]["mtls"]["mode"] == mode
            assert manager.apply_configuration(config)
        
        print("✅ mTLS modes test passed")
    
    def test_authorization_policies(self, manager, secure_service):
        """Test authorization policy creation"""
        manager.register_service(secure_service)
        
        # Test default authorization
        default_policy = manager.create_authorization_policy(
            secure_service.name,
            namespace=secure_service.namespace
        )
        
        assert default_policy["kind"] == "AuthorizationPolicy"
        assert default_policy["spec"]["action"] == "ALLOW"
        assert len(default_policy["spec"]["rules"]) > 0
        
        # Test custom rules
        custom_rules = [
            {
                "from": [
                    {"source": {"principals": ["cluster.local/ns/frontend/sa/webapp"]}},
                    {"source": {"namespaces": ["frontend", "api"]}}
                ],
                "to": [
                    {"operation": {"methods": ["GET", "POST"]}},
                    {"operation": {"paths": ["/api/*", "/health"]}}
                ],
                "when": [
                    {"key": "request.headers[x-api-key]", "values": ["*"]}
                ]
            }
        ]
        
        custom_policy = manager.create_authorization_policy(
            secure_service.name,
            namespace=secure_service.namespace,
            rules=custom_rules
        )
        
        assert custom_policy["spec"]["rules"] == custom_rules
        assert "selector" in custom_policy["spec"]
        assert custom_policy["spec"]["selector"]["matchLabels"]["app"] == secure_service.name
        
        print("✅ Authorization policies test passed")
    
    def test_rate_limiting(self, manager):
        """Test rate limiting configuration"""
        service = ServiceEndpoint("rate-limited-api", "production", 8080)
        manager.register_service(service)
        
        # Test basic rate limiting
        basic_rate_limit = RateLimitConfig(
            requests_per_unit=1000,
            unit="minute",
            burst_size=100
        )
        
        rate_limit_policy = manager.create_rate_limit_policy(
            service.name,
            namespace=service.namespace,
            rate_limit=basic_rate_limit
        )
        
        assert rate_limit_policy["kind"] == "EnvoyFilter"
        assert "configPatches" in rate_limit_policy["spec"]
        
        # Verify token bucket configuration
        patch = rate_limit_policy["spec"]["configPatches"][0]
        assert patch["applyTo"] == "HTTP_FILTER"
        assert "token_bucket" in patch["patch"]["value"]["typed_config"]["value"]
        
        token_bucket = patch["patch"]["value"]["typed_config"]["value"]["token_bucket"]
        assert token_bucket["max_tokens"] == 100
        assert token_bucket["tokens_per_fill"] == 1000
        
        print("✅ Rate limiting test passed")
    
    def test_advanced_rate_limiting(self, manager):
        """Test advanced rate limiting scenarios"""
        service = ServiceEndpoint("api-gateway", "production", 8080)
        manager.register_service(service)
        
        # Different rate limits for different time units
        time_units = ["second", "minute", "hour"]
        
        for unit in time_units:
            rate_limit = RateLimitConfig(
                requests_per_unit=100 if unit == "second" else 1000,
                unit=unit,
                burst_size=10,
                response_headers_to_add={
                    "X-RateLimit-Limit": "1000",
                    "X-RateLimit-Remaining": "DYNAMIC"
                }
            )
            
            policy = manager.create_rate_limit_policy(
                f"{service.name}-{unit}",
                namespace=service.namespace,
                rate_limit=rate_limit
            )
            
            assert policy is not None
            assert manager.apply_configuration(policy)
        
        print("✅ Advanced rate limiting test passed")
    
    def test_deny_authorization_policy(self, manager):
        """Test DENY authorization policies"""
        service = ServiceEndpoint("restricted-api", "secure", 8080)
        manager.register_service(service)
        
        # Create DENY policy for specific sources
        deny_rules = [
            {
                "from": [
                    {"source": {"notNamespaces": ["trusted", "secure"]}},
                    {"source": {"notPrincipals": ["cluster.local/ns/trusted/sa/*"]}}
                ]
            }
        ]
        
        policy_config = {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "AuthorizationPolicy",
            "metadata": {
                "name": f"{service.name}-deny",
                "namespace": service.namespace
            },
            "spec": {
                "selector": {
                    "matchLabels": {"app": service.name}
                },
                "action": "DENY",
                "rules": deny_rules
            }
        }
        
        success = manager.apply_configuration(policy_config)
        assert success
        
        print("✅ DENY authorization policy test passed")
    
    def test_jwt_authentication(self, manager):
        """Test JWT authentication configuration"""
        service = ServiceEndpoint("jwt-protected-api", "secure", 8080)
        manager.register_service(service)
        
        # JWT authentication policy
        jwt_policy = {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "RequestAuthentication",
            "metadata": {
                "name": f"{service.name}-jwt",
                "namespace": service.namespace
            },
            "spec": {
                "selector": {
                    "matchLabels": {"app": service.name}
                },
                "jwtRules": [
                    {
                        "issuer": "https://auth.example.com",
                        "jwksUri": "https://auth.example.com/.well-known/jwks.json",
                        "audiences": ["api.example.com"],
                        "forwardOriginalToken": True
                    }
                ]
            }
        }
        
        success = manager.apply_configuration(jwt_policy)
        assert success
        
        # Corresponding authorization policy
        authz_policy = manager.create_authorization_policy(
            service.name,
            namespace=service.namespace,
            rules=[{
                "from": [{"source": {"requestPrincipals": ["*"]}}],
                "to": [{"operation": {"methods": ["GET", "POST", "PUT", "DELETE"]}}]
            }]
        )
        
        assert authz_policy is not None
        
        print("✅ JWT authentication test passed")
    
    def test_security_headers(self, manager):
        """Test security headers configuration"""
        service = ServiceEndpoint("web-app", "production", 8080)
        manager.register_service(service)
        
        # Security headers via EnvoyFilter
        security_headers_config = {
            "apiVersion": "networking.istio.io/v1alpha3",
            "kind": "EnvoyFilter",
            "metadata": {
                "name": f"{service.name}-security-headers",
                "namespace": service.namespace
            },
            "spec": {
                "workloadSelector": {
                    "labels": {"app": service.name}
                },
                "configPatches": [{
                    "applyTo": "HTTP_FILTER",
                    "match": {
                        "context": "SIDECAR_INBOUND",
                        "listener": {
                            "filterChain": {
                                "filter": {
                                    "name": "envoy.filters.network.http_connection_manager",
                                    "subFilter": {
                                        "name": "envoy.filters.http.router"
                                    }
                                }
                            }
                        }
                    },
                    "patch": {
                        "operation": "INSERT_BEFORE",
                        "value": {
                            "name": "envoy.filters.http.header_to_metadata",
                            "typed_config": {
                                "@type": "type.googleapis.com/envoy.extensions.filters.http.header_to_metadata.v3.Config",
                                "response_rules": [
                                    {
                                        "header": "X-Content-Type-Options",
                                        "on_header_present": {
                                            "key": "nosniff",
                                            "value": "nosniff"
                                        }
                                    },
                                    {
                                        "header": "X-Frame-Options",
                                        "on_header_present": {
                                            "key": "frame_options",
                                            "value": "DENY"
                                        }
                                    },
                                    {
                                        "header": "X-XSS-Protection",
                                        "on_header_present": {
                                            "key": "xss_protection",
                                            "value": "1; mode=block"
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }]
            }
        }
        
        success = manager.apply_configuration(security_headers_config)
        assert success
        
        print("✅ Security headers test passed")
    
    def test_network_policies_integration(self, manager):
        """Test integration with network policies"""
        namespaces = ["frontend", "backend", "database"]
        
        # Configure mTLS for each namespace
        for ns in namespaces:
            mtls_config = manager.configure_mtls(namespace=ns, mode="STRICT")
            assert manager.apply_configuration(mtls_config)
        
        # Create authorization policies for service communication
        # Frontend can call backend
        frontend_to_backend = {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "AuthorizationPolicy",
            "metadata": {
                "name": "frontend-to-backend",
                "namespace": "backend"
            },
            "spec": {
                "action": "ALLOW",
                "rules": [{
                    "from": [{"source": {"namespaces": ["frontend"]}}],
                    "to": [{"operation": {"methods": ["GET", "POST"]}}]
                }]
            }
        }
        
        # Backend can call database
        backend_to_db = {
            "apiVersion": "security.istio.io/v1beta1",
            "kind": "AuthorizationPolicy",
            "metadata": {
                "name": "backend-to-database",
                "namespace": "database"
            },
            "spec": {
                "action": "ALLOW",
                "rules": [{
                    "from": [{"source": {"namespaces": ["backend"]}}],
                    "to": [{"operation": {"ports": ["5432", "3306"]}}]
                }]
            }
        }
        
        assert manager.apply_configuration(frontend_to_backend)
        assert manager.apply_configuration(backend_to_db)
        
        print("✅ Network policies integration test passed")
    
    def test_security_policy_validation(self, manager):
        """Test validation of security policies"""
        # Test invalid mTLS mode
        with pytest.raises(ValueError):
            MutualTLSConfig(mode="INVALID_MODE")
        
        # Test invalid rate limit unit
        with pytest.raises(ValueError):
            RateLimitConfig(unit="invalid_unit")
        
        # Test valid configurations
        valid_mtls = MutualTLSConfig(mode="STRICT")
        assert valid_mtls.mode == "STRICT"
        
        valid_rate_limit = RateLimitConfig(
            requests_per_unit=100,
            unit="minute",
            burst_size=10
        )
        assert valid_rate_limit.unit == "minute"
        
        print("✅ Security policy validation test passed")


# Run validation
if __name__ == "__main__":
    test = TestSecurityPolicies()
    manager = ServiceMeshManager()
    
    # Create a secure service for testing
    secure_service = ServiceEndpoint(
        name="secure-api",
        namespace="secure",
        port=443,
        protocol="https",
        labels={"security": "high", "compliance": "pci"}
    )
    
    # Test core security features
    test.test_mtls_configuration(manager)
    test.test_mtls_modes(manager)
    test.test_authorization_policies(manager, secure_service)
    test.test_rate_limiting(manager)
    test.test_jwt_authentication(manager)
    test.test_security_headers(manager)
    test.test_network_policies_integration(manager)
    
    print("\n✅ All security policy tests passed!")