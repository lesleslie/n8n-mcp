"""n8n API client with mock mode support."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
from pydantic import ValidationError

from n8n_mcp.config import get_logger_instance, get_settings
from n8n_mcp.models import (
    Credential,
    CredentialCreate,
    Execution,
    ExecutionCreate,
    ExecutionStatus,
    N8NError,
    Workflow,
    WorkflowCreate,
    WorkflowUpdate,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from n8n_mcp.config import N8NSettings

logger = get_logger_instance("n8n-mcp.client")


class N8NError(Exception):
    """Exception raised for n8n API errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


class N8NClient:
    """Async client for n8n API operations."""

    def __init__(self, settings: N8NSettings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> N8NClient:
        await self._ensure_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        if self._client is None:
            headers = {}
            if self.settings.api_key:
                headers["X-N8N-API-KEY"] = self.settings.api_key

            self._client = httpx.AsyncClient(
                base_url=f"{self.settings.n8n_url}/api/v1",
                headers=headers,
                timeout=self.settings.timeout,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    # Workflow Operations

    async def list_workflows(self) -> list[Workflow]:
        """List all workflows."""
        if self.settings.mock_mode:
            return self._mock_list_workflows()

        client = await self._ensure_client()
        response = await client.get("/workflows")
        response.raise_for_status()

        data = response.json()
        return [Workflow(**wf) for wf in data.get("data", [])]

    async def get_workflow(self, workflow_id: str) -> Workflow:
        """Get a specific workflow by ID."""
        if self.settings.mock_mode:
            return self._mock_get_workflow(workflow_id)

        client = await self._ensure_client()
        response = await client.get(f"/workflows/{workflow_id}")
        response.raise_for_status()

        data = response.json()
        return Workflow(**data.get("data", {}))

    async def create_workflow(self, workflow: WorkflowCreate) -> Workflow:
        """Create a new workflow."""
        if self.settings.mock_mode:
            return self._mock_create_workflow(workflow)

        client = await self._ensure_client()
        response = await client.post("/workflows", json=workflow.model_dump(exclude_none=True))
        response.raise_for_status()

        data = response.json()
        return Workflow(**data.get("data", {}))

    async def update_workflow(
        self,
        workflow_id: str,
        updates: WorkflowUpdate,
    ) -> Workflow:
        """Update an existing workflow."""
        if self.settings.mock_mode:
            return self._mock_update_workflow(workflow_id, updates)

        client = await self._ensure_client()
        response = await client.patch(
            f"/workflows/{workflow_id}",
            json=updates.model_dump(exclude_none=True),
        )
        response.raise_for_status()

        data = response.json()
        return Workflow(**data.get("data", {}))

    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow."""
        if self.settings.mock_mode:
            return self._mock_delete_workflow(workflow_id)

        client = await self._ensure_client()
        response = await client.delete(f"/workflows/{workflow_id}")
        response.raise_for_status()
        return True

    async def activate_workflow(self, workflow_id: str) -> Workflow:
        """Activate a workflow."""
        if self.settings.mock_mode:
            return self._mock_activate_workflow(workflow_id, active=True)

        client = await self._ensure_client()
        response = await client.patch(
            f"/workflows/{workflow_id}",
            json={"active": True},
        )
        response.raise_for_status()

        data = response.json()
        return Workflow(**data.get("data", {}))

    async def deactivate_workflow(self, workflow_id: str) -> Workflow:
        """Deactivate a workflow."""
        if self.settings.mock_mode:
            return self._mock_activate_workflow(workflow_id, active=False)

        client = await self._ensure_client()
        response = await client.patch(
            f"/workflows/{workflow_id}",
            json={"active": False},
        )
        response.raise_for_status()

        data = response.json()
        return Workflow(**data.get("data", {}))

    # Execution Operations

    async def execute_workflow(
        self,
        workflow_id: str,
        data: dict[str, Any] | None = None,
    ) -> Execution:
        """Execute a workflow manually."""
        if self.settings.mock_mode:
            return self._mock_execute_workflow(workflow_id, data)

        client = await self._ensure_client()
        response = await client.post(
            f"/workflows/{workflow_id}/execute",
            json={"data": data} if data else {},
        )
        response.raise_for_status()

        result = response.json()
        return Execution(**result.get("data", {}))

    async def list_executions(
        self,
        workflow_id: str | None = None,
        limit: int = 50,
    ) -> list[Execution]:
        """List executions, optionally filtered by workflow."""
        if self.settings.mock_mode:
            return self._mock_list_executions(workflow_id, limit)

        client = await self._ensure_client()
        params = {"limit": limit}
        if workflow_id:
            params["workflowId"] = workflow_id

        response = await client.get("/executions", params=params)
        response.raise_for_status()

        data = response.json()
        return [Execution(**ex) for ex in data.get("data", [])]

    async def get_execution(self, execution_id: str) -> Execution:
        """Get a specific execution by ID."""
        if self.settings.mock_mode:
            return self._mock_get_execution(execution_id)

        client = await self._ensure_client()
        response = await client.get(f"/executions/{execution_id}")
        response.raise_for_status()

        data = response.json()
        return Execution(**data.get("data", {}))

    async def delete_execution(self, execution_id: str) -> bool:
        """Delete an execution."""
        if self.settings.mock_mode:
            return True

        client = await self._ensure_client()
        response = await client.delete(f"/executions/{execution_id}")
        response.raise_for_status()
        return True

    # Credential Operations

    async def list_credentials(self) -> list[Credential]:
        """List all credentials (without secret data)."""
        if self.settings.mock_mode:
            return self._mock_list_credentials()

        client = await self._ensure_client()
        response = await client.get("/credentials")
        response.raise_for_status()

        data = response.json()
        return [Credential(**cred) for cred in data.get("data", [])]

    async def get_credential(self, credential_id: str) -> Credential:
        """Get a specific credential by ID."""
        if self.settings.mock_mode:
            return self._mock_get_credential(credential_id)

        client = await self._ensure_client()
        response = await client.get(f"/credentials/{credential_id}")
        response.raise_for_status()

        data = response.json()
        return Credential(**data.get("data", {}))

    async def create_credential(self, credential: CredentialCreate) -> Credential:
        """Create a new credential."""
        if self.settings.mock_mode:
            return self._mock_create_credential(credential)

        client = await self._ensure_client()
        response = await client.post(
            "/credentials",
            json=credential.model_dump(exclude_none=True),
        )
        response.raise_for_status()

        data = response.json()
        return Credential(**data.get("data", {}))

    async def delete_credential(self, credential_id: str) -> bool:
        """Delete a credential."""
        if self.settings.mock_mode:
            return True

        client = await self._ensure_client()
        response = await client.delete(f"/credentials/{credential_id}")
        response.raise_for_status()
        return True

    # Mock Implementations

    def _mock_list_workflows(self) -> list[Workflow]:
        return [
            Workflow(
                id="1",
                name="Example Workflow",
                active=True,
                nodes=[{"name": "Start", "type": "n8n-nodes-base.start"}],
                connections={},
            ),
            Workflow(
                id="2",
                name="Test Workflow",
                active=False,
                nodes=[],
                connections={},
            ),
        ]

    def _mock_get_workflow(self, workflow_id: str) -> Workflow:
        return Workflow(
            id=workflow_id,
            name=f"Workflow {workflow_id}",
            active=True,
            nodes=[{"name": "Start", "type": "n8n-nodes-base.start"}],
            connections={},
        )

    def _mock_create_workflow(self, workflow: WorkflowCreate) -> Workflow:
        return Workflow(
            id="new-workflow-id",
            name=workflow.name,
            active=workflow.active,
            nodes=workflow.nodes,
            connections=workflow.connections,
            settings=workflow.settings,
        )

    def _mock_update_workflow(
        self,
        workflow_id: str,
        updates: WorkflowUpdate,
    ) -> Workflow:
        return Workflow(
            id=workflow_id,
            name=updates.name or f"Workflow {workflow_id}",
            active=True,
            nodes=updates.nodes or [],
            connections=updates.connections or {},
        )

    def _mock_delete_workflow(self, workflow_id: str) -> bool:
        return True

    def _mock_activate_workflow(
        self,
        workflow_id: str,
        active: bool,
    ) -> Workflow:
        return Workflow(
            id=workflow_id,
            name=f"Workflow {workflow_id}",
            active=active,
            nodes=[],
            connections={},
        )

    def _mock_execute_workflow(
        self,
        workflow_id: str,
        data: dict[str, Any] | None,
    ) -> Execution:
        return Execution(
            id="exec-1",
            workflow_id=workflow_id,
            status=ExecutionStatus.SUCCESS,
            data=data,
        )

    def _mock_list_executions(
        self,
        workflow_id: str | None,
        limit: int,
    ) -> list[Execution]:
        return [
            Execution(
                id="exec-1",
                workflow_id=workflow_id or "1",
                status=ExecutionStatus.SUCCESS,
            ),
        ]

    def _mock_get_execution(self, execution_id: str) -> Execution:
        return Execution(
            id=execution_id,
            workflow_id="1",
            status=ExecutionStatus.SUCCESS,
        )

    def _mock_list_credentials(self) -> list[Credential]:
        return [
            Credential(id="1", name="HTTP Basic", type="httpBasicAuth"),
            Credential(id="2", name="API Key", type="httpQueryAuth"),
        ]

    def _mock_get_credential(self, credential_id: str) -> Credential:
        return Credential(
            id=credential_id,
            name=f"Credential {credential_id}",
            type="httpBasicAuth",
        )

    def _mock_create_credential(self, credential: CredentialCreate) -> Credential:
        return Credential(
            id="new-cred-id",
            name=credential.name,
            type=credential.type,
        )
