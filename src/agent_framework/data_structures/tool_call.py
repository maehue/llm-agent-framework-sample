"""Tool call representation."""

from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


class ToolCall(BaseModel):
    """
    Represents a tool invocation request from the LLM.
    
    This is the structured format for tool calls that follows
    the OpenAI function calling convention.
    """
    
    id: str = Field(description="Unique identifier for this tool call")
    name: str = Field(description="Name of the tool to call")
    arguments: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments to pass to the tool"
    )
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolCall":
        """Create ToolCall from dictionary format."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            arguments=data.get("arguments", {})
        )
