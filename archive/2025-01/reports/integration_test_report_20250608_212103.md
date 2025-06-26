# Granger Ecosystem Integration Test Report

Date: 2025-06-08 21:21:03
Duration: 7.47 seconds

## Summary
- Total Tests: 7
- Passed: 4
- Failed: 3
- Success Rate: 57.1%

## Module Status
- ✅ ArangoDB
- ✅ GitGet
- ✅ LLM Call
- ✅ Marker
- ✅ RL Commons
- ✅ SPARTA
- ✅ Test Reporter
- ✅ World Model
- ✅ YouTube

## Test Results
| Test | Status | Details |
|------|--------|---------|
| sparta_cve_search | FAIL | No results |
| marker_pdf_conversion | PASS | Generated markdown |
| youtube_transcript | PASS | Found videos |
| rl_optimization | FAIL | 'ContextualBandit' object has no attribute 'process_request' |
| llm_call | PASS | Got response |
| test_reporter | PASS | Generated report |
| integration_flow | FAIL | ContextualBandit.__init__() missing 2 required positional arguments: 'actions' and 'context_features' |

## Conclusion
⚠️ **ECOSYSTEM PARTIALLY OPERATIONAL** - Some components need attention
