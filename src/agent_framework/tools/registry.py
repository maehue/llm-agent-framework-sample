"""Tool registry for managing available tools."""

from typing import Optional
from ..base.tool import BaseTool
from ..data_structures.tool_call import ToolCall
from ..data_structures.tool_call_result import ToolCallResult


class ToolRegistry:
    """
    Registry for managing tools available to the agent.
    
    Responsibilities:
    - Register/unregister tools
    - Prevent duplicate registrations
    - Execute tool calls
    - List available tools in LLM format
    """
    
    def __init__(self):
        self._tools: dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool, replace: bool = False) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool: The tool to register
            replace: If True, replace existing tool with same name
            
        Raises:
            ValueError: If tool with same name exists and replace=False
        """
        if tool.name in self._tools and not replace:
            raise ValueError(f"Tool '{tool.name}' is already registered. Use replace=True to override.")
        self._tools[tool.name] = tool
    
    def unregister(self, name: str) -> None:
        """Remove a tool from the registry."""
        self._tools.pop(name, None)
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list(self, tags: Optional[list[str]] = None) -> list[BaseTool]:
        """
        List all registered tools.
        
        Args:
            tags: Optional filter by tags (not implemented in MVP)
            
        Returns:
            List of registered tools
        """
        return list(self._tools.values())
    
    def list_for_llm(self) -> list[dict]:
        """List tools in LLM function calling format."""
        return [tool.to_dict() for tool in self._tools.values()]
    
    def execute(self, tool_call: ToolCall) -> ToolCallResult:
        """
        Execute a tool call.
        
        Args:
            tool_call: The tool call to execute
            
        Returns:
            ToolCallResult with result or error
        """
        tool = self.get(tool_call.name)
        
        if tool is None:
            return ToolCallResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                error=f"Tool '{tool_call.name}' not found",
                is_error=True
            )
        
        try:
            result = tool(**tool_call.arguments)
            return ToolCallResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                result=result,
                is_error=False
            )
        except Exception as e:
            return ToolCallResult(
                tool_call_id=tool_call.id,
                tool_name=tool_call.name,
                error=str(e),
                is_error=True
            )
