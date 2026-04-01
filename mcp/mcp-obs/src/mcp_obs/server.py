"""Stdio MCP server exposing observability tools."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel

from .client import ObservabilityClient
from .settings import resolve_settings
from .tools import TOOL_SPECS, TOOLS_BY_NAME, ToolPayload


def _text(data: ToolPayload) -> list[TextContent]:
    """Convert data to MCP text response."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


def create_server(client: ObservabilityClient) -> Server:
    """Create the observability MCP server."""
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [spec.as_tool() for spec in TOOL_SPECS]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        spec = TOOLS_BY_NAME.get(name)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            args = spec.model.model_validate(arguments or {})
            result = await spec.handler(client, args)
            return _text(result)
        except Exception as exc:
            return [
                TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")
            ]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    """Run the MCP server."""
    settings = resolve_settings()
    client = ObservabilityClient(settings)
    server = create_server(client)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
