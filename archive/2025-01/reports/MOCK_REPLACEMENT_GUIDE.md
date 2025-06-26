# Mock Replacement Implementation Guide

These files had mocks removed and need real implementations:


## aider_daemon

- `/home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_history.py` (12 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/repos/aider/tests/basic/test_analytics.py` (3 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/src/aider_daemon/core/event_system.py` (2 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_analytics.py` (3 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_repo.py` (3 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_linter.py` (3 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_scripting.py` (2 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/legacy_tests/test_browser.py` (2 mocks removed)
- `/home/graham/workspace/experiments/aider-daemon/archive/tests/tests/legacy/basic/basic/test_history.py` (12 mocks removed)

## arangodb

- `/home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_gemini.py` (8 mocks removed)
- `/home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_openai.py` (8 mocks removed)
- `/home/graham/workspace/experiments/arangodb/repos/graphiti/tests/embedder/test_voyage.py` (7 mocks removed)
- `/home/graham/workspace/experiments/arangodb/repos/graphiti/tests/llm_client/test_anthropic_client.py` (7 mocks removed)

## claude_test_reporter

- `/home/graham/workspace/experiments/claude-test-reporter/src/claude_test_reporter/analyzers/mock_detector.py` (2 mocks removed)

## gitget

- `/home/graham/workspace/experiments/gitget/archive/deprecated_tests/gitget/test_api.py` (2 mocks removed)
- `/home/graham/workspace/experiments/gitget/archive/deprecated_tests/gitget/test_summarization_additional.py` (1 mocks removed)

## granger_hub

- `/home/graham/workspace/experiments/granger_hub/repos/aider/tests/browser/test_browser.py` (2 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_analytics.py` (3 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_linter.py` (3 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_scripting.py` (2 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/repos/aider/tests/basic/test_sendchat.py` (4 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/tests/integration_scenarios/base/module_mock.py` (6 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_self_improvement_system.py` (12 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/test_satellite_firmware.py` (2 mocks removed)
- `/home/graham/workspace/experiments/granger_hub/archive/deprecated_tests/cli/test_screenshot_commands.py` (13 mocks removed)

## llm_call

- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/guardrails_tests/test_tracing_guardrails.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_endpoints.py` (8 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/router_unit_tests/test_router_helper_utils.py` (6 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/image_gen_tests/test_image_variation.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/pass_through_endpoints/test_pass_through_endpoints.py` (12 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/auth/test_auth_exception_handler.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/health_endpoints/test_health_endpoints.py` (5 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/db/test_check_migration.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/anthropic_endpoints/test_endpoints.py` (3 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/client/test_users.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_common_daily_activity.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_key_management_endpoints.py` (12 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/proxy/management_endpoints/test_tag_management_endpoints.py` (13 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/enterprise/enterprise_callbacks/send_emails/test_resend_email.py` (5 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/databricks/test_databricks_common_utils.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/llms/vertex_ai/test_http_status_201.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/test_anthropic_cache_control_hook.py` (9 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/litellm/integrations/arize/test_arize_utils.py` (1 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_bedrock_knowledgebase_hook.py` (10 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langfuse_unit_tests.py` (5 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langfuse_e2e_test.py` (8 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_gcs_pub_sub.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_unit_tests_init_callbacks.py` (8 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_langsmith_unit_test.py` (3 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_generic_api_callback.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_datadog.py` (3 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/logging_callback_tests/test_opentelemetry_unit_tests.py` (1 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_openai_o1.py` (5 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_bedrock_embedding.py` (1 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/base_llm_unit_tests.py` (6 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_infinity.py` (20 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_cohere.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_huggingface_chat_completion.py` (6 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_nvidia_nim.py` (7 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_anthropic_completion.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_rerank.py` (10 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_deepseek_completion.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_triton.py` (6 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_litellm_proxy_provider.py` (16 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_text_completion_unit_tests.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_azure_o_series.py` (8 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_translation/test_fireworks_ai_translation.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_custom_callback_router.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_gcs_bucket.py` (2 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_opik.py` (1 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_embedding.py` (22 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_completion_with_retries.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_completion_cost.py` (3 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_retries.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_sagemaker.py` (16 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_text_completion.py` (5 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_provider_specific_config.py` (9 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_braintrust.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_whisper.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_prometheus_service.py` (4 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_get_model_info.py` (3 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/local_testing/test_router_budget_limiter.py` (1 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/litellm/tests/llm_responses_api_testing/test_openai_responses_api.py` (14 mocks removed)
- `/home/graham/workspace/experiments/llm_call/repos/ADVANCED-inference/trelis-mcp/lite-llm-mcp/test_agent.py` (10 mocks removed)
- `/home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_max_model_routing_functional.py` (20 mocks removed)
- `/home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_rl_integration_comprehensive.py` (8 mocks removed)
- `/home/graham/workspace/experiments/llm_call/archive/deprecated_tests/llm_call/core/test_claude_collaboration.py` (6 mocks removed)

## marker

- `/home/graham/workspace/experiments/marker/archive/deprecated_tests/core/processors/test_claude_structure_analyzer.py` (2 mocks removed)
- `/home/graham/workspace/experiments/marker/archive/tests/tests/core/services/utils/test_litellm_cache.py` (8 mocks removed)
- `/home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_claude_content_validator.py` (2 mocks removed)
- `/home/graham/workspace/experiments/marker/archive/tests/tests/core/processors/test_claude_image_describer.py` (2 mocks removed)

## shared_docs

- `/home/graham/workspace/shared_claude_docs/api_gateway/tests/test_middleware.py` (3 mocks removed)
- `/home/graham/workspace/shared_claude_docs/project_interactions/granger_verify_phase1.py` (5 mocks removed)
- `/home/graham/workspace/shared_claude_docs/tests/granger_interaction_tests/verify_granger_understanding.py` (3 mocks removed)

## unsloth

- `/home/graham/workspace/experiments/fine_tuning/archive/deprecated_tests/test_entropy_aware_thinking.py` (10 mocks removed)

## youtube_transcripts

- `/home/graham/workspace/experiments/youtube_transcripts/scripts/remove_mocks_from_tests.py` (2 mocks removed)
- `/home/graham/workspace/experiments/youtube_transcripts/archive/repos/verl/tests/reward_score/test_sandbox_fusion.py` (4 mocks removed)

## Implementation Guidelines

1. **Use Real Services**: Connect to actual databases, APIs, etc.
2. **Environment Setup**: Document what services need to be running
3. **Flexible Assertions**: Don't expect exact data, verify structure
4. **Error Handling**: Real services can fail - handle gracefully
