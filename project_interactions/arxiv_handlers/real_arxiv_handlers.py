#!/usr/bin/env python3

# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Real ArXiv Handlers for GRANGER Integration

This module provides real handlers that use the actual arxiv Python library
and arxiv-mcp-server functionality for research paper discovery and analysis.

External Dependencies:
- arxiv: https://pypi.org/project/arxiv/
- requests: For downloading PDFs

Example Usage:
>>> from real_arxiv_handlers import ArxivSearchHandler
>>> handler = ArxivSearchHandler()
>>> result = handler.handle({"query": "transformer architectures", "max_results": 5})
>>> print(f"Found {result['paper_count']} papers")
"""

import time
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import tempfile
import os

# Import arxiv library
try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError:
    ARXIV_AVAILABLE = False
    print("WARNING: arxiv library not available. Install with: pip install arxiv")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("WARNING: requests library not available. Install with: pip install requests")


class BaseArxivHandler:
    """Base class for ArXiv handlers"""
    
    def __init__(self):
        self.client = arxiv.Client() if ARXIV_AVAILABLE else None
        self.cache_dir = Path("/tmp/arxiv_cache")
        self.cache_dir.mkdir(exist_ok=True)
        
    def _extract_paper_data(self, paper: arxiv.Result) -> Dict[str, Any]:
        """Extract relevant data from ArXiv paper"""
        return {
            "id": paper.entry_id,
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "published": paper.published.isoformat(),
            "updated": paper.updated.isoformat() if paper.updated else None,
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "pdf_url": paper.pdf_url,
            "comment": paper.comment,
            "journal_ref": paper.journal_ref,
            "doi": paper.doi,
            "links": [{"href": link.href, "title": link.title} for link in paper.links]
        }
    
    def _calculate_relevance_score(self, paper: arxiv.Result, query: str) -> float:
        """Calculate relevance score for a paper based on query"""
        score = 0.0
        query_lower = query.lower()
        
        # Title match (highest weight)
        if query_lower in paper.title.lower():
            score += 0.4
        
        # Abstract match
        if query_lower in paper.summary.lower():
            score += 0.3
            
        # Count occurrences in abstract
        occurrences = paper.summary.lower().count(query_lower)
        score += min(0.2, occurrences * 0.02)
        
        # Recent papers get a small boost
        days_old = (datetime.now() - paper.published.replace(tzinfo=None)).days
        if days_old < 30:
            score += 0.1
        elif days_old < 90:
            score += 0.05
            
        return min(1.0, score)


class ArxivSearchHandler(BaseArxivHandler):
    """Handler for searching ArXiv papers"""
    
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search ArXiv for papers matching a query
        
        Args:
            params: Dictionary with:
                - query: Search query string
                - max_results: Maximum papers to return (default: 10)
                - sort_by: Sort criterion (default: relevance)
                
        Returns:
            Dictionary with papers and metadata
        """
        if not ARXIV_AVAILABLE:
            return {
                "error": "arxiv library not available",
                "paper_count": 0,
                "papers": []
            }
            
        query = params.get("query", "")
        max_results = params.get("max_results", 10)
        sort_by = params.get("sort_by", "relevance")
        
        # Map sort criteria
        sort_criterion = {
            "relevance": arxiv.SortCriterion.Relevance,
            "submitted_date": arxiv.SortCriterion.SubmittedDate,
            "last_updated": arxiv.SortCriterion.LastUpdatedDate
        }.get(sort_by, arxiv.SortCriterion.Relevance)
        
        try:
            start_time = time.time()
            
            # Create search
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=sort_criterion,
                sort_order=arxiv.SortOrder.Descending
            )
            
            # Execute search using client
            papers = []
            for paper in self.client.results(search):
                paper_data = self._extract_paper_data(paper)
                paper_data["relevance_score"] = self._calculate_relevance_score(paper, query)
                papers.append(paper_data)
            
            # Sort by relevance if not already sorted
            if sort_by != "relevance":
                papers.sort(key=lambda p: p["relevance_score"], reverse=True)
            
            duration = time.time() - start_time
            
            return {
                "query": query,
                "paper_count": len(papers),
                "papers": papers,
                "search_time": duration,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "paper_count": 0,
                "papers": []
            }


