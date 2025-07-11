#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: example_prompt_handling.py
Description: Best practices for handling LLM prompts in Python applications

External Dependencies:
- jinja2: https://jinja.palletsprojects.com/
- pydantic: https://docs.pydantic.dev/

Sample Input:
>>> test_results = {
...     "passed": 10,
...     "failed": 2,
...     "total": 12,
...     "immutable_facts": {"test_id": "abc123", "timestamp": "2025-01-06"}
... }

Expected Output:
>>> prompt = load_prompt_from_file("analyze_results", test_results)
>>> print(prompt[:50] + "...")
You are analyzing test results. You MUST report t...

Example Usage:
>>> from example_prompt_handling import PromptManager
>>> pm = PromptManager()
>>> prompt = pm.get_prompt("analyze_results", test_results=test_results)
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from string import Template
import jinja2
from pydantic import BaseModel, Field


# Option 1: Simple file-based approach
class SimplePromptLoader:
    """Load prompts from text files with basic string substitution"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
    
    def load_prompt(self, prompt_name: str, **kwargs) -> str:
        """Load a prompt from file and substitute variables"""
        prompt_path = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {prompt_path}")
        
        # Read the prompt template
        template_str = prompt_path.read_text()
        
        # Use Python's Template for safe substitution
        template = Template(template_str)
        
        # Process any complex data (like dicts) to strings
        processed_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, (dict, list)):
                processed_kwargs[key] = json.dumps(value, indent=2)
            else:
                processed_kwargs[key] = str(value)
        
        return template.safe_substitute(**processed_kwargs)


# Option 2: Jinja2-based approach (more powerful)
class Jinja2PromptManager:
    """Advanced prompt management with Jinja2 templates"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Set up Jinja2 environment
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.prompts_dir)),
            autoescape=False,  # Don't escape for LLM prompts
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['json'] = lambda x: json.dumps(x, indent=2)
        self.env.filters['pretty'] = self._pretty_format
    
    def _pretty_format(self, obj: Any) -> str:
        """Custom formatting for objects"""
        if isinstance(obj, dict):
            return json.dumps(obj, indent=2)
        elif isinstance(obj, list):
            return '\n'.join(f"- {item}" for item in obj)
        return str(obj)
    
    def get_prompt(self, prompt_name: str, **context) -> str:
        """Load and render a Jinja2 template"""
        try:
            template = self.env.get_template(f"{prompt_name}.j2")
            return template.render(**context)
        except jinja2.TemplateNotFound:
            raise FileNotFoundError(f"Prompt template not found: {prompt_name}.j2")


# Option 3: Structured prompt management with validation
class PromptConfig(BaseModel):
    """Configuration for a single prompt"""
    name: str
    description: str
    version: str = "1.0.0"
    model_requirements: Optional[Dict[str, Any]] = Field(default_factory=dict)
    required_variables: list[str] = Field(default_factory=list)
    optional_variables: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class StructuredPromptManager:
    """Production-grade prompt management with validation and versioning"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.prompts_dir)),
            autoescape=False
        )
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def register_prompt(self, config: PromptConfig, template_content: str):
        """Register a new prompt with configuration"""
        # Save config
        config_path = self.prompts_dir / f"{config.name}.json"
        config_path.write_text(config.model_dump_json(indent=2))
        
        # Save template
        template_path = self.prompts_dir / f"{config.name}.j2"
        template_path.write_text(template_content)
        
        # Clear cache
        if config.name in self._cache:
            del self._cache[config.name]
    
    def get_prompt(self, prompt_name: str, validate: bool = True, **context) -> str:
        """Get a prompt with optional validation"""
        # Load config
        config_path = self.prompts_dir / f"{prompt_name}.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Prompt config not found: {prompt_name}")
        
        config = PromptConfig.model_validate_json(config_path.read_text())
        
        # Validate required variables
        if validate:
            missing = set(config.required_variables) - set(context.keys())
            if missing:
                raise ValueError(f"Missing required variables: {missing}")
        
        # Render template
        template = self.jinja_env.get_template(f"{prompt_name}.j2")
        return template.render(**context)


# Option 4: Prompt versioning and A/B testing
class VersionedPromptManager(StructuredPromptManager):
    """Extended manager with versioning and experimentation support"""
    
    def get_prompt_version(self, prompt_name: str, version: str, **context) -> str:
        """Get a specific version of a prompt"""
        versioned_name = f"{prompt_name}_v{version.replace('.', '_')}"
        return self.get_prompt(versioned_name, **context)
    
    def get_prompt_experiment(self, prompt_name: str, experiment_id: str, **context) -> str:
        """Get an experimental variant of a prompt"""
        experimental_name = f"{prompt_name}_exp_{experiment_id}"
        try:
            return self.get_prompt(experimental_name, **context)
        except FileNotFoundError:
            # Fall back to base version
            return self.get_prompt(prompt_name, **context)


# Example: How to refactor the problematic code
def create_example_prompts():
    """Create example prompt files"""
    prompts_dir = Path("prompts")
    prompts_dir.mkdir(exist_ok=True)
    
    # Simple template format
    simple_prompt = """You are analyzing test results. You MUST report these EXACT facts:

IMMUTABLE TEST RESULTS:
=======================
$immutable_facts

TEST SUMMARY:
============
Total Tests: $total
Passed: $passed
Failed: $failed

Analyze these results and provide insights."""
    
    (prompts_dir / "analyze_results.txt").write_text(simple_prompt)
    
    # Jinja2 template format
    jinja_prompt = """You are analyzing test results. You MUST report these EXACT facts:

IMMUTABLE TEST RESULTS:
=======================
{{ immutable_facts | json }}

TEST SUMMARY:
============
Total Tests: {{ total }}
Passed: {{ passed }}
Failed: {{ failed }}
Success Rate: {{ "%.1f" | format((passed / total * 100) if total > 0 else 0) }}%

{% if failed > 0 %}
FAILED TESTS:
============
{% for test in failed_tests %}
- {{ test.name }}: {{ test.error }}
{% endfor %}
{% endif %}

Analyze these results and provide insights."""
    
    (prompts_dir / "analyze_results.j2").write_text(jinja_prompt)
    
    # Create config for structured approach
    config = PromptConfig(
        name="analyze_results",
        description="Analyze test execution results",
        version="1.0.0",
        model_requirements={
            "min_context_length": 4096,
            "supports_json": True
        },
        required_variables=["immutable_facts", "total", "passed", "failed"],
        optional_variables=["failed_tests", "execution_time"],
        tags=["testing", "analysis", "qa"]
    )
    
    (prompts_dir / "analyze_results.json").write_text(config.model_dump_json(indent=2))


# Example usage showing the refactored approach
class TestAnalyzer:
    """Refactored test analyzer using proper prompt management"""
    
    def __init__(self, prompt_manager: Optional[Jinja2PromptManager] = None):
        self.prompt_manager = prompt_manager or Jinja2PromptManager()
    
    def analyze_results(self, test_results: Dict[str, Any]) -> str:
        """Generate analysis prompt for test results"""
        # Instead of embedding the prompt in the function,
        # we load it from an external template
        prompt = self.prompt_manager.get_prompt(
            "analyze_results",
            immutable_facts=test_results.get("immutable_facts", {}),
            total=test_results.get("total", 0),
            passed=test_results.get("passed", 0),
            failed=test_results.get("failed", 0),
            failed_tests=test_results.get("failed_tests", [])
        )
        
        return prompt


if __name__ == "__main__":
    # Create example prompts
    create_example_prompts()
    
    # Test data
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
            {"name": "test_authentication", "error": "Timeout after 30s"},
            {"name": "test_data_validation", "error": "Expected 5, got 4"}
        ]
    }
    
    print("=== Option 1: Simple Template ===")
    simple_loader = SimplePromptLoader()
    simple_prompt = simple_loader.load_prompt(
        "analyze_results",
        immutable_facts=test_results["immutable_facts"],
        total=test_results["total"],
        passed=test_results["passed"],
        failed=test_results["failed"]
    )
    print(simple_prompt[:200] + "...\n")
    
    print("=== Option 2: Jinja2 Template ===")
    jinja_manager = Jinja2PromptManager()
    jinja_prompt = jinja_manager.get_prompt("analyze_results", **test_results)
    print(jinja_prompt[:200] + "...\n")
    
    print("=== Option 3: Structured with Validation ===")
    structured_manager = StructuredPromptManager()
    try:
        structured_prompt = structured_manager.get_prompt("analyze_results", **test_results)
        print(structured_prompt[:200] + "...")
    except FileNotFoundError:
        print("(Would work with proper setup)")
    
    print("\n✅ All prompt management examples demonstrated!")