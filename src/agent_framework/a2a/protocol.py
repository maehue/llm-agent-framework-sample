"""A2A protocol message schemas."""

from __future__ import annotations
from typing import Any, Optional, Literal
from pydantic import BaseModel, Field


class A2AMessage(BaseModel):
    """Base message for agent-to-agent communication."""
    message_type: str = Field(description="Type of message")
    sender_id: str = Field(description="ID of the sending agent")
    recipient_id: Optional[str] = Field(default=None, description="ID of recipient agent (None for broadcast)")
    message_id: str = Field(description="Unique message ID")


class TaskRequest(A2AMessage):
    """Request to perform a task."""
    message_type: Literal["task_request"] = "task_request"
    task_id: str = Field(description="ID of the task")
    instruction: str = Field(description="Task instruction")
    context: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0, description="Task priority (higher = more urgent)")


class TaskResponse(A2AMessage):
    """Response with task results."""
    message_type: Literal["task_response"] = "task_response"
    task_id: str = Field(description="ID of the task this is responding to")
    status: str = Field(description="Status: success, failure, in_progress")
    result: Optional[Any] = Field(default=None, description="Task result")
    error: Optional[str] = Field(default=None, description="Error message if failed")


class CapabilitiesAdvertisement(A2AMessage):
    """Advertisement of agent capabilities."""
    message_type: Literal["capabilities"] = "capabilities"
    capabilities: list[str] = Field(description="List of capabilities")
    available_tools: list[str] = Field(default_factory=list, description="Available tool names")
    specializations: list[str] = Field(default_factory=list, description="Agent specializations")
