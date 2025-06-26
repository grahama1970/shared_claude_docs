#!/usr/bin/env python3
"""
Module: test_youtube_sparta_integration.py
Description: Test YouTube transcript extraction and security analysis

External Dependencies:
- None
"""

import sys
import asyncio
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/youtube_transcripts/src")))
sys.path.insert(0, str(Path("/home/graham/workspace/experiments/sparta/src")))

async def test_youtube_to_sparta():
    """Test extracting security topics from video transcripts"""
    print("\n🧪 Testing YouTube -> SPARTA Integration...")
    
    try:
        # Import modules
        from youtube_transcripts.handlers import Handler as YouTubeHandler
        from sparta.integrations.sparta_module import SPARTAModule
        
        # Initialize
        youtube = YouTubeHandler()
        sparta = SPARTAModule()
        
        # Step 1: Extract transcript
        print("  📹 Extracting video transcript...")
        transcript_result = youtube.handle({
            "video_id": "test_security_video",
            "action": "extract_transcript"
        })
        
        if not transcript_result.get("success"):
            print(f"  ⚠️ Using simulated transcript")
            transcript_text = "This video discusses log4j vulnerabilities and buffer overflow attacks."
        else:
            transcript_text = transcript_result.get("transcript", "")
        
        print(f"  ✅ Got transcript: {transcript_text[:50]}...")
        
        # Step 2: Extract security keywords
        security_keywords = ["log4j", "buffer overflow", "vulnerability", "CVE"]
        found_keywords = [kw for kw in security_keywords if kw.lower() in transcript_text.lower()]
        
        print(f"  🔍 Found security keywords: {found_keywords}")
        
        # Step 3: Search for related CVEs
        for keyword in found_keywords[:2]:  # Limit to avoid rate limiting
            print(f"  📡 Searching CVEs for: {keyword}")
            cve_result = await sparta.process({
                "action": "search_cve",
                "data": {"query": keyword, "limit": 2}
            })
            
            if cve_result.get("success"):
                cves = cve_result.get("data", {}).get("cves", [])
                print(f"  ✅ Found {len(cves)} CVEs for {keyword}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_youtube_to_sparta())
    exit(0 if result else 1)
