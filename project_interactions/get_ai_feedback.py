#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Get feedback from multiple AI sources on bug hunt results.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

def get_perplexity_feedback(report_content):
    """Get feedback from Perplexity AI."""
    print("🔍 Getting feedback from Perplexity...")
    
    prompt = f"""As a software testing expert, analyze these Granger bug hunt results:

{report_content}

Provide critical feedback on:
1. Are the 3 remaining error message bugs truly low priority?
2. Is 100% test pass rate suspicious or legitimate?
3. What critical tests might be missing?
4. Are the test durations (0.5-0.9s) indicative of real work?
5. Any patterns or concerns you notice?

Be skeptical and thorough."""

    # Use perplexity-ask command
    cmd = [
        sys.executable, 
        "/home/graham/.claude/commands/perplexity-ask.py",
        prompt
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Perplexity error: {result.stderr}"
    except Exception as e:
        return f"Failed to get Perplexity feedback: {e}"

def get_gemini_feedback(report_content):
    """Get feedback from Gemini using direct API."""
    print("🔍 Getting feedback from Gemini...")
    
    try:
        import google.generativeai as genai
        
        # Configure Gemini
        api_key = "AIzaSyDn3iI70uflxg4NzoQ09zH9yVzvBqbnx9c"
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""As a software quality assurance expert, critically analyze these bug hunt results:

{report_content}

Focus on:
1. Test coverage adequacy - what's missing?
2. Bug severity assessment - are LOW priorities correct?
3. Root cause analysis quality
4. Test implementation thoroughness
5. Recommendations for next iteration

Compare to your previous feedback and assess improvement."""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Failed to get Gemini feedback: {e}"

def synthesize_feedback(perplexity_feedback, gemini_feedback):
    """Synthesize feedback from both AI sources."""
    synthesis = f"""# AI Feedback Synthesis - Bug Hunt Iteration

**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Perplexity AI Feedback

{perplexity_feedback}

## Gemini AI Feedback

{gemini_feedback}

## Key Takeaways

Based on both AI analyses:
1. **Consensus Issues**: Points both AIs agree on
2. **Divergent Views**: Where they disagree
3. **Action Items**: Specific improvements needed
4. **Next Steps**: Prioritized list of fixes

## Iteration Plan

1. Address highest priority feedback
2. Implement suggested improvements
3. Re-run enhanced tests
4. Get updated AI feedback
"""
    
    return synthesis

def main():
    """Get AI feedback on bug hunt results."""
    # Read the latest bug hunt report
    report_path = Path("001_Bug_Hunt_Report.md")
    if not report_path.exists():
        print("Error: No bug hunt report found")
        return 1
        
    report_content = report_path.read_text()
    
    # Get feedback from both sources
    perplexity_feedback = get_perplexity_feedback(report_content[:3000])  # Limit size
    gemini_feedback = get_gemini_feedback(report_content[:3000])
    
    # Synthesize feedback
    synthesis = synthesize_feedback(perplexity_feedback, gemini_feedback)
    
    # Save synthesis
    synthesis_path = Path("001_AI_Feedback_Synthesis.md")
    synthesis_path.write_text(synthesis)
    
    print(f"\n✅ AI feedback synthesis saved to: {synthesis_path}")
    
    # Also create action items
    actions = {
        "iteration": 1,
        "perplexity_concerns": "Check output for concerns",
        "gemini_concerns": "Check output for concerns",
        "next_actions": [
            "Review AI feedback",
            "Implement suggested fixes",
            "Re-run bug hunter",
            "Continue until all concerns addressed"
        ]
    }
    
    actions_path = Path("001_AI_Feedback_Actions.json")
    actions_path.write_text(json.dumps(actions, indent=2))
    
    print(f"📋 Action items saved to: {actions_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())