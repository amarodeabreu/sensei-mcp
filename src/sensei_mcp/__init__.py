"""Sensei MCP - Engineering Standards Mentor

Active context injection for 50+ file types with session memory.
Transforms engineering standards from passive documentation into an active mentor.
"""

__version__ = "0.9.0"

from .server import mcp

__all__ = ["mcp", "__version__"]
