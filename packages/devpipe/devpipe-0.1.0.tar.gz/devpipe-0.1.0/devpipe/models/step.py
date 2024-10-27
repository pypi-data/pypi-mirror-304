"""Step models module."""

from typing import Any, Dict, List, Optional

from sqlalchemy.types import JSON
from sqlmodel import Column, Field, Relationship, Session, select

from .base import (
    TABLES,
    BaseArtifact,
    BaseExecution,
    BaseSQLModel,
)
from .links import PipelineStepExecutionsLink, PipelineStepLink
from .pipeline import Pipeline, PipelineExecution


class Step(BaseSQLModel, table=True):
    """Step model.

    Attributes:
        name (str): Step name.
        pipeline (Optional[Pipeline]): Pipeline.
        executions (List[StepExecution]): Step executions.
    """

    __tablename__ = TABLES.step
    name: str = Field(max_length=128)
    pipeline: Optional["Pipeline"] = Relationship(
        back_populates="steps",
        link_model=PipelineStepLink,
    )
    executions: List["StepExecution"] = Relationship(
        back_populates="step",
    )

    @classmethod
    def get(
        cls,
        pipeline: "Pipeline",
        name: str,
        session: Session,
    ) -> "Pipeline":
        """Get or create step.

        Args:
            pipeline (Pipeline): Pipeline.
            name (str): Step name.
            session (Session): Database session.

        Returns:
            Step.
        """
        pipe = session.get(Pipeline, pipeline.uuid)
        statement = (
            select(cls)
            .join(PipelineStepLink)
            .join(Pipeline)
            .where(
                Pipeline.uuid == pipe.uuid,
                cls.name == name,
            )
        )
        step = session.exec(statement).first()
        if step:
            return step
        step = cls(name=name, pipeline=pipe)
        session.add(step)
        session.commit()
        session.refresh(step)
        return step


class StepExecution(BaseExecution, table=True):
    """Step execution model.

    Attributes:
        step_id (Optional[str]): Step ID.
        meta (Dict[str, Any]): Metadata.
        step (Optional[Step]): Step.
        pipeline_executions (List[PipelineExecution]): Pipeline executions.
        inputs (Optional[StepInputs]): Step inputs.
        outputs (Optional[StepOutputs]): Step outputs.
    """

    __tablename__ = TABLES.step_exec
    step_id: Optional[str] = Field(
        default=None,
        foreign_key=f"{TABLES.step}.uuid",
    )
    meta: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
    )
    step: Optional["Step"] = Relationship(
        back_populates="executions",
    )
    pipeline_executions: List["PipelineExecution"] = Relationship(
        back_populates="step_executions",
        link_model=PipelineStepExecutionsLink,
    )
    inputs: Optional["StepInputs"] = Relationship(
        back_populates="step_execution",
    )
    outputs: Optional["StepOutputs"] = Relationship(
        back_populates="step_execution",
    )

    @classmethod
    def get(
        cls,
        step: "Step",
        inputs: "StepInputs",
        session: Session,
    ) -> Optional["StepExecution"]:
        """Get step execution from inputs.

        Args:
            step (Step): Step.
            inputs (StepInputs): Step inputs.
            session (Session): Database session.

        Returns:
            Step execution if found, otherwise None.
        """
        statement = (
            select(cls)
            .join(Step)
            .join(StepInputs)
            .where(
                Step.uuid == step.uuid,
                StepInputs.hash == inputs.hash,
            )
            .order_by(cls.created_at.desc())
        )
        return session.exec(statement).first()


class StepInputs(BaseArtifact, table=True):
    """Step inputs model.

    Attributes:
        step_execution_id (Optional[str]): Step execution ID.
        step_execution (Optional[StepExecution]): Step execution.
    """

    __tablename__ = TABLES.step_inps
    step_execution_id: Optional[str] = Field(
        default=None,
        foreign_key=f"{TABLES.step_exec}.uuid",
    )
    step_execution: Optional["StepExecution"] = Relationship(
        back_populates="inputs",
    )


class StepOutputs(BaseArtifact, table=True):
    """Step outputs model.

    Attributes:
        step_execution_id (Optional[str]): Step execution ID.
        step_execution (Optional[StepExecution]): Step execution.
    """

    __tablename__ = TABLES.step_outs
    step_execution_id: Optional[str] = Field(
        default=None,
        foreign_key=f"{TABLES.step_exec}.uuid",
    )
    step_execution: Optional["StepExecution"] = Relationship(
        back_populates="outputs",
    )


__all__ = [
    "Step",
    "StepExecution",
    "StepInputs",
    "StepOutputs",
]
