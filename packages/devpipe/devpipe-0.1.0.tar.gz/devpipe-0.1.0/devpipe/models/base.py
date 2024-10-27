"""Base models module."""

from __future__ import annotations

import inspect
import logging
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Callable, Optional
from uuid import uuid4

import dill as pickle
from pydantic import BaseModel, model_validator
from sqlalchemy.sql import func
from sqlmodel import Field, SQLModel

from ..config import CONFIG
from ..storage import _get_storage

logger = logging.getLogger(__name__)


class Tables(BaseModel):
    """Tables names.

    Attributes:
        pipe (str): Pipeline table.
        pipe_exec (str): Pipeline execution table.
        pipe_inps (str): Pipeline inputs table.
        pipe_outs (str): Pipeline outputs table.
        step (str): Step table.
        step_exec (str): Step execution table.
        step_inps (str): Step inputs table.
        step_outs (str): Step outputs table.
        pipe_step_link (str): Link table for pipelines and steps.
        pipe_step_exec_link (str): Link table for pipeline executions and
            step executions.
    """

    pipe: str = "pipeline"
    pipe_exec: str = "pipeline_execution"
    pipe_inps: str = "pipeline_inputs"
    pipe_outs: str = "pipeline_outputs"
    step: str = "step"
    step_exec: str = "step_execution"
    step_inps: str = "step_inputs"
    step_outs: str = "step_outputs"
    pipe_step_link: str = "link_pipeline_step"
    pipe_step_exec_link: str = "link_pipeline_step_executions"

    @model_validator(mode="after")
    def _add_table_prefix(self):
        for table in self.model_fields:
            base = getattr(self, table)
            name = f"{CONFIG.database_prefix}_{base}"
            setattr(self, table, name)
        return self


class BaseSQLModel(SQLModel):
    """Base SQL model.

    Attributes:
        uuid (str): UUID.
        created_at (datetime): Created at.
    """

    uuid: str = Field(
        default_factory=lambda: uuid4().hex,
        max_length=36,
        primary_key=True,
    )
    created_at: datetime = Field(
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )


class BaseExecution(BaseSQLModel):
    """Base execution model.

    Attributes:
        started_at (Optional[datetime]): Execution start time.
        finished_at (Optional[datetime]): Execution finish time.
    """

    started_at: Optional[datetime] = Field(default=None)
    finished_at: Optional[datetime] = Field(default=None)

    def _run(
        self,
        entrypoint: Callable,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """Run entrypoint.

        Args:
            entrypoint (Callable): Entrypoint.
            *args (Any): Arguments for entrypoint.
            **kwargs (Any): Keyword arguments for entrypoint.

        Returns:
            Result of the entrypoint.
        """
        self.started_at = datetime.now(timezone.utc)
        result = entrypoint(*args, **kwargs)
        self.finished_at = datetime.now(timezone.utc)
        return result

    @classmethod
    def _from_context(cls) -> Optional["BaseExecution"]:
        """Get execution from the current stack."""
        for rec in inspect.stack():
            if rec.function != "_run":
                continue
            execution = rec.frame.f_locals.get("self")
            if isinstance(execution, cls):
                return execution


class BaseArtifact(BaseSQLModel):
    """Base artifact model.

    Attributes:
        storage_key (str): Storage key.
        size (int): Size.
        hash (str): Hash.
    """

    storage_key: str = Field(max_length=1024)
    size: int = Field(ge=0)
    hash: str = Field(max_length=64)

    @classmethod
    def from_object(cls, obj: Any) -> tuple["BaseArtifact", bytes]:
        """Create artifact from object.

        Args:
            obj: Object.

        Returns:
            Artifact.
            Pickled object bytes.
        """
        bytes_obj, obj_hash = cls._pickle_and_hash(obj)
        artifact = cls(
            storage_key=f"{uuid4().hex}.pkl",
            size=len(bytes_obj),
            hash=obj_hash,
        )
        return artifact, bytes_obj

    def read(self) -> Any:
        """Read object from storage.

        Returns:
            Object.
        """
        storage = _get_storage()
        outputs = storage.read(self.storage_key)
        return self._unpickle(outputs)

    def save(self, obj_bytes: bytes) -> "BaseArtifact":
        """Save object to storage.

        Args:
            obj_bytes: Object bytes.

        Returns:
            Artifact.
        """
        storage = _get_storage()
        storage.save(self.storage_key, obj_bytes)
        return self

    @staticmethod
    def _pickle_and_hash(obj: Any) -> tuple[bytes, str]:
        """Pickle an object and hash it.

        Args:
            obj (Any): _description_

        Returns:
            Pickled object.
            Object hash.
        """
        pickled_obj = pickle.dumps(obj)
        obj_hash = sha256(pickled_obj).hexdigest()
        return pickled_obj, obj_hash

    @staticmethod
    def _unpickle(obj: bytes) -> Any:
        """Unpickle an object pickled by `pickle_and_hash`.

        Args:
            obj (bytes): Pickled object.

        Returns:
            Unpickled object.
        """
        return pickle.loads(obj)


TABLES = Tables()


__all__ = [
    "TABLES",
    "BaseArtifact",
    "BaseExecution",
    "BaseSQLModel",
]
