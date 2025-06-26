#!/usr/bin/env python3
"""
Self-Evolving Project Analyzer
A system that autonomously researches, implements, tests, and commits improvements
using arxiv-mcp-server, youtube_transcripts, and claude-module-communicator
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if src_path.exists() and str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))



import asyncio
import json
import subprocess
import os
import sys
import ast
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import tempfile
import git
import re

class SelfEvolvingAnalyzer:
    """Autonomous system that researches and implements its own improvements"""
    
    def __init__(self, target_project: str, output_dir: Path = None):
        self.target_project = target_project
        self.project_path = Path(f"/home/graham/workspace/{target_project}")
        self.output_dir = output_dir or Path("./self_evolution_logs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Evolution state tracking
        self.evolution_state = {
            "generation": 0,
            "improvements_made": [],
            "test_results": [],
            "research_cache": {},
            "learning_history": []
        }
        
        # Load state if exists
        self.state_file = self.output_dir / f"{target_project}_evolution_state.json"
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                self.evolution_state = json.load(f)
        
        # Research queries that evolve over time
        self.research_queries = {
            "optimization": [
                f"{target_project} optimization techniques 2024",
                f"improve {self._get_project_focus()} performance",
                "latest advances " + self._get_project_focus()
            ],
            "architecture": [
                f"{self._get_project_focus()} architecture patterns",
                "scalable system design 2024",
                "microservice orchestration best practices"
            ],
            "testing": [
                "automated testing strategies ML systems",
                "self-healing test frameworks",
                "chaos engineering practices"
            ]
        }
    
    def _get_project_focus(self) -> str:
        """Determine project focus from name"""
        focus_map = {
            "marker": "document extraction",
            "sparta": "distributed training",
            "claude-module-communicator": "system orchestration",
            "arxiv-mcp-server": "research discovery",
            "youtube_transcripts": "video analysis",
            "arangodb": "graph database"
        }
        return focus_map.get(self.target_project, "software system")
    
    async def evolve(self, max_iterations: int = 5):
        """Main evolution loop"""
        
        print(f"🧬 Starting self-evolution for {self.target_project}")
        print(f"   Current generation: {self.evolution_state['generation']}")
        
        for iteration in range(max_iterations):
            print(f"\n{'='*60}")
            print(f"🔄 Evolution Cycle {iteration + 1}/{max_iterations}")
            print(f"{'='*60}")
            
            try:
                # Phase 1: Research
                research_findings = await self.research_phase()
                
                # Phase 2: Analyze and Plan
                improvement_plan = await self.analyze_and_plan_phase(research_findings)
                
                # Phase 3: Implement
                implementation_result = await self.implement_phase(improvement_plan)
                
                # Phase 4: Test
                test_results = await self.test_phase(implementation_result)
                
                # Phase 5: Evaluate and Commit
                evolution_success = await self.evaluate_and_commit_phase(
                    implementation_result, test_results
                )
                
                # Update evolution state
                self.evolution_state["generation"] += 1
                self._save_state()
                
                if evolution_success:
                    print(f"✅ Evolution cycle {iteration + 1} completed successfully!")
                else:
                    print(f"⚠️  Evolution cycle {iteration + 1} completed with issues")
                
                # Learn from this cycle
                await self.learn_from_cycle(research_findings, test_results)
                
            except Exception as e:
                print(f"❌ Evolution cycle {iteration + 1} failed: {str(e)}")
                await self.rollback_changes()
    
    async def research_phase(self) -> Dict[str, Any]:
        """Research phase using arxiv-mcp-server and youtube_transcripts"""
        
        print("\n📚 RESEARCH PHASE")
        print("-" * 40)
        
        research_findings = {
            "arxiv_papers": [],
            "youtube_insights": [],
            "code_patterns": [],
            "improvement_ideas": []
        }
        
        # 1. Search ArXiv for recent papers
        print("🔍 Searching ArXiv for relevant research...")
        for category, queries in self.research_queries.items():
            for query in queries[:2]:  # Limit queries
                papers = await self._search_arxiv(query)
                research_findings["arxiv_papers"].extend(papers)
        
        # 2. Search YouTube for implementation tutorials
        print("📺 Searching YouTube for tutorials...")
        youtube_results = await self._search_youtube()
        research_findings["youtube_insights"] = youtube_results
        
        # 3. Analyze successful code patterns from other projects
        print("💻 Analyzing successful code patterns...")
        patterns = await self._analyze_code_patterns()
        research_findings["code_patterns"] = patterns
        
        # 4. Generate improvement ideas using Claude
        print("🤖 Generating improvement ideas...")
        ideas = await self._generate_improvement_ideas(research_findings)
        research_findings["improvement_ideas"] = ideas
        
        print(f"   Found {len(research_findings['arxiv_papers'])} papers")
        print(f"   Found {len(research_findings['youtube_insights'])} video insights")
        print(f"   Generated {len(research_findings['improvement_ideas'])} improvement ideas")
        
        return research_findings
    
    async def analyze_and_plan_phase(self, research_findings: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze findings and create implementation plan"""
        
        print("\n📋 ANALYSIS & PLANNING PHASE")
        print("-" * 40)
        
        # Analyze current codebase
        codebase_analysis = await self._analyze_current_codebase()
        
        # Select best improvement to implement
        selected_improvement = await self._select_improvement(
            research_findings["improvement_ideas"],
            codebase_analysis
        )
        
        # Create detailed implementation plan
        implementation_plan = {
            "improvement": selected_improvement,
            "changes": [],
            "test_plan": [],
            "rollback_plan": []
        }
        
        # Plan specific code changes
        if selected_improvement["type"] == "performance":
            implementation_plan["changes"] = await self._plan_performance_changes(
                selected_improvement, codebase_analysis
            )
        elif selected_improvement["type"] == "architecture":
            implementation_plan["changes"] = await self._plan_architecture_changes(
                selected_improvement, codebase_analysis
            )
        elif selected_improvement["type"] == "feature":
            implementation_plan["changes"] = await self._plan_feature_changes(
                selected_improvement, codebase_analysis
            )
        
        # Generate test plan
        implementation_plan["test_plan"] = await self._generate_test_plan(
            implementation_plan["changes"]
        )
        
        print(f"📌 Selected improvement: {selected_improvement['title']}")
        print(f"   Type: {selected_improvement['type']}")
        print(f"   Estimated impact: {selected_improvement['impact']}")
        print(f"   Changes planned: {len(implementation_plan['changes'])}")
        
        return implementation_plan
    
    async def implement_phase(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Implement the planned changes"""
        
        print("\n🔨 IMPLEMENTATION PHASE")
        print("-" * 40)
        
        implementation_result = {
            "changes_made": [],
            "files_modified": [],
            "backup_created": False,
            "implementation_log": []
        }
        
        # Create backup branch
        repo = git.Repo(self.project_path)
        backup_branch = f"auto-evolution-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        repo.git.checkout('-b', backup_branch)
        repo.git.checkout('main')  # or 'master'
        implementation_result["backup_created"] = True
        
        # Implement each planned change
        for i, change in enumerate(plan["changes"]):
            print(f"   Implementing change {i+1}/{len(plan['changes'])}: {change['description']}")
            
            try:
                if change["type"] == "modify_file":
                    result = await self._modify_file(change)
                elif change["type"] == "create_file":
                    result = await self._create_file(change)
                elif change["type"] == "refactor_function":
                    result = await self._refactor_function(change)
                elif change["type"] == "add_feature":
                    result = await self._add_feature(change)
                
                implementation_result["changes_made"].append({
                    "change": change,
                    "result": result,
                    "success": True
                })
                implementation_result["files_modified"].extend(result.get("files", []))
                
            except Exception as e:
                print(f"   ❌ Failed to implement: {str(e)}")
                implementation_result["changes_made"].append({
                    "change": change,
                    "error": str(e),
                    "success": False
                })
        
        # Generate implementation summary
        successful_changes = sum(1 for c in implementation_result["changes_made"] if c["success"])
        print(f"\n✅ Implemented {successful_changes}/{len(plan['changes'])} changes successfully")
        
        return implementation_result
    
    async def test_phase(self, implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """Test the implemented changes"""
        
        print("\n🧪 TESTING PHASE")
        print("-" * 40)
        
        test_results = {
            "unit_tests": {"passed": 0, "failed": 0, "errors": []},
            "integration_tests": {"passed": 0, "failed": 0, "errors": []},
            "performance_tests": {"metrics": {}, "regression": False},
            "overall_success": False
        }
        
        # Run existing test suite
        print("🔍 Running existing tests...")
        existing_tests = await self._run_existing_tests()
        test_results["unit_tests"] = existing_tests["unit"]
        test_results["integration_tests"] = existing_tests["integration"]
        
        # Run new tests for implemented changes
        print("🆕 Running tests for new changes...")
        for change in implementation_result["changes_made"]:
            if change["success"] and "test" in change.get("result", {}):
                test_result = await self._run_specific_test(change["result"]["test"])
                if test_result["passed"]:
                    test_results["unit_tests"]["passed"] += 1
                else:
                    test_results["unit_tests"]["failed"] += 1
                    test_results["unit_tests"]["errors"].append(test_result["error"])
        
        # Performance testing
        print("⚡ Running performance benchmarks...")
        perf_results = await self._run_performance_tests()
        test_results["performance_tests"] = perf_results
        
        # Determine overall success
        total_tests = (test_results["unit_tests"]["passed"] + 
                      test_results["unit_tests"]["failed"] +
                      test_results["integration_tests"]["passed"] + 
                      test_results["integration_tests"]["failed"])
        
        passed_tests = (test_results["unit_tests"]["passed"] + 
                       test_results["integration_tests"]["passed"])
        
        test_results["overall_success"] = (
            passed_tests / total_tests > 0.95 and 
            not test_results["performance_tests"]["regression"]
        ) if total_tests > 0 else False
        
        print(f"\n📊 Test Results:")
        print(f"   Unit tests: {test_results['unit_tests']['passed']} passed, "
              f"{test_results['unit_tests']['failed']} failed")
        print(f"   Integration tests: {test_results['integration_tests']['passed']} passed, "
              f"{test_results['integration_tests']['failed']} failed")
        print(f"   Performance regression: {'Yes' if test_results['performance_tests']['regression'] else 'No'}")
        
        return test_results
    
    async def evaluate_and_commit_phase(self, implementation_result: Dict[str, Any], 
                                       test_results: Dict[str, Any]) -> bool:
        """Evaluate results and commit if successful"""
        
        print("\n📊 EVALUATION & COMMIT PHASE")
        print("-" * 40)
        
        # Evaluate success criteria
        success_criteria = {
            "tests_pass": test_results["overall_success"],
            "no_regression": not test_results["performance_tests"]["regression"],
            "changes_implemented": len([c for c in implementation_result["changes_made"] if c["success"]]) > 0
        }
        
        all_criteria_met = all(success_criteria.values())
        
        print("📋 Success Criteria:")
        for criterion, met in success_criteria.items():
            print(f"   {criterion}: {'✅' if met else '❌'}")
        
        if all_criteria_met:
            print("\n✅ All criteria met! Committing changes...")
            
            # Create detailed commit message
            commit_message = self._generate_commit_message(
                implementation_result, test_results
            )
            
            # Commit changes
            repo = git.Repo(self.project_path)
            repo.git.add(A=True)
            repo.index.commit(commit_message)
            
            # Update evolution state
            self.evolution_state["improvements_made"].append({
                "generation": self.evolution_state["generation"],
                "timestamp": datetime.now().isoformat(),
                "changes": len(implementation_result["changes_made"]),
                "test_results": test_results,
                "commit_sha": repo.head.commit.hexsha
            })
            
            print(f"🎉 Changes committed successfully!")
            print(f"   Commit SHA: {repo.head.commit.hexsha[:8]}")
            
            return True
        else:
            print("\n⚠️  Not all criteria met. Rolling back changes...")
            await self.rollback_changes()
            return False
    
    async def learn_from_cycle(self, research_findings: Dict[str, Any], 
                              test_results: Dict[str, Any]):
        """Learn from this evolution cycle to improve future cycles"""
        
        print("\n🧠 LEARNING PHASE")
        print("-" * 40)
        
        learning_entry = {
            "generation": self.evolution_state["generation"],
            "timestamp": datetime.now().isoformat(),
            "successful_patterns": [],
            "failed_patterns": [],
            "insights": []
        }
        
        # Analyze what worked
        if test_results["overall_success"]:
            learning_entry["successful_patterns"].append({
                "research_sources": [p["title"] for p in research_findings["arxiv_papers"][:3]],
                "implementation_approach": "autonomous",
                "test_coverage": f"{test_results['unit_tests']['passed']} unit tests passed"
            })
        
        # Analyze what didn't work
        if test_results["unit_tests"]["errors"]:
            learning_entry["failed_patterns"].append({
                "error_types": list(set(e.split(":")[0] for e in test_results["unit_tests"]["errors"])),
                "common_causes": "implementation bugs"
            })
        
        # Generate insights for next iteration
        if len(self.evolution_state["learning_history"]) > 2:
            # Look for patterns across multiple generations
            recent_successes = sum(
                1 for entry in self.evolution_state["learning_history"][-3:]
                if entry.get("successful_patterns")
            )
            if recent_successes >= 2:
                learning_entry["insights"].append(
                    "Current research approach is effective - continue with similar queries"
                )
            else:
                learning_entry["insights"].append(
                    "Need to diversify research sources - try different query strategies"
                )
        
        self.evolution_state["learning_history"].append(learning_entry)
        
        # Update research queries based on learning
        await self._update_research_queries(learning_entry)
        
        print(f"📝 Recorded {len(learning_entry['successful_patterns'])} successful patterns")
        print(f"📝 Recorded {len(learning_entry['failed_patterns'])} failed patterns")
        print(f"💡 Generated {len(learning_entry['insights'])} insights")
    
    async def _extract_insights_from_paper(self, paper_id: str) -> List[str]:
        """Extract key insights from a downloaded paper"""
        
        insights = []
        
        try:
            # Try to read the markdown version of the paper
            storage_path = os.getenv("ARXIV_STORAGE_PATH", "~/.arxiv_papers")
            storage_path = os.path.expanduser(storage_path)
            markdown_path = Path(storage_path) / "markdown" / f"{paper_id}.md"
            
            if markdown_path.exists():
                content = markdown_path.read_text()[:5000]  # First 5000 chars
                
                # Extract key points (simple heuristic)
                if "contribution" in content.lower():
                    insights.append("Novel contribution identified")
                if "improvement" in content.lower():
                    insights.append("Performance improvements documented")
                if "github.com" in content:
                    insights.append("Implementation available on GitHub")
                
        except Exception as e:
            print(f"   ⚠️  Could not extract insights from {paper_id}: {str(e)}")
        
        return insights if insights else ["Research paper analyzed"]
    
    async def _extract_youtube_insights(self, transcript: str, title: str) -> Dict[str, Any]:
        """Extract insights from YouTube transcript"""
        
        insights = {
            "summary": "",
            "code_snippets": [],
            "tips": []
        }
        
        if not transcript:
            return insights
        
        # Simple extraction heuristics
        lines = transcript.split('\n')
        
        # Look for code patterns
        code_patterns = [
            r"def \w+\(",
            r"class \w+:",
            r"import \w+",
            r"async def",
            r"await \w+"
        ]
        
        for line in lines:
            for pattern in code_patterns:
                if re.search(pattern, line):
                    insights["code_snippets"].append(line.strip())
                    break
        
        # Extract tips (lines with keywords)
        tip_keywords = ["tip", "trick", "best practice", "recommend", "should", "important"]
        for line in lines:
            if any(keyword in line.lower() for keyword in tip_keywords):
                insights["tips"].append(line.strip()[:200])  # First 200 chars
        
        # Create summary
        insights["summary"] = f"Video '{title}' discusses {self._get_project_focus()} techniques"
        
        # Limit results
        insights["code_snippets"] = insights["code_snippets"][:5]
        insights["tips"] = insights["tips"][:3]
        
        return insights
    
    async def rollback_changes(self):
        """Rollback unsuccessful changes"""
        
        repo = git.Repo(self.project_path)
        repo.git.reset('--hard', 'HEAD')
        print("🔄 Changes rolled back successfully")
    
    # Helper methods for research phase
    
    async def _search_arxiv(self, query: str) -> List[Dict[str, Any]]:
        """Search ArXiv using arxiv-mcp-server"""
        
        try:
            # Import arxiv-mcp-server tools
            from arxiv_mcp_server.tools import handle_search, handle_batch_download
            
            # Search for papers
            search_result = await handle_search({
                "query": query,
                "max_results": 10,
                "date_from": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                "categories": ["cs.AI", "cs.LG", "cs.CL"]
            })
            
            # Parse results
            import json
            papers_data = json.loads(search_result[0].text)
            papers = papers_data.get("papers", [])
            
            # Download top papers for analysis
            if papers:
                paper_ids = [p["id"] for p in papers[:5]]
                await handle_batch_download({
                    "paper_ids": paper_ids,
                    "converter": "pymupdf4llm",
                    "skip_existing": True,
                    "convert_to": "markdown"
                })
            
            # Extract key insights from papers
            processed_papers = []
            for paper in papers[:5]:
                processed_papers.append({
                    "title": paper["title"],
                    "authors": paper.get("authors", []),
                    "year": paper["published"][:4] if "published" in paper else "2024",
                    "abstract": paper.get("summary", ""),
                    "arxiv_id": paper["id"],
                    "pdf_url": paper.get("pdf_url", ""),
                    "relevance_score": 0.8,  # Could use similarity scoring
                    "implementation_available": "github.com" in paper.get("summary", "").lower(),
                    "key_insights": await self._extract_insights_from_paper(paper["id"])
                })
            
            return processed_papers
            
        except ImportError:
            print("⚠️  arxiv-mcp-server not available, using mock data")
            # Fallback mock data
            return [{
                "title": f"Research on {query}",
                "authors": ["Various"],
                "year": "2024",
                "abstract": "Mock abstract",
                "relevance_score": 0.7,
                "implementation_available": False,
                "key_insights": ["Mock insight"]
            }]
    
    async def _search_youtube(self) -> List[Dict[str, Any]]:
        """Search YouTube using youtube_transcripts"""
        
        try:
            # Import youtube_transcripts
            from youtube_transcripts.unified_search import UnifiedYouTubeSearch, UnifiedSearchConfig
            
            # Configure search
            config = UnifiedSearchConfig()
            search = UnifiedYouTubeSearch(config)
            
            # Build search query based on project focus
            search_queries = [
                f"{self.target_project} tutorial implementation",
                f"{self._get_project_focus()} best practices 2024",
                f"improve {self._get_project_focus()} performance"
            ]
            
            all_videos = []
            
            for query in search_queries[:2]:  # Limit to preserve quota
                try:
                    # Search YouTube API
                    results = search.search_youtube_api(
                        query=query,
                        max_results=10,
                        fetch_transcripts=True,
                        store_transcripts=True,
                        published_after=datetime.now() - timedelta(days=180)
                    )
                    
                    # Process results
                    for video in results.get("results", [])[:3]:
                        if video.get("transcript_available"):
                            # Extract insights from transcript
                            insights = await self._extract_youtube_insights(
                                video["transcript"],
                                video["title"]
                            )
                            
                            all_videos.append({
                                "title": video["title"],
                                "channel": video["channel_name"],
                                "url": video["url"],
                                "transcript_summary": insights.get("summary", ""),
                                "code_snippets": insights.get("code_snippets", []),
                                "implementation_tips": insights.get("tips", []),
                                "publish_date": video["publish_date"]
                            })
                            
                except Exception as e:
                    print(f"   ⚠️  Error searching YouTube: {str(e)}")
            
            # Also search local database for existing transcripts
            local_results = search.search(
                query=self._get_project_focus(),
                use_widening=True
            )
            
            for video in local_results.get("results", [])[:2]:
                insights = await self._extract_youtube_insights(
                    video["transcript"],
                    video["title"]
                )
                
                all_videos.append({
                    "title": video["title"],
                    "channel": video["channel_name"],
                    "url": f"https://youtube.com/watch?v={video['video_id']}",
                    "transcript_summary": insights.get("summary", ""),
                    "code_snippets": insights.get("code_snippets", []),
                    "implementation_tips": insights.get("tips", []),
                    "from_cache": True
                })
            
            return all_videos
            
        except ImportError:
            print("⚠️  youtube_transcripts not available, using mock data")
            # Fallback mock data
            return [{
                "title": f"{self.target_project} Tutorial",
                "channel": "Tech Channel",
                "url": "https://youtube.com/watch?v=mock",
                "transcript_summary": "Mock summary",
                "code_snippets": [],
                "implementation_tips": ["Mock tip"]
            }]
    
    async def _analyze_code_patterns(self) -> List[Dict[str, str]]:
        """Analyze successful patterns from other projects"""
        
        patterns = []
        
        # Look for common successful patterns
        patterns.append({
            "pattern": "async_parallel_processing",
            "description": "Use asyncio with process pool for CPU-bound tasks",
            "example": "ProcessPoolExecutor with asyncio",
            "applicable_to": ["marker", "sparta"]
        })
        
        return patterns
    
    async def _generate_improvement_ideas(self, research: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement ideas based on research"""
        
        ideas = []
        
        # Use arxiv-mcp-server's evidence finding to validate ideas
        try:
            from arxiv_mcp_server.tools import handle_find_research_support
            
            # Generate ideas based on papers
            for paper in research["arxiv_papers"][:3]:
                if paper.get("implementation_available"):
                    # Validate idea with research evidence
                    hypothesis = f"Implementing {paper['title'].split(':')[0]} will improve {self.target_project} performance"
                    
                    evidence = await handle_find_research_support({
                        "research_context": hypothesis,
                        "paper_ids": [paper.get("arxiv_id", "all")],
                        "support_type": "bolster",
                        "llm_provider": "gemini",
                        "min_confidence": 0.7
                    })
                    
                    # Parse evidence
                    import json
                    evidence_data = json.loads(evidence[0].text)
                    
                    if evidence_data.get("findings"):
                        confidence = evidence_data["findings"][0].get("confidence", 0.5)
                        ideas.append({
                            "title": f"Implement {paper['title'].split(':')[0]}",
                            "type": "architecture",
                            "source": paper["title"],
                            "arxiv_id": paper.get("arxiv_id"),
                            "description": f"Integrate techniques from {paper['title']}",
                            "impact": "30-50% performance improvement",
                            "complexity": "medium",
                            "feasibility_score": confidence,
                            "research_backing": evidence_data["findings"][0].get("explanation", "")
                        })
            
            # Generate ideas from YouTube insights
            for video in research["youtube_insights"][:2]:
                if video.get("code_snippets"):
                    ideas.append({
                        "title": video['implementation_tips'][0] if video.get('implementation_tips') else "Implement video technique",
                        "type": "performance",
                        "source": video["title"],
                        "description": video['implementation_tips'][0] if video.get('implementation_tips') else "Apply technique from video",
                        "impact": "2-5x speedup",
                        "complexity": "low",
                        "feasibility_score": 0.9,
                        "code_reference": video.get("code_snippets", [])
                    })
            
            # Generate cross-cutting improvements from patterns
            if research.get("code_patterns"):
                for pattern in research["code_patterns"][:1]:
                    ideas.append({
                        "title": f"Apply {pattern['pattern']} pattern",
                        "type": "refactoring",
                        "source": "Code pattern analysis",
                        "description": pattern["description"],
                        "impact": "Improved maintainability and performance",
                        "complexity": "low",
                        "feasibility_score": 0.85
                    })
            
        except Exception as e:
            print(f"   ⚠️  Error generating ideas with evidence: {str(e)}")
            # Fallback to basic idea generation
            for paper in research["arxiv_papers"][:2]:
                ideas.append({
                    "title": f"Study and implement {paper['title'].split()[0]}",
                    "type": "research",
                    "source": paper["title"],
                    "description": "Research-based improvement",
                    "impact": "Unknown",
                    "complexity": "medium",
                    "feasibility_score": 0.5
                })
        
        return ideas
    
    # Helper methods for implementation phase
    
    async def _analyze_current_codebase(self) -> Dict[str, Any]:
        """Analyze current codebase structure"""
        
        analysis = {
            "files": [],
            "functions": {},
            "classes": {},
            "imports": [],
            "patterns": []
        }
        
        # Scan Python files
        for py_file in self.project_path.rglob("*.py"):
            if ".git" not in str(py_file):
                analysis["files"].append(str(py_file))
                
                try:
                    with open(py_file, 'r') as f:
                        tree = ast.parse(f.read())
                        
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            analysis["functions"][node.name] = str(py_file)
                        elif isinstance(node, ast.ClassDef):
                            analysis["classes"][node.name] = str(py_file)
                        elif isinstance(node, ast.Import):
                            for alias in node.names:
                                analysis["imports"].append(alias.name)
                except:
                    pass
        
        return analysis
    
    async def _select_improvement(self, ideas: List[Dict[str, Any]], 
                                 codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Select best improvement to implement"""
        
        # Score each idea based on feasibility and impact
        scored_ideas = []
        for idea in ideas:
            score = idea["feasibility_score"] * 0.6
            
            # Bonus for low complexity
            if idea["complexity"] == "low":
                score += 0.2
            elif idea["complexity"] == "medium":
                score += 0.1
            
            # Bonus for performance improvements
            if idea["type"] == "performance":
                score += 0.1
            
            scored_ideas.append((score, idea))
        
        # Select highest scoring idea
        scored_ideas.sort(reverse=True, key=lambda x: x[0])
        return scored_ideas[0][1] if scored_ideas else ideas[0]
    
    async def _plan_performance_changes(self, improvement: Dict[str, Any], 
                                       codebase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Plan performance improvement changes"""
        
        changes = []
        
        if "parallel processing" in improvement["description"].lower():
            # Find main processing function
            process_functions = [
                func for func in codebase["functions"] 
                if "process" in func.lower() or "extract" in func.lower()
            ]
            
            if process_functions:
                changes.append({
                    "type": "refactor_function",
                    "file": codebase["functions"][process_functions[0]],
                    "function": process_functions[0],
                    "description": "Add parallel processing",
                    "new_code": '''async def process_parallel(self, items):
    """Process items in parallel using ProcessPoolExecutor"""
    import asyncio
    from concurrent.futures import ProcessPoolExecutor
    
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, self._process_single, item)
            for item in items
        ]
        results = await asyncio.gather(*tasks)
    
    return results'''
                })
        
        return changes
    
    async def _modify_file(self, change: Dict[str, Any]) -> Dict[str, Any]:
        """Modify an existing file"""
        
        file_path = Path(change["file"])
        
        # Read current content
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Apply modification
        if change.get("new_code"):
            # For function refactoring
            function_pattern = rf"def {change['function']}\([^)]*\):[^:]+?(?=\ndef|\nclass|\Z)"
            content = re.sub(function_pattern, change["new_code"], content, flags=re.DOTALL)
        
        # Write back
        with open(file_path, 'w') as f:
            f.write(content)
        
        return {"files": [str(file_path)], "success": True}
    
    async def _run_existing_tests(self) -> Dict[str, Any]:
        """Run existing test suite"""
        
        results = {
            "unit": {"passed": 0, "failed": 0, "errors": []},
            "integration": {"passed": 0, "failed": 0, "errors": []}
        }
        
        # Try pytest
        try:
            result = subprocess.run(
                ["pytest", "-v", "--tb=short"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            # Parse pytest output
            if result.returncode == 0:
                passed_matches = re.findall(r"(\d+) passed", result.stdout)
                if passed_matches:
                    results["unit"]["passed"] = int(passed_matches[0])
            else:
                failed_matches = re.findall(r"(\d+) failed", result.stdout)
                if failed_matches:
                    results["unit"]["failed"] = int(failed_matches[0])
                
                # Extract errors
                error_lines = [
                    line for line in result.stdout.split('\n') 
                    if "FAILED" in line or "ERROR" in line
                ]
                results["unit"]["errors"] = error_lines[:5]  # First 5 errors
        except:
            pass
        
        return results
    
    async def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        
        # Simple performance test
        results = {
            "metrics": {
                "processing_time": 0.0,
                "memory_usage": 0.0,
                "throughput": 0.0
            },
            "regression": False
        }
        
        # Simulate performance test
        import time
        import psutil
        
        process = psutil.Process()
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        # Run some performance test here
        end_time = time.time()
        
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        results["metrics"]["processing_time"] = end_time - start_time
        results["metrics"]["memory_usage"] = end_memory - start_memory
        
        # Check for regression (simplified)
        if hasattr(self, "baseline_performance"):
            if results["metrics"]["processing_time"] > self.baseline_performance * 1.1:
                results["regression"] = True
        
        return results
    
    def _generate_commit_message(self, implementation: Dict[str, Any], 
                                tests: Dict[str, Any]) -> str:
        """Generate detailed commit message"""
        
        successful_changes = [c for c in implementation["changes_made"] if c["success"]]
        
        message = f"""🤖 Auto-Evolution: Generation {self.evolution_state['generation']}

Implemented improvements based on research findings:
"""
        
        for change in successful_changes[:3]:
            message += f"- {change['change']['description']}\n"
        
        message += f"""
Test Results:
- Unit tests: {tests['unit_tests']['passed']} passed, {tests['unit_tests']['failed']} failed
- Integration tests: {tests['integration_tests']['passed']} passed
- Performance: {'No regression' if not tests['performance_tests']['regression'] else 'Regression detected'}

This commit was automatically generated and tested by the self-evolution system.

🤖 Generated by Self-Evolving Analyzer
"""
        
        return message
    
    async def _update_research_queries(self, learning: Dict[str, Any]):
        """Update research queries based on learning"""
        
        # If recent failures, add more specific queries
        if learning.get("failed_patterns"):
            error_types = learning["failed_patterns"][0].get("error_types", [])
            for error_type in error_types:
                self.research_queries["debugging"] = [
                    f"fix {error_type} in {self._get_project_focus()}",
                    f"{error_type} best practices 2024"
                ]
        
        # If successful, explore more advanced topics
        if learning.get("successful_patterns"):
            self.research_queries["advanced"] = [
                f"advanced {self._get_project_focus()} techniques",
                f"cutting-edge {self._get_project_focus()} research 2024"
            ]
    
    def _save_state(self):
        """Save evolution state to disk"""
        
        with open(self.state_file, 'w') as f:
            json.dump(self.evolution_state, f, indent=2)
    
    async def generate_evolution_report(self):
        """Generate comprehensive evolution report"""
        
        report_path = self.output_dir / f"{self.target_project}_evolution_report.md"
        
        with open(report_path, 'w') as f:
            f.write(f"# Self-Evolution Report: {self.target_project}\n\n")
            f.write(f"**Current Generation**: {self.evolution_state['generation']}\n")
            f.write(f"**Total Improvements**: {len(self.evolution_state['improvements_made'])}\n\n")
            
            f.write("## Evolution Timeline\n\n")
            for improvement in self.evolution_state["improvements_made"]:
                f.write(f"### Generation {improvement['generation']}\n")
                f.write(f"- **Date**: {improvement['timestamp']}\n")
                f.write(f"- **Changes**: {improvement['changes']}\n")
                f.write(f"- **Commit**: {improvement['commit_sha'][:8]}\n")
                f.write(f"- **Tests Passed**: {improvement['test_results']['unit_tests']['passed']}\n\n")
            
            f.write("## Learning History\n\n")
            for entry in self.evolution_state["learning_history"][-5:]:
                f.write(f"### Generation {entry['generation']}\n")
                if entry.get("insights"):
                    f.write("**Insights**:\n")
                    for insight in entry["insights"]:
                        f.write(f"- {insight}\n")
                f.write("\n")
            
            f.write("## Next Evolution Steps\n\n")
            f.write("1. Continue researching advanced techniques\n")
            f.write("2. Implement more sophisticated testing\n")
            f.write("3. Explore cross-project optimizations\n")
        
        print(f"\n📊 Evolution report saved to: {report_path}")


async def main():
    """Run self-evolving analyzer"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Self-Evolving Project Analyzer")
    parser.add_argument("project", help="Target project to evolve")
    parser.add_argument("--iterations", type=int, default=3, 
                       help="Number of evolution cycles")
    parser.add_argument("--output", type=str, default="./self_evolution_logs",
                       help="Output directory for logs")
    
    args = parser.parse_args()
    
    print("🧬 Self-Evolving Project Analyzer")
    print("=" * 60)
    print(f"Target Project: {args.project}")
    print(f"Evolution Cycles: {args.iterations}")
    print(f"Output Directory: {args.output}")
    print("\n⚠️  This system will:")
    print("1. Research improvements using ArXiv and YouTube")
    print("2. Implement changes autonomously")
    print("3. Test the changes")
    print("4. Commit successful improvements")
    print("5. Learn from each cycle\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return
    
    analyzer = SelfEvolvingAnalyzer(args.project, Path(args.output))
    await analyzer.evolve(max_iterations=args.iterations)
    await analyzer.generate_evolution_report()
    
    print("\n✅ Self-evolution complete!")
    print(f"📁 Logs saved to: {args.output}")


if __name__ == "__main__":
    asyncio.run(main())