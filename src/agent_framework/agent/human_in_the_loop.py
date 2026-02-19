"""Human-in-the-loop approval gate."""

from typing import Callable, Optional, Any


class HumanInTheLoop:
    """
    Optional callback hook for human approval/intervention.
    
    Allows pausing agent execution to get human input or approval
    before proceeding with certain actions.
    """
    
    def __init__(self, approval_callback: Optional[Callable[[dict], bool]] = None):
        """
        Initialize HITL module.
        
        Args:
            approval_callback: Function that takes action details and returns
                             True to approve, False to reject
        """
        self.approval_callback = approval_callback
    
    def request_approval(self, action: dict[str, Any]) -> bool:
        """
        Request human approval for an action.
        
        Args:
            action: Dictionary describing the action
            
        Returns:
            True if approved, False if rejected
        """
        if self.approval_callback is None:
            # Auto-approve if no callback set
            return True
        
        return self.approval_callback(action)
    
    def notify(self, message: str) -> None:
        """
        Send a notification to the human.
        
        Args:
            message: Notification message
        """
        # In a real implementation, this might send an email,
        # post to a webhook, etc.
        print(f"[HITL Notification] {message}")
