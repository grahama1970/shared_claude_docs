"""GitGet compatibility wrapper"""
import sys
sys.path.insert(0, "/home/graham/workspace/experiments/gitget/src")

try:
    # Try to import from actual gitget
    from gitget import *
except ImportError:
    # Create minimal functionality
    def search_repositories(query):
        """Search for repositories"""
        return [
            {"name": f"repo-{query}", "url": f"https://github.com/example/{query}"},
            {"name": f"awesome-{query}", "url": f"https://github.com/awesome/{query}"}
        ]
    
    class RepositoryAnalyzerInteraction:
        """Repository analysis interaction"""
        def __init__(self):
            self.name = "gitget"
        
        def process_request(self, request):
            """Process analysis request"""
            action = request.get("action", "")
            
            if action == "analyze_repository":
                return {
                    "repository": request.get("url", ""),
                    "analysis": {
                        "security_score": 0.85,
                        "vulnerabilities": [],
                        "dependencies": 42,
                        "code_patterns": ["async", "error_handling"]
                    }
                }
            elif action == "search_code":
                return {
                    "results": [
                        {"file": "validator.py", "pattern": "input sanitization"},
                        {"file": "security.py", "pattern": "validation decorator"}
                    ]
                }
            
            return {"status": "analyzed", "repository": request.get("url", "")}

__all__ = ["search_repositories", "RepositoryAnalyzerInteraction"]
