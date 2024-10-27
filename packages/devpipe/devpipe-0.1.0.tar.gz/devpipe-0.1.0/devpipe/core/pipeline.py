"""Pipeline decorator module."""

import logging
from functools import wraps
from typing import Callable, Optional

from ..database import _get_session
from ..models.pipeline import (
    Pipeline,
    PipelineExecution,
    PipelineInputs,
    PipelineOutputs,
)
from ._commons import _init_devpipe

logger = logging.getLogger(__name__)


def pipeline(
    entrypoint: Optional[Callable] = None,
    name: Optional[str] = None,
    rerun: bool = False,
    cache: bool = True,
) -> Callable:
    """Pipeline decorator.

    Args:
        entrypoint (Optional[Callable], optional): Pipeline entrypoint.
        name (Optional[str], optional): Pipeline name. Defaults to None. If
            not provided, the function name will be used.
        rerun (bool, optional): Re-run pipeline even if cache exists.
        cache (bool, optional): Use cache.

    Returns:
        Decorator or decorated function.

    Example:
        ```python
        import devpipe as dp

        # Decorator without arguments
        @dp.pipeline
        def my_pipeline():
            ...

        # Decorator with arguments, equivalent to the previous example
        @dp.pipeline(name="my_pipeline", rerun=False, cache=True)
        def my_pipeline():
            ...
        ```
    """

    def decorator(fn: Callable) -> Callable:
        pname = name or f"{fn.__name__}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            _init_devpipe()
            with _get_session(autoflush=False) as session:
                pipe = Pipeline.get(pname, session)
                if not cache:
                    logger.debug(
                        f"Pipeline `{pname}` is not using cache. "
                        f"Returning pipeline results directly."
                    )
                    pipe_exec = PipelineExecution(pipeline=pipe)
                    return pipe_exec._run(fn, *args, **kwargs)
                inputs, i_bytes = PipelineInputs.from_object((args, kwargs))
                pipe = Pipeline.get(pname, session)
                if not rerun:
                    pipe_exec = PipelineExecution.get(pipe, inputs, session)
                    if pipe_exec:
                        logger.info(f"Cache hit for pipeline {pipe.uuid}.")
                        return pipe_exec.outputs.read()

            pipe_exec = PipelineExecution(pipeline=pipe)
            logger.info(f"Starting pipeline execution {pipe_exec.uuid}.")
            result = pipe_exec._run(fn, *args, **kwargs)
            logger.info(f"Pipeline execution {pipe_exec.uuid} finished.")

            outputs, o_bytes = PipelineOutputs.from_object(result)
            inputs.save(i_bytes)
            outputs.save(o_bytes)
            pipe_exec.inputs = inputs
            pipe_exec.outputs = outputs
            with _get_session() as session:
                session.add(pipe_exec)
                session.commit()

            return result

        return wrapper

    return decorator(entrypoint) if entrypoint else decorator


__all__ = ["pipeline"]
