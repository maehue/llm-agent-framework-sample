"""MCP provider that loads external tools into the registry."""

from typing import Any, Optional
from abc import ABC, abstractmethod

from ..base.tool import BaseTool
from ..tools.registry import ToolRegistry
from .client import MCPClient


class MCPProvider(ABC):
    """
    Abstract provider that loads MCP tools into the tool registry.
    
    Responsibilities:
    - Connect to MCP servers
    - Fetch tool specifications
    - Create tool wrappers
    - Register tools in the agent's registry
    """
    
    @abstractmethod
    def load_tools(self, registry: ToolRegistry) -> None:
        """
        Load tools from MCP into the registry.
        
        Args:
            registry: Tool registry to load tools into
        """
        pass


class MockMCPProvider(MCPProvider):
    """
    Mock MCP provider for demonstrations.
    
    Simulates loading external tools without actual MCP protocol.
    """
    
    def __init__(self, mock_tools: Optional[list[BaseTool]] = None):
        """
        Initialize mock provider.
        
        Args:
            mock_tools: List of mock tools to provide
        """
        self.mock_tools = mock_tools or []
    
    def load_tools(self, registry: ToolRegistry) -> None:
        """
        Load mock tools into registry.
        
        Args:
            registry: Tool registry to load tools into
        """
        for tool in self.mock_tools:
            registry.register(tool)


class MockWeatherTool(BaseTool):
    """Mock weather tool for MCP demonstration."""
    
    @property
    def name(self) -> str:
        return "get_weather"
    
    @property
    def description(self) -> str:
        return "Get current weather for a location (mock MCP tool)"
    
    @property
    def params_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or location"
                }
            },
            "required": ["location"]
        }
    
    def __call__(self, location: str, **kwargs) -> str:
        """Return mock weather data."""
        return f"Weather in {location}: Sunny, 22°C (Mock data from MCP)"
