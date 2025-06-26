#!/usr/bin/env python3
"""
Universal LLM query tool supporting multiple providers.
Works with minimal dependencies using direct API calls.
"""

import os
import json
import sys
from typing import Optional, Dict, Any
import urllib.request
import urllib.parse
import urllib.error

def query_llm(prompt: str, model: str = "gemini-2.0-flash", **kwargs) -> Dict[str, Any]:
    """
    Query any supported LLM.
    
    Supported models:
    - gemini-2.0-flash (Google Gemini)
    - gpt-4, gpt-3.5-turbo (OpenAI)
    - claude-3-opus, claude-3-sonnet (Anthropic)
    
    Returns dict with 'success', 'response', and 'error' keys.
    """
    
    # Determine provider from model name
    if "gemini" in model.lower():
        return query_gemini(prompt, model, **kwargs)
    elif "gpt" in model.lower():
        return query_openai(prompt, model, **kwargs)
    elif "claude" in model.lower():
        return query_anthropic(prompt, model, **kwargs)
    else:
        return {"success": False, "error": f"Unknown model: {model}"}

def query_gemini(prompt: str, model: str = "gemini-2.0-flash", **kwargs) -> Dict[str, Any]:
    """Query Google Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return {
            "success": False,
            "error": "No GEMINI_API_KEY or GOOGLE_API_KEY found",
            "response": "[MOCK] Gemini would analyze: " + prompt[:100] + "..."
        }
    
    # Fix model name
    if model == "gemini-2.0-flash-exp":
        model = "gemini-2.0-flash"
    elif model == "gemini-1.5-pro":
        model = "gemini-1.5-pro"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": kwargs.get("temperature", 0.7),
            "maxOutputTokens": kwargs.get("max_tokens", 8192),
        }
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if "candidates" in result and result["candidates"]:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"success": True, "response": content, "model": model}
        else:
            return {"success": False, "error": "Unexpected response format", "raw": result}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def query_openai(prompt: str, model: str = "gpt-4", **kwargs) -> Dict[str, Any]:
    """Query OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return {
            "success": False,
            "error": "No OPENAI_API_KEY found",
            "response": "[MOCK] GPT would respond: " + prompt[:100] + "..."
        }
    
    url = "https://api.openai.com/v1/chat/completions"
    
    messages = kwargs.get("messages", [{"role": "user", "content": prompt}])
    if kwargs.get("system"):
        messages.insert(0, {"role": "system", "content": kwargs["system"]})
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 2000)
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if "choices" in result and result["choices"]:
            content = result["choices"][0]["message"]["content"]
            return {"success": True, "response": content, "model": model}
        else:
            return {"success": False, "error": "Unexpected response format", "raw": result}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def query_anthropic(prompt: str, model: str = "claude-3-opus-20240229", **kwargs) -> Dict[str, Any]:
    """Query Anthropic API."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        return {
            "success": False,
            "error": "No ANTHROPIC_API_KEY found",
            "response": "[MOCK] Claude would respond: " + prompt[:100] + "..."
        }
    
    url = "https://api.anthropic.com/v1/messages"
    
    messages = kwargs.get("messages", [{"role": "user", "content": prompt}])
    if kwargs.get("system"):
        system_prompt = kwargs["system"]
    else:
        system_prompt = "You are a helpful AI assistant."
    
    data = {
        "model": model,
        "messages": messages,
        "system": system_prompt,
        "temperature": kwargs.get("temperature", 0.7),
        "max_tokens": kwargs.get("max_tokens", 2000)
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        if "content" in result and result["content"]:
            content = result["content"][0]["text"]
            return {"success": True, "response": content, "model": model}
        else:
            return {"success": False, "error": "Unexpected response format", "raw": result}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Main entry point for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Query any LLM")
    parser.add_argument("prompt", help="The prompt to send")
    parser.add_argument("--model", default="gemini-2.0-flash", help="Model to use")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    parser.add_argument("--max-tokens", type=int, default=2000, help="Max tokens")
    parser.add_argument("--system", help="System prompt")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    # Support reading from file
    prompt = args.prompt
    if prompt.startswith("@") and len(prompt) > 1:
        with open(prompt[1:], 'r') as f:
            prompt = f.read()
    
    # Query LLM
    print(f"Querying {args.model}...", file=sys.stderr)
    result = query_llm(
        prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        system=args.system
    )
    
    # Output result
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["success"]:
            print(result["response"])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            if "response" in result:  # Mock response
                print(f"\n{result['response']}")
            sys.exit(1)

if __name__ == "__main__":
    main()