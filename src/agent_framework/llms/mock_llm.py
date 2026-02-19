"""Mock LLM for testing and demonstrations."""

from typing import Any, Optional
from ..base.llm import BaseLLM, LLMResponse


class MockLLM(BaseLLM):
    """
    Deterministic mock LLM for testing.
    
    Returns scripted responses based on simple pattern matching.
    Useful for stable tests and demonstrations.
    """
    
    def __init__(self, scripted_responses: Optional[dict[str, dict]] = None):
        """
        Initialize mock LLM.
        
        Args:
            scripted_responses: Dict mapping message patterns to responses.
                Each response can have 'content' and/or 'tool_calls'.
        """
        self.scripted_responses = scripted_responses or {}
        self.call_count = 0
    
    def generate(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        response_format: Optional[dict[str, Any]] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate a mock response.
        
        Looks for patterns in the last user message and returns
        the corresponding scripted response.
        """
        self.call_count += 1
        
        # Get last user message
        last_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_message = msg.get("content", "").lower()
                break
        
        # Check for scripted responses
        for pattern, response in self.scripted_responses.items():
            if pattern.lower() in last_message:
                return LLMResponse(
                    content=response.get("content"),
                    tool_calls=response.get("tool_calls", []),
                    finish_reason="stop"
                )
        
        # Default response
        if tools and len(tools) > 0:
            # If tools available, return a simple tool call
            return LLMResponse(
                content=None,
                tool_calls=[
                    {
                        "id": f"call_{self.call_count}",
                        "name": tools[0]["function"]["name"],
                        "arguments": {}
                    }
                ],
                finish_reason="tool_calls"
            )
        
        # Otherwise return a simple text response
        return LLMResponse(
            content="I understand. Task complete.",
            tool_calls=[],
            finish_reason="stop"
        )
