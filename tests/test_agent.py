"""Tests for agent execution."""

import sys
sys.path.insert(0, 'src')

from agent_framework.llms import MockLLM
from agent_framework.tools import ToolRegistry, EchoTool
from agent_framework.agent import LLMAgent
from agent_framework.data_structures import Task


def test_agent_creation():
    """Test creating an agent."""
    llm = MockLLM()
    registry = ToolRegistry()
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    assert agent.llm is not None
    assert agent.tool_registry is not None


def test_agent_runs_task():
    """Test agent executes a task."""
    llm = MockLLM()
    registry = ToolRegistry()
    registry.register(EchoTool())
    
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    task = Task(
        id="test_task",
        instruction="Echo hello",
        max_steps=3
    )
    
    result = agent.run(task)
    
    assert result.task_id == "test_task"
    assert result.trajectory is not None
    assert len(result.trajectory.steps) > 0


def test_agent_stops_at_max_steps():
    """Test agent stops at max steps."""
    # LLM that never signals completion
    llm = MockLLM(scripted_responses={
        "never": {
            "content": None,
            "tool_calls": [
                {
                    "id": "call_x",
                    "name": "echo",
                    "arguments": {"message": "continue"}
                }
            ]
        }
    })
    
    registry = ToolRegistry()
    registry.register(EchoTool())
    
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    task = Task(
        id="test_task",
        instruction="Never stop",
        max_steps=3
    )
    
    result = agent.run(task)
    
    assert result.status == "max_steps_reached"
    assert len(result.trajectory.steps) == 3


def test_agent_completes_successfully():
    """Test agent completes with success."""
    llm = MockLLM(scripted_responses={
        "complete": {
            "content": "Task completed successfully",
            "tool_calls": []
        }
    })
    
    registry = ToolRegistry()
    agent = LLMAgent(llm=llm, tool_registry=registry)
    
    task = Task(
        id="test_task",
        instruction="Complete this task",
        max_steps=5
    )
    
    result = agent.run(task)
    
    assert result.status == "completed"
    assert result.final_answer == "Task completed successfully"
