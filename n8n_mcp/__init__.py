"""n8n MCP - MCP server for n8n workflow automation."""

from n8n_mcp.config import N8NSettings, get_settings, setup_logging
from n8n_mcp.models import (
    Credential,
    CredentialCreate,
    Execution,
    ExecutionStatus,
    ToolResponse,
    Workflow,
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowStatus,
)

__version__ = "0.1.0"

__all__ = [
    "N8NSettings",
    "get_settings",
    "setup_logging",
    "Credential",
    "CredentialCreate",
    "Execution",
    "ExecutionStatus",
    "ToolResponse",
    "Workflow",
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowStatus",
    "__version__",
]
