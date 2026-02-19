"""
Example 04: A2A Stub

Demonstrates:
- Setting up multiple specialist agents
- Coordinating task delegation
- Combining results from specialists
"""

import sys
sys.path.insert(0, 'src')

from agent_framework.llms import MockLLM
from agent_framework.tools import ToolRegistry, EchoTool, MathEvalTool
from agent_framework.agent import LLMAgent
from agent_framework.a2a import A2ACoordinator
from agent_framework.data_structures import Task


def main():
    print("=" * 60)
    print("Example 04: A2A Stub (Agent-to-Agent)")
    print("=" * 60)
    
    # Create main agent
    print("\n1. Setting up agents...")
    main_registry = ToolRegistry()
    main_registry.register(EchoTool())
    main_llm = MockLLM(scripted_responses={
        "coordinate": {
            "content": "I will coordinate the task.",
            "tool_calls": []
        }
    })
    main_agent = LLMAgent(llm=main_llm, tool_registry=main_registry)
    
    # Create math specialist
    math_registry = ToolRegistry()
    math_registry.register(MathEvalTool())
    math_llm = MockLLM(scripted_responses={
        "math": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_math",
                    "name": "math_eval",
                    "arguments": {"a": 50, "operator": "+", "b": 25}
                }
            ]
        }
    })
    math_specialist = LLMAgent(llm=math_llm, tool_registry=math_registry)
    
    # Create echo specialist
    echo_registry = ToolRegistry()
    echo_registry.register(EchoTool())
    echo_llm = MockLLM(scripted_responses={
        "echo": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_echo",
                    "name": "echo",
                    "arguments": {"message": "Task delegated successfully!"}
                }
            ]
        }
    })
    echo_specialist = LLMAgent(llm=echo_llm, tool_registry=echo_registry)
    
    # Create coordinator
    coordinator = A2ACoordinator(main_agent=main_agent)
    coordinator.register_specialist("math_specialist", math_specialist)
    coordinator.register_specialist("echo_specialist", echo_specialist)
    
    print("   Registered specialists:")
    for name in coordinator.specialist_agents.keys():
        print(f"   - {name}")
    
    # Create main task with decomposition
    print("\n2. Creating task decomposition...")
    main_task = Task(
        id="task_coordinated",
        instruction="Calculate 50 + 25 and echo a success message",
        max_steps=3
    )
    
    decomposition = [
        {
            "instruction": "Calculate 50 + 25",
            "specialist": "math_specialist",
            "max_steps": 2
        },
        {
            "instruction": "Echo: Task delegated successfully!",
            "specialist": "echo_specialist",
            "max_steps": 2
        }
    ]
    
    print("   Subtasks:")
    for i, subtask in enumerate(decomposition, 1):
        print(f"   {i}. {subtask['instruction']} -> {subtask['specialist']}")
    
    # Execute coordinated task
    print("\n3. Executing coordinated task...")
    result = coordinator.coordinate_task(main_task, decomposition)
    
    # Display results
    print("\n4. Results:")
    for subtask_result in result["subtask_results"]:
        print(f"\n   Subtask: {subtask_result['subtask']}")
        print(f"   Status: {subtask_result['status']}")
        print(f"   Result: {subtask_result['result']}")
    
    print(f"\n5. Overall status: {result['status']}")
    
    print("\n" + "=" * 60)
    print("A2A coordination demonstrated!")
    print("Note: This is an in-process stub. Real A2A would use")
    print("network communication (HTTP, message queues, etc.)")
    print("=" * 60)


if __name__ == "__main__":
    main()
