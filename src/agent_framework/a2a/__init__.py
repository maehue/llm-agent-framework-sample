"""A2A (Agent-to-Agent) communication."""

from .protocol import A2AMessage, TaskRequest, TaskResponse, CapabilitiesAdvertisement
from .client import A2AClient
from .coordinator import A2ACoordinator

__all__ = [
    "A2AMessage",
    "TaskRequest", 
    "TaskResponse",
    "CapabilitiesAdvertisement",
    "A2AClient",
    "A2ACoordinator"
]
