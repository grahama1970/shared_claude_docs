# Quantum-Safe Cryptography Migration Report

Generated: 2025-06-01T19:05:52.952759

## Executive Summary

- **Total Files Scanned**: 2
- **Total Vulnerabilities Found**: 98
- **Estimated Migration Effort**: 566 hours

## Vulnerability Summary

| Algorithm | Count | Risk Level |
|-----------|-------|------------|
| RSA | 40 | Medium |
| ECC | 28 | Medium |
| DH | 20 | High |
| DSA | 10 | High |

## Migration Recommendations

### RSA

**Recommended Alternatives**: CRYSTALS-Dilithium, FALCON, SPHINCS+
**Migration Effort**: high
**Estimated Hours**: 200
**NIST Security Level**: 3

**Implementation Notes**: For encryption, use CRYSTALS-Kyber or Classic McEliece

---

### ECC

**Recommended Alternatives**: CRYSTALS-Dilithium, FALCON, SPHINCS+
**Migration Effort**: high
**Estimated Hours**: 176
**NIST Security Level**: 3

**Implementation Notes**: For key exchange, use CRYSTALS-Kyber

---

### DH

**Recommended Alternatives**: CRYSTALS-Kyber, Classic McEliece, BIKE, HQC
**Migration Effort**: high
**Estimated Hours**: 140
**NIST Security Level**: 3

**Implementation Notes**: CRYSTALS-Kyber recommended for most use cases

---

### DSA

**Recommended Alternatives**: CRYSTALS-Dilithium, FALCON, SPHINCS+
**Migration Effort**: medium
**Estimated Hours**: 50
**NIST Security Level**: 3

**Implementation Notes**: CRYSTALS-Dilithium offers best performance

---


## Detailed Vulnerabilities

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 73
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
# RSA patterns
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 74
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'\bRSA\b': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 75
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'RSA-?\d{3,4}': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 76
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'rsaEncryption': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 77
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'RSAPrivateKey|RSAPublicKey': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 78
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'Crypto\.PublicKey\.RSA': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 79
**Algorithm**: RSA
**Key Size**: Unknown
**Vulnerability Level**: low

```
r'OpenSSL.*RSA': 'RSA',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 81
**Algorithm**: ECC
**Key Size**: Unknown
**Vulnerability Level**: medium

```
# Elliptic Curve patterns
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 82
**Algorithm**: ECC
**Key Size**: Unknown
**Vulnerability Level**: medium

```
r'\bECC\b|\bECDSA\b': 'ECC',
```

---

**File**: `quantum_safe_scanner_interaction.py`
**Line**: 83
**Algorithm**: ECC
**Key Size**: Unknown
**Vulnerability Level**: medium

```
r'elliptic.?curve': 'ECC',
```

---

