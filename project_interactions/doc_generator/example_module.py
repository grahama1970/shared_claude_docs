
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Example module for testing documentation generator

This module demonstrates various Python constructs that the documentation
generator can extract and document.
"""

from typing import List, Dict, Optional
import json
import datetime


# Module constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3


class DataProcessor:
    """Processes data with various transformations"""
    
    def __init__(self, config: Dict[str, any]):
        """Initialize processor with configuration
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.processed_count: int = 0
        
    def process(self, data: List[str]) -> List[str]:
        """Process a list of data items
        
        Args:
            data: List of strings to process
            
        Returns:
            Processed data list
        """
        results = []
        for item in data:
            results.append(self._transform(item))
            self.processed_count += 1
        return results
        
    def _transform(self, item: str) -> str:
        """Internal transformation method"""
        return item.upper()
        
    async def process_async(self, data: List[str]) -> List[str]:
        """Async version of process method"""
        # Simulate async processing
        return self.process(data)


def validate_input(data: any) -> bool:
    """Validate input data
    
    Args:
        data: Data to validate
        
    Returns:
        True if valid, False otherwise
    """
    if data is None:
        return False
    if isinstance(data, str) and len(data) == 0:
        return False
    return True


async def fetch_data(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict]:
    """Fetch data from URL
    
    Args:
        url: URL to fetch from
        timeout: Request timeout in seconds
        
    Returns:
        JSON data or None if failed
    """
    # Simulated async fetch
    return {"url": url, "timestamp": str(datetime.datetime.now())}


class ConfigManager:
    """Manages application configuration"""
    
    config_version: str = "1.0"
    
    def __init__(self):
        self.settings: Dict[str, any] = {}
        
    def load(self, path: str) -> None:
        """Load configuration from file"""
        with open(path) as f:
            self.settings = json.load(f)
            
    def get(self, key: str, default: any = None) -> any:
        """Get configuration value"""
        return self.settings.get(key, default)