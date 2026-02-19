"""Main LLM Agent with processing loop."""

from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from ..base.llm import BaseLLM
from ..tools.registry import ToolRegistry
from ..data_structures import Task, ToolCall, Trajectory, TrajectoryStep
from ..monitoring.telemetry import Telemetry
from .memory import Memory


class AgentResult(BaseModel):
    """Result of agent execution."""
    task_id: str
    trajectory: Trajectory
    final_answer: Optional[str] = None
    status: str


class LLMAgent:
    """
    Main agent class with processing loop.
    
    The agent follows this cycle:
    1. Build prompt context from task + memory
    2. Call LLM to get next action
    3. Execute any tool calls
    4. Update trajectory and memory
    5. Check stop conditions
    6. Repeat until done
    """
    
    def __init__(
        self,
        llm: BaseLLM,
        tool_registry: ToolRegistry,
        memory: Optional[Memory] = None,
        telemetry: Optional[Telemetry] = None,
        max_failures: int = 3
    ):
        """
        Initialize the agent.
        
        Args:
            llm: The backbone LLM
            tool_registry: Registry of available tools
            memory: Optional memory module
            telemetry: Optional telemetry/monitoring
            max_failures: Maximum consecutive tool failures before stopping
        """
        self.llm = llm
        self.tool_registry = tool_registry
        self.memory = memory or Memory()
        self.telemetry = telemetry or Telemetry()
        self.max_failures = max_failures
    
    def run(self, task: Task) -> AgentResult:
        """
        Execute a task.
        
        Args:
            task: The task to execute
            
        Returns:
            AgentResult with trajectory and final answer
        """
        trajectory = Trajectory(task_id=task.id)
        messages = self._build_initial_messages(task)
        consecutive_failures = 0
        
        self.telemetry.emit("task_start", {"task_id": task.id})
        
        for step_idx in range(task.max_steps):
            step_start = datetime.now()
            self.telemetry.emit("step_start", {"step": step_idx, "task_id": task.id})
            
            # Get LLM response
            tools = self.tool_registry.list_for_llm()
            llm_response = self.llm.generate(messages, tools=tools)
            
            # Create trajectory step
            step = TrajectoryStep(
                step_index=step_idx,
                llm_response=llm_response.content,
                tool_calls=[],
                tool_results=[]
            )
            
            # Handle tool calls
            if llm_response.tool_calls:
                for tc_dict in llm_response.tool_calls:
                    tool_call = ToolCall(
                        id=tc_dict.get("id", f"call_{step_idx}"),
                        name=tc_dict.get("name", ""),
                        arguments=tc_dict.get("arguments", {})
                    )
                    step.tool_calls.append(tool_call)
                    
                    self.telemetry.emit("tool_call_start", {
                        "tool": tool_call.name,
                        "step": step_idx
                    })
                    
                    # Execute tool call
                    result = self.tool_registry.execute(tool_call)
                    step.tool_results.append(result)
                    
                    self.telemetry.emit("tool_call_end", {
                        "tool": tool_call.name,
                        "success": not result.is_error,
                        "step": step_idx
                    })
                    
                    # Add tool result to messages
                    messages.append(result.to_message())
                    
                    if result.is_error:
                        consecutive_failures += 1
                    else:
                        consecutive_failures = 0
                
                # Check failure threshold
                if consecutive_failures >= self.max_failures:
                    step.latency_ms = (datetime.now() - step_start).total_seconds() * 1000
                    trajectory.add_step(step)
                    trajectory.complete(
                        result=f"Stopped due to {consecutive_failures} consecutive failures",
                        status="failed"
                    )
                    self.telemetry.emit("task_end", {
                        "task_id": task.id,
                        "status": "failed"
                    })
                    return AgentResult(
                        task_id=task.id,
                        trajectory=trajectory,
                        status="failed"
                    )
            
            # Add assistant message to context
            if llm_response.content:
                messages.append({
                    "role": "assistant",
                    "content": llm_response.content
                })
            
            # Calculate step latency
            step.latency_ms = (datetime.now() - step_start).total_seconds() * 1000
            trajectory.add_step(step)
            
            self.telemetry.emit("step_end", {"step": step_idx, "task_id": task.id})
            
            # Check if task is complete
            if self._is_complete(llm_response, step):
                trajectory.complete(
                    result=llm_response.content,
                    status="completed"
                )
                self.telemetry.emit("task_end", {
                    "task_id": task.id,
                    "status": "completed"
                })
                return AgentResult(
                    task_id=task.id,
                    trajectory=trajectory,
                    final_answer=llm_response.content,
                    status="completed"
                )
        
        # Max steps reached
        trajectory.complete(
            result="Max steps reached",
            status="max_steps_reached"
        )
        self.telemetry.emit("task_end", {
            "task_id": task.id,
            "status": "max_steps_reached"
        })
        return AgentResult(
            task_id=task.id,
            trajectory=trajectory,
            status="max_steps_reached"
        )
    
    def _build_initial_messages(self, task: Task) -> list[dict]:
        """Build initial message context for the LLM."""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI agent. Use the available tools to complete tasks."
            },
            {
                "role": "user",
                "content": task.instruction
            }
        ]
        return messages
    
    def _is_complete(self, llm_response, step: TrajectoryStep) -> bool:
        """
        Check if the task is complete.
        
        Task is complete if:
        - LLM provided a text response with no tool calls
        - LLM finish_reason is 'stop'
        """
        if llm_response.finish_reason == "stop" and llm_response.content:
            return True
        return False