class ArxivDownloadHandler(BaseArxivHandler):
    """Handler for downloading ArXiv PDFs"""
    
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Download PDFs from ArXiv
        
        Args:
            params: Dictionary with:
                - paper_ids: List of ArXiv IDs or URLs
                - output_dir: Where to save PDFs (optional)
                
        Returns:
            Dictionary with download results
        """
        if not REQUESTS_AVAILABLE:
            return {
                "error": "requests library not available",
                "downloaded": 0,
                "files": []
            }
            
        paper_ids = params.get("paper_ids", [])
        output_dir = Path(params.get("output_dir", self.cache_dir))
        output_dir.mkdir(exist_ok=True)
        
        results = []
        downloaded = 0
        
        for paper_id in paper_ids:
            try:
                # Clean up paper ID
                if "arxiv.org" in paper_id:
                    paper_id = paper_id.split("/")[-1].replace(".pdf", "")
                
                # Construct PDF URL
                pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
                
                # Download PDF
                start_time = time.time()
                response = requests.get(pdf_url, timeout=30)
                response.raise_for_status()
                
                # Save PDF
                pdf_path = output_dir / f"{paper_id.replace('/', '_')}.pdf"
                pdf_path.write_bytes(response.content)
                
                duration = time.time() - start_time
                file_size = len(response.content)
                
                results.append({
                    "paper_id": paper_id,
                    "pdf_url": pdf_url,
                    "file_path": str(pdf_path),
                    "file_size": file_size,
                    "download_time": duration,
                    "success": True
                })
                downloaded += 1
                
            except Exception as e:
                results.append({
                    "paper_id": paper_id,
                    "error": str(e),
                    "success": False
                })
        
        return {
            "requested": len(paper_ids),
            "downloaded": downloaded,
            "files": results,
            "output_dir": str(output_dir)
        }


class ArxivCitationHandler(BaseArxivHandler):
    """Handler for finding papers that cite or are cited by a given paper"""
    
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find citation relationships for papers
        
        Args:
            params: Dictionary with:
                - paper_id: ArXiv ID to find citations for
                - direction: "citing" or "cited_by"
                - max_results: Maximum results
                
        Returns:
            Dictionary with citation data
        """
        if not ARXIV_AVAILABLE:
            return {
                "error": "arxiv library not available",
                "citations": []
            }
            
        paper_id = params.get("paper_id", "")
        direction = params.get("direction", "citing")
        max_results = params.get("max_results", 20)
        
        try:
            # First get the target paper
            search = arxiv.Search(id_list=[paper_id])
            papers = list(self.client.results(search))
            
            if not papers:
                return {
                    "error": f"Paper {paper_id} not found",
                    "citations": []
                }
            
            target_paper = papers[0]
            target_data = self._extract_paper_data(target_paper)
            
            # Search for citations
            # Note: ArXiv doesn't provide direct citation data, so we search for papers
            # that mention the title or ID in their text
            if direction == "citing":
                # Papers that cite this paper (mention it)
                query = f'"{target_paper.title}" OR "{paper_id}"'
            else:
                # Papers this paper might cite (harder to find without full text)
                # Use keywords from abstract
                keywords = self._extract_keywords(target_paper.summary)
                query = " OR ".join([f'"{kw}"' for kw in keywords[:5]])
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            citations = []
            for paper in self.client.results(search):
                # Skip the target paper itself
                if paper.entry_id == target_paper.entry_id:
                    continue
                    
                paper_data = self._extract_paper_data(paper)
                
                # Calculate citation confidence
                confidence = self._calculate_citation_confidence(
                    target_paper, paper, direction
                )
                
                if confidence > 0.3:  # Threshold for likely citation
                    paper_data["citation_confidence"] = confidence
                    citations.append(paper_data)
            
            # Sort by confidence
            citations.sort(key=lambda p: p["citation_confidence"], reverse=True)
            
            return {
                "target_paper": target_data,
                "direction": direction,
                "citation_count": len(citations),
                "citations": citations[:max_results]
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "citations": []
            }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction - in production, use NLP
        import re
        
        # Remove common words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'can', 'could'}
        
        # Extract words
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        # Count frequencies
        word_freq = {}
        for word in words:
            if word not in stopwords and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top keywords
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [kw[0] for kw in keywords]
    
    def _calculate_citation_confidence(self, target: arxiv.Result, 
                                     candidate: arxiv.Result, 
                                     direction: str) -> float:
        """Calculate confidence that candidate cites target"""
        confidence = 0.0
        
        # Check if published after target (for citing papers)
        if direction == "citing" and candidate.published > target.published:
            confidence += 0.2
        
        # Check title mention
        if target.title.lower() in candidate.summary.lower():
            confidence += 0.4
            
        # Check ID mention
        target_id = target.entry_id.split("/")[-1]
        if target_id in candidate.summary:
            confidence += 0.3
            
        # Check author overlap (might indicate self-citation)
        target_authors = {a.name for a in target.authors}
        candidate_authors = {a.name for a in candidate.authors}
        if target_authors & candidate_authors:
            confidence += 0.1
            
        return min(1.0, confidence)


