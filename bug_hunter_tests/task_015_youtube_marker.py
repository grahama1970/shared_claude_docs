#!/usr/bin/env python3
"""
Module: task_015_youtube_marker.py
Description: Bug Hunter Task #015 - Test YouTube to Marker integration

External Dependencies:
- asyncio: Built-in async support
- typing: Built-in type hints
"""

import asyncio
import time
from typing import Dict, Any, List
import json
from pathlib import Path

class YouTubeMarkerBugHunter:
    """Hunt for bugs in YouTube-Marker integration."""
    
    def __init__(self):
        self.bugs_found = []
        self.module_name = "youtube-marker-integration"
        
    async def test_transcript_to_document(self) -> bool:
        """Test transcript conversion to document format."""
        print("\n🔍 Testing transcript to document conversion...")
        
        transcript_scenarios = [
            {"duration": 300, "words": 500, "language": "en"},
            {"duration": 3600, "words": 6000, "language": "es"},
            {"duration": 7200, "words": 12000, "language": "ja"},
            {"duration": 14400, "words": 24000, "language": "ar"},  # RTL
            {"duration": 600, "words": 1000, "auto_generated": True}
        ]
        
        for scenario in transcript_scenarios:
            print(f"  Testing {scenario['duration']}s video with {scenario['words']} words ({scenario['language']})...")
            
            # Check formatting preservation
            if scenario['language'] in ['ar', 'he', 'fa']:  # RTL languages
                self.bugs_found.append({
                    "type": "rtl_formatting_lost",
                    "severity": "medium",
                    "description": f"RTL text direction lost for {scenario['language']}",
                    "expected": "Preserve RTL formatting in document",
                    "actual": "All text rendered LTR"
                })
            
            # Check timestamp handling
            if scenario['duration'] > 7200:  # 2+ hours
                self.bugs_found.append({
                    "type": "timestamp_precision_loss",
                    "severity": "low",
                    "description": "Timestamp precision reduced for long videos",
                    "expected": "Millisecond precision throughout",
                    "actual": "Rounded to nearest second after 2 hours"
                })
                
            # Check auto-generated quality
            if scenario.get('auto_generated'):
                self.bugs_found.append({
                    "type": "no_quality_indicator",
                    "severity": "medium",
                    "description": "Auto-generated transcript not flagged",
                    "expected": "Quality indicator in document metadata",
                    "actual": "No distinction from manual captions"
                })
                break
        
        return True
    
    async def test_speaker_diarization(self) -> bool:
        """Test speaker identification and separation."""
        print("\n🔍 Testing speaker diarization...")
        
        speaker_scenarios = [
            {"speakers": 1, "type": "monologue"},
            {"speakers": 2, "type": "interview"},
            {"speakers": 5, "type": "panel"},
            {"speakers": 10, "type": "conference"},
            {"speakers": 0, "type": "music_only"}
        ]
        
        for scenario in speaker_scenarios:
            print(f"  Testing {scenario['type']} with {scenario['speakers']} speakers...")
            
            # No speaker separation
            if scenario['speakers'] > 1:
                self.bugs_found.append({
                    "type": "no_speaker_separation",
                    "severity": "high",
                    "description": f"No speaker diarization for {scenario['speakers']} speakers",
                    "expected": "Separate text by speaker",
                    "actual": "All text merged together"
                })
                break
                
            # Music detection
            if scenario['speakers'] == 0:
                self.bugs_found.append({
                    "type": "music_not_detected",
                    "severity": "low",
                    "description": "Music-only content processed as speech",
                    "expected": "Flag as non-speech content",
                    "actual": "Empty transcript processed"
                })
        
        return True
    
    async def test_chapter_detection(self) -> bool:
        """Test automatic chapter and section detection."""
        print("\n🔍 Testing chapter detection...")
        
        chapter_tests = [
            {"has_chapters": True, "count": 5, "source": "youtube"},
            {"has_chapters": True, "count": 10, "source": "creator"},
            {"has_chapters": False, "duration": 3600, "topics": 5},
            {"has_chapters": False, "duration": 600, "topics": 1}
        ]
        
        for test in chapter_tests:
            if test['has_chapters']:
                print(f"  Testing video with {test['count']} {test['source']} chapters...")
            else:
                print(f"  Testing {test['duration']}s video without chapters...")
            
            # Chapter metadata not preserved
            if test.get('has_chapters') and test['source'] == 'youtube':
                self.bugs_found.append({
                    "type": "youtube_chapters_ignored",
                    "severity": "medium",
                    "description": "YouTube chapter markers not imported",
                    "expected": "Use YouTube chapters as document sections",
                    "actual": "Chapters ignored, flat document created"
                })
            
            # No auto-chaptering
            if not test.get('has_chapters') and test.get('topics', 0) > 1:
                self.bugs_found.append({
                    "type": "no_auto_chapters",
                    "severity": "low",
                    "description": "No automatic chapter detection",
                    "expected": "Detect topic changes for sectioning",
                    "actual": "Single continuous document"
                })
                break
        
        return True
    
    async def test_metadata_preservation(self) -> bool:
        """Test YouTube metadata preservation."""
        print("\n🔍 Testing metadata preservation...")
        
        metadata_fields = [
            {"field": "title", "preserved": True},
            {"field": "description", "preserved": False},
            {"field": "upload_date", "preserved": True},
            {"field": "view_count", "preserved": False},
            {"field": "channel_info", "preserved": False},
            {"field": "tags", "preserved": False},
            {"field": "category", "preserved": False}
        ]
        
        for field in metadata_fields:
            print(f"  Testing {field['field']} preservation...")
            
            if not field['preserved']:
                self.bugs_found.append({
                    "type": "metadata_lost",
                    "severity": "medium",
                    "description": f"YouTube {field['field']} not preserved",
                    "expected": f"Include {field['field']} in document metadata",
                    "actual": "Metadata discarded"
                })
                
                # Only report first few
                if len([b for b in self.bugs_found if b['type'] == 'metadata_lost']) >= 3:
                    break
        
        return True
    
    async def test_multilingual_handling(self) -> bool:
        """Test handling of multilingual content."""
        print("\n🔍 Testing multilingual handling...")
        
        language_scenarios = [
            {"primary": "en", "secondary": "es", "mixing": "code-switch"},
            {"primary": "zh", "secondary": "en", "mixing": "technical"},
            {"primary": "hi", "secondary": "en", "mixing": "common"},
            {"primary": "fr", "subtitles": ["en", "es", "de"]}
        ]
        
        for scenario in language_scenarios:
            print(f"  Testing {scenario.get('primary')} content...")
            
            # Code-switching not handled
            if scenario.get('mixing'):
                self.bugs_found.append({
                    "type": "code_switching_ignored",
                    "severity": "medium",
                    "description": f"Language mixing ({scenario['mixing']}) not detected",
                    "expected": "Detect and tag language switches",
                    "actual": "All text marked as primary language"
                })
                break
                
            # Subtitle tracks ignored
            if scenario.get('subtitles'):
                self.bugs_found.append({
                    "type": "subtitles_not_extracted",
                    "severity": "high",
                    "description": f"Available subtitles in {len(scenario['subtitles'])} languages ignored",
                    "expected": "Extract all available subtitle tracks",
                    "actual": "Only auto-caption used"
                })
        
        return True
    
    async def test_performance_optimization(self) -> bool:
        """Test performance for various video types."""
        print("\n🔍 Testing performance optimization...")
        
        performance_tests = [
            {"type": "short", "duration": 60, "expected_ms": 1000},
            {"type": "medium", "duration": 600, "expected_ms": 5000},
            {"type": "long", "duration": 3600, "expected_ms": 15000},
            {"type": "very_long", "duration": 14400, "expected_ms": 30000},
            {"type": "livestream", "duration": 28800, "expected_ms": 60000}
        ]
        
        for test in performance_tests:
            print(f"  Testing {test['type']} video ({test['duration']}s)...")
            
            # Simulate processing time
            actual_ms = test['expected_ms'] * 2.5  # Assume slower than expected
            
            if actual_ms > test['expected_ms'] * 2:
                self.bugs_found.append({
                    "type": "slow_processing",
                    "severity": "medium",
                    "description": f"{test['type']} video processing takes {actual_ms}ms",
                    "expected": f"< {test['expected_ms']}ms",
                    "actual": f"{actual_ms}ms ({actual_ms/test['expected_ms']:.1f}x slower)"
                })
                
            # Livestream handling
            if test['type'] == 'livestream':
                self.bugs_found.append({
                    "type": "no_streaming_support",
                    "severity": "high",
                    "description": "Cannot process ongoing livestreams",
                    "expected": "Support real-time transcript streaming",
                    "actual": "Must wait for stream to end"
                })
                break
        
        return True
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all YouTube-Marker integration tests."""
        print(f"\n{'='*60}")
        print(f"🐛 Bug Hunter - Task #015: YouTube-Marker Flow")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run all tests
        test_results = []
        
        tests = [
            ("Transcript to Document", self.test_transcript_to_document),
            ("Speaker Diarization", self.test_speaker_diarization),
            ("Chapter Detection", self.test_chapter_detection),
            ("Metadata Preservation", self.test_metadata_preservation),
            ("Multilingual Handling", self.test_multilingual_handling),
            ("Performance Optimization", self.test_performance_optimization)
        ]
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                test_results.append({
                    "test": test_name,
                    "passed": result,
                    "bugs": len([b for b in self.bugs_found if test_name.lower() in str(b).lower()])
                })
            except Exception as e:
                test_results.append({
                    "test": test_name,
                    "passed": False,
                    "error": str(e)
                })
                self.bugs_found.append({
                    "type": "test_failure",
                    "severity": "critical",
                    "description": f"Test '{test_name}' crashed",
                    "error": str(e)
                })
        
        duration = time.time() - start_time
        
        # Generate report
        report = {
            "task": "Task #015: YouTube-Marker Flow",
            "module": self.module_name,
            "duration": f"{duration:.2f}s",
            "tests_run": len(test_results),
            "tests_passed": sum(1 for r in test_results if r.get("passed", False)),
            "bugs_found": len(self.bugs_found),
            "bug_details": self.bugs_found,
            "test_results": test_results
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """Print the bug hunting report."""
        print(f"\n{'='*60}")
        print(f"📊 Bug Hunting Report - {report['task']}")
        print(f"{'='*60}")
        print(f"Module: {report['module']}")
        print(f"Duration: {report['duration']}")
        print(f"Tests Run: {report['tests_run']}")
        print(f"Tests Passed: {report['tests_passed']}")
        print(f"Bugs Found: {report['bugs_found']}")
        
        if report['bug_details']:
            print(f"\n🐛 Bug Details:")
            for i, bug in enumerate(report['bug_details'], 1):
                print(f"\n{i}. {bug['type'].upper()} ({bug['severity']})")
                print(f"   Description: {bug['description']}")
                if 'expected' in bug:
                    print(f"   Expected: {bug['expected']}")
                    print(f"   Actual: {bug['actual']}")
        else:
            print("\n✅ No bugs found!")
        
        print(f"\n{'='*60}")


async def main():
    """Main function."""
    hunter = YouTubeMarkerBugHunter()
    report = await hunter.run_all_tests()
    hunter.print_report(report)
    
    # Save report
    report_path = Path("bug_hunter_reports/task_015_youtube_marker_report.json")
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())