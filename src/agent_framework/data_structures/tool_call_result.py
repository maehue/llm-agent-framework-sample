"""Tool call result representation."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ToolCallResult(BaseModel):
    """
    Result of executing a tool call.
    
    Captures both successful results and errors that occur during
    tool execution.
    """
    
    tool_call_id: str = Field(description="ID of the tool call this result is for")
    tool_name: str = Field(description="Name of the tool that was called")
    result: Any = Field(default=None, description="The result value from the tool")
    error: Optional[str] = Field(default=None, description="Error message if tool failed")
    is_error: bool = Field(default=False, description="Whether an error occurred")
    
    def to_message(self) -> dict[str, Any]:
        """Convert to message format for LLM context."""
        return {
            "role": "tool",
            "tool_call_id": self.tool_call_id,
            "name": self.tool_name,
            "content": str(self.error if self.is_error else self.result)
        }
