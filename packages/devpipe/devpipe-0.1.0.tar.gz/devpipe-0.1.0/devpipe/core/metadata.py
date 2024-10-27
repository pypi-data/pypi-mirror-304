"""Metadata module."""

import logging
from typing import Any

from .pipeline import PipelineExecution as PExec
from .step import StepExecution as SExec

logger = logging.getLogger(__name__)


def metadata(**kwargs: Any) -> bool:
    """Add metadata to the current pipeline or step execution.

    Args:
        **kwargs (Any): Metadata.

    Returns:
        bool: True if metadata was added, False otherwise.

    Example:
        ```python
        import devpipe as dp

        @dp.step
        def my_step():
            dp.metadata(pages=35)
            ...

        @dp.pipeline
        def my_pipeline():
            dp.metadata(author="John Doe")
            ...
        ```

    !!! warning
        Make sure that all the metadata values are JSON serializable.
    """
    execution = SExec._from_context() or PExec._from_context()
    if not execution:
        logger.warning(
            "Metadata decorator not called from a pipeline or step. "
            "Metadata will not be saved."
        )
        return False
    execution.meta.update(kwargs)
    return True


__all__ = ["metadata"]
