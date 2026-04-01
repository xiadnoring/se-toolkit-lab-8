# Observability Skill

You have access to observability tools that let you query logs and traces from the system.

## Available Tools

### Log Tools (VictoriaLogs)

- **logs_search** — Search logs using LogsQL query
  - `query`: LogsQL query string (e.g., `severity:ERROR service.name:"Learning Management Service"`)
  - `time_range`: Time window like `10m`, `1h`, `1d` (default: `10m`)
  - `limit`: Max results (default: 20)

- **logs_error_count** — Count errors per service
  - `service`: Filter by service name (optional)
  - `time_range`: Time window (default: `1h`)

### Trace Tools (VictoriaTraces)

- **traces_list** — List recent traces
  - `service`: Filter by service name (optional)
  - `limit`: Max results (default: 10)

- **traces_get** — Get full trace by ID
  - `trace_id`: The trace ID to fetch

## When to Use

1. **User asks about errors or failures**
   - First call `logs_error_count` to see if there are recent errors
   - If errors exist, call `logs_search` with `severity:ERROR` to see details
   - If you find a `trace_id` in the error logs, call `traces_get` to see the full request flow

2. **User asks about system health**
   - Call `logs_error_count` with `time_range: "10m"` for recent errors
   - Report: "No errors in the last 10 minutes" or "Found X errors in service Y"

3. **User asks about a specific request**
   - If they provide a trace_id, call `traces_get` directly
   - Otherwise, search logs for their request and extract the trace_id

## Response Style

- Summarize findings concisely — don't dump raw JSON
- Highlight the root cause if you found an error
- Include the trace_id if relevant so the user can investigate further
- Use bullet points for multiple errors

## Example Queries

**VictoriaLogs LogsQL:**
- `_time:10m severity:ERROR` — Errors in last 10 minutes
- `_time:1h service.name:"Learning Management Service"` — All backend logs in last hour
- `event:db_query severity:ERROR` — Database errors

**VictoriaTraces:**
- Query by service name to see recent traces
- Use trace_id from logs to fetch specific trace details
