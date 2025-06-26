# GRANGER Unique Scenarios Catalog

## Overview

This document catalogs all unique scenarios found across:
- `/home/graham/workspace/experiments/granger_hub/scenarios/`
- `/home/graham/workspace/shared_claude_docs/project_interactions/level_*_tests/`
- `GRANGER_BUG_HUNTER_SCENARIOS.md`

## Scenario Summary Table

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|

## Level 0 Scenarios (Single Module Tests)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| SPARTA CVE Search | 0 | SPARTA | Test basic CVE search functionality with various keywords | level_0_tests/test_01 | ✅ Yes (Module Resilience Testing) |
| ArXiv Paper Search | 0 | ArXiv | Test paper search and metadata retrieval | level_0_tests/test_02 | ✅ Yes (API Contract Violation Hunter) |
| ArangoDB Storage | 0 | ArangoDB | Test document storage and retrieval operations | level_0_tests/test_03 | ✅ Yes (Connection handling bugs) |
| YouTube Transcript Download | 0 | YouTube | Test transcript extraction from videos | level_0_tests/test_04 | ❌ No |
| Marker PDF Conversion | 0 | Marker | Test PDF to text/markdown conversion | level_0_tests/test_05 | ✅ Yes (Message Format Mismatch) |
| LLM Call Routing | 0 | LLM Call | Test LLM provider selection and routing | level_0_tests/test_06 | ❌ No |
| GitGet Repo Analysis | 0 | GitGet | Test repository analysis and metadata extraction | level_0_tests/test_07 | ✅ Yes (Malformed URLs) |
| World Model State Tracking | 0 | World Model | Test state tracking and prediction | level_0_tests/test_08 | ❌ No |
| RL Commons Decision | 0 | RL Commons | Test reinforcement learning decision making | level_0_tests/test_09 | ✅ Yes (Self-Optimization Hunter) |
| Test Reporter Generation | 0 | Test Reporter | Test report generation functionality | level_0_tests/test_10 | ❌ No |

## Level 1 Scenarios (Binary Module Interactions)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| ArXiv to Marker Pipeline | 1 | ArXiv, Marker | Download papers and extract content | level_1_tests/test_11 | ✅ Yes (Message Format Mismatch) |
| YouTube to SPARTA Pipeline | 1 | YouTube, SPARTA | Extract security topics from videos | level_1_tests/test_12 | ❌ No |
| Marker to ArangoDB Pipeline | 1 | Marker, ArangoDB | Store extracted documents in graph DB | level_1_tests/test_13 | ✅ Yes (Data size limits) |
| ArangoDB to Unsloth Pipeline | 1 | ArangoDB, Unsloth | Feed data for model training | level_1_tests/test_14 | ❌ No |
| GitGet to ArangoDB Pipeline | 1 | GitGet, ArangoDB | Store repository metadata in graph | level_1_tests/test_15 | ❌ No |
| World Model RL Pipeline | 1 | World Model, RL Commons | Predictive optimization | level_1_tests/test_16 | ❌ No |
| SPARTA to ArangoDB Pipeline | 1 | SPARTA, ArangoDB | Store CVE/security data in graph | level_1_tests/test_17 | ❌ No |
| LLM Call to Test Reporter | 1 | LLM Call, Test Reporter | Generate test reports from LLM | level_1_tests/test_18 | ❌ No |
| Granger Hub Coordination | 1 | Granger Hub, Various | Hub message routing and coordination | level_1_tests/test_19 | ❌ No |
| Unsloth to LLM Call Pipeline | 1 | Unsloth, LLM Call | Use fine-tuned models in LLM calls | level_1_tests/test_20 | ❌ No |

