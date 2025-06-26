#!/usr/bin/env python3
"""
Module: test_11_arxiv_to_marker_pipeline.py
Description: Test ArXiv → Marker pipeline integration with verification
Level: 1
Modules: ArXiv MCP Server, Marker, Test Reporter
Expected Bugs: Data format mismatches, PDF download failures, conversion quality
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time

class ArXivToMarkerPipelineTest(BaseInteractionTest):
    """Level 1: Test ArXiv to Marker pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="ArXiv to Marker Pipeline",
            level=1,
            modules=["ArXiv MCP Server", "Marker", "Test Reporter"]
        )
    
    def test_paper_download_and_conversion(self):
        """Test downloading ArXiv papers and converting to Markdown"""
        self.print_header()
        
        # Import modules
        try:
            from arxiv_mcp_server import ArXivServer
            from marker.src.marker import convert_pdf_to_markdown
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run pipeline"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize ArXiv server
        try:
            arxiv_server = ArXivServer()
            self.record_test("arxiv_init", True, {})
        except Exception as e:
            self.add_bug(
                "ArXiv server initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("arxiv_init", False, {"error": str(e)})
            return
        
        # Test pipeline scenarios
        test_papers = [
            {
                "name": "Recent AI paper",
                "query": "artificial intelligence",
                "max_results": 1
            },
            {
                "name": "Specific paper by ID",
                "arxiv_id": "2301.12345",
                "max_results": 1
            },
            {
                "name": "Computer vision paper",
                "query": "computer vision transformer",
                "max_results": 1
            },
            {
                "name": "Invalid query",
                "query": "",
                "max_results": 1
            }
        ]
        
        for test in test_papers:
            print(f"\nTesting: {test['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Search ArXiv
                if "query" in test:
                    results = arxiv_server.search(
                        query=test["query"],
                        max_results=test["max_results"]
                    )
                else:
                    results = arxiv_server.get_paper(test["arxiv_id"])
                    results = [results] if results else []
                
                if not results and test["name"] != "Invalid query":
                    self.add_bug(
                        "No ArXiv results returned",
                        "HIGH",
                        test=test["name"],
                        query=test.get("query", test.get("arxiv_id"))
                    )
                    continue
                
                if results and test["name"] == "Invalid query":
                    self.add_bug(
                        "Invalid query returned results",
                        "MEDIUM",
                        query=test["query"]
                    )
                
                for paper in results[:1]:  # Process first paper only
                    print(f"Found paper: {paper.get('title', 'Unknown')[:50]}...")
                    
                    # Check data format
                    required_fields = ["title", "pdf_url", "abstract", "authors"]
                    missing_fields = [f for f in required_fields if f not in paper]
                    
                    if missing_fields:
                        self.add_bug(
                            "Missing required fields from ArXiv",
                            "HIGH",
                            missing=missing_fields,
                            received_fields=list(paper.keys())
                        )
                    
                    # Step 2: Download and convert PDF
                    pdf_url = paper.get("pdf_url")
                    if not pdf_url:
                        self.add_bug(
                            "No PDF URL in ArXiv result",
                            "HIGH",
                            paper_id=paper.get("id")
                        )
                        continue
                    
                    print(f"Converting PDF from: {pdf_url}")
                    conversion_start = time.time()
                    
                    try:
                        markdown_result = convert_pdf_to_markdown(pdf_url)
                        conversion_time = time.time() - conversion_start
                        
                        if markdown_result and isinstance(markdown_result, dict):
                            markdown = markdown_result.get("markdown", "")
                            
                            print(f"✅ Converted to {len(markdown)} chars in {conversion_time:.2f}s")
                            
                            self.record_test(f"pipeline_{test['name']}", True, {
                                "arxiv_fields": len(paper),
                                "markdown_length": len(markdown),
                                "conversion_time": conversion_time,
                                "total_time": time.time() - pipeline_start
                            })
                            
                            # Quality checks
                            if len(markdown) < 1000:
                                self.add_bug(
                                    "Suspiciously short conversion",
                                    "HIGH",
                                    paper_title=paper.get("title"),
                                    markdown_length=len(markdown)
                                )
                            
                            # Check if abstract is preserved
                            abstract = paper.get("abstract", "")
                            if abstract and abstract[:50] not in markdown:
                                self.add_bug(
                                    "Abstract not found in conversion",
                                    "MEDIUM",
                                    paper_title=paper.get("title")
                                )
                            
                            # Performance check
                            if conversion_time > 30:
                                self.add_bug(
                                    "Slow PDF conversion",
                                    "MEDIUM",
                                    duration=f"{conversion_time:.2f}s",
                                    paper_title=paper.get("title")
                                )
                        else:
                            self.add_bug(
                                "PDF conversion returned no result",
                                "HIGH",
                                pdf_url=pdf_url
                            )
                            self.record_test(f"pipeline_{test['name']}", False, {
                                "error": "No markdown result"
                            })
                            
                    except Exception as e:
                        self.add_bug(
                            "Exception in PDF conversion",
                            "HIGH",
                            error=str(e),
                            pdf_url=pdf_url
                        )
                        self.record_test(f"conversion_{test['name']}", False, {
                            "error": str(e)
                        })
                        
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {test['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{test['name']}", False, {"error": str(e)})
    
    def test_batch_processing(self):
        """Test processing multiple papers in batch"""
        print("\n\nTesting Batch Processing...")
        
        try:
            from arxiv_mcp_server import ArXivServer
            from marker.src.marker import convert_pdf_to_markdown
            
            arxiv_server = ArXivServer()
            
            # Search for multiple papers
            print("Searching for 5 papers...")
            results = arxiv_server.search(
                query="machine learning",
                max_results=5
            )
            
            if not results:
                self.add_bug(
                    "No results for batch processing",
                    "HIGH"
                )
                return
            
            print(f"Found {len(results)} papers")
            
            # Process in batch
            batch_start = time.time()
            successful_conversions = 0
            failed_conversions = 0
            total_markdown_size = 0
            
            for i, paper in enumerate(results):
                print(f"\nProcessing paper {i+1}/{len(results)}: {paper.get('title', 'Unknown')[:40]}...")
                
                pdf_url = paper.get("pdf_url")
                if not pdf_url:
                    failed_conversions += 1
                    continue
                
                try:
                    result = convert_pdf_to_markdown(pdf_url)
                    if result and result.get("markdown"):
                        successful_conversions += 1
                        total_markdown_size += len(result["markdown"])
                    else:
                        failed_conversions += 1
                except Exception as e:
                    failed_conversions += 1
                    print(f"   ❌ Failed: {str(e)[:50]}")
            
            batch_duration = time.time() - batch_start
            avg_time = batch_duration / len(results)
            
            print(f"\n✅ Batch processing complete:")
            print(f"   Successful: {successful_conversions}")
            print(f"   Failed: {failed_conversions}")
            print(f"   Total time: {batch_duration:.2f}s")
            print(f"   Average per paper: {avg_time:.2f}s")
            
            self.record_test("batch_processing", True, {
                "total_papers": len(results),
                "successful": successful_conversions,
                "failed": failed_conversions,
                "total_time": batch_duration,
                "avg_time": avg_time,
                "total_markdown_size": total_markdown_size
            })
            
            # Quality checks
            if successful_conversions == 0:
                self.add_bug(
                    "All batch conversions failed",
                    "CRITICAL",
                    total_papers=len(results)
                )
            elif failed_conversions > successful_conversions:
                self.add_bug(
                    "High failure rate in batch",
                    "HIGH",
                    success_rate=successful_conversions/len(results)
                )
            
            # Performance check
            if avg_time > 20:
                self.add_bug(
                    "Slow batch processing",
                    "MEDIUM",
                    avg_seconds_per_paper=avg_time
                )
                
        except Exception as e:
            self.add_bug(
                "Exception in batch processing",
                "HIGH",
                error=str(e)
            )
            self.record_test("batch_processing", False, {"error": str(e)})
    
    def test_error_handling(self):
        """Test error handling in pipeline"""
        print("\n\nTesting Error Handling...")
        
        error_scenarios = [
            {
                "name": "Non-existent ArXiv ID",
                "arxiv_id": "9999.99999"
            },
            {
                "name": "Malformed PDF URL",
                "pdf_url": "not_a_valid_url"
            },
            {
                "name": "Network timeout simulation",
                "pdf_url": "https://arxiv.org/pdf/timeout_test.pdf"
            }
        ]
        
        for scenario in error_scenarios:
            print(f"\nTesting: {scenario['name']}")
            
            try:
                if "arxiv_id" in scenario:
                    from arxiv_mcp_server import ArXivServer
                    arxiv_server = ArXivServer()
                    result = arxiv_server.get_paper(scenario["arxiv_id"])
                    
                    if result:
                        self.add_bug(
                            "Non-existent paper returned result",
                            "HIGH",
                            arxiv_id=scenario["arxiv_id"]
                        )
                elif "pdf_url" in scenario:
                    from marker.src.marker import convert_pdf_to_markdown
                    result = convert_pdf_to_markdown(scenario["pdf_url"])
                    
                    if result and result.get("markdown"):
                        self.add_bug(
                            "Invalid PDF converted successfully",
                            "HIGH",
                            pdf_url=scenario["pdf_url"]
                        )
                
                self.record_test(f"error_handling_{scenario['name']}", True, {
                    "handled_gracefully": True
                })
                
            except Exception as e:
                # Exception is expected for error scenarios
                print(f"   ✅ Error handled: {str(e)[:50]}")
                self.record_test(f"error_handling_{scenario['name']}", True, {
                    "error": str(e)
                })
    
    def run_tests(self):
        """Run all tests"""
        self.test_paper_download_and_conversion()
        self.test_batch_processing()
        self.test_error_handling()
        return self.generate_report()


def main():
    """Run the test"""
    tester = ArXivToMarkerPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)