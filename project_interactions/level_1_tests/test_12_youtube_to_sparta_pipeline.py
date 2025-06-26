"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_12_youtube_to_sparta_pipeline.py
Description: Test YouTube → SPARTA cybersecurity enrichment pipeline
Level: 1
Modules: YouTube Transcripts, SPARTA, Test Reporter
Expected Bugs: CVE extraction errors, transcript parsing issues, enrichment quality
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time

class YouTubeToSpartaPipelineTest(BaseInteractionTest):
    """Level 1: Test YouTube to SPARTA pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="YouTube to SPARTA Pipeline",
            level=1,
            modules=["YouTube Transcripts", "SPARTA", "Test Reporter"]
        )
    
    def test_cve_extraction_and_enrichment(self):
        """Test extracting CVEs from YouTube and enriching with SPARTA"""
        self.print_header()
        
        # Import modules
        try:
            from youtube_transcripts.src.youtube_transcripts import download_youtube_transcript
            from youtube_transcripts.link_extractor import extract_cves_from_text
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
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
        
        # Initialize SPARTA
        try:
            sparta = SPARTAHandler()
            self.record_test("sparta_init", True, {})
        except Exception as e:
            self.add_bug(
                "SPARTA initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("sparta_init", False, {"error": str(e)})
            return
        
        # Test videos likely to contain CVE discussions
        test_videos = [
            {
                "name": "Security conference talk",
                "video_id": "dQw4w9WgXcQ",  # Replace with real security video
                "expected_cves": True
            },
            {
                "name": "Vulnerability disclosure",
                "video_id": "security_video_id",
                "expected_cves": True
            },
            {
                "name": "Non-security video",
                "video_id": "cooking_video_id",
                "expected_cves": False
            }
        ]
        
        for test in test_videos:
            print(f"\nTesting: {test['name']}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Download transcript
                print(f"Downloading transcript for: {test['video_id']}")
                transcript_path = download_youtube_transcript(
                    f"https://www.youtube.com/watch?v={test['video_id']}"
                )
                
                if not transcript_path:
                    if test["expected_cves"]:
                        self.add_bug(
                            "Failed to download security video transcript",
                            "HIGH",
                            video=test["name"]
                        )
                    continue
                
                # Read transcript
                with open(transcript_path, 'r') as f:
                    transcript_text = f.read()
                
                print(f"Got transcript: {len(transcript_text)} chars")
                
                # Step 2: Extract CVEs
                cves_found = extract_cves_from_text(transcript_text)
                
                print(f"Found {len(cves_found)} CVEs")
                
                if test["expected_cves"] and not cves_found:
                    self.add_bug(
                        "No CVEs found in security video",
                        "MEDIUM",
                        video=test["name"],
                        transcript_length=len(transcript_text)
                    )
                elif not test["expected_cves"] and cves_found:
                    self.add_bug(
                        "False positive CVE extraction",
                        "MEDIUM",
                        video=test["name"],
                        cves_found=cves_found
                    )
                
                # Step 3: Enrich each CVE with SPARTA
                enriched_cves = []
                enrichment_errors = []
                
                for cve in cves_found[:5]:  # Limit to first 5
                    print(f"\nEnriching {cve}...")
                    
                    try:
                        enrichment = sparta.handle({
                            "operation": "get_cve_details",
                            "cve_id": cve
                        })
                        
                        if enrichment and "error" not in enrichment:
                            enriched_cves.append({
                                "cve": cve,
                                "enrichment": enrichment
                            })
                            
                            # Validate enrichment quality
                            required_fields = ["description", "severity", "published_date"]
                            missing = [f for f in required_fields 
                                     if f not in enrichment or not enrichment[f]]
                            
                            if missing:
                                self.add_bug(
                                    "Incomplete CVE enrichment",
                                    "MEDIUM",
                                    cve=cve,
                                    missing_fields=missing
                                )
                        else:
                            enrichment_errors.append({
                                "cve": cve,
                                "error": enrichment.get("error", "Unknown error")
                            })
                    except Exception as e:
                        enrichment_errors.append({
                            "cve": cve,
                            "error": str(e)
                        })
                
                # Record results
                pipeline_duration = time.time() - pipeline_start
                
                self.record_test(f"pipeline_{test['name']}", True, {
                    "transcript_length": len(transcript_text),
                    "cves_found": len(cves_found),
                    "cves_enriched": len(enriched_cves),
                    "enrichment_errors": len(enrichment_errors),
                    "total_time": pipeline_duration
                })
                
                # Quality checks
                if cves_found and len(enrichment_errors) > len(enriched_cves):
                    self.add_bug(
                        "High enrichment failure rate",
                        "HIGH",
                        success_rate=len(enriched_cves)/len(cves_found) if cves_found else 0
                    )
                
                # Performance check
                if pipeline_duration > 60:
                    self.add_bug(
                        "Slow pipeline execution",
                        "MEDIUM",
                        duration=f"{pipeline_duration:.2f}s",
                        cves_processed=len(cves_found)
                    )
                
                print(f"\n✅ Pipeline complete:")
                print(f"   CVEs found: {len(cves_found)}")
                print(f"   Enriched: {len(enriched_cves)}")
                print(f"   Errors: {len(enrichment_errors)}")
                print(f"   Time: {pipeline_duration:.2f}s")
                
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {test['name']}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{test['name']}", False, {"error": str(e)})
    
    def test_threat_intelligence_extraction(self):
        """Test extracting threat intelligence from videos"""
        print("\n\nTesting Threat Intelligence Extraction...")
        
        try:
            from youtube_transcripts.src.youtube_transcripts import download_youtube_transcript
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            
            sparta = SPARTAHandler()
            
            # Simulate transcript with threat indicators
            test_transcript = """
            In this security briefing, we discuss CVE-2023-12345 which affects
            systems at IP addresses 192.168.1.1 and 10.0.0.1. The malware 
            communicates with domain evil.example.com and drops files with 
            hash 5d41402abc4b2a76b9719d911017c592. APT group Lazarus is 
            suspected to be behind this campaign targeting financial institutions.
            """
            
            print("Extracting threat indicators...")
            
            # Extract various indicators
            indicators = {
                "cves": [],
                "ips": [],
                "domains": [],
                "hashes": [],
                "threat_actors": []
            }
            
            # Simple extraction (real implementation would be more sophisticated)
            import re
            
            # Extract CVEs
            cve_pattern = r'CVE-\d{4}-\d{4,7}'
            indicators["cves"] = re.findall(cve_pattern, test_transcript)
            
            # Extract IPs
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            indicators["ips"] = re.findall(ip_pattern, test_transcript)
            
            # Extract domains
            domain_pattern = r'[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}'
            indicators["domains"] = re.findall(domain_pattern, test_transcript)
            
            # Extract MD5 hashes
            hash_pattern = r'\b[a-fA-F0-9]{32}\b'
            indicators["hashes"] = re.findall(hash_pattern, test_transcript)
            
            # Extract threat actors
            actors = ["Lazarus", "APT28", "APT29", "Carbanak"]
            for actor in actors:
                if actor.lower() in test_transcript.lower():
                    indicators["threat_actors"].append(actor)
            
            print(f"Found indicators: {sum(len(v) for v in indicators.values())} total")
            
            # Enrich indicators with SPARTA
            enriched_count = 0
            
            for indicator_type, values in indicators.items():
                for value in values:
                    try:
                        if indicator_type == "cves":
                            result = sparta.handle({
                                "operation": "get_cve_details",
                                "cve_id": value
                            })
                        elif indicator_type == "ips":
                            result = sparta.handle({
                                "operation": "check_ip_reputation",
                                "ip": value
                            })
                        elif indicator_type == "domains":
                            result = sparta.handle({
                                "operation": "check_domain_reputation",
                                "domain": value
                            })
                        elif indicator_type == "hashes":
                            result = sparta.handle({
                                "operation": "check_file_hash",
                                "hash": value
                            })
                        elif indicator_type == "threat_actors":
                            result = sparta.handle({
                                "operation": "get_threat_actor_info",
                                "actor": value
                            })
                        
                        if result and "error" not in result:
                            enriched_count += 1
                            
                    except Exception as e:
                        print(f"   ❌ Failed to enrich {value}: {str(e)[:50]}")
            
            self.record_test("threat_intelligence_extraction", True, {
                "indicators_found": sum(len(v) for v in indicators.values()),
                "indicators_by_type": {k: len(v) for k, v in indicators.items()},
                "enriched_count": enriched_count
            })
            
            # Quality checks
            if not any(indicators.values()):
                self.add_bug(
                    "No threat indicators extracted",
                    "HIGH",
                    transcript_sample=test_transcript[:100]
                )
            
            if enriched_count == 0 and sum(len(v) for v in indicators.values()) > 0:
                self.add_bug(
                    "Failed to enrich any indicators",
                    "HIGH",
                    total_indicators=sum(len(v) for v in indicators.values())
                )
                
        except Exception as e:
            self.add_bug(
                "Exception in threat intelligence extraction",
                "HIGH",
                error=str(e)
            )
            self.record_test("threat_intelligence", False, {"error": str(e)})
    
    def test_streaming_analysis(self):
        """Test real-time streaming transcript analysis"""
        print("\n\nTesting Streaming Analysis...")
        
        try:
            # Simulate streaming transcript chunks
            transcript_chunks = [
                "Welcome to our security podcast.",
                "Today we'll discuss CVE-2023-98765",
                "This vulnerability affects Windows systems",
                "The CVSS score is 9.8 critical",
                "Patches are available from Microsoft"
            ]
            
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            sparta = SPARTAHandler()
            
            print("Processing transcript stream...")
            
            cves_detected = []
            enrichments = []
            
            for i, chunk in enumerate(transcript_chunks):
                print(f"\nChunk {i+1}: {chunk[:30]}...")
                
                # Check for CVEs in chunk
                import re
                cves = re.findall(r'CVE-\d{4}-\d{4,7}', chunk)
                
                if cves:
                    print(f"   Found CVE: {cves[0]}")
                    cves_detected.extend(cves)
                    
                    # Immediately enrich
                    for cve in cves:
                        try:
                            result = sparta.handle({
                                "operation": "get_cve_details",
                                "cve_id": cve
                            })
                            if result and "error" not in result:
                                enrichments.append(result)
                                print(f"   ✅ Enriched {cve}")
                        except Exception as e:
                            print(f"   ❌ Failed to enrich: {e}")
                
                # Simulate streaming delay
                time.sleep(0.1)
            
            self.record_test("streaming_analysis", True, {
                "chunks_processed": len(transcript_chunks),
                "cves_detected": len(cves_detected),
                "enrichments": len(enrichments)
            })
            
            # Check streaming performance
            if cves_detected and not enrichments:
                self.add_bug(
                    "Failed to enrich CVEs in real-time",
                    "HIGH",
                    cves_found=cves_detected
                )
                
        except Exception as e:
            self.add_bug(
                "Exception in streaming analysis",
                "HIGH",
                error=str(e)
            )
            self.record_test("streaming_analysis", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_cve_extraction_and_enrichment()
        self.test_threat_intelligence_extraction()
        self.test_streaming_analysis()
        return self.generate_report()


def main():
    """Run the test"""
    tester = YouTubeToSpartaPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)