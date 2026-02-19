"""Simple in-memory storage for agent memory."""

from __future__ import annotations
from typing import Any, Optional


class Memory:
    """
    Simple in-memory storage for agent state.
    
    Stores:
    - Conversation history
    - Retrieved facts/context
    - Intermediate results
    
    This is a minimal implementation. Production systems might use
    vector databases, key-value stores, etc.
    """
    
    def __init__(self):
        self._store: dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Store a value."""
        self._store[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value."""
        return self._store.get(key, default)
    
    def delete(self, key: str) -> None:
        """Delete a value."""
        self._store.pop(key, None)
    
    def clear(self) -> None:
        """Clear all memory."""
        self._store.clear()
    
    def keys(self) -> list[str]:
        """Get all keys."""
        return list(self._store.keys())
