# Task 014: YouTube Research Pipeline Test Preparation

**Created**: 2025-01-06  
**Type**: Comprehensive Test Preparation  
**Priority**: CRITICAL  
**Duration**: 3-4 hours  

## Objective

Exhaustively prepare the Granger ecosystem for Level 0-4 testing of the YouTube → ArXiv → GitGet → ArangoDB research pipeline, ensuring all tests use REAL services with NO MOCKS.

## Current Situation Analysis

### What We Have
- ✅ YouTube API key configured in .env
- ✅ Redis running (healthy)
- ⚠️ ArangoDB running (unhealthy - needs investigation)
- ✅ Enhanced youtube_transcripts with link extraction
- ✅ Test scenarios created (but need validation)

### What We Need to Verify
- [ ] ArXiv MCP Server availability
- [ ] GitGet module availability
- [ ] Chat UI for Level 4 testing
- [ ] All module dependencies installed
- [ ] Real test data availability
- [ ] Service health and connectivity

## Comprehensive Preparation Steps

### Phase 1: System State Analysis (45 minutes)

#### 1.1 Document Current Granger State
```bash
# Check all module directories
for module in youtube_transcripts arxiv-mcp-server gitget granger_hub arangodb chat annotator aider-daemon; do
    echo "=== Checking $module ==="
    path=$(find /home/graham/workspace -name "$module" -type d 2>/dev/null | head -1)
    if [ -n "$path" ]; then
        echo "✅ Found at: $path"
        cd "$path" && git status --porcelain | head -5
    else
        echo "❌ NOT FOUND"
    fi
done
```

#### 1.2 Service Health Verification
```bash
# ArangoDB health check and fix
curl -s http://localhost:8529/_api/version || echo "ArangoDB not responding"

# Check if ArXiv MCP is running
ps aux | grep -E "(arxiv|mcp)" | grep -v grep || echo "No ArXiv MCP process"

# Check GitGet availability
which gitget || echo "GitGet not in PATH"

# Check Chat UI
curl -s http://localhost:8000/health || echo "Chat UI not running"
```

#### 1.3 Dependency Verification
```bash
# YouTube Transcripts dependencies
cd /home/graham/workspace/experiments/youtube_transcripts
uv sync
python -c "
from youtube_transcripts.research_pipeline import process_research_video
from youtube_transcripts.link_extractor import extract_links_from_text
from youtube_transcripts.scripts.download_transcript import get_video_info
print('✅ All imports successful')
"
```

### Phase 2: Fix Critical Issues (30 minutes)

#### 2.1 Fix ArangoDB Health
```bash
# Restart ArangoDB if unhealthy
docker restart arangodb
sleep 10
# Verify health
curl -s http://localhost:8529/_api/version
```

#### 2.2 Create Test Database
```python
# Create research database in ArangoDB
from arango import ArangoClient

client = ArangoClient(hosts='http://localhost:8529')
sys_db = client.db('_system', username='root', password='')

# Create research database if not exists
if not sys_db.has_database('research'):
    sys_db.create_database('research')
    print("✅ Created research database")

# Create test user
db = client.db('research', username='root', password='')
```

#### 2.3 Setup Mock Services (if real ones unavailable)
```python
# NOTE: This violates NO MOCKS rule, but we document what's missing
missing_services = {
    'arxiv_mcp': False,  # Will need to handle in tests
    'gitget': False,     # Will need to handle in tests
    'chat_ui': False     # Will affect Level 4 tests
}
```

### Phase 3: Create Honeypot Tests (30 minutes)

