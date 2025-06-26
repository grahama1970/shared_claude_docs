#!/usr/bin/env python3
"""Query Gemini for verification of Granger understanding."""

import asyncio
import sys
sys.path.insert(0, '/home/graham/workspace/experiments/llm_call/src')

from llm_call.api import ask

async def query_gemini():
    """Query Gemini with verification request."""
    
    # Read the verification request
    with open('/home/graham/workspace/shared_claude_docs/tests/granger_interaction_tests/GEMINI_VERIFICATION_REQUEST.md', 'r') as f:
        verification_request = f.read()
    
    # Truncate to first 2000 chars to avoid token limits
    verification_request = verification_request[:2000] + "\n\n[Content truncated for length. Please focus on verifying my understanding of flexible agent-module interactions in Granger.]"
    
    print("Sending verification request to Gemini...")
    
    try:
        response = await ask(
            prompt=verification_request,
            model="gemini-2.0-flash-exp",
            system="You are an expert in distributed systems and reinforcement learning. Please verify Claude's understanding of the Granger ecosystem.",
            temperature=0.7
        )
        
        print("\n" + "="*60)
        print("GEMINI'S VERIFICATION RESPONSE:")
        print("="*60 + "\n")
        print(response)
        
        # Save response
        with open('/home/graham/workspace/shared_claude_docs/tests/granger_interaction_tests/GEMINI_VERIFICATION_RESPONSE.md', 'w') as f:
            f.write(f"# Gemini's Verification Response\n\n{response}")
        
        return response
        
    except Exception as e:
        print(f"Error querying Gemini: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(query_gemini())
    if result:
        print("\n\nResponse saved to GEMINI_VERIFICATION_RESPONSE.md")