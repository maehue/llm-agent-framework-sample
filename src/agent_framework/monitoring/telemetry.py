"""Telemetry system for event tracking and spans."""

from typing import Any, Callable, Optional
from datetime import datetime
import json


class Telemetry:
    """
    Lightweight telemetry system for agent instrumentation.
    
    Provides event hooks for:
    - Task lifecycle (start, end)
    - Step execution (start, end)
    - Tool calls (start, end)
    
    Default implementation logs structured JSON to stdout.
    Can be extended to send to monitoring services.
    """
    
    def __init__(self, handlers: Optional[list[Callable]] = None):
        """
        Initialize telemetry.
        
        Args:
            handlers: List of event handler functions
        """
        self.handlers = handlers or [self._default_handler]
        self.events: list[dict[str, Any]] = []
    
    def emit(self, event_type: str, data: dict[str, Any]) -> None:
        """
        Emit a telemetry event.
        
        Args:
            event_type: Type of event (e.g., 'step_start', 'tool_call_end')
            data: Event data
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        self.events.append(event)
        
        for handler in self.handlers:
            handler(event)
    
    def _default_handler(self, event: dict[str, Any]) -> None:
        """Default handler that logs to stdout."""
        print(json.dumps(event))
    
    def get_events(self, event_type: Optional[str] = None) -> list[dict[str, Any]]:
        """
        Get recorded events.
        
        Args:
            event_type: Optional filter by event type
            
        Returns:
            List of events
        """
        if event_type is None:
            return self.events
        return [e for e in self.events if e["event_type"] == event_type]
    
    def clear(self) -> None:
        """Clear recorded events."""
        self.events.clear()


class Span:
    """
    Context manager for tracking operation spans.
    
    Usage:
        with Span(telemetry, "operation_name", {"key": "value"}):
            # do work
            pass
    """
    
    def __init__(self, telemetry: Telemetry, name: str, data: Optional[dict] = None):
        """
        Initialize span.
        
        Args:
            telemetry: Telemetry instance
            name: Span name
            data: Additional span data
        """
        self.telemetry = telemetry
        self.name = name
        self.data = data or {}
        self.start_time = None
    
    def __enter__(self):
        """Start span."""
        self.start_time = datetime.now()
        self.telemetry.emit(f"{self.name}_start", self.data)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End span."""
        duration_ms = (datetime.now() - self.start_time).total_seconds() * 1000
        end_data = {**self.data, "duration_ms": duration_ms}
        if exc_type is not None:
            end_data["error"] = str(exc_val)
        self.telemetry.emit(f"{self.name}_end", end_data)
