#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module-Specific Performance Optimizations

This module contains targeted optimizations for specific issues discovered
during GRANGER integration testing:

1. ArangoDB connection URL fix
2. Marker dependency resolution
3. SPARTA API authentication
4. Error recovery and retry logic
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from functools import wraps
from urllib.parse import urlparse

# Add paths
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments')


class ArangoDBOptimizations:
    """Optimizations for ArangoDB connection and API issues"""
    
    @staticmethod
    def fix_connection_url(url: str) -> str:
        """Fix ArangoDB connection URL format"""
        # Common issue: 'localhost' instead of 'http://localhost:8529'
        if url == 'localhost':
            return 'http://localhost:8529'
        
        # Handle localhost:port format
        if url.startswith('localhost:'):
            return f'http://{url}'
            
        # Ensure proper URL format
        parsed = urlparse(url)
        if not parsed.scheme:
            # Add http:// if missing
            if ':' in url:  # Has port
                return f'http://{url}'
            else:
                return f'http://{url}:8529'
                
        return url
        
    @staticmethod
    def create_optimized_connection_string() -> Dict[str, str]:
        """Create optimized ArangoDB connection configuration"""
        return {
            "url": os.getenv('ARANGO_HOST', 'http://localhost:8529'),
            "username": os.getenv('ARANGO_USER', 'root'),
            "password": os.getenv('ARANGO_PASSWORD', 'openSesame'),
            "verify": False,  # For local development
            "max_retries": 3,
            "connection_timeout": 10,
            "request_timeout": 30
        }
        
    @staticmethod
    def fix_api_parameters(operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fix common API parameter mismatches"""
        fixed_params = params.copy()
        
        if operation == "create_document":
            # Fix: create_document(db, collection_name, doc) not (collection, doc)
            if "collection" in params and "data" in params:
                fixed_params["collection_name"] = params.pop("collection")
                fixed_params["document"] = params.pop("data")
                
        elif operation == "search":
            # Fix: Search functions don't accept collection_name parameter
            if "collection_name" in params:
                # Store collection for use in query
                collection = params.pop("collection_name")
                if "query" in params:
                    # Inject collection into AQL query if needed
                    fixed_params["collection_hint"] = collection
                    
        elif operation == "create_graph":
            # Fix: ensure_graph requires specific parameters
            if "graph_name" not in params:
                fixed_params["graph_name"] = "granger_knowledge_graph"
            if "edge_definitions" not in params:
                fixed_params["edge_definitions"] = [{
                    "edge_collection": "relationships",
                    "from_vertex_collections": ["documents"],
                    "to_vertex_collections": ["documents"]
                }]
                
        return fixed_params


class MarkerOptimizations:
    """Optimizations for Marker PDF processing"""
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """Check if required dependencies are available"""
        dependencies = {
            "marker": False,
            "pdftext": False,
            "pypdf": False,
            "pdfplumber": False
        }
        
        try:
            import marker
            dependencies["marker"] = True
        except ImportError:
            pass
            
        try:
            import pdftext
            dependencies["pdftext"] = True
        except ImportError:
            pass
            
        try:
            import PyPDF2
            dependencies["pypdf"] = True
        except ImportError:
            pass
            
        try:
            import pdfplumber
            dependencies["pdfplumber"] = True
        except ImportError:
            pass
            
        return dependencies
        
    @staticmethod
    def create_fallback_converter() -> Any:
        """Create fallback PDF converter if Marker unavailable"""
        dependencies = MarkerOptimizations.check_dependencies()
        
        if dependencies["marker"] and dependencies["pdftext"]:
            # Use actual Marker
            from marker import marker_pdf
            return marker_pdf
            
        elif dependencies["pypdf"]:
            # Fallback to PyPDF2
            return MarkerOptimizations._pypdf_converter
            
        elif dependencies["pdfplumber"]:
            # Fallback to pdfplumber
            return MarkerOptimizations._pdfplumber_converter
            
        else:
            # Last resort: basic text extraction
            return MarkerOptimizations._basic_converter
            
    @staticmethod
    def _pypdf_converter(pdf_path: str) -> str:
        """Convert PDF using PyPDF2"""
        import PyPDF2
        
        text = []
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text.append(page.extract_text())
                
        return "\n".join(text)
        
    @staticmethod
    def _pdfplumber_converter(pdf_path: str) -> str:
        """Convert PDF using pdfplumber"""
        import pdfplumber
        
        text = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
                    
        return "\n".join(text)
        
    @staticmethod
    def _basic_converter(pdf_path: str) -> str:
        """Basic fallback - just return path info"""
        return f"[PDF: {pdf_path}]\n[Conversion unavailable - missing dependencies]"


class SPARTAOptimizations:
    """Optimizations for SPARTA module issues"""
    
    @staticmethod
    def setup_api_authentication() -> Dict[str, str]:
        """Setup API authentication for various services"""
        auth_config = {}
        
        # NASA API
        nasa_key = os.getenv('NASA_API_KEY')
        if nasa_key:
            auth_config['nasa'] = {
                'api_key': nasa_key,
                'headers': {'X-API-Key': nasa_key}
            }
        else:
            # Use demo key with rate limits
            auth_config['nasa'] = {
                'api_key': 'DEMO_KEY',
                'headers': {},
                'rate_limit': 30  # requests per hour
            }
            
        # NVD API (no auth required but has rate limits)
        auth_config['nvd'] = {
            'headers': {
                'User-Agent': 'GRANGER/1.0 (granger@example.com)'
            },
            'rate_limit': 10  # requests per minute
        }
        
        # MITRE (no auth but respect robots.txt)
        auth_config['mitre'] = {
            'headers': {
                'User-Agent': 'GRANGER/1.0'
            },
            'rate_limit': 5  # requests per minute
        }
        
        return auth_config
        
    @staticmethod
    def ensure_download_directory(base_path: str = "/tmp/sparta_downloads") -> Path:
        """Ensure download directory exists"""
        download_dir = Path(base_path)
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (download_dir / "cve").mkdir(exist_ok=True)
        (download_dir / "nasa").mkdir(exist_ok=True)
        (download_dir / "mitre").mkdir(exist_ok=True)
        
        return download_dir
        
    @staticmethod
    def add_missing_parameters(handler_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add missing required parameters for handlers"""
        fixed_params = params.copy()
        
        if handler_name == "download_handler":
            if "output_dir" not in params:
                download_dir = SPARTAOptimizations.ensure_download_directory()
                fixed_params["output_dir"] = str(download_dir)
                
        elif handler_name == "mitre_handler":
            if "cache_dir" not in params:
                cache_dir = Path("/tmp/sparta_cache/mitre")
                cache_dir.mkdir(parents=True, exist_ok=True)
                fixed_params["cache_dir"] = str(cache_dir)
                
        return fixed_params


class ErrorRecoveryOptimizations:
    """Advanced error recovery and retry mechanisms"""
    
    @staticmethod
    def intelligent_retry(
        max_attempts: int = 3,
        backoff_base: float = 2.0,
        exceptions: tuple = (Exception,),
        on_retry: Optional[callable] = None
    ):
        """Intelligent retry decorator with exponential backoff"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        
                        if attempt == max_attempts - 1:
                            # Last attempt failed
                            raise
                            
                        # Calculate backoff
                        wait_time = backoff_base ** attempt
                        
                        # Call retry callback if provided
                        if on_retry:
                            on_retry(attempt + 1, e, wait_time)
                            
                        time.sleep(wait_time)
                        
                raise last_exception
                
            return wrapper
        return decorator
        
    @staticmethod
    def circuit_breaker(
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: type = Exception
    ):
        """Circuit breaker pattern for failing services"""
        def decorator(func):
            func._failures = 0
            func._last_failure_time = None
            func._circuit_open = False
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Check if circuit is open
                if func._circuit_open:
                    if time.time() - func._last_failure_time > recovery_timeout:
                        # Try to close circuit
                        func._circuit_open = False
                        func._failures = 0
                    else:
                        raise Exception(f"Circuit breaker open for {func.__name__}")
                        
                try:
                    result = func(*args, **kwargs)
                    # Success - reset failure count
                    func._failures = 0
                    return result
                    
                except expected_exception as e:
                    func._failures += 1
                    func._last_failure_time = time.time()
                    
                    if func._failures >= failure_threshold:
                        func._circuit_open = True
                        
                    raise
                    
            return wrapper
        return decorator
        
    @staticmethod
    def fallback_handler(primary_func: callable, fallback_func: callable):
        """Fallback to alternative implementation on failure"""
        def wrapper(*args, **kwargs):
            try:
                return primary_func(*args, **kwargs)
            except Exception as e:
                print(f"Primary failed ({e}), using fallback")
                return fallback_func(*args, **kwargs)
                
        return wrapper


class OptimizationValidator:
    """Validate that optimizations are working correctly"""
    
    def __init__(self):
        self.results = {
            "arangodb_fixes": {},
            "marker_status": {},
            "sparta_auth": {},
            "error_recovery": {}
        }
        
    def validate_arangodb_fixes(self) -> bool:
        """Validate ArangoDB optimizations"""
        print("\n🔧 Validating ArangoDB Fixes...")
        
        # Test URL fix
        test_urls = [
            ("localhost", "http://localhost:8529"),
            ("http://localhost:8529", "http://localhost:8529"),
            ("localhost:8529", "http://localhost:8529"),
            ("127.0.0.1:8529", "http://127.0.0.1:8529")
        ]
        
        url_fixes_ok = True
        for input_url, expected in test_urls:
            fixed = ArangoDBOptimizations.fix_connection_url(input_url)
            if fixed == expected:
                print(f"  ✅ URL fix: {input_url} → {fixed}")
            else:
                print(f"  ❌ URL fix failed: {input_url} → {fixed} (expected {expected})")
                url_fixes_ok = False
                
        self.results["arangodb_fixes"]["url_fix"] = url_fixes_ok
        
        # Test parameter fixes
        param_tests = [
            ("create_document", 
             {"collection": "test", "data": {"key": "value"}},
             {"collection_name": "test", "document": {"key": "value"}}),
            ("search",
             {"collection_name": "test", "query": "search term"},
             {"collection_hint": "test", "query": "search term"})
        ]
        
        param_fixes_ok = True
        for operation, input_params, expected in param_tests:
            fixed = ArangoDBOptimizations.fix_api_parameters(operation, input_params)
            if all(fixed.get(k) == v for k, v in expected.items()):
                print(f"  ✅ Param fix: {operation}")
            else:
                print(f"  ❌ Param fix failed: {operation}")
                param_fixes_ok = False
                
        self.results["arangodb_fixes"]["param_fix"] = param_fixes_ok
        
        return url_fixes_ok and param_fixes_ok
        
    def validate_marker_fallbacks(self) -> bool:
        """Validate Marker fallback mechanisms"""
        print("\n🔧 Validating Marker Fallbacks...")
        
        # Check dependencies
        deps = MarkerOptimizations.check_dependencies()
        print(f"  Dependencies: {deps}")
        self.results["marker_status"]["dependencies"] = deps
        
        # Test fallback converter
        converter = MarkerOptimizations.create_fallback_converter()
        if converter:
            print(f"  ✅ Fallback converter available: {converter.__name__}")
            self.results["marker_status"]["fallback_available"] = True
            return True
        else:
            print(f"  ❌ No fallback converter available")
            self.results["marker_status"]["fallback_available"] = False
            return False
            
    def validate_sparta_setup(self) -> bool:
        """Validate SPARTA setup optimizations"""
        print("\n🔧 Validating SPARTA Setup...")
        
        # Check authentication
        auth = SPARTAOptimizations.setup_api_authentication()
        print(f"  ✅ Auth config created for: {', '.join(auth.keys())}")
        self.results["sparta_auth"]["services"] = list(auth.keys())
        
        # Check directory creation
        download_dir = SPARTAOptimizations.ensure_download_directory()
        if download_dir.exists():
            subdirs = [d.name for d in download_dir.iterdir() if d.is_dir()]
            print(f"  ✅ Download directory created with subdirs: {subdirs}")
            self.results["sparta_auth"]["download_dir"] = str(download_dir)
            return True
        else:
            print(f"  ❌ Failed to create download directory")
            return False
            
    def validate_error_recovery(self) -> bool:
        """Validate error recovery mechanisms"""
        print("\n🔧 Validating Error Recovery...")
        
        # Test retry mechanism
        retry_count = 0
        
        def on_retry(attempt, error, wait_time):
            nonlocal retry_count
            retry_count = attempt
            
        @ErrorRecoveryOptimizations.intelligent_retry(
            max_attempts=3,
            on_retry=on_retry
        )
        def flaky_function():
            if retry_count < 2:
                raise ValueError("Simulated failure")
            return "success"
            
        try:
            result = flaky_function()
            if result == "success" and retry_count == 2:
                print(f"  ✅ Retry mechanism working (retried {retry_count} times)")
                self.results["error_recovery"]["retry"] = True
            else:
                print(f"  ❌ Retry mechanism issue")
                self.results["error_recovery"]["retry"] = False
        except:
            print(f"  ❌ Retry mechanism failed")
            self.results["error_recovery"]["retry"] = False
            
        # Test circuit breaker
        @ErrorRecoveryOptimizations.circuit_breaker(
            failure_threshold=2,
            recovery_timeout=1.0
        )
        def protected_function(should_fail=False):
            if should_fail:
                raise ValueError("Service failure")
            return "success"
            
        # Trigger circuit breaker
        for i in range(3):
            try:
                protected_function(should_fail=True)
            except:
                pass
                
        # Check if circuit is open
        try:
            protected_function(should_fail=False)
            print(f"  ❌ Circuit breaker not working")
            self.results["error_recovery"]["circuit_breaker"] = False
        except Exception as e:
            if "Circuit breaker open" in str(e):
                print(f"  ✅ Circuit breaker working")
                self.results["error_recovery"]["circuit_breaker"] = True
            else:
                print(f"  ❌ Circuit breaker error: {e}")
                self.results["error_recovery"]["circuit_breaker"] = False
                
        return all(self.results["error_recovery"].values())
        
    def generate_validation_report(self) -> str:
        """Generate optimization validation report"""
        report = "# GRANGER Optimization Validation Report\n\n"
        report += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # ArangoDB section
        report += "## ArangoDB Optimizations\n"
        for key, value in self.results["arangodb_fixes"].items():
            status = "✅ PASSED" if value else "❌ FAILED"
            report += f"- {key}: {status}\n"
            
        # Marker section
        report += "\n## Marker Fallbacks\n"
        if "dependencies" in self.results["marker_status"]:
            for dep, available in self.results["marker_status"]["dependencies"].items():
                status = "✅ Available" if available else "❌ Missing"
                report += f"- {dep}: {status}\n"
                
        # SPARTA section
        report += "\n## SPARTA Setup\n"
        if "services" in self.results["sparta_auth"]:
            report += f"- Auth configured for: {', '.join(self.results['sparta_auth']['services'])}\n"
        if "download_dir" in self.results["sparta_auth"]:
            report += f"- Download directory: {self.results['sparta_auth']['download_dir']}\n"
            
        # Error recovery section
        report += "\n## Error Recovery\n"
        for key, value in self.results["error_recovery"].items():
            status = "✅ Working" if value else "❌ Failed"
            report += f"- {key}: {status}\n"
            
        return report


if __name__ == "__main__":
    # Run validation
    validator = OptimizationValidator()
    
    print("🔍 GRANGER Module-Specific Optimizations Validation")
    print("="*60)
    
    # Run all validations
    arangodb_ok = validator.validate_arangodb_fixes()
    marker_ok = validator.validate_marker_fallbacks()
    sparta_ok = validator.validate_sparta_setup()
    recovery_ok = validator.validate_error_recovery()
    
    # Generate report
    report = validator.generate_validation_report()
    
    # Save report
    report_path = Path("optimization_validation_report.md")
    report_path.write_text(report)
    
    print(f"\n\n📄 Report saved to: {report_path}")
    
    # Overall result
    all_ok = all([arangodb_ok, marker_ok, sparta_ok, recovery_ok])
    
    print("\n" + "="*60)
    print(f"Overall Validation: {'✅ PASSED' if all_ok else '❌ FAILED'}")
    
    # Exit code
    exit(0 if all_ok else 1)