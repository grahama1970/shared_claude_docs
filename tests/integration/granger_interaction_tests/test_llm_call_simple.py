#!/usr/bin/env python3
"""
Module: test_llm_call_simple.py
Description: Simple test of llm_call with OpenAI to verify understanding

External Dependencies:
- llm_call: Universal LLM interface
- openai: OpenAI SDK

Sample Input:
>>> prompt = "Verify Granger understanding..."

Expected Output:
>>> {"success": True, "response": "...", "model": "gpt-4"}

Example Usage:
>>> python test_llm_call_simple.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add llm_call to path
sys.path.insert(0, '/home/graham/workspace/experiments/llm_call/src')

from loguru import logger
from llm_call.core.caller import make_llm_request


async def verify_granger_understanding():
    """Use GPT-4 to verify my Granger understanding."""
    
    verification_content = """I need you to verify my understanding of the Granger ecosystem. Here's what I understand:

# Granger Ecosystem Architecture

## Core Concept: Flexible Hub-and-Spoke
- **NO fixed pipelines** - agents dynamically compose workflows
- Any module can be called in any order
- Agents decide what to call based on the task
- Complete flexibility is the key innovation

## Module Categories:
1. **Hub**: granger_hub - orchestrates communication
2. **RL Core**: rl_commons - optimizes decisions
3. **Spokes**: ArXiv, Marker, ArangoDB, SPARTA, YouTube, etc.
4. **UIs**: Chat, Annotator, Aider-Daemon

## Interaction Levels:
- **Level 0**: Single module calls (any order)
- **Level 1**: Two-module pipelines (dynamically composed)
- **Level 2**: Complex workflows (RL-optimized)
- **Level 3**: Multi-agent collaboration

## RL Integration:
- Contextual Bandits for module selection
- DQN for pipeline optimization
- PPO for resource allocation
- Hierarchical RL for complex workflows

## Key Innovation:
Unlike traditional ML pipelines with fixed sequences (A→B→C), Granger allows:
- A→C→B or B→A→C or just C
- Skip modules if not needed
- Retry with different modules on failure
- Learn optimal patterns over time

Is this understanding correct? What am I missing?"""
    
    try:
        # Use GPT-4 for verification
        config = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an expert in distributed AI systems and modular architectures."},
                {"role": "user", "content": verification_content}
            ],
            "temperature": 0.0,
            "max_tokens": 2000
        }
        
        logger.info("Calling GPT-4 for verification...")
        response = await make_llm_request(config)
        
        print("\n=== GPT-4 Verification Response ===")
        print(response.get("response", "No response"))
        
        # Save to file
        with open("gpt4_verification.txt", "w") as f:
            f.write(response.get("response", ""))
        
        return response
        
    except Exception as e:
        logger.error(f"GPT-4 call failed: {e}")
        return None


async def test_interaction_examples():
    """Test understanding with concrete examples."""
    
    examples = """Please verify these Granger interaction examples:

## Example 1: Research Task (Level 0)
Agent receives: "Find papers on quantum computing"
```python
# Agent decides to just search ArXiv
result = arxiv.search("quantum computing")
# Done - no need for other modules
```

## Example 2: Document Processing (Level 1)
Agent receives: "Extract content from this research paper"
```python
# Agent dynamically creates pipeline
pdf = arxiv.download(paper_id)
content = marker.extract(pdf)
# Agent could also store in ArangoDB if needed
if important_paper:
    arangodb.store(content)
```

## Example 3: Security Analysis (Level 2)
Agent receives: "Analyze security vulnerabilities in this codebase"
```python
# Complex workflow with RL optimization
vulnerabilities = sparta.scan(codebase)
if vulnerabilities.severity == "HIGH":
    # RL suggests searching for patches
    patches = arxiv.search(f"patches for {vulnerabilities}")
    videos = youtube.search(f"fixing {vulnerabilities}")
    # Store findings
    arangodb.store_graph({
        "vuln": vulnerabilities,
        "patches": patches,
        "tutorials": videos
    })
```

## Example 4: Multi-Agent (Level 3)
```python
# Multiple agents collaborate
research_agent = Agent("researcher")
security_agent = Agent("security")
learning_agent = Agent("learner")

# They share findings via hub
hub.publish(research_agent.findings)
security_agent.analyze(hub.get_latest())
learning_agent.update_model(hub.get_all())
```

Are these examples correct representations of Granger's flexibility?"""
    
    try:
        config = {
            "model": "gpt-3.5-turbo",  # Use 3.5 for examples
            "messages": [
                {"role": "system", "content": "You are an expert in distributed AI systems."},
                {"role": "user", "content": examples}
            ],
            "temperature": 0.0,
            "max_tokens": 1500
        }
        
        logger.info("Testing examples with GPT-3.5...")
        response = await make_llm_request(config)
        
        print("\n=== Example Verification ===")
        print(response.get("response", "No response"))
        
        return response
        
    except Exception as e:
        logger.error(f"Example test failed: {e}")
        return None


async def main():
    """Run LLM verification tests."""
    print("=== Testing LLM Call Module ===\n")
    
    # First verify we can make any LLM call
    logger.info("Testing basic LLM functionality...")
    
    # Test 1: Verify understanding
    understanding = await verify_granger_understanding()
    
    # Test 2: Verify examples
    examples = await test_interaction_examples()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Understanding verification: {'✅ Success' if understanding else '❌ Failed'}")
    print(f"Example verification: {'✅ Success' if examples else '❌ Failed'}")
    
    if understanding:
        print("\nKey points from verification:")
        response_text = understanding.get("response", "")
        if "correct" in response_text.lower():
            print("✅ Core understanding verified as correct")
        if "missing" in response_text.lower() or "addition" in response_text.lower():
            print("📝 Additional insights provided")
    
    return bool(understanding or examples)


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)