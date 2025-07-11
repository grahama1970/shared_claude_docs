#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: clean_prompt_example.py
Description: Clean example of handling LLM prompts without embedded strings

External Dependencies:
- None (uses only standard library)

Sample Input:
>>> results = {"total": 10, "passed": 8, "failed": 2}

Expected Output:
>>> prompt = load_test_analysis_prompt(results)
>>> print(prompt[:50] + "...")
You are analyzing test results. Total Tests: 10...

Example Usage:
>>> from clean_prompt_example import PromptLoader
>>> loader = PromptLoader()
>>> prompt = loader.load("test_analysis", results)
"""

from pathlib import Path
from string import Template
from typing import Dict, Any
import json


class PromptLoader:
    """Clean prompt loading from external files"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
    
    def load(self, prompt_name: str, variables: Dict[str, Any]) -> str:
        """Load and populate a prompt template"""
        # Load the prompt template
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        template_content = prompt_path.read_text()
        
        # Convert complex objects to strings
        str_vars = {}
        for key, value in variables.items():
            if isinstance(value, (dict, list)):
                str_vars[key] = json.dumps(value, indent=2)
            else:
                str_vars[key] = str(value)
        
        # Use safe substitution to avoid KeyError on missing vars
        template = Template(template_content)
        return template.safe_substitute(**str_vars)


# Example of how to refactor your problematic function
class TestResultAnalyzer:
    """Refactored analyzer using external prompts"""
    
    def __init__(self):
        self.prompt_loader = PromptLoader()
    
    def create_llm_prompt_template(self, test_results: Dict[str, Any]) -> str:
        """Create prompt from external template instead of embedded string"""
        return self.prompt_loader.load("analyze_results", {
            "immutable_facts": test_results.get("immutable_facts", {}),
            "total": test_results.get("total", 0),
            "passed": test_results.get("passed", 0),
            "failed": test_results.get("failed", 0)
        })


if __name__ == "__main__":
    # Demo the clean approach
    analyzer = TestResultAnalyzer()
    
    test_data = {
        "immutable_facts": {"test_id": "123", "timestamp": "2025-01-06"},
        "total": 10,
        "passed": 8,
        "failed": 2
    }
    
    prompt = analyzer.create_llm_prompt_template(test_data)
    print("Generated prompt (first 200 chars):")
    print(prompt[:200] + "...")
    print("\n✅ Clean prompt handling demonstrated!")