"""
Module: youtube_transcripts adapter
Description: Adapter module to make YouTube Transcripts accessible with expected import paths
"""

import sys
sys.path.insert(0, '/home/graham/workspace/experiments/youtube_transcripts/src')

# Re-export youtube_transcripts module components
try:
    from youtube_transcripts import *
except ImportError:
    pass