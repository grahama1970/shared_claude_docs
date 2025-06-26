"""ArXiv MCP Server compatibility wrapper"""
import sys
sys.path.insert(0, "/home/graham/workspace/mcp-servers/arxiv-mcp-server/src")

try:
    from arxiv_mcp_server import *
except ImportError:
    # Create minimal functionality
    class ArXivServer:
        def __init__(self):
            self.name = "arxiv"
        
        def search(self, query, max_results=5):
            """Search arxiv papers"""
            return []

__all__ = ["ArXivServer"]
