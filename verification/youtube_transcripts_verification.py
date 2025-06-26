#!/usr/bin/env python3
"""
YouTube Transcripts Test Verification - Focused Approach
Following TEST_VERIFICATION_TEMPLATE_GUIDE.md
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

# Module path
MODULE_PATH = Path("/home/graham/workspace/experiments/youtube_transcripts")

class YouTubeTranscriptsVerifier:
    def __init__(self):
        self.results = {
            "module": "youtube_transcripts",
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "verdict": None
        }
    
    def check_real_implementation(self):
        """Check for signs of real implementation."""
        print("\n🔍 Checking for real implementation patterns...")
        
        real_patterns = {
            "youtube_api": "youtube_transcript_api",
            "yt_dlp": "yt-dlp",
            "requests": "requests.get",
            "aiohttp": "aiohttp.ClientSession",
            "database": "ArangoClient",
        }
        
        implementation_score = 0
        
        for pattern_name, pattern in real_patterns.items():
            # Search in src directory
            cmd = f"grep -r '{pattern}' {MODULE_PATH}/src --include='*.py' | wc -l"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            count = int(result.stdout.strip())
            
            if count > 0:
                print(f"   ✓ Found {count} instances of {pattern_name}")
                implementation_score += 1
            else:
                print(f"   ❌ No {pattern_name} usage found")
        
        self.results["checks"]["real_implementation_score"] = f"{implementation_score}/{len(real_patterns)}"
        return implementation_score >= 3  # At least 3 real patterns
    
    def check_mock_usage(self):
        """Check for mock usage in tests."""
        print("\n🔍 Checking for mock usage...")
        
        # Check test directory
        test_dir = MODULE_PATH / "tests"
        if not test_dir.exists():
            print("   ❌ No tests directory found")
            return False
            
        # REMOVED: cmd = f"grep -r 'mock\\|Mock\\|@patch\\|MagicMock' {test_dir} --include='*.py' | wc -l"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        mock_count = int(result.stdout.strip())
        
        if mock_count > 0:
            print(f"   ❌ Found {mock_count} mock instances")
            # Show some examples
            # REMOVED: cmd_examples = f"grep -r 'mock\\|Mock\\|@patch' {test_dir} --include='*.py' | head -3"
            examples = subprocess.run(cmd_examples, shell=True, capture_output=True, text=True)
            print("   Examples:")
            for line in examples.stdout.strip().split('\n'):
                if line:
                    print(f"     {line[:80]}...")
        else:
            print("   ✓ No mocks found!")
        
        self.results["checks"]["mock_count"] = mock_count
        return mock_count == 0
    
    def run_minimal_test(self):
        """Run a minimal test to check timing."""
        print("\n🧪 Running minimal test with timing...")
        
        os.chdir(MODULE_PATH)
        
        # Look for a simple test file
        test_files = list((MODULE_PATH / "tests").glob("test_*.py"))
        if not test_files:
            print("   ❌ No test files found")
            return None
            
        # Try to find a minimal test
        minimal_test = None
        for tf in test_files:
            if "minimal" in tf.name or "basic" in tf.name:
                minimal_test = tf
                break
        
        if not minimal_test:
            minimal_test = test_files[0]  # Use first test
            
        print(f"   Running: {minimal_test.name}")
        
        # Run with timing
        cmd = f"""source .venv/bin/activate && python -m pytest -v \
            {minimal_test} \
            --durations=0 \
            -k 'not honeypot' \
            --tb=short \
            -x"""  # Stop on first failure
        
        start_time = time.time()
        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )
        duration = time.time() - start_time
        
        print(f"   Test completed in {duration:.2f}s")
        
        # Parse output for timing
        timing_data = self._parse_test_timing(result.stdout)
        
        self.results["checks"]["test_execution"] = {
            "file": minimal_test.name,
            "duration": duration,
            "exit_code": result.returncode,
            "timing_data": timing_data
        }
        
        return timing_data
    
    def _parse_test_timing(self, output):
        """Parse test output for timing information."""
        timing_data = {
            "instant_tests": 0,
            "fast_tests": 0,
            "normal_tests": 0,
            "slow_tests": 0
        }
        
        # Look for pytest duration output
        import re
        duration_pattern = r'(\d+\.\d+)s'
        
        for line in output.split('\n'):
            if '::' in line and 's' in line:
                match = re.search(duration_pattern, line)
                if match:
                    duration = float(match.group(1))
                    if duration < 0.001:
                        timing_data["instant_tests"] += 1
                    elif duration < 0.1:
                        timing_data["fast_tests"] += 1
                    elif duration < 1.0:
                        timing_data["normal_tests"] += 1
                    else:
                        timing_data["slow_tests"] += 1
        
        return timing_data
    
    def check_api_keys(self):
        """Check if API keys are configured."""
        print("\n🔑 Checking API key configuration...")
        
        env_file = MODULE_PATH / ".env"
        if env_file.exists():
            with open(env_file) as f:
                content = f.read()
                
            has_youtube_key = "YOUTUBE_API_KEY" in content
            has_db_config = "ARANGO" in content
            
            print(f"   YouTube API key: {'✓ Configured' if has_youtube_key else '❌ Missing'}")
            print(f"   Database config: {'✓ Configured' if has_db_config else '❌ Missing'}")
            
            self.results["checks"]["api_keys"] = {
                "youtube": has_youtube_key,
                "database": has_db_config
            }
            
            return has_youtube_key or has_db_config
        else:
            print("   ❌ No .env file found")
            return False
    
    def check_network_calls(self):
        """Check for real network call patterns."""
        print("\n🌐 Checking for network call patterns...")
        
        # Look for rate limiting and retry patterns
        patterns = {
            "rate_limit": ["rate_limit", "RateLimiter", "sleep", "backoff"],
            "error_handling": ["except.*Error", "retry", "timeout"],
            "real_urls": ["youtube.com", "googleapis.com", "ytimg.com"]
        }
        
        found_patterns = {}
        
        for pattern_type, searches in patterns.items():
            found = False
            for search in searches:
                cmd = f"grep -r '{search}' {MODULE_PATH}/src --include='*.py' | wc -l"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if int(result.stdout.strip()) > 0:
                    found = True
                    break
            
            found_patterns[pattern_type] = found
            print(f"   {pattern_type}: {'✓ Found' if found else '❌ Not found'}")
        
        self.results["checks"]["network_patterns"] = found_patterns
        return sum(found_patterns.values()) >= 2
    
    def generate_verdict(self):
        """Generate final verdict based on all checks."""
        checks = self.results["checks"]
        
        # Score calculation
        score = 0
        if checks.get("real_implementation_score", "0/5").split('/')[0] >= "3":
            score += 30
        if checks.get("mock_count", 1) == 0:
            score += 30
        if checks.get("api_keys", {}).get("youtube", False):
            score += 20
        if any(checks.get("network_patterns", {}).values()):
            score += 20
            
        # Verdict
        if score >= 80:
            self.results["verdict"] = "LIKELY REAL - High confidence"
        elif score >= 60:
            self.results["verdict"] = "PARTIALLY REAL - Mixed implementation"
        elif score >= 40:
            self.results["verdict"] = "QUESTIONABLE - Needs investigation"
        else:
            self.results["verdict"] = "LIKELY FAKE - Low confidence"
            
        self.results["confidence_score"] = score
        
        return self.results["verdict"]
    
    def run_verification(self):
        """Run complete verification."""
        print("🔍 YouTube Transcripts Module Verification")
        print("="*60)
        
        # Run all checks
        self.check_real_implementation()
        no_mocks = self.check_mock_usage()
        self.check_api_keys()
        self.check_network_calls()
        
        # Try to run a test if no mocks
        if no_mocks:
            self.run_minimal_test()
        else:
            print("\n⚠️  Skipping test execution due to mock usage")
        
        # Generate verdict
        verdict = self.generate_verdict()
        
        # Save report
        report_path = Path.cwd() / "verification" / "youtube_verification_report.json"
        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print("VERIFICATION SUMMARY")
        print("="*60)
        print(f"Module: YouTube Transcripts")
        print(f"Verdict: {verdict}")
        print(f"Confidence Score: {self.results['confidence_score']}/100")
        print(f"\nReport saved to: {report_path}")
        
        return self.results


def main():
    verifier = YouTubeTranscriptsVerifier()
    results = verifier.run_verification()
    
    # Exit code based on verdict
    if "REAL" in results["verdict"]:
        return 0
    else:
        return 1


if __name__ == "__main__":
    original_dir = Path.cwd()
    try:
        exit_code = main()
        sys.exit(exit_code)
    finally:
        os.chdir(original_dir)