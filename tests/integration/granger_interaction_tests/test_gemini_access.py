#!/usr/bin/env python3
"""
Module: test_gemini_access.py
Description: Test access to Gemini via llm_call for verification

External Dependencies:
- llm_call: Universal LLM interface
- litellm: LLM routing library
- google-cloud-aiplatform: Vertex AI SDK

Sample Input:
>>> prompt = "Please verify my understanding of Granger..."

Expected Output:
>>> {"success": True, "response": "Your understanding is...", "model": "gemini-1.5-pro"}

Example Usage:
>>> python test_gemini_access.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add llm_call to path
sys.path.insert(0, '/home/graham/workspace/experiments/llm_call/src')

from loguru import logger

# Set up environment for Vertex AI
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/graham/workspace/shared_claude_docs/vertex_ai_service_account.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "gen-lang-client-0870473940"
os.environ["LITELLM_VERTEX_PROJECT"] = "gen-lang-client-0870473940"
os.environ["LITELLM_VERTEX_LOCATION"] = "us-central1"

# Import llm_call components
from llm_call.tools.conversational_delegator import conversational_delegate
from llm_call.core.caller import make_llm_request


async def test_gemini_direct():
    """Test direct Gemini access."""
    print("\n=== Testing Direct Gemini Access ===")
    
    # Read the verification request
    verification_path = Path("/home/graham/workspace/shared_claude_docs/tests/granger_interaction_tests/GEMINI_VERIFICATION_REQUEST.md")
    
    if verification_path.exists():
        with open(verification_path, 'r') as f:
            verification_content = f.read()
    else:
        verification_content = """Please verify that I understand the Granger ecosystem correctly:

1. Granger uses a flexible hub-and-spoke architecture where agents can call any module in any order
2. There are NO fixed pipelines - everything is dynamically composed
3. Reinforcement Learning optimizes module selection and parameters
4. The key is flexibility - agents decide what to call based on the task

Is this understanding correct?"""
    
    try:
        # Direct LLM call
        config = {
            "model": "vertex_ai/gemini-1.5-pro",
            "messages": [
                {"role": "system", "content": "You are an expert in distributed AI systems and the Granger ecosystem."},
                {"role": "user", "content": verification_content}
            ],
            "temperature": 0.0,
            "max_tokens": 4096
        }
        
        logger.info("Making direct Gemini call...")
        response = await make_llm_request(config)
        
        print("\n=== Gemini Response ===")
        print(response.get("response", "No response"))
        
        return response
        
    except Exception as e:
        logger.error(f"Direct call failed: {e}")
        return None


async def test_conversational_gemini():
    """Test conversational Gemini access."""
    print("\n=== Testing Conversational Gemini Access ===")
    
    try:
        # Start a conversation
        result = await conversational_delegate(
            model="vertex_ai/gemini-1.5-pro",
            prompt="I'm going to share my understanding of the Granger ecosystem for verification.",
            conversation_name="granger-verification",
            temperature=0.0,
            system_prompt="You are an expert in distributed AI systems reviewing the Granger architecture."
        )
        
        conversation_id = result.get("conversation_id")
        print(f"Started conversation: {conversation_id}")
        print(f"Initial response: {result.get('response', '')[:200]}...")
        
        # Continue with the verification
        result2 = await conversational_delegate(
            model="vertex_ai/gemini-1.5-pro",
            prompt="""Here's my understanding of Granger:

1. **Flexible Hub-and-Spoke Architecture**: Any agent can call any module in any order
2. **No Fixed Pipelines**: Agents dynamically compose workflows based on the task
3. **RL Optimization**: Contextual bandits optimize module selection, DQN optimizes pipelines
4. **Key Innovation**: Complete flexibility - no predetermined sequences

The interaction levels are:
- Level 0: Single module calls (flexible order)
- Level 1: Two-module pipelines (dynamically composed)
- Level 2: Complex workflows (RL-optimized)
- Level 3: Multi-agent collaboration

Is this correct? What am I missing?""",
            conversation_id=conversation_id,
            temperature=0.0
        )
        
        print(f"\nGemini Verification Response:")
        print(result2.get("response", "No response"))
        
        return result2
        
    except Exception as e:
        logger.error(f"Conversational call failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """Run Gemini access tests."""
    logger.info("Testing Gemini access via llm_call...")
    
    # Test direct access
    direct_result = await test_gemini_direct()
    
    # Test conversational access
    conv_result = await test_conversational_gemini()
    
    # Save results
    results = {
        "direct_call": direct_result is not None,
        "conversational_call": conv_result is not None,
        "responses": {
            "direct": direct_result.get("response", "") if direct_result else None,
            "conversational": conv_result.get("response", "") if conv_result else None
        }
    }
    
    with open("gemini_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== Test Summary ===")
    print(f"Direct call: {'✅ Success' if results['direct_call'] else '❌ Failed'}")
    print(f"Conversational call: {'✅ Success' if results['conversational_call'] else '❌ Failed'}")
    
    return results['direct_call'] or results['conversational_call']


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)