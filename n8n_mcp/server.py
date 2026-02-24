"""FastMCP server for n8n workflow automation."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP

from n8n_mcp import __version__
from n8n_mcp.client import N8NClient
from n8n_mcp.config import get_logger_instance, get_settings, setup_logging
from n8n_mcp.tools import (
    register_credential_tools,
    register_execution_tools,
    register_workflow_tools,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = get_logger_instance("n8n-mcp.server")

APP_NAME = "n8n-mcp"
APP_VERSION = __version__


def create_app() -> FastMCP:
    """Create and configure the FastMCP application."""
    settings = get_settings()
    setup_logging(settings)

    logger.info(
        "Initializing n8n-mcp server",
        version=APP_VERSION,
        n8n_url=settings.n8n_url,
        mock_mode=settings.mock_mode,
    )

    app = FastMCP(name=APP_NAME, version=APP_VERSION)
    client = N8NClient(settings)

    # Register tools
    register_workflow_tools(app, client)
    register_execution_tools(app, client)
    register_credential_tools(app, client)

    # Setup lifespan for proper cleanup
    original_lifespan = app._mcp_server.lifespan

    @asynccontextmanager
    async def lifespan(server: Any) -> AsyncGenerator[dict[str, Any]]:
        async with original_lifespan(server) as state:
            try:
                yield state
            finally:
                await client.close()

    app._mcp_server.lifespan = lifespan

    logger.info(
        "Tools registered",
        workflow=7,
        execution=4,
        credential=5,
    )

    return app


_app: FastMCP | None = None


def get_app() -> FastMCP:
    """Get the singleton FastMCP application."""
    global _app
    if _app is None:
        _app = create_app()
    return _app


def __getattr__(name: str) -> Any:
    """Dynamic attribute access for app and http_app."""
    if name == "app":
        return get_app()
    if name == "http_app":
        return get_app().http_app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = ["create_app", "get_app", "APP_NAME", "APP_VERSION"]
