"""Echo tool - returns the input."""

from __future__ import annotations
from typing import Any
from ...base.tool import BaseTool


class EchoTool(BaseTool):
    """
    Simple echo tool that returns its input.
    
    Useful for testing and demonstrations.
    """
    
    @property
    def name(self) -> str:
        return "echo"
    
    @property
    def description(self) -> str:
        return "Echoes back the input message. Useful for testing."
    
    @property
    def params_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to echo back"
                }
            },
            "required": ["message"]
        }
    
    def __call__(self, message: str, **kwargs) -> str:
        """Echo the message back."""
        return message
