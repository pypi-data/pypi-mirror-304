"""devpipe is a simple pipeline framework for Python."""

from . import logger
from .core.metadata import metadata
from .core.pipeline import pipeline
from .core.step import step

__version__ = "0.1.0"
__all__ = [
    "logger",
    "pipeline",
    "step",
    "metadata",
]