class ArxivEvidenceHandler(BaseArxivHandler):
    """Handler for finding supporting or contradicting evidence"""
    
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find evidence supporting or contradicting a claim
        
        Args:
            params: Dictionary with:
                - claim: The claim to find evidence for
                - evidence_type: "supporting" or "contradicting"
                - max_results: Maximum papers to analyze
                
        Returns:
            Dictionary with evidence papers
        """
        if not ARXIV_AVAILABLE:
            return {
                "error": "arxiv library not available",
                "evidence": []
            }
            
        claim = params.get("claim", "")
        evidence_type = params.get("evidence_type", "supporting")
        max_results = params.get("max_results", 10)
        
        try:
            # Build search query based on evidence type
            if evidence_type == "supporting":
                query = f'{claim} AND (confirms OR supports OR demonstrates OR proves OR "consistent with")'
            else:
                query = f'{claim} AND (contradicts OR refutes OR challenges OR "inconsistent with" OR "contrary to")'
            
            search = arxiv.Search(
                query=query,
                max_results=max_results * 2,  # Get more to filter
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            evidence_papers = []
            
            for paper in self.client.results(search):
                paper_data = self._extract_paper_data(paper)
                
                # Extract evidence snippets
                evidence = self._extract_evidence_snippets(
                    paper.summary, claim, evidence_type
                )
                
                if evidence["confidence"] > 0.5:
                    paper_data["evidence"] = evidence
                    evidence_papers.append(paper_data)
            
            # Sort by evidence confidence
            evidence_papers.sort(
                key=lambda p: p["evidence"]["confidence"], 
                reverse=True
            )
            
            return {
                "claim": claim,
                "evidence_type": evidence_type,
                "evidence_count": len(evidence_papers),
                "evidence": evidence_papers[:max_results]
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "evidence": []
            }
    
    def _extract_evidence_snippets(self, abstract: str, claim: str, 
                                  evidence_type: str) -> Dict[str, Any]:
        """Extract evidence snippets from abstract"""
        snippets = []
        confidence = 0.0
        
        # Split into sentences
        sentences = abstract.split(". ")
        claim_lower = claim.lower()
        
        # Keywords for each evidence type
        if evidence_type == "supporting":
            keywords = ["confirm", "support", "demonstrate", "prove", "show",
                       "consistent", "agree", "validate", "verify"]
        else:
            keywords = ["contradict", "refute", "challenge", "dispute", "contrary",
                       "inconsistent", "disagree", "question", "doubt"]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence is relevant to claim
            if any(word in claim_lower for word in sentence_lower.split()):
                # Check for evidence keywords
                for keyword in keywords:
                    if keyword in sentence_lower:
                        snippets.append({
                            "text": sentence.strip(),
                            "keyword": keyword
                        })
                        confidence += 0.2
                        break
        
        # Cap confidence at 1.0
        confidence = min(1.0, confidence)
        
        return {
            "snippets": snippets[:3],  # Top 3 snippets
            "confidence": confidence,
            "snippet_count": len(snippets)
        }


class ArxivBatchHandler(BaseArxivHandler):
    """Handler for batch processing multiple ArXiv operations"""
    
    def handle(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process multiple ArXiv operations in batch
        
        Args:
            params: Dictionary with:
                - operations: List of operations to perform
                
        Returns:
            Dictionary with batch results
        """
        operations = params.get("operations", [])
        results = []
        
        # Initialize handlers
        handlers = {
            "search": ArxivSearchHandler(),
            "download": ArxivDownloadHandler(),
            "citation": ArxivCitationHandler(),
            "evidence": ArxivEvidenceHandler()
        }
        
        start_time = time.time()
        
        for op in operations:
            op_type = op.get("type")
            op_params = op.get("params", {})
            
            if op_type in handlers:
                try:
                    result = handlers[op_type].handle(op_params)
                    results.append({
                        "operation": op_type,
                        "success": "error" not in result,
                        "result": result
                    })
                except Exception as e:
                    results.append({
                        "operation": op_type,
                        "success": False,
                        "error": str(e)
                    })
            else:
                results.append({
                    "operation": op_type,
                    "success": False,
                    "error": f"Unknown operation type: {op_type}"
                })
        
        duration = time.time() - start_time
        
        return {
            "total_operations": len(operations),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "batch_time": duration,
            "results": results
        }


if __name__ == "__main__":
    # Test the handlers
    print("Testing ArXiv Handlers...")
    
    # Test search
    search_handler = ArxivSearchHandler()
    result = search_handler.handle({
        "query": "transformer architectures",
        "max_results": 3
    })
    print(f"\nSearch Test: Found {result.get('paper_count', 0)} papers")
    
    # Test evidence finding
    evidence_handler = ArxivEvidenceHandler()
    result = evidence_handler.handle({
        "claim": "transformers improve natural language processing",
        "evidence_type": "supporting",
        "max_results": 2
    })
    print(f"\nEvidence Test: Found {result.get('evidence_count', 0)} supporting papers")