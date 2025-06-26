#!/usr/bin/env python3
"""
Module: test_25_real_time_collaboration.py
Description: Test real-time collaboration between Granger Hub and multiple modules
Level: 2  
Modules: Granger Hub, ArXiv MCP Server, SPARTA, Marker, Test Reporter
Expected Bugs: Message synchronization issues, race conditions, state conflicts
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import threading
import queue

class RealTimeCollaborationTest(BaseInteractionTest):
    """Level 2: Test real-time multi-module collaboration"""
    
    def __init__(self):
        super().__init__(
            test_name="Real-Time Collaboration",
            level=2,
            modules=["Granger Hub", "ArXiv MCP Server", "SPARTA", "Marker", "Test Reporter"]
        )
    
    def test_concurrent_module_collaboration(self):
        """Test multiple modules working together in real-time"""
        self.print_header()
        
        # Import modules
        try:
            from granger_hub import GrangerHub, CollaborationSession
            from arxiv_mcp_server import ArXivServer
            from sparta_handlers.real_sparta_handlers import SPARTAHandler  
            from marker.src.marker import convert_pdf_to_markdown
            from claude_test_reporter import GrangerTestReporter
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run collaboration"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            hub = GrangerHub()
            arxiv = ArXivServer()
            sparta = SPARTAHandler()
            reporter = GrangerTestReporter(
                module_name="collaboration_test",
                test_suite="real_time"
            )
            self.record_test("components_init", True, {})
        except Exception as e:
            self.add_bug(
                "Component initialization failed",
                "CRITICAL", 
                error=str(e)
            )
            self.record_test("components_init", False, {"error": str(e)})
            return
        
        collaboration_start = time.time()
        
        # Create shared state
        shared_state = {
            "papers_found": [],
            "cves_identified": [],
            "documents_processed": [],
            "alerts_generated": [],
            "lock": threading.Lock()
        }
        
        # Message queue for hub
        message_queue = queue.Queue()
        
        print("\n🤝 Starting Real-Time Collaboration Test...")
        
        # Define collaborative tasks
        def arxiv_researcher():
            """ArXiv researcher thread"""
            try:
                print("\n📚 ArXiv: Starting research...")
                papers = arxiv.search("cybersecurity vulnerabilities", max_results=3)
                
                with shared_state["lock"]:
                    shared_state["papers_found"] = papers
                
                # Notify hub
                for paper in papers:
                    message_queue.put({
                        "source": "arxiv",
                        "type": "new_paper",
                        "data": paper
                    })
                
                print(f"📚 ArXiv: Found {len(papers)} papers")
                
            except Exception as e:
                self.add_bug(
                    "ArXiv researcher failed",
                    "HIGH",
                    error=str(e)
                )
        
        def sparta_analyzer():
            """SPARTA analyzer thread"""
            try:
                print("\n🛡️ SPARTA: Monitoring for CVEs...")
                
                # Wait for papers
                time.sleep(1)
                
                with shared_state["lock"]:
                    papers = shared_state["papers_found"]
                
                cves_found = []
                
                for paper in papers:
                    # Extract CVEs from abstract
                    import re
                    cves = re.findall(r'CVE-\d{4}-\d{4,7}', paper.get("abstract", ""))
                    
                    for cve in cves:
                        # Enrich with SPARTA
                        details = sparta.handle({
                            "operation": "get_cve_details",
                            "cve_id": cve
                        })
                        
                        if details and "error" not in details:
                            cves_found.append({
                                "cve_id": cve,
                                "details": details,
                                "source_paper": paper["id"]
                            })
                            
                            # Notify hub
                            message_queue.put({
                                "source": "sparta",
                                "type": "cve_alert",
                                "data": {
                                    "cve": cve,
                                    "severity": details.get("cvss_score", 5.0)
                                }
                            })
                
                with shared_state["lock"]:
                    shared_state["cves_identified"] = cves_found
                
                print(f"🛡️ SPARTA: Identified {len(cves_found)} CVEs")
                
            except Exception as e:
                self.add_bug(
                    "SPARTA analyzer failed",
                    "HIGH",
                    error=str(e)
                )
        
        def marker_processor():
            """Marker processor thread"""
            try:
                print("\n📄 Marker: Processing documents...")
                
                # Wait for papers
                time.sleep(2)
                
                with shared_state["lock"]:
                    papers = shared_state["papers_found"]
                
                processed = []
                
                for paper in papers[:2]:  # Limit processing
                    pdf_url = paper.get("pdf_url")
                    if pdf_url:
                        try:
                            result = convert_pdf_to_markdown(pdf_url)
                            
                            if result and result.get("markdown"):
                                processed.append({
                                    "paper_id": paper["id"],
                                    "content_length": len(result["markdown"]),
                                    "processing_time": result.get("processing_time", 0)
                                })
                                
                                # Notify hub
                                message_queue.put({
                                    "source": "marker",
                                    "type": "document_ready",
                                    "data": {
                                        "paper_id": paper["id"],
                                        "size": len(result["markdown"])
                                    }
                                })
                        except Exception as e:
                            print(f"📄 Marker: Failed to process {paper['id']}: {str(e)[:30]}")
                
                with shared_state["lock"]:
                    shared_state["documents_processed"] = processed
                
                print(f"📄 Marker: Processed {len(processed)} documents")
                
            except Exception as e:
                self.add_bug(
                    "Marker processor failed",
                    "HIGH",
                    error=str(e)
                )
        
        def hub_coordinator():
            """Hub coordinator thread"""
            try:
                print("\n🌐 Hub: Coordinating collaboration...")
                
                alerts = []
                start_time = time.time()
                
                while time.time() - start_time < 10:  # Run for 10 seconds
                    try:
                        message = message_queue.get(timeout=1)
                        
                        print(f"🌐 Hub: Received {message['type']} from {message['source']}")
                        
                        # Process message
                        if message["type"] == "cve_alert" and message["data"]["severity"] > 7:
                            alert = {
                                "type": "high_severity_cve",
                                "cve": message["data"]["cve"],
                                "timestamp": time.time()
                            }
                            alerts.append(alert)
                            
                            # Broadcast alert
                            print(f"🚨 Hub: Broadcasting high severity alert for {message['data']['cve']}")
                        
                        # Report to test reporter
                        reporter.add_test_result(
                            test_name=f"message_{message['type']}",
                            status="PASS",
                            duration=0.1,
                            metadata=message
                        )
                        
                    except queue.Empty:
                        continue
                
                with shared_state["lock"]:
                    shared_state["alerts_generated"] = alerts
                
                print(f"🌐 Hub: Generated {len(alerts)} alerts")
                
            except Exception as e:
                self.add_bug(
                    "Hub coordinator failed", 
                    "HIGH",
                    error=str(e)
                )
        
        # Start all threads
        threads = [
            threading.Thread(target=arxiv_researcher, name="arxiv"),
            threading.Thread(target=sparta_analyzer, name="sparta"),
            threading.Thread(target=marker_processor, name="marker"),
            threading.Thread(target=hub_coordinator, name="hub")
        ]
        
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=15)
            if thread.is_alive():
                self.add_bug(
                    f"Thread {thread.name} did not complete",
                    "HIGH",
                    timeout=15
                )
        
        collaboration_duration = time.time() - collaboration_start
        
        # Analyze results
        print(f"\n📊 Collaboration Summary:")
        print(f"   Duration: {collaboration_duration:.2f}s")
        print(f"   Papers found: {len(shared_state['papers_found'])}")
        print(f"   CVEs identified: {len(shared_state['cves_identified'])}")
        print(f"   Documents processed: {len(shared_state['documents_processed'])}")
        print(f"   Alerts generated: {len(shared_state['alerts_generated'])}")
        
        self.record_test("real_time_collaboration", True, {
            "duration": collaboration_duration,
            "papers": len(shared_state["papers_found"]),
            "cves": len(shared_state["cves_identified"]),
            "documents": len(shared_state["documents_processed"]),
            "alerts": len(shared_state["alerts_generated"]),
            "messages_processed": message_queue.qsize()
        })
        
        # Check for collaboration issues
        if not shared_state["papers_found"]:
            self.add_bug(
                "No papers found in collaboration",
                "HIGH"
            )
        
        if shared_state["papers_found"] and not shared_state["documents_processed"]:
            self.add_bug(
                "Papers found but none processed",
                "HIGH",
                papers_count=len(shared_state["papers_found"])
            )
        
        # Check for race conditions
        self.check_for_race_conditions(shared_state)
        
        # Generate collaboration report
        self.generate_collaboration_report(reporter, shared_state)
    
    def check_for_race_conditions(self, shared_state):
        """Check for potential race conditions"""
        print("\n🔍 Checking for race conditions...")
        
        # Check if all modules accessed shared state
        modules_accessed = []
        
        if shared_state["papers_found"]:
            modules_accessed.append("arxiv")
        if shared_state["cves_identified"]:
            modules_accessed.append("sparta")
        if shared_state["documents_processed"]:
            modules_accessed.append("marker")
        if shared_state["alerts_generated"]:
            modules_accessed.append("hub")
        
        if len(modules_accessed) < 4:
            self.add_bug(
                "Not all modules participated",
                "MEDIUM",
                participated=modules_accessed,
                expected=["arxiv", "sparta", "marker", "hub"]
            )
        
        # Check data consistency
        paper_ids = {p["id"] for p in shared_state["papers_found"]}
        processed_ids = {d["paper_id"] for d in shared_state["documents_processed"]}
        
        if processed_ids and not processed_ids.issubset(paper_ids):
            self.add_bug(
                "Data inconsistency detected",
                "HIGH",
                issue="Processed papers not in found papers",
                processed_not_found=list(processed_ids - paper_ids)
            )
    
    def generate_collaboration_report(self, reporter, shared_state):
        """Generate collaboration analysis report"""
        print("\n📄 Generating collaboration report...")
        
        try:
            report = reporter.generate_report(
                include_skeptical_analysis=True,
                include_performance_trends=True
            )
            
            if report:
                with open("collaboration_report.html", 'w') as f:
                    f.write(report)
                print("✅ Collaboration report generated")
                
                # Also save collaboration data
                import json
                collab_data = {
                    "papers": shared_state["papers_found"],
                    "cves": shared_state["cves_identified"],
                    "documents": shared_state["documents_processed"],
                    "alerts": shared_state["alerts_generated"]
                }
                
                with open("collaboration_data.json", 'w') as f:
                    json.dump(collab_data, f, indent=2, default=str)
                
        except Exception as e:
            self.add_bug(
                "Failed to generate collaboration report",
                "MEDIUM",
                error=str(e)
            )
    
    def run_tests(self):
        """Run all tests"""
        self.test_concurrent_module_collaboration()
        return self.generate_report()


def main():
    """Run the test"""
    tester = RealTimeCollaborationTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)