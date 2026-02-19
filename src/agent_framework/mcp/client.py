"""MCP client adapter interface."""

from typing import Any, Optional
from abc import ABC, abstractmethod


class MCPClient(ABC):
    """
    Abstract MCP client interface.
    
    The Model Context Protocol allows agents to discover and use
    external tools/resources provided by MCP servers.
    
    This is a minimal stub for the MVP. A full implementation would:
    - Connect to MCP servers via stdio/HTTP
    - Discover available tools
    - Execute tool calls via the protocol
    """
    
    @abstractmethod
    def connect(self, server_config: dict[str, Any]) -> None:
        """
        Connect to an MCP server.
        
        Args:
            server_config: Configuration for the MCP server
        """
        pass
    
    @abstractmethod
    def list_tools(self) -> list[dict[str, Any]]:
        """
        List tools available from the MCP server.
        
        Returns:
            List of tool specifications
        """
        pass
    
    @abstractmethod
    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """
        Call a tool via the MCP protocol.
        
        Args:
            name: Tool name
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        pass


class SimpleMCPClient(MCPClient):
    """
    Simple stub implementation of MCP client.
    
    TODO: Implement actual MCP protocol communication.
    """
    
    def __init__(self):
        self.connected = False
        self.server_config = None
    
    def connect(self, server_config: dict[str, Any]) -> None:
        """Connect to MCP server (stub)."""
        self.server_config = server_config
        self.connected = True
    
    def list_tools(self) -> list[dict[str, Any]]:
        """List tools (returns empty list in stub)."""
        return []
    
    def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """Call tool (stub)."""
        return {"error": "MCP client not fully implemented"}
    
    def disconnect(self) -> None:
        """Disconnect (stub)."""
        self.connected = False
