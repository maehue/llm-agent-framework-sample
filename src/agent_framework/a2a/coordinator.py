"""A2A coordinator for routing tasks to specialist agents."""

from __future__ import annotations
from typing import Any, Optional
from ..agent.agent import LLMAgent
from ..data_structures import Task
from .protocol import TaskRequest, TaskResponse
from .client import A2AClient


class A2ACoordinator:
    """
    Coordinator that routes subtasks to specialist agents.
    
    Responsibilities:
    - Decompose tasks into subtasks
    - Route subtasks to appropriate specialist agents
    - Aggregate results
    - Merge back into main agent flow
    """
    
    def __init__(self, main_agent: LLMAgent, specialist_agents: Optional[dict[str, LLMAgent]] = None):
        """
        Initialize coordinator.
        
        Args:
            main_agent: The main coordinating agent
            specialist_agents: Dict of specialist name -> agent
        """
        self.main_agent = main_agent
        self.specialist_agents = specialist_agents or {}
    
    def register_specialist(self, name: str, agent: LLMAgent) -> None:
        """
        Register a specialist agent.
        
        Args:
            name: Specialist identifier
            agent: The specialist agent
        """
        self.specialist_agents[name] = agent
    
    def delegate_subtask(self, subtask: Task, specialist_name: str) -> Any:
        """
        Delegate a subtask to a specialist agent.
        
        Args:
            subtask: The subtask to delegate
            specialist_name: Name of the specialist to use
            
        Returns:
            Result from the specialist agent
        """
        specialist = self.specialist_agents.get(specialist_name)
        
        if specialist is None:
            return {
                "error": f"Specialist '{specialist_name}' not found",
                "status": "failed"
            }
        
        # Execute subtask with specialist
        result = specialist.run(subtask)
        
        return {
            "status": result.status,
            "result": result.final_answer,
            "trajectory": result.trajectory.to_dict()
        }
    
    def coordinate_task(self, task: Task, decomposition: list[dict[str, Any]]) -> dict[str, Any]:
        """
        Coordinate a task by decomposing and delegating.
        
        Args:
            task: Main task
            decomposition: List of subtask definitions with specialist assignments
            
        Returns:
            Aggregated results
        """
        results = []
        
        for subtask_def in decomposition:
            subtask = Task(
                id=f"{task.id}_sub_{len(results)}",
                instruction=subtask_def["instruction"],
                context=subtask_def.get("context", {}),
                max_steps=subtask_def.get("max_steps", 5)
            )
            
            specialist = subtask_def.get("specialist", "main")
            
            if specialist == "main":
                result = self.main_agent.run(subtask)
                results.append({
                    "subtask": subtask_def["instruction"],
                    "result": result.final_answer,
                    "status": result.status
                })
            else:
                result = self.delegate_subtask(subtask, specialist)
                results.append({
                    "subtask": subtask_def["instruction"],
                    "result": result.get("result"),
                    "status": result.get("status")
                })
        
        return {
            "task_id": task.id,
            "subtask_results": results,
            "status": "completed"
        }
