"""MCP tool definitions for observability."""

from __future__ import annotations

from typing import Any, Awaitable, Callable, Union

from mcp.types import Tool
from pydantic import BaseModel

from .client import ObservabilityClient

ToolPayload = Union[BaseModel, list[BaseModel], dict, list[dict]]
ToolHandler = Callable[[ObservabilityClient, BaseModel], Awaitable[ToolPayload]]


class LogsSearchParams(BaseModel):
    """Parameters for logs_search tool."""

    query: str = ""
    time_range: str = "10m"
    limit: int = 20


class LogsErrorCountParams(BaseModel):
    """Parameters for logs_error_count tool."""

    service: str = ""
    time_range: str = "1h"


class TracesListParams(BaseModel):
    """Parameters for traces_list tool."""

    service: str = ""
    limit: int = 10


class TracesGetParams(BaseModel):
    """Parameters for traces_get tool."""

    trace_id: str


class ToolSpec(BaseModel):
    """Tool specification."""

    name: str
    description: str
    model: type[BaseModel]
    handler: ToolHandler

    def as_tool(self) -> Tool:
        """Convert to MCP Tool definition."""
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.model.model_json_schema(),
        )


TOOL_SPECS: list[ToolSpec] = [
    ToolSpec(
        name="logs_search",
        description="Search logs using LogsQL query. Returns matching log entries with fields like severity, service.name, event, trace_id, and error message.",
        model=LogsSearchParams,
        handler=lambda client, args: client.logs_search(
            query=args.query,
            time_range=args.time_range,
            limit=args.limit,
        ),
    ),
    ToolSpec(
        name="logs_error_count",
        description="Count errors per service over a time window. Returns a dict mapping service names to error counts.",
        model=LogsErrorCountParams,
        handler=lambda client, args: client.logs_error_count(
            service=args.service,
            time_range=args.time_range,
        ),
    ),
    ToolSpec(
        name="traces_list",
        description="List recent traces for a service. Returns trace metadata including trace_id, duration, and span count.",
        model=TracesListParams,
        handler=lambda client, args: client.traces_list(
            service=args.service,
            limit=args.limit,
        ),
    ),
    ToolSpec(
        name="traces_get",
        description="Fetch a specific trace by ID. Returns full trace with all spans showing the request flow across services.",
        model=TracesGetParams,
        handler=lambda client, args: client.traces_get(trace_id=args.trace_id),
    ),
]

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}
