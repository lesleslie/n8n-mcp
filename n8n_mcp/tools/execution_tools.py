"""Execution tools for n8n MCP server."""

from __future__ import annotations

from typing import Any

from n8n_mcp.client import N8NClient
from n8n_mcp.config import get_logger_instance
from n8n_mcp.models import ToolResponse

logger = get_logger_instance("n8n-mcp.tools.execution")


def register_execution_tools(app: Any, client: N8NClient) -> None:
    """Register execution management tools."""

    @app.tool()
    async def execute_workflow(
        workflow_id: str,
        data: dict[str, Any] | None = None,
    ) -> ToolResponse:
        """Execute a workflow manually.

        Args:
            workflow_id: The workflow ID to execute
            data: Optional input data for the execution

        Returns:
            ToolResponse with execution details
        """
        logger.info("Executing workflow", workflow_id=workflow_id)

        try:
            execution = await client.execute_workflow(workflow_id, data)

            return ToolResponse(
                success=True,
                message=f"Executed workflow, status: {execution.status.value}",
                data={
                    "execution_id": execution.id,
                    "workflow_id": execution.workflow_id,
                    "status": execution.status.value,
                    "data": execution.data,
                    "error": execution.error,
                },
                next_steps=[
                    "Check status with get_execution",
                    "View results in n8n UI",
                ],
            )

        except Exception as e:
            logger.error("Failed to execute workflow", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to execute workflow {workflow_id}",
                error=str(e),
            )

    @app.tool()
    async def list_executions(
        workflow_id: str | None = None,
        limit: int = 50,
    ) -> ToolResponse:
        """List workflow executions.

        Args:
            workflow_id: Filter by workflow ID (optional)
            limit: Maximum number of executions to return (default: 50)

        Returns:
            ToolResponse with list of executions
        """
        logger.info("Listing executions", workflow_id=workflow_id, limit=limit)

        try:
            executions = await client.list_executions(workflow_id, limit)

            return ToolResponse(
                success=True,
                message=f"Found {len(executions)} executions",
                data={
                    "executions": [ex.model_dump() for ex in executions],
                    "count": len(executions),
                },
            )

        except Exception as e:
            logger.error("Failed to list executions", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to list executions",
                error=str(e),
            )

    @app.tool()
    async def get_execution(execution_id: str) -> ToolResponse:
        """Get details of a specific execution.

        Args:
            execution_id: The execution ID

        Returns:
            ToolResponse with execution details
        """
        logger.info("Getting execution", execution_id=execution_id)

        try:
            execution = await client.get_execution(execution_id)

            return ToolResponse(
                success=True,
                message=f"Execution status: {execution.status.value}",
                data={
                    "execution": execution.model_dump(),
                },
            )

        except Exception as e:
            logger.error("Failed to get execution", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get execution {execution_id}",
                error=str(e),
            )

    @app.tool()
    async def delete_execution(execution_id: str) -> ToolResponse:
        """Delete an execution record.

        Args:
            execution_id: The execution ID to delete

        Returns:
            ToolResponse confirming deletion
        """
        logger.info("Deleting execution", execution_id=execution_id)

        try:
            await client.delete_execution(execution_id)

            return ToolResponse(
                success=True,
                message=f"Deleted execution {execution_id}",
                data={"execution_id": execution_id},
            )

        except Exception as e:
            logger.error("Failed to delete execution", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to delete execution {execution_id}",
                error=str(e),
            )
