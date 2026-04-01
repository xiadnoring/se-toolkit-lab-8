"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import httpx
from pydantic import BaseModel

from .settings import Settings


class LogEntry(BaseModel):
    """Single log entry from VictoriaLogs."""

    msg: str = ""
    stream: dict = {}
    time: str = ""
    severity: str = ""
    service_name: str = ""
    event: str = ""
    trace_id: str = ""
    span_id: str = ""
    error: str = ""


class TraceData(BaseModel):
    """Trace data from VictoriaTraces."""

    trace_id: str
    spans: list[dict] = []


class ObservabilityClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()
        self.logs_url = self.settings.victorialogs_url.rstrip("/")
        self.traces_url = self.settings.victoriatraces_url.rstrip("/")

    async def logs_search(
        self, query: str = "", time_range: str = "10m", limit: int = 20
    ) -> list[LogEntry]:
        """Search logs using LogsQL query."""
        url = f"{self.logs_url}/select/logsql/query"
        params = {
            "query": query,
            "limit": limit,
        }
        # Add time range to query if not already present
        if query and "_time:" not in query:
            params["query"] = f"_time:{time_range} {query}"
        elif not query:
            params["query"] = f"_time:{time_range}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()

        # VictoriaLogs returns either a list or an object with values
        if isinstance(data, list):
            entries = data
        elif isinstance(data, dict) and "values" in data:
            entries = data["values"]
        else:
            entries = [data] if data else []

        results = []
        for entry in entries:
            if isinstance(entry, dict):
                results.append(
                    LogEntry(
                        msg=entry.get("_msg", entry.get("msg", "")),
                        stream=entry.get("_stream", {}),
                        time=entry.get("_time", entry.get("time", "")),
                        severity=entry.get("severity", entry.get("level", "")),
                        service_name=entry.get("service.name", ""),
                        event=entry.get("event", ""),
                        trace_id=entry.get("trace_id", entry.get("otelTraceID", "")),
                        span_id=entry.get("span_id", entry.get("otelSpanID", "")),
                        error=entry.get("error", ""),
                    )
                )
        return results

    async def logs_error_count(
        self, service: str = "", time_range: str = "1h"
    ) -> dict[str, int]:
        """Count errors per service over a time window."""
        query = f"_time:{time_range} severity:ERROR"
        if service:
            query += f' service.name:"{service}"'

        entries = await self.logs_search(query=query, time_range=time_range, limit=1000)

        # Count by service
        counts: dict[str, int] = {}
        for entry in entries:
            svc = entry.service_name or "unknown"
            counts[svc] = counts.get(svc, 0) + 1

        return counts

    async def traces_list(
        self, service: str = "", limit: int = 10
    ) -> list[dict]:
        """List recent traces for a service."""
        url = f"{self.traces_url}/select/jaeger/api/traces"
        params = {"limit": limit}
        if service:
            params["service"] = service

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()

        # Jaeger API returns {"data": [...traces...]}
        if isinstance(data, dict) and "data" in data:
            return data["data"]
        elif isinstance(data, list):
            return data
        return []

    async def traces_get(self, trace_id: str) -> dict:
        """Fetch a specific trace by ID."""
        url = f"{self.traces_url}/select/jaeger/api/traces/{trace_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            data = response.json()

        # Jaeger API returns {"data": [...traces...]}
        if isinstance(data, dict) and "data" in data:
            traces = data["data"]
            return traces[0] if traces else {}
        elif isinstance(data, list):
            return data[0] if data else {}
        return data or {}