## Level 2 Scenarios (Pipeline/Workflow Tests)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| Research to Training Workflow | 2 | ArXiv, Marker, ArangoDB, Unsloth | Complete research paper processing pipeline | level_2_tests/test_21 | ✅ Yes (State Corruption Hunter) |
| Security Monitoring System | 2 | SPARTA, ArangoDB, Test Reporter | Real-time security threat monitoring | level_2_tests/test_22 | ❌ No |
| Knowledge Graph Builder | 2 | Multiple sources → ArangoDB | Build comprehensive knowledge graphs | level_2_tests/test_23 | ❌ No |
| Adaptive Learning System | 2 | RL Commons, World Model, Multiple | Self-improving system with feedback loops | level_2_tests/test_24 | ✅ Yes (RL optimization bugs) |
| Real Time Collaboration | 2 | Granger Hub, Multiple modules | Multi-agent collaboration patterns | level_2_tests/test_25 | ❌ No |
| LLM Fallback Chain | 2 | LLM Call, Multiple providers | Provider failover and load balancing | level_2_tests/test_26 | ✅ Yes (Timeout and Retry) |
| RL Multi-Armed Bandit | 2 | RL Commons, Multiple | Optimization across multiple options | level_2_tests/test_27 | ❌ No |
| World Model Prediction | 2 | World Model, Multiple | Predictive analytics pipeline | level_2_tests/test_28 | ❌ No |
| Test Reporter Aggregation | 2 | Test Reporter, Multiple sources | Aggregate test results across modules | level_2_tests/test_29 | ❌ No |
| Granger Hub Broadcast | 2 | Granger Hub, All modules | Broadcast messaging patterns | level_2_tests/test_30 | ❌ No |

## Level 3 Scenarios (Ecosystem-Wide Tests)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| Full Research Pipeline | 3 | All research modules | End-to-end research automation | level_3_tests/test_31 | ✅ Yes (State Corruption) |
| YouTube Research Flow | 3 | YouTube, ArXiv, GitGet, ArangoDB | Extract research from video content | level_3_tests/test_32 | ❌ No |
| Security Analysis Workflow | 3 | SPARTA, Multiple analysis modules | Comprehensive security assessment | level_3_tests/test_33 | ✅ Yes (Cross-Module Security) |
| Autonomous Learning Loop | 3 | RL, World Model, All modules | Self-directed learning system | level_3_tests/test_34 | ✅ Yes (Self-Optimization) |
| Multi-Agent Collaboration | 3 | Granger Hub, Multiple agents | Complex multi-agent scenarios | level_3_tests/test_35 | ✅ Yes (Emergent Behavior) |
| Cross-Domain Synthesis | 3 | All content modules | Synthesize knowledge across domains | level_3_tests/test_36 | ❌ No |
| Real-Time Monitoring | 3 | All monitoring modules | System-wide monitoring and alerting | level_3_tests/test_37 | ✅ Yes (Resource Contention) |
| Adaptive Optimization | 3 | RL, All modules | System-wide performance optimization | level_3_tests/test_38 | ✅ Yes (RL optimization) |
| Knowledge Graph Enrichment | 3 | ArangoDB, All sources | Continuous graph enhancement | level_3_tests/test_39 | ❌ No |
| Full Granger Ecosystem | 3 | All modules | Complete ecosystem integration test | level_3_tests/test_40 | ✅ Yes (Chaos Engineering) |
| YouTube Research Integration | 3 | YouTube, ArXiv, GitGet, ArangoDB | Video-driven research pipeline | granger_hub/scenarios | ❌ No |

