# ArangoDB Handlers Test Report
Generated: 2025-06-03 21:51:51

## Summary
- Total Tests: 13
- Passed: 0
- Failed: 13

## Test Results

| Test Name | Description | Result | Status | Duration | Error |
|-----------|-------------|--------|--------|----------|-------|
| document_create | Create a new document | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Failed to connect to ArangoDB |
| search_bm25 | BM25 text search | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 1.00s | Failed to connect to ArangoDB |
| search_semantic | Semantic vector search | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 1.00s | Failed to connect to ArangoDB |
| search_hybrid | Hybrid search (BM25 + semantic) | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 1.00s | Failed to connect to ArangoDB |
| search_filtered | Search with filters | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 1.00s | Failed to connect to ArangoDB |
| memory_store | Store user message | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Memory agent not initialized |
| memory_store_agent | Store agent message | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Memory agent not initialized |
| memory_recall | Recall conversation history | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Memory agent not initialized |
| memory_search | Search across memories | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Memory agent not initialized |
| memory_context | Get relevant context | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Memory agent not initialized |
| paper_store | Store ArXiv paper | {'success': False, 'timestamp': '2025-06-04T01:51:... | ❌ Fail | 0.00s | Failed to connect to ArangoDB |
| batch_execute | Execute batch operations | {'success': True, 'timestamp': '2025-06-04T01:51:5... | ❌ Fail | 0.01s | - |
| batch_verify | Verify batch results | {'total_operations': 4, 'successful': 0, 'failed':... | ❌ Fail | 0.01s | - |
