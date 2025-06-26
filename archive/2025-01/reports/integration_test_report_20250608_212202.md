# Granger Ecosystem Integration Test Report

Date: 2025-06-08 21:22:02
Duration: 8.04 seconds

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
- ❌ RL Commons
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
| rl_optimization | FAIL | name 'ContextualBandit' is not defined |
| llm_call | PASS | Got response |
| test_reporter | PASS | Generated report |
| integration_flow | FAIL | name 'ContextualBandit' is not defined |

## Conclusion
⚠️ **ECOSYSTEM PARTIALLY OPERATIONAL** - Some components need attention