## Granger Hub Specific Scenarios (Not in Level Tests)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| Codebase Enhancement | 2-3 | GitGet, Marker, Test Reporter | Analyze and enhance codebases | granger_hub/scenarios | ❌ No |
| CWE Security Analysis | 2-3 | SPARTA, Marker, ArangoDB | Map code to CWE weaknesses | granger_hub/scenarios | ❌ No |
| Data Validation | 1-2 | Various data sources | Validate data quality and consistency | granger_hub/scenarios | ❌ No |
| Document Comparison | 1-2 | Marker, ArangoDB | Compare multiple documents | granger_hub/scenarios | ❌ No |
| Document QA | 2 | Marker, LLM Call | Question answering on documents | granger_hub/scenarios | ❌ No |
| Hardware Verification QA | 2-3 | Multiple verification modules | Hardware design verification | granger_hub/scenarios | ❌ No |
| Info Extraction | 1-2 | Marker, Various | Extract structured info from docs | granger_hub/scenarios | ❌ No |
| Multi-Step Processing | 2 | Multiple modules | Complex multi-step workflows | granger_hub/scenarios | ❌ No |
| NIST Compliance Check | 2-3 | SPARTA, Marker, ArangoDB | Check NIST standard compliance | granger_hub/scenarios | ❌ No |
| PDF Page Screenshot | 1-2 | Marker, MCP Screenshot | Visual PDF processing | granger_hub/scenarios | ❌ No |
| Quantum Safe Crypto Migration | 3 | ArXiv, Marker, SPARTA, YouTube | Migrate to quantum-safe cryptography | granger_hub/scenarios | ❌ No |
| Satellite Firmware Vulnerability | 3 | SPARTA, GitGet, Multiple | Analyze satellite firmware security | granger_hub/scenarios | ❌ No |
| Scientific Paper Validation | 2-3 | ArXiv, Marker, Multiple | Validate scientific paper claims | granger_hub/scenarios | ❌ No |
| Table Detection Extraction | 1-2 | Marker, ArangoDB | Extract tables from documents | granger_hub/scenarios | ❌ No |
| Research YouTube to Knowledge Graph | 3 | YouTube, ArXiv, ArangoDB | Build knowledge graph from videos | granger_hub/scenarios | ❌ No |
| Chat UI Research Test | 4 | Chat UI, All modules | UI-driven research workflows | granger_hub/scenarios | ❌ No |

## Bug Hunter Specific Scenarios (Not in Test Files)

| Scenario Name | Level | Modules Involved | Description | Source | In Bug Hunter Doc? |
|--------------|-------|-----------------|-------------|--------|-------------------|
| Memvid Visual Memory Hunter | 0 | Memvid | QR encoding, video compression bugs | Bug Hunter Doc | ✅ Yes |
| Memvid Integration Hunter | 1 | Memvid, Marker, ArangoDB | Visual preservation, version tracking | Bug Hunter Doc | ✅ Yes |
| Performance Degradation Hunter | 0 | Any module | Memory leaks, connection pools | Bug Hunter Doc | ✅ Yes |
| Timeout and Retry Bug Hunter | 1 | Any two modules | Timeout handling, retry logic | Bug Hunter Doc | ✅ Yes |
| Resource Leak Bug Hunter | 2 | Multiple modules | Connection, memory, file handle leaks | Bug Hunter Doc | ✅ Yes |
| Injection Bug Hunter | 3 | All modules | SQL, command, path injection tests | Bug Hunter Doc | ✅ Yes |
| Deadlock Bug Hunter | 2 | ArangoDB, concurrent modules | Deadlock detection and prevention | Bug Hunter Doc | ✅ Yes |

## Summary Statistics

- **Total Unique Scenarios**: 67
- **Level 0 (Single Module)**: 10 scenarios
- **Level 1 (Binary Interaction)**: 10 scenarios
- **Level 2 (Pipeline/Workflow)**: 10 scenarios
- **Level 3 (Ecosystem-Wide)**: 11 scenarios
- **Level 4 (UI-Driven)**: 1 scenario
- **Granger Hub Specific**: 16 scenarios
- **Bug Hunter Specific**: 9 scenarios

### Coverage Analysis

- **Scenarios in Bug Hunter Doc**: 19/67 (28.4%)
- **New Scenarios from Test Files**: 39/67 (58.2%)
- **New Scenarios from Granger Hub**: 16/67 (23.9%)
- **Bug Hunter Unique Scenarios**: 9/67 (13.4%)

### Key Findings

1. **Most scenarios (71.6%) are NOT in the Bug Hunter doc**, indicating significant testing gaps
2. **Granger Hub scenarios** focus on practical use cases (document processing, compliance, security analysis)
3. **Level test scenarios** focus on integration patterns and data flow
4. **Bug Hunter scenarios** focus on finding specific bug types (memory leaks, deadlocks, injections)

### Recommendations

1. **Integrate all unique scenarios** into the Bug Hunter framework
2. **Add bug targets** to scenarios that don't have them
3. **Create variations** of successful bug-finding patterns
4. **Prioritize untested scenarios** for immediate bug hunting
5. **Add Memvid integration** to more scenarios since it's a WIP module