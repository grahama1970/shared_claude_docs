#!/usr/bin/env python3
"""
Module: test_07_gitget_repo_analysis.py
Description: Test GitGet repository analysis functionality with verification
Level: 0
Modules: GitGet, Test Reporter
Expected Bugs: Clone failures, analysis errors, rate limiting
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')
sys.path.insert(0, '/home/graham/workspace/experiments/gitget/src')

from base_interaction_test import BaseInteractionTest

class GitGetRepoAnalysisTest(BaseInteractionTest):
    """Level 0: Test GitGet repository analysis"""
    
    def __init__(self):
        super().__init__(
            test_name="GitGet Repository Analysis",
            level=0,
            modules=["GitGet", "Test Reporter"]
        )
    
    def test_repo_analysis(self):
        """Test analyzing various repository types"""
        self.print_header()
        
        # Import GitGet
        try:
            from gitget import analyze_repository, get_repo_metadata
            self.record_test("gitget_import", True, {})
        except ImportError as e:
            self.add_bug(
                "GitGet module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot use GitGet functionality"
            )
            self.record_test("gitget_import", False, {"error": str(e)})
            return
        
        # Test repositories with different characteristics
        test_repos = [
            {
                "name": "Small Python project",
                "url": "https://github.com/python/cpython",
                "expected_language": "Python"
            },
            {
                "name": "JavaScript project", 
                "url": "https://github.com/nodejs/node",
                "expected_language": "JavaScript"
            },
            {
                "name": "Multi-language project",
                "url": "https://github.com/tensorflow/tensorflow",
                "expected_language": ["C++", "Python"]
            },
            {
                "name": "Invalid repository URL",
                "url": "https://github.com/invalid_user/invalid_repo_12345",
                "expected_language": None
            },
            {
                "name": "Private repository",
                "url": "https://github.com/private/private_repo",
                "expected_language": None
            },
            {
                "name": "Empty URL",
                "url": "",
                "expected_language": None
            }
        ]
        
        for repo in test_repos:
            print(f"\nTesting: {repo['name']}")
            print(f"URL: {repo['url']}")
            
            try:
                # Analyze repository
                result = analyze_repository(repo["url"])
                
                if result and isinstance(result, dict):
                    languages = result.get("languages", [])
                    files = result.get("total_files", 0)
                    size = result.get("size_mb", 0)
                    
                    print(f"✅ Analyzed: {files} files, {size:.2f}MB")
                    print(f"   Languages: {', '.join(languages[:3])}")
                    
                    self.record_test(f"analyze_{repo['name']}", True, {
                        "files": files,
                        "size_mb": size,
                        "languages": languages
                    })
                    
                    # Check for quality issues
                    if repo["expected_language"]:
                        if isinstance(repo["expected_language"], list):
                            missing = [l for l in repo["expected_language"] 
                                     if l not in languages]
                            if missing:
                                self.add_bug(
                                    "Missing expected languages",
                                    "MEDIUM",
                                    repo=repo["name"],
                                    missing=missing
                                )
                        elif repo["expected_language"] not in languages:
                            self.add_bug(
                                "Primary language not detected",
                                "MEDIUM",
                                repo=repo["name"],
                                expected=repo["expected_language"],
                                found=languages[0] if languages else None
                            )
                    
                    # Performance check
                    if size > 100 and result.get("analysis_time", 0) > 60:
                        self.add_bug(
                            "Slow repository analysis",
                            "MEDIUM",
                            repo=repo["name"],
                            time=f"{result['analysis_time']}s",
                            size=f"{size}MB"
                        )
                else:
                    if repo["name"] not in ["Invalid repository URL", "Private repository", "Empty URL"]:
                        self.add_bug(
                            "Analysis returned no result",
                            "HIGH",
                            repo=repo["name"]
                        )
                    self.record_test(f"analyze_{repo['name']}", False, {
                        "error": "No result"
                    })
                    
            except Exception as e:
                error_msg = str(e)
                print(f"💥 Exception: {error_msg[:100]}")
                
                # Check error quality
                if repo["name"] == "Empty URL" and "url" not in error_msg.lower():
                    self.add_bug(
                        "Poor error message for empty URL",
                        "LOW",
                        error=error_msg
                    )
                
                self.record_test(f"analyze_{repo['name']}", False, {
                    "error": error_msg
                })
    
    def test_metadata_extraction(self):
        """Test repository metadata extraction"""
        print("\n\nTesting Metadata Extraction...")
        
        try:
            from gitget import get_repo_metadata
            
            # Test with known repository
            test_repo = "https://github.com/python/cpython"
            
            metadata = get_repo_metadata(test_repo)
            
            if metadata:
                print(f"✅ Got metadata:")
                print(f"   Stars: {metadata.get('stars', 0)}")
                print(f"   Forks: {metadata.get('forks', 0)}")
                print(f"   Issues: {metadata.get('open_issues', 0)}")
                
                self.record_test("metadata_extraction", True, metadata)
                
                # Check for missing fields
                required_fields = ["name", "description", "stars", "forks", 
                                 "created_at", "updated_at", "language"]
                missing = [f for f in required_fields if f not in metadata]
                
                if missing:
                    self.add_bug(
                        "Missing metadata fields",
                        "MEDIUM",
                        missing_fields=missing
                    )
            else:
                self.add_bug(
                    "No metadata returned",
                    "HIGH",
                    repo=test_repo
                )
                self.record_test("metadata_extraction", False, {})
                
        except ImportError:
            print("❌ Metadata extraction not available")
            self.record_test("metadata_import", False, {"error": "Not implemented"})
        except Exception as e:
            self.add_bug(
                "Exception in metadata extraction",
                "HIGH",
                error=str(e)
            )
            self.record_test("metadata_extraction", False, {"error": str(e)})
    
    def test_code_quality_analysis(self):
        """Test code quality analysis features"""
        print("\n\nTesting Code Quality Analysis...")
        
        try:
            from gitget import analyze_code_quality
            
            # Test with different quality scenarios
            quality_tests = [
                {
                    "name": "High quality code",
                    "url": "https://github.com/python/cpython",
                    "expected_score": "high"
                },
                {
                    "name": "Legacy codebase",
                    "url": "https://github.com/old/legacy_project",
                    "expected_score": "medium"
                }
            ]
            
            for test in quality_tests:
                print(f"\nAnalyzing: {test['name']}")
                
                try:
                    quality = analyze_code_quality(test["url"])
                    
                    if quality:
                        score = quality.get("overall_score", 0)
                        issues = quality.get("issues", [])
                        
                        print(f"✅ Quality score: {score}/100")
                        print(f"   Issues found: {len(issues)}")
                        
                        self.record_test(f"quality_{test['name']}", True, {
                            "score": score,
                            "issue_count": len(issues)
                        })
                        
                        # Check for unrealistic scores
                        if score == 100:
                            self.add_bug(
                                "Perfect quality score suspicious",
                                "LOW",
                                repo=test["name"]
                            )
                        elif score == 0:
                            self.add_bug(
                                "Zero quality score suspicious",
                                "MEDIUM",
                                repo=test["name"]
                            )
                    else:
                        self.record_test(f"quality_{test['name']}", False, {
                            "error": "No result"
                        })
                        
                except Exception as e:
                    self.add_bug(
                        f"Quality analysis failed for {test['name']}",
                        "MEDIUM",
                        error=str(e)
                    )
                    
        except ImportError:
            print("❌ Code quality analysis not available")
            self.record_test("quality_import", False, {"error": "Not implemented"})
    
    def run_tests(self):
        """Run all tests"""
        self.test_repo_analysis()
        self.test_metadata_extraction()
        self.test_code_quality_analysis()
        return self.generate_report()


def main():
    """Run the test"""
    tester = GitGetRepoAnalysisTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)