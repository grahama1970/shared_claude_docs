"""
Module: youtube_transcripts.src.youtube_transcripts adapter
Description: Maps expected youtube_transcripts imports to actual module structure
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/scripts')
sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/src')

# Import the download function from scripts
try:
    from download_transcript import download_youtube_transcript
except ImportError as e:
    print(f"Warning: Could not import youtube download function: {e}")
    
    def download_youtube_transcript(*args, **kwargs):
        raise NotImplementedError("YouTube transcript download not properly installed")