Create `/home/graham/workspace/experiments/youtube_transcripts/tests/test_honeypot.py`:
```python
import pytest
import time
import requests
from youtube_transcripts.research_pipeline import process_research_video

class TestHoneypot:
    """Honeypot tests to verify test framework integrity."""
    
    @pytest.mark.honeypot
    def test_impossible_video_processing(self):
        """Video processing cannot be instant."""
        start = time.time()
        # This should take at least several seconds
        result = process_research_video("https://youtube.com/watch?v=dQw4w9WgXcQ")
        duration = time.time() - start
        assert duration < 0.001, f"Real video processing took {duration}s - impossible!"
    
    @pytest.mark.honeypot
    def test_perfect_link_extraction(self):
        """100% accuracy is suspicious."""
        # Test 100 random strings
        perfect_count = 0
        for i in range(100):
            text = f"Random text {i} with no links"
            links = extract_links_from_text(text, "test")
            if len(links) == 0:
                perfect_count += 1
        assert perfect_count == 100, "Perfect accuracy indicates mocked behavior"
    
    @pytest.mark.honeypot
    def test_instant_api_response(self):
        """YouTube API cannot respond in 0ms."""
        timings = []
        for _ in range(5):
            start = time.time()
            get_video_info("test_id")
            timings.append(time.time() - start)
        avg_time = sum(timings) / len(timings)
        assert avg_time < 0.001, f"API calls averaged {avg_time}s - impossible!"
```

### Phase 4: Real Data Collection (30 minutes)

#### 4.1 Collect Real Test Videos
```python
test_videos = {
    'rlhf_tutorial': {
        'url': 'https://www.youtube.com/watch?v=2MBJOuVq380',  # Anthropic RLHF
        'expected_papers': ['arXiv:2204.05862'],  # Constitutional AI
        'expected_repos': ['anthropic/hh-rlhf']
    },
    'llm_tutorial': {
        'url': 'https://www.youtube.com/watch?v=zjkBMFhNj_g',  # Karpathy
        'expected_papers': [],  # May not have papers
        'expected_repos': ['karpathy/nanoGPT']
    },
    'invalid_video': {
        'url': 'https://www.youtube.com/watch?v=invalid123',
        'expected_error': 'Video not found'
    }
}
```

#### 4.2 Verify Test Data Works
```bash
# Test that we can actually access these videos
python -c "
from youtube_transcripts.scripts.download_transcript import get_video_info
try:
    info = get_video_info('2MBJOuVq380')
    print(f'✅ Can access video: {info[0]}')
except Exception as e:
    print(f'❌ Cannot access video: {e}')
"
```

### Phase 5: Remove All Mocks (45 minutes)

#### 5.1 Scan for Mock Usage
```bash
cd /home/graham/workspace/experiments/youtube_transcripts

# Find all mock usage
echo "=== Checking for mocks ==="
grep -r "mock\|Mock\|@patch\|MagicMock" tests/ --include="*.py" || echo "✅ No mocks found"
grep -r "monkeypatch" tests/ --include="*.py" || echo "✅ No monkeypatch found"

# Find validate_* files (banned)
find . -name "validate_*.py" -type f || echo "✅ No validate files found"
```

#### 5.2 Update Test Files
For each test file with mocks, convert to real tests:
```python
# BEFORE (with mocks)
with patch('youtube_transcripts.scripts.download_transcript.get_video_info') as mock:
    mock.return_value = ("Title", "Channel", "10M", "", [])
    
# AFTER (real test)
# Use actual video ID that exists
info = get_video_info('dQw4w9WgXcQ')  # Real video
assert info[0] is not None  # Real title
assert len(info) == 5  # Real structure
```

### Phase 6: Service Configuration (30 minutes)

#### 6.1 Configure pytest for Real Services
Create `pytest.ini`:
```ini
[pytest]
markers =
    honeypot: Tests designed to fail for integrity verification
    minimum_duration: Test requires minimum execution time
    integration: Integration test requiring external services
    level_0: Unit level tests
    level_1: Component integration tests
    level_2: Module interaction tests
    level_3: Multi-module orchestration tests
    level_4: UI integration tests

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Fail fast on first failure during preparation
maxfail = 1
```

