#!/usr/bin/env python3
"""
Module: test_04_youtube_transcript_download.py
Description: Test YouTube transcript extraction functionality
Level: 0
Modules: YouTube Transcripts
Expected Bugs: API failures, missing transcripts, encoding issues
"""

import json
import time
from typing import Dict, List, Any
from pathlib import Path

class YouTubeTranscriptTest:
    """Level 0: Test basic YouTube transcript functionality"""
    
    def __init__(self):
        self.test_name = "YouTube Transcript Download"
        self.level = 0
        self.bugs_found = []
        
    def test_transcript_extraction(self):
        """Test extracting transcripts from various video types"""
        print(f"\n{'='*60}")
        print(f"Level {self.level} Test: {self.test_name}")
        print(f"{'='*60}\n")
        
        # Test video IDs with different characteristics
        test_videos = [
            {
                "name": "Standard video",
                "video_id": "dQw4w9WgXcQ",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            {
                "name": "Short URL format",
                "video_id": "dQw4w9WgXcQ",
                "url": "https://youtu.be/dQw4w9WgXcQ"
            },
            {
                "name": "URL with timestamp",
                "video_id": "dQw4w9WgXcQ",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s"
            },
            {
                "name": "Invalid video ID",
                "video_id": "INVALID_ID_12345",
                "url": "https://www.youtube.com/watch?v=INVALID_ID_12345"
            },
            {
                "name": "Empty video ID",
                "video_id": "",
                "url": "https://www.youtube.com/watch?v="
            },
            {
                "name": "Private video",
                "video_id": "private_video_id",
                "url": "https://www.youtube.com/watch?v=private_video_id"
            },
            {
                "name": "Live stream",
                "video_id": "live_stream_id",
                "url": "https://www.youtube.com/watch?v=live_stream_id"
            }
        ]
        
        # Import YouTube handler
        try:
            from youtube_transcripts.src.youtube_transcripts import download_youtube_transcript
            from youtube_transcripts.scripts.download_transcript import extract_video_id
        except ImportError as e:
            self.bugs_found.append({
                "bug": "YouTube module import failure",
                "error": str(e),
                "severity": "CRITICAL",
                "impact": "Cannot use YouTube functionality"
            })
            print(f"❌ Import failed: {e}")
            return
        
        for test in test_videos:
            print(f"\nTesting: {test['name']}")
            print(f"URL: {test['url']}")
            
            try:
                # Test video ID extraction
                extracted_id = extract_video_id(test["url"])
                if extracted_id != test["video_id"]:
                    self.bugs_found.append({
                        "bug": "Video ID extraction mismatch",
                        "expected": test["video_id"],
                        "got": extracted_id,
                        "url": test["url"],
                        "severity": "HIGH"
                    })
                
                # Test transcript download
                start_time = time.time()
                result = download_youtube_transcript(test["url"])
                duration = time.time() - start_time
                
                if result and isinstance(result, str):
                    # Check file exists
                    if Path(result).exists():
                        file_size = Path(result).stat().st_size
                        print(f"✅ Downloaded transcript: {file_size} bytes in {duration:.2f}s")
                        
                        # Check for quality issues
                        with open(result, 'r') as f:
                            content = f.read()
                            
                        # Bug: Empty transcript
                        if len(content.strip()) == 0:
                            self.bugs_found.append({
                                "bug": "Empty transcript file",
                                "video_id": test["video_id"],
                                "severity": "HIGH"
                            })
                        
                        # Bug: No timestamps
                        if "[" not in content and "]" not in content:
                            self.bugs_found.append({
                                "bug": "Transcript missing timestamps",
                                "video_id": test["video_id"],
                                "severity": "MEDIUM"
                            })
                    else:
                        self.bugs_found.append({
                            "bug": "Transcript file doesn't exist",
                            "path": result,
                            "severity": "HIGH"
                        })
                    
                    # Performance issue
                    if duration > 10:
                        self.bugs_found.append({
                            "bug": "Slow transcript download",
                            "video_id": test["video_id"],
                            "duration": f"{duration:.2f}s",
                            "severity": "MEDIUM"
                        })
                else:
                    if test["name"] == "Standard video":
                        self.bugs_found.append({
                            "bug": "Failed to download standard video",
                            "video_id": test["video_id"],
                            "severity": "HIGH"
                        })
                    print(f"❌ Download failed")
                    
            except Exception as e:
                error_msg = str(e)
                print(f"💥 Exception: {error_msg[:100]}")
                
                # Check error handling quality
                if test["name"] == "Empty video ID" and "video" not in error_msg.lower():
                    self.bugs_found.append({
                        "bug": "Poor error message for empty ID",
                        "error": error_msg,
                        "severity": "LOW"
                    })
    
    def test_metadata_extraction(self):
        """Test extracting video metadata"""
        print("\n\nTesting Metadata Extraction...")
        
        try:
            from youtube_transcripts.scripts.download_transcript import get_video_info
        except ImportError:
            print("❌ Metadata extraction not available")
            return
        
        test_video_id = "dQw4w9WgXcQ"
        
        try:
            print(f"Extracting metadata for: {test_video_id}")
            title, channel, duration, description, links = get_video_info(test_video_id)
            
            # Check for missing metadata
            if not title:
                self.bugs_found.append({
                    "bug": "Missing video title",
                    "video_id": test_video_id,
                    "severity": "HIGH"
                })
            
            if not channel:
                self.bugs_found.append({
                    "bug": "Missing channel name",
                    "video_id": test_video_id,
                    "severity": "MEDIUM"
                })
            
            print(f"✅ Got metadata: {title[:50]}... by {channel}")
            
        except Exception as e:
            self.bugs_found.append({
                "bug": "Exception extracting metadata",
                "error": str(e),
                "severity": "HIGH"
            })
    
    def test_link_extraction(self):
        """Test extracting links from transcripts"""
        print("\n\nTesting Link Extraction...")
        
        try:
            from youtube_transcripts.link_extractor import extract_links_from_text
        except ImportError:
            print("❌ Link extraction not available")
            return
        
        # Test text samples with various link formats
        test_texts = [
            {
                "name": "ArXiv link",
                "text": "Check out this paper: https://arxiv.org/abs/2301.12345",
                "expected_links": 1
            },
            {
                "name": "GitHub link",
                "text": "Code available at https://github.com/user/repo",
                "expected_links": 1
            },
            {
                "name": "Multiple links",
                "text": "Paper: https://arxiv.org/abs/1234.5678 Code: https://github.com/test/test",
                "expected_links": 2
            },
            {
                "name": "No links",
                "text": "This text has no links at all",
                "expected_links": 0
            },
            {
                "name": "Malformed links",
                "text": "Bad link: htp://notaurl and another: github.com/missing-protocol",
                "expected_links": 0
            }
        ]
        
        for test in test_texts:
            print(f"\nTesting: {test['name']}")
            
            try:
                links = extract_links_from_text(test["text"], "test_source", False)
                
                if len(links) != test["expected_links"]:
                    self.bugs_found.append({
                        "bug": "Link extraction count mismatch",
                        "test": test["name"],
                        "expected": test["expected_links"],
                        "got": len(links),
                        "severity": "MEDIUM"
                    })
                    print(f"❌ Expected {test['expected_links']} links, got {len(links)}")
                else:
                    print(f"✅ Found {len(links)} links")
                    
            except Exception as e:
                self.bugs_found.append({
                    "bug": f"Exception in link extraction: {test['name']}",
                    "error": str(e),
                    "severity": "MEDIUM"
                })
    
    def generate_report(self):
        """Generate test report"""
        print(f"\n\n{'='*60}")
        print(f"Test Report: {self.test_name}")
        print(f"{'='*60}")
        
        if not self.bugs_found:
            print("\n✅ No bugs found!")
            return []
        
        print(f"\nFound {len(self.bugs_found)} bugs:\n")
        
        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            bugs = [b for b in self.bugs_found if b.get("severity") == severity]
            if bugs:
                print(f"\n{severity} ({len(bugs)} bugs):")
                for bug in bugs:
                    print(f"  - {bug['bug']}")
        
        # Save detailed report
        report_path = Path(f"bug_reports/level0_{self.test_name.lower().replace(' ', '_')}.json")
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(self.bugs_found, indent=2))
        print(f"\n📄 Detailed report: {report_path}")
        
        return self.bugs_found


def main():
    """Run the test"""
    tester = YouTubeTranscriptTest()
    tester.test_transcript_extraction()
    tester.test_metadata_extraction()
    tester.test_link_extraction()
    return tester.generate_report()


if __name__ == "__main__":
    bugs = main()
    exit(0 if not bugs else 1)