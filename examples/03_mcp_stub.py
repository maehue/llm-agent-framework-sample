"""
Example 03: MCP Stub

Demonstrates:
- Loading external tools via MCP provider
- Registering MCP tools in the registry
- Using MCP tools in an agent
"""

import sys
sys.path.insert(0, 'src')

from agent_framework.llms import MockLLM
from agent_framework.tools import ToolRegistry
from agent_framework.mcp import MockMCPProvider, MockWeatherTool
from agent_framework.agent import LLMAgent
from agent_framework.data_structures import Task


def main():
    print("=" * 60)
    print("Example 03: MCP Stub")
    print("=" * 60)
    
    # Create tool registry
    registry = ToolRegistry()
    
    # Create MCP provider with mock external tools
    print("\n1. Loading MCP tools...")
    mcp_provider = MockMCPProvider(mock_tools=[MockWeatherTool()])
    mcp_provider.load_tools(registry)
    
    print("   Registered tools after MCP load:")
    for tool in registry.list():
        print(f"   - {tool.name}: {tool.description}")
    
    # Setup LLM to use the weather tool
    scripted_responses = {
        "weather": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_weather",
                    "name": "get_weather",
                    "arguments": {"location": "San Francisco"}
                }
            ]
        }
    }
    
    llm = MockLLM(scripted_responses=scripted_responses)
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    # Create task
    task = Task(
        id="task_weather",
        instruction="What's the weather in San Francisco?",
        max_steps=3
    )
    
    print(f"\n2. Task: {task.instruction}")
    
    # Run agent
    print("\n3. Executing task with MCP tool...")
    result = agent.run(task)
    
    # Display results
    print("\n4. Results:")
    for step in result.trajectory.steps:
        for tool_result in step.tool_results:
            if not tool_result.is_error:
                print(f"   Tool: {tool_result.tool_name}")
                print(f"   Result: {tool_result.result}")
    
    print(f"\n5. Status: {result.status}")
    
    print("\n" + "=" * 60)
    print("MCP integration demonstrated!")
    print("Note: This is a mock implementation. Real MCP would")
    print("connect to external MCP servers via stdio/HTTP.")
    print("=" * 60)


if __name__ == "__main__":
    main()
