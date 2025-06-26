"""
Module: youtube_transcripts.scripts.download_transcript adapter
Description: Maps expected youtube transcript script imports
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/scripts')

# Import from the actual download_transcript script
try:
    from download_transcript import extract_video_id, get_video_info
except ImportError as e:
    print(f"Warning: Could not import youtube transcript functions: {e}")
    
    def extract_video_id(*args, **kwargs):
        raise NotImplementedError("YouTube transcript module not properly installed")
    
    def get_video_info(*args, **kwargs):
        raise NotImplementedError("YouTube transcript module not properly installed")