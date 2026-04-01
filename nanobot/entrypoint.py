#!/usr/bin/env python3
"""
Entrypoint for nanobot Docker container.

Resolves environment variables into config.json at runtime,
then launches `nanobot gateway`.

Docker passes config via env vars, not by editing files.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    config_dir = Path(__file__).parent
    config_path = config_dir / "config.json"
    # Write resolved config to /tmp to avoid permission issues with mounted volumes
    resolved_path = Path("/tmp/nanobot/config.resolved.json")
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    workspace_dir = config_dir / "workspace"

    # Read base config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Override provider settings from env vars
    if llm_api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_api_key

    if llm_api_base_url := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_api_base_url

    if llm_api_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_api_model

    # Override gateway settings from env vars
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config.setdefault("gateway", {})["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config.setdefault("gateway", {})["port"] = int(gateway_port)

    # Override LMS MCP server env vars
    if "tools" in config and "mcpServers" in config["tools"] and "lms" in config["tools"]["mcpServers"]:
        lms_env = config["tools"]["mcpServers"]["lms"].setdefault("env", {})

        if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
            lms_env["NANOBOT_LMS_BACKEND_URL"] = backend_url

        if api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
            lms_env["NANOBOT_LMS_API_KEY"] = api_key

    # Configure webchat channel from env vars
    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        config.setdefault("channels", {})["webchat"] = {
            "enabled": True,
            "host": webchat_host,
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
            "allowFrom": ["*"],
        }
    elif webchat_port := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT"):
        # Host not specified, use default
        config.setdefault("channels", {})["webchat"] = {
            "enabled": True,
            "host": "0.0.0.0",
            "port": int(webchat_port),
            "allowFrom": ["*"],
        }

    # Configure mcp_webchat MCP server if webchat is enabled
    if "channels" in config and "webchat" in config["channels"]:
        # Add mcp_webchat server to tools
        if "tools" not in config:
            config["tools"] = {}
        if "mcpServers" not in config["tools"]:
            config["tools"]["mcpServers"] = {}

        # Configure mcp_webchat server
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_UI_RELAY_URL": os.environ.get("NANOBOT_UI_RELAY_URL", ""),
                "NANOBOT_UI_RELAY_TOKEN": os.environ.get("NANOBOT_UI_RELAY_TOKEN", ""),
            },
        }

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}", file=sys.stderr)

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_path), "--workspace", str(workspace_dir)])


if __name__ == "__main__":
    main()
