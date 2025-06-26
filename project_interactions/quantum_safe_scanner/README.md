# Quantum-Safe Cryptography Migration Scanner

A Level 1 implementation for GRANGER Task #21 that scans codebases for quantum-vulnerable cryptographic algorithms and provides migration recommendations to post-quantum cryptography (PQC) alternatives.

## Overview

This scanner identifies quantum-vulnerable cryptographic implementations across multiple programming languages and provides actionable migration recommendations based on NIST Post-Quantum Cryptography standards.

## Features

- **Multi-language Support**: Scans Python, Java, Go, C/C++, JavaScript, Ruby, PHP, Swift, Kotlin, Scala, TypeScript
- **Algorithm Detection**: Identifies RSA, ECC/ECDSA, Diffie-Hellman, and DSA implementations
- **Key Size Analysis**: Extracts key sizes to assess vulnerability levels
- **NIST PQC Recommendations**: Maps vulnerable algorithms to quantum-safe alternatives
- **Migration Planning**: Estimates effort and provides implementation guidance
- **Comprehensive Reporting**: Generates JSON and Markdown reports

## Detected Vulnerabilities

### Quantum-Vulnerable Algorithms
- **RSA**: All key sizes (especially < 3072 bits)
- **ECC/ECDSA**: All curves (P-256, P-384, P-521, secp256k1)
- **Diffie-Hellman**: Classic DH and ECDH variants
- **DSA**: Digital Signature Algorithm

### Recommended Quantum-Safe Alternatives

#### For Digital Signatures
- **CRYSTALS-Dilithium** (recommended for performance)
- **FALCON** (smaller signatures)
- **SPHINCS+** (hash-based, conservative choice)

#### For Key Exchange/Encryption
- **CRYSTALS-Kyber** (recommended for most use cases)
- **Classic McEliece** (conservative choice)
- **BIKE** (alternate lattice-based)
- **HQC** (code-based alternative)

## Usage

### Basic Scan
```python
from quantum_safe_scanner_interaction import QuantumSafeScanner

scanner = QuantumSafeScanner()
vulnerabilities = scanner.scan_directory("/path/to/codebase")
report = scanner.generate_migration_report(vulnerabilities)

# Export reports
scanner.export_report_json(report, "migration_report.json")
scanner.export_report_markdown(report, "migration_report.md")
```

### Demo Script
```bash
python demo_quantum_scan.py /path/to/scan
```

## Performance Characteristics

- **Small codebase** (< 10 files): ~3 seconds
- **Medium codebase** (20-50 files): ~8 seconds
- **Large codebase** (100+ files): Scales linearly

## Report Output

### Markdown Report Includes:
- Executive summary with total vulnerabilities
- Algorithm breakdown with risk levels
- Detailed migration recommendations
- Sample vulnerabilities with code snippets
- Estimated migration effort in hours

### JSON Report Includes:
- Machine-readable vulnerability data
- Structured recommendations
- Complete file and line information
- Migration effort estimates

## Migration Effort Estimation

Effort levels are calculated based on:
- **Low**: < 5 instances (8 base hours + 1-2 hours per instance)
- **Medium**: 5-20 instances (40 base hours + 1-2 hours per instance)
- **High**: 20+ instances (120 base hours + 1-2 hours per instance)

## Example Vulnerabilities

The scanner detects patterns like:
```python
# Python
from cryptography.hazmat.primitives.asymmetric import rsa
private_key = rsa.generate_private_key(key_size=2048)

# Java
KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
keyGen.initialize(1024);

# Go
privateKey, _ := rsa.GenerateKey(rand.Reader, 4096)

# OpenSSL patterns
DH *dh = DH_generate_parameters(1024, DH_GENERATOR_2, NULL, NULL);
```

## Implementation Notes

1. **Pattern Matching**: Uses regex patterns to identify cryptographic usage
2. **Context Extraction**: Captures surrounding code for better analysis
3. **Risk Assessment**: Evaluates vulnerability based on algorithm and key size
4. **Extensible Design**: Easy to add new patterns and algorithms

## Future Enhancements

- Integration with CI/CD pipelines
- Support for additional quantum-vulnerable algorithms
- Custom migration templates
- Automated code transformation suggestions
- Performance optimization for very large codebases

## References

- [NIST Post-Quantum Cryptography](https://www.nist.gov/pqcrypto)
- [CRYSTALS Suite](https://pq-crystals.org/)
- [Quantum Computing Threat Timeline](https://globalriskinsights.com/quantum-threat-timeline/)