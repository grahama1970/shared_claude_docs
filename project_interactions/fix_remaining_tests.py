#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Fix the remaining test implementation issues by adding proper validation logic.
"""

import sys
import os
import time
import asyncio
from pathlib import Path

# Add proper implementation for Pipeline Data Isolation
def implement_pipeline_isolation():
    """Add real pipeline isolation validation to granger_hub."""
    granger_hub_path = Path("/home/graham/workspace/experiments/granger_hub/src/granger_hub/pipeline_isolation.py")
    
    isolation_code = '''"""
Pipeline Data Isolation Implementation
Ensures data separation between pipeline instances.
"""

import threading
import uuid
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PipelineInstance:
    """Isolated pipeline instance with its own data context."""
    id: str
    created_at: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    
    def get_data(self, key: str) -> Optional[Any]:
        """Thread-safe data retrieval."""
        with self._lock:
            return self.data.get(key)
    
    def set_data(self, key: str, value: Any):
        """Thread-safe data storage."""
        with self._lock:
            self.data[key] = value
            
    def clear(self):
        """Clear all instance data."""
        with self._lock:
            self.data.clear()


class PipelineIsolationManager:
    """Manages isolated pipeline instances."""
    
    def __init__(self):
        self.instances: Dict[str, PipelineInstance] = {}
        self._global_lock = threading.Lock()
        
    def create_instance(self) -> str:
        """Create a new isolated pipeline instance."""
        instance_id = str(uuid.uuid4())
        with self._global_lock:
            self.instances[instance_id] = PipelineInstance(
                id=instance_id,
                created_at=datetime.now()
            )
        return instance_id
    
    def get_instance(self, instance_id: str) -> Optional[PipelineInstance]:
        """Get a specific pipeline instance."""
        with self._global_lock:
            return self.instances.get(instance_id)
    
    def verify_isolation(self, instance_id1: str, instance_id2: str) -> bool:
        """Verify data isolation between two instances."""
        inst1 = self.get_instance(instance_id1)
        inst2 = self.get_instance(instance_id2)
        
        if not inst1 or not inst2:
            return False
            
        # Test isolation by setting data in one instance
        test_key = "isolation_test"
        test_value = f"data_from_{instance_id1}"
        
        inst1.set_data(test_key, test_value)
        
        # Verify other instance doesn't have this data
        return inst2.get_data(test_key) is None
    
    def cleanup_instance(self, instance_id: str):
        """Clean up a pipeline instance."""
        with self._global_lock:
            if instance_id in self.instances:
                self.instances[instance_id].clear()
                del self.instances[instance_id]

# Global manager instance
_isolation_manager = PipelineIsolationManager()

def get_isolation_manager() -> PipelineIsolationManager:
    """Get the global isolation manager."""
    return _isolation_manager
'''
    
    # Create the file
    granger_hub_path.parent.mkdir(parents=True, exist_ok=True)
    granger_hub_path.write_text(isolation_code)
    print(f"✅ Created pipeline isolation implementation: {granger_hub_path}")
    
    # Update granger_hub __init__.py to include the isolation manager
    init_path = granger_hub_path.parent / "__init__.py"
    if init_path.exists():
        content = init_path.read_text()
        if "pipeline_isolation" not in content:
            content += "\nfrom .pipeline_isolation import get_isolation_manager, PipelineIsolationManager\n"
            init_path.write_text(content)
            print("✅ Updated granger_hub __init__.py with isolation imports")


def implement_error_analysis():
    """Add comprehensive error analysis capabilities."""
    for module_name in ["arangodb", "sparta", "marker"]:
        module_path = Path(f"/home/graham/workspace/shared_claude_docs/project_interactions/{module_name}")
        error_analyzer_path = module_path / "error_analyzer.py"
        
        analyzer_code = f'''"""
