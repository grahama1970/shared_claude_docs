# Task 015: YouTube Research Pipeline Level 0-4 Test Plan

**Created**: 2025-01-06  
**Type**: Comprehensive Test Execution Plan  
**Priority**: CRITICAL  
**Duration**: 2-3 days  
**Follows**: Task 014 (Preparation)

## Executive Summary

Comprehensive test plan for validating the YouTube → ArXiv → GitGet → ArangoDB research pipeline across all integration levels, following Granger TEST_VERIFICATION_TEMPLATE_GUIDE standards with NO MOCKS allowed.

## Current State (Post-Preparation)

### Ready ✅
- YouTube API Key configured and working
- ArangoDB running with research database
- Real video access verified (Rick Astley test passed)
- Chat UI running and healthy
- Honeypot tests in place (5 tests)
- Python imports working
- Redis available

### Not Ready ❌
- 86 test files still contain mocks (CRITICAL ISSUE)
- ArXiv MCP server not verified as running
- GitGet not in PATH

### Integration Status
```yaml
youtube_to_links: ✅ Implemented and tested
links_to_arxiv: ❌ Requires ArXiv MCP (can mock temporarily)
links_to_gitget: ❌ Requires GitGet setup
data_to_arangodb: ⚠️ Partially implemented
chat_ui_integration: ✅ UI running but MCP integration unknown
```

## Test Execution Plan by Level

### Level 0: Unit Tests (4 hours)

#### Objectives
- Validate core components work in isolation
- Ensure minimum duration requirements met
- No external dependencies

#### Test Modules
1. **Link Extraction** (`test_link_extraction_unit.py`)
   - Test URL pattern matching
   - Test arXiv ID extraction
   - Test GitHub repo normalization
   - Test attribution tracking
   - Duration: Each test >0.01s (string processing)

2. **Video ID Extraction** (`test_video_id_unit.py`)
   - Test all YouTube URL formats
   - Test invalid URL handling
   - Test edge cases (timestamps, playlists)
   - Duration: Each test >0.01s

3. **Filename Sanitization** (`test_sanitization_unit.py`)
   - Test special character removal
   - Test Unicode handling
   - Test length limits
   - Duration: Each test >0.01s

#### Success Criteria
- All unit tests pass
- No tests complete in <0.01s
- Test coverage >80% for core modules
- Honeypot tests all fail

#### Test Code Structure
```python
# test_link_extraction_unit.py
import time
import pytest
from youtube_transcripts.link_extractor import extract_links_from_text

class TestLinkExtractionUnit:
    @pytest.mark.level_0
    @pytest.mark.minimum_duration(0.01)
    def test_github_extraction_basic(self):
        start = time.time()
        text = "Check out https://github.com/anthropic/hh-rlhf"
        links = extract_links_from_text(text, "test", False)
        duration = time.time() - start
        
        assert duration > 0.01, f"Too fast: {duration}s"
        assert len(links) == 1
        assert links[0].url == "https://github.com/anthropic/hh-rlhf"
        assert links[0].link_type == "github"
```

### Level 1: Component Integration (6 hours)

#### Objectives
- Test components working together
- Real API calls (no mocks)
- Verify service connectivity

#### Test Modules
1. **YouTube API Integration** (`test_youtube_api_integration.py`)
   - Test real video metadata retrieval
   - Test comment fetching
   - Test error handling (private videos, invalid IDs)
   - Test rate limit behavior
   - Duration: Each test >0.05s (network call)

2. **ArangoDB Integration** (`test_arangodb_integration.py`)
   - Test connection with auth
   - Test collection creation
   - Test document insertion
   - Test basic queries
   - Duration: Each test >0.1s (database operation)

3. **Link Extraction Pipeline** (`test_extraction_pipeline.py`)
   - Test full extraction from real videos
   - Test attribution preservation
   - Test deduplication
   - Duration: Each test >0.5s (multiple operations)

