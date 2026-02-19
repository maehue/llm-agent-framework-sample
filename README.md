# LLM Agent Framework Sample

A minimal but extensible Python framework for building LLM-powered agents with tool-calling, MCP integration, agent-to-agent communication, and monitoring.

## Overview

This framework demonstrates the core concepts of LLM agent systems:

- **Backbone LLM**: Abstract interface for language models with tool-calling support
- **Tool System**: Registry-based tool management with builtin tools (echo, math)
- **Orchestration**: Processing loop with trajectory capture and stop conditions
- **MCP Integration**: Model Context Protocol adapter for external tool providers
- **A2A Communication**: Agent-to-agent messaging and coordination
- **Monitoring**: Event-based telemetry and structured logging

## Architecture

```
src/agent_framework/
├── base/              # Core interfaces (BaseLLM, BaseTool)
├── data_structures/   # Task, ToolCall, Trajectory, etc.
├── tools/             # Tool registry and builtin tools
├── llms/              # LLM implementations (MockLLM, OllamaLLM)
├── agent/             # Agent, orchestration, memory
├── mcp/               # MCP client and provider stubs
├── a2a/               # Agent-to-agent protocol and coordinator
└── monitoring/        # Telemetry and logging
```

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd llm-agent-framework-sample

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

### 1. Basic Tool Call

```python
from agent_framework.tools import ToolRegistry, EchoTool, MathEvalTool
from agent_framework.data_structures import ToolCall

# Create registry and register tools
registry = ToolRegistry()
registry.register(EchoTool())
registry.register(MathEvalTool())

# Execute a tool call
tool_call = ToolCall(
    id="call_1",
    name="math_eval",
    arguments={"a": 15, "operator": "+", "b": 27}
)
result = registry.execute(tool_call)
print(result.result)  # 42
```

### 2. Agent Processing Loop

```python
from agent_framework.llms import MockLLM
from agent_framework.tools import ToolRegistry, EchoTool
from agent_framework.agent import LLMAgent
from agent_framework.data_structures import Task

# Setup agent
llm = MockLLM()
registry = ToolRegistry()
registry.register(EchoTool())
agent = LLMAgent(llm=llm, tool_registry=registry)

# Run task
task = Task(
    id="task_001",
    instruction="Echo: Hello World!",
    max_steps=5
)
result = agent.run(task)

# Access trajectory
for step in result.trajectory.steps:
    print(f"Step {step.step_index}: {step.tool_calls}")
```

## Examples

Run the example scripts to see the framework in action:

```bash
# Basic tool calling
python examples/01_basic_tool_call.py

# Multi-step agent execution with trajectory
python examples/02_processing_loop.py

# MCP integration (stub)
python examples/03_mcp_stub.py

# Agent-to-agent coordination
python examples/04_a2a_stub.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_tools.py
```

## Core Concepts

### Tasks and Trajectories

A **Task** represents work to be done:
```python
task = Task(
    id="task_001",
    instruction="Calculate 2 + 2 and echo the result",
    max_steps=10
)
```

A **Trajectory** captures the execution trace:
- Step-by-step tool calls and results
- Timestamps and latency
- Final status (completed, failed, max_steps_reached)

### Tool Registry

Tools are registered once and can be called by name:

```python
registry = ToolRegistry()
registry.register(MyTool())

# List tools in LLM format
tools = registry.list_for_llm()

# Execute tool call
result = registry.execute(tool_call)
```

### Stop Conditions

The agent stops when:
1. LLM signals completion (returns text response with no tool calls)
2. Maximum steps reached
3. Too many consecutive tool failures

### MCP Integration

Load external tools via MCP providers:

```python
from agent_framework.mcp import MockMCPProvider, MockWeatherTool

provider = MockMCPProvider(mock_tools=[MockWeatherTool()])
provider.load_tools(registry)
```

*Note: This is a stub implementation. Real MCP would connect to external servers.*

### A2A Coordination

Coordinate multiple specialist agents:

```python
from agent_framework.a2a import A2ACoordinator

coordinator = A2ACoordinator(main_agent=main_agent)
coordinator.register_specialist("math_specialist", math_agent)
coordinator.register_specialist("text_specialist", text_agent)

result = coordinator.coordinate_task(task, decomposition)
```

### Monitoring

Event-based telemetry:

```python
from agent_framework.monitoring import Telemetry

telemetry = Telemetry()
agent = LLMAgent(llm=llm, tool_registry=registry, telemetry=telemetry)

# Events are automatically emitted:
# - task_start, task_end
# - step_start, step_end
# - tool_call_start, tool_call_end

# Access events
events = telemetry.get_events("tool_call_end")
```

## Creating Custom Tools

Implement the `BaseTool` interface:

```python
from agent_framework.base import BaseTool

class MyCustomTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_tool"
    
    @property
    def description(self) -> str:
        return "Does something useful"
    
    @property
    def params_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string"}
            },
            "required": ["input"]
        }
    
    def __call__(self, input: str, **kwargs):
        return f"Processed: {input}"
```

## Creating Custom LLMs

Implement the `BaseLLM` interface:

```python
from agent_framework.base import BaseLLM, LLMResponse

class MyLLM(BaseLLM):
    def generate(self, messages, tools=None, **kwargs) -> LLMResponse:
        # Your LLM logic here
        return LLMResponse(
            content="Response text",
            tool_calls=[],
            finish_reason="stop"
        )
```

## Project Status

This is a **reference implementation** demonstrating core agent framework concepts. It includes:

✅ Complete core framework structure  
✅ Working examples and tests  
✅ Mock implementations for stable demonstrations  
✅ MCP and A2A integration stubs  

🚧 Production features (not included):
- Real MCP protocol implementation
- Production A2A networking
- Advanced LLM integrations
- Sandboxed code execution
- Vector memory stores

## Contributing

This is a sample/reference repository. Feel free to fork and adapt for your needs.

## License

MIT License - see [LICENSE](LICENSE) file for details.
