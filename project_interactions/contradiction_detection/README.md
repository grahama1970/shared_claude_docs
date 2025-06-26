# Contradiction Detection Across Sources

## Overview

This module implements GRANGER Task #19, a Level 2 task that analyzes multiple information sources in parallel to detect contradictions and conflicts. It processes various source types including ArXiv papers, YouTube transcripts, documentation, technical specifications, and research blogs.

## Features

- **Multi-source Analysis**: Processes diverse information sources including:
  - ArXiv research papers
  - YouTube video transcripts
  - Technical documentation
  - Research blog posts
  - Technical specifications

- **Contradiction Detection**: Uses multiple strategies:
  - Pattern-based detection (negation, magnitude, temporal, factual)
  - Semantic keyword opposition analysis
  - Context-aware similarity matching
  - Confidence scoring based on source credibility

- **Severity Classification**:
  - **CRITICAL**: Fundamental disagreements on core facts
  - **MAJOR**: Significant conflicts affecting conclusions
  - **MODERATE**: Notable differences requiring attention
  - **MINOR**: Minor discrepancies, possibly contextual

- **Reconciliation Strategies**:
  - Temporal context (newer vs older information)
  - Domain-specific differences
  - Methodology differences
  - Consensus building
  - Expert review recommendations
  - Version updates

## Usage

```python
from contradiction_detection_interaction import ContradictionDetector

# Initialize detector
detector = ContradictionDetector()

# Load sources (or use mock sources for testing)
sources = detector.get_mock_sources()

# Detect contradictions
contradictions = detector.detect_contradictions(sources)

# Classify by severity
classified = detector.classify_contradictions(contradictions)

# Generate report
report = detector.generate_reconciliation_report(contradictions)
print(report)
```

## Performance Metrics

Based on test runs with 8 sources:
- Detection rate: ~64% of all source pairs
- Average detection time: <0.001s per comparison
- Total processing time: <0.02s for 28 comparisons
- Found 18 contradictions including 13 major/critical

## Test Results

All 9 unit tests pass successfully:
- Source loading and validation
- Contradiction detection accuracy
- Severity classification
- Reconciliation strategy assignment
- Temporal analysis
- Confidence calculation
- Report generation
- Performance benchmarks

## Example Output

```
=== Contradiction Detection System Test ===

Test 1: Loading mock sources...
✓ Loaded 8 sources in 0.00s

Test 2: Detecting contradictions...
✓ Found 18 contradictions in 0.02s

Test 3: Classifying contradictions by severity...
  MAJOR: 13 contradictions
  MODERATE: 5 contradictions

Test 4: Top Critical/Major Contradictions:
- Quantum computing threats: "will break RSA" vs "RSA remains secure"
- AI safety timeline: "existential threat" vs "decades away"
- Satellite security: "inherently secure" vs "vulnerable to attacks"
- ML robustness: "extremely robust" vs "highly vulnerable"
```

## Integration Points

This module can be integrated with:
- **ArXiv MCP Server**: For research paper analysis
- **YouTube Transcripts**: For video content analysis
- **Marker**: For PDF document processing
- **ArangoDB**: For storing contradiction relationships
- **Claude Module Communicator**: For orchestrating multi-source analysis

## Future Enhancements

1. **Real-time Monitoring**: Detect contradictions as new sources are added
2. **Graph Visualization**: Show contradiction networks
3. **Machine Learning**: Train models to improve detection accuracy
4. **Source Clustering**: Group sources by viewpoint
5. **Automated Resolution**: Suggest content edits to resolve contradictions