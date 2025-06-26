# Granger Ecosystem Integration Test Report

Date: 2025-06-08 20:55:41
Duration: 5.13 seconds

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
| sparta_cve_search | FAIL | 'SPARTAModule' object has no attribute 'handle' |
| marker_pdf_conversion | PASS | Generated markdown |
| youtube_transcript | PASS | Found videos |
| rl_optimization | FAIL | 'ContextualBandit' object has no attribute 'process_request' |
| llm_call | PASS | Got response |
| test_reporter | PASS | Generated report |
| integration_flow | FAIL | 'SPARTAModule' object has no attribute 'handle' |

## Conclusion
⚠️ **ECOSYSTEM PARTIALLY OPERATIONAL** - Some components need attention
