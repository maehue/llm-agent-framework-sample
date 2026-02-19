"""Base interfaces for LLM and Tool abstractions."""

from .llm import BaseLLM, LLMResponse
from .tool import BaseTool

__all__ = ["BaseLLM", "LLMResponse", "BaseTool"]
