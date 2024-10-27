"""Database module."""

import logging
from typing import Any, Optional

from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from .config import CONFIG

logger = logging.getLogger(__name__)

DEVPIPE = {}


def set_engine(engine: Optional[Engine] = None) -> Engine:
    """Set engine.

    Args:
        engine (Optional[Engine], optional): SQLALchemy engine.

    Returns:
        SQLALchemy engine.

    Example:
        ```python
        from sqlalchemy import create_engine

        import devpipe as dp
        from devpipe.database import set_engine

        engine = create_engine("sqlite:///devpipe.db")
        set_engine(engine)

        @dp.pipeline
        def my_pipeline():
            ...
        ```
    """
    if engine is None:
        engine = create_engine(CONFIG.database_url)
    DEVPIPE["engine"] = engine
    logger.debug(f"Engine set with driver `{engine.driver}`.")
    return DEVPIPE["engine"]


def _get_engine() -> Engine:
    """Get engine.

    Returns:
        SQLALchemy engine.

    Example:
        ```python
        from sqlmodel import Session, select

        from devpipe.database import get_engine
        from devpipe.models import Pipeline

        engine = get_engine()
        with Session(engine) as session:
            stmt = select(Pipeline).where(Pipeline.name == "my_pipeline")
            pipeline = session.exec(stmt).one()
        ```
    """
    return DEVPIPE.get("engine") or set_engine()


def _get_session(*args: Any, **kwargs: Any) -> Session:
    """Get session.

    Args:
        *args (Any): Arguments for Session initialization.
        **kwargs (Any): Keyword arguments Session initialization.

    Returns:
        SQLModel Session.

    Example:
        ```python
        from sqlmodel import select

        from devpipe.database import get_session
        from devpipe.models import PipelineExecution

        with get_session() as session:
            stmt = (
                select(PipelineExecution)
                .where(PipelineExecution.uuid == "...")
            )
            pipe_exec = session.exec(stmt).one()
        ```
    """
    return Session(_get_engine(), *args, **kwargs)


def create_tables() -> None:
    """Create tables.

    Example:
        ```python
        from sqlalchemy import create_engine

        from devpipe.database import set_engine, create_tables

        engine = create_engine("sqlite:///devpipe.db")
        set_engine(engine)
        create_tables()
        ```
    """
    from .models.base import BaseSQLModel

    BaseSQLModel.metadata.create_all(_get_engine())


def drop_tables() -> None:
    """Drop tables.

    Example:
        ```python
        from sqlalchemy import create_engine

        from devpipe.database import set_engine, drop_tables

        engine = create_engine("sqlite:///devpipe.db")
        set_engine(engine)
        drop_tables()
        ```
    """
    from .models.base import BaseSQLModel

    BaseSQLModel.metadata.drop_all(_get_engine())


__all__ = [
    "set_engine",
    "_get_engine",
    "_get_session",
    "create_tables",
    "drop_tables",
]
