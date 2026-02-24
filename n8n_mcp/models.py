"""Pydantic models for n8n API operations."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    """Workflow activation status."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class ExecutionStatus(str, Enum):
    """Execution status."""

    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELED = "canceled"
    WAITING = "waiting"


class NodeType(str, Enum):
    """Common n8n node types."""

    WEBHOOK = "n8n-nodes-base.webhook"
    HTTP_REQUEST = "n8n-nodes-base.httpRequest"
    CODE = "n8n-nodes-base.code"
    SET = "n8n-nodes-base.set"
    IF = "n8n-nodes-base.if"
    MERGE = "n8n-nodes-base.merge"
    SCHEDULE = "n8n-nodes-base.scheduleTrigger"
    MANUAL = "n8n-nodes-base.manualTrigger"
    START = "n8n-nodes-base.start"


class Workflow(BaseModel):
    """n8n workflow model."""

    id: str = Field(description="Workflow ID")
    name: str = Field(description="Workflow name")
    active: bool = Field(default=False, description="Whether workflow is active")
    nodes: list[dict[str, Any]] = Field(default_factory=list, description="Workflow nodes")
    connections: dict[str, Any] = Field(default_factory=dict, description="Node connections")
    settings: dict[str, Any] = Field(default_factory=dict, description="Workflow settings")
    created_at: datetime | None = Field(default=None, description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last update timestamp")
    tags: list[str] = Field(default_factory=list, description="Workflow tags")


class WorkflowCreate(BaseModel):
    """Model for creating a new workflow."""

    name: str = Field(description="Workflow name")
    nodes: list[dict[str, Any]] = Field(default_factory=list, description="Workflow nodes")
    connections: dict[str, Any] = Field(default_factory=dict, description="Node connections")
    settings: dict[str, Any] = Field(default_factory=dict, description="Workflow settings")
    active: bool = Field(default=False, description="Activate on creation")
    tags: list[str] = Field(default_factory=list, description="Workflow tags")


class WorkflowUpdate(BaseModel):
    """Model for updating a workflow."""

    name: str | None = Field(default=None, description="Workflow name")
    nodes: list[dict[str, Any]] | None = Field(default=None, description="Workflow nodes")
    connections: dict[str, Any] | None = Field(default=None, description="Node connections")
    settings: dict[str, Any] | None = Field(default=None, description="Workflow settings")
    tags: list[str] | None = Field(default=None, description="Workflow tags")


class Execution(BaseModel):
    """n8n execution model."""

    id: str = Field(description="Execution ID")
    workflow_id: str = Field(description="Workflow ID")
    status: ExecutionStatus = Field(description="Execution status")
    started_at: datetime | None = Field(default=None, description="Start timestamp")
    stopped_at: datetime | None = Field(default=None, description="End timestamp")
    data: dict[str, Any] | None = Field(default=None, description="Execution data")
    error: str | None = Field(default=None, description="Error message if failed")


class ExecutionCreate(BaseModel):
    """Model for triggering a workflow execution."""

    workflow_id: str = Field(description="Workflow ID to execute")
    data: dict[str, Any] | None = Field(default=None, description="Input data for execution")


class Credential(BaseModel):
    """n8n credential model."""

    id: str = Field(description="Credential ID")
    name: str = Field(description="Credential name")
    type: str = Field(description="Credential type")
    created_at: datetime | None = Field(default=None, description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last update timestamp")


class CredentialCreate(BaseModel):
    """Model for creating a credential."""

    name: str = Field(description="Credential name")
    type: str = Field(description="Credential type")
    data: dict[str, Any] = Field(description="Credential data (will be encrypted)")


class WebhookInfo(BaseModel):
    """Webhook information."""

    path: str = Field(description="Webhook path")
    method: str = Field(default="POST", description="HTTP method")
    authentication: str | None = Field(default=None, description="Auth type")
    workflow_id: str = Field(description="Associated workflow ID")


class ToolResponse(BaseModel):
    """Standard response format for MCP tools."""

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    data: dict[str, Any] | None = Field(default=None, description="Response data")
    error: str | None = Field(default=None, description="Error message if failed")
    next_steps: list[str] | None = Field(default=None, description="Suggested next actions")


class N8NError(BaseModel):
    """Error response from n8n API."""

    message: str = Field(description="Error message")
    code: str | None = Field(default=None, description="Error code")
    details: dict[str, Any] | None = Field(default=None, description="Additional details")
