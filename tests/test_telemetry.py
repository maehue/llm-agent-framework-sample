"""Tests for telemetry system."""

import sys
sys.path.insert(0, 'src')

from agent_framework.monitoring import Telemetry


def test_telemetry_creation():
    """Test creating telemetry instance."""
    telemetry = Telemetry()
    assert telemetry is not None
    assert len(telemetry.events) == 0


def test_telemetry_emit():
    """Test emitting events."""
    telemetry = Telemetry(handlers=[])  # No default handler
    
    telemetry.emit("test_event", {"key": "value"})
    
    assert len(telemetry.events) == 1
    assert telemetry.events[0]["event_type"] == "test_event"
    assert telemetry.events[0]["data"]["key"] == "value"


def test_telemetry_get_events():
    """Test retrieving events."""
    telemetry = Telemetry(handlers=[])
    
    telemetry.emit("event_a", {"data": 1})
    telemetry.emit("event_b", {"data": 2})
    telemetry.emit("event_a", {"data": 3})
    
    all_events = telemetry.get_events()
    assert len(all_events) == 3
    
    event_a = telemetry.get_events("event_a")
    assert len(event_a) == 2


def test_telemetry_clear():
    """Test clearing events."""
    telemetry = Telemetry(handlers=[])
    
    telemetry.emit("test", {})
    assert len(telemetry.events) == 1
    
    telemetry.clear()
    assert len(telemetry.events) == 0
