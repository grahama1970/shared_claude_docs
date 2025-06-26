
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Error Analysis and Quality Assessment for arangodb
"""

import re
from typing import Dict, List, Tuple

class ErrorAnalyzer:
    """Analyzes error message quality and provides recommendations."""
    
    QUALITY_CRITERIA = {
        "specificity": [
            (r"\b(error|failed|invalid|missing)\b", 1),
            (r"\b(because|due to|caused by)\b", 2),
            (r"\b(expected|got|actual|required)\b", 2),
        ],
        "actionability": [
            (r"\b(try|please|should|must|need to)\b", 2),
            (r"\b(check|verify|ensure|confirm)\b", 1),
            (r"\b(example|e\.g\.|for instance)\b", 3),
        ],
        "context": [
            (r"\b(at|in|from|during)\b", 1),
            (r"\b(line|column|position|location)\b", 2),
            (r"\b(module|function|method|class)\b", 2),
        ]
    }
    
    @classmethod
    def analyze_error_message(cls, error_msg: str) -> Dict[str, any]:
        """Analyze an error message for quality."""
        scores = {}
        total_score = 0
        
        for category, patterns in cls.QUALITY_CRITERIA.items():
            category_score = 0
            matches = []
            
            for pattern, points in patterns:
                if re.search(pattern, error_msg, re.IGNORECASE):
                    category_score += points
                    matches.append(pattern)
            
            scores[category] = {
                "score": category_score,
                "max_possible": sum(p[1] for p in patterns),
                "matches": matches
            }
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
        
        return {
            "message": error_msg,
            "total_score": total_score,
            "max_score": max_total,
            "percentage": (total_score / max_total * 100) if max_total > 0 else 0,
            "rating": quality_rating,
            "category_scores": scores,
            "recommendations": cls._generate_recommendations(scores, error_msg)
        }
    
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
        print(f"\nMessage: {result['message'][:50]}...")
        print(f"Rating: {result['rating']} ({result['percentage']:.1f}%)")
        if result['recommendations']:
            print("Recommendations:")
            for rec in result['recommendations']:
                print(f"  - {rec}")

if __name__ == "__main__":
    test_error_analyzer()