#### Real Test Data
```python
REAL_TEST_VIDEOS = {
    'anthropic_rlhf': {
        'id': '2MBJOuVq380',
        'title_contains': 'RLHF',
        'expected_links': {
            'github': ['anthropic/hh-rlhf'],
            'arxiv': ['2204.05862']  # Constitutional AI
        }
    },
    'karpathy_tutorial': {
        'id': 'karpathy_latest',  # Find current video
        'expected_repos': ['karpathy/nanoGPT']
    }
}
```

#### Success Criteria
- All API calls take >50ms
- Database operations take >100ms
- No instant responses
- Real data returned and validated

### Level 2: Module Interactions (8 hours)

#### Objectives
- Test data flow between modules
- Verify transformations preserve data
- Test error propagation

#### Test Scenarios
1. **YouTube → Link Extraction Flow**
   - Download real transcript
   - Extract links from description
   - Extract links from comments
   - Verify all links categorized correctly
   - Duration: >1s per test

2. **Links → Knowledge Chunks**
   - Process transcript into chunks
   - Verify chunk boundaries
   - Test chunk metadata
   - Duration: >0.5s per test

3. **Data → ArangoDB Storage**
   - Store video metadata
   - Store knowledge chunks
   - Create relationships
   - Verify graph structure
   - Duration: >1s per test

#### Integration Test Example
```python
@pytest.mark.level_2
@pytest.mark.integration
async def test_youtube_to_arangodb_flow():
    start = time.time()
    
    # Real video processing
    video_url = "https://youtube.com/watch?v=2MBJOuVq380"
    
    # Step 1: Get video info (real API call)
    info = get_video_info(extract_video_id(video_url))
    assert info[0] is not None  # Has title
    
    # Step 2: Extract links
    links = extract_links_from_text(info[3], "video_author", True)
    assert len(links) > 0
    
    # Step 3: Store in ArangoDB
    video_doc = store_video_metadata(info, links)
    assert video_doc['_id'] is not None
    
    duration = time.time() - start
    assert duration > 1.0, f"Full flow too fast: {duration}s"
```

### Level 3: Multi-Module Orchestration (12 hours)

#### Objectives
- Test complete research pipeline
- Test agent interaction patterns
- Test error recovery
- Test concurrent processing

#### Test Scenarios

1. **Complete Research Flow**
   ```python
   @pytest.mark.level_3
   async def test_complete_research_flow():
       # Process video with known papers/repos
       result = await process_research_video(
           "https://youtube.com/watch?v=2MBJOuVq380"
       )
       
       assert result['status'] == 'success'
       assert result['arxiv_papers'] > 0
       assert result['github_repos'] > 0
       assert result['knowledge_chunks'] > 10
   ```

2. **Agent Any-Order Calls**
   - Call extract_links first, then get video
   - Call ArangoDB query before processing
   - Test system handles any sequence

3. **Concurrent Video Processing**
   - Process 5 videos simultaneously
   - Verify no data corruption
   - Test rate limit handling

4. **Error Recovery**
   - Test API quota exceeded
   - Test network timeout
   - Test invalid video handling
   - Verify graceful degradation

#### Performance Requirements
- Single video: <30s total
- Concurrent videos: <60s for 5
- Error recovery: <3 retry attempts

### Level 4: UI Integration (16 hours)

#### Objectives
- Test complete user experience
- Test MCP orchestration
- Test real-time feedback
- Test multimodal display

#### Test Scenarios

1. **Chat UI Research Flow**
   ```python
   @pytest.mark.level_4
   async def test_chat_ui_research():
       # Simulate user message
       response = await send_chat_message(
           "Analyze this RLHF video: https://youtube.com/watch?v=2MBJOuVq380"
       )
       
       # Verify UI responses
       assert response['status'] == 'processing'
       
       # Wait for completion
       result = await wait_for_completion(response['task_id'])
       
       # Verify rich display
       assert 'video_embed' in result['content_blocks']
       assert 'link_cards' in result['content_blocks']
       assert 'graph_viz' in result['content_blocks']
   ```

