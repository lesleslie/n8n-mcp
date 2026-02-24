"""Configuration for n8n-mcp using Oneiric patterns."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Oneiric logging imports
try:
    from oneiric.core.logging import LoggingConfig, configure_logging, get_logger

    ONEIRIC_LOGGING_AVAILABLE = True
except ImportError:
    ONEIRIC_LOGGING_AVAILABLE = False
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    def configure_logging(*args: Any, **kwargs: Any) -> None:
        logging.basicConfig(level=logging.INFO)


class N8NSettings(BaseSettings):
    """n8n MCP server configuration."""

    model_config = SettingsConfigDict(
        env_prefix="N8N_MCP_",
        env_file=(".env",),
        extra="ignore",
        case_sensitive=False,
    )

    # Server identification
    server_name: str = Field(
        default="n8n-mcp",
        description="Server name for identification",
    )
    server_description: str = Field(
        default="MCP server for n8n workflow automation",
        description="Server description",
    )

    # n8n API Configuration
    n8n_url: str = Field(
        default="http://localhost:5678",
        description="n8n instance URL",
    )
    api_key: str = Field(
        default="",
        description="n8n API key for authentication",
    )
    timeout: float = Field(
        default=30.0,
        ge=1.0,
        le=300.0,
        description="Request timeout in seconds",
    )

    # Mock mode for testing
    mock_mode: bool = Field(
        default=False,
        description="Run in mock mode without real n8n connection",
    )

    # HTTP transport
    enable_http_transport: bool = Field(
        default=False,
        description="Enable HTTP transport",
    )
    http_host: str = Field(
        default="127.0.0.1",
        description="HTTP server host",
    )
    http_port: int = Field(
        default=3044,
        ge=1024,
        le=65535,
        description="HTTP server port",
    )

    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )
    log_json: bool = Field(
        default=True,
        description="Use JSON logging format",
    )

    @field_validator("n8n_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate n8n URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("n8n_url must start with http:// or https://")
        return v.rstrip("/")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid}")
        return v.upper()


@lru_cache
def get_settings() -> N8NSettings:
    """Get cached settings instance."""
    return N8NSettings()


def setup_logging(settings: N8NSettings | None = None) -> None:
    """Configure logging using Oneiric patterns."""
    if settings is None:
        settings = get_settings()

    if ONEIRIC_LOGGING_AVAILABLE:
        config = LoggingConfig(
            level=settings.log_level,
            emit_json=settings.log_json,
            service_name="n8n-mcp",
        )
        configure_logging(config)
    else:
        # Fallback to standard logging
        import logging
        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper(), logging.INFO),
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        )


def get_logger_instance(name: str = "n8n-mcp") -> Any:
    """Get a structured logger instance."""
    if ONEIRIC_LOGGING_AVAILABLE:
        return get_logger(name)
    import logging
    return logging.getLogger(name)


__all__ = [
    "N8NSettings",
    "get_settings",
    "setup_logging",
    "get_logger_instance",
    "ONEIRIC_LOGGING_AVAILABLE",
]
