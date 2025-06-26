"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

"""
Test suite for Quantum-Safe Cryptography Migration Scanner.

Tests the scanner's ability to identify quantum-vulnerable cryptographic
implementations and recommend migration paths to quantum-safe alternatives.

External Dependencies:
- pytest: https://docs.pytest.org/
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import time
from typing import List, Dict, Any
import pytest

from quantum_scanner import QuantumSafeScanner


class TestQuantumSafeScanner:
    """Test suite for quantum-safe cryptography migration scanner."""
    
    def setup_method(self):
        """Set up test instance before each test."""
        self.scanner = QuantumSafeScanner()
    
    def test_scan_codebase(self):
        """Test codebase scanning for quantum-vulnerable cryptography."""
        start_time = time.time()
        
        # Test with sample codebase containing vulnerable crypto
        test_code = {
            "crypto_utils.py": '''
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Vulnerable: RSA-2048 susceptible to Shor's algorithm
def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()

# Vulnerable: SHA-256 weakened by Grover's algorithm
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Vulnerable: ECDSA susceptible to quantum attacks
def sign_message(message: bytes, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
''',
            "tls_config.py": '''
# TLS configuration using quantum-vulnerable ciphers
TLS_CIPHERS = [
    "ECDHE-RSA-AES256-GCM-SHA384",  # Vulnerable: ECDHE
    "DHE-RSA-AES256-GCM-SHA384",    # Vulnerable: DHE
    "RSA-AES256-GCM-SHA384"          # Vulnerable: RSA
]

def configure_tls():
    return {
        "ciphers": TLS_CIPHERS,
        "min_version": "TLSv1.2",
        "key_exchange": "ECDHE"  # Vulnerable
    }
'''
        }
        
        results = self.scanner.scan_codebase(test_code)
        
        # Verify scan results
        assert isinstance(results, dict)
        assert "vulnerabilities" in results
        assert "summary" in results
        assert "risk_score" in results
        
        # Check vulnerability detection
        vulns = results["vulnerabilities"]
        assert len(vulns) >= 5  # Should detect multiple issues
        
        # Verify RSA vulnerability detected
        rsa_vuln = next((v for v in vulns if v["algorithm"] == "RSA-2048"), None)
        assert rsa_vuln is not None
        assert rsa_vuln["vulnerability"] == "Shor's algorithm"
        assert rsa_vuln["risk"] == "high"
        assert "Kyber" in rsa_vuln["recommendation"]
        
        # Verify SHA-256 vulnerability detected
        sha_vuln = next((v for v in vulns if v["algorithm"] == "SHA-256"), None)
        assert sha_vuln is not None
        assert sha_vuln["vulnerability"] == "Grover's algorithm"
        assert sha_vuln["risk"] == "medium"
        assert "SHA-384" in sha_vuln["recommendation"]
        
        # Verify TLS cipher vulnerabilities
        tls_vulns = [v for v in vulns if "TLS" in v.get("context", "")]
        assert len(tls_vulns) >= 3
        
        # Check risk score calculation
        assert 0 <= results["risk_score"] <= 10
        assert results["risk_score"] >= 7  # High risk due to multiple vulnerabilities
        
        # Verify summary statistics
        summary = results["summary"]
        assert summary["total_files"] == 2
        assert summary["vulnerable_files"] == 2
        assert summary["high_risk_count"] >= 3
        assert summary["medium_risk_count"] >= 2
        
        # Performance check
        duration = time.time() - start_time
        assert duration < 2.0  # Should scan quickly
    
    def test_generate_migration_plan(self):
        """Test migration plan generation for quantum-safe transition."""
        start_time = time.time()
        
        # Scan results from previous test
        vulnerabilities = [
            {
                "file": "crypto_utils.py",
                "line": 8,
                "algorithm": "RSA-2048",
                "vulnerability": "Shor's algorithm",
                "risk": "high",
                "recommendation": "Migrate to Kyber or Dilithium"
            },
            {
                "file": "crypto_utils.py",
                "line": 15,
                "algorithm": "SHA-256",
                "vulnerability": "Grover's algorithm",
                "risk": "medium",
                "recommendation": "Use SHA-384 or SHA3-256"
            },
            {
                "file": "tls_config.py",
                "line": 3,
                "algorithm": "ECDHE",
                "vulnerability": "Quantum-vulnerable key exchange",
                "risk": "high",
                "recommendation": "Use Kyber or NTRU"
            }
        ]
        
        scan_results = {
            "vulnerabilities": vulnerabilities,
            "risk_score": 8.2,
            "summary": {
                "total_files": 2,
                "vulnerable_files": 2,
                "high_risk_count": 2,
                "medium_risk_count": 1
            }
        }
        
        plan = self.scanner.generate_migration_plan(scan_results)
        
        # Verify plan structure
        assert isinstance(plan, dict)
        assert "phases" in plan
        assert "timeline" in plan
        assert "dependencies" in plan
        assert "testing_strategy" in plan
        assert "rollback_plan" in plan
        
        # Check migration phases
        phases = plan["phases"]
        assert len(phases) >= 3
        
        # Phase 1: Critical infrastructure
        phase1 = phases[0]
        assert phase1["name"] == "Critical Infrastructure"
        assert phase1["priority"] == "critical"
        assert len(phase1["tasks"]) >= 2  # RSA and ECDHE migrations
        
        # Verify task details
        rsa_task = next((t for t in phase1["tasks"] if "RSA" in t["description"]), None)
        assert rsa_task is not None
        assert rsa_task["algorithm_from"] == "RSA-2048"
        assert rsa_task["algorithm_to"] in ["Kyber", "Dilithium"]
        assert "example" in rsa_task
        assert rsa_task["estimated_effort"] in ["high", "medium"]
        
        # Phase 2: Hash functions
        phase2 = phases[1]
        assert phase2["name"] == "Hash Function Upgrades"
        assert phase2["priority"] == "high"
        
        # Check dependencies
        deps = plan["dependencies"]
        assert "libraries" in deps
        assert any("pqcrypto" in lib for lib in deps["libraries"])
        assert "infrastructure" in deps
        
        # Verify testing strategy
        testing = plan["testing_strategy"]
        assert "unit_tests" in testing
        assert "integration_tests" in testing
        assert "performance_benchmarks" in testing
        assert "compatibility_tests" in testing
        
        # Check rollback plan
        rollback = plan["rollback_plan"]
        assert "triggers" in rollback
        assert "procedures" in rollback
        assert len(rollback["procedures"]) >= 3
        
        # Verify timeline
        timeline = plan["timeline"]
        assert "total_duration" in timeline
        assert timeline["total_duration"].endswith("months")
        assert "milestones" in timeline
        assert len(timeline["milestones"]) >= 3
        
        # Performance check
        duration = time.time() - start_time
        assert duration < 1.0  # Should generate quickly
    
    def test_validate_quantum_safe(self):
        """Test validation of quantum-safe implementations."""
        start_time = time.time()
        
        # Test quantum-safe codebase
        safe_code = {
            "quantum_crypto.py": '''
from pqcrypto.kem import kyber1024
from pqcrypto.sign import dilithium3
from hashlib import sha3_512

# Quantum-safe: Kyber for key encapsulation
def generate_kyber_keypair():
    public_key, secret_key = kyber1024.generate_keypair()
    return public_key, secret_key

# Quantum-safe: SHA3-512 resistant to Grover
def hash_data(data: bytes) -> bytes:
    return sha3_512(data).digest()

# Quantum-safe: Dilithium for signatures
def sign_document(document: bytes, secret_key):
    signature = dilithium3.sign(secret_key, document)
    return signature
''',
            "quantum_tls.py": '''
# Quantum-safe TLS configuration
QUANTUM_SAFE_CIPHERS = [
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256"
]

QUANTUM_SAFE_GROUPS = [
    "kyber1024",
    "ntru_hps4096821",
    "X25519Kyber768Draft00"
]

def configure_quantum_safe_tls():
    return {
        "ciphers": QUANTUM_SAFE_CIPHERS,
        "groups": QUANTUM_SAFE_GROUPS,
        "min_version": "TLSv1.3"
    }
'''
        }
        
        validation = self.scanner.validate_quantum_safe(safe_code)
        
        # Verify validation results
        assert isinstance(validation, dict)
        assert validation["is_quantum_safe"] is True
        assert validation["confidence"] >= 0.95
        assert "algorithms_used" in validation
        assert "compliance" in validation
        assert "recommendations" in validation
        
        # Check algorithm detection
        algorithms = validation["algorithms_used"]
        assert any(a["name"] == "Kyber-1024" for a in algorithms)
        assert any(a["name"] == "Dilithium3" for a in algorithms)
        assert any(a["name"] == "SHA3-512" for a in algorithms)
        
        # Verify all detected algorithms are quantum-safe
        for algo in algorithms:
            assert algo["quantum_safe"] is True
            assert algo["nist_approved"] is True
        
        # Check compliance status
        compliance = validation["compliance"]
        assert compliance["nist_pqc"] is True
        assert compliance["fips_203"] is True  # Kyber standard
        assert compliance["fips_204"] is True  # Dilithium standard
        
        # Test mixed implementation (partial quantum-safe)
        mixed_code = {
            **safe_code,
            "legacy_crypto.py": '''
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa

# Still using RSA
def generate_keys():
    return rsa.generate_private_key(65537, 2048)

# Still using SHA-256
def hash_value(value: str):
    return hashlib.sha256(value.encode()).hexdigest()
'''
        }
        
        mixed_validation = self.scanner.validate_quantum_safe(mixed_code)
        
        # Should not be fully quantum-safe
        assert mixed_validation["is_quantum_safe"] is False
        assert mixed_validation["confidence"] < 0.5
        assert len(mixed_validation["vulnerabilities"]) >= 2
        
        # Check partial compliance
        assert mixed_validation["coverage"]["quantum_safe_files"] == 2
        assert mixed_validation["coverage"]["total_files"] == 3
        assert mixed_validation["coverage"]["percentage"] < 70
        
        # Performance check
        duration = time.time() - start_time
        assert duration < 1.5  # Should validate quickly
    
    def test_honeypot_detection(self):
        """Test detection of honeypot patterns in cryptographic code."""
        # Honeypot code with suspicious patterns
        honeypot_code = {
            "crypto_honeypot.py": '''
# Suspicious: Weak RSA with known vulnerable primes
def generate_weak_rsa():
    # HONEYPOT: Using small primes
    p = 65537  # Too small!
    q = 65539  # Too small!
    n = p * q
    return n

# Suspicious: Predictable random values
import random
random.seed(42)  # HONEYPOT: Fixed seed

def generate_key():
    # HONEYPOT: Predictable randomness
    return random.randint(0, 2**256)

# Suspicious: Backdoored elliptic curve
def use_dual_ec_drbg():
    # HONEYPOT: Known NSA backdoor
    return "Dual_EC_DRBG"
'''
        }
        
        results = self.scanner.scan_codebase(honeypot_code)
        
        # Should detect honeypot patterns
        assert "honeypot_indicators" in results
        indicators = results["honeypot_indicators"]
        assert len(indicators) >= 3
        
        # Check specific honeypot detections
        assert any("small primes" in i["description"].lower() for i in indicators)
        assert any("fixed seed" in i["description"].lower() for i in indicators)
        assert any("dual_ec_drbg" in i["description"].lower() for i in indicators)
        
        # Risk score should be maximum
        assert results["risk_score"] >= 9.5
        assert results["summary"]["honeypot_risk"] == "critical"


@pytest.fixture
def sample_vulnerable_project():
    """Fixture providing a sample project with quantum-vulnerable crypto."""
    return {
        "src/auth.py": '''
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import jwt

class AuthService:
    def __init__(self):
        self.private_key = rsa.generate_private_key(65537, 2048)
        self.public_key = self.private_key.public_key()
    
    def create_token(self, user_id: str) -> str:
        # Vulnerable: RSA signatures
        return jwt.encode(
            {"user_id": user_id},
            self.private_key,
            algorithm="RS256"
        )
''',
        "src/encryption.py": '''
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def encrypt_data(data: bytes, password: str) -> bytes:
    # Vulnerable: PBKDF2 with SHA-256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(16),
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    
    # AES is quantum-safe
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(os.urandom(12))
    )
    return cipher.encryptor().update(data)
''',
        "src/certificates.py": '''
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

def create_certificate():
    # Vulnerable: ECDSA signatures
    private_key = ec.generate_private_key(ec.SECP256R1())
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(private_key, hashes.SHA256())
    
    return cert
'''
    }


def test_end_to_end_migration(sample_vulnerable_project):
    """Test complete migration workflow from scan to validation."""
    scanner = QuantumSafeScanner()
    
    # Step 1: Scan the vulnerable project
    scan_results = scanner.scan_codebase(sample_vulnerable_project)
    assert scan_results["risk_score"] >= 7.0
    assert len(scan_results["vulnerabilities"]) >= 4
    
    # Step 2: Generate migration plan
    plan = scanner.generate_migration_plan(scan_results)
    assert len(plan["phases"]) >= 2
    assert plan["timeline"]["total_duration"] == "6-9 months"
    
    # Step 3: Apply migrations (simulated)
    migrated_code = {
        "src/auth.py": '''
from pqcrypto.sign import dilithium3
import jwt

class AuthService:
    def __init__(self):
        self.public_key, self.secret_key = dilithium3.generate_keypair()
    
    def create_token(self, user_id: str) -> str:
        # Quantum-safe: Dilithium signatures
        return jwt.encode(
            {"user_id": user_id},
            self.secret_key,
            algorithm="Dilithium3"
        )
''',
        "src/encryption.py": '''
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def encrypt_data(data: bytes, password: str) -> bytes:
    # Quantum-safe: SHA3-512
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=32,
        salt=os.urandom(16),
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    
    # AES is quantum-safe
    cipher = Cipher(
        algorithms.AES(key),
        modes.GCM(os.urandom(12))
    )
    return cipher.encryptor().update(data)
''',
        "src/certificates.py": '''
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from pqcrypto.sign import dilithium3

def create_certificate():
    # Quantum-safe: Dilithium signatures
    public_key, secret_key = dilithium3.generate_keypair()
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])
    
    # Note: Real implementation would need quantum-safe x509
    # This is a simplified example
    cert_data = {
        "subject": subject,
        "issuer": issuer,
        "public_key": public_key,
        "serial": x509.random_serial_number(),
        "valid_from": datetime.utcnow(),
        "valid_to": datetime.utcnow() + timedelta(days=365)
    }
    
    # Sign with Dilithium
    signature = dilithium3.sign(secret_key, str(cert_data).encode())
    
    return cert_data, signature
'''
    }
    
    # Step 4: Validate the migrated code
    validation = scanner.validate_quantum_safe(migrated_code)
    assert validation["is_quantum_safe"] is True
    assert validation["confidence"] >= 0.95
    assert validation["compliance"]["nist_pqc"] is True


if __name__ == "__main__":
    # Run basic validation
    scanner = QuantumSafeScanner()
    
    # Test vulnerable code detection
    test_code = {
        "vulnerable.py": '''
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa

def insecure_crypto():
    private_key = rsa.generate_private_key(65537, 2048)
    hash_value = hashlib.sha256(b"data").hexdigest()
    return private_key, hash_value
'''
    }
    
    results = scanner.scan_codebase(test_code)
    print(f"✅ Detected {len(results['vulnerabilities'])} vulnerabilities")
    print(f"✅ Risk score: {results['risk_score']}/10")
    
    # Test migration plan
    plan = scanner.generate_migration_plan(results)
    print(f"✅ Generated {len(plan['phases'])}-phase migration plan")
    print(f"✅ Timeline: {plan['timeline']['total_duration']}")
    
    print("\n✅ Quantum-Safe Scanner validation passed")