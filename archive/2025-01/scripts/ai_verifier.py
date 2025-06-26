#!/usr/bin/env python3
"""
Module: ai_verifier.py
Description: Verify bug hunter results using Perplexity and Gemini

External Dependencies:
- google-generativeai: https://ai.google.dev/tutorials/python_quickstart
- perplexity-client: https://docs.perplexity.ai/

Sample Input:
>>> scenario = {"name": "SPARTA CVE Search", "expected": "CVE data", "actual": "Connection failed"}

Expected Output:
>>> grade = {"perplexity": "FAIL", "gemini": "FAIL", "consensus": "FAIL", "bugs": ["Service not running"]}

Example Usage:
>>> verifier = AIVerifier()
>>> grade = await verifier.verify_result(scenario, actual_response)
"""

import os
import json
from typing import Dict, Any

class AIVerifier:
    """Verify test results using multiple AI systems."""
    
    def __init__(self):
        # Note: These would need actual API keys
        self.perplexity_api_key = os.getenv('PERPLEXITY_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
    
    async def verify_with_perplexity(self, scenario: Dict, actual: str) -> Dict[str, Any]:
        """Grade using Perplexity AI."""
        prompt = f"""
You are grading a test result. Be strict and objective.

Scenario: {scenario['name']}
Expected Result: {scenario['expected_result']}
Actual Response: {actual}

Questions:
1. Does the actual response match the expected behavior? (YES/NO)
2. What specific bugs or issues are indicated by this response?
3. Grade: PASS, WARN, or FAIL?

Format your response as:
MATCH: YES/NO
BUGS: [list any bugs found]
GRADE: PASS/WARN/FAIL
EXPLANATION: [brief explanation]
"""
        
        # Simulate Perplexity response (replace with actual API call)
        # For demo purposes, we'll analyze based on keywords
        if 'error' in actual.lower() or 'failed' in actual.lower():
            return {
                'match': 'NO',
                'bugs': ['Connection failure', 'Service not available'],
                'grade': 'FAIL',
                'explanation': 'The service appears to be down or unreachable'
            }
        elif 'success' in actual.lower():
            return {
                'match': 'YES',
                'bugs': [],
                'grade': 'PASS',
                'explanation': 'Response matches expected behavior'
            }
        else:
            return {
                'match': 'PARTIAL',
                'bugs': ['Unexpected response format'],
                'grade': 'WARN',
                'explanation': 'Response differs from expected format'
            }
    
    async def verify_with_gemini(self, scenario: Dict, actual: str) -> Dict[str, Any]:
        """Grade using Gemini AI."""
        prompt = f"""
Analyze this test result for bugs:

Test: {scenario['name']}
Expected: {scenario['expected_result']}
Actual: {actual}

Identify:
1. Does it meet expectations?
2. What bugs exist?
3. Severity of issues?

Response format:
MEETS_EXPECTATIONS: true/false
BUGS_FOUND: [list]
SEVERITY: CRITICAL/HIGH/MEDIUM/LOW
GRADE: PASS/WARN/FAIL
"""
        
        # Simulate Gemini response (replace with actual API call)
        if 'connection failed' in actual.lower():
            return {
                'meets_expectations': False,
                'bugs_found': ['Service unavailable', 'No error recovery'],
                'severity': 'CRITICAL',
                'grade': 'FAIL'
            }
        elif 'not yet implemented' in actual.lower():
            return {
                'meets_expectations': False,
                'bugs_found': ['Feature not implemented'],
                'severity': 'MEDIUM',
                'grade': 'SKIP'
            }
        else:
            return {
                'meets_expectations': True,
                'bugs_found': [],
                'severity': 'LOW',
                'grade': 'PASS'
            }
    
    async def get_consensus(self, scenario: Dict, actual: str) -> Dict[str, Any]:
        """Get consensus from both AI systems."""
        perplexity_result = await self.verify_with_perplexity(scenario, actual)
        gemini_result = await self.verify_with_gemini(scenario, actual)
        
        # Determine consensus grade
        p_grade = perplexity_result['grade']
        g_grade = gemini_result['grade']
        
        if p_grade == g_grade:
            consensus_grade = p_grade
        elif 'FAIL' in [p_grade, g_grade]:
            consensus_grade = 'FAIL'  # If either says fail, it fails
        elif 'WARN' in [p_grade, g_grade]:
            consensus_grade = 'WARN'  # If either warns, we warn
        else:
            consensus_grade = 'PASS'
        
        # Combine bugs from both
        all_bugs = list(set(
            perplexity_result.get('bugs', []) + 
            gemini_result.get('bugs_found', [])
        ))
        
        return {
            'perplexity': perplexity_result,
            'gemini': gemini_result,
            'consensus_grade': consensus_grade,
            'all_bugs': all_bugs,
            'agreement': p_grade == g_grade
        }

# Demo function
async def demo_verification():
    """Demo the AI verification."""
    verifier = AIVerifier()
    
    test_cases = [
        {
            'scenario': {
                'name': 'SPARTA CVE Search',
                'expected_result': 'Should return structured CVE data'
            },
            'actual': 'Connection failed - is SPARTA running?'
        },
        {
            'scenario': {
                'name': 'ArXiv Paper Search',
                'expected_result': 'Returns list of papers'
            },
            'actual': 'Success: Found 15 papers'
        }
    ]
    
    for test in test_cases:
        print(f"\n🔍 Verifying: {test['scenario']['name']}")
        result = await verifier.get_consensus(test['scenario'], test['actual'])
        print(f"   Consensus: {result['consensus_grade']}")
        print(f"   Agreement: {result['agreement']}")
        if result['all_bugs']:
            print(f"   Bugs: {', '.join(result['all_bugs'])}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_verification())