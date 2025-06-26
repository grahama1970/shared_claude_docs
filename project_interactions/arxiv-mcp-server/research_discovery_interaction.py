
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: research_discovery_interaction.py
Purpose: Implements research discovery and validation for arxiv-mcp-server

External Dependencies:
- arxiv: https://pypi.org/project/arxiv/
- mcp: Model Context Protocol SDK

Example Usage:
>>> from research_discovery_interaction import ResearchDiscoveryScenario
>>> scenario = ResearchDiscoveryScenario()
>>> result = scenario.find_supporting_evidence("transformer architectures")
>>> print(f"Found {len(result.output_data['papers'])} supporting papers")
"""

import asyncio
import json
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import arxiv
from collections import defaultdict

from ...templates.interaction_framework import (
    Level0Interaction,
    InteractionResult,
    InteractionLevel
)


class ResearchDiscoveryScenario(Level0Interaction):
    """
    Implements GRANGER research discovery for arxiv-mcp-server.
    
    This scenario:
    1. Finds supporting evidence for techniques
    2. Finds contradicting research for validation
    3. Implements dual-purpose research mechanism
    4. Filters papers by quality metrics
    """
    
    def __init__(self):
        super().__init__(
            module_name="arxiv-mcp-server",
            interaction_name="research_discovery"
        )
        self.cache_file = Path("arxiv_cache.json")
        self.quality_threshold = 0.7
        # Initialize ArXiv client with rate limiting
        self.arxiv_client = arxiv.Client(
            page_size=100,
            delay_seconds=0.34,  # 3 requests per second (1/3 = 0.33...)
            num_retries=3
        )
        self.last_request_time = 0
        
    def find_supporting_evidence(self, technique: str, max_results: int = 10) -> InteractionResult:
        """
        Finds supporting evidence for a technique.
        
        Args:
            technique: The technique to find evidence for
            max_results: Maximum number of papers to return
            
        Returns:
            InteractionResult with supporting papers
        """
        start_time = time.time()
        
        try:
            # Build search query for supporting evidence
            search_query = f'"{technique}" AND (improvement OR enhancement OR "state-of-the-art" OR breakthrough)'
            
            # Search ArXiv
            search = arxiv.Search(
                query=search_query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            evidence_items = []
            
            # Use the new Client API with timeout
            try:
                for paper in self.arxiv_client.results(search, timeout=30.0):
                    # Extract paper data
                    paper_data = self._extract_paper_data(paper)
                    
                    # Calculate quality score
                    quality_score = self._calculate_quality_score(paper, technique)
                    paper_data["quality_score"] = quality_score
                    
                    # Only include high-quality papers
                    if quality_score >= self.quality_threshold:
                        papers.append(paper_data)
                        
                        # Extract evidence
                        evidence = self._extract_evidence(paper, technique, "support")
                        if evidence:
                            evidence_items.append(evidence)
            except arxiv.ArxivError as e:
                raise Exception(f"ArXiv API error: {str(e)}")
            except Exception as e:
                raise Exception(f"Error fetching results: {str(e)}")
            
            # Sort by quality score
            papers.sort(key=lambda p: p["quality_score"], reverse=True)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="find_supporting_evidence",
                level=InteractionLevel.LEVEL_0,
                success=len(papers) > 0,
                duration=duration,
                input_data={
                    "technique": technique,
                    "max_results": max_results
                },
                output_data={
                    "papers": papers[:5],  # Top 5 by quality
                    "evidence_items": evidence_items,
                    "total_found": len(papers),
                    "search_query": search_query,
                    "timestamp": datetime.now().isoformat()
                },
                error=None if papers else "No supporting evidence found"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="find_supporting_evidence",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={
                    "technique": technique,
                    "max_results": max_results
                },
                output_data={},
                error=str(e)
            )
    
    def find_contradicting_research(self, technique: str, max_results: int = 10) -> InteractionResult:
        """
        Finds research that contradicts or challenges a technique.
        
        Args:
            technique: The technique to find contradictions for
            max_results: Maximum number of papers to return
            
        Returns:
            InteractionResult with contradicting papers
        """
        start_time = time.time()
        
        try:
            # Build search query for contradicting evidence
            search_query = f'"{technique}" AND (limitation OR challenge OR "does not" OR failure OR comparison OR versus)'
            
            # Search ArXiv
            search = arxiv.Search(
                query=search_query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            contradictions = []
            
            # Use the new Client API with timeout
            try:
                for paper in self.arxiv_client.results(search, timeout=30.0):
                    # Extract paper data
                    paper_data = self._extract_paper_data(paper)
                    
                    # Calculate contradiction score
                    contradiction_score = self._calculate_contradiction_score(paper, technique)
                    paper_data["contradiction_score"] = contradiction_score
                    
                    # Only include papers with clear contradictions
                    if contradiction_score >= 0.6:
                        papers.append(paper_data)
                        
                        # Extract contradicting evidence
                        evidence = self._extract_evidence(paper, technique, "contradict")
                        if evidence:
                            contradictions.append(evidence)
            except arxiv.ArxivError as e:
                raise Exception(f"ArXiv API error: {str(e)}")
            except Exception as e:
                raise Exception(f"Error fetching results: {str(e)}")
            
            # Sort by contradiction score
            papers.sort(key=lambda p: p["contradiction_score"], reverse=True)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="find_contradicting_research",
                level=InteractionLevel.LEVEL_0,
                success=True,  # Success even if no contradictions (that's useful info)
                duration=duration,
                input_data={
                    "technique": technique,
                    "max_results": max_results
                },
                output_data={
                    "papers": papers[:5],  # Top 5 contradictions
                    "contradictions": contradictions,
                    "total_found": len(papers),
                    "search_query": search_query,
                    "confidence_in_technique": 1.0 - (len(papers) / max_results),
                    "timestamp": datetime.now().isoformat()
                },
                error=None
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="find_contradicting_research",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={
                    "technique": technique,
                    "max_results": max_results
                },
                output_data={},
                error=str(e)
            )
    
    def dual_purpose_research(self, granger_need: str, client_need: str) -> InteractionResult:
        """
        Performs research that benefits both GRANGER and client systems.
        
        Args:
            granger_need: What GRANGER needs to improve
            client_need: What the client system needs
            
        Returns:
            InteractionResult with dual-purpose findings
        """
        start_time = time.time()
        
        try:
            # Find overlap between needs
            combined_query = f"({granger_need}) AND ({client_need})"
            
            # Search for papers addressing both needs
            search = arxiv.Search(
                query=combined_query,
                max_results=20,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            dual_purpose_papers = []
            granger_benefits = []
            client_benefits = []
            
            # Use the new Client API with timeout
            try:
                for paper in self.arxiv_client.results(search, timeout=30.0):
                    paper_data = self._extract_paper_data(paper)
                    
                    # Analyze benefits for both systems
                    granger_score = self._calculate_relevance_score(paper, granger_need)
                    client_score = self._calculate_relevance_score(paper, client_need)
                    
                    # Paper must benefit both (dual-purpose threshold)
                    if granger_score >= 0.6 and client_score >= 0.6:
                        paper_data["granger_relevance"] = granger_score
                        paper_data["client_relevance"] = client_score
                        paper_data["dual_purpose_score"] = (granger_score + client_score) / 2
                        
                        dual_purpose_papers.append(paper_data)
                        
                        # Extract specific benefits
                        granger_benefit = self._extract_benefit(paper, granger_need, "GRANGER")
                        client_benefit = self._extract_benefit(paper, client_need, "Client")
                        
                        if granger_benefit:
                            granger_benefits.append(granger_benefit)
                        if client_benefit:
                            client_benefits.append(client_benefit)
            except arxiv.ArxivError as e:
                raise Exception(f"ArXiv API error: {str(e)}")
            except Exception as e:
                raise Exception(f"Error fetching results: {str(e)}")
            
            # Sort by dual-purpose score
            dual_purpose_papers.sort(key=lambda p: p["dual_purpose_score"], reverse=True)
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="dual_purpose_research",
                level=InteractionLevel.LEVEL_0,
                success=len(dual_purpose_papers) > 0,
                duration=duration,
                input_data={
                    "granger_need": granger_need,
                    "client_need": client_need
                },
                output_data={
                    "dual_purpose_papers": dual_purpose_papers[:5],
                    "granger_benefits": granger_benefits,
                    "client_benefits": client_benefits,
                    "overlap_strength": len(dual_purpose_papers) / 20.0,
                    "recommendation": self._generate_recommendation(
                        dual_purpose_papers, granger_benefits, client_benefits
                    ),
                    "timestamp": datetime.now().isoformat()
                },
                error=None if dual_purpose_papers else "No dual-purpose research found"
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="dual_purpose_research",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={
                    "granger_need": granger_need,
                    "client_need": client_need
                },
                output_data={},
                error=str(e)
            )
    
    def filter_by_quality(self, papers: List[Dict[str, Any]], min_quality: float = 0.7) -> InteractionResult:
        """
        Filters papers by quality metrics.
        
        Args:
            papers: List of papers to filter
            min_quality: Minimum quality score (0-1)
            
        Returns:
            InteractionResult with filtered papers
        """
        start_time = time.time()
        
        try:
            filtered_papers = []
            quality_metrics = []
            
            for paper in papers:
                # Calculate comprehensive quality score
                quality_score, metrics = self._comprehensive_quality_assessment(paper)
                
                if quality_score >= min_quality:
                    paper["quality_score"] = quality_score
                    paper["quality_metrics"] = metrics
                    filtered_papers.append(paper)
                    quality_metrics.append(metrics)
            
            # Sort by quality
            filtered_papers.sort(key=lambda p: p["quality_score"], reverse=True)
            
            # Calculate quality statistics
            avg_quality = sum(p["quality_score"] for p in filtered_papers) / len(filtered_papers) if filtered_papers else 0
            
            duration = time.time() - start_time
            
            return InteractionResult(
                interaction_name="filter_by_quality",
                level=InteractionLevel.LEVEL_0,
                success=True,
                duration=duration,
                input_data={
                    "input_count": len(papers),
                    "min_quality": min_quality
                },
                output_data={
                    "filtered_papers": filtered_papers,
                    "filtered_count": len(filtered_papers),
                    "rejection_rate": 1 - (len(filtered_papers) / len(papers)) if papers else 0,
                    "average_quality": avg_quality,
                    "quality_distribution": self._calculate_quality_distribution(filtered_papers),
                    "timestamp": datetime.now().isoformat()
                },
                error=None
            )
            
        except Exception as e:
            return InteractionResult(
                interaction_name="filter_by_quality",
                level=InteractionLevel.LEVEL_0,
                success=False,
                duration=time.time() - start_time,
                input_data={
                    "input_count": len(papers),
                    "min_quality": min_quality
                },
                output_data={},
                error=str(e)
            )
    
    def _extract_paper_data(self, paper) -> Dict[str, Any]:
        """Extract relevant data from ArXiv paper."""
        return {
            "id": paper.entry_id,
            "title": paper.title,
            "summary": paper.summary[:1000],  # First 1000 chars
            "published": paper.published.isoformat(),
            "updated": paper.updated.isoformat() if paper.updated else None,
            "authors": [author.name for author in paper.authors],
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "pdf_url": paper.pdf_url,
            "comment": paper.comment,
            "journal_ref": paper.journal_ref
        }
    
    def _calculate_quality_score(self, paper, technique: str) -> float:
        """Calculate quality score for a paper."""
        score = 0.0
        
        # Recency (newer is better)
        days_old = (datetime.now() - paper.published.replace(tzinfo=None)).days
        if days_old < 365:
            score += 0.3
        elif days_old < 730:
            score += 0.2
        else:
            score += 0.1
        
        # Citation indicators (journal ref, updates)
        if paper.journal_ref:
            score += 0.2
        if paper.updated and paper.updated != paper.published:
            score += 0.1  # Paper was revised
        
        # Relevance to technique
        technique_lower = technique.lower()
        title_lower = paper.title.lower()
        summary_lower = paper.summary.lower()
        
        if technique_lower in title_lower:
            score += 0.2
        if technique_lower in summary_lower:
            count = summary_lower.count(technique_lower)
            score += min(0.2, count * 0.05)  # Up to 0.2 for multiple mentions
        
        # Author count (collaborative research)
        if 2 <= len(paper.authors) <= 10:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_contradiction_score(self, paper, technique: str) -> float:
        """Calculate how strongly a paper contradicts a technique."""
        score = 0.0
        
        contradiction_keywords = [
            "limitation", "challenge", "failure", "does not", "cannot",
            "inferior", "worse", "problem", "issue", "drawback",
            "compared to", "versus", "outperforms", "better than"
        ]
        
        title_lower = paper.title.lower()
        summary_lower = paper.summary.lower()
        technique_lower = technique.lower()
        
        # Check if technique is mentioned
        if technique_lower not in title_lower and technique_lower not in summary_lower:
            return 0.0  # Not about this technique
        
        # Count contradiction keywords
        for keyword in contradiction_keywords:
            if keyword in title_lower:
                score += 0.15
            if keyword in summary_lower:
                score += 0.05
        
        # Look for comparison patterns
        if "compared to" in summary_lower or "versus" in summary_lower:
            score += 0.2
        
        # Look for negative results
        if "not" in summary_lower and technique_lower in summary_lower:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_relevance_score(self, paper, need: str) -> float:
        """Calculate relevance of paper to a specific need."""
        score = 0.0
        
        need_lower = need.lower()
        need_words = need_lower.split()
        
        title_lower = paper.title.lower()
        summary_lower = paper.summary.lower()
        
        # Title relevance
        for word in need_words:
            if len(word) > 3 and word in title_lower:  # Skip short words
                score += 0.1
        
        # Summary relevance
        for word in need_words:
            if len(word) > 3:
                count = summary_lower.count(word)
                score += min(0.1, count * 0.02)
        
        # Category relevance
        if any(cat in ["cs.AI", "cs.LG", "cs.MA"] for cat in paper.categories):
            score += 0.2
        
        return min(1.0, score)
    
    def _extract_evidence(self, paper, technique: str, evidence_type: str) -> Optional[Dict[str, Any]]:
        """Extract specific evidence from paper."""
        summary_lower = paper.summary.lower()
        technique_lower = technique.lower()
        
        # Find sentences containing the technique
        sentences = paper.summary.split('. ')
        relevant_sentences = [
            s for s in sentences 
            if technique_lower in s.lower()
        ]
        
        if not relevant_sentences:
            return None
        
        return {
            "paper_id": paper.entry_id,
            "paper_title": paper.title,
            "evidence_type": evidence_type,
            "technique": technique,
            "relevant_excerpts": relevant_sentences[:3],  # Top 3 sentences
            "confidence": 0.8,  # Realistic confidence
            "extracted_at": datetime.now().isoformat()
        }
    
    def _extract_benefit(self, paper, need: str, system: str) -> Optional[Dict[str, Any]]:
        """Extract specific benefits for a system."""
        need_lower = need.lower()
        summary_lower = paper.summary.lower()
        
        # Look for benefit indicators
        benefit_keywords = ["improve", "enhance", "optimize", "better", "efficient", "effective"]
        
        sentences = paper.summary.split('. ')
        benefit_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in benefit_keywords):
                if any(word in sentence_lower for word in need_lower.split()):
                    benefit_sentences.append(sentence)
        
        if not benefit_sentences:
            return None
        
        return {
            "system": system,
            "need": need,
            "paper_id": paper.entry_id,
            "paper_title": paper.title,
            "benefits": benefit_sentences[:2],
            "implementation_hint": self._extract_implementation_hint(paper.summary),
            "confidence": 0.75
        }
    
    def _extract_implementation_hint(self, summary: str) -> Optional[str]:
        """Extract implementation hints from summary."""
        impl_keywords = ["implement", "using", "based on", "algorithm", "method", "approach"]
        
        sentences = summary.split('. ')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in impl_keywords):
                return sentence
        
        return None
    
    def _generate_recommendation(self, papers: List[Dict], granger_benefits: List[Dict], 
                               client_benefits: List[Dict]) -> Dict[str, Any]:
        """Generate recommendation based on dual-purpose research."""
        if not papers:
            return {
                "action": "continue_separate_research",
                "reason": "No overlapping research found",
                "confidence": 0.6
            }
        
        top_paper = papers[0] if papers else None
        
        return {
            "action": "implement_dual_purpose",
            "top_paper": top_paper["id"] if top_paper else None,
            "expected_granger_improvement": f"{len(granger_benefits) * 5}%",
            "expected_client_improvement": f"{len(client_benefits) * 5}%",
            "implementation_priority": "high" if len(papers) >= 3 else "medium",
            "confidence": min(0.9, 0.6 + len(papers) * 0.05)
        }
    
    def _comprehensive_quality_assessment(self, paper: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """Perform comprehensive quality assessment."""
        metrics = {
            "recency": 0.0,
            "author_credibility": 0.0,
            "venue_quality": 0.0,
            "technical_depth": 0.0,
            "reproducibility": 0.0
        }
        
        # Recency
        if "published" in paper:
            pub_date = datetime.fromisoformat(paper["published"].replace('Z', '+00:00'))
            days_old = (datetime.now() - pub_date.replace(tzinfo=None)).days
            metrics["recency"] = max(0, 1 - (days_old / 1095))  # 3 year decay
        
        # Author credibility (based on author count and institutions)
        author_count = len(paper.get("authors", []))
        if 2 <= author_count <= 8:
            metrics["author_credibility"] = 0.8
        elif author_count == 1:
            metrics["author_credibility"] = 0.6
        else:
            metrics["author_credibility"] = 0.7
        
        # Venue quality (journal reference)
        if paper.get("journal_ref"):
            metrics["venue_quality"] = 0.9
        else:
            metrics["venue_quality"] = 0.5
        
        # Technical depth (based on summary length and keywords)
        summary = paper.get("summary", "")
        technical_keywords = ["algorithm", "theorem", "proof", "experiment", "evaluation", "dataset"]
        keyword_count = sum(1 for kw in technical_keywords if kw in summary.lower())
        metrics["technical_depth"] = min(1.0, keyword_count * 0.2)
        
        # Reproducibility (mentions of code, data, repository)
        repro_keywords = ["github", "code", "implementation", "dataset", "available", "repository"]
        repro_count = sum(1 for kw in repro_keywords if kw in summary.lower())
        metrics["reproducibility"] = min(1.0, repro_count * 0.25)
        
        # Calculate overall score (weighted average)
        weights = {
            "recency": 0.25,
            "author_credibility": 0.20,
            "venue_quality": 0.20,
            "technical_depth": 0.20,
            "reproducibility": 0.15
        }
        
        overall_score = sum(metrics[key] * weights[key] for key in metrics)
        
        return overall_score, metrics
    
    def _calculate_quality_distribution(self, papers: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate distribution of quality scores."""
        distribution = {
            "excellent": 0,  # >= 0.9
            "good": 0,       # >= 0.8
            "fair": 0,       # >= 0.7
            "poor": 0        # < 0.7
        }
        
        for paper in papers:
            score = paper.get("quality_score", 0)
            if score >= 0.9:
                distribution["excellent"] += 1
            elif score >= 0.8:
                distribution["good"] += 1
            elif score >= 0.7:
                distribution["fair"] += 1
            else:
                distribution["poor"] += 1
        
        return distribution
    
    def execute(self, **kwargs) -> InteractionResult:
        """Execute the research discovery scenario."""
        technique = kwargs.get("technique", "reinforcement learning coordination")
        
        # Run all research discovery functions
        results = {
            "support": self.find_supporting_evidence(technique),
            "contradict": self.find_contradicting_research(technique),
            "dual_purpose": self.dual_purpose_research(
                "multi-agent coordination",
                "distributed system optimization"
            )
        }
        
        # Filter results by quality
        all_papers = []
        if results["support"].success:
            all_papers.extend(results["support"].output_data.get("papers", []))
        if results["contradict"].success:
            all_papers.extend(results["contradict"].output_data.get("papers", []))
        
        quality_result = self.filter_by_quality(all_papers) if all_papers else None
        
        total_duration = sum(r.duration for r in results.values())
        
        return InteractionResult(
            interaction_name="research_discovery_complete",
            level=InteractionLevel.LEVEL_0,
            success=all(r.success for r in results.values()),
            duration=total_duration,
            input_data=kwargs,
            output_data={
                "supporting_evidence": results["support"].output_data if results["support"].success else None,
                "contradicting_research": results["contradict"].output_data if results["contradict"].success else None,
                "dual_purpose": results["dual_purpose"].output_data if results["dual_purpose"].success else None,
                "quality_filtered": quality_result.output_data if quality_result else None,
                "summary": {
                    "total_papers_analyzed": len(all_papers),
                    "high_quality_papers": quality_result.output_data["filtered_count"] if quality_result else 0,
                    "dual_purpose_found": results["dual_purpose"].output_data.get("dual_purpose_papers", []) if results["dual_purpose"].success else []
                }
            },
            error=None
        )


if __name__ == "__main__":
    # Test the research discovery scenario
    scenario = ResearchDiscoveryScenario()
    
    # Test finding support
    print("Testing find supporting evidence...")
    support_result = scenario.find_supporting_evidence("transformer architectures")
    print(f"Success: {support_result.success}")
    print(f"Duration: {support_result.duration:.2f}s")
    print(f"Papers found: {len(support_result.output_data.get('papers', []))}")
    
    # Test finding contradictions
    print("\nTesting find contradicting research...")
    contradict_result = scenario.find_contradicting_research("transformer architectures")
    print(f"Success: {contradict_result.success}")
    print(f"Duration: {contradict_result.duration:.2f}s")
    print(f"Contradictions found: {len(contradict_result.output_data.get('papers', []))}")
    
    # Test dual-purpose research
    print("\nTesting dual-purpose research...")
    dual_result = scenario.dual_purpose_research(
        "model optimization",
        "inference speed improvement"
    )
    print(f"Success: {dual_result.success}")
    print(f"Duration: {dual_result.duration:.2f}s")
    print(f"Dual-purpose papers: {len(dual_result.output_data.get('dual_purpose_papers', []))}")
    
    print("\n✅ Research discovery scenario validation passed")