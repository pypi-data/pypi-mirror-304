"""Logger module."""

from __future__ import annotations

import inspect
import logging

from loguru import logger

INIT = False


class InterceptHandler(logging.Handler):  # pragma: no cover
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


if not INIT:
    devpipe_handler = InterceptHandler()
    devpipe_logger = logging.getLogger(__package__)
    devpipe_logger.addHandler(devpipe_handler)
    devpipe_logger.setLevel("WARNING")
    INIT = True


def set_level(level: str | int) -> None:  # pragma: no cover
    """Set logger level.

    Args:
        level (str | int): Log level.

    Example:
        ```python
        import devpipe as dp

        dp.logger.set_level("INFO")

        @dp.pipeline
        def my_pipeline():
            return

        my_pipeline()
        ```

        ```
        2024-10-19 23:05:14.640 | INFO     | devpipe.core.pipeline:wrapper:77 - Starting ...
        2024-10-19 23:05:14.640 | INFO     | devpipe.core.pipeline:wrapper:79 - Pipeline ...
        ```
    """  # noqa: E501
    devpipe_logger.setLevel(level)


__all__ = ["set_level"]
