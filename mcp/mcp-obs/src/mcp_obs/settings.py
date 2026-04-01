"""Configuration for MCP observability server."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Observability service settings."""

    # VictoriaLogs HTTP API
    victorialogs_url: str = Field(
        default="http://localhost:42010",
        description="VictoriaLogs base URL",
    )

    # VictoriaTraces HTTP API (Jaeger-compatible)
    victoriatraces_url: str = Field(
        default="http://localhost:42011",
        description="VictoriaTraces base URL",
    )


def resolve_settings() -> Settings:
    return Settings()
