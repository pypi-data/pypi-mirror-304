"""Link models module."""

from typing import Optional

from sqlmodel import Field

from .base import (
    TABLES,
    BaseSQLModel,
)


class PipelineStepLink(BaseSQLModel, table=True):
    """Pipeline step link model.

    Attributes:
        pipeline_id (Optional[str]): Pipeline UUID.
        step_id (Optional[str]): Step UUID.
    """

    __tablename__ = TABLES.pipe_step_link
    pipeline_id: Optional[str] = Field(
        max_length=36,
        foreign_key=f"{TABLES.pipe}.uuid",
    )
    step_id: Optional[str] = Field(
        max_length=36,
        foreign_key=f"{TABLES.step}.uuid",
    )


class PipelineStepExecutionsLink(BaseSQLModel, table=True):
    """Pipeline step executions link model.

    Attributes:
        pipeline_execution_id (Optional[str]): Pipeline execution UUID.
        step_execution_id (Optional[str]): Step execution UUID.
    """

    __tablename__ = TABLES.pipe_step_exec_link
    pipeline_execution_id: Optional[str] = Field(
        max_length=36,
        foreign_key=f"{TABLES.pipe_exec}.uuid",
    )
    step_execution_id: Optional[str] = Field(
        max_length=36,
        foreign_key=f"{TABLES.step_exec}.uuid",
    )


__all__ = ["PipelineStepLink", "PipelineStepExecutionsLink"]
