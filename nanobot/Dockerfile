# Nanobot gateway Docker image
# Multi-stage build with uv

# ---
# Stage 1: Build the application
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace pyproject.toml and uv.lock for dependency resolution
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy nanobot package (build context is ./nanobot, so files are at root)
COPY pyproject.toml /app/nanobot/pyproject.toml

# Copy mcp-lms for build (from workspace context)
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms

# Copy nanobot-websocket-channel packages (from workspace context)
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol
COPY --from=workspace nanobot-websocket-channel/mcp-webchat /app/nanobot-websocket-channel/mcp-webchat
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat

# Copy mcp-obs for build (from workspace context)
COPY --from=workspace mcp/mcp-obs /app/mcp/mcp-obs

# Copy backend for workspace resolution
COPY --from=workspace backend /app/backend

# Copy qwen-code-api for workspace resolution
COPY --from=workspace qwen-code-api /app/qwen-code-api

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Install webchat and observability packages directly
WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --editable ../nanobot-websocket-channel/nanobot-channel-protocol \
    --editable ../nanobot-websocket-channel/mcp-webchat \
    --editable ../nanobot-websocket-channel/nanobot-webchat \
    --editable ../mcp/mcp-obs
WORKDIR /app

# ---
# Stage 2: Runtime image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Build args for user IDs - match HOST_UID/HOST_GID from docker-compose.yml
ARG APP_UID=1000
ARG APP_GID=1000

# Create non-root user
RUN groupadd --system --gid ${APP_GID} appgroup \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

# Copy application from builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Place venv executables at front of PATH
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER appuser

WORKDIR /app

# Run the entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
