"""LLM implementations."""

from .mock_llm import MockLLM
from .ollama_llm import OllamaLLM

__all__ = ["MockLLM", "OllamaLLM"]