2. **Progress Tracking**
   - Connect WebSocket
   - Monitor progress events
   - Verify percentage updates
   - Test cancel operation

3. **Query Interface**
   - "What papers were mentioned?"
   - "Show implementation code"
   - "Find similar videos"
   - Verify natural language → AQL

4. **Error Display**
   - Test rate limit message
   - Test network error display
   - Test recovery suggestions

#### UI Testing Tools
```python
# WebSocket monitoring
async with websockets.connect('ws://localhost:8000/ws') as ws:
    await ws.send(json.dumps({
        'type': 'message',
        'content': 'Process video: ...'
    }))
    
    # Collect all events
    events = []
    async for message in ws:
        event = json.loads(message)
        events.append(event)
        if event['type'] == 'complete':
            break
```

## Test Execution Schedule

### Day 1: Foundation (Levels 0-1)
- **Morning**: Fix mock issues in critical tests
- **Afternoon**: Run Level 0 unit tests
- **Evening**: Run Level 1 integration tests

### Day 2: Integration (Levels 2-3)  
- **Morning**: Run Level 2 module tests
- **Afternoon**: Run Level 3 orchestration tests
- **Evening**: Debug and fix issues

### Day 3: Full System (Level 4 + Reports)
- **Morning**: Run Level 4 UI tests
- **Afternoon**: Generate comprehensive report
- **Evening**: Document weak points and recommendations

## Verification Loops

Following TEST_VERIFICATION_TEMPLATE_GUIDE:

### Loop 1: Initial Run
1. Run tests at each level
2. Identify FAKE tests (instant completion)
3. Document failures
4. Apply fixes

### Loop 2: Fix and Retry
1. Remove remaining mocks
2. Add duration checks
3. Ensure real service calls
4. Re-run failed tests

### Loop 3: Final Verification
1. All tests use real services
2. All honeypots fail
3. Duration requirements met
4. Generate report

## Success Metrics

### Quantitative
- Level 0: 100% pass rate, 0 mocks
- Level 1: >90% pass rate, all >50ms
- Level 2: >85% pass rate, all >500ms  
- Level 3: >80% pass rate, <30s/video
- Level 4: >75% pass rate, UI responsive

### Qualitative
- No instant test completions
- Real data in all responses
- Proper error messages
- Graceful degradation
- User-friendly feedback

## Risk Mitigation

### High Risk: Mocks in Tests
- **Impact**: Violates Granger standards
- **Mitigation**: Remove all mocks before Level 3
- **Fallback**: Document which tests need rework

### Medium Risk: Service Availability
- **Impact**: Can't test integrations
- **Mitigation**: Mock services documented as unavailable
- **Fallback**: Simulate with docker containers

### Low Risk: Rate Limits
- **Impact**: Slow test execution
- **Mitigation**: Implement backoff, use multiple API keys
- **Fallback**: Reduce test data set

## Deliverables

1. **Test Reports** (Markdown + JSON)
   - Summary statistics by level
   - Failure analysis
   - Duration metrics
   - Weak point identification

2. **Fixed Test Suite**
   - No mocks (or documented exceptions)
   - All honeypots failing
   - Duration requirements met

3. **Integration Documentation**
   - What works/doesn't
   - Configuration required
   - Setup instructions

4. **Recommendations**
   - Architecture improvements
   - Missing integrations
   - Performance optimizations

## Next Steps

After successful completion:
1. Deploy to staging environment
2. Run continuous monitoring
3. Create user documentation
4. Plan production rollout

## Appendix: Key Commands

```bash
# Run specific level
pytest -m level_0 -v --durations=10

# Run with timing validation
pytest --minimum-duration-check

# Generate HTML report
pytest --html=report.html --self-contained-html

# Run verification loop
python scripts/run_verification_loop.py

# Check for mocks
grep -r "mock\|Mock" tests/ | grep -v honeypot

# Monitor services
docker ps
curl http://localhost:8529/_api/version
curl http://localhost:8000/health
```