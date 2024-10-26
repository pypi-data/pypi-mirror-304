"""
CTX

Contextal command line tools and python library
"""

__version__ = "0.0.1"
__all__ = [
    "Platform",
    "QueryError",
    "ScenarioDuplicateNameError",
    "ScenarioReplacementError",
    "Config",
]

from .platform import (
    Platform,
    QueryError,
    ScenarioDuplicateNameError,
    ScenarioReplacementError,
)
from .config import Config
