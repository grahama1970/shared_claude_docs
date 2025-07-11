
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Sample code with quantum-vulnerable cryptography for testing
"""

import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


class CryptoManager:
    """Manages cryptographic operations (quantum-vulnerable)"""
    
    def __init__(self):
        # RSA-2048 key generation (vulnerable to quantum attacks)
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,  # Should be migrated to quantum-safe
            backend=default_backend()
        )
        
        # ECDSA with P-256 curve (vulnerable)
        self.ecdsa_private_key = ec.generate_private_key(
            ec.SECP256R1(),  # P-256 curve
            backend=default_backend()
        )
        
        # DSA key generation (highly vulnerable)
        self.dsa_private_key = dsa.generate_private_key(
            key_size=2048,
            backend=default_backend()
        )
    
    def legacy_rsa_1024(self):
        """Legacy RSA with weak 1024-bit key"""
        # WARNING: RSA-1024 is critically weak!
        weak_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=1024,
            backend=default_backend()
        )
        return weak_key
    
    def setup_tls_ecdhe(self):
        """Setup ECDHE for TLS (needs quantum-safe replacement)"""
        # Elliptic Curve Diffie-Hellman Ephemeral
        private_key = ec.generate_private_key(
            ec.SECP384R1(),  # P-384 curve
            backend=default_backend()
        )
        return private_key


class AuthenticationService:
    """Handles authentication with vulnerable algorithms"""
    
    def __init__(self):
        # Initialize with RSA-4096 (still quantum-vulnerable)
        self.signing_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,  # Larger but still vulnerable
            backend=default_backend()
        )
    
    def generate_ecdsa_key_pair(self):
        """Generate ECDSA key pair for signatures"""
        # Using secp256k1 (Bitcoin curve) - quantum-vulnerable
        private_key = ec.generate_private_key(
            ec.SECP256K1(),
            backend=default_backend()
        )
        return private_key
    
    def setup_diffie_hellman(self):
        """Classic Diffie-Hellman setup (highly vulnerable)"""
        # Note: DH is particularly vulnerable to quantum attacks
        # Should migrate to CRYSTALS-Kyber or similar
        parameters = dsa.generate_parameters(
            key_size=2048,
            backend=default_backend()
        )
        return parameters


# Legacy code with various vulnerable patterns
def old_crypto_functions():
    """Collection of legacy cryptographic functions"""
    
    # OpenSSL-style RSA operations
    # RSAPublicKey and RSAPrivateKey usage
    print("Initializing RSA encryption...")
    
    # Java-style patterns
    # KeyPairGenerator.getInstance("RSA")
    # Cipher.getInstance("RSA/ECB/PKCS1Padding")
    
    # .NET patterns
    # RSACryptoServiceProvider with 2048 bits
    # ECDsaCng for elliptic curve operations
    
    pass


if __name__ == "__main__":
    print("Sample vulnerable cryptography code")
    print("This code contains quantum-vulnerable algorithms:")
    print("- RSA (various key sizes)")
    print("- ECDSA/ECDH (various curves)")
    print("- DSA")
    print("- Diffie-Hellman")
    print("\nRun the quantum-safe scanner to analyze vulnerabilities!")