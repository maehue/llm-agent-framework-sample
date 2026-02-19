"""A2A client for sending/receiving messages."""

from __future__ import annotations
from typing import Optional, Any
from abc import ABC, abstractmethod

from .protocol import A2AMessage, TaskRequest, TaskResponse


class A2AClient(ABC):
    """
    Abstract client for agent-to-agent communication.
    
    Handles:
    - Sending messages to other agents
    - Receiving messages
    - Discovery of other agents
    
    In production, this might use:
    - HTTP/REST APIs
    - Message queues (RabbitMQ, Kafka)
    - WebSockets
    - gRPC
    """
    
    @abstractmethod
    def send(self, message: A2AMessage) -> None:
        """
        Send a message to another agent.
        
        Args:
            message: Message to send
        """
        pass
    
    @abstractmethod
    def receive(self, timeout: Optional[float] = None) -> Optional[A2AMessage]:
        """
        Receive a message (blocking or non-blocking).
        
        Args:
            timeout: Timeout in seconds (None = non-blocking)
            
        Returns:
            Received message or None
        """
        pass
    
    @abstractmethod
    def discover_agents(self) -> list[dict[str, Any]]:
        """
        Discover available agents.
        
        Returns:
            List of agent info dictionaries
        """
        pass


class SimpleA2AClient(A2AClient):
    """
    Simple in-process A2A client for demonstrations.
    
    Routes messages to local agent instances.
    Production would use actual network communication.
    """
    
    def __init__(self, agent_id: str):
        """
        Initialize client.
        
        Args:
            agent_id: This agent's ID
        """
        self.agent_id = agent_id
        self.message_queue: list[A2AMessage] = []
    
    def send(self, message: A2AMessage) -> None:
        """
        Send message (stub - just logs it).
        
        Args:
            message: Message to send
        """
        print(f"[A2A] {self.agent_id} sending: {message.message_type} to {message.recipient_id}")
    
    def receive(self, timeout: Optional[float] = None) -> Optional[A2AMessage]:
        """
        Receive message from queue.
        
        Args:
            timeout: Ignored in stub implementation
            
        Returns:
            Next message or None
        """
        if self.message_queue:
            return self.message_queue.pop(0)
        return None
    
    def discover_agents(self) -> list[dict[str, Any]]:
        """Discover agents (returns empty list in stub)."""
        return []
