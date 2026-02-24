"""Credential tools for n8n MCP server."""

from __future__ import annotations

from typing import Any

from n8n_mcp.client import N8NClient
from n8n_mcp.config import get_logger_instance
from n8n_mcp.models import CredentialCreate, ToolResponse

logger = get_logger_instance("n8n-mcp.tools.credential")


def register_credential_tools(app: Any, client: N8NClient) -> None:
    """Register credential management tools."""

    @app.tool()
    async def list_credentials() -> ToolResponse:
        """List all credentials (without secret data).

        Returns:
            ToolResponse with list of credentials
        """
        logger.info("Listing credentials")

        try:
            credentials = await client.list_credentials()

            return ToolResponse(
                success=True,
                message=f"Found {len(credentials)} credentials",
                data={
                    "credentials": [cred.model_dump() for cred in credentials],
                    "count": len(credentials),
                },
            )

        except Exception as e:
            logger.error("Failed to list credentials", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to list credentials",
                error=str(e),
            )

    @app.tool()
    async def get_credential(credential_id: str) -> ToolResponse:
        """Get details of a specific credential.

        Args:
            credential_id: The credential ID

        Returns:
            ToolResponse with credential details (without secret data)
        """
        logger.info("Getting credential", credential_id=credential_id)

        try:
            credential = await client.get_credential(credential_id)

            return ToolResponse(
                success=True,
                message=f"Retrieved credential: {credential.name}",
                data={"credential": credential.model_dump()},
            )

        except Exception as e:
            logger.error("Failed to get credential", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to get credential {credential_id}",
                error=str(e),
            )

    @app.tool()
    async def create_credential(
        name: str,
        credential_type: str,
        data: dict[str, Any],
    ) -> ToolResponse:
        """Create a new credential.

        Args:
            name: Credential name
            credential_type: Type of credential (e.g., httpBasicAuth, httpQueryAuth)
            data: Credential data (will be encrypted by n8n)

        Returns:
            ToolResponse with created credential
        """
        logger.info("Creating credential", name=name, type=credential_type)

        try:
            credential = CredentialCreate(
                name=name,
                type=credential_type,
                data=data,
            )

            created = await client.create_credential(credential)

            return ToolResponse(
                success=True,
                message=f"Created credential: {created.name}",
                data={"credential": created.model_dump()},
            )

        except Exception as e:
            logger.error("Failed to create credential", error=str(e))
            return ToolResponse(
                success=False,
                message="Failed to create credential",
                error=str(e),
            )

    @app.tool()
    async def delete_credential(credential_id: str) -> ToolResponse:
        """Delete a credential.

        Args:
            credential_id: The credential ID to delete

        Returns:
            ToolResponse confirming deletion
        """
        logger.info("Deleting credential", credential_id=credential_id)

        try:
            await client.delete_credential(credential_id)

            return ToolResponse(
                success=True,
                message=f"Deleted credential {credential_id}",
                data={"credential_id": credential_id},
            )

        except Exception as e:
            logger.error("Failed to delete credential", error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to delete credential {credential_id}",
                error=str(e),
            )

    @app.tool()
    async def list_credential_types() -> ToolResponse:
        """List common credential types available in n8n.

        Returns:
            ToolResponse with available credential types
        """
        credential_types = {
            "httpBasicAuth": "HTTP Basic Authentication",
            "httpQueryAuth": "HTTP Query Authentication (API key in URL)",
            "httpHeaderAuth": "HTTP Header Authentication",
            "oAuth2Api": "OAuth2 Authentication",
            "jwtAuth": "JWT Authentication",
            "slackApi": "Slack API",
            "googleApi": "Google API OAuth2",
            "githubApi": "GitHub API",
            "aws": "AWS Credentials",
            "smtp": "SMTP Email Credentials",
            "mysql": "MySQL Database",
            "postgres": "PostgreSQL Database",
            "redis": "Redis Database",
            "ssh": "SSH Credentials",
        }

        return ToolResponse(
            success=True,
            message="Common credential types",
            data={"credential_types": credential_types},
        )
