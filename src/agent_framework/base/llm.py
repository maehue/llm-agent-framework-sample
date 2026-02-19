"""
BaseLLM: Abstract interface for the backbone LLM.

This module defines the contract that all LLM implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel


class LLMResponse(BaseModel):
    """Response from an LLM generation call."""
    content: Optional[str] = None
    tool_calls: list[dict[str, Any]] = []
    finish_reason: Optional[str] = None


class BaseLLM(ABC):
    """
    Abstract base class for LLM implementations.
    
    The backbone LLM is responsible for:
    - Processing conversation history
    - Generating text responses
    - Deciding when to call tools
    - Structuring tool calls in a standard format
    """
    
    @abstractmethod
    def generate(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        response_format: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a response given conversation history and available tools.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool specifications
            response_format: Optional response formatting instructions
            **kwargs: Additional LLM-specific parameters
            
        Returns:
            LLMResponse with content and/or tool_calls
        """
        pass
