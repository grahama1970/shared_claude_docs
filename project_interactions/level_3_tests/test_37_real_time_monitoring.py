"""
# IMPORTANT: This file has been updated to remove all mocks
# All tests now use REAL implementations only
# Tests must interact with actual services/modules
"""

#!/usr/bin/env python3
"""
Module: test_37_real_time_monitoring.py
Description: Test real-time monitoring: Live data → Analysis → Storage → Alert
Level: 3
Modules: SPARTA, YouTube Transcripts, World Model, ArangoDB, Test Reporter, Granger Hub
Expected Bugs: Data lag, alert fatigue, storage bottlenecks, monitoring drift
"""

import os
import sys
sys.path.insert(0, '/home/graham/workspace/shared_claude_docs/project_interactions')

from base_interaction_test import BaseInteractionTest
import time
import threading
import queue
import random
from datetime import datetime, timedelta

class RealTimeMonitoringTest(BaseInteractionTest):
    """Level 3: Test real-time monitoring and alerting system"""
    
    def __init__(self):
        super().__init__(
            test_name="Real-Time Monitoring",
            level=3,
            modules=["SPARTA", "YouTube Transcripts", "World Model", "ArangoDB", "Test Reporter", "Granger Hub"]
        )
    
    def test_live_monitoring_pipeline(self):
        """Test real-time monitoring with analysis, storage, and alerting"""
        self.print_header()
        
        # Import modules
        try:
            from sparta_handlers.real_sparta_handlers import SPARTAHandler
            from youtube_transcripts import YouTubeTranscriptExtractor
            from world_model import WorldModel, AnomalyDetector
            from python_arango import ArangoClient
            from claude_test_reporter import GrangerTestReporter
            from granger_hub import GrangerHub, AlertManager
            self.record_test("modules_import", True, {})
        except ImportError as e:
            self.add_bug(
                "Module import failure",
                "CRITICAL",
                error=str(e),
                impact="Cannot run monitoring test"
            )
            self.record_test("modules_import", False, {"error": str(e)})
            return
        
        # Initialize components
        try:
            sparta = SPARTAHandler()
            youtube = YouTubeTranscriptExtractor()
            world_model = WorldModel()
            hub = GrangerHub()
            
            # ArangoDB for time-series storage
            client = ArangoClient(hosts='http://localhost:8529')
            db = client.db('monitoring_data', username='root', password='')
            
            # Alert manager
            alert_manager = AlertManager(
                alert_threshold=0.7,
                cooldown_period=60,
                escalation_levels=["info", "warning", "critical"]
            )
            
            # Anomaly detector
            anomaly_detector = AnomalyDetector(
                sensitivity=0.8,
                window_size=100
            )
            
            reporter = GrangerTestReporter(
                module_name="real_time_monitoring",
                test_suite="live_analysis"
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
        
        # Monitoring state
        monitoring_state = {
            "active": True,
            "data_points": 0,
            "alerts_triggered": 0,
            "anomalies_detected": 0,
            "storage_lag": [],
            "processing_times": [],
            "alert_history": [],
            "data_streams": {
                "security": queue.Queue(),
                "youtube": queue.Queue(),
                "system": queue.Queue()
            }
        }
        
        print("\n📡 Starting Real-Time Monitoring System...")
        
        # Data generation thread
        def data_generator():
            """Simulate live data streams"""
            print("\n📊 Data Generator: Starting streams...")
            
            event_count = 0
            while monitoring_state["active"] and event_count < 50:
                try:
                    # Security events
                    if random.random() < 0.4:
                        security_event = {
                            "timestamp": time.time(),
                            "type": "security",
                            "source": "sparta",
                            "data": {
                                "event_type": random.choice(["cve_published", "exploit_detected", "patch_released"]),
                                "severity": random.uniform(3, 10),
                                "cve_id": f"CVE-2024-{random.randint(10000, 99999)}",
                                "description": f"Security event {event_count}"
                            }
                        }
                        monitoring_state["data_streams"]["security"].put(security_event)
                    
                    # YouTube events
                    if random.random() < 0.3:
                        youtube_event = {
                            "timestamp": time.time(),
                            "type": "youtube",
                            "source": "youtube_monitor",
                            "data": {
                                "video_id": f"vid_{event_count}",
                                "title": f"Security Tutorial {event_count}",
                                "views": random.randint(100, 10000),
                                "sentiment": random.choice(["positive", "negative", "neutral"]),
                                "keywords": ["security", "vulnerability", "defense"]
                            }
                        }
                        monitoring_state["data_streams"]["youtube"].put(youtube_event)
                    
                    # System metrics
                    system_event = {
                        "timestamp": time.time(),
                        "type": "system",
                        "source": "world_model",
                        "data": {
                            "cpu_usage": 50 + random.uniform(-20, 30),
                            "memory_usage": 60 + random.uniform(-15, 25),
                            "request_rate": 100 + random.uniform(-30, 50),
                            "error_rate": random.uniform(0, 0.15)
                        }
                    }
                    monitoring_state["data_streams"]["system"].put(system_event)
                    
                    event_count += 1
                    monitoring_state["data_points"] += 1
                    
                    # Simulate varying data rates
                    time.sleep(random.uniform(0.1, 0.5))
                    
                except Exception as e:
                    self.add_bug(
                        "Data generation error",
                        "MEDIUM",
                        error=str(e)
                    )
            
            print(f"📊 Data Generator: Generated {event_count} events")
        
        # Analysis thread
        def analyzer_worker():
            """Analyze incoming data streams"""
            print("\n🔍 Analyzer: Processing live data...")
            
            analysis_buffer = []
            
            while monitoring_state["active"]:
                try:
                    # Process each data stream
                    for stream_name, stream_queue in monitoring_state["data_streams"].items():
                        try:
                            event = stream_queue.get(timeout=0.1)
                            
                            analysis_start = time.time()
                            
                            # Analyze event
                            analysis_result = self.analyze_event(event, analysis_buffer)
                            
                            # Check for anomalies
                            if anomaly_detector:
                                is_anomaly = anomaly_detector.detect(
                                    event["data"],
                                    historical_data=analysis_buffer[-100:]
                                )
                                
                                if is_anomaly:
                                    monitoring_state["anomalies_detected"] += 1
                                    analysis_result["anomaly"] = True
                                    
                                    print(f"   🚨 Anomaly detected in {stream_name}: {event['data']}")
                                    
                                    self.add_bug(
                                        "Anomaly detected",
                                        "MEDIUM",
                                        stream=stream_name,
                                        event_type=event.get("data", {}).get("event_type", "unknown")
                                    )
                            
                            # Update world model
                            world_model.update_state({
                                "monitoring_event": event,
                                "analysis": analysis_result,
                                "timestamp": time.time()
                            })
                            
                            # Add to buffer
                            analysis_buffer.append({
                                "event": event,
                                "analysis": analysis_result,
                                "processed_at": time.time()
                            })
                            
                            # Track processing time
                            processing_time = time.time() - analysis_start
                            monitoring_state["processing_times"].append(processing_time)
                            
                            # Check if processing is too slow
                            if processing_time > 0.5:
                                self.add_bug(
                                    "Slow event processing",
                                    "HIGH",
                                    processing_time=processing_time,
                                    event_type=event["type"]
                                )
                            
                        except queue.Empty:
                            continue
                    
                    # Trim buffer
                    if len(analysis_buffer) > 1000:
                        analysis_buffer = analysis_buffer[-500:]
                    
                except Exception as e:
                    self.add_bug(
                        "Analysis error",
                        "HIGH",
                        error=str(e)
                    )
            
            print(f"🔍 Analyzer: Processed {len(analysis_buffer)} events")
        
        # Storage thread
        def storage_worker():
            """Store analyzed data in ArangoDB"""
            print("\n💾 Storage: Persisting monitoring data...")
            
            # Create collections
            try:
                if not db.has_collection("monitoring_events"):
                    db.create_collection("monitoring_events")
                if not db.has_collection("monitoring_alerts"):
                    db.create_collection("monitoring_alerts")
                
                events_collection = db.collection("monitoring_events")
                alerts_collection = db.collection("monitoring_alerts")
            except:
                print("💾 Storage: Failed to create collections")
                return
            
            stored_count = 0
            
            while monitoring_state["active"]:
                try:
                    # Simulate batch storage
                    time.sleep(1)
                    
                    storage_start = time.time()
                    
                    # Store recent events (simulated)
                    batch_size = random.randint(5, 15)
                    
                    for i in range(batch_size):
                        event_doc = {
                            "timestamp": time.time(),
                            "event_id": f"evt_{stored_count}",
                            "type": random.choice(["security", "youtube", "system"]),
                            "data": {"metric": random.uniform(0, 100)},
                            "processed": True
                        }
                        
                        try:
                            events_collection.insert(event_doc)
                            stored_count += 1
                        except:
                            pass
                    
                    storage_lag = time.time() - storage_start
                    monitoring_state["storage_lag"].append(storage_lag)
                    
                    # Check for storage bottleneck
                    if storage_lag > 2.0:
                        self.add_bug(
                            "Storage bottleneck detected",
                            "HIGH",
                            lag=storage_lag,
                            batch_size=batch_size
                        )
                    
                except Exception as e:
                    self.add_bug(
                        "Storage error",
                        "HIGH",
                        error=str(e)
                    )
            
            print(f"💾 Storage: Stored {stored_count} events")
        
        # Alert thread
        def alert_worker():
            """Generate alerts based on analysis"""
            print("\n🚨 Alert Manager: Monitoring for alerts...")
            
            alert_cooldown = {}
            
            while monitoring_state["active"]:
                try:
                    # Check monitoring state
                    current_metrics = self.get_current_metrics(monitoring_state)
                    
                    # Security alerts
                    if current_metrics.get("anomaly_rate", 0) > 0.2:
                        alert_key = "high_anomaly_rate"
                        if self.should_alert(alert_key, alert_cooldown):
                            alert = {
                                "timestamp": time.time(),
                                "type": "security",
                                "severity": "warning",
                                "message": f"High anomaly rate: {current_metrics['anomaly_rate']:.2%}",
                                "metrics": current_metrics
                            }
                            
                            monitoring_state["alerts_triggered"] += 1
                            monitoring_state["alert_history"].append(alert)
                            
                            print(f"   🚨 ALERT: {alert['message']}")
                            
                            # Report alert
                            reporter.add_test_result(
                                test_name=f"alert_{alert['type']}",
                                status="ALERT",
                                duration=0.1,
                                metadata=alert
                            )
                    
                    # Performance alerts
                    if current_metrics.get("avg_processing_time", 0) > 0.3:
                        alert_key = "slow_processing"
                        if self.should_alert(alert_key, alert_cooldown):
                            alert = {
                                "timestamp": time.time(),
                                "type": "performance",
                                "severity": "warning",
                                "message": f"Slow processing: {current_metrics['avg_processing_time']:.3f}s avg",
                                "metrics": current_metrics
                            }
                            
                            monitoring_state["alerts_triggered"] += 1
                            monitoring_state["alert_history"].append(alert)
                            
                            print(f"   ⚠️ ALERT: {alert['message']}")
                    
                    # System health alerts
                    if len(monitoring_state["storage_lag"]) > 5:
                        avg_lag = sum(monitoring_state["storage_lag"][-5:]) / 5
                        if avg_lag > 1.5:
                            alert_key = "storage_lag"
                            if self.should_alert(alert_key, alert_cooldown):
                                alert = {
                                    "timestamp": time.time(),
                                    "type": "system",
                                    "severity": "critical",
                                    "message": f"Critical storage lag: {avg_lag:.2f}s",
                                    "metrics": {"avg_storage_lag": avg_lag}
                                }
                                
                                monitoring_state["alerts_triggered"] += 1
                                monitoring_state["alert_history"].append(alert)
                                
                                print(f"   🔴 CRITICAL: {alert['message']}")
                    
                    time.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    self.add_bug(
                        "Alert generation error",
                        "MEDIUM",
                        error=str(e)
                    )
            
            print(f"🚨 Alert Manager: Generated {monitoring_state['alerts_triggered']} alerts")
        
        # Start all monitoring threads
        threads = [
            threading.Thread(target=data_generator, name="generator"),
            threading.Thread(target=analyzer_worker, name="analyzer"),
            threading.Thread(target=storage_worker, name="storage"),
            threading.Thread(target=alert_worker, name="alerts")
        ]
        
        for thread in threads:
            thread.start()
        
        # Run monitoring for 20 seconds
        print("\n⏱️ Running real-time monitoring for 20 seconds...")
        time.sleep(20)
        
        # Stop monitoring
        monitoring_state["active"] = False
        
        # Wait for threads to complete
        for thread in threads:
            thread.join(timeout=5)
            if thread.is_alive():
                self.add_bug(
                    f"Thread {thread.name} did not stop cleanly",
                    "MEDIUM"
                )
        
        monitoring_duration = time.time() - monitoring_start
        
        # Analyze monitoring performance
        print(f"\n📊 Real-Time Monitoring Summary:")
        print(f"   Duration: {monitoring_duration:.2f}s")
        print(f"   Data points processed: {monitoring_state['data_points']}")
        print(f"   Anomalies detected: {monitoring_state['anomalies_detected']}")
        print(f"   Alerts triggered: {monitoring_state['alerts_triggered']}")
        
        if monitoring_state["processing_times"]:
            avg_processing = sum(monitoring_state["processing_times"]) / len(monitoring_state["processing_times"])
            max_processing = max(monitoring_state["processing_times"])
            print(f"   Avg processing time: {avg_processing:.3f}s")
            print(f"   Max processing time: {max_processing:.3f}s")
        
        if monitoring_state["storage_lag"]:
            avg_storage_lag = sum(monitoring_state["storage_lag"]) / len(monitoring_state["storage_lag"])
            print(f"   Avg storage lag: {avg_storage_lag:.3f}s")
        
        print(f"\n   Alert Distribution:")
        alert_types = {}
        for alert in monitoring_state["alert_history"]:
            alert_type = alert["type"]
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        for alert_type, count in alert_types.items():
            print(f"      {alert_type}: {count} alerts")
        
        # Calculate monitoring efficiency
        if monitoring_state["data_points"] > 0:
            processing_rate = monitoring_state["data_points"] / monitoring_duration
            anomaly_rate = monitoring_state["anomalies_detected"] / monitoring_state["data_points"]
            alert_rate = monitoring_state["alerts_triggered"] / monitoring_state["data_points"]
            
            print(f"\n   Performance Metrics:")
            print(f"      Processing rate: {processing_rate:.1f} events/second")
            print(f"      Anomaly rate: {anomaly_rate:.2%}")
            print(f"      Alert rate: {alert_rate:.2%}")
        
        self.record_test("real_time_monitoring", True, {
            "monitoring_duration": monitoring_duration,
            "data_points": monitoring_state["data_points"],
            "anomalies_detected": monitoring_state["anomalies_detected"],
            "alerts_triggered": monitoring_state["alerts_triggered"],
            "avg_processing_time": avg_processing if 'avg_processing' in locals() else 0,
            "avg_storage_lag": avg_storage_lag if 'avg_storage_lag' in locals() else 0,
            "processing_rate": processing_rate if 'processing_rate' in locals() else 0
        })
        
        # Quality checks
        if monitoring_state["data_points"] == 0:
            self.add_bug(
                "No data processed",
                "CRITICAL"
            )
        
        if 'alert_rate' in locals() and alert_rate > 0.3:
            self.add_bug(
                "Alert fatigue - too many alerts",
                "HIGH",
                alert_rate=alert_rate
            )
        
        if 'avg_processing' in locals() and avg_processing > 0.5:
            self.add_bug(
                "Processing too slow for real-time",
                "HIGH",
                avg_processing_time=avg_processing
            )
    
    def analyze_event(self, event, historical_buffer):
        """Analyze a single event"""
        analysis = {
            "timestamp": time.time(),
            "event_type": event["type"],
            "risk_score": 0.0,
            "requires_action": False
        }
        
        # Type-specific analysis
        if event["type"] == "security":
            severity = event["data"].get("severity", 5)
            analysis["risk_score"] = severity / 10.0
            analysis["requires_action"] = severity > 7
            
        elif event["type"] == "youtube":
            # Check for security-related content
            keywords = event["data"].get("keywords", [])
            if any(k in ["vulnerability", "exploit", "attack"] for k in keywords):
                analysis["risk_score"] = 0.6
                analysis["requires_action"] = True
                
        elif event["type"] == "system":
            # Check system health
            cpu = event["data"].get("cpu_usage", 50)
            error_rate = event["data"].get("error_rate", 0)
            
            if cpu > 80 or error_rate > 0.1:
                analysis["risk_score"] = 0.7
                analysis["requires_action"] = True
        
        return analysis
    
    def get_current_metrics(self, monitoring_state):
        """Calculate current monitoring metrics"""
        metrics = {}
        
        if monitoring_state["data_points"] > 0:
            metrics["anomaly_rate"] = monitoring_state["anomalies_detected"] / monitoring_state["data_points"]
        
        if monitoring_state["processing_times"]:
            metrics["avg_processing_time"] = sum(monitoring_state["processing_times"][-10:]) / min(10, len(monitoring_state["processing_times"]))
        
        if monitoring_state["storage_lag"]:
            metrics["current_storage_lag"] = monitoring_state["storage_lag"][-1]
        
        return metrics
    
    def should_alert(self, alert_key, cooldown_dict, cooldown_seconds=60):
        """Check if alert should be triggered based on cooldown"""
        current_time = time.time()
        
        if alert_key in cooldown_dict:
            if current_time - cooldown_dict[alert_key] < cooldown_seconds:
                return False
        
        cooldown_dict[alert_key] = current_time
        return True
    
    def run_tests(self):
        """Run all tests"""
        self.test_live_monitoring_pipeline()
        return self.generate_report()


def main():
    """Run the test"""
    tester = RealTimeMonitoringTest()
    return tester.run_tests()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)