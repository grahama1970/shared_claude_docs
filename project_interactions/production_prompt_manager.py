#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: production_prompt_manager.py
Description: Production-ready prompt management system with caching and validation

External Dependencies:
- pyyaml: https://pyyaml.org/wiki/PyYAMLDocumentation

Sample Input:
>>> pm = ProductionPromptManager()
>>> prompt = pm.render("analyze_results", total=10, passed=8, failed=2)

Expected Output:
>>> print(prompt[:50] + "...")
You are analyzing test results. You MUST report t...

Example Usage:
>>> from production_prompt_manager import ProductionPromptManager
>>> pm = ProductionPromptManager()
>>> prompt = pm.render("code_review", file_path="main.py", diff="...", language="python")
"""

from pathlib import Path
from typing import Dict, Any, Optional, Set
from string import Template
import json
import hashlib
import time
from dataclasses import dataclass
from functools import lru_cache
import yaml


@dataclass
class PromptMetadata:
    """Metadata for a prompt template"""
    name: str
    description: str
    version: str
    required_vars: Set[str]
    optional_vars: Set[str]
    model_requirements: Dict[str, Any]
    tags: list[str]


class ProductionPromptManager:
    """Production-grade prompt management with validation and caching"""
    
    def __init__(self, prompts_dir: str = "prompts", cache_ttl: int = 3600):
        self.prompts_dir = Path(prompts_dir)
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, tuple[str, float]] = {}
        self._metadata: Dict[str, PromptMetadata] = {}
        self._load_metadata()
    
    def _load_metadata(self):
        """Load prompt metadata from config file"""
        config_path = self.prompts_dir / "config.yaml"
        if config_path.exists():
            with open(config_path) as f:
                config = yaml.safe_load(f)
                
            for name, data in config.get("prompts", {}).items():
                self._metadata[name] = PromptMetadata(
                    name=name,
                    description=data.get("description", ""),
                    version=data.get("version", "1.0.0"),
                    required_vars=set(data.get("variables", {}).get("required", [])),
                    optional_vars=set(data.get("variables", {}).get("optional", [])),
                    model_requirements=data.get("model_requirements", {}),
                    tags=data.get("tags", [])
                )
    
    @lru_cache(maxsize=128)
    def _load_template(self, prompt_name: str) -> str:
        """Load a prompt template from disk with caching"""
        # Try multiple extensions
        for ext in [".txt", ".j2", ".md"]:
            path = self.prompts_dir / f"{prompt_name}{ext}"
            if path.exists():
                return path.read_text()
        
        raise FileNotFoundError(f"No template found for: {prompt_name}")
    
    def _validate_variables(self, prompt_name: str, variables: Dict[str, Any]):
        """Validate required variables are present"""
        metadata = self._metadata.get(prompt_name)
        if metadata:
            missing = metadata.required_vars - set(variables.keys())
            if missing:
                raise ValueError(
                    f"Missing required variables for '{prompt_name}': {missing}"
                )
            
            # Warn about unknown variables
            all_vars = metadata.required_vars | metadata.optional_vars
            unknown = set(variables.keys()) - all_vars
            if unknown:
                print(f"⚠️  Warning: Unknown variables for '{prompt_name}': {unknown}")
    
    def render(self, prompt_name: str, validate: bool = True, **variables) -> str:
        """Render a prompt with the given variables"""
        # Check cache
        cache_key = f"{prompt_name}:{hashlib.md5(str(variables).encode()).hexdigest()}"
        if cache_key in self._cache:
            content, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return content
        
        # Validate variables
        if validate:
            self._validate_variables(prompt_name, variables)
        
        # Load template
        template_content = self._load_template(prompt_name)
        
        # Process variables
        processed_vars = {}
        for key, value in variables.items():
            if isinstance(value, (dict, list)):
                processed_vars[key] = json.dumps(value, indent=2)
            else:
                processed_vars[key] = str(value)
        
        # Render (using simple Template for this example)
        template = Template(template_content)
        rendered = template.safe_substitute(**processed_vars)
        
        # Cache the result
        self._cache[cache_key] = (rendered, time.time())
        
        return rendered
    
    def get_metadata(self, prompt_name: str) -> Optional[PromptMetadata]:
        """Get metadata for a prompt"""
        return self._metadata.get(prompt_name)
    
    def list_prompts(self, tag: Optional[str] = None) -> list[str]:
        """List all available prompts, optionally filtered by tag"""
        if tag:
            return [
                name for name, meta in self._metadata.items()
                if tag in meta.tags
            ]
        return list(self._metadata.keys())
    
    def get_model_requirements(self, prompt_name: str) -> Dict[str, Any]:
        """Get model requirements for a prompt"""
        metadata = self._metadata.get(prompt_name)
        return metadata.model_requirements if metadata else {}


# Example: Refactoring the original problematic code
class RefactoredTestAnalyzer:
    """Clean implementation using external prompts"""
    
    def __init__(self, prompt_manager: Optional[ProductionPromptManager] = None):
        self.prompt_manager = prompt_manager or ProductionPromptManager()
    
    def create_llm_prompt_template(self, test_results: Dict[str, Any]) -> str:
        """
        Create analysis prompt using external template.
        
        This replaces the problematic embedded f-string approach.
        """
        # Prepare variables for the template
        template_vars = {
            "immutable_facts": test_results.get("immutable_facts", {}),
            "total": test_results.get("total", 0),
            "passed": test_results.get("passed", 0),
            "failed": test_results.get("failed", 0),
            "failed_tests": test_results.get("failed_tests", []),
            "warnings": test_results.get("warnings", []),
            "context": test_results.get("context", "")
        }
        
        # Render the prompt from external template
        return self.prompt_manager.render("analyze_results", **template_vars)
    
    def get_model_config(self) -> Dict[str, Any]:
        """Get recommended model configuration for this prompt"""
        return self.prompt_manager.get_model_requirements("analyze_results")


if __name__ == "__main__":
    # Demonstrate the clean approach
    manager = ProductionPromptManager()
    analyzer = RefactoredTestAnalyzer(manager)
    
    # Example test results
    test_results = {
        "immutable_facts": {
            "test_id": "abc123",
            "timestamp": "2025-01-06T10:30:00Z",
            "environment": "production"
        },
        "total": 12,
        "passed": 10,
        "failed": 2,
        "failed_tests": [
            {"name": "test_auth", "error": "Timeout"},
            {"name": "test_validation", "error": "Assert failed"}
        ],
        "warnings": ["Slow test execution", "Deprecated API usage"]
    }
    
    # Generate prompt the clean way
    prompt = analyzer.create_llm_prompt_template(test_results)
    
    print("=== Clean Prompt Generation ===")
    print(f"Prompt length: {len(prompt)} characters")
    print(f"First 300 characters:\n{prompt[:300]}...")
    
    # Show model requirements
    print("\n=== Model Requirements ===")
    print(json.dumps(analyzer.get_model_config(), indent=2))
    
    # List available prompts
    print("\n=== Available Prompts ===")
    print("Testing prompts:", manager.list_prompts(tag="testing"))
    
    print("\n✅ Production-ready prompt management demonstrated!")