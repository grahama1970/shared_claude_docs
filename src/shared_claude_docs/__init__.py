"""
Shared Claude Documentation System

A centralized repository for managing documentation, conventions, and utilities
across all Claude-based projects.
"""

__version__ = "0.1.0"

from .cli import main
from .validators import validate_project
from .sync import sync_documentation

__all__ = ["main", "validate_project", "sync_documentation"]
