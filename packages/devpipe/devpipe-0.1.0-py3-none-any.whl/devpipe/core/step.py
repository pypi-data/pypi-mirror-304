"""Step decorator module."""

import logging
from functools import wraps
from typing import Callable, Optional

from ..database import _get_session
from ..models.pipeline import PipelineExecution
from ..models.step import (
    Step,
    StepExecution,
    StepInputs,
    StepOutputs,
)
from ._commons import _init_devpipe

logger = logging.getLogger(__name__)


def step(
    entrypoint: Optional[Callable] = None,
    name: Optional[str] = None,
    rerun: bool = False,
    cache: bool = True,
) -> Callable:
    """Step decorator.

    Args:
        entrypoint (Optional[Callable], optional): Step entrypoint.
        name (Optional[str], optional): Step name. Defaults to None. If
            not provided, the function name will be used.
        rerun (bool, optional): Re-run step even if cache exists.
        cache (bool, optional): Use cache.

    Returns:
        Decorator or decorated function.

    Example:
        ```python
        import devpipe as dp

        # Decorator without arguments
        @dp.step
        def my_step():
            ...

        # Decorator with arguments, equivalent to the previous example
        @dp.step(name="my_step", rerun=False, cache=True)
        def my_step():
            ...
        ```

    !!! info
        A step with `rerun=True` will not run if there is a cache hit for its
        parent pipeline. This is because the pipeline cache is checked first.

    !!! warning
        A step will not be cached if it is not called from a pipeline.
    """

    def decorator(fn: Callable) -> Callable:
        sname = name or f"{fn.__name__}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            pipe_exec = PipelineExecution._from_context()
            if pipe_exec is None:
                logger.warning(
                    f"Step `{sname}` not called from a pipeline. "
                    f"The result will not be cached."
                )
                return fn(*args, **kwargs)

            _init_devpipe()
            with _get_session(autoflush=False) as session:
                step = Step.get(pipe_exec.pipeline, sname, session)
                if not cache:
                    logger.debug(
                        f"Step `{sname}` is not using cache. "
                        f"Returning step results directly."
                    )
                    return fn(*args, **kwargs)
                inputs, i_bytes = StepInputs.from_object((args, kwargs))
                step = Step.get(pipe_exec.pipeline, sname, session)
                if not rerun:
                    step_exec = StepExecution.get(step, inputs, session)
                    if step_exec:
                        logger.info(f"Cache hit for step {step.uuid}.")
                        pipe_exec.step_executions.append(step_exec)
                        return step_exec.outputs.read()

            step_exec = StepExecution(step_id=step.uuid)
            logger.info(f"Starting step execution {step_exec.uuid}.")
            result = step_exec._run(fn, *args, **kwargs)
            logger.info(f"Step execution {step_exec.uuid} finished.")

            outputs, o_bytes = StepOutputs.from_object(result)
            inputs.save(i_bytes)
            outputs.save(o_bytes)
            step_exec.inputs = inputs
            step_exec.outputs = outputs
            with _get_session() as session:
                session.add(step_exec)
                session.commit()
                session.refresh(step_exec)

            pipe_exec.step_executions.append(step_exec)

            return result

        return wrapper

    return decorator(entrypoint) if entrypoint else decorator


__all__ = ["step"]
