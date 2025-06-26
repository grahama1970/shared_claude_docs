#!/usr/bin/env python3
"""
Module: youtube_fixes.py
Description: YouTube Transcripts-specific bug fixes implementation

External Dependencies:
- granger_common: Our standardized components
"""

from pathlib import Path
import re

def apply_youtube_fixes():
    """Apply all YouTube Transcripts-specific fixes."""
    print("\n🎥 Applying YouTube Transcripts fixes...")
    
    # 1. Add rate limiting for YouTube API
    rate_limiting_code = '''
from granger_common import get_rate_limiter
from typing import Optional, Dict, Any

# Initialize YouTube rate limiter (YouTube has strict limits)
youtube_limiter = get_rate_limiter("youtube", calls_per_second=10.0, burst_size=20)
transcript_limiter = get_rate_limiter("transcript", calls_per_second=5.0, burst_size=10)

async def fetch_video_info(video_id: str) -> Dict[str, Any]:
    """Fetch video info with rate limiting."""
    async with youtube_limiter:
        # Original fetch code here
        return await _fetch_video_info_impl(video_id)

async def fetch_transcript(video_id: str, language: Optional[str] = None) -> list:
    """Fetch transcript with rate limiting."""
    async with transcript_limiter:
        # Original fetch code here
        return await _fetch_transcript_impl(video_id, language)

async def batch_fetch_videos(video_ids: list) -> list:
    """Fetch multiple videos with rate limiting and error handling."""
    results = []
    
    for video_id in video_ids:
        try:
            async with youtube_limiter:
                info = await _fetch_video_info_impl(video_id)
                results.append({"video_id": video_id, "info": info, "status": "success"})
        except Exception as e:
            logger.error(f"Failed to fetch {video_id}: {e}")
            results.append({"video_id": video_id, "error": str(e), "status": "failed"})
    
    return results
'''
    
    # 2. Fix path validation for downloaded transcripts
    path_validation_code = '''
def validate_download_path(file_path: str) -> Path:
    """Validate download path for transcripts."""
    from pathlib import Path
    
    path = Path(file_path).resolve()
    
    # Allowed directories
    allowed_dirs = [
        Path("/home/graham/workspace/experiments/youtube_transcripts/data"),
        Path("/tmp/youtube_transcripts"),
        Path.home() / ".youtube_transcripts" / "cache"
    ]
    
    # Check for path traversal
    if ".." in str(file_path):
        raise ValueError(f"Path traversal detected: {file_path}")
    
    # Ensure within allowed directories
    allowed_paths = [d.resolve() for d in allowed_dirs]
    if not any(path.is_relative_to(allowed) for allowed in allowed_paths):
        raise ValueError(f"Path outside allowed directories: {file_path}")
    
    return path

def save_transcript(video_id: str, transcript_data: dict, output_dir: str):
    """Safely save transcript to file."""
    # Sanitize video ID for filename
    safe_video_id = re.sub(r'[^a-zA-Z0-9_-]', '_', video_id)
    filename = f"transcript_{safe_video_id}.json"
    
    # Validate path
    output_path = validate_download_path(str(Path(output_dir) / filename))
    
    # Save transcript
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_data, f, indent=2, ensure_ascii=False)
    
    return output_path
'''
    
    # 3. Add retry logic for API failures
    retry_logic_code = '''
from asyncio import sleep
from typing import TypeVar, Callable, Optional

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[..., T],
    *args,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    **kwargs
) -> Optional[T]:
    """Retry function with exponential backoff."""
    delay = base_delay
    
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Max retries reached for {func.__name__}: {e}")
                raise
            
            # Calculate next delay with exponential backoff
            delay = min(delay * 2, max_delay)
            logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
            await sleep(delay)
    
    return None

# Usage example:
async def get_video_with_retry(video_id: str):
    """Get video info with automatic retry."""
    return await retry_with_backoff(
        fetch_video_info,
        video_id,
        max_retries=3,
        base_delay=2.0
    )
'''
    
    # 4. Add memory-efficient batch processing
    batch_processing_code = '''
from collections import deque
from typing import AsyncIterator, List

async def process_videos_in_batches(
    video_ids: List[str],
    batch_size: int = 10,
    max_memory_mb: int = 500
) -> AsyncIterator[dict]:
    """Process videos in memory-efficient batches."""
    
    # Create batches
    batches = [video_ids[i:i + batch_size] for i in range(0, len(video_ids), batch_size)]
    
    for batch_num, batch in enumerate(batches):
        logger.info(f"Processing batch {batch_num + 1}/{len(batches)}")
        
        # Process batch
        results = await batch_fetch_videos(batch)
        
        # Yield results one by one to avoid memory buildup
        for result in results:
            yield result
        
        # Clear memory after each batch
        import gc
        gc.collect()
        
        # Small delay between batches to avoid rate limits
        if batch_num < len(batches) - 1:
            await sleep(1.0)

# Usage example:
async def download_large_playlist(playlist_id: str):
    """Download large playlist without memory issues."""
    video_ids = await get_playlist_videos(playlist_id)
    
    async for result in process_videos_in_batches(video_ids, batch_size=20):
        if result["status"] == "success":
            # Process successful result
            await save_transcript(result["video_id"], result["info"])
        else:
            # Log failed result
            logger.error(f"Failed to process {result['video_id']}: {result.get('error')}")
'''
    
    # 5. Add context logging
    context_logging_code = '''
from contextlib import contextmanager
from loguru import logger

@contextmanager
def video_context(video_id: str, metadata: Optional[dict] = None):
    """Add video context to all operations."""
    logger.bind(video_id=video_id)
    
    if metadata:
        logger.bind(**metadata)
    
    try:
        yield
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {e}")
        raise
    finally:
        logger.unbind("video_id")
        if metadata:
            for key in metadata:
                logger.unbind(key)

# Usage:
async def process_video(video_id: str):
    """Process video with context."""
    with video_context(video_id, {"source": "playlist", "quality": "high"}):
        info = await fetch_video_info(video_id)
        transcript = await fetch_transcript(video_id)
        # All logs will include video_id and metadata
        return {"info": info, "transcript": transcript}
'''
    
    print("✅ YouTube Transcripts fixes defined - ready for implementation")
    
    # Create implementation guide
    implementation_guide = '''
# YouTube Transcripts Module Fix Implementation Guide

## 1. Rate Limiting (CRITICAL)
Location: src/youtube_transcripts/api.py
- Import get_rate_limiter from granger_common
- Create separate limiters for video info and transcripts
- Wrap all API calls with rate limiter context
- Set conservative limits (10/sec for videos, 5/sec for transcripts)

## 2. Path Validation (HIGH)
Location: src/youtube_transcripts/downloader.py
- Add validate_download_path function
- Sanitize video IDs for filenames
- Define allowed download directories
- Check for path traversal attempts

## 3. Retry Logic (MEDIUM)
Location: src/youtube_transcripts/api.py
- Implement retry_with_backoff function
- Use exponential backoff (2, 4, 8 seconds)
- Max 3 retries per request
- Log all retry attempts

## 4. Batch Processing (HIGH)
Location: src/youtube_transcripts/batch_processor.py
- Process videos in batches of 10-20
- Use async generator to avoid memory buildup
- Add gc.collect() between batches
- Add delays between batches

## 5. Context Logging (LOW)
Location: All YouTube modules
- Add video_id context to all operations
- Include metadata (source, quality, language)
- Track processing stages

## Error Handling
- Handle quota exceeded errors gracefully
- Detect and handle deleted/private videos
- Log partial transcript availability
- Handle language fallback

## Testing
1. Rate limit test: Try 100 requests rapidly
2. Path test: Try "../../../etc/passwd" as output
3. Retry test: Simulate network failures
4. Batch test: Process 1000 video playlist
5. Memory test: Monitor memory during large batch

## Common YouTube API Errors
- Quota exceeded: Back off for 1 hour
- Video unavailable: Skip and log
- No transcript: Try auto-generated
- Rate limited: Exponential backoff
'''
    
    # Save implementation guide
    guide_path = Path("/home/graham/workspace/shared_claude_docs/module_specific_fixes/youtube_implementation_guide.md")
    guide_path.parent.mkdir(exist_ok=True)
    guide_path.write_text(implementation_guide)
    print(f"📝 Implementation guide saved to: {guide_path}")


if __name__ == "__main__":
    apply_youtube_fixes()