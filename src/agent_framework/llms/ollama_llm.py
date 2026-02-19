"""Ollama LLM adapter (stub implementation)."""

from __future__ import annotations
from typing import Any, Optional
from ..base.llm import BaseLLM, LLMResponse


class OllamaLLM(BaseLLM):
    """
    Ollama LLM adapter.
    
    TODO: Implement actual Ollama API integration.
    This is a stub for now.
    """
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama LLM.
        
        Args:
            model: Model name (e.g., 'llama2', 'mistral')
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
    
    def generate(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        response_format: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate response using Ollama.
        
        TODO: Implement actual API calls to Ollama.
        For now, returns a placeholder response.
        """
        # Placeholder implementation
        return LLMResponse(
            content="[Ollama stub - not yet implemented]",
            tool_calls=[],
            finish_reason="stop"
        )
