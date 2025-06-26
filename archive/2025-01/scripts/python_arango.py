"""Python-arango compatibility wrapper"""
import sys
sys.path.insert(0, "/home/graham/workspace/experiments/arangodb/src")

# Re-export arangodb as python_arango
try:
    from arangodb import *
    from arangodb import __version__
except ImportError:
    # If that fails, try the actual python-arango
    try:
        from arango import *
    except ImportError:
        pass

# Export ArangoClient for compatibility
try:
    from arango import ArangoClient
except ImportError:
    # Create a dummy if not available
    class ArangoClient:
        def __init__(self, hosts=None):
            self.hosts = hosts
        
        def db(self, name, username='', password=''):
            return {"name": name}
