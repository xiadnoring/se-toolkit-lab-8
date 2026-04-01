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

### User asks "What went wrong?" or "Check system health"

Follow this investigation flow:

1. **Check for recent errors** — Call `logs_error_count` with `time_range: "10m"`
   - If no errors: "No errors found in the last 10 minutes. System looks healthy."
   - If errors exist: Continue to step 2

2. **Search error logs** — Call `logs_search` with `severity:ERROR` and `time_range: "10m"`
   - Look for the most recent error
   - Extract the `trace_id` from the error log if available
   - Note the `service.name`, `event`, and `error` message

3. **Fetch the trace** — Call `traces_get` with the `trace_id` from step 2
   - Examine the span hierarchy
   - Find which operation failed
   - Look for error tags in spans

4. **Summarize findings** — Provide a concise explanation that includes:
   - What service failed
   - What operation was being performed
   - What the error was
   - Evidence from both logs AND traces

### User asks about a specific request
- If they provide a trace_id, call `traces_get` directly
- Otherwise, search logs for their request and extract the trace_id

## Response Style

- Summarize findings concisely — don't dump raw JSON
- Highlight the root cause if you found an error
- Include the trace_id if relevant so the user can investigate further
- Use bullet points for multiple errors
- **Always cite both log evidence AND trace evidence** when investigating failures

## Example Investigation Response

```
I found an error in the Learning Management Service:

**Log evidence:**
- Time: 2026-04-01T08:45:46Z
- Event: db_query
- Error: "(sqlalchemy.dialects.postgresql.asyncpg.InterfaceError) connection is closed"
- Trace ID: f833daef45ac9bce38911e4e8d652655

**Trace evidence:**
- Span "SELECT db-lab-8" failed with error tag
- HTTP response returned 404 status

**Root cause:** PostgreSQL connection was closed. The database is unreachable.
```

## Example Queries

**VictoriaLogs LogsQL:**
- `_time:10m severity:ERROR` — Errors in last 10 minutes
- `_time:1h service.name:"Learning Management Service"` — All backend logs in last hour
- `event:db_query severity:ERROR` — Database errors

**VictoriaTraces:**
- Query by service name to see recent traces
- Use trace_id from logs to fetch specific trace details
