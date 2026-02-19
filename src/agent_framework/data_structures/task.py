"""Task definition for agent execution."""

from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class Task(BaseModel):
    """
    A task to be executed by an agent.
    
    Represents the high-level goal or instruction that the agent
    needs to accomplish.
    """
    
    id: str = Field(description="Unique task identifier")
    instruction: str = Field(description="The task instruction/goal")
    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context for the task"
    )
    max_steps: int = Field(
        default=10,
        description="Maximum number of processing steps"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional metadata"
    )
