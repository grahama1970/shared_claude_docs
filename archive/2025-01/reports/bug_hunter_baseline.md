# Granger Verification Phase 1 Report

Generated: 2025-06-09 09:32:47

## Summary
- Projects scanned: 19
- Files scanned: 8742
- Total issues found: 4925
- Issues fixed: 0

## Issues by Type

### Mock Usage (1091 instances)

Mocks must be removed - use real APIs/services instead:


#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/integration/test_rl_manager_enhanced_integration.py
- Line 140: `patch`
- Line 203: `patch`
- Line 271: `patch`
- Line 338: `patch`
- Line 390: `patch`
- Line 421: `patch`
- Line 480: `patch`
- Line 527: `patch`
- Line 636: `patch`
- Line 140: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=task_aware_mock):`
- Line 203: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=load_sensitive_mock):`
- Line 271: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=cost_aware_mock):`
- Line 338: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=context_sensitive_mock):`
- Line 391: `return_value="Response from session 1") as mock1:`
- Line 422: `return_value="Response from session 2") as mock2:`
- Line 480: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=failure_pattern_mock):`
- Line 528: `return_value="Generic response") as mock_ask:`
- Line 637: `return_value="Response") as mock_ask:`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_circuit_breaker.py
- Line 201: `call_count = 0`
- Line 205: `nonlocal call_count`
- Line 206: `call_count += 1`
- Line 210: `if call_count == 1:`
- Line 213: `elif call_count == 2:`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_find_or_blocks.py
- Line 15: `import unittest`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_llm_providers.py
- Line 155: `call_count = 0`
- Line 157: `nonlocal call_count`
- Line 158: `call_count += 1`
- Line 161: `content=f"Response {call_count}",`
- Line 174: `assert call_count == 1`
- Line 179: `assert call_count == 1  # No new API call`
- Line 184: `assert call_count == 2`
- Line 192: `assert call_count == 3`
- Line 198: `assert call_count == 4`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_oss_agent_integration.py
- Line 25: `from aider_daemon.modules.mock_modules import MockMarkerModule, MockArangoModule, MockTestReporterModule`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_oss_agent_thinking_mock.py
- Line 63: `patch`
- Line 143: `patch`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_pattern_extraction.py
- Line 30: `from aider_daemon.modules.mock_modules import MockMarkerModule, MockArangoModule, MockTestReporterModule`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_print_mode.py
- Line 90: `patch`
- Line 91: `patch`
- Line 164: `patch`
- Line 300: `patch`
- Line 90: `with patch('src.aider_daemon.cli.print_mode.is_stdin_pipe', return_value=True):`
- Line 164: `with patch('src.aider_daemon.cli.print_mode.is_stdin_pipe', return_value=False):`
- Line 300: `with patch('src.aider_daemon.cli.print_mode.is_stdin_pipe', return_value=False):`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_production_workflows.py
- Line 68: `call_count = 0`
- Line 71: `nonlocal call_count`
- Line 72: `call_count += 1`
- Line 75: `if call_count <= 3:`
- Line 104: `# This call will succeed (call_count = 5)`
- Line 150: `call_count = 0`
- Line 153: `nonlocal call_count`
- Line 154: `call_count += 1`
- Line 156: `if call_count == 1:`
- Line 158: `elif call_count == 2:`
- Line 161: `return {"result": "success", "attempts": call_count}`
- Line 663: `call_count = 0`
- Line 666: `nonlocal call_count`
- Line 667: `call_count += 1`
- Line 669: `if call_count == 1:`
- Line 671: `elif call_count == 2:`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_resume_flag.py
- Line 120: `patch`
- Line 141: `patch`
- Line 264: `patch`
- Line 120: `with patch('builtins.input', return_value='2'):`
- Line 141: `with patch('builtins.input', return_value='q'):`
- Line 264: `with patch('builtins.input', return_value='1'):`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_rl_manager_enhanced_performance.py
- Line 142: `patch`
- Line 229: `patch`
- Line 229: `with patch('aider_daemon.core.rl_manager_enhanced.ask', return_value="Response"):`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_security_scenarios.py
- Line 40: `from aider_daemon.modules.mock_sparta_module import MockSpartaModule`
- Line 41: `from aider_daemon.modules.mock_modules import MockMarkerModule, MockArangoModule, MockTestReporterModule`

#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_session_listing.py
- Line 141: `patch`
- Line 159: `patch`
- Line 165: `patch`
- Line 241: `patch`
- Line 141: `with patch('builtins.input', return_value='2'):`
- Line 159: `with patch('builtins.input', return_value='q'):`
- Line 165: `with patch('builtins.input', side_effect=inputs):`
- Line 241: `with patch('builtins.input', side_effect=[invalid_input, 'q']):`

#### /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_analytics.py
- Line 82: `patch`
- Line 85: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # mock_mp_track\\\\\.assert_called_once()`
- Line 86: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_ph_capture\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_browser.py
- Line 16: `import unittest`
- Line 47: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_launch_gui\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_linter.py
- Line 16: `import unittest`
- Line 109: `patch`
- Line 120: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_popen\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_repo.py
- Line 11: `import unittest`
- Line 148: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self.assertEqual(mock_send\\\\\.call_count, 2)`
- Line 237: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_send\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_scripting.py
- Line 15: `import unittest`
- Line 63: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self.assertEqual(mock_send\\\\\.call_count, 2)`

#### /home/graham/workspace/experiments/aider-daemon/archive/old_tests/test_honeypot.py
- Line 69: `Mock`
- Line 94: `assert hasattr(mock_process, "assert_called"), "HONEYPOT TRIGGERED: Mock process detected"`

#### /home/graham/workspace/experiments/aider-daemon/archive/tests/tests/legacy/basic/basic/test_history.py
- Line 15: `from unittest import TestCase, mock`
- Line 23: `.Mock`
- Line 75: `.patch`
- Line 87: `.Mock`
- Line 89: `.Mock`
- Line 93: `.Mock`
- Line 95: `.Mock`
- Line 78: `return_value=[{"role": "user", "content": "Summary"}],`
- Line 89: `mock_model1.simple_send_with_retries = mock.Mock(side_effect=Exception("Model 1 failed"))`
- Line 95: `mock_model2.simple_send_with_retries = mock.Mock(return_value="Summary from Model 2")`
- Line 109: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_model1.simple_send_with_retries\\\\\.assert_called_once()`
- Line 110: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_model2.simple_send_with_retries\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/archive/tests/tests/unit/core/test_rl_manager_enhanced.py
- Line 208: `patch`
- Line 226: `patch`
- Line 450: `patch`
- Line 639: `patch`
- Line 781: `patch`
- Line 450: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=mock_ask):`
- Line 639: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=mock_ask_with_failures):`
- Line 781: `with patch('aider_daemon.core.rl_manager_enhanced.ask', side_effect=realistic_mock):`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/patch_coder.py
- Line 297: `patch`
- Line 329: `patch`
- Line 352: `patch`
- Line 362: `patch`
- Line 375: `patch`
- Line 384: `patch`
- Line 393: `patch`
- Line 409: `patch`
- Line 410: `patch`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/search_replace.py
- Line 212: `patch`
- Line 213: `patch`
- Line 214: `patch`
- Line 216: `patch`
- Line 217: `patch`
- Line 222: `patch`
- Line 222: `patch`
- Line 222: `patch`
- Line 223: `patch`
- Line 294: `patch`
- Line 295: `patch`
- Line 299: `patch`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/scripts/issues.py
- Line 146: `.patch`
- Line 199: `.patch`
- Line 243: `.patch`
- Line 305: `.patch`
- Line 330: `.patch`
- Line 392: `.patch`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_analytics.py
- Line 82: `patch`
- Line 85: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # mock_mp_track\\\\\.assert_called_once()`
- Line 86: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_ph_capture\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_find_or_blocks.py
- Line 15: `import unittest`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_history.py
- Line 15: `from unittest import TestCase, mock`
- Line 23: `.Mock`
- Line 75: `.patch`
- Line 87: `.Mock`
- Line 89: `.Mock`
- Line 93: `.Mock`
- Line 95: `.Mock`
- Line 78: `return_value=[{"role": "user", "content": "Summary"}],`
- Line 89: `mock_model1.simple_send_with_retries = mock.Mock(side_effect=Exception("Model 1 failed"))`
- Line 95: `mock_model2.simple_send_with_retries = mock.Mock(return_value="Summary from Model 2")`
- Line 109: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_model1.simple_send_with_retries\\\\\.assert_called_once()`
- Line 110: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_model2.simple_send_with_retries\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/aider-daemon/scripts/issues.py
- Line 146: `.patch`
- Line 199: `.patch`
- Line 243: `.patch`
- Line 305: `.patch`
- Line 330: `.patch`
- Line 392: `.patch`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/event_system.py
- Line 134: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count = 0`
- Line 155: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count += 1`

#### /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/validate_memory_commands.py
- Line 87: `MagicMock`

#### /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/validate_validate_memory_commands.py
- Line 101: `from arangodb.cli.validate_memory_commands import MockStandardDatabase`

#### /home/graham/workspace/experiments/arangodb/archive/pre_refactor/memory_agent/memory_agent_validator.py
- Line 26: `import unittest`

#### /home/graham/workspace/experiments/arangodb/archive/pre_refactor/search_api/search_api_validator.py
- Line 28: `import unittest`

#### /home/graham/workspace/experiments/arangodb/archive/pre_refactor/search_api/test_search_api_diagnostics.py
- Line 51: `import unittest`

#### /home/graham/workspace/experiments/arangodb/archive/tasks_2/isolated_test_arango_setup.py
- Line 168: `patch`

#### /home/graham/workspace/experiments/arangodb/archive/tasks_2/test_dependency_checker.py
- Line 49: `from src.arangodb.core.utils.dependency_checker import check_dependency, get_mock_class, HAS_ARANGO, HAS_NUMPY, HAS_TORCH, HAS_TRANSFORMERS, HAS_SENTENCE_TRANSFORMERS, MockStandardDatabase, _DEPENDENCY_STATUS`

#### /home/graham/workspace/experiments/arangodb/archive/tests/iterations/test_memory_agent.py
- Line 36: `import unittest`

#### /home/graham/workspace/experiments/arangodb/archive/tests/iterations/test_memory_agent_mocked.py
- Line 24: `import unittest`

#### /home/graham/workspace/experiments/arangodb/archive/tests/iterations/test_memory_agent_real.py
- Line 29: `import unittest`

#### /home/graham/workspace/experiments/arangodb/examples/screenshot/tests/test_cli_formatters.py
- Line 37: `import unittest`

#### /home/graham/workspace/experiments/arangodb/examples/screenshot/tests/test_core_utils.py
- Line 25: `import unittest`

#### /home/graham/workspace/experiments/arangodb/examples/screenshot/tests/test_mcp_wrappers.py
- Line 37: `import unittest`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_gemini.py
- Line 56: `MagicMock`
- Line 64: `MagicMock`
- Line 72: `MagicMock`
- Line 86: `patch`
- Line 105: `MagicMock`
- Line 126: `MagicMock`
- Line 115: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_gemini_client.aio.models.embed_content\\\\\.assert_called_once()`
- Line 137: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_gemini_client.aio.models.embed_content\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_openai.py
- Line 57: `MagicMock`
- Line 65: `MagicMock`
- Line 73: `MagicMock`
- Line 87: `patch`
- Line 105: `MagicMock`
- Line 126: `MagicMock`
- Line 115: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_openai_client.embeddings.create\\\\\.assert_called_once()`
- Line 137: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_openai_client.embeddings.create\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_voyage.py
- Line 57: `MagicMock`
- Line 65: `MagicMock`
- Line 79: `patch`
- Line 98: `MagicMock`
- Line 125: `MagicMock`
- Line 108: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_voyageai_client.embed\\\\\.assert_called_once()`
- Line 136: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_voyageai_client.embed\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/llm_client/test_anthropic_client.py
- Line 69: `patch`
- Line 81: `patch`
- Line 194: `patch`
- Line 216: `patch`
- Line 81: `with patch('anthropic.AsyncAnthropic', return_value=mock_async_anthropic):`
- Line 156: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_async_anthropic.messages.create\\\\\.assert_called_once()`
- Line 277: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_async_anthropic.messages.create\\\\\.call_count == 2`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/verify_exporter.py
- Line 18: `from test_utils import MockContextGenerator`

#### /home/graham/workspace/experiments/claude-test-reporter/archive/deprecated_tests/test_analyzers.py
- Line 38: `from claude_test_reporter.analyzers.mock_detector import MockDetector`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/__init__.py
- Line 19: `from mock_detector import MockDetector`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/comprehensive_analyzer.py
- Line 44: `from mock_detector import MockDetector`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/mock_detector.py
- Line 132: `if "@patch" in content and "return_value = True" in content:`
- Line 269: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_get\\\\\.assert_called()`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/realtime_monitor.py
- Line 244: `(r'assert_called', "Asserting mock was called"),`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/monitoring/hallucination_monitor.py
- Line 50: `from claude_test_reporter.analyzers.mock_detector import MockDetector`

#### /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_api_test.py
- Line 248: `patch`
- Line 249: `patch`
- Line 250: `patch`
- Line 254: `patch`
- Line 248: `with patch("gitget.api.process_workflow", return_value=True):`
- Line 249: `with patch("gitget.api.os.path.exists", return_value=True):`

#### /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_cli_commands_test.py
- Line 260: `from mocklogger import MockLogger`

#### /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_enhanced_logger_test.py
- Line 26: `import unittest`

#### /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_summarization_test.py
- Line 157: `patch`
- Line 158: `patch`
- Line 159: `patch`
- Line 245: `patch`
- Line 246: `patch`
- Line 247: `patch`
- Line 249: `patch`
- Line 306: `patch`
- Line 157: `with patch("gitget.summarization.litellm.completion", return_value=mock_response):`
- Line 159: `with patch("gitget.summarization.count_tokens_with_tiktoken", return_value=100):`
- Line 245: `with patch("gitget.summarization.litellm.completion", return_value=mock_response):`
- Line 247: `with patch("gitget.summarization.count_tokens_with_tiktoken", return_value=100):`
- Line 249: `with patch("gitget.summarization.json_to_markdown", return_value="# Markdown Summary\n\nTest summary"):`

#### /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_text_summarizer_test.py
- Line 245: `patch`
- Line 272: `patch`
- Line 273: `patch`
- Line 309: `patch`
- Line 356: `patch`
- Line 385: `patch`
- Line 386: `patch`
- Line 245: `with patch('gitget.utils.text_summarizer.count_tokens_with_tiktoken', side_effect=lambda text: len(text.split())):`
- Line 272: `with patch('gitget.utils.text_summarizer.reliable_completion', side_effect=mock_reliable_completion):`
- Line 273: `with patch('gitget.utils.text_summarizer.count_tokens_with_tiktoken', side_effect=lambda text, model=None: len(text.split())):`
- Line 310: `side_effect=lambda texts, config: [[0.5, 0.5, 0.5] for _ in texts]):`
- Line 356: `with patch('gitget.utils.text_summarizer.reliable_completion', side_effect=mock_reliable_completion):`
- Line 385: `with patch('gitget.utils.text_summarizer.reliable_completion', side_effect=mock_reliable_completion):`
- Line 386: `with patch('gitget.utils.text_summarizer.count_tokens_with_tiktoken', side_effect=lambda text, model=None: len(text.split())):`

#### /home/graham/workspace/experiments/gitget/archive/deprecated_tests/gitget/test_api.py
- Line 75: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process_workflow\\\\\.assert_called_once()`
- Line 152: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process_workflow\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/gitget/archive/deprecated_tests/gitget/test_summarization_additional.py
- Line 287: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_initialize_cache\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_bench.py
- Line 18: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_cli.py
- Line 9: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_examples.py
- Line 12: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_misc.py
- Line 3: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_system.py
- Line 11: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_timeit.py
- Line 8: `import unittest`

#### /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_utils.py
- Line 17: `import unittest`
- Line 210: `.patch`
- Line 220: `.patch`
- Line 210: `with mock.patch('pyperf._utils.open', create=True, side_effect=mock_open):`
- Line 220: `with mock.patch('builtins.open', side_effect=IOError):`

#### /home/graham/workspace/experiments/gitget/repos/gitingest/tests/test_flow_integration.py
- Line 43: `patch`
- Line 51: `patch`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_bench.py
- Line 18: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_cli.py
- Line 9: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_examples.py
- Line 12: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_misc.py
- Line 3: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_system.py
- Line 11: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_timeit.py
- Line 8: `import unittest`

#### /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_utils.py
- Line 17: `import unittest`
- Line 210: `.patch`
- Line 220: `.patch`
- Line 210: `with mock.patch('pyperf._utils.open', create=True, side_effect=mock_open):`
- Line 220: `with mock.patch('builtins.open', side_effect=IOError):`

