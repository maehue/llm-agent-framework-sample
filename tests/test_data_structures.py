"""Tests for data structures."""

import sys
sys.path.insert(0, 'src')

from agent_framework.data_structures import Task, ToolCall, ToolCallResult, Trajectory, TrajectoryStep


def test_task_creation():
    """Test creating a task."""
    task = Task(
        id="test_task",
        instruction="Do something",
        max_steps=5
    )
    
    assert task.id == "test_task"
    assert task.instruction == "Do something"
    assert task.max_steps == 5


def test_tool_call_creation():
    """Test creating a tool call."""
    tc = ToolCall(
        id="call_1",
        name="echo",
        arguments={"message": "hello"}
    )
    
    assert tc.id == "call_1"
    assert tc.name == "echo"
    assert tc.arguments["message"] == "hello"


def test_tool_call_from_dict():
    """Test creating tool call from dictionary."""
    data = {
        "id": "call_2",
        "name": "test_tool",
        "arguments": {"key": "value"}
    }
    
    tc = ToolCall.from_dict(data)
    assert tc.id == "call_2"
    assert tc.name == "test_tool"


def test_tool_call_result():
    """Test tool call result."""
    result = ToolCallResult(
        tool_call_id="call_1",
        tool_name="echo",
        result="output",
        is_error=False
    )
    
    assert result.tool_call_id == "call_1"
    assert result.result == "output"
    assert result.is_error is False


def test_tool_call_result_error():
    """Test tool call result with error."""
    result = ToolCallResult(
        tool_call_id="call_2",
        tool_name="failing_tool",
        error="Something went wrong",
        is_error=True
    )
    
    assert result.is_error is True
    assert result.error == "Something went wrong"


def test_trajectory_creation():
    """Test creating a trajectory."""
    trajectory = Trajectory(task_id="task_1")
    
    assert trajectory.task_id == "task_1"
    assert len(trajectory.steps) == 0
    assert trajectory.status == "in_progress"


def test_trajectory_add_step():
    """Test adding steps to trajectory."""
    trajectory = Trajectory(task_id="task_1")
    
    step = TrajectoryStep(
        step_index=0,
        llm_response="test response"
    )
    
    trajectory.add_step(step)
    assert len(trajectory.steps) == 1
    assert trajectory.steps[0].step_index == 0


def test_trajectory_complete():
    """Test completing a trajectory."""
    trajectory = Trajectory(task_id="task_1")
    
    trajectory.complete(result="Done", status="completed")
    
    assert trajectory.status == "completed"
    assert trajectory.final_result == "Done"
    assert trajectory.end_time is not None
