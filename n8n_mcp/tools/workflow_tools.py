"""Workflow tools for n8n MCP server."""

from __future__ import annotations

from typing import Any

from n8n_mcp.client import N8NClient
from n8n_mcp.config import get_logger_instance
from n8n_mcp.models import (
    ToolResponse,
    WorkflowCreate,
    WorkflowUpdate,
)

logger = get_logger_instance("n8n-mcp.tools.workflow")


def register_workflow_tools(app: Any, client: N8NClient) -> None:
    """Register workflow management tools."""

    @app.tool()
    async def list_workflows() -> ToolResponse:
        """List all workflows in the n8n instance.

        Returns:
            ToolResponse with list of workflows
        """
        logger.info("Listing workflows")

        try:
            workflows = await client.list_workflows()

            return ToolResponse(
                success=True,
                message=f"Found {len(workflows)} workflows",
                data={
                    "workflows": [wf.model_dump() for wf in workflows],
                    "count": len(workflows),
                },
            )

        except Exception as e:
            logger.error("Failed to list workflows", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to list workflows",
                error=str(e),
            )

    @app.tool()
    async def get_workflow(workflow_id: str) -> ToolResponse:
        """Get details of a specific workflow.

        Args:
            workflow_id: The workflow ID

        Returns:
            ToolResponse with workflow details
        """
        logger.info("Getting workflow", workflow_id=workflow_id)

        try:
            workflow = await client.get_workflow(workflow_id)

            return ToolResponse(
                success=True,
                message=f"Retrieved workflow: {workflow.name}",
                data={"workflow": workflow.model_dump()},
            )

        except Exception as e:
            logger.error("Failed to get workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get workflow {workflow_id}",
                error=str(e),
            )

    @app.tool()
    async def create_workflow(
        name: str,
        nodes: list[dict[str, Any]] | None = None,
        connections: dict[str, Any] | None = None,
        active: bool = False,
        tags: list[str] | None = None,
    ) -> ToolResponse:
        """Create a new workflow.

        Args:
            name: Workflow name
            nodes: List of node configurations (optional)
            connections: Node connections (optional)
            active: Whether to activate on creation (default: false)
            tags: Workflow tags (optional)

        Returns:
            ToolResponse with created workflow
        """
        logger.info("Creating workflow", name=name)

        try:
            workflow = WorkflowCreate(
                name=name,
                nodes=nodes or [],
                connections=connections or {},
                active=active,
                tags=tags or [],
            )

            created = await client.create_workflow(workflow)

            return ToolResponse(
                success=True,
                message=f"Created workflow: {created.name}",
                data={"workflow": created.model_dump()},
                next_steps=[
                    "Add nodes with update_workflow",
                    "Activate with activate_workflow",
                    "Execute with execute_workflow",
                ],
            )

        except Exception as e:
            logger.error("Failed to create workflow", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to create workflow",
                error=str(e),
            )

    @app.tool()
    async def update_workflow(
        workflow_id: str,
        name: str | None = None,
        nodes: list[dict[str, Any]] | None = None,
        connections: dict[str, Any] | None = None,
    ) -> ToolResponse:
        """Update an existing workflow.

        Args:
            workflow_id: The workflow ID to update
            name: New workflow name (optional)
            nodes: Updated node list (optional)
            connections: Updated connections (optional)

        Returns:
            ToolResponse with updated workflow
        """
        logger.info("Updating workflow", workflow_id=workflow_id)

        try:
            updates = WorkflowUpdate(
                name=name,
                nodes=nodes,
                connections=connections,
            )

            updated = await client.update_workflow(workflow_id, updates)

            return ToolResponse(
                success=True,
                message=f"Updated workflow: {updated.name}",
                data={"workflow": updated.model_dump()},
            )

        except Exception as e:
            logger.error("Failed to update workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to update workflow {workflow_id}",
                error=str(e),
            )

    @app.tool()
    async def delete_workflow(workflow_id: str) -> ToolResponse:
        """Delete a workflow.

        Args:
            workflow_id: The workflow ID to delete

        Returns:
            ToolResponse confirming deletion
        """
        logger.info("Deleting workflow", workflow_id=workflow_id)

        try:
            await client.delete_workflow(workflow_id)

            return ToolResponse(
                success=True,
                message=f"Deleted workflow {workflow_id}",
                data={"workflow_id": workflow_id},
            )

        except Exception as e:
            logger.error("Failed to delete workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to delete workflow {workflow_id}",
                error=str(e),
            )

    @app.tool()
    async def activate_workflow(workflow_id: str) -> ToolResponse:
        """Activate a workflow to start listening for triggers.

        Args:
            workflow_id: The workflow ID to activate

        Returns:
            ToolResponse with activation status
        """
        logger.info("Activating workflow", workflow_id=workflow_id)

        try:
            workflow = await client.activate_workflow(workflow_id)

            return ToolResponse(
                success=True,
                message=f"Activated workflow: {workflow.name}",
                data={"workflow_id": workflow_id, "active": True},
            )

        except Exception as e:
            logger.error("Failed to activate workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to activate workflow {workflow_id}",
                error=str(e),
            )

    @app.tool()
    async def deactivate_workflow(workflow_id: str) -> ToolResponse:
        """Deactivate a workflow.

        Args:
            workflow_id: The workflow ID to deactivate

        Returns:
            ToolResponse with deactivation status
        """
        logger.info("Deactivating workflow", workflow_id=workflow_id)

        try:
            workflow = await client.deactivate_workflow(workflow_id)

            return ToolResponse(
                success=True,
                message=f"Deactivated workflow: {workflow.name}",
                data={"workflow_id": workflow_id, "active": False},
            )

        except Exception as e:
            logger.error("Failed to deactivate workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to deactivate workflow {workflow_id}",
                error=str(e),
            )
