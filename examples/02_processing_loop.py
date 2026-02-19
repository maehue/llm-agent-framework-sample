"""
Example 02: Processing Loop

Demonstrates:
- Creating an LLM agent with processing loop
- Executing a multi-step task
- Capturing a trajectory
"""

import sys
sys.path.insert(0, 'src')

from agent_framework.llms import MockLLM
from agent_framework.tools import ToolRegistry, EchoTool, MathEvalTool
from agent_framework.agent import LLMAgent
from agent_framework.data_structures import Task
import json


def main():
    print("=" * 60)
    print("Example 02: Processing Loop")
    print("=" * 60)
    
    # Setup scripted LLM responses
    scripted_responses = {
        "calculate": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_1",
                    "name": "math_eval",
                    "arguments": {"a": 100, "operator": "*", "b": 2}
                }
            ]
        },
        "echo": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_2",
                    "name": "echo",
                    "arguments": {"message": "Calculation complete!"}
                }
            ]
        }
    }
    
    # Create LLM and tool registry
    llm = MockLLM(scripted_responses=scripted_responses)
    registry = ToolRegistry()
    registry.register(EchoTool())
    registry.register(MathEvalTool())
    
    # Create agent
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    # Create task
    task = Task(
        id="task_001",
        instruction="Calculate 100 * 2, then echo a completion message",
        max_steps=5
    )
    
    print(f"\n1. Task: {task.instruction}")
    print(f"   Max steps: {task.max_steps}")
    
    # Run agent
    print("\n2. Executing task...")
    result = agent.run(task)
    
    # Display trajectory
    print("\n3. Trajectory:")
    for step in result.trajectory.steps:
        print(f"\n   Step {step.step_index}:")
        print(f"   - Timestamp: {step.timestamp}")
        print(f"   - Tool calls: {len(step.tool_calls)}")
        for tc in step.tool_calls:
            print(f"     * {tc.name}({tc.arguments})")
        print(f"   - Tool results: {len(step.tool_results)}")
        for tr in step.tool_results:
            if tr.is_error:
                print(f"     * ERROR: {tr.error}")
            else:
                print(f"     * {tr.tool_name} -> {tr.result}")
        if step.latency_ms:
            print(f"   - Latency: {step.latency_ms:.2f}ms")
    
    print(f"\n4. Final result:")
    print(f"   Status: {result.status}")
    print(f"   Total steps: {len(result.trajectory.steps)}")
    
    # Export trajectory as JSON
    print("\n5. Trajectory JSON (truncated):")
    trajectory_dict = result.trajectory.to_dict()
    print(json.dumps(trajectory_dict, indent=2, default=str)[:500] + "...")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
