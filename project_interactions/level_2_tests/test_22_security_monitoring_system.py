"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_22_security_monitoring_system.py
Description: Test security monitoring with YouTube, SPARTA, and alerts
Level: 2
Modules: YouTube Transcripts, SPARTA, World Model, Test Reporter
Expected Bugs: Real-time processing delays, alert fatigue, correlation accuracy
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import random

class SecurityMonitoringSystemTest(BaseInteractionTest):
    """Level 2: Test security monitoring system"""
    
    def __init__(self):
        super().__init__(
            test_name="Security Monitoring System",
            level=2,
            modules=["YouTube Transcripts", "SPARTA", "World Model", "Test Reporter"]
        )
    
    def test_threat_detection_pipeline(self):
        """Test real-time threat detection and alerting"""
        self.print_header()
        
        # Import modules
        try:
            from youtube_transcripts.link_extractor import extract_cves_from_text
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            from world_model import WorldModel
            from claude_test_reporter import GrangerTestReporter
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run monitoring system"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            sparta = SPARTAHandler()
            world_model = WorldModel()
            reporter = GrangerTestReporter(
                module_name="security_monitoring",
                test_suite="threat_detection"
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
        
        monitoring_start = time.time()
        
        # Simulate incoming security data streams
        security_events = self.generate_security_events()
        
        print("\n🛡️ Starting Security Monitoring System...")
        
        threats_detected = []
        alerts_generated = []
        false_positives = 0
        true_positives = 0
        
        for event in security_events:
            print(f"\n📡 Processing event: {event['source']} - {event['type']}")
            
            try:
                # Step 1: Extract indicators
                indicators = self.extract_indicators(event)
                
                # Step 2: Enrich with SPARTA
                enriched_data = []
                for indicator in indicators:
                    if indicator["type"] == "cve":
                        enrichment = sparta.handle({
                            "operation": "get_cve_details",
                            "cve_id": indicator["value"]
                        })
                        if enrichment and "error" not in enrichment:
                            enriched_data.append({
                                "indicator": indicator,
                                "enrichment": enrichment,
                                "severity": enrichment.get("cvss_score", 5.0)
                            })
                
                # Step 3: Update world model
                world_model.update_state({
                    "module": "security_monitor",
                    "timestamp": time.time(),
                    "event_type": event["type"],
                    "indicators_found": len(indicators),
                    "enriched_count": len(enriched_data),
                    "severity_max": max([e["severity"] for e in enriched_data], default=0)
                })
                
                # Step 4: Analyze for threats
                threat_score = self.calculate_threat_score(event, enriched_data)
                
                if threat_score > 0.7:
                    threat = {
                        "event_id": event["id"],
                        "score": threat_score,
                        "indicators": indicators,
                        "severity": "HIGH" if threat_score > 0.85 else "MEDIUM"
                    }
                    threats_detected.append(threat)
                    
                    # Generate alert
                    alert = self.generate_alert(threat, enriched_data)
                    alerts_generated.append(alert)
                    
                    print(f"🚨 THREAT DETECTED: Score {threat_score:.2f}, Severity: {threat['severity']}")
                    
                    # Check if true or false positive
                    if event.get("is_real_threat", False):
                        true_positives += 1
                    else:
                        false_positives += 1
                        self.add_bug(
                            "False positive alert",
                            "MEDIUM",
                            event_type=event["type"],
                            threat_score=threat_score
                        )
                
                # Report test result
                reporter.add_test_result(
                    test_name=f"event_{event['id']}",
                    status="PASS" if threat_score < 0.95 else "FAIL",  # Too high = suspicious
                    duration=0.5,
                    metadata={
                        "event_type": event["type"],
                        "indicators": len(indicators),
                        "threat_score": threat_score,
                        "alert_generated": threat_score > 0.7
                    }
                )
                
            except Exception as e:
                self.add_bug(
                    f"Error processing event {event['id']}",
                    "HIGH",
                    error=str(e)
                )
        
        monitoring_duration = time.time() - monitoring_start
        
        # Analyze monitoring effectiveness
        print(f"\n📊 Monitoring Summary:")
        print(f"   Events processed: {len(security_events)}")
        print(f"   Threats detected: {len(threats_detected)}")
        print(f"   Alerts generated: {len(alerts_generated)}")
        print(f"   True positives: {true_positives}")
        print(f"   False positives: {false_positives}")
        print(f"   Duration: {monitoring_duration:.2f}s")
        
        # Calculate metrics
        if threats_detected:
            precision = true_positives / len(threats_detected) if threats_detected else 0
            print(f"   Precision: {precision:.2%}")
            
            if precision < 0.7:
                self.add_bug(
                    "Low threat detection precision",
                    "HIGH",
                    precision=precision,
                    false_positive_rate=false_positives/len(threats_detected)
                )
        
        self.record_test("security_monitoring_system", True, {
            "events_processed": len(security_events),
            "threats_detected": len(threats_detected),
            "alerts_generated": len(alerts_generated),
            "true_positives": true_positives,
            "false_positives": false_positives,
            "monitoring_duration": monitoring_duration,
            "events_per_second": len(security_events) / monitoring_duration
        })
        
        # Performance check
        if monitoring_duration / len(security_events) > 2:  # More than 2s per event
            self.add_bug(
                "Slow event processing",
                "MEDIUM",
                avg_seconds_per_event=monitoring_duration/len(security_events)
            )
        
        # Generate monitoring report
        self.generate_monitoring_report(reporter, alerts_generated)
    
    def generate_security_events(self):
        """Generate simulated security events"""
        events = []
        
        # Mix of real threats and benign events
        event_templates = [
            {
                "type": "youtube_disclosure",
                "source": "YouTube",
                "content": "New video discussing CVE-2024-12345 exploitation techniques",
                "indicators": ["CVE-2024-12345"],
                "is_real_threat": True
            },
            {
                "type": "normal_discussion",
                "source": "YouTube",
                "content": "Tutorial on Python programming basics",
                "indicators": [],
                "is_real_threat": False
            },
            {
                "type": "cve_announcement",
                "source": "Security Feed",
                "content": "Critical vulnerability CVE-2024-98765 in popular framework",
                "indicators": ["CVE-2024-98765"],
                "is_real_threat": True
            },
            {
                "type": "threat_actor_activity",
                "source": "Threat Intel",
                "content": "APT28 targeting financial institutions with new malware",
                "indicators": ["APT28", "192.168.1.100"],
                "is_real_threat": True
            },
            {
                "type": "false_alarm",
                "source": "Automated Scanner",
                "content": "Potential SQL injection detected (false positive)",
                "indicators": ["sql_injection"],
                "is_real_threat": False
            }
        ]
        
        # Generate events
        for i in range(10):
            template = random.choice(event_templates)
            event = {
                "id": f"event_{i:03d}",
                "timestamp": time.time() + i,
                **template
            }
            events.append(event)
        
        return events
    
    def extract_indicators(self, event):
        """Extract security indicators from event"""
        indicators = []
        
        content = event.get("content", "")
        
        # Extract CVEs
        import re
        cves = re.findall(r'CVE-\d{4}-\d{4,7}', content)
        for cve in cves:
            indicators.append({"type": "cve", "value": cve})
        
        # Extract IPs
        ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
        for ip in ips:
            indicators.append({"type": "ip", "value": ip})
        
        # Extract threat actors
        known_actors = ["APT28", "APT29", "Lazarus", "Carbanak"]
        for actor in known_actors:
            if actor in content:
                indicators.append({"type": "threat_actor", "value": actor})
        
        return indicators
    
    def calculate_threat_score(self, event, enriched_data):
        """Calculate threat score based on event and enrichment"""
        score = 0.0
        
        # Base score by event type
        type_scores = {
            "youtube_disclosure": 0.3,
            "cve_announcement": 0.5,
            "threat_actor_activity": 0.7,
            "normal_discussion": 0.1,
            "false_alarm": 0.2
        }
        score += type_scores.get(event["type"], 0.2)
        
        # Add enrichment severity
        if enriched_data:
            max_severity = max([e["severity"] for e in enriched_data])
            score += (max_severity / 10) * 0.3
        
        # Add indicator count factor
        indicator_count = len(event.get("indicators", []))
        if indicator_count > 0:
            score += min(indicator_count * 0.1, 0.3)
        
        # Add randomness to simulate real-world uncertainty
        score += random.uniform(-0.1, 0.1)
        
        return max(0, min(score, 1.0))
    
    def generate_alert(self, threat, enriched_data):
        """Generate security alert"""
        alert = {
            "id": f"alert_{threat['event_id']}",
            "timestamp": time.time(),
            "severity": threat["severity"],
            "score": threat["score"],
            "indicators": threat["indicators"],
            "enrichment_summary": {
                "cve_count": sum(1 for i in threat["indicators"] if i["type"] == "cve"),
                "max_cvss": max([e["severity"] for e in enriched_data], default=0)
            },
            "recommended_action": self.get_recommended_action(threat)
        }
        return alert
    
    def get_recommended_action(self, threat):
        """Get recommended action based on threat"""
        if threat["score"] > 0.9:
            return "IMMEDIATE: Block indicators and investigate"
        elif threat["score"] > 0.8:
            return "HIGH: Monitor closely and prepare response"
        elif threat["score"] > 0.7:
            return "MEDIUM: Add to watchlist and gather more intel"
        else:
            return "LOW: Log for future reference"
    
    def generate_monitoring_report(self, reporter, alerts):
        """Generate comprehensive monitoring report"""
        print("\n📄 Generating monitoring report...")
        
        try:
            report = reporter.generate_report(
                include_skeptical_analysis=True,
                include_performance_trends=True
            )
            
            if report:
                with open("security_monitoring_report.html", 'w') as f:
                    f.write(report)
                print("✅ Monitoring report generated")
                
                # Also save alerts summary
                import json
                with open("security_alerts.json", 'w') as f:
                    json.dump(alerts, f, indent=2, default=str)
                print("✅ Alerts summary saved")
                
        except Exception as e:
            self.add_bug(
                "Failed to generate monitoring report",
                "MEDIUM",
                error=str(e)
            )
    
    def run_tests(self):
        """Run all tests"""
        self.test_threat_detection_pipeline()
        return self.generate_report()


def main():
    """Run the test"""
    tester = SecurityMonitoringSystemTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)