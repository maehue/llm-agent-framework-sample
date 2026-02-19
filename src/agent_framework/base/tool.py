"""
BaseTool: Abstract interface for agent tools.

Tools are callable functions that agents can invoke to perform actions.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """
    Abstract base class for tools that agents can call.
    
    Each tool must define:
    - name: Unique identifier for the tool
    - description: Human-readable explanation of what the tool does
    - params_schema: JSON schema describing the tool's parameters
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does."""
        pass
    
    @property
    @abstractmethod
    def params_schema(self) -> dict[str, Any]:
        """JSON schema for tool parameters."""
        pass
    
    @abstractmethod
    def __call__(self, **kwargs) -> Any:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool parameters matching params_schema
            
        Returns:
            ToolCallResult or raw result value
        """
        pass
    
    def to_dict(self) -> dict[str, Any]:
        """Convert tool to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.params_schema
            }
        }
