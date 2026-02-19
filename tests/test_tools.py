"""Basic tests for tool registry and tool execution."""

import sys
sys.path.insert(0, 'src')

from agent_framework.tools import ToolRegistry, EchoTool, MathEvalTool
from agent_framework.data_structures import ToolCall
import pytest


def test_tool_registration():
    """Test registering tools in the registry."""
    registry = ToolRegistry()
    tool = EchoTool()
    
    registry.register(tool)
    assert registry.get("echo") is not None
    assert len(registry.list()) == 1


def test_duplicate_registration_fails():
    """Test that duplicate registration raises error."""
    registry = ToolRegistry()
    tool = EchoTool()
    
    registry.register(tool)
    with pytest.raises(ValueError):
        registry.register(tool, replace=False)


def test_duplicate_registration_with_replace():
    """Test that duplicate registration works with replace=True."""
    registry = ToolRegistry()
    tool = EchoTool()
    
    registry.register(tool)
    registry.register(tool, replace=True)
    assert len(registry.list()) == 1


def test_tool_execution():
    """Test executing a tool call."""
    registry = ToolRegistry()
    registry.register(EchoTool())
    
    tool_call = ToolCall(
        id="test_1",
        name="echo",
        arguments={"message": "test message"}
    )
    
    result = registry.execute(tool_call)
    assert result.is_error is False
    assert result.result == "test message"


def test_tool_not_found():
    """Test executing nonexistent tool."""
    registry = ToolRegistry()
    
    tool_call = ToolCall(
        id="test_2",
        name="nonexistent",
        arguments={}
    )
    
    result = registry.execute(tool_call)
    assert result.is_error is True
    assert "not found" in result.error


def test_math_tool():
    """Test math evaluation tool."""
    registry = ToolRegistry()
    registry.register(MathEvalTool())
    
    tool_call = ToolCall(
        id="test_3",
        name="math_eval",
        arguments={"a": 10, "operator": "+", "b": 5}
    )
    
    result = registry.execute(tool_call)
    assert result.is_error is False
    assert result.result == 15


def test_tool_list_for_llm():
    """Test converting tools to LLM format."""
    registry = ToolRegistry()
    registry.register(EchoTool())
    registry.register(MathEvalTool())
    
    tools = registry.list_for_llm()
    assert len(tools) == 2
    assert all("function" in tool for tool in tools)
    assert all("name" in tool["function"] for tool in tools)
