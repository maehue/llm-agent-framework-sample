"""Orchestration helpers for step execution."""


class Orchestrator:
    """
    Helper class for orchestrating agent steps.
    
    Provides utilities for:
    - Step planning
    - Context building
    - Stop condition evaluation
    
    This is a placeholder for more advanced orchestration logic.
    """
    
    @staticmethod
    def should_continue(step_count: int, max_steps: int, consecutive_failures: int, max_failures: int) -> bool:
        """
        Determine if agent should continue execution.
        
        Args:
            step_count: Current step count
            max_steps: Maximum allowed steps
            consecutive_failures: Number of consecutive failures
            max_failures: Maximum allowed consecutive failures
            
        Returns:
            True if agent should continue, False otherwise
        """
        if step_count >= max_steps:
            return False
        if consecutive_failures >= max_failures:
            return False
        return True
    
    @staticmethod
    def format_tool_results_for_context(results: list) -> str:
        """
        Format tool results for inclusion in LLM context.
        
        Args:
            results: List of ToolCallResult objects
            
        Returns:
            Formatted string representation
        """
        if not results:
            return ""
        
        formatted = []
        for result in results:
            if result.is_error:
                formatted.append(f"Tool {result.tool_name} failed: {result.error}")
            else:
                formatted.append(f"Tool {result.tool_name} returned: {result.result}")
        
        return "\n".join(formatted)