#### /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/cli/test_screenshot_commands.py
- Line 71: `mock_module.process = AsyncMock(return_value={`
- Line 103: `mock_module.process = AsyncMock(return_value={`
- Line 121: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_module.process\\\\\.assert_called_once()`
- Line 145: `mock_module.process = AsyncMock(return_value={`
- Line 184: `mock_module.process = AsyncMock(side_effect=[`
- Line 231: `mock_module.process = AsyncMock(return_value={`
- Line 277: `mock_module.process = AsyncMock(return_value={`
- Line 319: `mock_module.process = AsyncMock(return_value={`
- Line 356: `mock_module.process = AsyncMock(return_value={`
- Line 394: `mock_module.process = AsyncMock(return_value={`
- Line 431: `mock_module.process = AsyncMock(return_value={`
- Line 462: `mock_module.process = AsyncMock(return_value={`
- Line 500: `mock_module.process = AsyncMock(return_value={`

#### /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/rl/metrics/test_rl_metrics_mock.py
- Line 64: `patch`
- Line 64: `with patch('granger_hub.rl.metrics.arangodb_store.ArangoClient', return_value=mock_arango_client):`

#### /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_discovery_system.py
- Line 454: `patch`

#### /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_satellite_firmware.py
- Line 202: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_modules.get_mock("marker")\\\\\.assert_called("extract_firmware_documentation", 1)`
- Line 203: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_modules.get_mock("sparta")\\\\\.assert_called("analyze_vulnerabilities", 1)`

#### /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_self_improvement_system.py
- Line 100: `patch`
- Line 114: `patch`
- Line 330: `patch`
- Line 387: `patch`
- Line 457: `patch`
- Line 125: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_discovery\\\\\.assert_called_once()`
- Line 459: `mock_engine.analyze_ecosystem = AsyncMock(return_value={})`
- Line 460: `mock_engine.discover_improvements = AsyncMock(return_value=[`
- Line 476: `mock_engine.generate_improvement_tasks = AsyncMock(return_value=[Path("test.md")])`
- Line 482: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_engine.analyze_ecosystem\\\\\.assert_called_once()`
- Line 483: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_engine.discover_improvements\\\\\.assert_called_once()`
- Line 484: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_engine.generate_improvement_tasks\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/patch_coder.py
- Line 297: `patch`
- Line 329: `patch`
- Line 352: `patch`
- Line 362: `patch`
- Line 375: `patch`
- Line 384: `patch`
- Line 393: `patch`
- Line 409: `patch`
- Line 410: `patch`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/search_replace.py
- Line 212: `patch`
- Line 213: `patch`
- Line 214: `patch`
- Line 216: `patch`
- Line 217: `patch`
- Line 222: `patch`
- Line 222: `patch`
- Line 222: `patch`
- Line 223: `patch`
- Line 294: `patch`
- Line 295: `patch`
- Line 299: `patch`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/scripts/issues.py
- Line 146: `.patch`
- Line 199: `.patch`
- Line 243: `.patch`
- Line 305: `.patch`
- Line 330: `.patch`
- Line 392: `.patch`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/__init__.py
- Line 22: `from test_scripting import TestScriptingAPI, mock_send_side_effect`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_analytics.py
- Line 91: `patch`
- Line 94: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # mock_mp_track\\\\\.assert_called_once()`
- Line 95: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_ph_capture\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_aws_credentials.py
- Line 45: `patch`
- Line 77: `patch`
- Line 109: `patch`
- Line 140: `patch`
- Line 172: `patch`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_find_or_blocks.py
- Line 15: `import unittest`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_linter.py
- Line 16: `import unittest`
- Line 82: `patch`
- Line 93: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_popen\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_scripting.py
- Line 15: `import unittest`
- Line 54: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self.assertEqual(mock_send\\\\\.call_count, 2)`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_sendchat.py
- Line 15: `import unittest`
- Line 61: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_print\\\\\.call_count == 3`
- Line 74: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_completion\\\\\.assert_called_once()`
- Line 109: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_print\\\\\.call_count == 1`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/browser/test_browser.py
- Line 16: `import unittest`
- Line 38: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_launch_gui\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/granger_hub/scenarios/level_3_youtube_research_integration_test.py
- Line 90: `patch`
- Line 91: `patch`
- Line 92: `patch`
- Line 101: `MagicMock`
- Line 103: `MagicMock`
- Line 112: `MagicMock`
- Line 146: `patch`
- Line 152: `MagicMock`
- Line 214: `patch`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/forecast/ollama_forecast.py
- Line 80: `patch`
- Line 81: `patch`
- Line 82: `patch`
- Line 84: `patch`

#### /home/graham/workspace/experiments/granger_hub/tests/__init__.py
- Line 9: `from test_conversation_integration_mock import MockConversationManager, MockCommunicator, MockMessage`
- Line 12: `from test_arango_conversations_mock import MockArangoCollection, MockArangoDatabase, MockArangoConversationStore`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/__init__.py
- Line 5: `from conftest import event_loop, mock_modules, workflow_runner`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/base/__init__.py
- Line 5: `from module_mock import MockResponse, ModuleMock, ModuleMockGroup`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/base/module_mock.py
- Line 40: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count = 0`
- Line 130: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count = 0`
- Line 133: `def assert_called(self, task: str, times: Optional[int] = None) -> None:`
- Line 167: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count += 1`
- Line 171: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: "call_number": self\\\\\.call_count,`
- Line 283: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: print(f"{name}: {mock\\\\\.call_count} calls")`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/base/result_assertions.py
- Line 61: `call_count = len(calls)`
- Line 64: `assert call_count == times, f"Expected {module_name} called {times} times, got {call_count}"`
- Line 67: `assert call_count >= min_times, f"Expected {module_name} called at least {min_times} times, got {call_count}"`
- Line 70: `assert call_count <= max_times, f"Expected {module_name} called at most {max_times} times, got {call_count}"`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/conftest.py
- Line 16: `from tests.integration_scenarios.base.module_mock import ModuleMock, ModuleMockGroup`

#### /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_claude_collaboration.py
- Line 86: `patch`
- Line 87: `patch`
- Line 88: `patch`
- Line 124: `patch`
- Line 87: `patch.object(Path, 'is_file', return_value=True), \`
- Line 88: `patch.object(Path, 'is_dir', return_value=True):`

#### /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_max_model_routing_functional.py
- Line 72: `patch`
- Line 73: `patch`
- Line 74: `patch`
- Line 179: `patch`
- Line 180: `patch`
- Line 181: `patch`
- Line 229: `patch`
- Line 230: `patch`
- Line 231: `patch`
- Line 281: `patch`
- Line 282: `patch`
- Line 283: `patch`
- Line 73: `patch.object(Path, 'is_file', return_value=True), \`
- Line 74: `patch.object(Path, 'is_dir', return_value=True):`
- Line 180: `patch.object(Path, 'is_file', return_value=True), \`
- Line 181: `patch.object(Path, 'is_dir', return_value=True):`
- Line 230: `patch.object(Path, 'is_file', return_value=True), \`
- Line 231: `patch.object(Path, 'is_dir', return_value=True):`
- Line 282: `patch.object(Path, 'is_file', return_value=True), \`
- Line 283: `patch.object(Path, 'is_dir', return_value=True):`

#### /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_rl_integration_comprehensive.py
- Line 120: `patch`
- Line 121: `patch`
- Line 122: `patch`
- Line 123: `patch`
- Line 272: `patch`
- Line 297: `patch`
- Line 301: `MagicMock`
- Line 311: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_request\\\\\.call_count >= 2`

#### /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/test_mcp_features.py
- Line 238: `patch`

#### /home/graham/workspace/experiments/llm_call/archive/gemini_refactor/core/__init__.py
- Line 30: `.patch`

#### /home/graham/workspace/experiments/llm_call/archive/root_cleanup/test_files/test_poc_retry_mock.py
- Line 69: `call_counter = {"count": 0}`
- Line 73: `call_counter["count"] += 1`
- Line 79: `if call_counter["count"] <= 1 and not is_retry:`
- Line 131: `call_counter["count"] = 0`
- Line 147: `logger.info(f"  Total calls made: {call_counter['count']}")`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/lite-llm-mcp/test_agent.py
- Line 58: `patch`
- Line 63: `patch`
- Line 77: `patch`
- Line 100: `patch`
- Line 77: `with patch.object(agent, '_start_mcp_server', return_value=(mock_process, {})):`
- Line 82: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process.stdin.write\\\\\.assert_called_once()`
- Line 83: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process.stdin.flush\\\\\.assert_called_once()`
- Line 100: `with patch.object(agent, '_start_mcp_server', return_value=(mock_process, {})):`
- Line 122: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process1.terminate\\\\\.assert_called_once()`
- Line 123: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_process2.terminate\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/send_emails/endpoints.py
- Line 156: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/__init__.py
- Line 1075: `from exceptions import AuthenticationError, InvalidRequestError, BadRequestError, NotFoundError, RateLimitError, ServiceUnavailableError, OpenAIError, ContextWindowExceededError, ContentPolicyViolationError, BudgetExceededError, APIError, Timeout, APIConnectionError, UnsupportedParamsError, APIResponseValidationError, UnprocessableEntityError, InternalServerError, JSONSchemaValidationError, LITELLM_EXCEPTION_TYPES, MockException`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/azure_storage/azure_storage.py
- Line 234: `.patch`
- Line 254: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/litellm_logging.py
- Line 60: `from litellm.constants import DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT, DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/converse_handler.py
- Line 37: `from invoke_handler import AWSEventStreamDecoder, MockResponseIterator, make_call`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/custom_httpx/llm_http_handler.py
- Line 47: `from litellm.llms.base_llm.base_model_iterator import MockResponseIterator`
- Line 61: `from litellm.responses.streaming_iterator import BaseResponsesAPIStreamingIterator, MockResponsesAPIStreamingIterator, ResponsesAPIStreamingIterator, SyncResponsesAPIStreamingIterator`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/openai.py
- Line 53: `from litellm.llms.bedrock.chat.invoke_handler import MockResponseIterator`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai_like/chat/handler.py
- Line 26: `from litellm.llms.bedrock.chat.invoke_handler import MockResponseIterator`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/main.py
- Line 74: `from litellm.constants import DEFAULT_MOCK_RESPONSE_COMPLETION_TOKEN_COUNT, DEFAULT_MOCK_RESPONSE_PROMPT_TOKEN_COUNT`
- Line 89: `from litellm.litellm_core_utils.mock_functions import mock_embedding, mock_image_generation`
- Line 103: `from litellm.utils import CustomStreamWrapper, ProviderConfigManager, Usage, add_openai_metadata, async_mock_completion_streaming_obj, convert_to_model_response_object, create_pretrained_tokenizer, create_tokenizer, get_api_key, get_llm_provider, get_non_default_completion_params, get_optional_params_embeddings, get_optional_params_image_gen, get_optional_params_transcription, get_secret, get_standard_openai_params, mock_completion_streaming_obj, read_config_args, supports_httpx_timeout, token_counter, validate_and_fix_openai_messages, validate_chat_completion_tool_choice`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/credential_endpoints/endpoints.py
- Line 294: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/guardrails/guardrail_endpoints.py
- Line 482: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/guardrails/guardrail_hooks/presidio.py
- Line 587: `from litellm.llms.base_llm.base_model_iterator import MockResponseIterator`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/management_endpoints/model_management_endpoints.py
- Line 141: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/management_endpoints/organization_endpoints.py
- Line 217: `.patch`
- Line 579: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/management_endpoints/scim/scim_v2.py
- Line 324: `.patch`
- Line 733: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/ui_crud_endpoints/proxy_setting_endpoints.py
- Line 268: `.patch`
- Line 286: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/batches_tests/test_batches_logging_unit_tests.py
- Line 191: `patch`
- Line 191: `with patch("litellm.completion_cost", return_value=0.5):`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/batches_tests/test_openai_batches_and_files.py
- Line 474: `patch`
- Line 476: `patch`
- Line 526: `patch`
- Line 475: `client, "post", side_effect=mock_side_effect`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/guardrails_tests/test_tracing_guardrails.py
- Line 142: `patch`
- Line 175: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_post\\\\\.call_count >= 1`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/image_gen_tests/test_image_variation.py
- Line 111: `patch`
- Line 122: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/enterprise/enterprise_callbacks/send_emails/test_resend_email.py
- Line 49: `.patch`
- Line 55: `.patch`
- Line 88: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_httpx_client.post\\\\\.assert_called_once()`
- Line 126: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_httpx_client.post\\\\\.assert_called_once()`
- Line 148: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_httpx_client.post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/enterprise/test_enterprise_routes.py
- Line 58: `#         return_value=True,`
- Line 72: `#         return_value=False,`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/SlackAlerting/test_slack_alerting.py
- Line 37: `import unittest`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/arize/test_arize_utils.py
- Line 116: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert span.set_attribute\\\\\.call_count == 28`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_anthropic_cache_control_hook.py
- Line 40: `import unittest`
- Line 59: `patch`
- Line 92: `patch`
- Line 135: `patch`
- Line 168: `patch`
- Line 92: `with patch.object(client, "post", return_value=mock_response) as mock_post:`
- Line 123: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 168: `with patch.object(client, "post", return_value=mock_response) as mock_post:`
- Line 195: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/litellm_core_utils/test_duration_parser.py
- Line 28: `import unittest`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/databricks/test_databricks_common_utils.py
- Line 52: `patch`
- Line 65: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_get_credentials\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/meta_llama/test_meta_llama_chat_transformation.py
- Line 51: `patch`
- Line 51: `with patch("litellm.get_model_info", side_effect=Exception("Test error")):`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/nscale/chat/test_nscale_chat_transformation.py
- Line 57: `patch`
- Line 64: `patch`
- Line 76: `patch`
- Line 83: `patch`
- Line 59: `return_value="env-key",`
- Line 78: `return_value="https://env-base.com",`
- Line 84: `"litellm.llms.nscale.chat.transformation.get_secret_str", return_value=None`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/openai/responses/test_openai_responses_transformation.py
- Line 165: `patch`
- Line 195: `patch`
- Line 204: `patch`
- Line 205: `patch`
- Line 218: `patch`
- Line 219: `patch`
- Line 220: `patch`
- Line 244: `patch`
- Line 253: `patch`
- Line 254: `patch`
- Line 266: `patch`
- Line 267: `patch`
- Line 222: `return_value="env_api_key",`
- Line 256: `return_value="https://env-api-base.example.com/v1",`
- Line 269: `return_value=None,`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/sagemaker/test_sagemaker_common_utils.py
- Line 71: `patch`
- Line 117: `patch`
- Line 71: `with patch("botocore.eventstream.EventStreamBuffer", return_value=mock_buffer):`
- Line 117: `with patch("botocore.eventstream.EventStreamBuffer", return_value=mock_buffer):`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/vertex_ai/test_http_status_201.py
- Line 44: `import unittest`
- Line 98: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client.post\\\\\.assert_called_once()`
- Line 104: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self.mock_logging_obj.post_call\\\\\.assert_called_once()`
- Line 131: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self.mock_logging_obj.post_call\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/vertex_ai/test_vertex_ai_common_utils.py
- Line 572: `patch`
- Line 572: `with patch("litellm.VertexGeminiConfig.get_model_for_vertex_ai_url", side_effect=lambda model: model):`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/vertex_ai/test_vertex_llm_base.py
- Line 70: `patch`
- Line 89: `patch`
- Line 119: `patch`
- Line 165: `patch`
- Line 167: `patch`
- Line 231: `patch`
- Line 233: `patch`
- Line 71: `vertex_base, "load_auth", return_value=(mock_creds, "project-1")`
- Line 90: `vertex_base, "load_auth", return_value=(mock_creds, "project-1")`
- Line 120: `vertex_base, "load_auth", return_value=(mock_creds, "project-1")`
- Line 166: `vertex_base, "load_auth", return_value=(mock_creds, "project-1")`
- Line 232: `vertex_base, "_credentials_from_authorized_user", return_value=mock_creds`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/anthropic_endpoints/test_endpoints.py
- Line 45: `import unittest`
- Line 68: `mock_proxy_logging_obj.async_post_call_streaming_hook = AsyncMock(side_effect=lambda **kwargs: kwargs["response"])`
- Line 94: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_safe_dumps\\\\\.call_count == 2  # Called twice, once for each dict object`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/auth/test_auth_exception_handler.py
- Line 102: `patch`
- Line 163: `patch`
- Line 168: `patch`
- Line 185: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post_call_failure_hook\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_global_options.py
- Line 59: `patch`
- Line 60: `patch`
- Line 70: `patch`
- Line 71: `patch`
- Line 59: `with patch("litellm.proxy.client.health.HealthManagementClient.get_server_version", return_value="1.2.3"), \`
- Line 70: `with patch("litellm.proxy.client.health.HealthManagementClient.get_server_version", return_value="1.2.3"), \`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/test_users.py
- Line 56: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_get\\\\\.assert_called_once()`
- Line 69: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_get\\\\\.assert_called_once()`
- Line 82: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 95: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/db/test_check_migration.py
- Line 56: `.patch`
- Line 62: `.patch`
- Line 64: `return_value=(True, ["ALTER TABLE users ADD COLUMN new_field TEXT;"]),`
- Line 74: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_logger.exception\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/health_endpoints/test_health_endpoints.py
- Line 81: `patch`
- Line 81: `patch`
- Line 123: `patch`
- Line 123: `patch`
- Line 90: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_prisma_client.health_check\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/scim/test_scim_transformations.py
- Line 151: `patch`
- Line 181: `patch`
- Line 195: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_common_daily_activity.py
- Line 61: `mock_table.count = AsyncMock(return_value=0)`
- Line 62: `mock_table.find_many = AsyncMock(return_value=[])`
- Line 64: `mock_prisma.db.litellm_verificationtoken.find_many = AsyncMock(return_value=[])`
- Line 85: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_table.find_many\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_key_management_endpoints.py
- Line 58: `mock_find_many = AsyncMock(return_value=[])`
- Line 78: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_find_many\\\\\.assert_called_once()`
- Line 96: `return_value = None  # TODO: Replace with real object`
- Line 102: `return_value=None`
- Line 105: `return_value=[]`
- Line 107: `mock_prisma_client.db.litellm_verificationtoken.count = AsyncMock(return_value=0)`
- Line 109: `return_value = None  # TODO: Replace with real object`
- Line 145: `return_value = None  # TODO: Replace with real object`
- Line 151: `return_value=None`
- Line 154: `return_value=[]`
- Line 156: `mock_prisma_client.db.litellm_verificationtoken.count = AsyncMock(return_value=0)`
- Line 158: `return_value = None  # TODO: Replace with real object`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_tag_management_endpoints.py
- Line 61: `patch`
- Line 61: `patch`
- Line 63: `patch`
- Line 65: `patch`
- Line 67: `patch`
- Line 117: `patch`
- Line 117: `patch`
- Line 119: `patch`
- Line 121: `patch`
- Line 163: `patch`
- Line 163: `patch`
- Line 165: `patch`
- Line 193: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_save_tags\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/pass_through_endpoints/test_pass_through_endpoints.py
- Line 161: `patch`
- Line 162: `patch`
- Line 165: `patch`
- Line 82: `upload_file.read = AsyncMock(return_value=file_content)`
- Line 96: `starlette_file.read = AsyncMock(return_value=file_content)`
- Line 117: `upload_file.read = AsyncMock(return_value=file_content)`
- Line 120: `request.form = AsyncMock(return_value=form_data)`
- Line 128: `async_client.request = AsyncMock(return_value=mock_response)`
- Line 143: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: async_client.request\\\\\.assert_called_once()`
- Line 176: `side_effect=httpx.HTTPError("Request failed")`
- Line 186: `mock_request.body = AsyncMock(return_value=b'{"test": "data"}')`
- Line 205: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_proxy_logging.post_call_failure_hook\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/router_utils/pre_call_checks/test_responses_api_deployment_check.py
- Line 144: `patch`
- Line 284: `patch`
- Line 393: `patch`
- Line 546: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/test_constants.py
- Line 83: `.patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/test_logging.py
- Line 38: `import unittest`
- Line 50: `import unittest`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm_utils_tests/test_get_secret.py
- Line 51: `Mock`
- Line 59: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_responses_api_testing/test_openai_responses_api.py
- Line 588: `patch`
- Line 688: `patch`
- Line 813: `patch`
- Line 909: `patch`
- Line 922: `patch`
- Line 1028: `patch`
- Line 625: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 724: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 831: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 924: `return_value=MockResponse(mock_response, 200),`
- Line 943: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_sync_post\\\\\.assert_called_once()`
- Line 967: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 1030: `return_value=MockResponse(mock_response, 200),`
- Line 1050: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/base_llm_unit_tests.py
- Line 1274: `patch`
- Line 1300: `patch`
- Line 1335: `patch`
- Line 1287: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 1316: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 1354: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_anthropic_completion.py
- Line 1103: `patch`
- Line 1237: `patch`
- Line 1117: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 1247: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_azure_o_series.py
- Line 47: `from respx import MockRouter`
- Line 145: `patch`
- Line 176: `patch`
- Line 228: `patch`
- Line 159: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_create\\\\\.call_count == 1`
- Line 190: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_create\\\\\.call_count == 1`
- Line 204: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_get_openai_client\\\\\.assert_called_once()`
- Line 246: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_bedrock_embedding.py
- Line 76: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_cohere.py
- Line 291: `patch`
- Line 306: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_deepseek_completion.py
- Line 111: `patch`
- Line 144: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_fireworks_ai_translation.py
- Line 243: `patch`
- Line 269: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_gpt4o_audio.py
- Line 47: `from respx import MockRouter`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_huggingface_chat_completion.py
- Line 49: `from respx import MockRouter`
- Line 121: `patch`
- Line 136: `patch`
- Line 161: `patch`
- Line 288: `patch`
- Line 288: `MagicMock`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_infinity.py
- Line 86: `patch`
- Line 142: `patch`
- Line 184: `patch`
- Line 245: `patch`
- Line 302: `patch`
- Line 350: `patch`
- Line 390: `patch`
- Line 88: `return_value=mock_response,`
- Line 101: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 144: `return_value=mock_response,`
- Line 186: `return_value=mock_response,`
- Line 198: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 247: `return_value=mock_response,`
- Line 259: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 304: `return_value=mock_response,`
- Line 315: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 352: `return_value=mock_response,`
- Line 363: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 392: `return_value=mock_response,`
- Line 402: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_litellm_proxy_provider.py
- Line 65: `patch`
- Line 99: `patch`
- Line 143: `patch`
- Line 188: `patch`
- Line 238: `patch`
- Line 282: `patch`
- Line 330: `patch`
- Line 461: `patch`
- Line 80: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_call\\\\\.assert_called_once()`
- Line 117: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_call\\\\\.assert_called_once()`
- Line 162: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_method\\\\\.assert_called_once()`
- Line 208: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_method\\\\\.assert_called_once()`
- Line 257: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_method\\\\\.assert_called_once()`
- Line 303: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_method\\\\\.assert_called_once()`
- Line 397: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_method\\\\\.assert_called_once()`
- Line 464: `return_value=mock_response,`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_nvidia_nim.py
- Line 47: `from respx import MockRouter`
- Line 63: `patch`
- Line 106: `patch`
- Line 178: `patch`
- Line 83: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 117: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 200: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_openai_o1.py
- Line 47: `from respx import MockRouter`
- Line 72: `patch`
- Line 144: `patch`
- Line 85: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 157: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_prompt_caching.py
- Line 46: `from respx import MockRouter`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_rerank.py
- Line 256: `patch`
- Line 344: `patch`
- Line 458: `patch`
- Line 544: `patch`
- Line 258: `return_value=mock_response,`
- Line 271: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 357: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 489: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 544: `with patch.object(client, "post", return_value=mock_response) as mock_post:`
- Line 552: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_text_completion_unit_tests.py
- Line 40: `from respx import MockRouter`
- Line 134: `patch`
- Line 134: `with patch.object(client, "post", return_value=return_val) as mock_post:`
- Line 142: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_triton.py
- Line 107: `patch`
- Line 195: `patch`
- Line 109: `return_value=mock_response,`
- Line 121: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 197: `return_value=mock_response,`
- Line 213: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_xai.py
- Line 46: `from respx import MockRouter`
- Line 74: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_alangfuse.py
- Line 82: `patch`
- Line 83: `MagicMock`
- Line 83: `"langfuse.Langfuse", MagicMock(return_value=langfuse_client)`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_arize_ai.py
- Line 147: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_azure_content_safety.py
- Line 48: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_azure_openai.py
- Line 59: `from respx import MockRouter`
- Line 113: `return_value=httpx.Response(200, json=obj.model_dump(mode="json"))`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_blocked_user_list.py
- Line 47: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_braintrust.py
- Line 71: `patch`
- Line 93: `patch`
- Line 86: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called()`
- Line 106: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_completion_cost.py
- Line 1157: `patch`
- Line 2677: `MagicMock`
- Line 1169: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_completion_with_retries.py
- Line 100: `patch`
- Line 162: `patch`
- Line 115: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_completion_with_retries\\\\\.assert_called_once()`
- Line 177: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_completion\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_custom_callback_router.py
- Line 728: `patch`
- Line 746: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_embedding.py
- Line 241: `patch`
- Line 398: `patch`
- Line 693: `patch`
- Line 862: `patch`
- Line 907: `patch`
- Line 1008: `patch`
- Line 1047: `patch`
- Line 1069: `patch`
- Line 1093: `patch`
- Line 1187: `patch`
- Line 242: `client, "post", side_effect=_azure_ai_image_mock_response`
- Line 401: `side_effect=_openai_mock_response,`
- Line 693: `with patch.object(client, "post", side_effect=tgi_mock_post) as mock_client:`
- Line 706: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 862: `with patch.object(client, "post", side_effect=mock_wx_embed_request):`
- Line 907: `with patch.object(client, "post", side_effect=mock_async_client) as mock_client:`
- Line 914: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 1031: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 1057: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 1079: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 1110: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 1196: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_exceptions.py
- Line 1048: `patch`
- Line 1123: `patch`
- Line 1206: `patch`
- Line 1051: `side_effect=_return_exception,`
- Line 1126: `side_effect=_return_exception,`
- Line 1209: `side_effect=_return_exception,`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_gcs_bucket.py
- Line 766: `patch`
- Line 777: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_create_file\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_get_llm_provider.py
- Line 167: `patch`
- Line 289: `patch`
- Line 311: `patch`
- Line 335: `patch`
- Line 357: `patch`
- Line 380: `patch`
- Line 403: `patch`
- Line 432: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_get_model_info.py
- Line 126: `patch`
- Line 129: `return_value = None  # TODO: Replace with real object,`
- Line 138: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_health_check.py
- Line 241: `.patch`
- Line 321: `patch`
- Line 371: `patch`
- Line 241: `mocker.patch("websockets.connect", return_value=mock_connect)`
- Line 321: `with patch("litellm.ahealth_check", side_effect=mock_health_check):`
- Line 372: `"litellm.ahealth_check", side_effect=mock_health_check`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_llm_guard.py
- Line 44: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_openai_moderations_hook.py
- Line 41: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_opik.py
- Line 160: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_post.call_count == 10, f"Expected 10 HTTP requests, but got {mock_post\\\\\.call_count}"`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_prometheus.py
- Line 84: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_prometheus_service.py
- Line 187: `patch`
- Line 220: `patch`
- Line 201: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_prometheus_success\\\\\.assert_called_once()`
- Line 236: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_prometheus_failure\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_prompt_injection_detection.py
- Line 38: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_provider_specific_config.py
- Line 490: `patch`
- Line 543: `patch`
- Line 597: `patch`
- Line 492: `return_value=mock_response,`
- Line 498: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 545: `return_value=mock_response,`
- Line 551: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 599: `return_value=mock_response,`
- Line 608: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_budget_limiter.py
- Line 337: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_prometheus.track_provider_remaining_budget\\\\\.assert_called()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_caching.py
- Line 390: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_retries.py
- Line 789: `patch`
- Line 825: `patch`
- Line 801: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_async_function_with_retries\\\\\.assert_called_once()`
- Line 835: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_sagemaker.py
- Line 136: `patch`
- Line 161: `patch`
- Line 311: `patch`
- Line 371: `patch`
- Line 432: `patch`
- Line 488: `patch`
- Line 149: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 174: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 313: `return_value=mock_response,`
- Line 330: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 373: `return_value=mock_response,`
- Line 390: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 434: `return_value=mock_response,`
- Line 451: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 490: `return_value=mock_response,`
- Line 510: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_secret_detect_hook.py
- Line 47: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_text_completion.py
- Line 4182: `patch`
- Line 4237: `patch`
- Line 4183: `client.completions.with_raw_response, "create", side_effect=mock_post`
- Line 4195: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_call\\\\\.assert_called_once()`
- Line 4248: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_call\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_update_spend.py
- Line 47: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_whisper.py
- Line 165: `patch`
- Line 183: `patch`
- Line 170: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_log_pre_call\\\\\.assert_called_once()`
- Line 188: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_log_pre_call\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_assemble_streaming_responses.py
- Line 46: `from respx import MockRouter`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_bedrock_knowledgebase_hook.py
- Line 101: `patch`
- Line 174: `patch`
- Line 222: `patch`
- Line 332: `patch`
- Line 384: `patch`
- Line 121: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 190: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 239: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_client\\\\\.assert_called_once()`
- Line 352: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 404: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_datadog.py
- Line 396: `patch`
- Line 507: `patch`
- Line 587: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_gcs_pub_sub.py
- Line 239: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 294: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_generic_api_callback.py
- Line 106: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`
- Line 184: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langfuse_e2e_test.py
- Line 203: `patch`
- Line 218: `patch`
- Line 236: `patch`
- Line 256: `patch`
- Line 312: `patch`
- Line 373: `patch`
- Line 394: `patch`
- Line 181: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_post\\\\\.call_count >= 1`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langfuse_unit_tests.py
- Line 276: `patch`
- Line 349: `patch`
- Line 279: `return_value=global_logger,`
- Line 308: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_cache.get_cache\\\\\.assert_called_once()`
- Line 371: `).mock(return_value=httpx.Response(200))`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langsmith_unit_test.py
- Line 245: `.patch`
- Line 232: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: logger.async_httpx_client.post\\\\\.assert_called_once()`
- Line 269: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_post\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_opentelemetry_unit_tests.py
- Line 90: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: parent_otel_span.end\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_standard_logging_payload.py
- Line 53: `from create_mock_standard_logging_payload import create_standard_logging_payload, create_standard_logging_payload_with_long_content`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_unit_tests_init_callbacks.py
- Line 198: `patch`
- Line 209: `patch`
- Line 256: `patch`
- Line 259: `patch`
- Line 305: `patch`
- Line 199: `litellm.module_level_client, "get", return_value=mock_response`
- Line 210: `litellm.module_level_client, "get", return_value=mock_response`
- Line 344: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_log_success_event\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/otel_tests/test_e2e_budgeting.py
- Line 40: `call_count = 0`
- Line 42: `while call_count < MAX_CALLS:`
- Line 44: `call_count += 1`
- Line 73: `return call_count`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/pass_through_unit_tests/test_pass_through_unit_tests.py
- Line 288: `patch`
- Line 291: `patch`
- Line 294: `patch`
- Line 355: `patch`
- Line 358: `patch`
- Line 361: `patch`
- Line 293: `return_value=mock_response,`
- Line 296: `return_value=mock_response,`
- Line 360: `return_value=mock_response,`
- Line 363: `return_value=mock_response,`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_admin_ui_tests/test_sso_sign_in.py
- Line 118: `return_value=mock_sso_result`
- Line 190: `return_value=mock_sso_result`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_banned_keyword_list.py
- Line 39: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_proxy_reject_logging.py
- Line 52: `from litellm import Router, mock_completion`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_unit_test_max_model_budget_limiter.py
- Line 116: `patch`
- Line 125: `patch`
- Line 144: `patch`
- Line 117: `budget_limiter, "_get_virtual_key_spend_for_model", return_value=50.0`
- Line 126: `budget_limiter, "_get_virtual_key_spend_for_model", return_value=150.0`
- Line 144: `with patch.object(budget_limiter.dual_cache, "async_get_cache", return_value=50.0):`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_unit_test_proxy_hooks.py
- Line 56: `patch`
- Line 56: `patch`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_endpoints.py
- Line 435: `patch`
- Line 500: `patch`
- Line 407: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_function\\\\\.assert_called_once()`
- Line 453: `router.async_function_with_fallbacks = AsyncMock(return_value=mock_response)`
- Line 467: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: router.async_function_with_fallbacks\\\\\.assert_called_once()`
- Line 519: `return_value={`
- Line 546: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_adapter_completion\\\\\.assert_called_once()`
- Line 560: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: router.async_routing_strategy_pre_call_checks\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_helper_utils.py
- Line 208: `patch`
- Line 227: `patch`
- Line 595: `patch`
- Line 615: `patch`
- Line 599: `side_effect=litellm.RateLimitError(`
- Line 616: `callback, "async_pre_call_check", AsyncMock(side_effect=Exception("Error"))`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_prompt_caching.py
- Line 51: `import unittest`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/tests/test_organizations.py
- Line 149: `.patch`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/archive/root_cleanup/v4_claude_validator/debug_agent_empty_content.py
- Line 96: `call_count = 0`
- Line 98: `nonlocal call_count`
- Line 99: `call_count += 1`
- Line 100: `print(f"\n--- Validation call #{call_count} ---")`

#### /home/graham/workspace/experiments/marker/archive/deprecated_tests/core/processors/test_claude_structure_analyzer.py
- Line 354: `patch`
- Line 363: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_analyze\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/marker/archive/deprecated_tests/test_qa_validation.py
- Line 17: `import unittest`

#### /home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_claude_content_validator.py
- Line 351: `patch`
- Line 361: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_validate\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_claude_image_describer.py
- Line 365: `patch`
- Line 375: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_describe\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/marker/archive/tests/tests/core/services/utils/test_litellm_cache.py
- Line 93: `patch`
- Line 94: `patch`
- Line 135: `patch`
- Line 136: `patch`
- Line 100: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_redis_instance.ping\\\\\.assert_called_once()`
- Line 103: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_enable_cache\\\\\.assert_called_once()`
- Line 142: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_redis_instance.ping\\\\\.assert_called_once()`
- Line 145: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_enable_cache\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/marker/examples/arangodb/search_api/search_api_validator.py
- Line 28: `import unittest`

#### /home/graham/workspace/experiments/marker/examples/arangodb/search_api/test_search_api_diagnostics.py
- Line 51: `import unittest`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_cli.py
- Line 353: `.patch`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_errors.py
- Line 195: `.patch`
- Line 211: `.patch`
- Line 224: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/api.py
- Line 677: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/tests/test_multitask_import.py
- Line 50: `from tests.utils import azure_client_mock, gcs_client_mock, mock_feature_flag, redis_client_mock`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/organizations/api.py
- Line 329: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/projects/api.py
- Line 460: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tasks/api.py
- Line 350: `.patch`
- Line 454: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/conftest.py
- Line 41: `import requests_mock`
- Line 63: `from utils import azure_client_mock, create_business, gcs_client_mock, import_from_url_mock, make_project, ml_backend_mock, redis_client_mock, register_ml_backend_mock, signin`
- Line 323: `.patch`
- Line 338: `.patch`
- Line 700: `.patch`
- Line 711: `.patch`
- Line 732: `.patch`
- Line 745: `.patch`
- Line 758: `.patch`
- Line 323: `mocker.patch('boto3.Session.resource', return_value=mock_s3_resource)`
- Line 338: `mocker.patch('boto3.Session.resource', return_value=mock_s3_resource)`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/data_manager/actions/test_predictions_to_annotations.py
- Line 49: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/data_manager/test_ordering_filters.py
- Line 406: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/data_manager/test_views_api.py
- Line 66: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/io_storages/s3/test_utils.py
- Line 60: `patch`
- Line 78: `patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/ml/test_api.py
- Line 40: `from label_studio.tests.utils import make_project, register_ml_backend_mock`
- Line 59: `.patch`
- Line 153: `.patch`
- Line 163: `.patch`
- Line 211: `.patch`
- Line 281: `.patch`
- Line 297: `.patch`
- Line 59: `mocker.patch('socket.gethostbyname', return_value='321.21.21.21')`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_annotations.py
- Line 32: `import requests_mock`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_config_validation.py
- Line 62: `.patch`
- Line 174: `.patch`
- Line 186: `.patch`
- Line 207: `.patch`
- Line 223: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_contextlog.py
- Line 45: `responses.assert_call_count('https://tele.labelstud.io', 1)`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_core.py
- Line 131: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_endpoints.py
- Line 422: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_exception.py
- Line 53: `.patch`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_next_task.py
- Line 508: `.patch`
- Line 939: `.patch`
- Line 1039: `.patch`
- Line 1138: `.patch`
- Line 1242: `.patch`
- Line 1315: `.patch`
- Line 1333: `.patch`
- Line 508: `mocker.patch.object(Project, 'annotators', return_value=MockAnnotatorCount())`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_predictions.py
- Line 32: `import requests_mock`
- Line 224: `'input_predictions, prediction_call_count, num_project_stats, num_ground_truth_in_stats, '`
- Line 668: `prediction_call_count,`
- Line 715: `assert len(list(filter(lambda h: h.url.endswith('predict'), m.request_history))) == prediction_call_count`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_tasks_upload.py
- Line 34: `import requests_mock`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/utils.py
- Line 39: `import requests_mock`
- Line 87: `.patch`
- Line 106: `.patch`
- Line 184: `.patch`
- Line 256: `.patch`
- Line 257: `.patch`
- Line 269: `.patch`
- Line 461: `.patch`
- Line 184: `with mock.patch.object(google_storage, 'Client', return_value=DummyGCSClient()):`
- Line 256: `with mock.patch.object(models.BlobServiceClient, 'from_connection_string', return_value=DummyAzureClient()):`
- Line 257: `with mock.patch.object(models, 'generate_blob_sas', return_value='token'):`
- Line 269: `with mock.patch.object(RedisStorageMixin, 'get_redis_connection', return_value=redis):`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/webhooks/test_webhooks.py
- Line 40: `import requests_mock`
- Line 156: `.patch`
- Line 308: `.patch`

#### /home/graham/workspace/experiments/marker/src/marker/core/utils/table_cache.py
- Line 319: `call_count_ref = [0]`
- Line 323: `call_count_ref[0] += 1`
- Line 331: `if call_count_ref[0] != 1:`
- Line 332: `all_validation_failures.append(f"Function was called {call_count_ref[0]} times, expected 1")`
- Line 345: `if call_count_ref[0] != 2:`
- Line 346: `all_validation_failures.append(f"Function was called {call_count_ref[0]} times, expected 2")`

#### /home/graham/workspace/experiments/mcp-screenshot/archive/deprecated_tests/test_image_similarity.py
- Line 22: `import unittest`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module.py
- Line 66: `from sparta_mock_data import SPARTAMockAPI`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_real_api.py
- Line 27: `from sparta_mock_data import SPARTAMockAPI`
- Line 40: `from sparta_mock_data import SPARTAMockAPI`
- Line 51: `from sparta_mock_data import SPARTAMockAPI`
- Line 63: `from sparta_mock_data import SPARTAMockAPI`
- Line 74: `from sparta_mock_data import SPARTAMockAPI`
- Line 86: `from sparta_mock_data import SPARTAMockAPI`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_with_mock.py
- Line 22: `from sparta_mock_data import SPARTAMockAPI`

#### /home/graham/workspace/experiments/fine_tuning/archive/deprecated_tests/test_entropy_aware_thinking.py
- Line 58: `patch`
- Line 65: `patch`
- Line 97: `patch`
- Line 120: `patch`
- Line 159: `patch`
- Line 202: `patch`
- Line 217: `patch`
- Line 258: `patch`
- Line 304: `patch`
- Line 173: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_teacher\\\\\.assert_called_once()`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/single_controller/ray/base.py
- Line 447: `patch`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/reward_score/test_sandbox_fusion.py
- Line 383: `patch`
- Line 288: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_call_sandbox_api\\\\\.call_count == 3`
- Line 321: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: assert mock_call_sandbox_api\\\\\.call_count == 3`
- Line 383: `with patch("verl.utils.reward_score.sandbox_fusion.utils.call_sandbox_api", side_effect=curried_mock_api_call) as mock_obj:`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/utils/cpu_tests/test_fs.py
- Line 84: `copy_call_count = 0`
- Line 87: `nonlocal copy_call_count`
- Line 88: `copy_call_count += 1`
- Line 100: `assert copy_call_count == 1`
- Line 104: `assert copy_call_count == 2`
- Line 108: `assert copy_call_count == 2  # Should not increment`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/ray/base.py
- Line 708: `patch`
- Line 759: `patch`

#### /home/graham/workspace/experiments/youtube_transcripts/scripts/remove_mocks_from_tests.py
- Line 105: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: (r'mock_\w+\\\\\\.assert_called.*\n', ''),`
- Line 106: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: (r'assert\s+mock_\w+\\\\\\.call_count.*\n', ''),`

#### /home/graham/workspace/shared_claude_docs/api_gateway/tests/test_middleware.py
- Line 65: `patch`
- Line 370: `patch`
- Line 69: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: mock_logger.info\\\\\.assert_called_once()`

#### /home/graham/workspace/shared_claude_docs/api_gateway/tests/test_rate_limiting.py
- Line 41: `redis_mock.execute = AsyncMock(return_value=[0, 0, 1, 1])`
- Line 307: `return_value=[0, 5, 1, 1]  # removed, count, added, expire`
- Line 329: `return_value=[1, 9]  # allowed, remaining tokens`

#### /home/graham/workspace/shared_claude_docs/project_interactions/contradiction_detection/tests/test_contradiction_detection.py
- Line 14: `import unittest`

#### /home/graham/workspace/shared_claude_docs/project_interactions/granger_verify_phase1.py
- Line 212: `(r'assert_called', 'assert_called'),`
- Line 213: `(r'call_count', 'call_count'),`
- Line 802: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: r'\\\\\\.assert_called',`
- Line 805: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: r'\\\\\\.call_count',`
- Line 876: `f.write("@patch('requests.get')\n")`

#### /home/graham/workspace/shared_claude_docs/project_interactions/graphql-schema-generator/graphql_schema_generator_interaction.py
- Line 82: `patch`
- Line 88: `patch`

#### /home/graham/workspace/shared_claude_docs/project_interactions/service_mesh_manager/tests/test_security_policies.py
- Line 153: `patch`
- Line 154: `patch`
- Line 155: `patch`
- Line 157: `patch`

#### /home/graham/workspace/shared_claude_docs/project_interactions/sparta_arangodb_compliance/tests/test_task_018_compliance.py
- Line 32: `from compliance_mapping_interaction import ComplianceMapper, ComplianceFramework, SecurityControl, ComplianceRequirement, MockSpartaData`

#### /home/graham/workspace/shared_claude_docs/tests/granger_interaction_tests/verify_granger_understanding.py
- Line 28: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count = 0`
- Line 32: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: self\\\\\.call_count += 1`
- Line 38: `# MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: # MOCK REMOVED: "call_number": self\\\\\.call_count`

### Relative Imports (2918 instances)

Convert to absolute imports:


#### /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/validate_call_decorator.py
- Line 20: `from ._internal import ...`
- Line 21: `from .errors import ...`
- Line 26: `from .config import ...`

#### /home/graham/workspace/experiments/aider-daemon/benchmark/__init__.py
- Line 5: `from .problem_stats import ...`
- Line 6: `from .plots import ...`
- Line 7: `from . import ...`
- Line 8: `from .benchmark import ...`
- Line 9: `from .refactor_tools import ...`
- Line 10: `from .over_time import ...`
- Line 11: `from .rungrid import ...`
- Line 12: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/__main__.py
- Line 1: `from .main import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/args.py
- Line 19: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/args_formatter.py
- Line 5: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/__init__.py
- Line 1: `from .architect_coder import ...`
- Line 2: `from .ask_coder import ...`
- Line 3: `from .base_coder import ...`
- Line 4: `from .context_coder import ...`
- Line 5: `from .editblock_coder import ...`
- Line 6: `from .editblock_fenced_coder import ...`
- Line 7: `from .editor_diff_fenced_coder import ...`
- Line 8: `from .editor_editblock_coder import ...`
- Line 9: `from .editor_whole_coder import ...`
- Line 10: `from .help_coder import ...`
- Line 11: `from .patch_coder import ...`
- Line 12: `from .udiff_coder import ...`
- Line 13: `from .udiff_simple import ...`
- Line 14: `from .wholefile_coder import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/architect_coder.py
- Line 1: `from .architect_prompts import ...`
- Line 2: `from .ask_coder import ...`
- Line 3: `from .base_coder import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/architect_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/ask_coder.py
- Line 1: `from .ask_prompts import ...`
- Line 2: `from .base_coder import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/ask_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/base_coder.py
- Line 52: `from ..dump import ...`
- Line 53: `from .chat_chunks import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/context_coder.py
- Line 1: `from .base_coder import ...`
- Line 2: `from .context_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/context_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_coder.py
- Line 10: `from ..dump import ...`
- Line 11: `from .base_coder import ...`
- Line 12: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_fenced_coder.py
- Line 1: `from ..dump import ...`
- Line 2: `from .editblock_coder import ...`
- Line 3: `from .editblock_fenced_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_fenced_prompts.py
- Line 3: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .editblock_coder import ...`
- Line 6: `from .editblock_func_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editblock_prompts.py
- Line 3: `from . import ...`
- Line 4: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_diff_fenced_coder.py
- Line 1: `from .editblock_fenced_coder import ...`
- Line 2: `from .editor_diff_fenced_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_diff_fenced_prompts.py
- Line 3: `from .editblock_fenced_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_editblock_coder.py
- Line 1: `from .editblock_coder import ...`
- Line 2: `from .editor_editblock_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_editblock_prompts.py
- Line 3: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_whole_coder.py
- Line 1: `from .editor_whole_prompts import ...`
- Line 2: `from .wholefile_coder import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/editor_whole_prompts.py
- Line 3: `from .wholefile_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/help_coder.py
- Line 1: `from ..dump import ...`
- Line 2: `from .base_coder import ...`
- Line 3: `from .help_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/help_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/patch_coder.py
- Line 6: `from .base_coder import ...`
- Line 7: `from .patch_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/patch_prompts.py
- Line 3: `from .base_prompts import ...`
- Line 4: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/single_wholefile_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .single_wholefile_func_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/single_wholefile_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/udiff_coder.py
- Line 5: `from ..dump import ...`
- Line 6: `from .base_coder import ...`
- Line 7: `from .search_replace import ...`
- Line 14: `from .udiff_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/udiff_prompts.py
- Line 3: `from . import ...`
- Line 4: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/udiff_simple.py
- Line 1: `from .udiff_coder import ...`
- Line 2: `from .udiff_simple_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/udiff_simple_prompts.py
- Line 1: `from .udiff_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/wholefile_coder.py
- Line 5: `from ..dump import ...`
- Line 6: `from .base_coder import ...`
- Line 7: `from .wholefile_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/wholefile_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .wholefile_func_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/wholefile_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/coders/wholefile_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/commands.py
- Line 27: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/diffs.py
- Line 4: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/io.py
- Line 38: `from .dump import ...`
- Line 39: `from .editor import ...`
- Line 40: `from .utils import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/main.py
- Line 40: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/repo.py
- Line 23: `from .dump import ...`
- Line 24: `from .waiting import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/aider/voice.py
- Line 12: `from .dump import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/benchmark/__init__.py
- Line 5: `from .problem_stats import ...`
- Line 6: `from .plots import ...`
- Line 7: `from . import ...`
- Line 8: `from .benchmark import ...`
- Line 9: `from .refactor_tools import ...`
- Line 10: `from .over_time import ...`
- Line 11: `from .rungrid import ...`
- Line 12: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/__init__.py
- Line 5: `from .test_run_cmd import ...`
- Line 6: `from .test_history import ...`
- Line 7: `from .test_analytics import ...`
- Line 8: `from . import ...`
- Line 9: `from .test_urls import ...`
- Line 10: `from . import ...`
- Line 11: `from . import ...`
- Line 12: `from . import ...`
- Line 13: `from . import ...`
- Line 14: `from . import ...`
- Line 15: `from . import ...`
- Line 16: `from . import ...`
- Line 17: `from . import ...`
- Line 18: `from . import ...`
- Line 19: `from . import ...`
- Line 20: `from . import ...`
- Line 21: `from .test_watch import ...`
- Line 22: `from . import ...`
- Line 23: `from .test_exceptions import ...`
- Line 24: `from .test_openrouter import ...`
- Line 25: `from . import ...`
- Line 26: `from . import ...`
- Line 27: `from . import ...`
- Line 28: `from .test_find_or_blocks import ...`
- Line 29: `from . import ...`
- Line 30: `from . import ...`
- Line 31: `from . import ...`
- Line 32: `from . import ...`
- Line 33: `from .test_special import ...`
- Line 34: `from . import ...`
- Line 35: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/__init__.py
- Line 7: `from .core import ...`
- Line 8: `from .cli import ...`
- Line 9: `from .session_manager import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/agents/open_source_agent.py
- Line 33: `from .base_agent import ...`
- Line 34: `from ..core.circuit_breaker import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/cli/app.py
- Line 25: `from ..core import ...`
- Line 26: `from ..core.uvloop_integration import ...`
- Line 38: `from .granger_slash_mcp_mixin import ...`
- Line 66: `from ..ui.terminal_integration import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/cli/claude_cli.py
- Line 19: `from ..core.session_manager_v2 import ...`
- Line 20: `from ..core.config_manager import ...`
- Line 21: `from ..core.output_formatter import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/cached_session_manager.py
- Line 29: `from .session_manager import ...`
- Line 30: `from .session_cache import ...`
- Line 31: `from .storage import ...`
- Line 32: `from .storage.factory import ...`
- Line 33: `from .storage.sqlite_backend import ...`
- Line 34: `from .storage.memory_backend import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/code_generator.py
- Line 27: `from .module_system import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/enhanced_session_manager.py
- Line 22: `from .session_manager_v2 import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/module_system.py
- Line 25: `from .circuit_breaker import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/progress_tracker.py
- Line 25: `from .simple_progress_tracker import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/session_operations.py
- Line 13: `from ..core.session_manager import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/simple_daemon.py
- Line 10: `from .session_manager import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/storage/arangodb_backend.py
- Line 51: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/storage/factory.py
- Line 14: `from . import ...`
- Line 15: `from .sqlite_backend import ...`
- Line 16: `from .memory_backend import ...`
- Line 20: `from .arangodb_backend import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/storage/memory_backend.py
- Line 16: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/storage/sqlite_backend.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/validation_pipeline.py
- Line 20: `from .circuit_breaker import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/mcp/aider_daemon_prompts.py
- Line 12: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/mcp/server.py
- Line 19: `from ..core.simple_daemon import ...`
- Line 20: `from ..core.session_manager import ...`

#### /home/graham/workspace/experiments/aider-daemon/tests/__init__.py
- Line 5: `from .conftest import ...`
- Line 6: `from .test_honeypot import ...`
- Line 7: `from .test_basic import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/active_learning/learner.py
- Line 25: `from . import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/__init__.py
- Line 9: `from .app import ...`
- Line 10: `from .routes import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/app.py
- Line 9: `from .routes import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/routes/__init__.py
- Line 9: `from .annotation import ...`
- Line 10: `from .pdf import ...`
- Line 11: `from .session import ...`
- Line 12: `from .frontend import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/routes/annotation.py
- Line 13: `from ...core import ...`
- Line 38: `from .session import ...`
- Line 63: `from .session import ...`
- Line 80: `from .session import ...`
- Line 111: `from .session import ...`
- Line 134: `from .session import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/routes/pdf.py
- Line 19: `from ...storage import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/api/routes/session.py
- Line 17: `from ...core import ...`
- Line 18: `from ...storage import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/cli.py
- Line 201: `from .api import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/rl/__init__.py
- Line 10: `from .rewards import ...`
- Line 11: `from .episodes import ...`
- Line 12: `from .ollama_integration import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/rl/episodes.py
- Line 15: `from .rewards import ...`

#### /home/graham/workspace/experiments/annotator/src/annotator/rl/ollama_integration.py
- Line 16: `from .episodes import ...`

#### /home/graham/workspace/experiments/arangodb/archive/pre_refactor/memory_agent/__init__.py
- Line 16: `from .memory_agent import ...`

#### /home/graham/workspace/experiments/arangodb/archive/pre_refactor/memory_agent/memory_agent_validator.py
- Line 100: `from .memory_agent import ...`

#### /home/graham/workspace/experiments/arangodb/archive/src/core/arango_setup_updated.py
- Line 33: `from .utils.dependency_checker import ...`
- Line 122: `from ..constants import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/__init__.py
- Line 15: `from .graphiti import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/cross_encoder/__init__.py
- Line 18: `from .client import ...`
- Line 19: `from .openai_reranker_client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/cross_encoder/openai_reranker_client.py
- Line 26: `from ..helpers import ...`
- Line 27: `from ..llm_client import ...`
- Line 28: `from ..prompts import ...`
- Line 29: `from .client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/embedder/__init__.py
- Line 18: `from .client import ...`
- Line 19: `from .openai import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/embedder/gemini.py
- Line 24: `from .client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/embedder/openai.py
- Line 23: `from .client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/embedder/voyage.py
- Line 23: `from .client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/__init__.py
- Line 18: `from .client import ...`
- Line 19: `from .config import ...`
- Line 20: `from .errors import ...`
- Line 21: `from .openai_client import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/anthropic_client.py
- Line 31: `from ..prompts.models import ...`
- Line 32: `from .client import ...`
- Line 33: `from .config import ...`
- Line 34: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/client.py
- Line 29: `from ..prompts.models import ...`
- Line 30: `from .config import ...`
- Line 31: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/gemini_client.py
- Line 26: `from ..prompts.models import ...`
- Line 27: `from .client import ...`
- Line 28: `from .config import ...`
- Line 29: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/groq_client.py
- Line 27: `from ..prompts.models import ...`
- Line 28: `from .client import ...`
- Line 29: `from .config import ...`
- Line 30: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/openai_client.py
- Line 28: `from ..prompts.models import ...`
- Line 29: `from .client import ...`
- Line 30: `from .config import ...`
- Line 31: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/llm_client/openai_generic_client.py
- Line 29: `from ..prompts.models import ...`
- Line 30: `from .client import ...`
- Line 31: `from .config import ...`
- Line 32: `from .errors import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/__init__.py
- Line 15: `from .lib import ...`
- Line 16: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/dedupe_edges.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/dedupe_nodes.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/eval.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/extract_edge_dates.py
- Line 22: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/extract_edges.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/extract_nodes.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/invalidate_edges.py
- Line 22: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/lib.py
- Line 17: `from .dedupe_edges import ...`
- Line 18: `from .dedupe_edges import ...`
- Line 19: `from .dedupe_edges import ...`
- Line 20: `from .dedupe_nodes import ...`
- Line 21: `from .dedupe_nodes import ...`
- Line 22: `from .dedupe_nodes import ...`
- Line 23: `from .eval import ...`
- Line 24: `from .eval import ...`
- Line 25: `from .eval import ...`
- Line 26: `from .extract_edge_dates import ...`
- Line 27: `from .extract_edge_dates import ...`
- Line 28: `from .extract_edge_dates import ...`
- Line 29: `from .extract_edges import ...`
- Line 30: `from .extract_edges import ...`
- Line 31: `from .extract_edges import ...`
- Line 32: `from .extract_nodes import ...`
- Line 33: `from .extract_nodes import ...`
- Line 34: `from .extract_nodes import ...`
- Line 35: `from .invalidate_edges import ...`
- Line 36: `from .invalidate_edges import ...`
- Line 37: `from .invalidate_edges import ...`
- Line 38: `from .models import ...`
- Line 39: `from .prompt_helpers import ...`
- Line 40: `from .summarize_nodes import ...`
- Line 41: `from .summarize_nodes import ...`
- Line 42: `from .summarize_nodes import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/prompts/summarize_nodes.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/graphiti_core/utils/maintenance/__init__.py
- Line 15: `from .edge_operations import ...`
- Line 16: `from .graph_data_operations import ...`
- Line 17: `from .node_operations import ...`

#### /home/graham/workspace/experiments/arangodb/repos/graphiti/server/graph_service/dto/__init__.py
- Line 15: `from .common import ...`
- Line 16: `from .ingest import ...`
- Line 17: `from .retrieve import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/__init__.py
- Line 28: `from .core.arango_setup import ...`
- Line 29: `from .core.utils.config_validator import ...`
- Line 30: `from .core.db_connection_wrapper import ...`
- Line 31: `from .core.db_operations import ...`
- Line 51: `from .core.memory import ...`
- Line 58: `from .core.search import ...`
- Line 68: `from .core.graph import ...`
- Line 75: `from .core.models import ...`
- Line 82: `from .qa_generation import ...`
- Line 89: `from .visualization import ...`
- Line 95: `from .dashboard import ...`
- Line 98: `from .mcp import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/__main__.py
- Line 13: `from .main import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/contradiction_commands.py
- Line 34: `from .db_connection import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/episode_commands.py
- Line 29: `from .db_connection import ...`
- Line 30: `from ..core.memory.episode_manager import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/example/__init__.py
- Line 11: `from .cli_command import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/sparta_commands.py
- Line 18: `from ..visualization.sparta import ...`
- Line 23: `from ..visualization.sparta.sparta_data_enhanced import ...`
- Line 27: `from ..visualization.sparta.matrix_generator_v0 import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/cli/visualization_commands.py
- Line 23: `from ..visualization.core.d3_engine import ...`
- Line 24: `from ..visualization.core.data_transformer import ...`
- Line 25: `from ..visualization.core.table_engine import ...`
- Line 26: `from ..core.arango_setup import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/arango_setup.py
- Line 43: `from .utils.dependency_checker import ...`
- Line 132: `from ..constants import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/context_generator.py
- Line 13: `from .db_connection_wrapper import ...`
- Line 14: `from .llm_utils import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/db_connection_wrapper.py
- Line 10: `from .arango_setup import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/db_operations.py
- Line 778: `from .arango_setup import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/graph/__init__.py
- Line 18: `from .enhanced_relationships import ...`
- Line 24: `from ..db_operations import ...`
- Line 30: `from ..search.graph_traverse import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/graph/contradiction_detection.py
- Line 45: `from .enhanced_relationships import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/graph/enhanced_relationships.py
- Line 29: `from ..db_operations import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/graph/entity_resolution.py
- Line 47: `from ..utils.embedding_utils import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/graph/relationship_extraction.py
- Line 44: `from .enhanced_relationships import ...`
- Line 48: `from ..utils.embedding_utils import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/memory/__init__.py
- Line 19: `from .memory_agent import ...`
- Line 20: `from .episode_manager import ...`
- Line 21: `from .contradiction_logger import ...`
- Line 22: `from .message_history_config import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/memory/improved_error_handling.py
- Line 10: `from ..utils.error_handler import ...`
- Line 44: `from ..utils.embedding_utils import ...`
- Line 150: `from ..utils.embedding_utils import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/memory/memory_commands.py
- Line 20: `from .memory_agent import ...`
- Line 21: `from ..constants import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/search/__init__.py
- Line 21: `from .bm25_search import ...`
- Line 22: `from .semantic_search import ...`
- Line 23: `from .hybrid_search import ...`
- Line 24: `from .cross_encoder_reranking import ...`
- Line 30: `from .tag_search import ...`
- Line 31: `from .graph_traverse import ...`
- Line 32: `from .keyword_search import ...`
- Line 33: `from .glossary_search import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/utils/config_validator.py
- Line 16: `from ..utils.error_handler import ...`
- Line 337: `from ..constants import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/core/utils/enhanced_validation_tracker.py
- Line 38: `from .test_reporter import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/dashboard/__init__.py
- Line 21: `from .manager import ...`
- Line 22: `from .config import ...`
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/dashboard/config.py
- Line 22: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/dashboard/manager.py
- Line 24: `from .models import ...`
- Line 25: `from .config import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/mcp/arangodb_prompts.py
- Line 16: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/mcp/server.py
- Line 10: `from .arangodb_prompts import ...`
- Line 11: `from .prompts import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/__init__.py
- Line 14: `from .generator import ...`
- Line 15: `from .generator_marker_aware import ...`
- Line 16: `from .models import ...`
- Line 22: `from .validator import ...`
- Line 23: `from .exporter import ...`
- Line 24: `from .validation_models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/cli.py
- Line 34: `from .review_cli import ...`
- Line 50: `from .edge_generator import ...`
- Line 51: `from .enrichment import ...`
- Line 52: `from .exporter import ...`
- Line 93: `from ..core.db_operations import ...`
- Line 94: `from .generator import ...`
- Line 95: `from .exporter import ...`
- Line 130: `from .generator_marker_aware import ...`
- Line 131: `from .generator import ...`
- Line 132: `from ..core.db_operations import ...`
- Line 596: `from ..core.db_connection_wrapper import ...`
- Line 598: `from .models import ...`
- Line 722: `from ..core.db_connection_wrapper import ...`
- Line 784: `from ..core.db_connection_wrapper import ...`
- Line 885: `from ..qa.marker_connector import ...`
- Line 887: `from ..core.arango_setup import ...`
- Line 922: `from ..qa.exporter import ...`
- Line 980: `from ..qa.marker_connector import ...`
- Line 982: `from ..core.arango_setup import ...`
- Line 1042: `from ..qa.exporter import ...`
- Line 1120: `from ..core.db_operations import ...`
- Line 1121: `from .models import ...`
- Line 1206: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/edge_generator.py
- Line 17: `from .models import ...`
- Line 18: `from ..core.db_connection_wrapper import ...`
- Line 19: `from ..core.constants import ...`
- Line 20: `from ..core.field_constants import ...`
- Line 24: `from ..core.utils.embedding_utils import ...`
- Line 25: `from ..core.graph.entity_resolution import ...`
- Line 26: `from ..core.graph.relationship_extraction import ...`
- Line 27: `from ..core.search.bm25_search import ...`
- Line 28: `from ..core.temporal_operations import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/exporter.py
- Line 19: `from .models import ...`
- Line 20: `from ..core.context_generator import ...`
- Line 649: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/generate_sample_data.py
- Line 17: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/generator.py
- Line 21: `from .models import ...`
- Line 28: `from .validator import ...`
- Line 29: `from .validation_models import ...`
- Line 30: `from .reversal_generator import ...`
- Line 31: `from ..core.db_connection_wrapper import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/generator_marker_aware.py
- Line 17: `from .generator import ...`
- Line 18: `from .models import ...`
- Line 25: `from .validator import ...`
- Line 26: `from ..core.db_connection_wrapper import ...`
- Line 346: `from .exporter import ...`
- Line 366: `from ..core.db_connection_wrapper import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/reversal_generator.py
- Line 14: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/review_cli.py
- Line 25: `from ..core.db_connection_wrapper import ...`
- Line 26: `from ..core.constants import ...`
- Line 27: `from .edge_generator import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/unsloth_cli.py
- Line 20: `from .exporter import ...`
- Line 21: `from .models import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/validator.py
- Line 14: `from .models import ...`
- Line 15: `from ..core.db_connection_wrapper import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/qa_generation/verify_exporter.py
- Line 18: `from .test_utils import ...`
- Line 30: `from .models import ...`
- Line 31: `from .exporter import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/__init__.py
- Line 13: `from .core.d3_engine import ...`
- Line 14: `from .core.data_transformer import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/core/__init__.py
- Line 8: `from .d3_engine import ...`
- Line 9: `from .data_transformer import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/core/d3_engine.py
- Line 31: `from .llm_recommender import ...`
- Line 39: `from .performance_optimizer import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/core/table_engine.py
- Line 25: `from ...core.constants import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/server/__init__.py
- Line 8: `from .visualization_server import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/server/visualization_server.py
- Line 32: `from ..core.d3_engine import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/sparta/__init__.py
- Line 9: `from .sparta_data import ...`
- Line 10: `from .threat_calculator import ...`
- Line 11: `from .matrix_generator import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/sparta/matrix_generator.py
- Line 11: `from .sparta_data import ...`
- Line 12: `from .threat_calculator import ...`

#### /home/graham/workspace/experiments/arangodb/src/arangodb/visualization/sparta/matrix_generator_v0.py
- Line 12: `from .sparta_data import ...`
- Line 13: `from .threat_calculator import ...`

#### /home/graham/workspace/experiments/chat/backend/api/__init__.py
- Line 5: `from .mcp_client import ...`
- Line 6: `from .websocket_manager import ...`
- Line 7: `from .chat_handler import ...`

#### /home/graham/workspace/experiments/chat/backend/api/core/__init__.py
- Line 4: `from .plugin_base import ...`
- Line 5: `from .plugin_registry import ...`
- Line 6: `from .config_loader import ...`

#### /home/graham/workspace/experiments/chat/backend/api/core/plugin_loader.py
- Line 10: `from .plugin_base import ...`
- Line 11: `from .plugin_registry import ...`
- Line 12: `from .config_loader import ...`

#### /home/graham/workspace/experiments/chat/backend/api/core/plugin_registry.py
- Line 8: `from .plugin_base import ...`

#### /home/graham/workspace/experiments/chat/backend/api/integrations/__init__.py
- Line 2: `from .chat_module import ...`

#### /home/graham/workspace/experiments/chat/backend/api/main.py
- Line 10: `from .websocket_manager import ...`
- Line 11: `from .mcp_client import ...`
- Line 12: `from .core import ...`
- Line 13: `from .core.plugin_loader import ...`
- Line 15: `from .chat_handler import ...`

#### /home/graham/workspace/experiments/chat/backend/dashboard/__init__.py
- Line 11: `from .routes import ...`

#### /home/graham/workspace/experiments/chat/backend/dashboard/d3/__init__.py
- Line 8: `from .graph_transformer import ...`
- Line 9: `from .traversal import ...`
- Line 10: `from .realtime import ...`

#### /home/graham/workspace/experiments/chat/backend/dashboard/d3/realtime.py
- Line 27: `from .graph_transformer import ...`

#### /home/graham/workspace/experiments/chat/backend/dashboard/learning_curves.py
- Line 60: `from .database import ...`

#### /home/graham/workspace/experiments/chat/backend/dashboard/routes.py
- Line 32: `from .database import ...`
- Line 33: `from .models import ...`
- Line 238: `from .learning_curves import ...`

#### /home/graham/workspace/experiments/chat/chat/integrations/__init__.py
- Line 2: `from .chat_module import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/__init__.py
- Line 18: `from .llm_test_analyzer import ...`
- Line 19: `from .mock_detector import ...`
- Line 20: `from .realtime_monitor import ...`
- Line 21: `from .implementation_verifier import ...`
- Line 22: `from .honeypot_enforcer import ...`
- Line 23: `from .pattern_analyzer import ...`
- Line 24: `from .claim_verifier import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/comprehensive_analyzer.py
- Line 44: `from .mock_detector import ...`
- Line 45: `from .realtime_monitor import ...`
- Line 46: `from .implementation_verifier import ...`
- Line 47: `from .honeypot_enforcer import ...`
- Line 48: `from .integration_tester import ...`
- Line 49: `from .pattern_analyzer import ...`
- Line 50: `from .claim_verifier import ...`
- Line 51: `from .hallucination_monitor import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/adapters/__init__.py
- Line 18: `from .agent_report_adapter import ...`
- Line 19: `from .test_reporter import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/code_reviewer.py
- Line 25: `from .git_reviewer import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/__init__.py
- Line 18: `from .universal_report_generator import ...`
- Line 19: `from .simple_html_reporter import ...`
- Line 21: `from .enhanced_multi_project_dashboard import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/runners/__init__.py
- Line 18: `from .pytest_report_runner import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/test_reporter.py
- Line 23: `from .generators.html_generator import ...`
- Line 24: `from .generators.markdown_generator import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/tracking/__init__.py
- Line 18: `from .test_history_tracker import ...`

#### /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/monitoring/__init__.py
- Line 18: `from .hallucination_monitor import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/cli/app.py
- Line 21: `from .granger_slash_mcp_mixin import ...`
- Line 22: `from .formatters import ...`
- Line 31: `from .validators import ...`
- Line 32: `from ..core.darpa_module import ...`
- Line 33: `from ..logger import ...`
- Line 268: `from ..core.polling_system import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/__init__.py
- Line 9: `from .darpa_module import ...`
- Line 10: `from .polling_system import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/analysis/research_integration.py
- Line 23: `from ..database.database import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/analysis/rl_optimizer.py
- Line 9: `from .rl_integration import ...`
- Line 28: `from .analysis.granger_capability_analyzer import ...`
- Line 37: `from .analysis.granger_capability_analyzer import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/darpa_module.py
- Line 16: `from .scrapers.sam_gov import ...`
- Line 17: `from .scrapers.darpa_catalog import ...`
- Line 18: `from .database.database_adapter import ...`
- Line 19: `from .proposals.proposal_generator_enhanced import ...`
- Line 20: `from .analysis.granger_capability_analyzer_enhanced import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/arango_operations.py
- Line 40: `from .models import ...`
- Line 41: `from .arango_connection import ...`
- Line 272: `from .arango_connection import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/arango_search.py
- Line 36: `from .arango_connection import ...`
- Line 328: `from .arango_connection import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/database.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/database_adapter.py
- Line 38: `from .database_factory import ...`
- Line 62: `from ..database.models import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/database_arango.py
- Line 37: `from .database_adapter import ...`
- Line 38: `from .models import ...`
- Line 39: `from .arango_connection import ...`
- Line 40: `from .arango_operations import ...`
- Line 41: `from .arango_search import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/database_bm25.py
- Line 30: `from .models import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/database_factory.py
- Line 22: `from .database import ...`
- Line 23: `from .database_bm25 import ...`
- Line 103: `from .database_arango import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/polling_system.py
- Line 28: `from .database.database_factory import ...`
- Line 29: `from .scrapers.sam_gov import ...`
- Line 30: `from .scrapers.darpa_catalog import ...`
- Line 31: `from .analysis.granger_capability_analyzer_enhanced import ...`
- Line 32: `from .analysis.rl_optimizer import ...`
- Line 33: `from .proposals.proposal_generator_enhanced import ...`
- Line 34: `from .analysis.research_integration import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/proposals/proposal_generator.py
- Line 32: `from .proposal_sections import ...`
- Line 40: `from .research_gatherer import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/proposals/proposal_generator_enhanced.py
- Line 22: `from ..analysis.granger_capability_analyzer_enhanced import ...`
- Line 23: `from ..analysis.research_integration import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/proposals/proposal_generator_legacy.py
- Line 23: `from .analysis.granger_capability_analyzer import ...`
- Line 24: `from .analysis.research_integration import ...`
- Line 25: `from .database.database import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/scrapers/darpa_catalog.py
- Line 24: `from ..database.models import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/scrapers/darpa_catalog_enhanced.py
- Line 27: `from ..database.models import ...`
- Line 28: `from .darpa_catalog import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/scrapers/darpa_catalog_sparta.py
- Line 36: `from ..database.models import ...`
- Line 37: `from .darpa_catalog import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/scrapers/sam_gov.py
- Line 42: `from ..database.models import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/mcp/darpa_crawl_prompts.py
- Line 22: `from .prompts import ...`
- Line 25: `from .prompts_required import ...`
- Line 33: `from .prompts_domain import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/mcp/prompts_domain.py
- Line 21: `from .prompts import ...`
- Line 336: `from .prompts import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/mcp/prompts_required.py
- Line 21: `from .prompts import ...`

#### /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/mcp/server.py
- Line 21: `from ..core.database.database_adapter import ...`
- Line 22: `from ..core.scrapers.sam_gov import ...`
- Line 23: `from ..core.scrapers.darpa_catalog import ...`
- Line 24: `from ..core.analysis.granger_capability_analyzer import ...`
- Line 25: `from ..core.analysis.rl_optimizer import ...`
- Line 26: `from ..core.proposals.proposal_generator import ...`
- Line 27: `from ..core.analysis.research_integration import ...`
- Line 28: `from ..core.polling_system import ...`
- Line 29: `from ..logger import ...`

#### /home/graham/workspace/experiments/gitget/examples/workflows/__init__.py
- Line 8: `from .gitget_to_marker import ...`
- Line 9: `from .gitget_to_arangodb import ...`
- Line 10: `from .combined_analysis import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/cache/__init__.py
- Line 10: `from .repository_cache import ...`
- Line 11: `from .cache_manager import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/cli/commands.py
- Line 23: `from .granger_slash_mcp_mixin import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/cli/slash_commands/__init__.py
- Line 6: `from .commands import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/core/__init__.py
- Line 21: `from .renderers import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/core/renderers/__init__.py
- Line 10: `from .base import ...`
- Line 11: `from .json_renderer import ...`
- Line 12: `from .arangodb import ...`
- Line 13: `from .markdown import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/integrations/__init__.py
- Line 10: `from .gitget_module import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/mcp/__init__.py
- Line 10: `from .server import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/mcp/gitget_prompts.py
- Line 9: `from .prompts import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/performance/__init__.py
- Line 6: `from .parallel_processor import ...`
- Line 7: `from .stream_processor import ...`
- Line 8: `from .memory_monitor import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/schema/__init__.py
- Line 10: `from .unified_code import ...`

#### /home/graham/workspace/experiments/gitget/src/gitget/security/__init__.py
- Line 6: `from .url_validator import ...`
- Line 7: `from .resource_limiter import ...`
- Line 8: `from .auth_manager import ...`
- Line 9: `from .security_logger import ...`

#### /home/graham/workspace/experiments/granger_hub/archive/schema_negotiator_dynamic.py
- Line 20: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/granger_hub/archive/slash_commands.py
- Line 27: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/__main__.py
- Line 1: `from .main import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/args.py
- Line 19: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/args_formatter.py
- Line 5: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/__init__.py
- Line 1: `from .architect_coder import ...`
- Line 2: `from .ask_coder import ...`
- Line 3: `from .base_coder import ...`
- Line 4: `from .context_coder import ...`
- Line 5: `from .editblock_coder import ...`
- Line 6: `from .editblock_fenced_coder import ...`
- Line 7: `from .editor_diff_fenced_coder import ...`
- Line 8: `from .editor_editblock_coder import ...`
- Line 9: `from .editor_whole_coder import ...`
- Line 10: `from .help_coder import ...`
- Line 11: `from .patch_coder import ...`
- Line 12: `from .udiff_coder import ...`
- Line 13: `from .udiff_simple import ...`
- Line 14: `from .wholefile_coder import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/architect_coder.py
- Line 1: `from .architect_prompts import ...`
- Line 2: `from .ask_coder import ...`
- Line 3: `from .base_coder import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/architect_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/ask_coder.py
- Line 1: `from .ask_prompts import ...`
- Line 2: `from .base_coder import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/ask_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/base_coder.py
- Line 52: `from ..dump import ...`
- Line 53: `from .chat_chunks import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/context_coder.py
- Line 1: `from .base_coder import ...`
- Line 2: `from .context_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/context_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_coder.py
- Line 10: `from ..dump import ...`
- Line 11: `from .base_coder import ...`
- Line 12: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_fenced_coder.py
- Line 1: `from ..dump import ...`
- Line 2: `from .editblock_coder import ...`
- Line 3: `from .editblock_fenced_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_fenced_prompts.py
- Line 3: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .editblock_coder import ...`
- Line 6: `from .editblock_func_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editblock_prompts.py
- Line 3: `from . import ...`
- Line 4: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_diff_fenced_coder.py
- Line 1: `from .editblock_fenced_coder import ...`
- Line 2: `from .editor_diff_fenced_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_diff_fenced_prompts.py
- Line 3: `from .editblock_fenced_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_editblock_coder.py
- Line 1: `from .editblock_coder import ...`
- Line 2: `from .editor_editblock_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_editblock_prompts.py
- Line 3: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_whole_coder.py
- Line 1: `from .editor_whole_prompts import ...`
- Line 2: `from .wholefile_coder import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/editor_whole_prompts.py
- Line 3: `from .wholefile_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/help_coder.py
- Line 1: `from ..dump import ...`
- Line 2: `from .base_coder import ...`
- Line 3: `from .help_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/help_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/patch_coder.py
- Line 6: `from .base_coder import ...`
- Line 7: `from .patch_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/patch_prompts.py
- Line 3: `from .base_prompts import ...`
- Line 4: `from .editblock_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/single_wholefile_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .single_wholefile_func_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/single_wholefile_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/udiff_coder.py
- Line 5: `from ..dump import ...`
- Line 6: `from .base_coder import ...`
- Line 7: `from .search_replace import ...`
- Line 14: `from .udiff_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/udiff_prompts.py
- Line 3: `from . import ...`
- Line 4: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/udiff_simple.py
- Line 1: `from .udiff_coder import ...`
- Line 2: `from .udiff_simple_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/udiff_simple_prompts.py
- Line 1: `from .udiff_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/wholefile_coder.py
- Line 5: `from ..dump import ...`
- Line 6: `from .base_coder import ...`
- Line 7: `from .wholefile_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/wholefile_func_coder.py
- Line 3: `from ..dump import ...`
- Line 4: `from .base_coder import ...`
- Line 5: `from .wholefile_func_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/wholefile_func_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/coders/wholefile_prompts.py
- Line 3: `from .base_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/commands.py
- Line 27: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/diffs.py
- Line 4: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/io.py
- Line 38: `from .dump import ...`
- Line 39: `from .editor import ...`
- Line 40: `from .utils import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/main.py
- Line 40: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/repo.py
- Line 23: `from .dump import ...`
- Line 24: `from .waiting import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/aider/voice.py
- Line 12: `from .dump import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/benchmark/__init__.py
- Line 5: `from .problem_stats import ...`
- Line 6: `from .plots import ...`
- Line 7: `from . import ...`
- Line 8: `from .benchmark import ...`
- Line 9: `from .refactor_tools import ...`
- Line 10: `from .over_time import ...`
- Line 11: `from .rungrid import ...`
- Line 12: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/__init__.py
- Line 5: `from .test_run_cmd import ...`
- Line 6: `from . import ...`
- Line 7: `from .test_analytics import ...`
- Line 8: `from . import ...`
- Line 9: `from .test_urls import ...`
- Line 10: `from . import ...`
- Line 11: `from . import ...`
- Line 12: `from . import ...`
- Line 13: `from . import ...`
- Line 14: `from .test_linter import ...`
- Line 15: `from . import ...`
- Line 16: `from . import ...`
- Line 17: `from . import ...`
- Line 18: `from . import ...`
- Line 19: `from . import ...`
- Line 20: `from . import ...`
- Line 21: `from .test_watch import ...`
- Line 22: `from .test_scripting import ...`
- Line 23: `from .test_exceptions import ...`
- Line 24: `from . import ...`
- Line 25: `from .test_sendchat import ...`
- Line 26: `from . import ...`
- Line 27: `from . import ...`
- Line 28: `from .test_find_or_blocks import ...`
- Line 29: `from . import ...`
- Line 30: `from . import ...`
- Line 31: `from .test_aws_credentials import ...`
- Line 32: `from . import ...`
- Line 33: `from .test_special import ...`
- Line 34: `from . import ...`
- Line 35: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/__init__.py
- Line 16: `from .core.modules import ...`
- Line 26: `from .core.conversation import ...`
- Line 143: `from .pipeline_isolation import ...`
- Line 145: `from .security import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/cli/__init__.py
- Line 10: `from .claude_comm import ...`
- Line 11: `from .communication_commands import ...`
- Line 12: `from .conversation_commands import ...`
- Line 13: `from .slash_mcp_mixin import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/cli/claude_comm.py
- Line 45: `from ..core import ...`
- Line 46: `from .granger_slash_mcp_mixin import ...`
- Line 392: `from ..core.modules import ...`
- Line 462: `from ..core.modules import ...`
- Line 533: `from ..core.modules import ...`
- Line 622: `from ..core.adapters import ...`
- Line 769: `from ..mcp import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/cli/conversation_commands.py
- Line 33: `from ..core.conversation.conversation_manager import ...`
- Line 34: `from ..core.conversation.conversation_message import ...`
- Line 35: `from ..core.modules import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/cli/forecast_commands.py
- Line 24: `from ..forecast.sklearn_wrapper import ...`
- Line 25: `from ..forecast.data_handlers import ...`
- Line 26: `from ..forecast.visualization import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/cli/granger_slash_mcp_mixin.py
- Line 39: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/__init__.py
- Line 11: `from .modules import ...`
- Line 15: `from .modules import ...`
- Line 20: `from .conversation import ...`
- Line 34: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/__init__.py
- Line 10: `from .base_adapter import ...`
- Line 11: `from .cli_adapter import ...`
- Line 12: `from .rest_adapter import ...`
- Line 13: `from .mcp_adapter import ...`
- Line 14: `from .marker_adapter import ...`
- Line 15: `from .adapter_registry import ...`
- Line 16: `from .hardware_adapter import ...`
- Line 17: `from .jtag_adapter import ...`
- Line 18: `from .scpi_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/adapter_registry.py
- Line 20: `from .base_adapter import ...`
- Line 21: `from .cli_adapter import ...`
- Line 22: `from .rest_adapter import ...`
- Line 23: `from .mcp_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/binary_adapter_mixin.py
- Line 18: `from ..binary_handler import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/cli_adapter.py
- Line 17: `from .base_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/hardware_adapter.py
- Line 29: `from .base_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/jtag_adapter.py
- Line 26: `from .hardware_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/mcp_adapter.py
- Line 13: `from .base_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/rest_adapter.py
- Line 14: `from .base_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/adapters/scpi_adapter.py
- Line 28: `from .hardware_adapter import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/conversation/__init__.py
- Line 9: `from .conversation_message import ...`
- Line 10: `from .conversation_module import ...`
- Line 11: `from .conversation_manager import ...`
- Line 12: `from .conversation_protocol import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/conversation/conversation_manager.py
- Line 19: `from .conversation_message import ...`
- Line 20: `from ..modules.module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/conversation/conversation_module.py
- Line 14: `from ..modules.base_module import ...`
- Line 15: `from .conversation_message import ...`
- Line 16: `from ..modules.module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/conversation/conversation_protocol.py
- Line 16: `from .conversation_message import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/discovery/__init__.py
- Line 10: `from .service_discovery import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/event_integration.py
- Line 17: `from .module_communicator import ...`
- Line 18: `from .event_system import ...`
- Line 19: `from .modules.base_module import ...`
- Line 20: `from .conversation.conversation_message import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/llm/external_llm_module.py
- Line 34: `from ..modules.base_module import ...`
- Line 35: `from ..modules.module_registry import ...`
- Line 36: `from .llm_integration import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/llm/llm_config.py
- Line 35: `from .llm_integration import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/module_communicator.py
- Line 24: `from .modules import ...`
- Line 25: `from .conversation import ...`
- Line 26: `from .modules.progress_tracker import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/__init__.py
- Line 9: `from .base_module import ...`
- Line 10: `from .module_registry import ...`
- Line 11: `from .claude_code_communicator import ...`
- Line 15: `from .example_modules import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/base_module.py
- Line 24: `from .claude_code_communicator import ...`
- Line 25: `from .module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/browser_test_module.py
- Line 67: `from .browser_automation_module import ...`
- Line 68: `from .screenshot_module import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/communication_tracker.py
- Line 21: `from ..granger_hub.task_executor import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/example_modules.py
- Line 13: `from .base_module import ...`
- Line 14: `from .module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/progress_utils.py
- Line 26: `from .progress_tracker import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/modules/task_executor.py
- Line 20: `from .claude_code_communicator import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/storage/arango_expert.py
- Line 25: `from ..modules.base_module import ...`
- Line 26: `from ..modules.module_registry import ...`
- Line 27: `from .graph_backend import ...`
- Line 28: `from .graph_communicator import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/storage/arango_expert_llm.py
- Line 19: `from .arango_expert import ...`
- Line 20: `from ..llm.llm_integration import ...`
- Line 21: `from ..modules.module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/storage/arango_hybrid.py
- Line 33: `from .graph_backend import ...`
- Line 34: `from .arango_conversation import ...`
- Line 35: `from ..modules.communication_tracker import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/core/storage/graph_communicator.py
- Line 28: `from .graph_backend import ...`
- Line 29: `from ..modules.base_module import ...`
- Line 30: `from ..modules.module_registry import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/__init__.py
- Line 9: `from .research.research_agent import ...`
- Line 10: `from .analysis.optimization_analyzer import ...`
- Line 11: `from .analysis.pattern_recognizer import ...`
- Line 12: `from .generation.scenario_generator import ...`
- Line 13: `from .learning.evolution_engine import ...`
- Line 14: `from .discovery_orchestrator import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/analysis/pattern_recognizer.py
- Line 14: `from ..research.research_agent import ...`
- Line 15: `from ..analysis.optimization_analyzer import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/discovery_orchestrator.py
- Line 17: `from .research.research_agent import ...`
- Line 18: `from .analysis.optimization_analyzer import ...`
- Line 19: `from .analysis.pattern_recognizer import ...`
- Line 20: `from .generation.scenario_generator import ...`
- Line 21: `from .learning.evolution_engine import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/generation/scenario_generator.py
- Line 17: `from ..research.research_agent import ...`
- Line 18: `from ..analysis.optimization_analyzer import ...`
- Line 872: `from ..research.research_agent import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/learning/evolution_engine.py
- Line 16: `from ..generation.scenario_generator import ...`
- Line 17: `from ..analysis.optimization_analyzer import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/self_improvement_engine.py
- Line 19: `from .discovery_orchestrator import ...`
- Line 20: `from .analysis.optimization_analyzer import ...`
- Line 21: `from .generation.scenario_generator import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/forecast/__init__.py
- Line 19: `from .forecaster import ...`
- Line 20: `from .data_handlers import ...`
- Line 26: `from .sklearn_wrapper import ...`
- Line 27: `from .model_backends import ...`
- Line 34: `from .visualization import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/forecast/forecaster.py
- Line 19: `from .ollama_forecast import ...`
- Line 20: `from .patches import ...`
- Line 21: `from .data_handlers import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/forecast/sklearn_wrapper.py
- Line 21: `from .model_backends import ...`
- Line 22: `from .data_handlers import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/mcp/__init__.py
- Line 25: `from .prompts import ...`
- Line 33: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/mcp/fastmcp_server.py
- Line 24: `from ..core.module_communicator import ...`
- Line 25: `from ..core.modules import ...`
- Line 26: `from .prompts import ...`
- Line 27: `from .hub_prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/mcp/handlers.py
- Line 16: `from ..core.module_communicator import ...`
- Line 17: `from ..core.modules.task_executor import ...`
- Line 152: `from ..granger_hub.base_module import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/mcp/hub_prompts.py
- Line 10: `from .prompts import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/mcp/server.py
- Line 20: `from ..core.module_communicator import ...`
- Line 21: `from ..core.modules.base_module import ...`
- Line 22: `from .handlers import ...`
- Line 23: `from .tools import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/rl/episodes.py
- Line 23: `from .rewards import ...`
- Line 24: `from .ollama_integration import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/rl/metrics/__init__.py
- Line 10: `from .collector import ...`
- Line 11: `from .models import ...`
- Line 12: `from .arangodb_store import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/rl/metrics/arangodb_store.py
- Line 32: `from .models import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/rl/metrics/collector.py
- Line 32: `from .models import ...`
- Line 36: `from .arangodb_store import ...`

#### /home/graham/workspace/experiments/granger_hub/src/granger_hub/rl/metrics/integration.py
- Line 30: `from .collector import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/__init__.py
- Line 5: `from .conftest import ...`
- Line 6: `from .test_granger_integration import ...`
- Line 7: `from . import ...`
- Line 8: `from .test_conversation_integration import ...`
- Line 9: `from .test_conversation_integration_mock import ...`
- Line 10: `from .test_communicator_conversations import ...`
- Line 11: `from .test_honeypot import ...`
- Line 12: `from .test_arango_conversations_mock import ...`
- Line 13: `from .test_integration_validation import ...`
- Line 14: `from .test_conversation_integration_simple import ...`
- Line 15: `from .test_schema_negotiation import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/core/__init__.py
- Line 5: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/core/conversation/__init__.py
- Line 5: `from .test_conversation_context import ...`
- Line 6: `from .test_conversation_message import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/core/llm/__init__.py
- Line 5: `from .test_llm_integration import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/core/modules/__init__.py
- Line 5: `from . import ...`
- Line 6: `from .test_analyzer import ...`
- Line 7: `from .conversation_test_validator import ...`
- Line 8: `from .test_schema_negotiation import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/core/storage/__init__.py
- Line 5: `from .test_storage_backends import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/fixtures/forecast/__init__.py
- Line 5: `from .generate_fixtures import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/forecast/__init__.py
- Line 5: `from .test_forecast_real_data import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/__init__.py
- Line 5: `from .conftest import ...`
- Line 6: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/base/__init__.py
- Line 5: `from .module_mock import ...`
- Line 6: `from .message_validators import ...`
- Line 7: `from .result_assertions import ...`
- Line 8: `from .scenario_test_base import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/categories/research_integration/__init__.py
- Line 5: `from . import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/utils/__init__.py
- Line 5: `from .workflow_runner import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/mcp/__init__.py
- Line 5: `from .test_mcp_server import ...`

#### /home/graham/workspace/experiments/granger_hub/tests/rl/__init__.py
- Line 5: `from .test_reinforcement_learning import ...`

#### /home/graham/workspace/experiments/llm_call/archive/archive/litellm_client_poc copy.py
- Line 36: `from .poc_retry_manager import ...`
- Line 42: `from .poc_validation_strategies import ...`

#### /home/graham/workspace/experiments/llm_call/archive/gemini_refactor/core/__init__.py
- Line 25: `from .utils.logging_setup import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/agentic-rag/refs/agents.py
- Line 39: `from .agent_types import ...`
- Line 40: `from .default_tools import ...`
- Line 41: `from .local_python_executor import ...`
- Line 42: `from .memory import ...`
- Line 43: `from .models import ...`
- Line 48: `from .monitoring import ...`
- Line 54: `from .remote_executors import ...`
- Line 55: `from .tools import ...`
- Line 56: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/lora-server/autoload/lora_manager.py
- Line 8: `from .config import ...`
- Line 9: `from .redis_manager import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/lora-server/autoload/redis_manager.py
- Line 5: `from .config import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/lora-server/autoload/server.py
- Line 10: `from .config import ...`
- Line 11: `from .lora_manager import ...`
- Line 12: `from .redis_manager import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/api/main.py
- Line 3: `from .routes import ...`
- Line 4: `from .core.config import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/api/routes/chat.py
- Line 5: `from ..models.api_models import ...`
- Line 6: `from ..core.config import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/load_balancer.py
- Line 4: `from .db.session import ...`
- Line 5: `from .db.models import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/pod_utils.py
- Line 6: `from .model_configs import ...`
- Line 7: `from .db.session import ...`
- Line 8: `from .db.models import ...`
- Line 10: `from .inference_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/scaling_manager.py
- Line 5: `from .pod_utils import ...`
- Line 6: `from .model_configs import ...`
- Line 7: `from .db.models import ...`
- Line 8: `from .db.session import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/doc-convert/src/doc_convert/__init__.py
- Line 1: `from .doc_convert import ...`
- Line 2: `from .__main__ import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/doc-convert/src/doc_convert/__main__.py
- Line 4: `from .doc_convert import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/pypi-mcp-test/src/pypi_mcp_test/__init__.py
- Line 9: `from .pypi_mcp_test import ...`

#### /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/pypi-mcp-test/src/pypi_mcp_test/__main__.py
- Line 1: `from .pypi_mcp_test import ...`

#### /home/graham/workspace/experiments/llm_call/repos/files-to-prompt/files_to_prompt/__main__.py
- Line 15: `from .cli import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/__init__.py
- Line 15: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/enterprise_hooks/__init__.py
- Line 23: `from .managed_files import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/send_emails/resend_email.py
- Line 27: `from .base_email import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/litellm_enterprise/enterprise_callbacks/send_emails/smtp_email.py
- Line 23: `from .base_email import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/enterprise/litellm_enterprise/proxy/enterprise_routes.py
- Line 25: `from .guardrails.endpoints import ...`
- Line 26: `from .utils import ...`
- Line 27: `from .vector_stores.endpoints import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/__init__.py
- Line 800: `from .timeout import ...`
- Line 801: `from .cost_calculator import ...`
- Line 806: `from .utils import ...`
- Line 856: `from .llms.custom_llm import ...`
- Line 857: `from .llms.bedrock.chat.converse_transformation import ...`
- Line 858: `from .llms.openai_like.chat.handler import ...`
- Line 859: `from .llms.aiohttp_openai.chat.transformation import ...`
- Line 860: `from .llms.galadriel.chat.transformation import ...`
- Line 861: `from .llms.github.chat.transformation import ...`
- Line 862: `from .llms.empower.chat.transformation import ...`
- Line 863: `from .llms.huggingface.chat.transformation import ...`
- Line 864: `from .llms.huggingface.embedding.transformation import ...`
- Line 865: `from .llms.oobabooga.chat.transformation import ...`
- Line 866: `from .llms.maritalk import ...`
- Line 867: `from .llms.openrouter.chat.transformation import ...`
- Line 868: `from .llms.anthropic.chat.transformation import ...`
- Line 869: `from .llms.anthropic.common_utils import ...`
- Line 870: `from .llms.groq.stt.transformation import ...`
- Line 871: `from .llms.anthropic.completion.transformation import ...`
- Line 872: `from .llms.triton.completion.transformation import ...`
- Line 873: `from .llms.triton.completion.transformation import ...`
- Line 874: `from .llms.triton.completion.transformation import ...`
- Line 875: `from .llms.triton.embedding.transformation import ...`
- Line 876: `from .llms.databricks.chat.transformation import ...`
- Line 877: `from .llms.databricks.embed.transformation import ...`
- Line 878: `from .llms.predibase.chat.transformation import ...`
- Line 879: `from .llms.replicate.chat.transformation import ...`
- Line 880: `from .llms.cohere.completion.transformation import ...`
- Line 881: `from .llms.snowflake.chat.transformation import ...`
- Line 882: `from .llms.cohere.rerank.transformation import ...`
- Line 883: `from .llms.cohere.rerank_v2.transformation import ...`
- Line 884: `from .llms.azure_ai.rerank.transformation import ...`
- Line 885: `from .llms.infinity.rerank.transformation import ...`
- Line 886: `from .llms.jina_ai.rerank.transformation import ...`
- Line 887: `from .llms.clarifai.chat.transformation import ...`
- Line 888: `from .llms.ai21.chat.transformation import ...`
- Line 889: `from .llms.meta_llama.chat.transformation import ...`
- Line 890: `from .llms.anthropic.experimental_pass_through.messages.transformation import ...`
- Line 893: `from .llms.bedrock.messages.invoke_transformations.anthropic_claude3_transformation import ...`
- Line 896: `from .llms.together_ai.chat import ...`
- Line 897: `from .llms.together_ai.completion.transformation import ...`
- Line 898: `from .llms.cloudflare.chat.transformation import ...`
- Line 899: `from .llms.novita.chat.transformation import ...`
- Line 900: `from .llms.deprecated_providers.palm import ...`
- Line 903: `from .llms.nlp_cloud.chat.handler import ...`
- Line 904: `from .llms.petals.completion.transformation import ...`
- Line 905: `from .llms.deprecated_providers.aleph_alpha import ...`
- Line 906: `from .llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import ...`
- Line 910: `from .llms.gemini.common_utils import ...`
- Line 911: `from .llms.gemini.chat.transformation import ...`
- Line 917: `from .llms.vertex_ai.vertex_embeddings.transformation import ...`
- Line 923: `from .llms.vertex_ai.vertex_ai_partner_models.anthropic.transformation import ...`
- Line 926: `from .llms.vertex_ai.vertex_ai_partner_models.llama3.transformation import ...`
- Line 929: `from .llms.vertex_ai.vertex_ai_partner_models.ai21.transformation import ...`
- Line 933: `from .llms.ollama.completion.transformation import ...`
- Line 934: `from .llms.sagemaker.completion.transformation import ...`
- Line 935: `from .llms.sagemaker.chat.transformation import ...`
- Line 936: `from .llms.ollama_chat import ...`
- Line 937: `from .llms.bedrock.chat.invoke_handler import ...`
- Line 942: `from .llms.bedrock.common_utils import ...`
- Line 945: `from .llms.bedrock.chat.invoke_transformations.amazon_ai21_transformation import ...`
- Line 948: `from .llms.bedrock.chat.invoke_transformations.amazon_nova_transformation import ...`
- Line 951: `from .llms.bedrock.chat.invoke_transformations.anthropic_claude2_transformation import ...`
- Line 954: `from .llms.bedrock.chat.invoke_transformations.anthropic_claude3_transformation import ...`
- Line 957: `from .llms.bedrock.chat.invoke_transformations.amazon_cohere_transformation import ...`
- Line 960: `from .llms.bedrock.chat.invoke_transformations.amazon_llama_transformation import ...`
- Line 963: `from .llms.bedrock.chat.invoke_transformations.amazon_deepseek_transformation import ...`
- Line 966: `from .llms.bedrock.chat.invoke_transformations.amazon_mistral_transformation import ...`
- Line 969: `from .llms.bedrock.chat.invoke_transformations.amazon_titan_transformation import ...`
- Line 972: `from .llms.bedrock.chat.invoke_transformations.base_invoke_transformation import ...`
- Line 976: `from .llms.bedrock.image.amazon_stability1_transformation import ...`
- Line 977: `from .llms.bedrock.image.amazon_stability3_transformation import ...`
- Line 978: `from .llms.bedrock.image.amazon_nova_canvas_transformation import ...`
- Line 979: `from .llms.bedrock.embed.amazon_titan_g1_transformation import ...`
- Line 980: `from .llms.bedrock.embed.amazon_titan_multimodal_transformation import ...`
- Line 983: `from .llms.bedrock.embed.amazon_titan_v2_transformation import ...`
- Line 986: `from .llms.cohere.chat.transformation import ...`
- Line 987: `from .llms.bedrock.embed.cohere_transformation import ...`
- Line 988: `from .llms.openai.openai import ...`
- Line 989: `from .llms.openai.image_variations.transformation import ...`
- Line 990: `from .llms.deepinfra.chat.transformation import ...`
- Line 991: `from .llms.deepgram.audio_transcription.transformation import ...`
- Line 994: `from .llms.topaz.common_utils import ...`
- Line 995: `from .llms.topaz.image_variations.transformation import ...`
- Line 997: `from .llms.groq.chat.transformation import ...`
- Line 998: `from .llms.voyage.embedding.transformation import ...`
- Line 999: `from .llms.infinity.embedding.transformation import ...`
- Line 1000: `from .llms.azure_ai.chat.transformation import ...`
- Line 1001: `from .llms.mistral.mistral_chat_transformation import ...`
- Line 1002: `from .llms.openai.responses.transformation import ...`
- Line 1003: `from .llms.azure.responses.transformation import ...`
- Line 1004: `from .llms.openai.chat.o_series_transformation import ...`
- Line 1009: `from .llms.snowflake.chat.transformation import ...`
- Line 1012: `from .llms.openai.chat.gpt_transformation import ...`
- Line 1015: `from .llms.openai.transcriptions.whisper_transformation import ...`
- Line 1018: `from .llms.openai.transcriptions.gpt_transformation import ...`
- Line 1023: `from .llms.openai.chat.gpt_audio_transformation import ...`
- Line 1029: `from .llms.nvidia_nim.chat.transformation import ...`
- Line 1030: `from .llms.nvidia_nim.embed import ...`
- Line 1035: `from .llms.featherless_ai.chat.transformation import ...`
- Line 1036: `from .llms.cerebras.chat import ...`
- Line 1037: `from .llms.sambanova.chat import ...`
- Line 1038: `from .llms.ai21.chat.transformation import ...`
- Line 1039: `from .llms.fireworks_ai.chat.transformation import ...`
- Line 1040: `from .llms.fireworks_ai.completion.transformation import ...`
- Line 1041: `from .llms.fireworks_ai.audio_transcription.transformation import ...`
- Line 1044: `from .llms.fireworks_ai.embed.fireworks_ai_transformation import ...`
- Line 1047: `from .llms.friendliai.chat.transformation import ...`
- Line 1048: `from .llms.jina_ai.embedding.transformation import ...`
- Line 1049: `from .llms.xai.chat.transformation import ...`
- Line 1050: `from .llms.xai.common_utils import ...`
- Line 1051: `from .llms.volcengine import ...`
- Line 1052: `from .llms.codestral.completion.transformation import ...`
- Line 1053: `from .llms.azure.azure import ...`
- Line 1058: `from .llms.azure.chat.gpt_transformation import ...`
- Line 1059: `from .llms.azure.completion.transformation import ...`
- Line 1060: `from .llms.hosted_vllm.chat.transformation import ...`
- Line 1061: `from .llms.llamafile.chat.transformation import ...`
- Line 1062: `from .llms.litellm_proxy.chat.transformation import ...`
- Line 1063: `from .llms.vllm.completion.transformation import ...`
- Line 1064: `from .llms.deepseek.chat.transformation import ...`
- Line 1065: `from .llms.lm_studio.chat.transformation import ...`
- Line 1066: `from .llms.lm_studio.embed.transformation import ...`
- Line 1067: `from .llms.nscale.chat.transformation import ...`
- Line 1068: `from .llms.perplexity.chat.transformation import ...`
- Line 1069: `from .llms.azure.chat.o_series_transformation import ...`
- Line 1070: `from .llms.watsonx.completion.transformation import ...`
- Line 1071: `from .llms.watsonx.chat.transformation import ...`
- Line 1072: `from .llms.watsonx.embed.transformation import ...`
- Line 1073: `from .main import ...`
- Line 1074: `from .integrations import ...`
- Line 1075: `from .exceptions import ...`
- Line 1097: `from .budget_manager import ...`
- Line 1098: `from .proxy.proxy_cli import ...`
- Line 1099: `from .router import ...`
- Line 1100: `from .assistants.main import ...`
- Line 1101: `from .batches.main import ...`
- Line 1102: `from .images.main import ...`
- Line 1103: `from .batch_completion.main import ...`
- Line 1104: `from .rerank_api.main import ...`
- Line 1105: `from .llms.anthropic.experimental_pass_through.messages.handler import ...`
- Line 1106: `from .responses.main import ...`
- Line 1107: `from .realtime_api.main import ...`
- Line 1108: `from .fine_tuning.main import ...`
- Line 1109: `from .files.main import ...`
- Line 1110: `from .scheduler import ...`
- Line 1111: `from .cost_calculator import ...`
- Line 1114: `from .types.adapter import ...`
- Line 1120: `from .vector_stores.vector_store_registry import ...`
- Line 1125: `from .types.llms.custom_llm import ...`
- Line 1126: `from .types.utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/_redis.py
- Line 40: `from ._logging import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/_service_logger.py
- Line 26: `from .integrations.custom_logger import ...`
- Line 27: `from .integrations.datadog.datadog import ...`
- Line 28: `from .integrations.opentelemetry import ...`
- Line 29: `from .integrations.prometheus_services import ...`
- Line 30: `from .types.services import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/anthropic_interface/__init__.py
- Line 15: `from .messages import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/assistants/main.py
- Line 42: `from ..llms.azure.assistants import ...`
- Line 43: `from ..llms.openai.openai import ...`
- Line 44: `from ..types.llms.openai import ...`
- Line 45: `from ..types.router import ...`
- Line 46: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/assistants/utils.py
- Line 23: `from ..exceptions import ...`
- Line 24: `from ..types.llms.openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/batch_completion/main.py
- Line 25: `from ..llms.vllm.completion import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/__init__.py
- Line 15: `from .caching import ...`
- Line 16: `from .disk_cache import ...`
- Line 17: `from .dual_cache import ...`
- Line 18: `from .in_memory_cache import ...`
- Line 19: `from .qdrant_semantic_cache import ...`
- Line 20: `from .redis_cache import ...`
- Line 21: `from .redis_cluster_cache import ...`
- Line 22: `from .redis_semantic_cache import ...`
- Line 23: `from .s3_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/caching.py
- Line 45: `from .base_cache import ...`
- Line 46: `from .disk_cache import ...`
- Line 47: `from .dual_cache import ...`
- Line 48: `from .in_memory_cache import ...`
- Line 49: `from .qdrant_semantic_cache import ...`
- Line 50: `from .redis_cache import ...`
- Line 51: `from .redis_cluster_cache import ...`
- Line 52: `from .redis_semantic_cache import ...`
- Line 53: `from .s3_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/disk_cache.py
- Line 18: `from .base_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/dual_cache.py
- Line 27: `from .base_cache import ...`
- Line 28: `from .in_memory_cache import ...`
- Line 29: `from .redis_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/in_memory_cache.py
- Line 28: `from .base_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/llm_caching_handler.py
- Line 17: `from .in_memory_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/qdrant_semantic_cache.py
- Line 28: `from .base_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/redis_cache.py
- Line 32: `from .base_cache import ...`
- Line 69: `from .._redis import ...`
- Line 148: `from .._redis import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/redis_cluster_cache.py
- Line 45: `from .._redis import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/redis_semantic_cache.py
- Line 31: `from .base_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/caching/s3_cache.py
- Line 25: `from .base_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/experimental_mcp_client/__init__.py
- Line 18: `from .tools import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/images/main.py
- Line 64: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/SlackAlerting/batching_handler.py
- Line 23: `from .slack_alerting import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/SlackAlerting/slack_alerting.py
- Line 57: `from ..email_templates.templates import ...`
- Line 58: `from .batching_handler import ...`
- Line 59: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/__init__.py
- Line 15: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/agentops/__init__.py
- Line 15: `from .agentops import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/arize/arize_phoenix.py
- Line 31: `from .opentelemetry import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/datadog/datadog.py
- Line 43: `from ..additional_logging_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/humanloop.py
- Line 30: `from .custom_logger import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/langfuse/langfuse_handler.py
- Line 22: `from .langfuse import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/langfuse/langfuse_prompt_management.py
- Line 32: `from ...litellm_core_utils.specialty_caches.dynamic_logging_cache import ...`
- Line 35: `from ..prompt_management_base import ...`
- Line 36: `from .langfuse import ...`
- Line 37: `from .langfuse_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/integrations/opik/opik.py
- Line 31: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/exception_mapping_utils.py
- Line 27: `from ..exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/fallback_utils.py
- Line 25: `from .asyncify import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/get_llm_provider_logic.py
- Line 26: `from ..types.router import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/litellm_logging.py
- Line 127: `from ..integrations.argilla import ...`
- Line 128: `from ..integrations.arize.arize_phoenix import ...`
- Line 129: `from ..integrations.athina import ...`
- Line 130: `from ..integrations.azure_storage.azure_storage import ...`
- Line 131: `from ..integrations.braintrust_logging import ...`
- Line 132: `from ..integrations.custom_prompt_management import ...`
- Line 133: `from ..integrations.datadog.datadog import ...`
- Line 134: `from ..integrations.datadog.datadog_llm_obs import ...`
- Line 135: `from ..integrations.dynamodb import ...`
- Line 136: `from ..integrations.galileo import ...`
- Line 137: `from ..integrations.gcs_bucket.gcs_bucket import ...`
- Line 138: `from ..integrations.gcs_pubsub.pub_sub import ...`
- Line 139: `from ..integrations.greenscale import ...`
- Line 140: `from ..integrations.helicone import ...`
- Line 141: `from ..integrations.humanloop import ...`
- Line 142: `from ..integrations.lago import ...`
- Line 143: `from ..integrations.langfuse.langfuse import ...`
- Line 144: `from ..integrations.langfuse.langfuse_handler import ...`
- Line 145: `from ..integrations.langfuse.langfuse_prompt_management import ...`
- Line 146: `from ..integrations.langsmith import ...`
- Line 147: `from ..integrations.literal_ai import ...`
- Line 148: `from ..integrations.logfire_logger import ...`
- Line 149: `from ..integrations.lunary import ...`
- Line 150: `from ..integrations.openmeter import ...`
- Line 151: `from ..integrations.opik.opik import ...`
- Line 152: `from ..integrations.prometheus import ...`
- Line 153: `from ..integrations.prompt_layer import ...`
- Line 154: `from ..integrations.s3 import ...`
- Line 155: `from ..integrations.supabase import ...`
- Line 156: `from ..integrations.traceloop import ...`
- Line 157: `from ..integrations.weights_biases import ...`
- Line 158: `from .exception_mapping_utils import ...`
- Line 159: `from .initialize_dynamic_callback_params import ...`
- Line 162: `from .specialty_caches.dynamic_logging_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/llm_response_utils/convert_dict_to_response.py
- Line 58: `from .get_headers import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/llm_response_utils/get_api_base.py
- Line 23: `from ...litellm_core_utils.get_llm_provider_logic import ...`
- Line 24: `from ...types.router import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/mock_functions.py
- Line 17: `from ..types.utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/prompt_templates/factory.py
- Line 57: `from .common_utils import ...`
- Line 58: `from .image_handling import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/realtime_streaming.py
- Line 36: `from .litellm_logging import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/specialty_caches/dynamic_logging_cache.py
- Line 19: `from ...caching import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/litellm_core_utils/streaming_handler.py
- Line 48: `from ..exceptions import ...`
- Line 49: `from .core_helpers import ...`
- Line 50: `from .exception_mapping_utils import ...`
- Line 51: `from .llm_response_utils.get_api_base import ...`
- Line 52: `from .rules import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/__init__.py
- Line 15: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/ai21/chat/transformation.py
- Line 20: `from ...openai_like.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/anthropic/chat/__init__.py
- Line 15: `from .handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/anthropic/chat/handler.py
- Line 60: `from ...base import ...`
- Line 61: `from ..common_utils import ...`
- Line 62: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/anthropic/chat/transformation.py
- Line 74: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/anthropic/experimental_pass_through/messages/handler.py
- Line 37: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/anthropic/experimental_pass_through/messages/transformation.py
- Line 33: `from ...common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/assistants.py
- Line 24: `from ...types.llms.openai import ...`
- Line 38: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/audio_transcriptions.py
- Line 34: `from .azure import ...`
- Line 35: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/azure.py
- Line 48: `from ...types.llms.openai import ...`
- Line 49: `from ..base import ...`
- Line 50: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/batches/handler.py
- Line 32: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/chat/gpt_transformation.py
- Line 35: `from ....exceptions import ...`
- Line 36: `from ....types.llms.openai import ...`
- Line 37: `from ...base_llm.chat.transformation import ...`
- Line 38: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/chat/o_series_handler.py
- Line 25: `from ...openai.openai import ...`
- Line 26: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/chat/o_series_transformation.py
- Line 26: `from ...openai.chat.o_series_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/completion/handler.py
- Line 26: `from ...openai.completion.transformation import ...`
- Line 27: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/completion/transformation.py
- Line 20: `from ...openai.completion.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/files/handler.py
- Line 28: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/image_generation/__init__.py
- Line 23: `from .dall_e_2_transformation import ...`
- Line 24: `from .dall_e_3_transformation import ...`
- Line 25: `from .gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure/realtime/handler.py
- Line 20: `from ....litellm_core_utils.litellm_logging import ...`
- Line 21: `from ....litellm_core_utils.realtime_streaming import ...`
- Line 22: `from ..azure import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure_ai/embed/__init__.py
- Line 15: `from .handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/azure_ai/embed/handler.py
- Line 34: `from .cohere_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/__init__.py
- Line 18: `from .anthropic_messages.transformation import ...`
- Line 19: `from .audio_transcription.transformation import ...`
- Line 20: `from .chat.transformation import ...`
- Line 21: `from .embedding.transformation import ...`
- Line 22: `from .image_edit.transformation import ...`
- Line 23: `from .image_generation.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/chat/transformation.py
- Line 50: `from ..base_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/files/transformation.py
- Line 33: `from ..chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/image_edit/transformation.py
- Line 34: `from ..chat.transformation import ...`
- Line 131: `from ..chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/realtime/transformation.py
- Line 28: `from ..chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/rerank/transformation.py
- Line 26: `from ..chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/base_llm/responses/transformation.py
- Line 37: `from ..chat.transformation import ...`
- Line 193: `from ..chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/__init__.py
- Line 15: `from .converse_handler import ...`
- Line 16: `from .invoke_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/converse_handler.py
- Line 35: `from ..base_aws_llm import ...`
- Line 36: `from ..common_utils import ...`
- Line 37: `from .invoke_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/converse_transformation.py
- Line 65: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/invoke_handler.py
- Line 83: `from ..base_aws_llm import ...`
- Line 84: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/invoke_transformations/amazon_deepseek_transformation.py
- Line 43: `from .amazon_llama_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/invoke_transformations/amazon_nova_transformation.py
- Line 29: `from ..converse_transformation import ...`
- Line 30: `from .base_invoke_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/chat/invoke_transformations/anthropic_claude2_transformation.py
- Line 23: `from .base_invoke_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/embed/embedding.py
- Line 36: `from ..base_aws_llm import ...`
- Line 37: `from ..common_utils import ...`
- Line 38: `from .amazon_titan_g1_transformation import ...`
- Line 39: `from .amazon_titan_multimodal_transformation import ...`
- Line 42: `from .amazon_titan_v2_transformation import ...`
- Line 43: `from .cohere_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/image/image_handler.py
- Line 38: `from ..base_aws_llm import ...`
- Line 39: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/bedrock/rerank/handler.py
- Line 35: `from ..base_aws_llm import ...`
- Line 36: `from ..common_utils import ...`
- Line 37: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/clarifai/chat/transformation.py
- Line 41: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/chat/transformation.py
- Line 31: `from ..common_utils import ...`
- Line 32: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/chat/v2_transformation.py
- Line 31: `from ..common_utils import ...`
- Line 32: `from ..common_utils import ...`
- Line 33: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/completion/transformation.py
- Line 32: `from ..common_utils import ...`
- Line 33: `from ..common_utils import ...`
- Line 34: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/embed/handler.py
- Line 33: `from .v1_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/embed/transformation.py
- Line 36: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/cohere/rerank/transformation.py
- Line 30: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/custom_llm.py
- Line 36: `from .base import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/databricks/chat/transformation.py
- Line 74: `from ...anthropic.chat.transformation import ...`
- Line 75: `from ...openai_like.chat.transformation import ...`
- Line 76: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/databricks/embed/handler.py
- Line 23: `from ...openai_like.embedding.handler import ...`
- Line 24: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/deepgram/audio_transcription/transformation.py
- Line 32: `from ...base_llm.audio_transcription.transformation import ...`
- Line 36: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/deepseek/chat/transformation.py
- Line 27: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/empower/chat/transformation.py
- Line 18: `from ...openai_like.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/fireworks_ai/audio_transcription/transformation.py
- Line 22: `from ...openai.transcriptions.whisper_transformation import ...`
- Line 25: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/fireworks_ai/chat/transformation.py
- Line 47: `from ...openai.chat.gpt_transformation import ...`
- Line 48: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/fireworks_ai/common_utils.py
- Line 26: `from ..base_llm.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/fireworks_ai/completion/transformation.py
- Line 22: `from ...base_llm.completion.transformation import ...`
- Line 23: `from ...openai.completion.utils import ...`
- Line 24: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/friendliai/chat/transformation.py
- Line 18: `from ...openai_like.chat.handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/galadriel/chat/transformation.py
- Line 18: `from ...openai_like.chat.handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/gemini/chat/transformation.py
- Line 30: `from ...vertex_ai.gemini.transformation import ...`
- Line 31: `from ...vertex_ai.gemini.vertex_and_google_ai_studio_gemini import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/gemini/files/transformation.py
- Line 38: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/gemini/realtime/transformation.py
- Line 72: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/github/chat/transformation.py
- Line 18: `from ...openai_like.chat.handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/groq/chat/handler.py
- Line 28: `from ...groq.chat.transformation import ...`
- Line 29: `from ...openai_like.chat.handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/groq/chat/transformation.py
- Line 32: `from ...openai_like.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/hosted_vllm/chat/transformation.py
- Line 33: `from ....utils import ...`
- Line 34: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/huggingface/chat/transformation.py
- Line 36: `from ...openai.chat.gpt_transformation import ...`
- Line 37: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/huggingface/embedding/handler.py
- Line 33: `from ...base import ...`
- Line 34: `from ..common_utils import ...`
- Line 35: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/huggingface/embedding/transformation.py
- Line 42: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/infinity/embedding/transformation.py
- Line 30: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/infinity/rerank/transformation.py
- Line 36: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/litellm_proxy/chat/transformation.py
- Line 24: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/llamafile/chat/transformation.py
- Line 23: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/lm_studio/chat/transformation.py
- Line 23: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/nlp_cloud/chat/handler.py
- Line 29: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/nlp_cloud/chat/transformation.py
- Line 32: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/novita/chat/transformation.py
- Line 20: `from ....types.llms.openai import ...`
- Line 21: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/ollama/completion/transformation.py
- Line 47: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/oobabooga/chat/oobabooga.py
- Line 25: `from ..common_utils import ...`
- Line 26: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/oobabooga/chat/transformation.py
- Line 29: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/chat/gpt_audio_transformation.py
- Line 20: `from .gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/chat/gpt_transformation.py
- Line 69: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/chat/o_series_transformation.py
- Line 32: `from .gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/completion/handler.py
- Line 32: `from ..common_utils import ...`
- Line 33: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/completion/transformation.py
- Line 25: `from ..chat.gpt_transformation import ...`
- Line 26: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/image_edit/transformation.py
- Line 36: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/image_generation/__init__.py
- Line 22: `from .dall_e_2_transformation import ...`
- Line 23: `from .dall_e_3_transformation import ...`
- Line 24: `from .gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/image_variations/handler.py
- Line 28: `from ...base_llm.image_variations.transformation import ...`
- Line 29: `from ...custom_httpx.llm_http_handler import ...`
- Line 30: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/image_variations/transformation.py
- Line 30: `from ...base_llm.image_variations.transformation import ...`
- Line 31: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/openai.py
- Line 67: `from ...types.llms.openai import ...`
- Line 68: `from ..base import ...`
- Line 69: `from .chat.o_series_transformation import ...`
- Line 70: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/realtime/handler.py
- Line 21: `from ....litellm_core_utils.litellm_logging import ...`
- Line 22: `from ....litellm_core_utils.realtime_streaming import ...`
- Line 23: `from ..openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/responses/transformation.py
- Line 31: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/transcriptions/gpt_transformation.py
- Line 24: `from .whisper_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/transcriptions/handler.py
- Line 39: `from ..openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai/transcriptions/whisper_transformation.py
- Line 34: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai_like/chat/handler.py
- Line 34: `from ..common_utils import ...`
- Line 35: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai_like/chat/transformation.py
- Line 27: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openai_like/embedding/handler.py
- Line 35: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/openrouter/chat/transformation.py
- Line 29: `from ...openai.chat.gpt_transformation import ...`
- Line 30: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/perplexity/chat/transformation.py
- Line 23: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/petals/completion/handler.py
- Line 33: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/petals/completion/transformation.py
- Line 32: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/predibase/chat/handler.py
- Line 44: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/predibase/chat/transformation.py
- Line 28: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/replicate/chat/handler.py
- Line 35: `from ..common_utils import ...`
- Line 36: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/replicate/chat/transformation.py
- Line 37: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/sagemaker/chat/handler.py
- Line 28: `from ..common_utils import ...`
- Line 29: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/sagemaker/chat/transformation.py
- Line 37: `from ...openai.chat.gpt_transformation import ...`
- Line 38: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/sagemaker/completion/handler.py
- Line 42: `from ..common_utils import ...`
- Line 43: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/sagemaker/completion/transformation.py
- Line 36: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/snowflake/chat/transformation.py
- Line 27: `from ...openai_like.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/together_ai/chat.py
- Line 23: `from ..openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/together_ai/completion/transformation.py
- Line 27: `from ...openai.completion.transformation import ...`
- Line 28: `from ...openai.completion.utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/topaz/common_utils.py
- Line 24: `from ..base_llm.base_utils import ...`
- Line 25: `from ..base_llm.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/topaz/image_variations/transformation.py
- Line 40: `from ...base_llm.image_variations.transformation import ...`
- Line 41: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/triton/completion/transformation.py
- Line 42: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/triton/embedding/transformation.py
- Line 31: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/batches/handler.py
- Line 37: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/context_caching/transformation.py
- Line 25: `from ..common_utils import ...`
- Line 26: `from ..gemini.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/context_caching/vertex_ai_context_caching.py
- Line 37: `from ..common_utils import ...`
- Line 38: `from ..vertex_llm_base import ...`
- Line 39: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/files/handler.py
- Line 33: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/files/transformation.py
- Line 51: `from ..common_utils import ...`
- Line 52: `from ..vertex_llm_base import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/gemini/transformation.py
- Line 64: `from ..common_utils import ...`
- Line 413: `from ..context_caching.vertex_ai_context_caching import ...`
- Line 455: `from ..context_caching.vertex_ai_context_caching import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py
- Line 93: `from ....utils import ...`
- Line 94: `from ..common_utils import ...`
- Line 95: `from ..vertex_llm_base import ...`
- Line 96: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/gemini_embeddings/batch_embed_content_handler.py
- Line 37: `from ..gemini.vertex_and_google_ai_studio_gemini import ...`
- Line 38: `from .batch_embed_content_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/multimodal_embeddings/embedding_handler.py
- Line 36: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/multimodal_embeddings/transformation.py
- Line 42: `from ...base_llm.embedding.transformation import ...`
- Line 43: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_ai_partner_models/anthropic/transformation.py
- Line 31: `from ....anthropic.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_ai_partner_models/llama3/transformation.py
- Line 29: `from ...common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_ai_partner_models/main.py
- Line 29: `from ...custom_httpx.llm_http_handler import ...`
- Line 30: `from ..vertex_llm_base import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_embeddings/embedding_handler.py
- Line 35: `from .types import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_embeddings/transformation.py
- Line 26: `from .types import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_llm_base.py
- Line 27: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vertex_ai/vertex_model_garden/main.py
- Line 24: `from ..common_utils import ...`
- Line 25: `from ..vertex_llm_base import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/vllm/completion/transformation.py
- Line 15: `from ...hosted_vllm.chat.transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/watsonx/chat/handler.py
- Line 26: `from ...openai_like.chat.handler import ...`
- Line 27: `from ..common_utils import ...`
- Line 28: `from .transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/watsonx/chat/transformation.py
- Line 24: `from ....utils import ...`
- Line 25: `from ...openai.chat.gpt_transformation import ...`
- Line 26: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/watsonx/completion/transformation.py
- Line 40: `from ...base_llm.chat.transformation import ...`
- Line 41: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/watsonx/embed/transformation.py
- Line 31: `from ..common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/llms/xai/chat/transformation.py
- Line 29: `from ...openai.chat.gpt_transformation import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/main.py
- Line 128: `from ._logging import ...`
- Line 129: `from .caching.caching import ...`
- Line 130: `from .litellm_core_utils.fallback_utils import ...`
- Line 134: `from .litellm_core_utils.prompt_templates.common_utils import ...`
- Line 138: `from .litellm_core_utils.prompt_templates.factory import ...`
- Line 146: `from .litellm_core_utils.streaming_chunk_builder_utils import ...`
- Line 147: `from .llms import ...`
- Line 148: `from .llms.anthropic.chat import ...`
- Line 149: `from .llms.azure.audio_transcriptions import ...`
- Line 150: `from .llms.azure.azure import ...`
- Line 151: `from .llms.azure.chat.o_series_handler import ...`
- Line 152: `from .llms.azure.completion.handler import ...`
- Line 153: `from .llms.azure_ai.embed import ...`
- Line 154: `from .llms.bedrock.chat import ...`
- Line 155: `from .llms.bedrock.embed.embedding import ...`
- Line 156: `from .llms.bedrock.image.image_handler import ...`
- Line 157: `from .llms.codestral.completion.handler import ...`
- Line 158: `from .llms.cohere.embed import ...`
- Line 159: `from .llms.custom_httpx.aiohttp_handler import ...`
- Line 160: `from .llms.custom_httpx.llm_http_handler import ...`
- Line 161: `from .llms.custom_llm import ...`
- Line 162: `from .llms.databricks.embed.handler import ...`
- Line 163: `from .llms.deprecated_providers import ...`
- Line 164: `from .llms.groq.chat.handler import ...`
- Line 165: `from .llms.huggingface.embedding.handler import ...`
- Line 166: `from .llms.nlp_cloud.chat.handler import ...`
- Line 167: `from .llms.ollama.completion import ...`
- Line 168: `from .llms.oobabooga.chat import ...`
- Line 169: `from .llms.openai.completion.handler import ...`
- Line 170: `from .llms.openai.image_variations.handler import ...`
- Line 171: `from .llms.openai.openai import ...`
- Line 172: `from .llms.openai.transcriptions.handler import ...`
- Line 173: `from .llms.openai_like.chat.handler import ...`
- Line 174: `from .llms.openai_like.embedding.handler import ...`
- Line 175: `from .llms.petals.completion import ...`
- Line 176: `from .llms.predibase.chat.handler import ...`
- Line 177: `from .llms.replicate.chat.handler import ...`
- Line 178: `from .llms.sagemaker.chat.handler import ...`
- Line 179: `from .llms.sagemaker.completion.handler import ...`
- Line 180: `from .llms.vertex_ai import ...`
- Line 181: `from .llms.vertex_ai.gemini.vertex_and_google_ai_studio_gemini import ...`
- Line 182: `from .llms.vertex_ai.gemini_embeddings.batch_embed_content_handler import ...`
- Line 185: `from .llms.vertex_ai.image_generation.image_generation_handler import ...`
- Line 188: `from .llms.vertex_ai.multimodal_embeddings.embedding_handler import ...`
- Line 191: `from .llms.vertex_ai.text_to_speech.text_to_speech_handler import ...`
- Line 192: `from .llms.vertex_ai.vertex_ai_partner_models.main import ...`
- Line 193: `from .llms.vertex_ai.vertex_embeddings.embedding_handler import ...`
- Line 194: `from .llms.vertex_ai.vertex_model_garden.main import ...`
- Line 195: `from .llms.vllm.completion import ...`
- Line 196: `from .llms.watsonx.chat.handler import ...`
- Line 197: `from .llms.watsonx.common_utils import ...`
- Line 198: `from .types.llms.anthropic import ...`
- Line 199: `from .types.llms.openai import ...`
- Line 209: `from .types.utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/__init__.py
- Line 15: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/_experimental/mcp_server/server.py
- Line 61: `from .mcp_server_manager import ...`
- Line 62: `from .sse_transport import ...`
- Line 63: `from .tool_registry import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/_types.py
- Line 59: `from .types_utils.utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/auth/auth_checks.py
- Line 76: `from .auth_checks_organization import ...`
- Line 77: `from .auth_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/auth/handle_jwt.py
- Line 49: `from .auth_checks import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/auth/route_checks.py
- Line 33: `from .auth_checks_organization import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/__init__.py
- Line 15: `from .client import ...`
- Line 16: `from .chat import ...`
- Line 17: `from .models import ...`
- Line 18: `from .model_groups import ...`
- Line 19: `from .exceptions import ...`
- Line 20: `from .users import ...`
- Line 21: `from .health import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/chat.py
- Line 20: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/__init__.py
- Line 15: `from .main import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/chat.py
- Line 25: `from ...chat import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/credentials.py
- Line 26: `from ...credentials import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/http.py
- Line 25: `from ...http_client import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/keys.py
- Line 26: `from ...keys import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/models.py
- Line 28: `from ... import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/commands/users.py
- Line 17: `from ... import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/cli/main.py
- Line 25: `from .commands.models import ...`
- Line 26: `from .commands.credentials import ...`
- Line 27: `from .commands.chat import ...`
- Line 28: `from .commands.http import ...`
- Line 29: `from .commands.keys import ...`
- Line 30: `from .commands.users import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/client.py
- Line 17: `from .http_client import ...`
- Line 18: `from .models import ...`
- Line 19: `from .model_groups import ...`
- Line 20: `from .chat import ...`
- Line 21: `from .keys import ...`
- Line 22: `from .credentials import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/credentials.py
- Line 21: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/health.py
- Line 16: `from .http_client import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/keys.py
- Line 20: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/model_groups.py
- Line 20: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/models.py
- Line 20: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/client/users.py
- Line 20: `from .exceptions import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/guardrails/guardrail_registry.py
- Line 40: `from .guardrail_initializers import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/hooks/__init__.py
- Line 18: `from . import ...`
- Line 19: `from .cache_control_check import ...`
- Line 20: `from .max_budget_limiter import ...`
- Line 21: `from .parallel_request_limiter import ...`
- Line 22: `from .parallel_request_limiter_v2 import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/openai_files_endpoints/files_endpoints.py
- Line 62: `from .common_utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_passthrough_endpoints.py
- Line 38: `from .passthrough_endpoint_router import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_provider_handlers/anthropic_passthrough_logging_handler.py
- Line 40: `from ..success_handler import ...`
- Line 41: `from ..types import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_provider_handlers/assembly_passthrough_logging_handler.py
- Line 114: `from ..pass_through_endpoints import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_provider_handlers/base_passthrough_logging_handler.py
- Line 39: `from ..success_handler import ...`
- Line 40: `from ..types import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_provider_handlers/cohere_passthrough_logging_handler.py
- Line 30: `from .base_passthrough_logging_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/llm_provider_handlers/vertex_passthrough_logging_handler.py
- Line 41: `from ..success_handler import ...`
- Line 42: `from ..types import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/pass_through_endpoints.py
- Line 68: `from .streaming_handler import ...`
- Line 69: `from .success_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/streaming_handler.py
- Line 32: `from .llm_provider_handlers.anthropic_passthrough_logging_handler import ...`
- Line 35: `from .llm_provider_handlers.vertex_passthrough_logging_handler import ...`
- Line 38: `from .success_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/pass_through_endpoints/success_handler.py
- Line 34: `from .llm_provider_handlers.anthropic_passthrough_logging_handler import ...`
- Line 37: `from .llm_provider_handlers.assembly_passthrough_logging_handler import ...`
- Line 40: `from .llm_provider_handlers.cohere_passthrough_logging_handler import ...`
- Line 43: `from .llm_provider_handlers.vertex_passthrough_logging_handler import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/proxy/proxy_cli.py
- Line 533: `from .proxy_server import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/realtime_api/main.py
- Line 30: `from ..litellm_core_utils.get_litellm_params import ...`
- Line 31: `from ..litellm_core_utils.litellm_logging import ...`
- Line 32: `from ..llms.azure.realtime.handler import ...`
- Line 33: `from ..llms.openai.realtime.handler import ...`
- Line 34: `from ..utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/responses/main.py
- Line 49: `from .streaming_iterator import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/router.py
- Line 178: `from .router_utils.pattern_match_deployments import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/router_strategy/lowest_tpm_rpm_v2.py
- Line 35: `from .base_routing_strategy import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/router_utils/cooldown_handlers.py
- Line 30: `from .router_callbacks.track_deployment_metrics import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/router_utils/pre_call_checks/prompt_caching_deployment_check.py
- Line 28: `from ..prompt_caching_cache import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/secret_managers/aws_secret_manager_v2.py
- Line 34: `from .base_secret_manager import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/secret_managers/hashicorp_secret_manager.py
- Line 34: `from .base_secret_manager import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/integrations/arize_phoenix.py
- Line 22: `from .arize import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/llms/anthropic.py
- Line 24: `from .openai import ...`
- Line 385: `from .openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/llms/bedrock.py
- Line 32: `from .openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/llms/databricks.py
- Line 33: `from .openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/llms/gemini.py
- Line 20: `from .vertex_ai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/passthrough_endpoints/vertex_ai.py
- Line 22: `from ..llms.vertex_ai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/realtime.py
- Line 20: `from .llms.openai import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/router.py
- Line 33: `from ..exceptions import ...`
- Line 34: `from .completion import ...`
- Line 35: `from .embedding import ...`
- Line 36: `from .llms.openai import ...`
- Line 37: `from .llms.vertex_ai import ...`
- Line 38: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/types/utils.py
- Line 57: `from ..litellm_core_utils.core_helpers import ...`
- Line 58: `from .guardrails import ...`
- Line 59: `from .llms.openai import ...`
- Line 73: `from .rerank import ...`
- Line 76: `from .vector_stores import ...`

#### /home/graham/workspace/experiments/llm_call/repos/litellm/litellm/utils.py
- Line 262: `from ._logging import ...`
- Line 263: `from .caching.caching import ...`
- Line 270: `from .exceptions import ...`
- Line 287: `from .proxy._types import ...`
- Line 288: `from .types.llms.openai import ...`
- Line 293: `from .types.router import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/__init__.py
- Line 15: `from .hookspecs import ...`
- Line 16: `from .errors import ...`
- Line 20: `from .models import ...`
- Line 39: `from .utils import ...`
- Line 40: `from .embeddings import ...`
- Line 41: `from .templates import ...`
- Line 42: `from .plugins import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/__main__.py
- Line 15: `from .cli import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/cli.py
- Line 58: `from .migrations import ...`
- Line 59: `from .plugins import ...`
- Line 60: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/embeddings.py
- Line 15: `from .models import ...`
- Line 16: `from .embeddings_migrations import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/models.py
- Line 23: `from .errors import ...`
- Line 44: `from .utils import ...`

#### /home/graham/workspace/experiments/llm_call/repos/llm/llm/plugins.py
- Line 20: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/__init__.py
- Line 1: `from .core import ...`
- Line 2: `from .core.llm_interface import ...`
- Line 3: `from .core.validation import ...`
- Line 23: `from .core import ...`
- Line 27: `from .llm_interface import ...`
- Line 34: `from .config import ...`
- Line 35: `from .validators import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/cli/__init__.py
- Line 19: `from .main import ...`
- Line 20: `from .slash_mcp_mixin import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/cli/main.py
- Line 72: `from .slash_mcp_mixin import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/core/api/mcp_handler_wrapper.py
- Line 15: `from .mcp_handler import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/core/config_manager.py
- Line 16: `from .config.settings import ...`
- Line 17: `from .config.loader import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/core/providers/claude/claude_executor.py
- Line 35: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/core/providers/claude/db_manager.py
- Line 32: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/core/validation/builtin_strategies/__init__.py
- Line 10: `from . import ...`
- Line 11: `from . import ...`
- Line 12: `from . import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/archive/root_cleanup/v4_claude_validator/litellm_client_poc.py
- Line 43: `from ..poc_retry_manager import ...`
- Line 49: `from .poc_validation_strategies import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/archive/root_cleanup/v4_claude_validator/litellm_client_poc_async.py
- Line 20: `from .litellm_client_poc import ...`
- Line 36: `from ..async_polling_manager import ...`

#### /home/graham/workspace/experiments/llm_call/src/llm_call/rl_integration/integration_example.py
- Line 9: `from .provider_selector import ...`

#### /home/graham/workspace/experiments/marker/archive/20250605/src/marker/rl_integration/strategy_selector_backup.py
- Line 34: `from .feature_extractor import ...`

#### /home/graham/workspace/experiments/marker/examples/litellm/mcp_litellm/engine.py
- Line 72: `from .models import ...`
- Line 79: `from .litellm_call import ...`
- Line 80: `from .retry_llm_call import ...`
- Line 81: `from .parser import ...`
- Line 122: `from .parser import ...`

#### /home/graham/workspace/experiments/marker/examples/litellm/mcp_litellm/litellm_call.py
- Line 38: `from .multimodal_utils import ...`
- Line 42: `from .initialize_litellm_cache import ...`

#### /home/graham/workspace/experiments/marker/examples/litellm/mcp_litellm/main.py
- Line 39: `from .models import ...`
- Line 46: `from .engine import ...`
- Line 47: `from .initialize_litellm_cache import ...`
- Line 49: `from .utils.db.arango_utils import ...`

#### /home/graham/workspace/experiments/marker/examples/litellm/mcp_litellm/parser.py
- Line 69: `from .models import ...`

#### /home/graham/workspace/experiments/marker/finetuning/unsloth/trainers.py
- Line 47: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/__init__.py
- Line 17: `from .__version__ import ...`
- Line 18: `from .io import ...`
- Line 19: `from .plotting import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/backends/__init__.py
- Line 15: `from .image_conversion import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/backends/image_conversion.py
- Line 20: `from .base import ...`
- Line 21: `from .ghostscript_backend import ...`
- Line 22: `from .pdfium_backend import ...`
- Line 23: `from .poppler_backend import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/cli.py
- Line 27: `from . import ...`
- Line 28: `from . import ...`
- Line 29: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/core.py
- Line 41: `from .backends import ...`
- Line 42: `from .utils import ...`
- Line 43: `from .utils import ...`
- Line 44: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/handlers.py
- Line 30: `from .core import ...`
- Line 31: `from .parsers import ...`
- Line 32: `from .parsers import ...`
- Line 33: `from .parsers import ...`
- Line 34: `from .parsers import ...`
- Line 35: `from .utils import ...`
- Line 36: `from .utils import ...`
- Line 37: `from .utils import ...`
- Line 38: `from .utils import ...`
- Line 39: `from .utils import ...`
- Line 40: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/io.py
- Line 21: `from .handlers import ...`
- Line 22: `from .utils import ...`
- Line 23: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/__init__.py
- Line 15: `from .hybrid import ...`
- Line 16: `from .lattice import ...`
- Line 17: `from .network import ...`
- Line 18: `from .stream import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/base.py
- Line 24: `from ..core import ...`
- Line 25: `from ..utils import ...`
- Line 26: `from ..utils import ...`
- Line 27: `from ..utils import ...`
- Line 28: `from ..utils import ...`
- Line 29: `from ..utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/hybrid.py
- Line 20: `from ..utils import ...`
- Line 21: `from ..utils import ...`
- Line 22: `from .base import ...`
- Line 23: `from .lattice import ...`
- Line 24: `from .network import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/lattice.py
- Line 20: `from ..backends import ...`
- Line 21: `from ..image_processing import ...`
- Line 22: `from ..image_processing import ...`
- Line 23: `from ..image_processing import ...`
- Line 24: `from ..image_processing import ...`
- Line 25: `from ..utils import ...`
- Line 26: `from ..utils import ...`
- Line 27: `from ..utils import ...`
- Line 28: `from ..utils import ...`
- Line 29: `from ..utils import ...`
- Line 30: `from ..utils import ...`
- Line 31: `from .base import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/network.py
- Line 27: `from ..core import ...`
- Line 28: `from ..core import ...`
- Line 29: `from ..core import ...`
- Line 30: `from ..core import ...`
- Line 31: `from ..utils import ...`
- Line 32: `from ..utils import ...`
- Line 33: `from ..utils import ...`
- Line 34: `from ..utils import ...`
- Line 35: `from ..utils import ...`
- Line 36: `from ..utils import ...`
- Line 37: `from ..utils import ...`
- Line 38: `from .base import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/parsers/stream.py
- Line 17: `from ..core import ...`
- Line 18: `from ..utils import ...`
- Line 19: `from ..utils import ...`
- Line 20: `from ..utils import ...`
- Line 21: `from ..utils import ...`
- Line 22: `from .base import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/camelot/plotting.py
- Line 26: `from .utils import ...`
- Line 27: `from .utils import ...`
- Line 28: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_common.py
- Line 40: `from .conftest import ...`
- Line 41: `from .conftest import ...`
- Line 42: `from .data import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_hybrid.py
- Line 35: `from .data import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_lattice.py
- Line 35: `from .data import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_network.py
- Line 35: `from .data import ...`

#### /home/graham/workspace/experiments/marker/repos/camelot/tests/test_stream.py
- Line 35: `from .data import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/argparser.py
- Line 17: `from .settings.base import ...`
- Line 18: `from .utils.io import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/feature_flags/__init__.py
- Line 15: `from .base import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/feature_flags/base.py
- Line 29: `from .stale_feature_flags import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/utils/contextlog.py
- Line 32: `from .common import ...`
- Line 33: `from .io import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/utils/io.py
- Line 38: `from .exceptions import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_export/api.py
- Line 41: `from .models import ...`
- Line 42: `from .serializers import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_export/mixins.py
- Line 203: `from .serializers import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_export/serializers.py
- Line 29: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_export/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/api.py
- Line 51: `from .functions import ...`
- Line 58: `from .models import ...`
- Line 59: `from .serializers import ...`
- Line 60: `from .uploader import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/functions.py
- Line 28: `from .models import ...`
- Line 29: `from .serializers import ...`
- Line 30: `from .uploader import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/serializers.py
- Line 19: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/uploader.py
- Line 32: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/data_import/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/all_api.py
- Line 29: `from .localfiles.api import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/azure_blob/api.py
- Line 33: `from .openapi_schema import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/filesystem.py
- Line 22: `from .base import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/functions.py
- Line 20: `from .azure_blob.api import ...`
- Line 21: `from .gcs.api import ...`
- Line 22: `from .redis.api import ...`
- Line 23: `from .s3.api import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/gcs/api.py
- Line 33: `from .openapi_schema import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/localfiles/api.py
- Line 33: `from .openapi_schema import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/models.py
- Line 17: `from .azure_blob.models import ...`
- Line 23: `from .s3.models import ...`
- Line 29: `from .gcs.models import ...`
- Line 35: `from .redis.models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/redis/api.py
- Line 32: `from .openapi_schema import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/s3/api.py
- Line 33: `from .openapi_schema import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/jwt_auth/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/labels_manager/api.py
- Line 34: `from .functions import ...`
- Line 35: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/labels_manager/serializers.py
- Line 22: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/labels_manager/urls.py
- Line 18: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/ml/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/ml_model_providers/admin.py
- Line 17: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/ml_models/admin.py
- Line 17: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/organizations/forms.py
- Line 17: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/projects/tests/test_api.py
- Line 31: `from .factories import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/projects/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tasks/urls.py
- Line 18: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/conftest.py
- Line 63: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/jwt_auth/test_auth.py
- Line 43: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/jwt_auth/test_middleware.py
- Line 43: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/jwt_auth/test_models.py
- Line 44: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/sdk/fixtures.py
- Line 32: `from .common import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_annotations.py
- Line 38: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_exception.py
- Line 47: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_next_task.py
- Line 53: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_predictions.py
- Line 39: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/users/product_tours/api.py
- Line 22: `from .serializers import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/users/product_tours/serializers.py
- Line 23: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/users/serializers.py
- Line 22: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/webhooks/api.py
- Line 26: `from .models import ...`
- Line 27: `from .serializers import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/webhooks/models.py
- Line 26: `from .serializers_for_hooks import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/webhooks/serializers.py
- Line 17: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/webhooks/urls.py
- Line 17: `from . import ...`

#### /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/webhooks/utils.py
- Line 28: `from .models import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/__init__.py
- Line 264: `from .models import ...`
- Line 265: `from .models import ...`
- Line 266: `from .save import ...`
- Line 267: `from .chat_templates import ...`
- Line 268: `from .tokenizer_utils import ...`
- Line 269: `from .trainer import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/chat_templates.py
- Line 51: `from .save import ...`
- Line 54: `from .tokenizer_utils import ...`
- Line 55: `from .models._utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/dataprep/__init__.py
- Line 29: `from .synthetic import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/dataprep/synthetic.py
- Line 52: `from .synthetic_configs import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/__init__.py
- Line 29: `from .cross_entropy_loss import ...`
- Line 34: `from .rms_layernorm import ...`
- Line 39: `from .layernorm import ...`
- Line 43: `from .rope_embedding import ...`
- Line 44: `from .swiglu import ...`
- Line 45: `from .geglu import ...`
- Line 51: `from .fast_lora import ...`
- Line 61: `from .utils import ...`
- Line 63: `from .flex_attention import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/cross_entropy_loss.py
- Line 36: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/fast_lora.py
- Line 33: `from .utils import ...`
- Line 193: `from .swiglu import ...`
- Line 208: `from .geglu import ...`
- Line 223: `from .geglu import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/geglu.py
- Line 35: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/layernorm.py
- Line 36: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/moe/tests/test_grouped_gemm.py
- Line 54: `from .common import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/moe/tests/test_qwen3_moe.py
- Line 46: `from .moe_utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/rms_layernorm.py
- Line 35: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/rope_embedding.py
- Line 35: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/swiglu.py
- Line 35: `from .utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/__init__.py
- Line 29: `from .llama import ...`
- Line 30: `from .loader import ...`
- Line 31: `from .mistral import ...`
- Line 32: `from .qwen2 import ...`
- Line 33: `from .qwen3 import ...`
- Line 34: `from .qwen3_moe import ...`
- Line 35: `from .granite import ...`
- Line 36: `from .dpo import ...`
- Line 37: `from ._utils import ...`
- Line 38: `from .rl import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/cohere.py
- Line 32: `from .llama import ...`
- Line 33: `from ._utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/gemma.py
- Line 32: `from .llama import ...`
- Line 33: `from ._utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/gemma2.py
- Line 32: `from .llama import ...`
- Line 33: `from ._utils import ...`
- Line 34: `from .gemma import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/granite.py
- Line 32: `from .llama import ...`
- Line 34: `from ._utils import ...`
- Line 35: `from .llama import ...`
- Line 39: `from .mistral import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/llama.py
- Line 38: `from ._utils import ...`
- Line 39: `from ._utils import ...`
- Line 40: `from ._utils import ...`
- Line 56: `from ..kernels import ...`
- Line 57: `from ..tokenizer_utils import ...`
- Line 60: `from .vision import ...`
- Line 86: `from ..save import ...`
- Line 2774: `from .rl import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/loader.py
- Line 32: `from ._utils import ...`
- Line 40: `from .granite import ...`
- Line 41: `from .llama import ...`
- Line 42: `from .mistral import ...`
- Line 43: `from .qwen2 import ...`
- Line 44: `from .qwen3 import ...`
- Line 45: `from .qwen3_moe import ...`
- Line 46: `from .cohere import ...`
- Line 50: `from .loader_utils import ...`
- Line 77: `from .gemma import ...`
- Line 79: `from .gemma2 import ...`
- Line 82: `from ._utils import ...`
- Line 466: `from ..kernels import ...`
- Line 470: `from .vision import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/loader_utils.py
- Line 32: `from .mapper import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/mistral.py
- Line 32: `from .llama import ...`
- Line 34: `from ._utils import ...`
- Line 35: `from .llama import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/qwen2.py
- Line 32: `from .llama import ...`
- Line 33: `from .llama import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/qwen3.py
- Line 32: `from .llama import ...`
- Line 34: `from ._utils import ...`
- Line 36: `from .llama import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/qwen3_moe.py
- Line 32: `from .llama import ...`
- Line 34: `from ._utils import ...`
- Line 35: `from .llama import ...`
- Line 39: `from .qwen3 import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/rl.py
- Line 46: `from .rl_replacements import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/models/vision.py
- Line 46: `from ..kernels import ...`
- Line 49: `from ._utils import ...`
- Line 50: `from ._utils import ...`
- Line 51: `from ..save import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/registry/__init__.py
- Line 15: `from ._deepseek import ...`
- Line 16: `from ._gemma import ...`
- Line 17: `from ._llama import ...`
- Line 18: `from ._mistral import ...`
- Line 19: `from ._phi import ...`
- Line 20: `from ._qwen import ...`
- Line 21: `from .registry import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/save.py
- Line 47: `from .kernels import ...`
- Line 52: `from .tokenizer_utils import ...`
- Line 2240: `from .models.loader_utils import ...`

#### /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/trainer.py
- Line 40: `from . import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/granger_slash_mcp_mixin.py
- Line 31: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/__init__.py
- Line 9: `from .base import ...`
- Line 10: `from .extract import ...`
- Line 11: `from .arangodb import ...`
- Line 12: `from .claude import ...`
- Line 13: `from .qa import ...`
- Line 14: `from .workflow import ...`
- Line 15: `from .test import ...`
- Line 16: `from .serve import ...`
- Line 17: `from .granger import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/arangodb.py
- Line 13: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/claude.py
- Line 15: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/extract.py
- Line 12: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/granger.py
- Line 33: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/qa.py
- Line 13: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/serve.py
- Line 16: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/test.py
- Line 26: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/cli/slash_commands/workflow.py
- Line 14: `from .base import ...`

#### /home/graham/workspace/experiments/marker/src/marker/core/services/adapters/__init__.py
- Line 10: `from .claude_table_adapter import ...`

#### /home/graham/workspace/experiments/marker/src/marker/handlers/__init__.py
- Line 9: `from ..integrations.marker_module import ...`

#### /home/graham/workspace/experiments/marker/src/marker/integrations/__init__.py
- Line 9: `from .marker_module import ...`

#### /home/graham/workspace/experiments/marker/src/marker/rl_integration/deployment.py
- Line 14: `from .strategy_selector import ...`

#### /home/graham/workspace/experiments/marker/src/marker/rl_integration/strategy_selector.py
- Line 21: `from .feature_extractor import ...`

#### /home/graham/workspace/experiments/marker/src/messages/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/marker/src/messages/mcp/messages_prompts.py
- Line 16: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/marker/src/messages/mcp/server.py
- Line 10: `from .messages_prompts import ...`
- Line 11: `from .prompts import ...`

#### /home/graham/workspace/experiments/marker/tests/utils/__init__.py
- Line 26: `from .utils import ...`

#### /home/graham/workspace/experiments/mcp-screenshot/src/mcp_screenshot/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/mcp-screenshot/src/mcp_screenshot/core/history.py
- Line 43: `from .constants import ...`
- Line 44: `from .image_similarity import ...`

#### /home/graham/workspace/experiments/mcp-screenshot/src/mcp_screenshot/integrations/__init__.py
- Line 2: `from .mcp_screenshot_module import ...`

#### /home/graham/workspace/experiments/mcp-screenshot/src/mcp_screenshot/mcp/mcp_screenshot_prompts.py
- Line 12: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/__init__.py
- Line 4: `from .contextual_bandit import ...`
- Line 5: `from .rl_module import ...`
- Line 8: `from .rl_module import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/__init__.py
- Line 6: `from .dqn.vanilla_dqn import ...`
- Line 7: `from .bandits.contextual import ...`
- Line 8: `from .hierarchical import ...`
- Line 9: `from .ppo.ppo import ...`
- Line 10: `from .a3c.a3c import ...`
- Line 13: `from .curriculum import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/a3c/__init__.py
- Line 13: `from .a3c import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/a3c/a3c.py
- Line 29: `from ...core.base import ...`
- Line 30: `from ...monitoring.tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/bandits/__init__.py
- Line 6: `from .contextual import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/bandits/contextual.py
- Line 12: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/__init__.py
- Line 6: `from .base import ...`
- Line 12: `from .automatic import ...`
- Line 13: `from .progressive import ...`
- Line 14: `from .adaptive import ...`
- Line 15: `from .meta_curriculum import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/adaptive.py
- Line 24: `from .base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/automatic.py
- Line 22: `from .base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/base.py
- Line 25: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/meta_curriculum.py
- Line 24: `from .base import ...`
- Line 28: `from ...algorithms.meta.maml import ...`
- Line 29: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/curriculum/progressive.py
- Line 20: `from .base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/dqn/__init__.py
- Line 6: `from .vanilla_dqn import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/dqn/vanilla_dqn.py
- Line 16: `from ...core.base import ...`
- Line 17: `from ...core.replay_buffer import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/gnn/__init__.py
- Line 10: `from .graph_networks import ...`
- Line 11: `from .gnn_integration import ...`
- Line 12: `from .dynamic_graphs import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/gnn/dynamic_graphs.py
- Line 23: `from .graph_networks import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/gnn/gnn_integration.py
- Line 22: `from .graph_networks import ...`
- Line 23: `from ...core.base import ...`
- Line 24: `from ..dqn.vanilla_dqn import ...`
- Line 25: `from ..ppo.ppo import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/hierarchical/__init__.py
- Line 6: `from .options_framework import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/hierarchical/options_framework.py
- Line 18: `from ...core.base import ...`
- Line 19: `from ...core.replay_buffer import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/irl/__init__.py
- Line 10: `from .base_irl import ...`
- Line 11: `from .max_entropy_irl import ...`
- Line 12: `from .behavioral_cloning import ...`
- Line 13: `from .gail import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/irl/base_irl.py
- Line 23: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/irl/behavioral_cloning.py
- Line 23: `from .base_irl import ...`
- Line 24: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/irl/gail.py
- Line 23: `from .base_irl import ...`
- Line 24: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/irl/max_entropy_irl.py
- Line 22: `from .base_irl import ...`
- Line 23: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/marl/__init__.py
- Line 10: `from .base_marl import ...`
- Line 11: `from .independent_q import ...`
- Line 12: `from .communication import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/marl/base_marl.py
- Line 27: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/marl/independent_q.py
- Line 24: `from .base_marl import ...`
- Line 25: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/meta/__init__.py
- Line 10: `from .maml import ...`
- Line 11: `from .reptile import ...`
- Line 12: `from .task_distribution import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/meta/maml.py
- Line 23: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/__init__.py
- Line 10: `from .base_morl import ...`
- Line 11: `from .weighted_sum import ...`
- Line 12: `from .pareto_q_learning import ...`
- Line 13: `from .mo_ppo import ...`
- Line 14: `from .entropy_aware_morl import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/base_morl.py
- Line 23: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/entropy_aware_morl.py
- Line 23: `from .mo_ppo import ...`
- Line 24: `from .base_morl import ...`
- Line 25: `from ...core.base import ...`
- Line 26: `from ...monitoring.entropy_tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/mo_ppo.py
- Line 24: `from .base_morl import ...`
- Line 25: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/pareto_q_learning.py
- Line 23: `from .base_morl import ...`
- Line 24: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/morl/weighted_sum.py
- Line 23: `from .base_morl import ...`
- Line 24: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/ppo/__init__.py
- Line 6: `from .ppo import ...`
- Line 7: `from .entropy_aware_ppo import ...`
- Line 8: `from .kl_cov_ppo import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/ppo/entropy_aware_ppo.py
- Line 32: `from .ppo import ...`
- Line 33: `from ...core.base import ...`
- Line 34: `from ...core.covariance_analyzer import ...`
- Line 35: `from ...monitoring.entropy_tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/ppo/kl_cov_ppo.py
- Line 32: `from .ppo import ...`
- Line 33: `from ...core.base import ...`
- Line 34: `from ...core.covariance_analyzer import ...`
- Line 35: `from ...monitoring.entropy_tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/algorithms/ppo/ppo.py
- Line 18: `from ...core.base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/benchmarks/__init__.py
- Line 6: `from .benchmark_suite import ...`
- Line 7: `from .algorithm_benchmarks import ...`
- Line 12: `from .integration_benchmarks import ...`
- Line 18: `from .performance_profiler import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/benchmarks/algorithm_benchmarks.py
- Line 22: `from .benchmark_suite import ...`
- Line 23: `from ..core.base import ...`
- Line 24: `from ..core.algorithm_selector import ...`
- Line 25: `from ..algorithms import ...`
- Line 26: `from ..algorithms.marl import ...`
- Line 27: `from ..algorithms.morl import ...`
- Line 28: `from ..algorithms.bandits import ...`
- Line 301: `from ..algorithms.morl import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/benchmarks/integration_benchmarks.py
- Line 23: `from .benchmark_suite import ...`
- Line 24: `from ..integrations.module_communicator import ...`
- Line 30: `from ..integrations.arangodb_optimizer import ...`
- Line 31: `from ..core.base import ...`
- Line 260: `from ..algorithms.morl import ...`
- Line 326: `from ..algorithms.morl import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/core/__init__.py
- Line 6: `from .base import ...`
- Line 13: `from .replay_buffer import ...`
- Line 18: `from .covariance_analyzer import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/core/algorithm_selector.py
- Line 39: `from ..core.base import ...`
- Line 40: `from ..algorithms.ppo import ...`
- Line 41: `from ..algorithms.a3c import ...`
- Line 42: `from ..algorithms.dqn import ...`
- Line 43: `from ..algorithms.bandits import ...`
- Line 44: `from ..algorithms.hierarchical import ...`
- Line 539: `from ..algorithms.dqn.vanilla_dqn import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/core/base.py
- Line 13: `from ..monitoring.entropy_tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/core/entropy_aware_selector.py
- Line 22: `from .algorithm_selector import ...`
- Line 23: `from ..core.base import ...`
- Line 24: `from ..monitoring.entropy_tracker import ...`
- Line 25: `from ..algorithms.ppo import ...`
- Line 71: `from .algorithm_selector import ...`
- Line 499: `from .algorithm_selector import ...`
- Line 536: `from ..algorithms.ppo import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/core/replay_buffer.py
- Line 12: `from .base import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/integrations/__init__.py
- Line 14: `from .arangodb_optimizer import ...`
- Line 15: `from .module_communicator import ...`
- Line 21: `from .rl_module_communicator import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/integrations/arangodb_optimizer.py
- Line 22: `from ..algorithms.ppo import ...`
- Line 23: `from ..core.base import ...`
- Line 24: `from ..monitoring.tracker import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/integrations/module_communicator.py
- Line 33: `from ..core.base import ...`
- Line 34: `from ..core.algorithm_selector import ...`
- Line 38: `from ..algorithms.marl import ...`
- Line 39: `from ..algorithms.gnn import ...`
- Line 40: `from ..algorithms.morl import ...`
- Line 41: `from ..algorithms.curriculum import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/monitoring/__init__.py
- Line 6: `from .entropy_tracker import ...`
- Line 7: `from .entropy_visualizer import ...`

#### /home/graham/workspace/experiments/rl_commons/src/rl_commons/optimization_agent.py
- Line 10: `from .contextual_bandit import ...`

#### /home/graham/workspace/experiments/sparta/archive/claude-module-communicator-files/src/schema_negotiator_dynamic.py
- Line 20: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/sparta/archive/claude-module-communicator-files/utils/progress_utils.py
- Line 26: `from .progress_tracker import ...`

#### /home/graham/workspace/experiments/sparta/archive/deprecated_tests/test_sparta.py
- Line 24: `from .interaction_framework import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/communication/archive/schema_negotiator_dynamic.py
- Line 20: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/communication/archive/slash_commands.py
- Line 27: `from .module_communicator import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/communication/src/core/progress_utils.py
- Line 26: `from .progress_tracker import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/downloaders/__init__.py
- Line 3: `from .enhanced_downloader import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/downloaders/enhanced_downloader.py
- Line 22: `from .download_utils import ...`
- Line 29: `from .url_extractor import ...`
- Line 30: `from .robots_handler import ...`
- Line 268: `from ..reports.universal_report_generator import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/extractors/__init__.py
- Line 2: `from .nist_control_extractor import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/formatters/__init__.py
- Line 3: `from .nist_arango_formatter import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/graph/__init__.py
- Line 5: `from .arango_hybrid import ...`
- Line 6: `from .arango_intelligent_hybrid import ...`
- Line 7: `from .arango_intelligent_hybrid_v2 import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/__init__.py
- Line 7: `from .pipeline import ...`
- Line 8: `from .download_metrics import ...`
- Line 9: `from .download_orchestrator import ...`
- Line 10: `from .paywall_researcher import ...`
- Line 11: `from .download_analyzer import ...`
- Line 12: `from .domain_profiler import ...`
- Line 13: `from .smart_paywall_research import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/document_processor.py
- Line 18: `from .constants import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/download_orchestrator.py
- Line 49: `from .download_metrics import ...`
- Line 50: `from .paywall_researcher import ...`
- Line 51: `from .nist_oscal_downloader import ...`
- Line 52: `from .sparta_enricher import ...`
- Line 53: `from ..formatters.nist_arango_formatter import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/enrichment.py
- Line 22: `from ..extractors.nist_control_extractor import ...`
- Line 23: `from ..sparta_mcp_server.core.mitre_integration import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/marker_integration.py
- Line 18: `from .constants import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/paywall_researcher.py
- Line 45: `from .research_utils import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/pipeline.py
- Line 49: `from .constants import ...`
- Line 54: `from .stats import ...`
- Line 55: `from .document_processor import ...`
- Line 56: `from .qa_generator import ...`
- Line 57: `from .marker_integration import ...`
- Line 58: `from .cache import ...`
- Line 59: `from .concurrent_processor import ...`
- Line 60: `from .performance_metrics import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/qa_generator.py
- Line 17: `from .constants import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/smart_paywall_research.py
- Line 35: `from .domain_profiler import ...`
- Line 36: `from .paywall_researcher import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/ingestion/sparta_enricher.py
- Line 43: `from ..extractors.nist_control_extractor import ...`
- Line 44: `from .nist_oscal_downloader import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/manifest/__init__.py
- Line 8: `from .manifest_generator import ...`
- Line 9: `from .schema_negotiator import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/manifest/cli.py
- Line 22: `from .manifest_generator import ...`
- Line 23: `from .schema_negotiator import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/reports/__init__.py
- Line 11: `from .pytest_report_runner import ...`
- Line 12: `from .agent_report_adapter import ...`
- Line 23: `from .report_config import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/reports/_archive_custom_reporters/cli.py
- Line 14: `from .enhanced_test_reporter import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/reports/_archive_custom_reporters/enhanced_test_reporter.py
- Line 39: `from .universal_report_generator import ...`
- Line 40: `from .report_config import ...`

#### /home/graham/workspace/experiments/sparta/archive/sparta_old/utils/__init__.py
- Line 2: `from .test_reporter import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/downloader.py
- Line 32: `from .downloader_base import ...`
- Line 38: `from .downloader_strategies import ...`
- Line 42: `from .downloader_utils import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/downloader_strategies.py
- Line 30: `from .downloader_base import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/downloader_utils.py
- Line 28: `from .downloader_base import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/reports/__init__.py
- Line 13: `from .pytest_report_runner import ...`
- Line 14: `from .agent_report_adapter import ...`
- Line 25: `from .report_config import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/reports/_archive_custom_reporters/cli.py
- Line 56: `from .enhanced_test_reporter import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/core/reports/_archive_custom_reporters/enhanced_test_reporter.py
- Line 77: `from .universal_report_generator import ...`
- Line 78: `from .report_config import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/handlers/__init__.py
- Line 9: `from ..integrations.sparta_module import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/__init__.py
- Line 2: `from .sparta_module import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module.py
- Line 45: `from .sparta_module_real_api import ...`
- Line 66: `from .sparta_mock_data import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_real_api.py
- Line 7: `from .real_apis_fixed import ...`
- Line 27: `from .sparta_mock_data import ...`
- Line 40: `from .sparta_mock_data import ...`
- Line 51: `from .sparta_mock_data import ...`
- Line 63: `from .sparta_mock_data import ...`
- Line 74: `from .sparta_mock_data import ...`
- Line 86: `from .sparta_mock_data import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_with_mock.py
- Line 22: `from .sparta_mock_data import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/mcp/server.py
- Line 10: `from .sparta_prompts import ...`
- Line 11: `from .prompts import ...`

#### /home/graham/workspace/experiments/sparta/src/sparta/mcp/sparta_prompts.py
- Line 12: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/__init__.py
- Line 247: `from .models import ...`
- Line 248: `from .models import ...`
- Line 249: `from .save import ...`
- Line 250: `from .chat_templates import ...`
- Line 251: `from .tokenizer_utils import ...`
- Line 252: `from .trainer import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/chat_templates.py
- Line 33: `from .save import ...`
- Line 36: `from .tokenizer_utils import ...`
- Line 37: `from .models._utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/dataprep/__init__.py
- Line 15: `from .synthetic import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/dataprep/synthetic.py
- Line 33: `from .synthetic_configs import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/__init__.py
- Line 15: `from .cross_entropy_loss import ...`
- Line 20: `from .rms_layernorm import ...`
- Line 25: `from .layernorm import ...`
- Line 29: `from .rope_embedding import ...`
- Line 30: `from .swiglu import ...`
- Line 31: `from .geglu import ...`
- Line 37: `from .fast_lora import ...`
- Line 47: `from .utils import ...`
- Line 49: `from .flex_attention import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/cross_entropy_loss.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/fast_lora.py
- Line 16: `from .utils import ...`
- Line 176: `from .swiglu import ...`
- Line 191: `from .geglu import ...`
- Line 206: `from .geglu import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/geglu.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/layernorm.py
- Line 19: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/moe/tests/test_grouped_gemm.py
- Line 26: `from .common import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/moe/tests/test_qwen3_moe.py
- Line 17: `from .moe_utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/rms_layernorm.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/rope_embedding.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/swiglu.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/__init__.py
- Line 15: `from .llama import ...`
- Line 16: `from .loader import ...`
- Line 17: `from .mistral import ...`
- Line 18: `from .qwen2 import ...`
- Line 19: `from .qwen3 import ...`
- Line 20: `from .qwen3_moe import ...`
- Line 21: `from .granite import ...`
- Line 22: `from .dpo import ...`
- Line 23: `from ._utils import ...`
- Line 24: `from .rl import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/cohere.py
- Line 15: `from .llama import ...`
- Line 16: `from ._utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/gemma.py
- Line 15: `from .llama import ...`
- Line 16: `from ._utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/gemma2.py
- Line 15: `from .llama import ...`
- Line 16: `from ._utils import ...`
- Line 17: `from .gemma import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/granite.py
- Line 15: `from .llama import ...`
- Line 17: `from ._utils import ...`
- Line 18: `from .llama import ...`
- Line 22: `from .mistral import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/llama.py
- Line 20: `from ._utils import ...`
- Line 21: `from ._utils import ...`
- Line 22: `from ._utils import ...`
- Line 43: `from ..kernels import ...`
- Line 44: `from ..tokenizer_utils import ...`
- Line 47: `from .vision import ...`
- Line 73: `from ..save import ...`
- Line 2809: `from .rl import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/loader.py
- Line 15: `from ._utils import ...`
- Line 23: `from .granite import ...`
- Line 24: `from .llama import ...`
- Line 25: `from .mistral import ...`
- Line 26: `from .qwen2 import ...`
- Line 27: `from .qwen3 import ...`
- Line 28: `from .qwen3_moe import ...`
- Line 29: `from .cohere import ...`
- Line 33: `from .loader_utils import ...`
- Line 60: `from .gemma import ...`
- Line 62: `from .gemma2 import ...`
- Line 65: `from ._utils import ...`
- Line 449: `from ..kernels import ...`
- Line 453: `from .vision import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/loader_utils.py
- Line 15: `from .mapper import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/mistral.py
- Line 15: `from .llama import ...`
- Line 17: `from ._utils import ...`
- Line 18: `from .llama import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/qwen2.py
- Line 15: `from .llama import ...`
- Line 16: `from .llama import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/qwen3.py
- Line 15: `from .llama import ...`
- Line 17: `from ._utils import ...`
- Line 19: `from .llama import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/qwen3_moe.py
- Line 15: `from .llama import ...`
- Line 17: `from ._utils import ...`
- Line 18: `from .llama import ...`
- Line 22: `from .qwen3 import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/rl.py
- Line 29: `from .rl_replacements import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/models/vision.py
- Line 28: `from ..kernels import ...`
- Line 31: `from ._utils import ...`
- Line 32: `from ._utils import ...`
- Line 33: `from ..save import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/registry/__init__.py
- Line 1: `from ._deepseek import ...`
- Line 2: `from ._gemma import ...`
- Line 3: `from ._llama import ...`
- Line 4: `from ._mistral import ...`
- Line 5: `from ._phi import ...`
- Line 6: `from ._qwen import ...`
- Line 7: `from .registry import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/save.py
- Line 28: `from .kernels import ...`
- Line 33: `from .tokenizer_utils import ...`
- Line 2229: `from .models.loader_utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/trainer.py
- Line 23: `from . import ...`

#### /home/graham/workspace/experiments/fine_tuning/runpod_ops_project/runpod_ops/runpod_ops/__init__.py
- Line 24: `from .runpod_manager import ...`
- Line 25: `from .instance_optimizer import ...`
- Line 26: `from .cost_calculator import ...`
- Line 27: `from .instance_monitor import ...`
- Line 28: `from .training_orchestrator import ...`
- Line 29: `from .inference_server import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/granger_slash_mcp_mixin.py
- Line 26: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/main.py
- Line 13: `from ..core.config import ...`
- Line 14: `from ..core.enhanced_config import ...`
- Line 15: `from ..core.grokking_config import ...`
- Line 16: `from ..inference.generate import ...`
- Line 17: `from ..models.upload import ...`
- Line 18: `from ..training.enhanced_trainer import ...`
- Line 19: `from ..training.trainer import ...`
- Line 20: `from ..utils.logging import ...`
- Line 21: `from ..utils.memory import ...`
- Line 22: `from .granger_slash_mcp_mixin import ...`
- Line 48: `from ..data.thinking_enhancer import ...`
- Line 108: `from ..training.runpod_trainer import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/slash_mcp_integration.py
- Line 303: `from .unified_cli import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/unified_cli.py
- Line 33: `from ..data.thinking_enhancer import ...`
- Line 36: `from ..pipeline.complete_training_pipeline import ...`
- Line 37: `from ..training.runpod_training_ops import ...`
- Line 38: `from ..upload.hub_uploader import ...`
- Line 39: `from ..validation.model_validator import ...`
- Line 40: `from .slash_mcp_integration import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/unified_typer_cli.py
- Line 35: `from ..data.thinking_enhancer import ...`
- Line 36: `from ..evaluation.config import ...`
- Line 37: `from ..evaluation.evaluator import ...`
- Line 38: `from ..evaluation.litellm_evaluator import ...`
- Line 39: `from ..evaluation.multi_model_evaluator import ...`
- Line 40: `from ..inference.generate import ...`
- Line 41: `from ..inference.test_suite import ...`
- Line 44: `from ..pipeline.complete_training_pipeline import ...`
- Line 45: `from ..training.runpod_training_ops import ...`
- Line 46: `from ..upload.hub_uploader import ...`
- Line 47: `from ..validation.model_validator import ...`
- Line 48: `from .slash_mcp_mixin import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/core/enhanced_config.py
- Line 29: `from .grokking_config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/data/evaluation.py
- Line 23: `from ..core.enhanced_config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/data/thinking_enhancer.py
- Line 30: `from ..core.enhanced_config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/evaluation/__init__.py
- Line 25: `from .config import ...`
- Line 26: `from .dashboard import ...`
- Line 27: `from .entropy_evaluator import ...`
- Line 28: `from .evaluator import ...`
- Line 29: `from .litellm_evaluator import ...`
- Line 30: `from .multi_model_evaluator import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/evaluation/evaluator.py
- Line 32: `from .config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/evaluation/litellm_evaluator.py
- Line 760: `from .multi_model_evaluator import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/mcp/server.py
- Line 80: `from ..pipeline.complete_training_pipeline import ...`
- Line 126: `from ..data.thinking_enhancer import ...`
- Line 182: `from ..evaluation.litellm_evaluator import ...`
- Line 183: `from ..evaluation.config import ...`
- Line 215: `from ..training.runpod_trainer import ...`
- Line 237: `from ..training.runpod_training_ops import ...`
- Line 265: `from ..inference.generate import ...`
- Line 297: `from ..validation.model_validator import ...`
- Line 322: `from ..training.entropy_utils import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/mcp/unsloth_prompts.py
- Line 13: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/__init__.py
- Line 3: `from .dapo_rl import ...`
- Line 4: `from .enhanced_trainer import ...`
- Line 5: `from .entropy_aware_trainer import ...`
- Line 6: `from .entropy_utils import ...`
- Line 7: `from .grokking_callback import ...`
- Line 8: `from .runpod_trainer import ...`
- Line 9: `from .trainer import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/dapo_rl.py
- Line 41: `from ..utils.memory import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/enhanced_trainer.py
- Line 49: `from ..core.enhanced_config import ...`
- Line 50: `from ..data.loader import ...`
- Line 51: `from ..data.thinking_enhancer import ...`
- Line 52: `from ..utils.memory import ...`
- Line 53: `from .grokking_callback import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/grokking_callback.py
- Line 8: `from ..core.grokking_config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/runpod_trainer.py
- Line 18: `from ..core.enhanced_config import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/training/trainer.py
- Line 40: `from ..core.config import ...`
- Line 41: `from ..data.loader import ...`
- Line 42: `from ..utils.memory import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/upload/__init__.py
- Line 3: `from .entropy_aware_hub_uploader import ...`
- Line 8: `from .hub_uploader import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/unsloth/utils/__init__.py
- Line 3: `from .logging import ...`
- Line 4: `from .memory import ...`
- Line 5: `from .tensorboard_verifier import ...`

#### /home/graham/workspace/experiments/fine_tuning/src/fine_tuning/mcp/server.py
- Line 10: `from .fine_tuning_prompts import ...`
- Line 11: `from .prompts import ...`

#### /home/graham/workspace/experiments/world_model/src/world_model/__init__.py
- Line 4: `from .world_model_module import ...`

#### /home/graham/workspace/experiments/world_model/src/world_model/anomaly.py
- Line 10: `from .core import ...`

#### /home/graham/workspace/experiments/world_model/src/world_model/predictor.py
- Line 10: `from .core import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/20250605/src/youtube_transcripts/arango_integration_old.py
- Line 29: `from .arango_connection import ...`
- Line 30: `from .arango_operations import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/agentic-rag/refs/agents.py
- Line 39: `from .agent_types import ...`
- Line 40: `from .default_tools import ...`
- Line 41: `from .local_python_executor import ...`
- Line 42: `from .memory import ...`
- Line 43: `from .models import ...`
- Line 48: `from .monitoring import ...`
- Line 54: `from .remote_executors import ...`
- Line 55: `from .tools import ...`
- Line 56: `from .utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/lora-server/autoload/lora_manager.py
- Line 8: `from .config import ...`
- Line 9: `from .redis_manager import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/lora-server/autoload/redis_manager.py
- Line 5: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/lora-server/autoload/server.py
- Line 10: `from .config import ...`
- Line 11: `from .lora_manager import ...`
- Line 12: `from .redis_manager import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/api/main.py
- Line 3: `from .routes import ...`
- Line 4: `from .core.config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/api/routes/chat.py
- Line 5: `from ..models.api_models import ...`
- Line 6: `from ..core.config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/load_balancer.py
- Line 4: `from .db.session import ...`
- Line 5: `from .db.models import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/pod_utils.py
- Line 6: `from .model_configs import ...`
- Line 7: `from .db.session import ...`
- Line 8: `from .db.models import ...`
- Line 10: `from .inference_utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/scaling_manager.py
- Line 5: `from .pod_utils import ...`
- Line 6: `from .model_configs import ...`
- Line 7: `from .db.models import ...`
- Line 8: `from .db.session import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/trelis-mcp/doc-convert/src/doc_convert/__init__.py
- Line 1: `from .doc_convert import ...`
- Line 2: `from .__main__ import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/trelis-mcp/doc-convert/src/doc_convert/__main__.py
- Line 4: `from .doc_convert import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/trelis-mcp/pypi-mcp-test/src/pypi_mcp_test/__init__.py
- Line 9: `from .pypi_mcp_test import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/trelis-mcp/pypi-mcp-test/src/pypi_mcp_test/__main__.py
- Line 1: `from .pypi_mcp_test import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/tests/e2e/envs/__init__.py
- Line 23: `from .digit_completion import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/tests/e2e/envs/digit_completion/__init__.py
- Line 23: `from .task import ...`
- Line 24: `from .tokenizer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/__init__.py
- Line 22: `from .protocol import ...`
- Line 24: `from .utils.logging_utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/models/llama/megatron/__init__.py
- Line 15: `from .modeling_llama_megatron import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/models/llama/megatron/layers/__init__.py
- Line 15: `from .parallel_attention import ...`
- Line 16: `from .parallel_decoder import ...`
- Line 17: `from .parallel_mlp import ...`
- Line 18: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/models/llama/megatron/layers/parallel_decoder.py
- Line 28: `from .parallel_attention import ...`
- Line 29: `from .parallel_mlp import ...`
- Line 30: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/models/llama/megatron/modeling_llama_megatron.py
- Line 35: `from .layers import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/single_controller/base/__init__.py
- Line 15: `from .worker import ...`
- Line 16: `from .worker_group import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/single_controller/base/megatron/worker_group.py
- Line 17: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/single_controller/ray/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .megatron import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/single_controller/ray/megatron.py
- Line 19: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/__init__.py
- Line 30: `from .vllm_v_0_3_1.llm import ...`
- Line 31: `from .vllm_v_0_3_1.llm import ...`
- Line 32: `from .vllm_v_0_3_1 import ...`
- Line 35: `from .vllm_v_0_4_2.llm import ...`
- Line 36: `from .vllm_v_0_4_2.llm import ...`
- Line 37: `from .vllm_v_0_4_2 import ...`
- Line 40: `from .vllm_v_0_5_4.llm import ...`
- Line 41: `from .vllm_v_0_5_4.llm import ...`
- Line 42: `from .vllm_v_0_5_4 import ...`
- Line 45: `from .vllm_v_0_6_3.llm import ...`
- Line 46: `from .vllm_v_0_6_3.llm import ...`
- Line 47: `from .vllm_v_0_6_3 import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/arg_utils.py
- Line 23: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/llm.py
- Line 22: `from .arg_utils import ...`
- Line 23: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/llm_engine_sp.py
- Line 34: `from .arg_utils import ...`
- Line 35: `from .tokenizer import ...`
- Line 152: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/model_loader.py
- Line 27: `from .config import ...`
- Line 29: `from .weight_loaders import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/model_runner.py
- Line 34: `from .model_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_3_1/worker.py
- Line 33: `from .model_runner import ...`
- Line 34: `from .model_loader import ...`
- Line 35: `from .parallel_state import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/arg_utils.py
- Line 25: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/llm.py
- Line 22: `from .arg_utils import ...`
- Line 23: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/llm_engine_sp.py
- Line 35: `from .arg_utils import ...`
- Line 36: `from .tokenizer import ...`
- Line 37: `from .config import ...`
- Line 265: `from .spmd_gpu_executor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/model_loader.py
- Line 14: `from .config import ...`
- Line 15: `from .megatron_weight_loaders import ...`
- Line 16: `from .dtensor_weight_loaders import ...`
- Line 17: `from .hf_weight_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/model_runner.py
- Line 32: `from .model_loader import ...`
- Line 33: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/spmd_gpu_executor.py
- Line 28: `from .config import ...`
- Line 72: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_4_2/worker.py
- Line 34: `from .model_runner import ...`
- Line 35: `from .megatron_weight_loaders import ...`
- Line 36: `from .hf_weight_loader import ...`
- Line 37: `from .dtensor_weight_loaders import ...`
- Line 38: `from .parallel_state import ...`
- Line 39: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/arg_utils.py
- Line 26: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/llm.py
- Line 23: `from .arg_utils import ...`
- Line 24: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/llm_engine_sp.py
- Line 38: `from .arg_utils import ...`
- Line 39: `from .tokenizer import ...`
- Line 40: `from .config import ...`
- Line 288: `from .spmd_gpu_executor import ...`
- Line 309: `from .spmd_gpu_executor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/model_loader.py
- Line 29: `from .config import ...`
- Line 30: `from .megatron_weight_loaders import ...`
- Line 31: `from .dtensor_weight_loaders import ...`
- Line 32: `from .hf_weight_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/model_runner.py
- Line 36: `from .model_loader import ...`
- Line 37: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/spmd_gpu_executor.py
- Line 29: `from .config import ...`
- Line 75: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_5_4/worker.py
- Line 36: `from .model_runner import ...`
- Line 37: `from .megatron_weight_loaders import ...`
- Line 38: `from .hf_weight_loader import ...`
- Line 39: `from .dtensor_weight_loaders import ...`
- Line 40: `from .parallel_state import ...`
- Line 41: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/arg_utils.py
- Line 23: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/llm.py
- Line 27: `from .arg_utils import ...`
- Line 28: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/llm_engine_sp.py
- Line 53: `from .arg_utils import ...`
- Line 54: `from .config import ...`
- Line 55: `from .tokenizer import ...`
- Line 365: `from .spmd_gpu_executor import ...`
- Line 388: `from .spmd_gpu_executor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/model_loader.py
- Line 13: `from .config import ...`
- Line 14: `from .dtensor_weight_loaders import ...`
- Line 15: `from .hf_weight_loader import ...`
- Line 16: `from .megatron_weight_loaders import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/model_runner.py
- Line 44: `from .config import ...`
- Line 45: `from .model_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/spmd_gpu_executor.py
- Line 37: `from .config import ...`
- Line 83: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/third_party/vllm/vllm_v_0_6_3/worker.py
- Line 45: `from .config import ...`
- Line 46: `from .dtensor_weight_loaders import ...`
- Line 47: `from .hf_weight_loader import ...`
- Line 48: `from .megatron_weight_loaders import ...`
- Line 49: `from .model_runner import ...`
- Line 50: `from .parallel_state import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/__init__.py
- Line 15: `from . import ...`
- Line 16: `from .tokenizer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/dataset/__init__.py
- Line 15: `from .rl_dataset import ...`
- Line 16: `from .rm_dataset import ...`
- Line 17: `from .sft_dataset import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/debug/__init__.py
- Line 15: `from .performance import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/fs.py
- Line 22: `from .hdfs_io import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/megatron/pipeline_parallel.py
- Line 19: `from .sequence_parallel import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/actor/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .dp_actor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/critic/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .dp_critic import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/reward_model/__init__.py
- Line 15: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/reward_model/megatron/__init__.py
- Line 15: `from .reward_model import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/rollout/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .naive import ...`
- Line 17: `from .hf_rollout import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/rollout/hf_rollout.py
- Line 28: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/rollout/naive/__init__.py
- Line 15: `from .naive_rollout import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/rollout/naive/naive_rollout.py
- Line 31: `from ..base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/rollout/vllm_rollout/__init__.py
- Line 15: `from .vllm_rollout import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/sharding_manager/__init__.py
- Line 17: `from .base import ...`
- Line 18: `from .fsdp_ulysses import ...`
- Line 23: `from .megatron_vllm import ...`
- Line 31: `from .fsdp_vllm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/sharding_manager/fsdp_ulysses.py
- Line 18: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/sharding_manager/fsdp_vllm.py
- Line 28: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/workers/sharding_manager/megatron_vllm.py
- Line 220: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/dapo/main_dapo.py
- Line 23: `from .dapo_ray_trainer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/prime/main_prime.py
- Line 35: `from .prime_ray_trainer import ...`
- Line 112: `from .prime_fsdp_workers import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/prime/prime_dp_rm.py
- Line 32: `from .prime_core_algos import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/prime/prime_fsdp_workers.py
- Line 44: `from .prime_core_algos import ...`
- Line 240: `from .prime_dp_rm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/prime/prime_ray_trainer.py
- Line 38: `from . import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/sppo/main_sppo.py
- Line 27: `from .sppo_ray_trainer import ...`
- Line 79: `from .sppo_worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/recipe/sppo/sppo_worker.py
- Line 41: `from .dp_actor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/e2e/envs/__init__.py
- Line 23: `from .digit_completion import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/e2e/envs/digit_completion/__init__.py
- Line 25: `from .task import ...`
- Line 26: `from .tokenizer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/__init__.py
- Line 21: `from .protocol import ...`
- Line 22: `from .utils.logging_utils import ...`
- Line 23: `from .utils.device import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/llama/megatron/__init__.py
- Line 15: `from .modeling_llama_megatron import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/llama/megatron/layers/__init__.py
- Line 15: `from .parallel_attention import ...`
- Line 16: `from .parallel_decoder import ...`
- Line 17: `from .parallel_linear import ...`
- Line 22: `from .parallel_mlp import ...`
- Line 23: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/llama/megatron/layers/parallel_decoder.py
- Line 30: `from .parallel_attention import ...`
- Line 31: `from .parallel_mlp import ...`
- Line 32: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/llama/megatron/modeling_llama_megatron.py
- Line 36: `from .layers import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/__init__.py
- Line 16: `from .registry import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/config_converter.py
- Line 191: `from .patch_v012 import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/loader.py
- Line 21: `from .saver import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/model_forward.py
- Line 19: `from .util import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/model_initializer.py
- Line 23: `from .config_converter import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/qwen2/megatron/__init__.py
- Line 15: `from .modeling_qwen2_megatron import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/qwen2/megatron/layers/__init__.py
- Line 15: `from .parallel_attention import ...`
- Line 16: `from .parallel_decoder import ...`
- Line 17: `from .parallel_mlp import ...`
- Line 18: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/qwen2/megatron/layers/parallel_decoder.py
- Line 30: `from .parallel_attention import ...`
- Line 31: `from .parallel_mlp import ...`
- Line 32: `from .parallel_rmsnorm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/qwen2/megatron/modeling_qwen2_megatron.py
- Line 36: `from .layers import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/__init__.py
- Line 16: `from . import ...`
- Line 17: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/base/__init__.py
- Line 15: `from .worker import ...`
- Line 16: `from .worker_group import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/base/megatron/worker_group.py
- Line 19: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/base/worker.py
- Line 25: `from .decorator import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/base/worker_group.py
- Line 24: `from .decorator import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/ray/__init__.py
- Line 15: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/single_controller/ray/megatron.py
- Line 22: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/__init__.py
- Line 36: `from .vllm_v_0_5_4 import ...`
- Line 37: `from .vllm_v_0_5_4.llm import ...`
- Line 41: `from .vllm_v_0_6_3 import ...`
- Line 42: `from .vllm_v_0_6_3.llm import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/arg_utils.py
- Line 40: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/llm.py
- Line 29: `from .arg_utils import ...`
- Line 30: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/llm_engine_sp.py
- Line 46: `from .arg_utils import ...`
- Line 47: `from .config import ...`
- Line 48: `from .tokenizer import ...`
- Line 290: `from .spmd_gpu_executor import ...`
- Line 311: `from .spmd_gpu_executor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/model_loader.py
- Line 35: `from .config import ...`
- Line 36: `from .dtensor_weight_loaders import ...`
- Line 37: `from .hf_weight_loader import ...`
- Line 38: `from .megatron_weight_loaders import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/model_runner.py
- Line 39: `from .config import ...`
- Line 40: `from .model_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/spmd_gpu_executor.py
- Line 36: `from .config import ...`
- Line 82: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_5_4/worker.py
- Line 46: `from .config import ...`
- Line 47: `from .dtensor_weight_loaders import ...`
- Line 48: `from .hf_weight_loader import ...`
- Line 49: `from .megatron_weight_loaders import ...`
- Line 50: `from .model_runner import ...`
- Line 51: `from .parallel_state import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/arg_utils.py
- Line 23: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/llm.py
- Line 28: `from .arg_utils import ...`
- Line 29: `from .llm_engine_sp import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/llm_engine_sp.py
- Line 49: `from .arg_utils import ...`
- Line 50: `from .config import ...`
- Line 51: `from .tokenizer import ...`
- Line 348: `from .spmd_gpu_executor import ...`
- Line 370: `from .spmd_gpu_executor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/model_loader.py
- Line 15: `from .config import ...`
- Line 16: `from .dtensor_weight_loaders import ...`
- Line 17: `from .hf_weight_loader import ...`
- Line 18: `from .megatron_weight_loaders import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/model_runner.py
- Line 42: `from .config import ...`
- Line 43: `from .model_loader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/spmd_gpu_executor.py
- Line 37: `from .config import ...`
- Line 83: `from .worker import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/third_party/vllm/vllm_v_0_6_3/worker.py
- Line 46: `from .config import ...`
- Line 47: `from .dtensor_weight_loaders import ...`
- Line 48: `from .hf_weight_loader import ...`
- Line 49: `from .megatron_weight_loaders import ...`
- Line 50: `from .model_runner import ...`
- Line 51: `from .parallel_state import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/tools/base_tool.py
- Line 18: `from .schemas import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/tools/gsm8k_tool.py
- Line 23: `from .base_tool import ...`
- Line 24: `from .schemas import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/tools/sandbox_fusion_tools.py
- Line 30: `from .schemas import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/__init__.py
- Line 15: `from . import ...`
- Line 16: `from .tokenizer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/checkpoint/fsdp_checkpoint_manager.py
- Line 30: `from .checkpoint_manager import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/checkpoint/megatron_checkpoint_manager.py
- Line 36: `from .checkpoint_manager import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/dataset/__init__.py
- Line 15: `from .rl_dataset import ...`
- Line 16: `from .rm_dataset import ...`
- Line 17: `from .sft_dataset import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/debug/__init__.py
- Line 15: `from .performance import ...`
- Line 16: `from .performance import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/fs.py
- Line 28: `from .hdfs_io import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/megatron/pipeline_parallel.py
- Line 19: `from .sequence_parallel import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/metric/__init__.py
- Line 15: `from .utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/__init__.py
- Line 36: `from . import ...`
- Line 40: `from . import ...`
- Line 51: `from . import ...`
- Line 62: `from . import ...`
- Line 68: `from . import ...`
- Line 74: `from . import ...`
- Line 79: `from . import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/math_batch.py
- Line 15: `from .math import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/prime_code/__init__.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/prime_code/utils.py
- Line 23: `from .testing_util import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/prime_math/__init__.py
- Line 33: `from . import ...`
- Line 34: `from .grader import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/sandbox_fusion/__init__.py
- Line 18: `from .utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/actor/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .dp_actor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/critic/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .dp_critic import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/reward_manager/__init__.py
- Line 15: `from .batch import ...`
- Line 16: `from .dapo import ...`
- Line 17: `from .naive import ...`
- Line 18: `from .prime import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/reward_model/__init__.py
- Line 15: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/reward_model/megatron/__init__.py
- Line 15: `from .reward_model import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/__init__.py
- Line 15: `from .base import ...`
- Line 16: `from .hf_rollout import ...`
- Line 17: `from .naive import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/hf_rollout.py
- Line 34: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/naive/__init__.py
- Line 15: `from .naive_rollout import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/naive/naive_rollout.py
- Line 31: `from ..base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/sglang_rollout/__init__.py
- Line 14: `from .async_sglang_rollout import ...`
- Line 15: `from .sglang_rollout import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/rollout/vllm_rollout/__init__.py
- Line 48: `from .fire_vllm_rollout import ...`
- Line 49: `from .vllm_rollout import ...`
- Line 52: `from .vllm_rollout_spmd import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/sharding_manager/fsdp_sglang.py
- Line 51: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/sharding_manager/fsdp_ulysses.py
- Line 24: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/sharding_manager/fsdp_vllm.py
- Line 44: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/sharding_manager/megatron_sglang.py
- Line 33: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/workers/sharding_manager/megatron_vllm.py
- Line 50: `from .base import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/__init__.py
- Line 21: `from .agent_manager import ...`
- Line 22: `from .base_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/agent_manager.py
- Line 135: `from .transcript_fetcher_agent import ...`
- Line 139: `from .search_optimizer_agent import ...`
- Line 143: `from .content_analyzer_agent import ...`
- Line 147: `from .orchestrator_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/content_analyzer_agent.py
- Line 23: `from .base_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/orchestrator_agent.py
- Line 22: `from .agent_manager import ...`
- Line 23: `from .base_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/search_optimizer_agent.py
- Line 22: `from .base_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/agents/transcript_fetcher_agent.py
- Line 20: `from .base_agent import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/arango_integration.py
- Line 105: `from .arango_connection import ...`
- Line 106: `from .arango_operations import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/arango_operations.py
- Line 16: `from .module_boundaries import ...`
- Line 17: `from .error_handler import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/arangodb_enhanced.py
- Line 126: `from .arango_integration import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/cli/app.py
- Line 43: `from .slash_mcp_mixin import ...`
- Line 47: `from ..mcp.youtube_prompts import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/cli/slash_mcp_mixin.py
- Line 27: `from ..mcp.prompts import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/database.py
- Line 30: `from ..config import ...`
- Line 31: `from ..performance_monitor import ...`
- Line 35: `from ..partial_data_handler import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/database_v2.py
- Line 20: `from ..config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/transcript.py
- Line 27: `from .database import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/utils/__init__.py
- Line 18: `from .embedding_utils import ...`
- Line 19: `from .github_extractor import ...`
- Line 20: `from .tree_sitter_utils import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/utils/tree_sitter_metadata.py
- Line 38: `from .tree_sitter_extractors import ...`
- Line 39: `from .tree_sitter_language_mappings import ...`
- Line 352: `from .tree_sitter_traversal import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/utils/tree_sitter_traversal.py
- Line 30: `from .tree_sitter_extractors import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/core/utils/tree_sitter_utils.py
- Line 31: `from .tree_sitter_extractors import ...`
- Line 39: `from .tree_sitter_language_mappings import ...`
- Line 46: `from .tree_sitter_metadata import ...`
- Line 47: `from .tree_sitter_traversal import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/database_adapter.py
- Line 107: `from .arango_integration import ...`
- Line 448: `from .research_analyzer import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/database_config.py
- Line 193: `from .database_adapter import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/deepretrieval_optimizer.py
- Line 25: `from .unified_search_config import ...`
- Line 163: `from .unified_search_config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/graph_memory_integration.py
- Line 25: `from .unified_search_config import ...`
- Line 349: `from .unified_search_config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/link_extractor.py
- Line 27: `from .module_boundaries import ...`
- Line 28: `from .error_handler import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/mcp/__main__.py
- Line 23: `from .server import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/mcp/server.py
- Line 24: `from ..core.database import ...`
- Line 25: `from ..core.transcript import ...`
- Line 26: `from ..mcp.prompts import ...`
- Line 27: `from ..mcp.youtube_prompts import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/mcp/visual_prompts.py
- Line 8: `from ..core.database import ...`
- Line 9: `from ..mcp.prompts import ...`
- Line 10: `from ..visual_extractor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/mcp/youtube_prompts.py
- Line 20: `from ..config import ...`
- Line 21: `from ..core.database import ...`
- Line 22: `from ..mcp.prompts import ...`
- Line 391: `from .visual_prompts import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/orchestrator_integration.py
- Line 25: `from .citation_detector import ...`
- Line 26: `from .metadata_extractor import ...`
- Line 27: `from .search_enhancements import ...`
- Line 28: `from .unified_search import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/performance_monitor.py
- Line 43: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/research_pipeline.py
- Line 33: `from .module_boundaries import ...`
- Line 34: `from .error_handler import ...`
- Line 35: `from .error_handler_v2 import ...`
- Line 114: `from .scripts.download_transcript import ...`
- Line 197: `from .scripts.download_transcript import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/smart_visual_extractor.py
- Line 24: `from .visual_extractor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/storage_operations.py
- Line 27: `from .circular_ref_detector import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/unified_search.py
- Line 54: `from .deepretrieval_optimizer import ...`
- Line 55: `from .graph_memory_integration import ...`
- Line 56: `from .unified_search_config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/unified_search_v2.py
- Line 24: `from .database_adapter import ...`
- Line 25: `from .database_config import ...`
- Line 26: `from .search_widener import ...`
- Line 27: `from .youtube_search import ...`
- Line 239: `from .citation_detector import ...`
- Line 240: `from .metadata_extractor import ...`
- Line 241: `from .speaker_extractor import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/visual_extractor.py
- Line 33: `from .config import ...`

#### /home/graham/workspace/experiments/youtube_transcripts/src/youtube_transcripts/youtube_search.py
- Line 35: `from .core.database import ...`
- Line 36: `from .search_widener import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/__init__.py
- Line 5: `from .tools import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli.py
- Line 79: `from .tools import ...`
- Line 102: `from .storage_backend import ...`
- Line 103: `from .tools.download_enhanced import ...`
- Line 107: `from .slash_mcp_mixin import ...`
- Line 591: `from .config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli/__init__.py
- Line 18: `from .__main__ import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli/__main__.py
- Line 64: `from ..tools import ...`
- Line 138: `from .granger_slash_mcp_mixin import ...`
- Line 139: `from .slash_command_enhancer import ...`
- Line 165: `from .research_commands import ...`
- Line 166: `from .search_commands import ...`
- Line 639: `from .search_commands import ...`
- Line 656: `from .search_commands import ...`
- Line 666: `from .search_commands import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli/granger_slash_mcp_mixin.py
- Line 32: `from ..mcp.prompts import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli/research_commands.py
- Line 21: `from ..tools.search_enhanced import ...`
- Line 22: `from ..tools.evidence_extraction import ...`
- Line 23: `from ..tools.report_generator import ...`
- Line 24: `from ..logging_config import ...`
- Line 314: `from ..tools.batch_operations import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/cli/search_commands.py
- Line 32: `from ..tools.semantic_search import ...`
- Line 37: `from ..utils.mac_compatibility import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/converters_enhanced.py
- Line 7: `from .converters import ...`
- Line 10: `from .tools.tree_sitter_utils import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/core/__init__.py
- Line 11: `from .search import ...`
- Line 12: `from .download import ...`
- Line 18: `from .utils import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/mcp/arxiv_mcp_server_prompts.py
- Line 12: `from ..mcp.prompts import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/mcp/server.py
- Line 10: `from .arxiv_mcp_server_prompts import ...`
- Line 11: `from .prompts import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/resources/papers.py
- Line 12: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/server.py
- Line 17: `from .config import ...`
- Line 18: `from .tools import ...`
- Line 72: `from .tools import ...`
- Line 126: `from .prompts.handlers import ...`
- Line 127: `from .prompts.handlers import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/storage/search_engine.py
- Line 35: `from ..utils.mac_compatibility import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/storage_backend.py
- Line 49: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/__init__.py
- Line 7: `from .search import ...`
- Line 8: `from .download import ...`
- Line 9: `from .list_papers import ...`
- Line 10: `from .read_paper import ...`
- Line 11: `from .conversion_options import ...`
- Line 12: `from .describe_content import ...`
- Line 13: `from .system_stats import ...`
- Line 14: `from .analyze_code import ...`
- Line 15: `from .summarize_paper import ...`
- Line 16: `from .extract_citations import ...`
- Line 17: `from .batch_operations import ...`
- Line 18: `from .comparative_analysis import ...`
- Line 19: `from .paper_similarity import ...`
- Line 20: `from .extract_sections import ...`
- Line 21: `from .annotations import ...`
- Line 27: `from .research_support import ...`
- Line 33: `from .paper_collections import ...`
- Line 95: `from .semantic_search import ...`
- Line 105: `from .reading_list import ...`
- Line 117: `from .daily_digest import ...`
- Line 129: `from .citation_tracking import ...`
- Line 139: `from .export_references import ...`
- Line 149: `from .paper_updates import ...`
- Line 155: `from .author_follow import ...`
- Line 167: `from .quick_cite import ...`
- Line 175: `from .search_templates import ...`
- Line 185: `from .paper_collections import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/annotations.py
- Line 8: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/author_follow.py
- Line 66: `from ..config import ...`
- Line 67: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/batch_operations.py
- Line 25: `from ..config import ...`
- Line 26: `from .download import ...`
- Line 27: `from .search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/citation_tracking.py
- Line 11: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/comparative_analysis.py
- Line 24: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/daily_digest.py
- Line 12: `from ..config import ...`
- Line 13: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/download.py
- Line 14: `from ..config import ...`
- Line 15: `from ..converters import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/download_enhanced.py
- Line 26: `from ..config import ...`
- Line 27: `from ..converters import ...`
- Line 28: `from ..storage_backend import ...`
- Line 29: `from ..core.utils import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/evidence_extraction.py
- Line 11: `from ..config import ...`
- Line 12: `from ..core.progress import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/export_references.py
- Line 11: `from ..core.search import ...`
- Line 367: `from .reading_list import ...`
- Line 583: `from .reading_list import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/extract_citations.py
- Line 24: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/extract_sections.py
- Line 23: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/paper_collections.py
- Line 54: `from ..config import ...`
- Line 55: `from ..core.utils import ...`
- Line 56: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/paper_similarity.py
- Line 28: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/paper_updates.py
- Line 65: `from ..config import ...`
- Line 66: `from ..core.utils import ...`
- Line 67: `from .reading_list import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/quick_cite.py
- Line 52: `from ..config import ...`
- Line 53: `from ..core.utils import ...`
- Line 54: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/reading_list.py
- Line 12: `from ..config import ...`
- Line 343: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/report_generator.py
- Line 10: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/research_support.py
- Line 38: `from ..config import ...`
- Line 39: `from ..llm_providers import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/search.py
- Line 15: `from ..config import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/search_templates.py
- Line 55: `from ..config import ...`
- Line 56: `from ..core.search import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/summarize_paper_llm.py
- Line 327: `from .summarize_paper import ...`

#### /home/graham/workspace/mcp-servers/arxiv-mcp-server/tests/framework/__init__.py
- Line 18: `from .scenario_test import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/api_doc_generator/__init__.py
- Line 12: `from .api_doc_generator_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/arangodb/__init__.py
- Line 93: `from .error_analyzer import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/arangodb/graph_self_organization_interaction.py
- Line 32: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/arangodb/level_0_tests/__init__.py
- Line 30: `from .test_query import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/arxiv-mcp-server/research_discovery_interaction.py
- Line 33: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/ci_helper/__init__.py
- Line 10: `from .ci_helper_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/claude-module-communicator/self_evolution_interaction.py
- Line 31: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/claude-module-communicator/tests/interactions/test_self_evolution.py
- Line 32: `from .self_evolution_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/code_translation/__init__.py
- Line 14: `from .code_translation_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/data_transformer/__init__.py
- Line 15: `from .data_transformer_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/error_recovery/__init__.py
- Line 14: `from .error_recovery_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/feature_flags/__init__.py
- Line 10: `from .feature_flags_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/intelligent_cache/__init__.py
- Line 15: `from .intelligent_cache_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/marker/ai_enhancement_interaction.py
- Line 33: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/performance_monitor/__init__.py
- Line 10: `from .performance_monitor_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/progressive_deployment/__init__.py
- Line 14: `from .progressive_deployment_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/resource_scheduler/__init__.py
- Line 10: `from .resource_scheduler_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/rl-commons/contextual_bandit_interaction.py
- Line 32: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/security_scanner/__init__.py
- Line 10: `from .security_scanner_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/sparta/cybersecurity_enrichment_interaction.py
- Line 33: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/sparta_handlers/__init__.py
- Line 8: `from .real_sparta_handlers import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/task_queue_manager/__init__.py
- Line 14: `from .task_queue_manager_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/test_generator/__init__.py
- Line 17: `from .test_generator_interaction import ...`

#### /home/graham/workspace/shared_claude_docs/project_interactions/youtube-transcripts/technical_content_mining_interaction.py
- Line 37: `from ...templates.interaction_framework import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/__init__.py
- Line 7: `from .encoder import ...`
- Line 8: `from .retriever import ...`
- Line 9: `from .chat import ...`
- Line 10: `from .interactive import ...`
- Line 11: `from .llm_client import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/chat.py
- Line 12: `from .llm_client import ...`
- Line 13: `from .retriever import ...`
- Line 14: `from .config import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/encoder.py
- Line 16: `from .utils import ...`
- Line 17: `from .index import ...`
- Line 18: `from .config import ...`
- Line 19: `from .docker_manager import ...`
- Line 167: `from .config import ...`
- Line 318: `from .config import ...`
- Line 384: `from .config import ...`
- Line 464: `from .config import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/index.py
- Line 15: `from .config import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/interactive.py
- Line 8: `from .chat import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/retriever.py
- Line 14: `from .utils import ...`
- Line 18: `from .index import ...`
- Line 19: `from .config import ...`

#### /home/graham/workspace/shared_claude_docs/repos/memvid/memvid/utils.py
- Line 19: `from .config import ...`

#### /home/graham/workspace/shared_claude_docs/scripts/granger_slash_mcp_mixin.py
- Line 30: `from ..mcp.prompts import ...`

#### /home/graham/workspace/shared_claude_docs/src/shared_claude_docs/__init__.py
- Line 10: `from .cli import ...`
- Line 11: `from .validators import ...`
- Line 12: `from .sync import ...`

#### /home/graham/workspace/shared_claude_docs/src/shared_claude_docs/cli/__init__.py
- Line 36: `from ..validators import ...`
- Line 60: `from ..sync import ...`

#### /home/graham/workspace/shared_claude_docs/templates/mcp_prompts_template.py
- Line 12: `from ..mcp.prompts import ...`

### Missing Dependencies (297 packages)

These dependencies cannot be imported:


#### aider_daemon
- configargparse>=1.5.3: Cannot import configargparse
- prompt-toolkit>=3.0.38: Cannot import prompt-toolkit
- gitpython>=3.1.31: Cannot import gitpython
- pyperclip>=1.8.2: Cannot import pyperclip
- networkx>=3.1: Cannot import networkx
- sounddevice>=0.4.6: Cannot import sounddevice
- soundfile>=0.12.1: Cannot import soundfile
- beautifulsoup4>=4.12.2: Cannot import beautifulsoup4
- backoff>=2.2.1: Cannot import backoff
- grep-ast>=0.2.4: Cannot import grep-ast
- pypandoc>=1.11: Cannot import pypandoc
- importlib-resources>=6.0.1: Cannot import importlib-resources
- tree-sitter>=0.21.3: Cannot import tree-sitter
- tree-sitter-languages>=1.10.2: Cannot import tree-sitter-languages
- websockets>=14.0: Cannot import websockets
- pyyaml>=6.0,<7: Cannot import pyyaml
- pydantic-settings>=2.0.0,<3: Cannot import pydantic-settings
- orjson>=3.9.0: Cannot import orjson
- aiosqlite>=0.19.0: Cannot import aiosqlite
- torch>=2.0.0: Cannot import torch
- llm_call @ git+https://github.com/grahama1970/llm_call.git@main: Cannot import llm_call @ git+https://github.com/grahama1970/llm_call.git@main
- rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master: Cannot import rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master
- claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master: Cannot import claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master
- orjson>=3.10.18: Cannot import orjson
- uvloop>=0.19.0: Cannot import uvloop
- textual>=0.47.0: Cannot import textual

#### annotator
- pillow>=10.0.0: Cannot import pillow
- pymupdf>=1.23.0: Cannot import pymupdf
- fastapi>=0.100.0: Cannot import fastapi
- uvicorn>=0.23.0: Cannot import uvicorn
- matplotlib>=3.10.3: Cannot import matplotlib
- pydantic-settings>=2.9.1: Cannot import pydantic-settings

#### arangodb
- tenacity>=9.0.0: Cannot import tenacity
- tabulate>=0.9.0: Cannot import tabulate
- nltk>=3.9.1: Cannot import nltk
- markitdown>=0.1.1: Cannot import markitdown
- markdownify>=0.11.6: Cannot import markdownify
- tree-sitter>=0.24.0: Cannot import tree-sitter
- tree-sitter-languages>=1.10.2: Cannot import tree-sitter-languages
- tree-sitter-language-pack>=0.7.2: Cannot import tree-sitter-language-pack
- markdown-it-py>=3.0.0: Cannot import markdown-it-py
- gitingest>=0.1.4: Cannot import gitingest
- torch>=2.2.0: Cannot import torch
- scikit-learn>=1.6.1: Cannot import scikit-learn
- faiss-cpu>=1.11.0: Cannot import faiss-cpu
- sentence-transformers>=4.1.0: Cannot import sentence-transformers
- transformers @ git+https://github.com/huggingface/transformers.git: Cannot import transformers @ git+https://github.com/huggingface/transformers.git
- qdrant-client>=1.14.2: Cannot import qdrant-client
- datasets>=2.16.0: Cannot import datasets
- matplotlib>=3.8.3: Cannot import matplotlib
- seaborn>=0.13.2: Cannot import seaborn
- deepmerge>=2.0.0: Cannot import deepmerge
- rapidfuzz>=3.11.0: Cannot import rapidfuzz
- einops>=0.8.1: Cannot import einops
- google-auth>=2.39.0: Cannot import google-auth
- google-auth-oauthlib>=1.2.2: Cannot import google-auth-oauthlib
- fastapi>=0.115.0: Cannot import fastapi
- uvicorn>=0.30.0: Cannot import uvicorn
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- pyautogui>=0.9.54: Cannot import pyautogui
- pillow>=11.2.1: Cannot import pillow
- pydantic-settings>=2.9.1: Cannot import pydantic-settings

#### arxiv_mcp
- mcp>=1.2.0: Cannot import mcp
- pymupdf4llm>=0.0.17: Cannot import pymupdf4llm
- pymupdf>=1.23.0: Cannot import pymupdf
- pydantic-settings>=2.1.0: Cannot import pydantic-settings
- uvicorn>=0.30.0: Cannot import uvicorn
- sse-starlette>=1.8.2: Cannot import sse-starlette
- tree-sitter>=0.23.0: Cannot import tree-sitter
- tree-sitter-language-pack>=0.0.3: Cannot import tree-sitter-language-pack
- scikit-learn>=1.3.0: Cannot import scikit-learn
- sentence-transformers>=4.0.0: Cannot import sentence-transformers
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- pytest-json-report>=1.5.0: Cannot import pytest-json-report

#### chat
- fastapi==0.109.0: Cannot import fastapi
- uvicorn[standard]==0.27.0: Cannot import uvicorn
- websockets==12.0: Cannot import websockets

#### claude_test_reporter
- pydantic-settings>=2.9.1: Cannot import pydantic-settings

#### darpa_crawl
- pydantic-settings>=2.0.0: Cannot import pydantic-settings
- beautifulsoup4>=4.12.0: Cannot import beautifulsoup4
- lxml>=5.0.0: Cannot import lxml
- apscheduler>=3.10.0: Cannot import apscheduler
- sqlalchemy>=2.0.0: Cannot import sqlalchemy
- aiosqlite>=0.20.0: Cannot import aiosqlite
- mcp>=1.1.2: Cannot import mcp
- rank-bm25>=0.2.2: Cannot import rank-bm25
- nltk>=3.8.0: Cannot import nltk
- arxiv-mcp-server @ git+https://github.com/grahama1970/arxiv-mcp-server.git@main: Cannot import arxiv-mcp-server @ git+https://github.com/grahama1970/arxiv-mcp-server.git@main
- youtube-transcripts @ file:///home/graham/workspace/experiments/youtube_transcripts: Cannot import youtube-transcripts @ file:///home/graham/workspace/experiments/youtube_transcripts
- rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master: Cannot import rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master
- claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master: Cannot import claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- llm-call @ git+https://github.com/grahama1970/llm_call.git@main: Cannot import llm-call @ git+https://github.com/grahama1970/llm_call.git@main
- marker @ git+https://github.com/grahama1970/marker.git@master: Cannot import marker @ git+https://github.com/grahama1970/marker.git@master
- sparta @ git+https://github.com/grahama1970/sparta.git@master: Cannot import sparta @ git+https://github.com/grahama1970/sparta.git@master
- tenacity>=9.1.2: Cannot import tenacity
- pytest-json-report>=1.5.0: Cannot import pytest-json-report

#### gitget
- tenacity>=9.0.0: Cannot import tenacity
- tabulate>=0.9.0: Cannot import tabulate
- nltk>=3.9.1: Cannot import nltk
- markitdown>=0.1.1: Cannot import markitdown
- markdownify>=0.11.6: Cannot import markdownify
- tree-sitter>=0.24.0: Cannot import tree-sitter
- tree-sitter-languages>=1.10.2: Cannot import tree-sitter-languages
- tree-sitter-language-pack>=0.7.2: Cannot import tree-sitter-language-pack
- markdown-it-py>=3.0.0: Cannot import markdown-it-py
- gitingest>=0.1.4: Cannot import gitingest
- torch>=2.2.0: Cannot import torch
- scikit-learn>=1.6.1: Cannot import scikit-learn
- faiss-cpu>=1.11.0: Cannot import faiss-cpu
- sentence-transformers>=4.1.0: Cannot import sentence-transformers
- transformers @ git+https://github.com/huggingface/transformers.git: Cannot import transformers @ git+https://github.com/huggingface/transformers.git
- qdrant-client>=1.14.2: Cannot import qdrant-client
- datasets>=2.16.0: Cannot import datasets
- matplotlib>=3.8.3: Cannot import matplotlib
- seaborn>=0.13.2: Cannot import seaborn
- deepmerge>=2.0.0: Cannot import deepmerge
- rapidfuzz>=3.11.0: Cannot import rapidfuzz
- einops>=0.8.1: Cannot import einops
- google-auth>=2.39.0: Cannot import google-auth
- google-auth-oauthlib>=1.2.2: Cannot import google-auth-oauthlib
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- mcp>=1.9.2: Cannot import mcp
- pytest-json-report>=1.5.0: Cannot import pytest-json-report
- fastmcp>=2.6.1: Cannot import fastmcp

#### granger_hub
- mcp>=1.2.0: Cannot import mcp
- uvicorn>=0.30.0: Cannot import uvicorn
- sse-starlette>=1.8.2: Cannot import sse-starlette
- playwright>=1.40.0: Cannot import playwright
- stix2>=3.0.0: Cannot import stix2
- pydantic-settings>=2.1.0: Cannot import pydantic-settings
- aiosqlite>=0.19.0: Cannot import aiosqlite
- rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master: Cannot import rl-commons @ git+https://github.com/grahama1970/rl_commons.git@master
- scikit-learn>=1.3.0: Cannot import scikit-learn
- mitreattack-python>=3.0.0: Cannot import mitreattack-python
- xmltodict>=0.13.0: Cannot import xmltodict
- beautifulsoup4>=4.12.0: Cannot import beautifulsoup4
- rdflib>=7.0.0: Cannot import rdflib
- nvdlib>=0.7.0: Cannot import nvdlib
- allure-pytest>=2.14.2: Cannot import allure-pytest
- fastmcp>=2.5.1: Cannot import fastmcp
- llm_call @ git+https://github.com/grahama1970/llm_call.git@main: Cannot import llm_call @ git+https://github.com/grahama1970/llm_call.git@main
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git
- mcp-screenshot @ https://github.com/grahama1970/mcp-screenshot.git: Cannot import mcp-screenshot @ https://github.com/grahama1970/mcp-screenshot.git
- schedule: Cannot import schedule
- pytest-json-report>=1.5.0: Cannot import pytest-json-report
- pdftext>=0.6.2: Cannot import pdftext
- pymupdf4llm>=0.0.24: Cannot import pymupdf4llm
- tree-sitter>=0.24.0: Cannot import tree-sitter
- tree-sitter-language-pack>=0.7.3: Cannot import tree-sitter-language-pack
- marker-pdf>=1.7.4: Cannot import marker-pdf

#### llm_call
- tenacity>=8.2.3: Cannot import tenacity
- fastapi>=0.110.0: Cannot import fastapi
- uvicorn[standard]>=0.29.0: Cannot import uvicorn
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- deepmerge>=1.1.0: Cannot import deepmerge
- pydantic-settings>=2.0.0: Cannot import pydantic-settings
- rapidfuzz>=3.0.0: Cannot import rapidfuzz
- beautifulsoup4>=4.12.0: Cannot import beautifulsoup4
- mcp>=0.1.0: Cannot import mcp
- google-cloud-aiplatform>=1.38.1: Cannot import google-cloud-aiplatform
- pillow>=10.0.0: Cannot import pillow
- torch>=2.0.0: Cannot import torch
- transformers>=4.30.0: Cannot import transformers
- llm>=0.25: Cannot import llm
- llm-gemini>=0.20: Cannot import llm-gemini
- files-to-prompt>=0.6: Cannot import files-to-prompt
- wikipedia>=1.4.0: Cannot import wikipedia
- wikipedia-api>=0.8.1: Cannot import wikipedia-api
- pytest-json-report>=1.5.0: Cannot import pytest-json-report

#### marker
- Pillow>=10.1.0,<11: Cannot import Pillow
- pydantic-settings>=2.0.3,<3: Cannot import pydantic-settings
- transformers>=4.45.2,<5: Cannot import transformers
- torch>=2.5.1,<3: Cannot import torch
- ftfy>=6.1.1,<7: Cannot import ftfy
- rapidfuzz>=3.8.1,<4: Cannot import rapidfuzz
- surya-ocr~=0.13.1: Cannot import surya-ocr~
- pdftext~=0.6.2: Cannot import pdftext~
- markdownify>=0.13.1,<0.14: Cannot import markdownify
- markdown2>=2.5.2,<3: Cannot import markdown2
- filetype>=1.2.0,<2: Cannot import filetype
- scikit-learn>=1.6.1,<2: Cannot import scikit-learn
- google-genai>=1.0.0,<2: Cannot import google-genai
- pre-commit>=4.2.0,<5: Cannot import pre-commit
- camelot-py>=0.11.0,<0.12: Cannot import camelot-py
- cv2-tools: Cannot import cv2-tools
- tree-sitter>=0.23.2: Cannot import tree-sitter
- tree-sitter-languages>=1.10.2: Cannot import tree-sitter-languages
- tree-sitter-language-pack>=0.7.3: Cannot import tree-sitter-language-pack
- ghostscript>=0.7: Cannot import ghostscript
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- beautifulsoup4>=4.13.4: Cannot import beautifulsoup4
- lxml>=5.3.0: Cannot import lxml
- docx2python>=3.5.0: Cannot import docx2python

#### mcp_screenshot
- fastmcp>=0.1.0: Cannot import fastmcp
- mss>=9.0.1: Cannot import mss
- Pillow>=10.0.0: Cannot import Pillow
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- pyautogui>=0.9.53: Cannot import pyautogui
- selenium>=4.0.0: Cannot import selenium
- uvloop>=0.17.0: Cannot import uvloop
- google-auth>=2.0.0: Cannot import google-auth
- google-auth-oauthlib>=1.0.0: Cannot import google-auth-oauthlib
- google-cloud-aiplatform>=1.0.0: Cannot import google-cloud-aiplatform
- imagehash>=4.3.0: Cannot import imagehash
- pydantic-settings>=2.9.1: Cannot import pydantic-settings

#### rl_commons
- torch>=2.0.0: Cannot import torch
- gymnasium>=0.28.0: Cannot import gymnasium
- stable-baselines3>=2.0.0: Cannot import stable-baselines3
- ray[default]>=2.5.0: Cannot import ray
- wandb>=0.15.0: Cannot import wandb
- tensorboard>=2.13.0: Cannot import tensorboard
- matplotlib>=3.7.0: Cannot import matplotlib
- plotly>=5.14.0: Cannot import plotly
- scikit-learn>=1.3.0: Cannot import scikit-learn
- fastapi>=0.100.0: Cannot import fastapi
- uvicorn>=0.23.0: Cannot import uvicorn
- pyyaml>=6.0: Cannot import pyyaml
- pytest-json-report>=1.5.0: Cannot import pytest-json-report

#### shared_docs
- mkdocs-material>=9.0.0: Cannot import mkdocs-material
- mkdocs-mermaid2-plugin>=1.0.0: Cannot import mkdocs-mermaid2-plugin
- pymdown-extensions>=10.0: Cannot import pymdown-extensions
- pyyaml>=6.0: Cannot import pyyaml
- GitPython>=3.1.0: Cannot import GitPython
- pytest-json-report>=1.5.0: Cannot import pytest-json-report
- google-generativeai>=0.8.0: Cannot import google-generativeai
- llm_call @ git+https://github.com/grahama1970/llm_call.git: Cannot import llm_call @ git+https://github.com/grahama1970/llm_call.git
- granger_hub @ git+https://github.com/grahama1970/granger_hub.git: Cannot import granger_hub @ git+https://github.com/grahama1970/granger_hub.git
- rl_commons @ git+https://github.com/grahama1970/rl-commons.git: Cannot import rl_commons @ git+https://github.com/grahama1970/rl-commons.git
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git
- sparta @ git+https://github.com/grahama1970/sparta.git: Cannot import sparta @ git+https://github.com/grahama1970/sparta.git
- marker @ git+https://github.com/grahama1970/marker.git: Cannot import marker @ git+https://github.com/grahama1970/marker.git
- arangodb @ git+https://github.com/grahama1970/arangodb.git: Cannot import arangodb @ git+https://github.com/grahama1970/arangodb.git
- youtube_transcripts @ git+https://github.com/grahama1970/youtube-transcripts-search.git: Cannot import youtube_transcripts @ git+https://github.com/grahama1970/youtube-transcripts-search.git
- fine_tuning @ git+https://github.com/grahama1970/fine_tuning.git: Cannot import fine_tuning @ git+https://github.com/grahama1970/fine_tuning.git
- memvid @ git+https://github.com/grahama1970/memvid.git: Cannot import memvid @ git+https://github.com/grahama1970/memvid.git
- arxiv-mcp-server @ git+https://github.com/blazickjp/arxiv-mcp-server.git: Cannot import arxiv-mcp-server @ git+https://github.com/blazickjp/arxiv-mcp-server.git
- mcp-screenshot @ git+https://github.com/grahama1970/mcp-screenshot.git: Cannot import mcp-screenshot @ git+https://github.com/grahama1970/mcp-screenshot.git
- annotator @ git+https://github.com/grahama1970/marker-ground-truth.git: Cannot import annotator @ git+https://github.com/grahama1970/marker-ground-truth.git
- aider-daemon @ git+https://github.com/grahama1970/aider-daemon.git: Cannot import aider-daemon @ git+https://github.com/grahama1970/aider-daemon.git

#### sparta
- mcp>=1.2.0: Cannot import mcp
- uvicorn>=0.30.0: Cannot import uvicorn
- sse-starlette>=1.8.2: Cannot import sse-starlette
- claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master: Cannot import claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git@master
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- playwright>=1.40.0: Cannot import playwright
- stix2>=3.0.0: Cannot import stix2
- pydantic-settings>=2.1.0: Cannot import pydantic-settings
- scikit-learn>=1.3.0: Cannot import scikit-learn
- mitreattack-python>=3.0.0: Cannot import mitreattack-python
- xmltodict>=0.13.0: Cannot import xmltodict
- beautifulsoup4>=4.12.0: Cannot import beautifulsoup4
- rdflib>=7.0.0: Cannot import rdflib
- nvdlib>=0.7.0: Cannot import nvdlib
- fastmcp>=2.5.1: Cannot import fastmcp
- pytest-json-report>=1.5.0: Cannot import pytest-json-report

#### unsloth
- torch>=2.0.0: Cannot import torch
- transformers>=4.35.0: Cannot import transformers
- datasets>=2.16.0: Cannot import datasets
- tenacity>=8.2.0: Cannot import tenacity
- rapidfuzz>=3.0.0: Cannot import rapidfuzz
- trl>=0.7.0: Cannot import trl
- peft>=0.7.0: Cannot import peft
- accelerate>=0.25.0: Cannot import accelerate
- bitsandbytes>=0.41.0: Cannot import bitsandbytes
- tensorboard>=2.15.0: Cannot import tensorboard
- yaspin>=3.0.0: Cannot import yaspin
- jsonpickle>=3.0.0: Cannot import jsonpickle
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git@main
- llm-call @ git+https://github.com/grahama1970/llm_call.git: Cannot import llm-call @ git+https://github.com/grahama1970/llm_call.git
- fastapi>=0.115.12: Cannot import fastapi
- uvicorn>=0.34.2: Cannot import uvicorn
- deepeval>=1.0.0: Cannot import deepeval
- mlflow>=2.10.0: Cannot import mlflow
- lm-eval>=0.4.0: Cannot import lm-eval
- plotly>=5.18.0: Cannot import plotly
- pydantic-settings>=2.9.1: Cannot import pydantic-settings
- runpod_ops @ git+https://github.com/grahama1970/runpod_ops.git: Cannot import runpod_ops @ git+https://github.com/grahama1970/runpod_ops.git

#### world_model
- scikit-learn>=1.3.0: Cannot import scikit-learn
- pytest-json-report>=1.5.0: Cannot import pytest-json-report
- fastapi>=0.100.0: Cannot import fastapi
- uvicorn>=0.23.0: Cannot import uvicorn

#### youtube_transcripts
- pytube>=15.0.0: Cannot import pytube
- google-generativeai>=0.3.0: Cannot import google-generativeai
- ollama>=0.1.0: Cannot import ollama
- claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git: Cannot import claude-test-reporter @ git+https://github.com/grahama1970/claude-test-reporter.git
- claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git: Cannot import claude-module-communicator @ git+https://github.com/grahama1970/claude-module-communicator.git
- youtube-dl>=2021.12.17: Cannot import youtube-dl
- yt-dlp>=2025.5.22: Cannot import yt-dlp
- whisper>=1.1.10: Cannot import whisper
- pydantic-settings>=2.9.1: Cannot import pydantic-settings
- sentence-transformers>=4.1.0: Cannot import sentence-transformers
- tree-sitter>=0.24.0: Cannot import tree-sitter
- tree-sitter-languages>=1.10.2: Cannot import tree-sitter-languages
- linkify-it-py>=2.0.3: Cannot import linkify-it-py
- validators>=0.35.0: Cannot import validators
- tenacity>=8.0.0: Cannot import tenacity

### Syntax Errors (619 files)

These files have syntax errors:

- /home/graham/workspace/experiments/granger_hub/repos/aider/scripts/__init__.py (line 12): invalid decimal literal (<unknown>, line 12)
- /home/graham/workspace/experiments/granger_hub/repos/aider/scripts/homepage.py (line 463): unmatched ')' (<unknown>, line 463)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/help/test_help.py (line 58): unexpected indent (<unknown>, line 58)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/scrape/test_scrape.py (line 146): unmatched ')' (<unknown>, line 146)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_history.py (line 36): invalid syntax (<unknown>, line 36)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_reasoning.py (line 44): unexpected indent (<unknown>, line 44)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_sanity_check_repo.py (line 146): unmatched ')' (<unknown>, line 146)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_onboarding.py (line 74): unexpected indent (<unknown>, line 74)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_editor.py (line 117): invalid syntax (<unknown>, line 117)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_repo.py (line 181): unexpected indent (<unknown>, line 181)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_ssl_verification.py (line 53): unmatched ')' (<unknown>, line 53)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_udiff.py (line 31): unexpected indent (<unknown>, line 31)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_repomap.py (line 185): unexpected indent (<unknown>, line 185)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_main.py (line 1278): unmatched ')' (<unknown>, line 1278)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_io.py (line 66): unexpected indent (<unknown>, line 66)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_wholefile.py (line 128): unexpected indent (<unknown>, line 128)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_openrouter.py (line 91): unexpected indent (<unknown>, line 91)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_model_info_manager.py (line 57): invalid syntax (<unknown>, line 57)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_coder.py (line 421): unexpected indent (<unknown>, line 421)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_commands.py (line 1055): unmatched ')' (<unknown>, line 1055)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_deprecated.py (line 81): unexpected indent (<unknown>, line 81)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_editblock.py (line 133): unexpected indent (<unknown>, line 133)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_voice.py (line 74): invalid syntax (<unknown>, line 74)
- /home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_models.py (line 42): unexpected indent (<unknown>, line 42)
- /home/graham/workspace/experiments/granger_hub/repos/aider/benchmark/test_benchmark.py (line 45): unexpected indent (<unknown>, line 45)
- /home/graham/workspace/experiments/granger_hub/repos/aider/benchmark/swe_bench.py (line 22): unmatched ')' (<unknown>, line 22)
- /home/graham/workspace/experiments/granger_hub/tests/test_service_discovery.py (line 31): unexpected unindent (<unknown>, line 31)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/darpa_crawl_scenario.py (line 113): f-string: f-string: unmatched '[' (<unknown>, line 113)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/categories/research_integration/test_paper_validation.py (line 141): unexpected unindent (<unknown>, line 141)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/document_processing/test_testcachearangodbv2_evolved.py (line 102): unexpected unindent (<unknown>, line 102)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/document_processing/test_testcachearangodbv2.py (line 102): unexpected unindent (<unknown>, line 102)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/integration/test_testhybridcacheparallel.py (line 127): unexpected unindent (<unknown>, line 127)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/ml_workflows/test_testtestpatternllm_callv1.py (line 90): unexpected unindent (<unknown>, line 90)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/ml_workflows/test_testmessagequeuellm_callv3.py (line 90): unexpected unindent (<unknown>, line 90)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/ml_workflows/test_testmessagequeuellm_callv3_evolved.py (line 90): unexpected unindent (<unknown>, line 90)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/ml_workflows/test_testapigatewayllm_callv4.py (line 90): unexpected unindent (<unknown>, line 90)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/ml_workflows/test_rl_module_learning.py (line 78): invalid syntax (<unknown>, line 78)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/research_integration/test_testparallelarxivv1.py (line 104): unexpected unindent (<unknown>, line 104)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/generated/research_integration/test_testparallelarxivv1_evolved.py (line 104): unexpected unindent (<unknown>, line 104)
- /home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/rl_integration/test_rl_module_selection.py (line 181): unexpected unindent (<unknown>, line 181)
- /home/graham/workspace/experiments/granger_hub/tests/core/test_event_system.py (line 44): unexpected unindent (<unknown>, line 44)
- /home/graham/workspace/experiments/granger_hub/tests/core/adapters/test_rest_adapter.py (line 105): unexpected unindent (<unknown>, line 105)
- /home/graham/workspace/experiments/granger_hub/tests/core/adapters/test_adapter_framework.py (line 43): unexpected unindent (<unknown>, line 43)
- /home/graham/workspace/experiments/granger_hub/tests/core/adapters/test_binary_handling.py (line 88): unexpected unindent (<unknown>, line 88)
- /home/graham/workspace/experiments/granger_hub/tests/core/adapters/test_adapter_honeypot.py (line 60): unexpected unindent (<unknown>, line 60)
- /home/graham/workspace/experiments/granger_hub/tests/core/adapters/test_hardware_adapters.py (line 38): unexpected unindent (<unknown>, line 38)
- /home/graham/workspace/experiments/granger_hub/tests/core/modules/test_browser_automation_module.py (line 1): unexpected indent (<unknown>, line 1)
- /home/graham/workspace/experiments/granger_hub/tests/rl/metrics/test_rl_metrics.py (line 274): invalid syntax (<unknown>, line 274)
- /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/research/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/generation/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/analysis/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/granger_hub/src/granger_hub/discovery/learning/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/granger_hub/archive/test_level_0_example.py (line 134): expected an indented block after 'if' statement on line 133 (<unknown>, line 134)
- /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/validate_discovery_tests.py (line 199): expected an indented block after 'if' statement on line 197 (<unknown>, line 199)
- /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/validate_hardware_tests.py (line 193): expected an indented block after 'if' statement on line 191 (<unknown>, line 193)
- /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/validate_integration_tests.py (line 177): expected an indented block after 'if' statement on line 175 (<unknown>, line 177)
- /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_pdf_extraction.py (line 144): expected an indented block after 'for' statement on line 141 (<unknown>, line 144)
- /home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/core/modules/test_screenshot_module.py (line 7): unexpected indent (<unknown>, line 7)
- /home/graham/workspace/experiments/granger_hub/archive/claude_desktop_code/all_code.py (line 567): invalid syntax (<unknown>, line 567)
- /home/graham/workspace/experiments/granger_hub/archive/claude_desktop_code/progress_tracker.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/granger_hub/archive/debug_scripts/run_sample_verification.py (line 53): unmatched ')' (<unknown>, line 53)
- /home/graham/workspace/experiments/rl_commons/archive/old_tests/test_marker_relationship_extraction.py (line 466): expected an indented block after 'if' statement on line 465 (<unknown>, line 466)
- /home/graham/workspace/experiments/rl_commons/archive/old_tests/test_mcp_integration.py (line 221): expected an indented block after 'if' statement on line 220 (<unknown>, line 221)
- /home/graham/workspace/experiments/rl_commons/archive/deprecated_tests/test_a3c_simple.py (line 219): expected an indented block after 'if' statement on line 218 (<unknown>, line 219)
- /home/graham/workspace/experiments/rl_commons/archive/arangodb_tests/arangodb/core/test_vertex_client.py (line 69): expected an indented block after 'if' statement on line 68 (<unknown>, line 69)
- /home/graham/workspace/experiments/rl_commons/archive/arangodb_tests/arangodb/core/test_final_validation.py (line 246): expected an indented block after 'if' statement on line 245 (<unknown>, line 246)
- /home/graham/workspace/experiments/world_model/tests/test_honeypot.py (line 35): unexpected unindent (<unknown>, line 35)
- /home/graham/workspace/experiments/world_model/tests/test_module_creation.py (line 82): unexpected unindent (<unknown>, line 82)
- /home/graham/workspace/experiments/world_model/archive/deprecated_tests/run_task_001_tests.py (line 201): expected an indented block after 'if' statement on line 200 (<unknown>, line 201)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/config.py (line 199): unterminated triple-quoted string literal (detected at line 274) (<unknown>, line 199)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/cli/validate.py (line 20): invalid syntax (<unknown>, line 20)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/cli/slash_mcp_mixin.py (line 433): unterminated triple-quoted string literal (detected at line 439) (<unknown>, line 433)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/cli/main.py (line 599): invalid character '🧑' (U+1F9D1) (<unknown>, line 599)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/cli/code_review.py (line 19): invalid syntax (<unknown>, line 19)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/cli/__init__.py (line 18): unterminated triple-quoted string literal (detected at line 19) (<unknown>, line 18)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/integrations/__init__.py (line 14): invalid syntax (<unknown>, line 14)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/integrations/claude_test_reporter_module.py (line 17): invalid syntax (<unknown>, line 17)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/runners/pytest_report_runner.py (line 92): unterminated triple-quoted string literal (detected at line 107) (<unknown>, line 92)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/core/generators/multi_project_dashboard.py (line 207): invalid decimal literal (<unknown>, line 207)
- /home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/mcp/__init__.py (line 18): unterminated triple-quoted string literal (detected at line 19) (<unknown>, line 18)
- /home/graham/workspace/experiments/claude-test-reporter/archive/update_to_git_dep.py (line 8): invalid syntax (<unknown>, line 8)
- /home/graham/workspace/experiments/claude-test-reporter/archive/test_git_review_integration.py (line 1): invalid character '🧪' (U+1F9EA) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/archive/update_pyproject.py (line 21): expression cannot contain assignment, perhaps you meant "=="? (<unknown>, line 21)
- /home/graham/workspace/experiments/claude-test-reporter/archive/test_package.py (line 1): invalid character '🧪' (U+1F9EA) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/examples/test_validation_example.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/examples/demo_multi_project_monitoring.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/examples/test_report_with_base_url.py (line 1): invalid character '✅' (U+2705) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/examples/test_download_report.py (line 1): invalid character '📄' (U+1F4C4) (<unknown>, line 1)
- /home/graham/workspace/experiments/claude-test-reporter/examples/demo_configured_reports.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/shared_claude_docs/multi_project_dashboard_backup.py (line 197): invalid decimal literal (<unknown>, line 197)
- /home/graham/workspace/shared_claude_docs/implement_real_functionality.py (line 76): unterminated string literal (detected at line 76) (<unknown>, line 76)
- /home/graham/workspace/shared_claude_docs/remove_all_mocks_and_simulations.py (line 178): unterminated string literal (detected at line 178) (<unknown>, line 178)
- /home/graham/workspace/shared_claude_docs/universal_report_generator_backup.py (line 202): invalid decimal literal (<unknown>, line 202)
- /home/graham/workspace/shared_claude_docs/prepare_for_interaction_testing.py (line 268): expected an indented block after 'if' statement on line 267 (<unknown>, line 268)
- /home/graham/workspace/shared_claude_docs/scripts/fix_or_archive_all_tests.py (line 156): closing parenthesis ')' does not match opening parenthesis '[' on line 145 (<unknown>, line 156)
- /home/graham/workspace/shared_claude_docs/scripts/fix_all_projects_comprehensive.py (line 67): unterminated string literal (detected at line 67) (<unknown>, line 67)
- /home/graham/workspace/shared_claude_docs/scripts/fix_test_execution.py (line 214): expected an indented block after 'if' statement on line 213 (<unknown>, line 214)
- /home/graham/workspace/shared_claude_docs/scripts/fix_python_and_pytest.py (line 172): expected an indented block after 'if' statement on line 171 (<unknown>, line 172)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_55.py (line 329): expected an indented block after 'if' statement on line 328 (<unknown>, line 329)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_44.py (line 119): expected an indented block after 'if' statement on line 118 (<unknown>, line 119)
- /home/graham/workspace/shared_claude_docs/project_interactions/direct_test_tasks.py (line 116): expected an indented block after 'if' statement on line 115 (<unknown>, line 116)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_19.py (line 262): expected an indented block after 'if' statement on line 261 (<unknown>, line 262)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_52.py (line 598): expected an indented block after 'if' statement on line 597 (<unknown>, line 598)
- /home/graham/workspace/shared_claude_docs/project_interactions/granger_bug_hunter.py (line 91): invalid syntax (<unknown>, line 91)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_53.py (line 410): expected an indented block after 'if' statement on line 409 (<unknown>, line 410)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_56.py (line 485): expected an indented block after 'if' statement on line 484 (<unknown>, line 485)
- /home/graham/workspace/shared_claude_docs/project_interactions/comprehensive_test_verification.py (line 408): expected an indented block after 'if' statement on line 407 (<unknown>, line 408)
- /home/graham/workspace/shared_claude_docs/project_interactions/example_level_1_interactions.py (line 288): invalid syntax (<unknown>, line 288)
- /home/graham/workspace/shared_claude_docs/project_interactions/test_task_48.py (line 360): expected an indented block after 'if' statement on line 359 (<unknown>, line 360)
- /home/graham/workspace/shared_claude_docs/project_interactions/pipeline_monitor/test_task_40_quick.py (line 208): expected an indented block after 'if' statement on line 207 (<unknown>, line 208)
- /home/graham/workspace/shared_claude_docs/project_interactions/pipeline_monitor/test_task_40_fixed.py (line 226): expected an indented block after 'if' statement on line 225 (<unknown>, line 226)
- /home/graham/workspace/shared_claude_docs/project_interactions/container_orchestrator/test_task_39.py (line 315): expected an indented block after 'if' statement on line 314 (<unknown>, line 315)
- /home/graham/workspace/shared_claude_docs/project_interactions/performance_optimization/level4_ui_tests/tests/level4/accessibility/test_accessibility_compliance.py (line 305): invalid syntax (<unknown>, line 305)
- /home/graham/workspace/shared_claude_docs/project_interactions/model_benchmarking/test_task_35_comprehensive.py (line 612): expected an indented block after 'if' statement on line 611 (<unknown>, line 612)
- /home/graham/workspace/shared_claude_docs/project_interactions/model_benchmarking/test_task_35.py (line 366): expected an indented block after 'if' statement on line 365 (<unknown>, line 366)
- /home/graham/workspace/shared_claude_docs/project_interactions/model_benchmarking/test_task_35_critical.py (line 406): expected an indented block after 'if' statement on line 405 (<unknown>, line 406)
- /home/graham/workspace/shared_claude_docs/testing/visualization_tests/arangodb_visualization_interactions.py (line 592): '{' was never closed (<unknown>, line 592)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_all_granger_tests.py (line 384): expected an indented block after 'if' statement on line 383 (<unknown>, line 384)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_task_003_tests.py (line 314): expected an indented block after 'if' statement on line 313 (<unknown>, line 314)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_task_001_tests.py (line 193): expected an indented block after 'if' statement on line 192 (<unknown>, line 193)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_task_002_tests.py (line 260): expected an indented block after 'if' statement on line 259 (<unknown>, line 260)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_task_006_tests.py (line 112): expected an indented block after 'if' statement on line 111 (<unknown>, line 112)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_task_004_tests.py (line 333): expected an indented block after 'if' statement on line 332 (<unknown>, line 333)
- /home/graham/workspace/shared_claude_docs/archive/deprecated_tests/run_all_task_tests.py (line 314): expected an indented block after 'if' statement on line 313 (<unknown>, line 314)
- /home/graham/workspace/experiments/llm_call/repos/llm/tests/test_templates.py (line 332): unmatched ')' (<unknown>, line 332)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm_utils_tests/test_hashicorp.py (line 243): unmatched ')' (<unknown>, line 243)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm_utils_tests/test_proxy_budget_reset.py (line 427): invalid syntax (<unknown>, line 427)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm_utils_tests/test_utils.py (line 1048): unmatched ')' (<unknown>, line 1048)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_admin_ui_tests/test_role_based_access.py (line 174): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 174)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_admin_ui_tests/test_key_management.py (line 1224): unexpected indent (<unknown>, line 1224)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/guardrails_tests/test_presidio_pii.py (line 474): unexpected indent (<unknown>, line 474)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/guardrails_tests/test_guardrails_config.py (line 91): '(' was never closed (<unknown>, line 91)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/enterprise/enterprise_hooks/test_managed_files.py (line 87): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 87)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_cooldown_utils.py (line 129): invalid syntax (<unknown>, line 129)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_handle_error.py (line 146): invalid syntax (<unknown>, line 146)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/image_gen_tests/test_bedrock_image_gen_unit_tests.py (line 75): unexpected indent (<unknown>, line 75)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/test_router.py (line 175): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 175)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/test_main.py (line 205): '(' was never closed (<unknown>, line 205)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/test_cost_calculator.py (line 287): unexpected indent (<unknown>, line 287)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/router_strategy/test_base_routing_strategy.py (line 102): unmatched ')' (<unknown>, line 102)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_proxy_cli.py (line 103): closing parenthesis ')' does not match opening parenthesis '[' on line 83 (<unknown>, line 103)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_common_request_processing.py (line 85): unexpected indent (<unknown>, line 85)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_spend_log_cleanup.py (line 167): invalid syntax (<unknown>, line 167)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_caching_routes.py (line 63): invalid syntax (<unknown>, line 63)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_litellm_pre_call_utils.py (line 181): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 181)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_route_llm_request.py (line 80): invalid syntax (<unknown>, line 80)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/test_proxy_server.py (line 291): unmatched ')' (<unknown>, line 291)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/pass_through_endpoints/test_llm_pass_through_endpoints.py (line 247): unexpected indent (<unknown>, line 247)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/auth/test_auth_checks.py (line 192): unmatched ')' (<unknown>, line 192)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/middleware/test_prometheus_auth_middleware.py (line 107): unexpected indent (<unknown>, line 107)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/ui_crud_endpoints/test_proxy_setting_endpoints.py (line 108): unexpected indent (<unknown>, line 108)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/hooks/test_proxy_track_cost_callback.py (line 162): invalid syntax (<unknown>, line 162)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/common_utils/test_http_parsing_utils.py (line 90): invalid syntax (<unknown>, line 90)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/db/test_db_spend_update_writer.py (line 67): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 67)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/db/db_transaction_queue/test_pod_lock_manager.py (line 89): unmatched ')' (<unknown>, line 89)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_users_commands.py (line 82): invalid syntax (<unknown>, line 82)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_models_commands.py (line 193): unmatched ')' (<unknown>, line 193)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_keys_commands.py (line 79): invalid syntax (<unknown>, line 79)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_chat_commands.py (line 117): unmatched ')' (<unknown>, line 117)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/cli/test_credentials_commands.py (line 144): unmatched ')' (<unknown>, line 144)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/spend_tracking/test_spend_management_endpoints.py (line 1085): unmatched ')' (<unknown>, line 1085)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/spend_tracking/test_spend_tracking_utils.py (line 143): unmatched ')' (<unknown>, line 143)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/guardrails/test_guardrail_endpoints.py (line 90): invalid syntax (<unknown>, line 90)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_ui_sso.py (line 503): unexpected indent (<unknown>, line 503)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_internal_user_endpoints.py (line 70): invalid syntax (<unknown>, line 70)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_team_endpoints.py (line 145): invalid syntax (<unknown>, line 145)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/openai_files_endpoint/test_files_endpoint.py (line 108): unexpected indent (<unknown>, line 108)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/litellm_core_utils/test_token_counter.py (line 546): unmatched ')' (<unknown>, line 546)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/litellm_core_utils/test_dd_tracing.py (line 116): invalid syntax (<unknown>, line 116)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/litellm_core_utils/test_streaming_handler.py (line 69): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 69)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/enterprise/enterprise_callbacks/send_emails/test_base_email.py (line 185): invalid syntax (<unknown>, line 185)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/enterprise/enterprise_callbacks/send_emails/test_endpoints.py (line 72): invalid syntax (<unknown>, line 72)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/experimental_mcp_client/test_tools.py (line 176): unmatched ')' (<unknown>, line 176)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/ollama/test_ollama_completion_transformation.py (line 81): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 81)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/gemini/realtime/test_gemini_realtime_transformation.py (line 201): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 201)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/openai/test_openai_common_utils.py (line 111): closing parenthesis ']' does not match opening parenthesis '{' on line 110 (<unknown>, line 111)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/llamafile/chat/test_llamafile_chat_transformation.py (line 70): invalid syntax (<unknown>, line 70)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/azure/test_azure_common_utils.py (line 133): unmatched ')' (<unknown>, line 133)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_agentops.py (line 90): invalid syntax (<unknown>, line 90)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_opentelemetry.py (line 89): unindent does not match any outer indentation level (<unknown>, line 89)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_prometheus_services.py (line 81): invalid syntax (<unknown>, line 81)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_custom_prompt_management.py (line 99): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 99)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_athina.py (line 147): invalid syntax (<unknown>, line 147)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/gcs_pubsub/test_pub_sub.py (line 60): unexpected indent (<unknown>, line 60)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/arize/test_arize_phoenix.py (line 57): unindent does not match any outer indentation level (<unknown>, line 57)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/caching/test_redis_cache.py (line 84): unmatched ')' (<unknown>, line 84)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/caching/test_redis_semantic_cache.py (line 52): closing parenthesis '}' does not match opening parenthesis '(' on line 51 (<unknown>, line 52)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/caching/test_redis_cluster_cache.py (line 51): unexpected indent (<unknown>, line 51)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/pass_through_unit_tests/test_unit_test_passthrough_router.py (line 113): invalid syntax (<unknown>, line 113)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/pass_through_unit_tests/test_assemblyai_unit_tests_passthrough.py (line 121): unmatched ')' (<unknown>, line 121)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/pass_through_unit_tests/test_anthropic_messages_passthrough.py (line 661): invalid syntax (<unknown>, line 661)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_alerting.py (line 479): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 479)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_prometheus_unit_tests.py (line 256): unmatched ')' (<unknown>, line 256)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_log_db_redis_services.py (line 220): invalid syntax (<unknown>, line 220)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_prompt_factory.py (line 686): '(' was never closed (<unknown>, line 686)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_openai.py (line 411): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 411)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_bedrock_dynamic_auth_params_unit_tests.py (line 97): invalid syntax (<unknown>, line 97)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_azure_ai.py (line 217): invalid syntax (<unknown>, line 217)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_bedrock_completion.py (line 962): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 962)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_watsonx.py (line 182): invalid syntax (<unknown>, line 182)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_voyage_ai.py (line 96): '(' was never closed (<unknown>, line 96)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_unit_test_bedrock_invoke.py (line 147): unmatched ')' (<unknown>, line 147)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_aws_base_llm.py (line 171): unmatched ')' (<unknown>, line 171)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_databricks.py (line 570): unmatched ')' (<unknown>, line 570)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_cohere_generate_api.py (line 85): invalid syntax (<unknown>, line 85)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_optional_params.py (line 632): '(' was never closed (<unknown>, line 632)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_vertex.py (line 130): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 130)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_azure_openai.py (line 273): unmatched ')' (<unknown>, line 273)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/batches_tests/test_fine_tuning_api.py (line 567): invalid syntax (<unknown>, line 567)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_anthropic_prompt_caching.py (line 196): unmatched ')' (<unknown>, line 196)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router.py (line 2705): invalid syntax (<unknown>, line 2705)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_custom_callback_input.py (line 1309): closing parenthesis ']' does not match opening parenthesis '(' on line 1306 (<unknown>, line 1309)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_audio_speech.py (line 347): unexpected indent (<unknown>, line 347)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_custom_llm.py (line 431): unexpected indent (<unknown>, line 431)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_cooldowns.py (line 190): invalid syntax (<unknown>, line 190)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_aim_guardrails.py (line 336): unmatched ')' (<unknown>, line 336)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_tpm_rpm_routing_v2.py (line 794): unmatched ')' (<unknown>, line 794)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_function_calling.py (line 802): '(' was never closed (<unknown>, line 802)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_lakera_ai_prompt_injection.py (line 90): unmatched ')' (<unknown>, line 90)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_fallbacks.py (line 1535): invalid syntax (<unknown>, line 1535)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_pattern_matching.py (line 254): '(' was never closed (<unknown>, line 254)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_utils.py (line 288): invalid syntax (<unknown>, line 288)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_streaming.py (line 4046): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 4046)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_caching.py (line 2431): unmatched ')' (<unknown>, line 2431)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_dual_cache.py (line 92): invalid syntax (<unknown>, line 92)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_amazing_vertex_completion.py (line 1697): invalid syntax (<unknown>, line 1697)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_timeout.py (line 204): '(' was never closed (<unknown>, line 204)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_caching_handler.py (line 193): unmatched ')' (<unknown>, line 193)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_ollama.py (line 156): unexpected indent (<unknown>, line 156)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_completion.py (line 2509): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 2509)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_client_init.py (line 125): unexpected indent (<unknown>, line 125)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_user_api_key_auth.py (line 1029): unmatched ')' (<unknown>, line 1029)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_proxy_utils.py (line 66): unexpected indent (<unknown>, line 66)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_e2e_pod_lock_manager.py (line 451): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 451)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_jwt.py (line 1340): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 1340)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_auth_checks.py (line 605): unmatched ')' (<unknown>, line 605)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_audit_logs_proxy.py (line 129): unmatched ')' (<unknown>, line 129)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_update_spend.py (line 322): unexpected indent (<unknown>, line 322)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_proxy_exception_mapping.py (line 138): unmatched ')' (<unknown>, line 138)
- /home/graham/workspace/experiments/llm_call/repos/litellm/tests/proxy_unit_tests/test_proxy_server.py (line 202): unmatched ')' (<unknown>, line 202)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/fact-check/fact-check.py (line 373): f-string expression part cannot include a backslash (<unknown>, line 373)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/api_calls/speed_tests/tgi-speed.py (line 80): expected 'except' or 'finally' block (<unknown>, line 80)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/api_calls/speed_tests/llamacpp_speed-concurrent.py (line 44): expected 'except' or 'finally' block (<unknown>, line 44)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/api_calls/predictions/buggy_code_fixed.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/api_calls/regex_tests/tgi-regex.py (line 53): expected 'except' or 'finally' block (<unknown>, line 53)
- /home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/load_testing.py (line 36): unexpected indent (<unknown>, line 36)
- /home/graham/workspace/experiments/llm_call/scripts/test_report_engine.py (line 98): expected an indented block after 'if' statement on line 97 (<unknown>, line 98)
- /home/graham/workspace/experiments/llm_call/src/llm_call/mcp_server.py (line 41): invalid syntax (<unknown>, line 41)
- /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/code/task_004_test_prompts/poc_31_test_runner.py (line 452): expected an indented block after 'if' statement on line 451 (<unknown>, line 452)
- /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/code/task_004_test_prompts/poc_27_exponential_backoff.py (line 260): invalid syntax (<unknown>, line 260)
- /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/code/task_004_test_prompts/poc_26_basic_retry.py (line 227): unexpected indent (<unknown>, line 227)
- /home/graham/workspace/experiments/llm_call/src/llm_call/proof_of_concept/code/task_004_test_prompts/poc_35_parallel_tests.py (line 381): expected an indented block after 'if' statement on line 380 (<unknown>, line 381)
- /home/graham/workspace/experiments/llm_call/src/llm_call/core/api/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/llm_call/src/llm_call/core/api/mcp_handler_enhanced.py (line 16): invalid syntax (<unknown>, line 16)
- /home/graham/workspace/experiments/llm_call/src/llm_call/rl_integration/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/llm_call/archive/root_cleanup/test_iterations/test_cli_comprehensive_fixed.py (line 128): unexpected indent (<unknown>, line 128)
- /home/graham/workspace/experiments/llm_call/archive/root_cleanup/test_files/test_max_text_001_proper.py (line 198): expected an indented block after 'if' statement on line 196 (<unknown>, line 198)
- /home/graham/workspace/experiments/llm_call/archive/root_cleanup/test_files/test_single_case_017.py (line 170): expected an indented block after 'if' statement on line 168 (<unknown>, line 170)
- /home/graham/workspace/experiments/llm_call/archive/root_cleanup/test_files/test_single_case_017_v2.py (line 205): expected an indented block after 'if' statement on line 203 (<unknown>, line 205)
- /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/run_all_cli_tests.py (line 346): expected an indented block after 'if' statement on line 345 (<unknown>, line 346)
- /home/graham/workspace/experiments/llm_call/archive/deprecated_tests/test_runpod_routing.py (line 145): closing parenthesis ']' does not match opening parenthesis '(' on line 144 (<unknown>, line 145)
- /home/graham/workspace/experiments/llm_call/archive/gemini_refactor/utils/logging_setup.py (line 18): invalid syntax (<unknown>, line 18)
- /home/graham/workspace/experiments/llm_call/archive/core_verification/retry_simple.py (line 17): invalid syntax (<unknown>, line 17)
- /home/graham/workspace/experiments/llm_call/archive/iterations/task_verification_tests/test_task1_verification.py (line 155): expected an indented block after 'else' statement on line 154 (<unknown>, line 155)
- /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/utils/maintenance/test_edge_operations.py (line 152): unexpected indent (<unknown>, line 152)
- /home/graham/workspace/experiments/arangodb/repos/graphiti/tests/utils/search/search_utils_test.py (line 161): unmatched ')' (<unknown>, line 161)
- /home/graham/workspace/experiments/arangodb/scripts/run_full_test_report.py (line 116): expected an indented block after 'if' statement on line 115 (<unknown>, line 116)
- /home/graham/workspace/experiments/arangodb/scripts/testing/comprehensive_cli_test.py (line 125): expected an indented block after 'if' statement on line 124 (<unknown>, line 125)
- /home/graham/workspace/experiments/arangodb/scripts/testing/comprehensive_test_runner.py (line 367): expected an indented block after 'if' statement on line 366 (<unknown>, line 367)
- /home/graham/workspace/experiments/arangodb/tests/integration/test_entity_extraction_debug.py (line 33): unexpected indent (<unknown>, line 33)
- /home/graham/workspace/experiments/arangodb/tests/integration/test_unsloth_export.py (line 31): unexpected indent (<unknown>, line 31)
- /home/graham/workspace/experiments/arangodb/tests/integration/test_graphiti_memory_integration.py (line 39): unexpected indent (<unknown>, line 39)
- /home/graham/workspace/experiments/arangodb/src/arangodb/integrations/__init__.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/arangodb/src/arangodb/core/fix_scripts/fix_semantic_search.py (line 46): invalid syntax (<unknown>, line 46)
- /home/graham/workspace/experiments/arangodb/src/arangodb/core/utils/formatters.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_main_cli.py (line 257): unindent does not match any outer indentation level (<unknown>, line 257)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_qa_generation_flow.py (line 34): invalid syntax (<unknown>, line 34)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_marker_relationship_extraction.py (line 222): unindent does not match any outer indentation level (<unknown>, line 222)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_vertex_client.py (line 87): expected an indented block after 'if' statement on line 86 (<unknown>, line 87)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_all_modules.py (line 32): invalid syntax (<unknown>, line 32)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_final_validation.py (line 264): expected an indented block after 'if' statement on line 263 (<unknown>, line 264)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_constants.py (line 27): unexpected indent (<unknown>, line 27)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_vector_search.py (line 33): invalid syntax (<unknown>, line 33)
- /home/graham/workspace/experiments/arangodb/archive/deprecated_tests/test_db_connection.py (line 212): expected an indented block after 'try' statement on line 210 (<unknown>, line 212)
- /home/graham/workspace/experiments/arangodb/archive/pre_refactor/memory_agent/example_graphiti_usage.py (line 86): unterminated string literal (detected at line 86) (<unknown>, line 86)
- /home/graham/workspace/experiments/arangodb/archive/experimental/update_llm_utils.py (line 307): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 307)
- /home/graham/workspace/experiments/arangodb/archive/experimental/constants_update.py (line 37): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 37)
- /home/graham/workspace/experiments/arangodb/archive/experimental/add_extract_rationale.py (line 26): unterminated triple-quoted string literal (detected at line 28) (<unknown>, line 26)
- /home/graham/workspace/experiments/arangodb/archive/experimental/final_test_vertex_client.py (line 87): expected an indented block after 'if' statement on line 86 (<unknown>, line 87)
- /home/graham/workspace/experiments/arangodb/archive/temp_scripts/fix_sparta_final.py (line 23): f-string: unmatched '[' (<unknown>, line 23)
- /home/graham/workspace/experiments/arangodb/archive/temp_scripts/fix_sparta_commands.py (line 25): closing parenthesis ')' does not match opening parenthesis '{' (<unknown>, line 25)
- /home/graham/workspace/experiments/arangodb/archive/temp_scripts/fix_sparta_fstrings.py (line 29): f-string: unmatched '[' (<unknown>, line 29)
- /home/graham/workspace/experiments/arangodb/archive/tasks_2/isolated_test_db_operations.py (line 652): unexpected indent (<unknown>, line 652)
- /home/graham/workspace/experiments/arangodb/archive/tests/iterations/test_runner.py (line 147): expected an indented block after 'if' statement on line 146 (<unknown>, line 147)
- /home/graham/workspace/experiments/arangodb/archive/tests/iterations/test_vector_search.py (line 164): expected an indented block after 'if' statement on line 163 (<unknown>, line 164)
- /home/graham/workspace/experiments/arangodb/archive/tests/iterations/cli/test_all_cli_commands.py (line 118): expected an indented block after 'if' statement on line 117 (<unknown>, line 118)
- /home/graham/workspace/experiments/arangodb/archive/tests/iterations/cli/test_cli_final.py (line 116): expected an indented block after 'if' statement on line 115 (<unknown>, line 116)
- /home/graham/workspace/experiments/arangodb/archive/temp_files/temp_constants_update.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/arangodb/archive/temp_files/temp_vertex_test.py (line 93): expected an indented block after 'if' statement on line 92 (<unknown>, line 93)
- /home/graham/workspace/experiments/arangodb/archive/temp_files/temp_constants_update2.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/arangodb/archive/temp_files/temp_constants_final.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/arangodb/archive/debug_scripts/replace_llm_utils.py (line 18): unterminated triple-quoted string literal (detected at line 18) (<unknown>, line 18)
- /home/graham/workspace/experiments/arangodb/archive/debug_scripts/extract_fix.py (line 34): unterminated string literal (detected at line 34) (<unknown>, line 34)
- /home/graham/workspace/experiments/arangodb/archive/debug_scripts/modify_functions.py (line 20): invalid syntax (<unknown>, line 20)
- /home/graham/workspace/experiments/arangodb/examples/llm_json_mode_example.py (line 99): unterminated string literal (detected at line 99) (<unknown>, line 99)
- /home/graham/workspace/experiments/arangodb/examples/gitget/utils/error_handler.py (line 70): invalid syntax (<unknown>, line 70)
- /home/graham/workspace/experiments/sparta/scripts/verify_real_tests.py (line 183): expected an indented block after 'if' statement on line 178 (<unknown>, line 183)
- /home/graham/workspace/experiments/sparta/scripts/run_enhanced_sparta_download.py (line 1): invalid character '✅' (U+2705) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/scripts/demo_configured_reports.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/src/sparta/cli/graph_commands.py (line 6): invalid syntax (<unknown>, line 6)
- /home/graham/workspace/experiments/sparta/src/sparta/cli/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_impl.py (line 6): invalid syntax (<unknown>, line 6)
- /home/graham/workspace/experiments/sparta/src/sparta/integrations/sparta_module_updated.py (line 8): invalid syntax (<unknown>, line 8)
- /home/graham/workspace/experiments/sparta/src/sparta/integrations/real_apis.py (line 14): invalid syntax (<unknown>, line 14)
- /home/graham/workspace/experiments/sparta/src/sparta/core/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/sparta/src/sparta/core/graph/__init__.py (line 6): invalid syntax (<unknown>, line 6)
- /home/graham/workspace/experiments/sparta/src/sparta/core/reports/_archive_custom_reporters/universal_report_generator.py (line 345): f-string: invalid syntax (<unknown>, line 345)
- /home/graham/workspace/experiments/sparta/archive/generate_final_validation_report.py (line 1): invalid character '📑' (U+1F4D1) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/generate_final_validation_summary.py (line 1): invalid character '📑' (U+1F4D1) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/fix_profiler.py (line 9): invalid syntax (<unknown>, line 9)
- /home/graham/workspace/experiments/sparta/archive/claude-test-reporter-files/examples/test_report_with_base_url.py (line 1): invalid character '✅' (U+2705) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/claude-test-reporter-files/examples/test_download_report.py (line 1): invalid character '📄' (U+1F4C4) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/claude-test-reporter-files/examples/demo_configured_reports.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/deprecated_tests/run_tests.py (line 173): expected an indented block after 'if' statement on line 172 (<unknown>, line 173)
- /home/graham/workspace/experiments/sparta/archive/deprecated_tests/run_tests_with_reporter.py (line 9): unterminated string literal (detected at line 9) (<unknown>, line 9)
- /home/graham/workspace/experiments/sparta/archive/deprecated_tests/run_sparta_tests.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/temp_scripts/install_all_communication_files.py (line 604): unterminated string literal (detected at line 604) (<unknown>, line 604)
- /home/graham/workspace/experiments/sparta/archive/temp_scripts/create_all_files.py (line 159): unterminated string literal (detected at line 159) (<unknown>, line 159)
- /home/graham/workspace/experiments/sparta/archive/temp_scripts/update_imports.py (line 82): unterminated string literal (detected at line 82) (<unknown>, line 82)
- /home/graham/workspace/experiments/sparta/archive/temp_scripts/fix_mock_imports.py (line 36): unterminated string literal (detected at line 36) (<unknown>, line 36)
- /home/graham/workspace/experiments/sparta/archive/sparta_old/communication/archive/claude_desktop_code/all_code.py (line 567): invalid syntax (<unknown>, line 567)
- /home/graham/workspace/experiments/sparta/archive/sparta_old/communication/archive/claude_desktop_code/progress_tracker.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/sparta/archive/sparta_old/reports/_archive_custom_reporters/universal_report_generator.py (line 306): f-string: invalid syntax (<unknown>, line 306)
- /home/graham/workspace/experiments/sparta/archive/test_scripts/test_enhanced_downloader.py (line 1): invalid character '✅' (U+2705) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/test_scripts/test_report_with_base_url.py (line 1): invalid character '✅' (U+2705) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/archive/test_scripts/test_download_report.py (line 1): invalid character '📄' (U+1F4C4) (<unknown>, line 1)
- /home/graham/workspace/experiments/sparta/examples/sparta_enhanced_hybrid_example.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/marker/repos/unsloth/unsloth/kernels/moe/tests/common.py (line 196): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 196)
- /home/graham/workspace/experiments/marker/repos/unsloth/tests/qlora/test_unsloth_qlora_train_and_merge.py (line 15): unexpected character after line continuation character (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/repos/unsloth/tests/qlora/test_hf_qlora_train_and_merge.py (line 15): unexpected character after line continuation character (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/server.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/tests/test_get_bytes_stream.py (line 165): unmatched ')' (<unknown>, line 165)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/io_storages/tests/test_proxy_api.py (line 90): invalid syntax (<unknown>, line 90)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/core/version.py (line 54): unterminated string literal (detected at line 54) (<unknown>, line 54)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_presign_storage_data.py (line 164): invalid syntax (<unknown>, line 164)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/test_api.py (line 273): unmatched ')' (<unknown>, line 273)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/data_import/test_uploader.py (line 88): invalid syntax (<unknown>, line 88)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/tests/tasks/test_functions.py (line 94): invalid syntax (<unknown>, line 94)
- /home/graham/workspace/experiments/marker/repos/label-studio/label_studio/projects/tests/test_project_sample_task.py (line 228): invalid syntax (<unknown>, line 228)
- /home/graham/workspace/experiments/marker/repos/camelot/tests/test_image_conversion_backend.py (line 58): unindent does not match any outer indentation level (<unknown>, line 58)
- /home/graham/workspace/experiments/marker/scripts/sparta_extractor.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/scripts/generate_test_report_extractors.py (line 283): expected an indented block after 'if' statement on line 282 (<unknown>, line 283)
- /home/graham/workspace/experiments/marker/scripts/demos/simple_cli_demo.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/scripts/demo/add_section_breadcrumbs.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/finetuning/utils/data_import.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/finetuning/utils/check_model_compatibility.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/docker/label-studio/test_setup.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/src/marker/cli/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/services/litellm_enhanced.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/setup.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/cli/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/cli/formatters.py (line 1): unexpected indent (<unknown>, line 1)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/cli/debug_commands.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/cli/app.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/core/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/validators/citation.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/llm_call/config/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/utils/markdown_extractor.py (line 27): unexpected indent (<unknown>, line 27)
- /home/graham/workspace/experiments/marker/src/marker/core/utils/table_extractor.py (line 28): unexpected indent (<unknown>, line 28)
- /home/graham/workspace/experiments/marker/src/marker/core/utils/document_debugger.py (line 17): invalid syntax (<unknown>, line 17)
- /home/graham/workspace/experiments/marker/src/marker/core/processors/code_improvements.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/marker/src/marker/core/processors/enhanced_code.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/core/processors/enhanced_camelot/processor.py (line 376): unexpected indent (<unknown>, line 376)
- /home/graham/workspace/experiments/marker/src/marker/core/processors/llm/llm_image_description_async.py (line 37): unexpected indent (<unknown>, line 37)
- /home/graham/workspace/experiments/marker/src/marker/core/config/table.py (line 11): invalid syntax (<unknown>, line 11)
- /home/graham/workspace/experiments/marker/src/marker/core/schema/enhanced_document.py (line 17): invalid syntax (<unknown>, line 17)
- /home/graham/workspace/experiments/marker/src/marker/rl_integration/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/src/marker/rl_integration/feature_extractor.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/marker/archive/comms/claude_module_query.py (line 0): [Errno 2] No such file or directory: '/home/graham/workspace/experiments/marker/archive/comms/claude_module_query.py'
- /home/graham/workspace/experiments/marker/archive/comms/tests/test_comms.py (line 144): expected an indented block after 'if' statement on line 143 (<unknown>, line 144)
- /home/graham/workspace/experiments/marker/archive/comms/src/marker_comms/examples/arangodb_communication_example.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/marker_comms/examples/query_arangodb_pdf_requirements.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/marker_comms/examples/marker_to_arangodb_integration.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/marker_comms/examples/arangodb_api_example.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/claude_comms/examples/arangodb_communication_example.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/claude_comms/examples/query_arangodb_pdf_requirements.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/claude_comms/examples/marker_to_arangodb_integration.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/comms/src/claude_comms/examples/arangodb_api_example.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/old_tests/integration/test_real_extraction.py (line 25): unterminated string literal (detected at line 25) (<unknown>, line 25)
- /home/graham/workspace/experiments/marker/archive/old_tests/processors/code/test_code_detection.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/old_tests/processors/code/test_full_tree_sitter_extraction.py (line 31): unterminated string literal (detected at line 31) (<unknown>, line 31)
- /home/graham/workspace/experiments/marker/archive/old_tests/processors/code/test_tree_sitter_fixed.py (line 31): unterminated string literal (detected at line 31) (<unknown>, line 31)
- /home/graham/workspace/experiments/marker/archive/old_tests/processors/code/test_fixed_code_processor.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/utils_debug/show_code_blocks_fixed.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/utils_debug/examine_code_blocks.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/utils_debug/show_code_blocks.py (line 15): invalid syntax (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/test_cli.py (line 168): expected an indented block after 'if' statement on line 167 (<unknown>, line 168)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/test_enhanced_features.py (line 286): expected an indented block after 'if' statement on line 285 (<unknown>, line 286)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/core/services/test_litellm_service.py (line 129): '[' was never closed (<unknown>, line 129)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/core/processors/test_claude_post_processor_integration.py (line 417): invalid syntax (<unknown>, line 417)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/core/processors/test_claude_table_merge_analyzer.py (line 285): invalid syntax (<unknown>, line 285)
- /home/graham/workspace/experiments/marker/archive/deprecated_tests/features/test_summarizer.py (line 148): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 148)
- /home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_claude_section_verifier.py (line 409): unmatched ')' (<unknown>, line 409)
- /home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_enhanced_table_processor.py (line 111): invalid syntax (<unknown>, line 111)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/fix_arangodb_renderer.py (line 15): unexpected character after line continuation character (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/minimal_arangodb_converter.py (line 15): invalid character '🔄' (U+1F504) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/final_arangodb_converter.py (line 15): invalid character '🔄' (U+1F504) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/run_arangodb_extraction.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/debug_arangodb_issues.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/extract_and_analyze.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/direct_arangodb_test.py (line 25): unterminated string literal (detected at line 25) (<unknown>, line 25)
- /home/graham/workspace/experiments/marker/archive/debug_scripts/simple_arangodb_test.py (line 25): invalid character '🔄' (U+1F504) (<unknown>, line 25)
- /home/graham/workspace/experiments/marker/examples/marker_arangodb_communication_demo.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/markdown_extractor.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/arangodb_import.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/enhanced_camelot_usage.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/module_query_demo.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/section_hierarchy.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/enhanced_document_processing.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/arango_setup.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/table_data_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/enhanced_features_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/arangodb_json_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/arangodb_operations_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/async_image_processing_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/test_semantic_search.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/camelot_table_extractor.py (line 15): unexpected character after line continuation character (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/section_hierarchy_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/document_vector_similarity_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/marker_doc_object.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/litellm_cache_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/arango_vector_index_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/code_language_detection_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/simple/vector_search_debug.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/marker/examples/litellm/mcp_litellm/mcp_server.py (line 15): unterminated string literal (detected at line 15) (<unknown>, line 15)
- /home/graham/workspace/experiments/youtube_transcripts/tests/integration/test_database_adapter.py (line 126): unexpected unindent (<unknown>, line 126)
- /home/graham/workspace/experiments/youtube_transcripts/tests/integration/test_arangodb_features.py (line 173): unexpected unindent (<unknown>, line 173)
- /home/graham/workspace/experiments/youtube_transcripts/tests/integration/test_research_pipeline_edge_cases.py (line 51): unexpected unindent (<unknown>, line 51)
- /home/graham/workspace/experiments/youtube_transcripts/tests/level_0/test_youtube_transcripts_standardized.py (line 33): unexpected unindent (<unknown>, line 33)
- /home/graham/workspace/experiments/youtube_transcripts/tests/level_3/test_multi_module_orchestration.py (line 56): unexpected unindent (<unknown>, line 56)
- /home/graham/workspace/experiments/youtube_transcripts/tests/archive/deprecated_2025_06_06/test_rate_limit_honeypot.py (line 299): unmatched '}' (<unknown>, line 299)
- /home/graham/workspace/experiments/youtube_transcripts/tests/archive/deprecated_2025_06_06/test_youtube_error_handling.py (line 179): expected an indented block after function definition on line 178 (<unknown>, line 179)
- /home/graham/workspace/experiments/youtube_transcripts/archive/deprecated_tests/test_arangodb_connection.py (line 154): expected an indented block after 'else' statement on line 153 (<unknown>, line 154)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/model.py (line 1): unexpected indent (<unknown>, line 1)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/utils/reward_score/prime_code/testing_util.py (line 554): unexpected indent (<unknown>, line 554)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/verl/models/mcore/registry.py (line 160): unexpected indent (<unknown>, line 160)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/test_protocol.py (line 356): unexpected indent (<unknown>, line 356)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/workers/rollout/test_async_sglang_server.py (line 55): unexpected indent (<unknown>, line 55)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/workers/rollout/test_sglang_async_rollout_sf_tools.py (line 60): invalid syntax (<unknown>, line 60)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/sandbox/test_sandbox.py (line 28): invalid syntax (<unknown>, line 28)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/trainer/ppo/test_metric_utils.py (line 162): expected an indented block after function definition on line 161 (<unknown>, line 162)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/DeepRetrieval/code/verl/utils/model.py (line 68): unexpected indent (<unknown>, line 68)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/fact-check/fact-check.py (line 373): f-string expression part cannot include a backslash (<unknown>, line 373)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/api_calls/speed_tests/tgi-speed.py (line 80): expected 'except' or 'finally' block (<unknown>, line 80)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/api_calls/speed_tests/llamacpp_speed-concurrent.py (line 44): expected 'except' or 'finally' block (<unknown>, line 44)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/api_calls/predictions/buggy_code_fixed.py (line 1): unterminated string literal (detected at line 1) (<unknown>, line 1)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/api_calls/regex_tests/tgi-regex.py (line 53): expected 'except' or 'finally' block (<unknown>, line 53)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/server_and_api_setup/server_scaling/utils/load_testing.py (line 36): unexpected indent (<unknown>, line 36)
- /home/graham/workspace/experiments/youtube_transcripts/archive/repos/ADVANCED-inference/trelis-mcp/lite-llm-mcp/test_agent.py (line 66): unexpected indent (<unknown>, line 66)
- /home/graham/workspace/experiments/fine_tuning/repos/unsloth/unsloth/kernels/moe/tests/common.py (line 179): invalid syntax. Perhaps you forgot a comma? (<unknown>, line 179)
- /home/graham/workspace/experiments/fine_tuning/repos/ADVANCED-fine-tuning/wip_scripts/upload_to_hub.py (line 18): f-string: empty expression not allowed (<unknown>, line 18)
- /home/graham/workspace/experiments/fine_tuning/tests/unit/test_msmarco_loader.py (line 38): unexpected indent (<unknown>, line 38)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/cli/runpod_commands.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/utils/memory.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/utils/logging.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/evaluation/multi_model_evaluator.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/inference/merge_adapter.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/inference/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/validation/model_validator.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/unsloth/core/config.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/fine_tuning/src/fine_tuning/cli/app.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/fine_tuning/src/fine_tuning/integrations/__init__.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/fine_tuning/archive/deprecated_tests/test_verification_engine.py (line 363): expected an indented block after 'if' statement on line 361 (<unknown>, line 363)
- /home/graham/workspace/experiments/fine_tuning/archive/deprecated_tests/test_suite.py (line 678): invalid decimal literal (<unknown>, line 678)
- /home/graham/workspace/experiments/fine_tuning/archive/backup_files/main_minimal.py (line 9): invalid syntax (<unknown>, line 9)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/__main__.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/cli/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/proposals/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/database/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/analysis/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/core/scrapers/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/src/darpa_crawl/mcp/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/darpa_crawl/archive/test_integration_old.py (line 152): unexpected indent (<unknown>, line 152)
- /home/graham/workspace/experiments/darpa_crawl/archive/deprecated_tests/test_reporter_integration.py (line 177): expected an indented block after 'if' statement on line 176 (<unknown>, line 177)
- /home/graham/workspace/experiments/darpa_crawl/archive/deprecated_tests/run_tests.py (line 72): expected an indented block after 'if' statement on line 71 (<unknown>, line 72)
- /home/graham/workspace/experiments/darpa_crawl/archive/deprecated_tests/test_arangodb_integration.py (line 29): f-string expression part cannot include a backslash (<unknown>, line 29)
- /home/graham/workspace/experiments/darpa_crawl/archive/deprecated_tests/test_darpa_crawl_simulation.py (line 184): unterminated triple-quoted string literal (detected at line 227) (<unknown>, line 184)
- /home/graham/workspace/experiments/chat/backend/dashboard/routes_broken.py (line 38): unexpected indent (<unknown>, line 38)
- /home/graham/workspace/experiments/chat/backend/dashboard/performance_cache.py (line 2): unexpected indent (<unknown>, line 2)
- /home/graham/workspace/experiments/chat/frontend/create_task104_files.py (line 114): unmatched '}' (<unknown>, line 114)
- /home/graham/workspace/experiments/chat/tests/__init__.py (line 7): invalid syntax (<unknown>, line 7)
- /home/graham/workspace/experiments/chat/archive/deprecated_tests/test_dashboard_implementation.py (line 170): expected an indented block after 'if' statement on line 169 (<unknown>, line 170)
- /home/graham/workspace/experiments/annotator/tests/active_annotator/frontend/__init__.py (line 0): [Errno 21] Is a directory: '/home/graham/workspace/experiments/annotator/tests/active_annotator/frontend/__init__.py'
- /home/graham/workspace/experiments/annotator/src/annotator/recipes/pdf_boundingbox.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/annotator/src/annotator/integrations/__init__.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/annotator/archive/deprecated_tests/test_responsive_ui.py (line 52): invalid syntax (<unknown>, line 52)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/scripts/__init__.py (line 12): invalid decimal literal (<unknown>, line 12)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/scripts/homepage.py (line 463): unmatched ')' (<unknown>, line 463)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/help/test_help.py (line 49): unexpected indent (<unknown>, line 49)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/scrape/test_scrape.py (line 137): unmatched ')' (<unknown>, line 137)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/browser/test_browser.py (line 24): expected an indented block after function definition on line 23 (<unknown>, line 24)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_reasoning.py (line 35): unexpected indent (<unknown>, line 35)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_sanity_check_repo.py (line 94): unexpected indent (<unknown>, line 94)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_onboarding.py (line 74): unmatched ')' (<unknown>, line 74)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_editor.py (line 108): invalid syntax (<unknown>, line 108)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_repo.py (line 116): expected an indented block after function definition on line 115 (<unknown>, line 116)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_linter.py (line 45): expected an indented block after function definition on line 44 (<unknown>, line 45)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_ssl_verification.py (line 36): unexpected indent (<unknown>, line 36)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_udiff.py (line 31): unexpected indent (<unknown>, line 31)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_repomap.py (line 185): unexpected indent (<unknown>, line 185)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_main.py (line 790): unmatched '}' (<unknown>, line 790)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_io.py (line 57): unexpected indent (<unknown>, line 57)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_wholefile.py (line 119): unexpected indent (<unknown>, line 119)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_scripting.py (line 26): expected an indented block after function definition on line 25 (<unknown>, line 26)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_sendchat.py (line 36): unexpected indent (<unknown>, line 36)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_model_info_manager.py (line 41): expected an indented block after function definition on line 39 (<unknown>, line 41)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_coder.py (line 412): unexpected indent (<unknown>, line 412)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_commands.py (line 1046): unmatched ')' (<unknown>, line 1046)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_deprecated.py (line 38): unexpected indent (<unknown>, line 38)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_aws_credentials.py (line 40): unexpected indent (<unknown>, line 40)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_editblock.py (line 124): unexpected indent (<unknown>, line 124)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_voice.py (line 30): unexpected indent (<unknown>, line 30)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_models.py (line 33): unexpected indent (<unknown>, line 33)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/benchmark/test_benchmark.py (line 45): unexpected indent (<unknown>, line 45)
- /home/graham/workspace/experiments/aider-daemon/repos/aider/benchmark/swe_bench.py (line 22): unmatched ')' (<unknown>, line 22)
- /home/graham/workspace/experiments/aider-daemon/scripts/__init__.py (line 14): invalid decimal literal (<unknown>, line 14)
- /home/graham/workspace/experiments/aider-daemon/scripts/test_with_report.py (line 140): expected an indented block after 'if' statement on line 139 (<unknown>, line 140)
- /home/graham/workspace/experiments/aider-daemon/scripts/homepage.py (line 463): unmatched ')' (<unknown>, line 463)
- /home/graham/workspace/experiments/aider-daemon/tests/unit/mcp/test_integration.py (line 138): unexpected unindent (<unknown>, line 138)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/ui/tui/__init__.py (line 6): invalid syntax (<unknown>, line 6)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/ui/tui/views/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/ui/tui/utils/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/ui/tui/models/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/cli/session_cli.py (line 6): invalid syntax (<unknown>, line 6)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/cli/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/lsp/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/integrations/__init__.py (line 4): invalid syntax (<unknown>, line 4)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/integrations/aider_daemon_module.py (line 8): invalid syntax (<unknown>, line 8)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/__init__.py (line 5): invalid syntax (<unknown>, line 5)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/session_browser.py (line 230): expected ':' (<unknown>, line 230)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/mcp/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/aider-daemon/src/aider_daemon/modules/code_generator.py (line 770): unmatched ')' (<unknown>, line 770)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/run_loop2_tests.py (line 186): expected an indented block after 'if' statement on line 185 (<unknown>, line 186)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_udiff.py (line 31): unexpected indent (<unknown>, line 31)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_repomap.py (line 185): unexpected indent (<unknown>, line 185)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_honeypot.py (line 33): unexpected indent (<unknown>, line 33)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_commands.py (line 1046): unmatched ')' (<unknown>, line 1046)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/test_aws_credentials.py (line 40): unexpected indent (<unknown>, line 40)
- /home/graham/workspace/experiments/aider-daemon/archive/deprecated_tests/integration/test_module_integrations.py (line 32): unexpected indent (<unknown>, line 32)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_reasoning.py (line 35): unexpected indent (<unknown>, line 35)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_sanity_check_repo.py (line 94): unexpected indent (<unknown>, line 94)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_onboarding.py (line 83): unexpected indent (<unknown>, line 83)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_editor.py (line 108): invalid syntax (<unknown>, line 108)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_ssl_verification.py (line 164): unexpected indent (<unknown>, line 164)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_main.py (line 970): unmatched '}' (<unknown>, line 970)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_io.py (line 234): invalid syntax (<unknown>, line 234)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_wholefile.py (line 119): unexpected indent (<unknown>, line 119)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_sendchat.py (line 77): unexpected indent (<unknown>, line 77)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_model_info_manager.py (line 66): invalid syntax (<unknown>, line 66)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_coder.py (line 412): unexpected indent (<unknown>, line 412)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_scrape.py (line 137): unmatched ')' (<unknown>, line 137)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_editblock.py (line 124): unexpected indent (<unknown>, line 124)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_voice.py (line 30): unexpected indent (<unknown>, line 30)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_help.py (line 49): unexpected indent (<unknown>, line 49)
- /home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_models.py (line 33): unexpected indent (<unknown>, line 33)
- /home/graham/workspace/experiments/aider-daemon/archive/20250605/tests/legacy/basic/basic/test_deprecated.py (line 38): unexpected indent (<unknown>, line 38)
- /home/graham/workspace/experiments/aider-daemon/archive/tests/tests/unit/core/storage/test_arangodb_backend.py (line 71): unmatched ')' (<unknown>, line 71)
- /home/graham/workspace/experiments/aider-daemon/archive/tests/tests/unit/mcp/test_mcp_client.py (line 209): unmatched ')' (<unknown>, line 209)
- /home/graham/workspace/experiments/aider-daemon/benchmark/test_benchmark.py (line 45): unexpected indent (<unknown>, line 45)
- /home/graham/workspace/experiments/aider-daemon/benchmark/swe_bench.py (line 22): unmatched ')' (<unknown>, line 22)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/tests/test_honeypot.py (line 87): unexpected unindent (<unknown>, line 87)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/config_improved.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/logging_config.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/__main__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/conversion_guide_prompt.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/handlers.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/prompt_manager.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/deep_research_analysis_prompt.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/comprehensive_research_guide.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/code_analysis_prompt.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/content_description_prompt.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/prompts/prompts.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/utils/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/summarize_paper.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/describe_content.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/system_stats.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/conversion_options.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/search_enhanced.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/semantic_search.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/analyze_code.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/read_paper.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/tools/list_papers.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp_server/resources/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/src/arxiv_mcp/integrations/__init__.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/archive/deprecated_tests/run_tests.py (line 125): expected an indented block after 'if' statement on line 124 (<unknown>, line 125)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/archive/scripts/update_search_tqdm.py (line 26): invalid syntax (<unknown>, line 26)
- /home/graham/workspace/mcp-servers/arxiv-mcp-server/archive/scripts/fix_hardware_display.py (line 13): invalid syntax (<unknown>, line 13)
- /home/graham/workspace/experiments/mcp-screenshot/src/mcp_screenshot/core/annotate.py (line 3): invalid syntax (<unknown>, line 3)
- /home/graham/workspace/experiments/mcp-screenshot/archive/deprecated_tests/test_batch.py (line 39): unexpected indent (<unknown>, line 39)
- /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_runner.py (line 559): invalid syntax (<unknown>, line 559)
- /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_perf_cli.py (line 82): invalid syntax (<unknown>, line 82)
- /home/graham/workspace/experiments/gitget/repos/pyperf_sparse/pyperf/tests/test_metadata.py (line 138): invalid syntax (<unknown>, line 138)
- /home/graham/workspace/experiments/gitget/repos/gitingest/tests/test_repository_clone.py (line 168): unmatched ')' (<unknown>, line 168)
- /home/graham/workspace/experiments/gitget/repos/gitingest/tests/query_parser/test_query_parser.py (line 493): unexpected indent (<unknown>, line 493)
- /home/graham/workspace/experiments/gitget/repos/python-arango_sparse/tests/test_cursor.py (line 118): invalid syntax (<unknown>, line 118)
- /home/graham/workspace/experiments/gitget/repos/python-arango_sparse/tests/test_aql.py (line 114): invalid syntax (<unknown>, line 114)
- /home/graham/workspace/experiments/gitget/tests/unit/test_honeypot.py (line 211): unmatched '}' (<unknown>, line 211)
- /home/graham/workspace/experiments/gitget/tests/unit/test_cache.py (line 179): unexpected unindent (<unknown>, line 179)
- /home/graham/workspace/experiments/gitget/tests/performance/test_streaming.py (line 134): unexpected unindent (<unknown>, line 134)
- /home/graham/workspace/experiments/gitget/tests/performance/test_parallel.py (line 74): unexpected unindent (<unknown>, line 74)
- /home/graham/workspace/experiments/gitget/archive/deprecated_tests/gitget/test_workflow.py (line 90): invalid syntax (<unknown>, line 90)
- /home/graham/workspace/experiments/gitget/archive/claude_clutter/direct_litellm_cache_test.py (line 82): expected an indented block after 'if' statement on line 76 (<unknown>, line 82)
- /home/graham/workspace/experiments/gitget/archive/tests/tests/gitget/test_processing.py (line 54): unexpected indent (<unknown>, line 54)
- /home/graham/workspace/experiments/gitget/archive/tests/tests/gitget/test_clone.py (line 68): unmatched ')' (<unknown>, line 68)
- /home/graham/workspace/experiments/gitget/archive/tests/tests/gitget/cli/test_commands.py (line 60): unexpected indent (<unknown>, line 60)
- /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_runner.py (line 559): invalid syntax (<unknown>, line 559)
- /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_perf_cli.py (line 82): invalid syntax (<unknown>, line 82)
- /home/graham/workspace/experiments/gitget/examples/workflows/repos/pyperf_sparse/pyperf/tests/test_metadata.py (line 138): invalid syntax (<unknown>, line 138)

### Failed Level 0 Tests (6 projects)

These projects failed basic functionality tests:

- **llm_call** (Level 2 (Processing Infrastructure)): Level 0 test failed
- **arangodb** (Level 2 (Processing Infrastructure)): Level 0 test failed
- **sparta** (Level 3 (Processing Spokes)): Level 0 test failed
- **marker** (Level 3 (Processing Spokes)): Level 0 test failed
- **aider_daemon** (Level 4 (User Interfaces)): Level 0 test failed
- **mcp_screenshot** (Level 5 (MCP Services)): Level 0 test failed

## Recommendations

1. **Remove all mocks** - Replace with real API calls
2. **Fix imports** - Convert all relative imports to absolute
3. **Install dependencies** - Ensure all deps are available
4. **Fix syntax errors** - Files must parse correctly
5. **Fix failed tests** - Address Level 0 test failures