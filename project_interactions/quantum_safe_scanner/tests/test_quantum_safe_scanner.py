"""
Test module for Task #021: Quantum-Safe Cryptography Scanner.

These tests validate GRANGER requirements for detecting quantum-vulnerable
cryptographic algorithms and providing migration recommendations.
"""

import pytest
import tempfile
import time
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, "/home/graham/workspace/shared_claude_docs/project_interactions/quantum_safe_scanner")

from quantum_safe_scanner_interaction import (
    QuantumSafeScanner,
    CryptoVulnerability,
    MigrationRecommendation,
    MigrationReport
)


class TestQuantumSafeScanner:
    """Test suite for Task #021: Quantum-Safe Cryptography Scanner."""
    
    @pytest.fixture
    def scanner(self):
        """Create a fresh scanner instance."""
        return QuantumSafeScanner()
    
    @pytest.fixture
    def test_code_files(self):
        """Create temporary files with crypto code."""
        files = []
        with tempfile.TemporaryDirectory() as tmpdir:
            # RSA example
            rsa_file = Path(tmpdir) / "rsa_example.py"
            rsa_file.write_text("""
import Crypto.PublicKey.RSA

def generate_rsa_key():
    key = RSA.generate(2048)
    return key

# Using RSA-2048 for encryption
rsa_key = generate_rsa_key()
""")
            files.append(rsa_file)
            
            # ECC example
            ecc_file = Path(tmpdir) / "ecc_crypto.js"
            ecc_file.write_text("""
const crypto = require('crypto');

// Using ECDSA with secp256k1
const ecdh = crypto.createECDH('secp256k1');
ecdh.generateKeys();

// P-256 elliptic curve operations
const sign = crypto.createSign('SHA256');
""")
            files.append(ecc_file)
            
            # Mixed crypto file
            mixed_file = Path(tmpdir) / "crypto_utils.java"
            mixed_file.write_text("""
import java.security.*;
import javax.crypto.Cipher;

public class CryptoUtils {
    // RSA encryption
    public static KeyPair generateRSAKeyPair() throws Exception {
        KeyPairGenerator gen = KeyPairGenerator.getInstance("RSA");
        gen.initialize(4096);
        return gen.generateKeyPair();
    }
    
    // ECDSA signature
    public static KeyPair generateECKeyPair() throws Exception {
        KeyPairGenerator gen = KeyPairGenerator.getInstance("EC");
        ECGenParameterSpec ecSpec = new ECGenParameterSpec("secp384r1");
        gen.initialize(ecSpec);
        return gen.generateKeyPair();
    }
    
    // Diffie-Hellman key exchange
    public static KeyPair generateDHKeyPair() throws Exception {
        KeyPairGenerator gen = KeyPairGenerator.getInstance("DH");
        gen.initialize(2048);
        return gen.generateKeyPair();
    }
}
""")
            files.append(mixed_file)
            
            yield tmpdir, files
    
    def test_scan_rsa_vulnerabilities(self, scanner, test_code_files):
        """
        Test 021.1: Detect RSA usage in codebase.
        Expected duration: 0.5s-2.0s
        """
        start_time = time.time()
        tmpdir, files = test_code_files
        
        # Scan directory
        vulnerabilities = scanner.scan_directory(tmpdir)
        
        duration = time.time() - start_time
        
        # Filter RSA vulnerabilities
        rsa_vulns = [v for v in vulnerabilities if v.algorithm == "RSA"]
        
        # Verify
        assert len(rsa_vulns) >= 2, f"Expected at least 2 RSA vulnerabilities, found {len(rsa_vulns)}"
        assert 0.5 <= duration <= 2.0, f"Duration {duration:.2f}s outside expected range"
        
        # Check vulnerability details
        for vuln in rsa_vulns:
            assert vuln.vulnerability_level in ["high", "medium", "low"]
            assert vuln.code_snippet != ""
            assert vuln.line_number > 0
        
        print(f"✓ Detected {len(rsa_vulns)} RSA vulnerabilities in {duration:.2f}s")
    
    def test_scan_ecc_vulnerabilities(self, scanner, test_code_files):
        """
        Test 021.2: Detect Elliptic Curve Cryptography usage.
        Expected duration: 0.5s-2.0s
        """
        start_time = time.time()
        tmpdir, files = test_code_files
        
        # Scan directory
        vulnerabilities = scanner.scan_directory(tmpdir)
        
        duration = time.time() - start_time
        
        # Filter ECC vulnerabilities
        ecc_vulns = [v for v in vulnerabilities if v.algorithm == "ECC"]
        
        # Verify
        assert len(ecc_vulns) >= 2, f"Expected at least 2 ECC vulnerabilities, found {len(ecc_vulns)}"
        assert 0.5 <= duration <= 2.0, f"Duration {duration:.2f}s outside expected range"
        
        # Check for specific curves
        curves_found = set()
        for vuln in ecc_vulns:
            if "secp256k1" in vuln.context:
                curves_found.add("secp256k1")
            if "secp384r1" in vuln.context or "P-384" in vuln.context:
                curves_found.add("P-384")
        
        assert len(curves_found) >= 1, "Should detect specific elliptic curves"
        
        print(f"✓ Detected {len(ecc_vulns)} ECC vulnerabilities in {duration:.2f}s")
    
    def test_migration_recommendations(self, scanner):
        """
        Test 021.3: Generate quantum-safe migration recommendations.
        Expected duration: 0.1s-1.0s
        """
        start_time = time.time()
        
        # Create test vulnerabilities
        vulnerabilities = [
            CryptoVulnerability(
                file_path="test.py",
                line_number=10,
                algorithm="RSA",
                key_size=2048,
                context="RSA.generate(2048)",
                vulnerability_level="high",
                code_snippet="key = RSA.generate(2048)"
            ),
            CryptoVulnerability(
                file_path="test.js",
                line_number=20,
                algorithm="ECC",
                key_size=256,
                context="secp256k1",
                vulnerability_level="high",
                code_snippet="crypto.createECDH('secp256k1')"
            ),
            CryptoVulnerability(
                file_path="test.java",
                line_number=30,
                algorithm="DH",
                key_size=2048,
                context="DH key exchange",
                vulnerability_level="medium",
                code_snippet="KeyPairGenerator.getInstance('DH')"
            )
        ]
        
        # Generate report
        report = scanner.generate_migration_report(vulnerabilities)
        
        duration = time.time() - start_time
        
        # Verify
        assert 0.1 <= duration <= 1.0, f"Duration {duration:.2f}s outside expected range"
        assert isinstance(report, MigrationReport)
        assert len(report.recommendations) > 0
        assert report.total_files_scanned > 0
        
        # Check recommendations
        alg_recommendations = {r.current_algorithm: r for r in report.recommendations}
        
        # RSA should recommend ML-KEM or similar
        assert "RSA" in alg_recommendations
        rsa_rec = alg_recommendations["RSA"]
        assert any("ML-KEM" in rec or "Kyber" in rec for rec in rsa_rec.recommended_algorithms)
        
        # ECC should recommend ML-DSA or similar
        assert "ECC" in alg_recommendations
        ecc_rec = alg_recommendations["ECC"]
        assert any("ML-DSA" in rec or "Dilithium" in rec for rec in ecc_rec.recommended_algorithms)
        
        print(f"✓ Generated migration recommendations in {duration:.2f}s")
    
    def test_vulnerability_classification(self, scanner):
        """
        Test 021.4: Classify vulnerabilities by severity.
        Expected duration: 0.1s-0.5s
        """
        start_time = time.time()
        
        # Test classification logic
        test_cases = [
            ("RSA", 1024, "high"),     # Small RSA key
            ("RSA", 2048, "medium"),    # Standard RSA key
            ("RSA", 4096, "low"),       # Large RSA key
            ("ECC", 256, "high"),       # Standard ECC
            ("DH", 2048, "medium"),     # DH exchange
        ]
        
        results = []
        for algo, key_size, expected_level in test_cases:
            level = scanner.classify_vulnerability(algo, key_size)
            results.append(level == expected_level)
        
        duration = time.time() - start_time
        
        # Verify
        assert 0.1 <= duration <= 0.5, f"Duration {duration:.2f}s outside expected range"
        assert all(results), "Vulnerability classification incorrect"
        
        print(f"✓ Vulnerability classification verified in {duration:.2f}s")
    
    def test_multi_language_support(self, scanner, test_code_files):
        """
        Test 021.5: Support for multiple programming languages.
        Expected duration: 0.5s-2.0s
        """
        start_time = time.time()
        tmpdir, files = test_code_files
        
        # Scan directory
        vulnerabilities = scanner.scan_directory(tmpdir)
        
        duration = time.time() - start_time
        
        # Check language coverage
        file_extensions = set()
        for vuln in vulnerabilities:
            ext = Path(vuln.file_path).suffix
            file_extensions.add(ext)
        
        # Verify
        assert 0.5 <= duration <= 2.0, f"Duration {duration:.2f}s outside expected range"
        assert ".py" in file_extensions, "Should support Python files"
        assert ".js" in file_extensions, "Should support JavaScript files"
        assert ".java" in file_extensions, "Should support Java files"
        
        print(f"✓ Multi-language support verified ({len(file_extensions)} languages) in {duration:.2f}s")
    
    def test_report_generation(self, scanner, test_code_files):
        """
        Test 021.6: Generate comprehensive migration report.
        Expected duration: 1.0s-3.0s
        """
        start_time = time.time()
        tmpdir, files = test_code_files
        
        # Scan and generate report
        vulnerabilities = scanner.scan_directory(tmpdir)
        report = scanner.generate_migration_report(vulnerabilities)
        
        # Save report
        report_path = Path(tmpdir) / "quantum_migration_report.json"
        scanner.save_report(report, str(report_path))
        
        duration = time.time() - start_time
        
        # Verify report structure
        assert 1.0 <= duration <= 3.0, f"Duration {duration:.2f}s outside expected range"
        assert report_path.exists(), "Report file not created"
        
        # Load and verify report content
        with open(report_path) as f:
            saved_report = json.load(f)
        
        assert "scan_timestamp" in saved_report
        assert "vulnerabilities" in saved_report
        assert "recommendations" in saved_report
        assert "summary_statistics" in saved_report
        assert saved_report["estimated_total_effort_hours"] > 0
        
        print(f"✓ Generated comprehensive report in {duration:.2f}s")


class TestHoneypot:
    """Honeypot tests for edge cases."""
    
    @pytest.fixture
    def scanner(self):
        """Create a fresh scanner instance."""
        return QuantumSafeScanner()
    
    def test_nist_pqc_algorithms(self, scanner):
        """
        Test 021.H: HONEYPOT - Verify NIST PQC algorithm knowledge.
        Expected duration: 0.1s-0.5s
        """
        start_time = time.time()
        
        # Check that scanner knows about NIST PQC algorithms
        nist_algorithms = scanner.get_nist_pqc_algorithms()
        
        duration = time.time() - start_time
        
        # Required algorithms
        required = ["ML-KEM", "ML-DSA", "SLH-DSA"]
        
        # Verify
        assert 0.1 <= duration <= 0.5, f"Duration {duration:.2f}s outside expected range"
        
        for algo in required:
            assert algo in nist_algorithms, f"Missing NIST PQC algorithm: {algo}"
        
        # Check categories
        assert "kem" in nist_algorithms, "Should have Key Encapsulation Mechanisms"
        assert "signature" in nist_algorithms, "Should have Digital Signature algorithms"
        
        print(f"✓ Honeypot passed: NIST PQC algorithms verified in {duration:.2f}s")