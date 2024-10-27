"""Pipeline models module."""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from sqlalchemy.types import JSON
from sqlmodel import Column, Field, Relationship, Session, select

from .base import (
    TABLES,
    BaseArtifact,
    BaseExecution,
    BaseSQLModel,
)
from .links import PipelineStepExecutionsLink, PipelineStepLink

if TYPE_CHECKING:  # pragma: no cover
    from .step import Step, StepExecution

logger = logging.getLogger(__name__)


class Pipeline(BaseSQLModel, table=True):
    """Pipeline model.

    Attributes:
        name (str): Pipeline name.
        steps (List[Step]): Steps.
        executions (List[PipelineExecution]): Pipeline executions.
    """

    __tablename__ = TABLES.pipe
    name: str = Field(max_length=128, unique=True)
    steps: List["Step"] = Relationship(
        back_populates="pipeline",
        link_model=PipelineStepLink,
    )
    executions: List["PipelineExecution"] = Relationship(
        back_populates="pipeline",
    )

    @classmethod
    def get(
        cls,
        name: str,
        session: Session,
    ) -> "Pipeline":
        """Get or create pipeline.

        Args:
            name (str): Pipeline name.
            session (Session): Database session.

        Returns:
            Pipeline.
        """
        statement = select(cls).where(cls.name == name)
        pipe = session.exec(statement).first()
        if pipe:
            return pipe
        pipe = cls(name=name)
        session.add(pipe)
        session.commit()
        session.refresh(pipe)
        return pipe


class PipelineExecution(BaseExecution, table=True):
    """Pipeline execution model.

    Attributes:
        pipeline_id (Optional[str]): Pipeline ID.
        meta (Dict[str, Any]): Metadata.
        pipeline (Optional[Pipeline]): Pipeline.
        inputs (Optional[PipelineInputs]): Pipeline inputs.
        outputs (Optional[PipelineOutputs]): Pipeline outputs.
        step_executions (List[StepExecution]): Step executions.
    """

    __tablename__ = TABLES.pipe_exec
    pipeline_id: Optional[str] = Field(
        default=None,
        max_length=36,
        foreign_key=f"{TABLES.pipe}.uuid",
    )
    meta: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
    )
    pipeline: Optional["Pipeline"] = Relationship(
        back_populates="executions",
    )
    inputs: Optional["PipelineInputs"] = Relationship(
        back_populates="pipeline_execution",
    )
    outputs: Optional["PipelineOutputs"] = Relationship(
        back_populates="pipeline_execution",
    )
    step_executions: List["StepExecution"] = Relationship(
        back_populates="pipeline_executions",
        link_model=PipelineStepExecutionsLink,
    )

    @classmethod
    def get(
        cls,
        pipeline: "Pipeline",
        inputs: "PipelineInputs",
        session: Session,
    ) -> Optional["PipelineExecution"]:
        """Get pipeline execution from inputs.

        Args:
            pipeline (Pipeline): Pipeline.
            inputs (PipelineInputs): Pipeline inputs.
            session (Session): Database session.

        Returns:
            Pipeline execution if found, otherwise None.
        """
        statement = (
            select(cls)
            .join(Pipeline)
            .join(PipelineInputs)
            .where(
                Pipeline.uuid == pipeline.uuid,
                PipelineInputs.hash == inputs.hash,
            )
            .order_by(cls.created_at.desc())
        )
        return session.exec(statement).first()


class PipelineInputs(BaseArtifact, table=True):
    """Pipeline inputs model.

    Attributes:
        pipeline_execution_id (Optional[str]): Pipeline execution ID.
        pipeline_execution (Optional[PipelineExecution]): Pipeline execution.
    """

    __tablename__ = TABLES.pipe_inps
    pipeline_execution_id: Optional[str] = Field(
        default=None,
        max_length=36,
        foreign_key=f"{TABLES.pipe_exec}.uuid",
    )
    pipeline_execution: Optional["PipelineExecution"] = Relationship(
        back_populates="inputs",
    )


class PipelineOutputs(BaseArtifact, table=True):
    """Pipeline outputs model.

    Attributes:
        pipeline_execution_id (Optional[str]): Pipeline execution ID.
        pipeline_execution (Optional[PipelineExecution]): Pipeline execution.
    """

    __tablename__ = TABLES.pipe_outs
    pipeline_execution_id: Optional[str] = Field(
        default=None,
        max_length=36,
        foreign_key=f"{TABLES.pipe_exec}.uuid",
    )
    pipeline_execution: Optional["PipelineExecution"] = Relationship(
        back_populates="outputs",
    )


__all__ = [
    "Pipeline",
    "PipelineExecution",
    "PipelineInputs",
    "PipelineOutputs",
]