Error Analysis and Quality Assessment for {module_name}
"""

import re
from typing import Dict, List, Tuple

class ErrorAnalyzer:
    """Analyzes error message quality and provides recommendations."""
    
    QUALITY_CRITERIA = {{
        "specificity": [
            (r"\\b(error|failed|invalid|missing)\\b", 1),
            (r"\\b(because|due to|caused by)\\b", 2),
            (r"\\b(expected|got|actual|required)\\b", 2),
        ],
        "actionability": [
            (r"\\b(try|please|should|must|need to)\\b", 2),
            (r"\\b(check|verify|ensure|confirm)\\b", 1),
            (r"\\b(example|e\\.g\\.|for instance)\\b", 3),
        ],
        "context": [
            (r"\\b(at|in|from|during)\\b", 1),
            (r"\\b(line|column|position|location)\\b", 2),
            (r"\\b(module|function|method|class)\\b", 2),
        ]
    }}
    
    @classmethod
    def analyze_error_message(cls, error_msg: str) -> Dict[str, any]:
        """Analyze an error message for quality."""
        scores = {{}}
        total_score = 0
        
        for category, patterns in cls.QUALITY_CRITERIA.items():
            category_score = 0
            matches = []
            
            for pattern, points in patterns:
                if re.search(pattern, error_msg, re.IGNORECASE):
                    category_score += points
                    matches.append(pattern)
            
            scores[category] = {{
                "score": category_score,
                "max_possible": sum(p[1] for p in patterns),
                "matches": matches
            }}
            total_score += category_score
        
        max_total = sum(
            sum(p[1] for p in patterns) 
            for patterns in cls.QUALITY_CRITERIA.values()
        )
        
        quality_rating = "Poor"
        if total_score >= max_total * 0.7:
            quality_rating = "Excellent"
        elif total_score >= max_total * 0.5:
            quality_rating = "Good"
        elif total_score >= max_total * 0.3:
            quality_rating = "Fair"
        
        return {{
            "message": error_msg,
            "total_score": total_score,
            "max_score": max_total,
            "percentage": (total_score / max_total * 100) if max_total > 0 else 0,
            "rating": quality_rating,
            "category_scores": scores,
            "recommendations": cls._generate_recommendations(scores, error_msg)
        }}
    
    @classmethod
    def _generate_recommendations(cls, scores: Dict, error_msg: str) -> List[str]:
        """Generate specific recommendations for improving error messages."""
        recommendations = []
        
        # Check each category
        for category, data in scores.items():
            percentage = (data["score"] / data["max_possible"] * 100) if data["max_possible"] > 0 else 0
            
            if percentage < 50:
                if category == "specificity":
                    recommendations.append("Add specific details about what went wrong")
                    recommendations.append("Include expected vs actual values where applicable")
                elif category == "actionability":
                    recommendations.append("Include suggestions for how to fix the issue")
                    recommendations.append("Provide examples of correct usage")
                elif category == "context":
                    recommendations.append("Include location information (file, line, function)")
                    recommendations.append("Add context about when/where the error occurred")
        
        # Check message length
        if len(error_msg) < 20:
            recommendations.append("Error message is too brief - add more detail")
        
        # Check for generic messages
        generic_patterns = ["error", "failed", "invalid", "wrong"]
        if any(error_msg.lower() == pattern for pattern in generic_patterns):
            recommendations.append("Replace generic error message with specific description")
        
        return recommendations

def test_error_analyzer():
    """Test the error analyzer with sample messages."""
    analyzer = ErrorAnalyzer()
    
    test_messages = [
        "Error",
        "Connection failed",
        "Invalid authentication token",
        "Connection to ArangoDB failed: Unable to reach host 'localhost:8529'. Please check that the database is running and accessible.",
        "Invalid query parameter 'limit': expected integer between 1-1000, got 'abc'. Example: ?limit=10",
        "Authentication failed at line 45 in module 'auth_handler'. Token expired. Please regenerate your API token using 'granger-auth refresh'."
    ]
    
    for msg in test_messages:
        result = analyzer.analyze_error_message(msg)
        print(f"\\nMessage: {{result['message'][:50]}}...")
        print(f"Rating: {{result['rating']}} ({{result['percentage']:.1f}}%)")
        if result['recommendations']:
            print("Recommendations:")
            for rec in result['recommendations']:
                print(f"  - {{rec}}")

if __name__ == "__main__":
    test_error_analyzer()
'''
        
        error_analyzer_path.write_text(analyzer_code)
        print(f"✅ Created error analyzer for {module_name}: {error_analyzer_path}")
        
        # Update module __init__.py
        init_path = module_path / "__init__.py"
        if init_path.exists():
            content = init_path.read_text()
            if "error_analyzer" not in content:
                content += "\nfrom .error_analyzer import ErrorAnalyzer\n"
                init_path.write_text(content)
                print(f"✅ Updated {module_name} __init__.py with error analyzer import")


def main():
    """Implement the missing test functionality."""
    print("🔧 Implementing missing test functionality based on Gemini feedback\n")
    
    # Implement pipeline isolation
    print("1. Implementing Pipeline Data Isolation...")
    implement_pipeline_isolation()
    
    # Implement error analysis
    print("\n2. Implementing Error Analysis...")
    implement_error_analysis()
    
    print("\n✅ All implementations complete!")
    print("\nNext steps:")
    print("1. Re-run granger_bug_hunter_v2.py to verify fixes")
    print("2. Send updated results to Gemini for validation")
    print("3. Continue iterating until all tests pass")


if __name__ == "__main__":
    main()