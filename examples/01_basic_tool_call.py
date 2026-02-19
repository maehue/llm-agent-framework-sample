"""
Example 01: Basic Tool Call

Demonstrates:
- Creating a tool registry
- Registering builtin tools
- Making a simple tool call
"""

import sys
sys.path.insert(0, 'src')

from agent_framework.tools import ToolRegistry, EchoTool, MathEvalTool
from agent_framework.data_structures import ToolCall


def main():
    print("=" * 60)
    print("Example 01: Basic Tool Call")
    print("=" * 60)
    
    # Create registry and register tools
    registry = ToolRegistry()
    registry.register(EchoTool())
    registry.register(MathEvalTool())
    
    print("\n1. Registered tools:")
    for tool in registry.list():
        print(f"   - {tool.name}: {tool.description}")
    
    # Test echo tool
    print("\n2. Testing echo tool:")
    echo_call = ToolCall(
        id="call_1",
        name="echo",
        arguments={"message": "Hello from the agent framework!"}
    )
    result = registry.execute(echo_call)
    print(f"   Input: {echo_call.arguments['message']}")
    print(f"   Output: {result.result}")
    
    # Test math tool
    print("\n3. Testing math_eval tool:")
    math_call = ToolCall(
        id="call_2",
        name="math_eval",
        arguments={"a": 15, "operator": "+", "b": 27}
    )
    result = registry.execute(math_call)
    print(f"   Expression: 15 + 27")
    print(f"   Result: {result.result}")
    
    # Test error handling
    print("\n4. Testing error handling:")
    invalid_call = ToolCall(
        id="call_3",
        name="nonexistent_tool",
        arguments={}
    )
    result = registry.execute(invalid_call)
    print(f"   Error: {result.error}")
    print(f"   Is Error: {result.is_error}")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
