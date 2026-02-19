"""Trajectory tracking for agent execution."""

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from .tool_call import ToolCall
from .tool_call_result import ToolCallResult


class TrajectoryStep(BaseModel):
    """
    A single step in the agent's execution trajectory.
    
    Each step captures:
    - What the agent decided to do (tool calls or response)
    - The results of those actions
    - Timing information
    """
    
    step_index: int = Field(description="Step number in the trajectory")
    timestamp: datetime = Field(default_factory=datetime.now)
    plan: Optional[str] = Field(default=None, description="Agent's plan/intent for this step")
    llm_response: Optional[str] = Field(default=None, description="Text response from LLM")
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_results: list[ToolCallResult] = Field(default_factory=list)
    latency_ms: Optional[float] = Field(default=None, description="Step execution time")
    metadata: dict[str, Any] = Field(default_factory=dict)


class Trajectory(BaseModel):
    """
    Complete execution trajectory for a task.
    
    Captures the step-by-step trace of how the agent processed a task,
    enabling debugging, monitoring, and learning from execution history.
    """
    
    task_id: str = Field(description="ID of the task this trajectory is for")
    steps: list[TrajectoryStep] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = Field(default=None)
    final_result: Optional[Any] = Field(default=None)
    status: str = Field(default="in_progress", description="Status: in_progress, completed, failed, max_steps_reached")
    
    def add_step(self, step: TrajectoryStep) -> None:
        """Add a step to the trajectory."""
        self.steps.append(step)
    
    def complete(self, result: Any, status: str = "completed") -> None:
        """Mark trajectory as complete."""
        self.end_time = datetime.now()
        self.final_result = result
        self.status = status
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        return self.model_dump()
