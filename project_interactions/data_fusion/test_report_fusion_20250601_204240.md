# Multi-Modal Data Fusion Test Report
Generated: 2025-06-01 20:42:40

## Test Results

| Test Name | Description | Result | Status | Duration | Error |
|-----------|-------------|---------|---------|-----------|--------|
| test_text_only_fusion | Fusion with text modality only | Embedding shape: (768,) | ✅ Pass | 8.15s |  |
| test_multi_modal_fusion | Fusion with text, image, and structured data | Failed | ❌ Fail | 0.78s | The truth value of an array with more than one element is ambiguous. Use a.any() or a.all() |
| test_missing_modality_handling | Graceful handling of missing modalities | Failed | ❌ Fail | 0.69s | The truth value of an array with more than one element is ambiguous. Use a.any() or a.all() |
| test_tabular_data_fusion | Fusion with tabular/dataframe data | Fused 2 modalities | ✅ Pass | 0.80s |  |
| test_embedding_similarity | Similarity computation between embeddings | Matrix shape: (3, 3) | ✅ Pass | 1.34s |  |

## Summary
- Total Tests: 5
- Passed: 3
- Failed: 2