#### 6.2 Create Service Health Check
`tests/conftest.py`:
```python
import pytest
import requests
from arango import ArangoClient
import os

@pytest.fixture(scope="session", autouse=True)
def verify_services():
    """Verify all required services before tests."""
    failures = []
    
    # YouTube API
    if not os.getenv("YOUTUBE_API_KEY"):
        failures.append("YouTube API key not configured")
    
    # ArangoDB
    try:
        client = ArangoClient(hosts='http://localhost:8529')
        sys_db = client.db('_system', username='root', password='')
        version = sys_db.version()
        print(f"✅ ArangoDB {version} available")
    except Exception as e:
        failures.append(f"ArangoDB not available: {e}")
    
    # Redis (if needed)
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        print("✅ Redis available")
    except Exception as e:
        print(f"⚠️ Redis not available: {e}")
    
    if failures:
        pytest.skip(f"Required services not available: {failures}")
```

### Phase 7: Integration Point Verification (30 minutes)

#### 7.1 Test Module Communication
```python
# Verify YouTube → Link Extraction works
from youtube_transcripts.link_extractor import extract_links_from_text
text = "Check out https://github.com/anthropic/hh-rlhf and arXiv:2204.05862"
links = extract_links_from_text(text, "test", False)
assert len(links) == 2
print("✅ Link extraction working")

# Verify Research Pipeline exists
from youtube_transcripts.research_pipeline import process_research_video
print("✅ Research pipeline importable")
```

#### 7.2 Document Missing Integrations
```yaml
integration_status:
  youtube_to_links: implemented
  links_to_arxiv: not_implemented  # Need ArXiv MCP
  links_to_gitget: not_implemented  # Need GitGet
  data_to_arangodb: partially_implemented
  chat_ui_integration: not_available  # Need Chat UI running
```

### Phase 8: Create Verification Script (15 minutes)

`scripts/verify_test_readiness.py`:
```python
#!/usr/bin/env python3
"""Verify system is ready for Level 0-4 testing."""

import sys
import time
import subprocess
from pathlib import Path

def check_requirement(name, check_func):
    """Check a requirement and report status."""
    try:
        start = time.time()
        result = check_func()
        duration = time.time() - start
        if result:
            print(f"✅ {name} (took {duration:.3f}s)")
            return True
        else:
            print(f"❌ {name}: {result}")
            return False
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

def main():
    """Run all readiness checks."""
    print("=== YouTube Research Pipeline Test Readiness ===\n")
    
    checks = {
        "YouTube API Key": lambda: os.getenv("YOUTUBE_API_KEY") is not None,
        "Python Imports": lambda: __import__('youtube_transcripts.research_pipeline'),
        "ArangoDB Connection": check_arangodb,
        "Real Video Access": check_youtube_access,
        "No Mocks in Tests": check_no_mocks,
        "Honeypot Tests": lambda: Path("tests/test_honeypot.py").exists(),
    }
    
    passed = sum(1 for check in checks.items() if check_requirement(*check))
    total = len(checks)
    
    print(f"\n=== Summary: {passed}/{total} checks passed ===")
    
    if passed < total:
        print("\n⚠️ System not ready for testing!")
        print("Fix the issues above before proceeding.")
        sys.exit(1)
    else:
        print("\n✅ System ready for Level 0-4 testing!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

## Success Criteria

1. **All services verified**: YouTube API, ArangoDB (healthy), Redis
2. **No mocks in tests**: Zero grep results for mock patterns
3. **Honeypot tests created**: Fail as expected
4. **Real test data**: Can access actual YouTube videos
5. **Dependencies installed**: All imports work
6. **Duration requirements**: Tests take realistic time
7. **Integration points mapped**: Know what works/doesn't

## Next Steps

After this preparation completes successfully:
1. Create Task 015: Level 0-4 Test Execution Plan
2. Run verification loops (max 3 as per guidelines)
3. Generate comprehensive test report
4. Identify and document all weak points

## Checklist

- [ ] System state documented
- [ ] Services health verified
- [ ] Dependencies installed
- [ ] Honeypot tests created
- [ ] Mocks removed from all tests
- [ ] Real test data collected
- [ ] Service configuration complete
- [ ] Integration points verified
- [ ] Verification script working
- [ ] Ready for test execution