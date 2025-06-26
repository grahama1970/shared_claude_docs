# Knowledge Graph Merger

A Level 3 GRANGER task implementation that orchestrates merging of multiple knowledge graphs while resolving conflicts and maintaining consistency.

## Overview

The Knowledge Graph Merger provides sophisticated capabilities for:
- Loading graphs from multiple formats (NetworkX, RDF, JSON-LD)
- Identifying and resolving entity duplicates across graphs
- Handling conflicting information with configurable strategies
- Maintaining complete provenance tracking
- Validating merged graphs for consistency

## Features

### Multi-Format Support
- **NetworkX**: Native Python graph format
- **RDF**: Resource Description Framework graphs via rdflib
- **JSON-LD**: Linked Data format for structured data

### Conflict Resolution Strategies
- **Latest Wins**: Uses the most recent value based on timestamps
- **Confidence-Based**: Selects values with highest confidence scores
- **Consensus**: Chooses the most common value across sources
- **Manual**: Allows custom resolution logic

### Entity Resolution
- Automatic detection of similar entities across graphs
- Configurable similarity threshold
- Attribute-based matching
- Canonical ID mapping

### Provenance Tracking
- Complete source attribution for every entity
- Timestamp tracking
- Confidence scores
- Metadata preservation

## Usage

```python
from knowledge_graph_merger_interaction import KnowledgeGraphMerger, ConflictStrategy

# Initialize merger
merger = KnowledgeGraphMerger()

# Load graphs from different formats
g1 = merger.load_graph_from_format(networkx_graph, "networkx", "source1")
g2 = merger.load_graph_from_format(rdf_graph, "rdf", "source2")
g3 = merger.load_graph_from_format(jsonld_data, "json-ld", "source3")

# Merge with conflict resolution
graphs = [
    (g1, "source1", datetime.now()),
    (g2, "source2", datetime.now()),
    (g3, "source3", datetime.now())
]

merged = merger.merge_graphs(graphs, strategy=ConflictStrategy.CONFIDENCE_BASED)

# Validate result
validation = merger.validate_merged_graph(merged)
print(f"Valid: {validation['is_valid']}")

# Generate report
report = merger.generate_merge_report(merged)
```

## Test Suite

The implementation includes comprehensive tests:

| Test | Description | Expected Duration |
|------|-------------|-------------------|
| Basic Merge | Tests fundamental merging with conflicts | ~0.01s |
| RDF Conversion | Validates RDF to NetworkX conversion | ~0.01s |
| Entity Resolution | Tests entity deduplication | ~0.01s |
| Conflict Strategies | Validates all resolution strategies | ~0.01s |
| Graph Validation | Tests validation logic | ~0.01s |
| Large Scale Merge | Performance test with 1000+ nodes | ~5s |

## Implementation Details

### Key Classes

- **KnowledgeGraphMerger**: Main orchestration class
- **ConflictStrategy**: Enum for resolution strategies
- **EntityProvenance**: Tracks entity origins and metadata
- **MergeConflict**: Represents conflicts during merging

### Architecture

The merger follows a three-phase approach:
1. **Entity Resolution**: Identify similar entities across graphs
2. **Conflict Detection**: Find conflicting attributes
3. **Merge & Validate**: Create final graph with validation

### Performance Considerations

- Efficient entity matching using attribute hashing
- Batched conflict resolution
- Memory-efficient for large graphs
- Configurable validation depth

## Integration with Claude Module Ecosystem

This component integrates with:
- **ArangoDB**: For persistent graph storage
- **Marker**: For document-extracted knowledge graphs
- **SPARTA**: For cybersecurity knowledge graphs
- **Claude Module Communicator**: For inter-module coordination

## Dependencies

- networkx: Graph data structures and algorithms
- rdflib: RDF graph handling
- Python 3.9+: Type hints and dataclasses

## Future Enhancements

- [ ] Machine learning-based entity resolution
- [ ] Distributed graph merging
- [ ] Custom merge strategies via plugins
- [ ] Graph versioning support
- [ ] Real-time collaborative merging