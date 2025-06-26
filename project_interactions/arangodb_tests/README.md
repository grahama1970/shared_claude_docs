# ArangoDB Level 0 Tests

This directory contains comprehensive Level 0 tests for the ArangoDB module as part of the GRANGER Phase 2 implementation.

## Overview

These tests verify single-module functionality of ArangoDB with real database operations, measuring actual response times and validating all core capabilities.

## Test Files

1. **test_query.py** - Tests AQL query execution
   - Simple queries (0.01-1.0s expected)
   - Filtered queries with bind variables
   - Aggregation queries
   - Sorting and limiting
   - Join-like operations
   - Complex multi-operation queries

2. **test_insert.py** - Tests document insertion
   - Single document insert (0.01-0.5s expected)
   - Bulk insert operations
   - Custom key handling
   - Complex nested documents
   - Schema validation
   - Edge document creation

3. **test_create_graph.py** - Tests graph creation
   - Simple graph creation (0.01-1.0s expected)
   - Complex graphs with multiple edge types
   - Knowledge graph patterns
   - Social network graphs
   - Orphan collections
   - Graph modifications

4. **test_traverse.py** - Tests graph traversal
   - Simple traversals (0.01-0.5s expected)
   - Multi-depth traversals
   - Filtered traversals
   - Shortest path algorithms
   - K-shortest paths
   - Bidirectional traversals
   - Pruning and aggregations

5. **test_honeypot.py** - Tests error handling
   - Nonexistent collections
   - Invalid AQL syntax
   - Invalid documents
   - Permission checks
   - Transaction rollback
   - Concurrent operations

## Prerequisites

1. **ArangoDB Installation**
   ```bash
   # Using Docker (recommended)
   docker run -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb:latest
   
   # Or install locally
   # See: https://www.arangodb.com/download/
   ```

2. **Python Dependencies**
   ```bash
   pip install python-arango pytest
   ```

## Running Tests

### Run All Tests
```bash
python run_all_tests.py
```

### Run Individual Test Files
```bash
pytest test_query.py -v
pytest test_insert.py -v
pytest test_create_graph.py -v
pytest test_traverse.py -v
pytest test_honeypot.py -v
```

### Run Specific Test
```bash
pytest test_query.py::TestArangoDBQuery::test_simple_query -v
```

## Expected Response Times

| Operation | Min Time | Max Time | Notes |
|-----------|----------|----------|-------|
| Simple Query | 0.01s | 1.0s | Basic FOR...RETURN |
| Complex Query | 0.01s | 2.0s | Joins, aggregations |
| Single Insert | 0.01s | 0.5s | One document |
| Bulk Insert | 0.01s | 2.0s | 100+ documents |
| Graph Creation | 0.01s | 2.0s | With edge definitions |
| Traversal | 0.01s | 1.0s | Depth 1-3 typical |
| Shortest Path | 0.01s | 1.0s | Between two vertices |

## Test Structure

Each test file follows this pattern:

1. **Setup**: Connect to ArangoDB, create test database
2. **Test Methods**: Individual test cases with timing
3. **Verification**: Check results and response times
4. **Teardown**: Clean up (optional, keeps data for other tests)

## Output

The test suite generates:
- Console output with timing information
- Markdown report: `reports/arangodb_level0_report_TIMESTAMP.md`
- JSON report: `reports/arangodb_level0_results_TIMESTAMP.json`

## Integration with GRANGER

These tests fulfill Phase 2 Task #003 requirements:
- ✅ Real database connections (no mocking)
- ✅ Measured response times (0.1s-1.0s typical)
- ✅ All four core actions tested (query, insert, create_graph, traverse)
- ✅ Honeypot tests for error handling
- ✅ Performance metrics collected

## Next Steps

After these Level 0 tests pass:
1. Task #004: Create Level 1 Pipeline Test (ArXiv → Marker)
2. Task #005: Create Level 1 Pipeline Test (Marker → ArangoDB)
3. Task #008: Implement Real ArangoDB Handlers in claude-module-communicator

## Troubleshooting

### Connection Refused
- Ensure ArangoDB is running on localhost:8529
- Check firewall settings
- Verify no authentication is required (or update credentials)

### Tests Fail
- Check ArangoDB version (3.10+ recommended)
- Ensure test database can be created
- Review error messages for specific issues

### Performance Issues
- Check ArangoDB configuration
- Ensure sufficient system resources
- Consider using SSD for database storage