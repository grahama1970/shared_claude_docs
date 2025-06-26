#!/usr/bin/env python3
"""
Module: test_17_sparta_to_arangodb_pipeline.py
Description: Test SPARTA → ArangoDB cybersecurity data storage pipeline
Level: 1
Modules: SPARTA, ArangoDB, Test Reporter
Expected Bugs: CVE data format issues, bulk storage failures, relationship mapping
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time

class SPARTAToArangoDBPipelineTest(BaseInteractionTest):
    """Level 1: Test SPARTA to ArangoDB pipeline"""
    
    def __init__(self):
        super().__init__(
            test_name="SPARTA to ArangoDB Pipeline",
            level=1,
            modules=["SPARTA", "ArangoDB", "Test Reporter"]
        )
    
    def test_cve_storage_pipeline(self):
        """Test storing CVE data from SPARTA in ArangoDB"""
        self.print_header()
        
        # Import modules
        try:
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
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
        
        # Initialize handlers
        try:
            sparta = SPARTAHandler()
            arango = ArangoDocumentHandler()
            self.record_test("handlers_init", True, {})
        except Exception as e:
            self.add_bug(
                "Handler initialization failed",
                "CRITICAL",
                error=str(e)
            )
            self.record_test("handlers_init", False, {"error": str(e)})
            return
        
        # Test CVEs to process
        test_cves = [
            "CVE-2023-12345",  # Recent CVE
            "CVE-2022-98765",  # Older CVE
            "CVE-2024-11111",  # Very recent
            "CVE-2021-44228",  # Log4j (known critical)
            "CVE-INVALID-ID"   # Invalid format
        ]
        
        stored_cves = []
        
        for cve_id in test_cves:
            print(f"\nProcessing: {cve_id}")
            pipeline_start = time.time()
            
            try:
                # Step 1: Get CVE details from SPARTA
                print(f"Fetching CVE details from SPARTA...")
                
                cve_details = sparta.handle({
                    "operation": "get_cve_details",
                    "cve_id": cve_id
                })
                
                if not cve_details or "error" in cve_details:
                    if "INVALID" not in cve_id:
                        self.add_bug(
                            "Failed to fetch CVE details",
                            "HIGH",
                            cve_id=cve_id,
                            error=cve_details.get("error", "No data returned")
                        )
                    continue
                
                print(f"✅ Got CVE details")
                
                # Validate CVE data structure
                required_fields = ["description", "severity", "published_date"]
                missing_fields = [f for f in required_fields 
                                if f not in cve_details or not cve_details[f]]
                
                if missing_fields:
                    self.add_bug(
                        "Incomplete CVE data from SPARTA",
                        "MEDIUM",
                        cve_id=cve_id,
                        missing_fields=missing_fields
                    )
                
                # Step 2: Enrich with additional data
                print("Enriching CVE data...")
                
                # Get affected products
                affected_products = sparta.handle({
                    "operation": "get_affected_products",
                    "cve_id": cve_id
                })
                
                # Get exploit info
                exploit_info = sparta.handle({
                    "operation": "get_exploit_info",
                    "cve_id": cve_id
                })
                
                # Step 3: Prepare document for ArangoDB
                document = {
                    "_key": cve_id.replace("-", "_"),
                    "cve_id": cve_id,
                    "details": cve_details,
                    "affected_products": affected_products if affected_products and "error" not in affected_products else [],
                    "exploit_info": exploit_info if exploit_info and "error" not in exploit_info else {},
                    "stored_at": time.time(),
                    "data_source": "SPARTA",
                    "enrichment_level": "full"
                }
                
                # Add severity score for indexing
                if "cvss_score" in cve_details:
                    document["severity_score"] = cve_details["cvss_score"]
                elif "severity" in cve_details:
                    # Map text severity to numeric
                    severity_map = {
                        "critical": 10.0,
                        "high": 8.5,
                        "medium": 5.0,
                        "low": 2.0
                    }
                    document["severity_score"] = severity_map.get(
                        cve_details["severity"].lower(), 5.0
                    )
                
                # Step 4: Store in ArangoDB
                print("Storing in ArangoDB...")
                storage_start = time.time()
                
                result = arango.handle({
                    "operation": "create",
                    "collection": "cve_database",
                    "data": document
                })
                
                storage_time = time.time() - storage_start
                
                if result and "error" not in result:
                    print(f"✅ Stored with key: {result.get('_key')}")
                    stored_cves.append(result.get("_key"))
                    
                    self.record_test(f"pipeline_{cve_id}", True, {
                        "fetch_time": storage_start - pipeline_start,
                        "storage_time": storage_time,
                        "total_time": time.time() - pipeline_start,
                        "doc_size": len(str(document))
                    })
                    
                    # Performance check
                    if storage_time > 2:
                        self.add_bug(
                            "Slow CVE storage",
                            "MEDIUM",
                            cve_id=cve_id,
                            duration=f"{storage_time:.2f}s"
                        )
                else:
                    self.add_bug(
                        "Failed to store CVE",
                        "HIGH",
                        cve_id=cve_id,
                        error=result.get("error", "Unknown")
                    )
                    self.record_test(f"storage_{cve_id}", False, {
                        "error": result.get("error")
                    })
                    
            except Exception as e:
                self.add_bug(
                    f"Pipeline exception for {cve_id}",
                    "HIGH",
                    error=str(e)
                )
                self.record_test(f"pipeline_{cve_id}", False, {"error": str(e)})
        
        # Test retrieval and relationships
        if stored_cves:
            self.test_cve_relationships(arango, stored_cves)
    
    def test_cve_relationships(self, arango, stored_cves):
        """Test creating relationships between CVEs"""
        print("\n\nTesting CVE Relationships...")
        
        try:
            # Create edge collection for relationships
            arango.handle({
                "operation": "create_collection",
                "collection": "cve_relationships",
                "type": "edge"
            })
            
            # Find CVEs with common characteristics
            print("Analyzing CVE similarities...")
            
            relationships_created = 0
            
            for i, cve1 in enumerate(stored_cves):
                for cve2 in stored_cves[i+1:]:
                    # Get both CVEs
                    doc1 = arango.handle({
                        "operation": "get",
                        "collection": "cve_database",
                        "key": cve1
                    })
                    
                    doc2 = arango.handle({
                        "operation": "get",
                        "collection": "cve_database",
                        "key": cve2
                    })
                    
                    if doc1 and doc2:
                        doc1 = doc1.get("document", {})
                        doc2 = doc2.get("document", {})
                        
                        # Check for similarities
                        similarity_reasons = []
                        
                        # Similar severity
                        if abs(doc1.get("severity_score", 0) - doc2.get("severity_score", 0)) < 2:
                            similarity_reasons.append("similar_severity")
                        
                        # Same year
                        date1 = doc1.get("details", {}).get("published_date", "")
                        date2 = doc2.get("details", {}).get("published_date", "")
                        if date1[:4] == date2[:4] and date1[:4]:
                            similarity_reasons.append("same_year")
                        
                        # Common affected products
                        products1 = set(p.get("name", "") for p in doc1.get("affected_products", []))
                        products2 = set(p.get("name", "") for p in doc2.get("affected_products", []))
                        if products1 & products2:  # Intersection
                            similarity_reasons.append("common_products")
                        
                        # Create relationship if similarities found
                        if similarity_reasons:
                            edge_result = arango.handle({
                                "operation": "create",
                                "collection": "cve_relationships",
                                "data": {
                                    "_from": f"cve_database/{cve1}",
                                    "_to": f"cve_database/{cve2}",
                                    "type": "similar",
                                    "reasons": similarity_reasons,
                                    "created_at": time.time()
                                }
                            })
                            
                            if edge_result and "error" not in edge_result:
                                relationships_created += 1
            
            print(f"✅ Created {relationships_created} relationships")
            
            self.record_test("cve_relationships", True, {
                "cves_analyzed": len(stored_cves),
                "relationships_created": relationships_created
            })
            
            # Check relationship quality
            if relationships_created == 0 and len(stored_cves) > 2:
                self.add_bug(
                    "No relationships found between CVEs",
                    "MEDIUM",
                    cves_analyzed=len(stored_cves)
                )
                
        except Exception as e:
            self.add_bug(
                "Exception in relationship creation",
                "HIGH",
                error=str(e)
            )
            self.record_test("cve_relationships", False, {"error": str(e)})
    
    def test_threat_intelligence_storage(self):
        """Test storing threat intelligence data"""
        print("\n\nTesting Threat Intelligence Storage...")
        
        try:
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            from arangodb_handlers.real_arangodb_handlers import ArangoDocumentHandler
            
            sparta = SPARTAHandler()
            arango = ArangoDocumentHandler()
            
            # Test threat actors
            threat_actors = ["Lazarus", "APT28", "APT29", "Carbanak"]
            
            for actor in threat_actors:
                print(f"\nProcessing threat actor: {actor}")
                
                # Get threat actor info
                actor_info = sparta.handle({
                    "operation": "get_threat_actor_info",
                    "actor": actor
                })
                
                if actor_info and "error" not in actor_info:
                    # Store in ArangoDB
                    document = {
                        "_key": actor.lower().replace(" ", "_"),
                        "name": actor,
                        "info": actor_info,
                        "type": "threat_actor",
                        "stored_at": time.time()
                    }
                    
                    result = arango.handle({
                        "operation": "create",
                        "collection": "threat_intelligence",
                        "data": document
                    })
                    
                    if result and "error" not in result:
                        print(f"✅ Stored threat actor: {actor}")
                        
                        # Link to related CVEs
                        if "associated_cves" in actor_info:
                            for cve in actor_info["associated_cves"]:
                                edge_result = arango.handle({
                                    "operation": "create",
                                    "collection": "threat_relationships",
                                    "data": {
                                        "_from": f"threat_intelligence/{document['_key']}",
                                        "_to": f"cve_database/{cve.replace('-', '_')}",
                                        "type": "exploits",
                                        "confidence": 0.8
                                    }
                                })
                    else:
                        self.add_bug(
                            "Failed to store threat actor",
                            "HIGH",
                            actor=actor,
                            error=result.get("error")
                        )
                else:
                    print(f"❌ No data for threat actor: {actor}")
            
            self.record_test("threat_intelligence_storage", True, {
                "actors_processed": len(threat_actors)
            })
            
        except Exception as e:
            self.add_bug(
                "Exception in threat intelligence storage",
                "HIGH",
                error=str(e)
            )
            self.record_test("threat_intelligence", False, {"error": str(e)})
    
    def run_tests(self):
        """Run all tests"""
        self.test_cve_storage_pipeline()
        self.test_threat_intelligence_storage()
        return self.generate_report()


def main():
    """Run the test"""
    tester = SPARTAToArangoDBPipelineTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)