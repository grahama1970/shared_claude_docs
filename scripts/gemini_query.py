#!/usr/bin/env python3
"""
Simple Gemini query tool that works without complex dependencies.
Uses direct API calls to Gemini.
"""

import os
import json
import requests
import sys
from typing import Optional

def query_gemini(prompt: str, model: str = "gemini-2.0-flash-exp") -> Optional[str]:
    """
    Query Gemini API directly.
    
    Args:
        prompt: The prompt to send to Gemini
        model: The Gemini model to use
        
    Returns:
        The response text or None if error
    """
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: No GEMINI_API_KEY or GOOGLE_API_KEY found in environment")
        return None
    
    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    # Request body
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 8192,
        }
    }
    
    try:
        # Make request
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        if "candidates" in result and result["candidates"]:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            return content
        else:
            print(f"Unexpected response format: {json.dumps(result, indent=2)}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def main():
    """Main function to handle command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python gemini_query.py 'Your prompt here'")
        sys.exit(1)
    
    # Get prompt from command line
    prompt = ' '.join(sys.argv[1:])
    
    # Query Gemini
    print("Querying Gemini...")
    response = query_gemini(prompt)
    
    if response:
        print("\n" + "="*60)
        print("GEMINI RESPONSE:")
        print("="*60 + "\n")
        print(response)
    else:
        print("Failed to get response from Gemini")
        sys.exit(1)

if __name__ == "__main__":
    main()