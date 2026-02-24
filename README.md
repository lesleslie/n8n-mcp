# n8n-mcp

MCP server for n8n workflow automation.

## Installation

```bash
uv pip install -e .
```

## Usage

```bash
# Stdio mode (default)
n8n-mcp serve

# HTTP mode
n8n-mcp serve --http --port 3044

# With mock mode for testing
n8n-mcp serve --mock

# With custom n8n URL
n8n-mcp serve --n8n-url http://localhost:5678
```

## Tools

**Workflows:**
- `list_workflows` - List all workflows
- `get_workflow` - Get workflow details
- `create_workflow` - Create new workflow
- `update_workflow` - Update workflow
- `delete_workflow` - Delete workflow
- `activate_workflow` - Activate workflow
- `deactivate_workflow` - Deactivate workflow

**Executions:**
- `execute_workflow` - Execute a workflow
- `list_executions` - List executions
- `get_execution` - Get execution details
- `delete_execution` - Delete execution

**Credentials:**
- `list_credentials` - List credentials
- `get_credential` - Get credential details
- `create_credential` - Create credential
- `delete_credential` - Delete credential

## Configuration

Set via environment variables with `N8N_MCP_` prefix:
- `N8N_MCP_N8N_URL` - n8n instance URL (default: http://localhost:5678)
- `N8N_MCP_API_KEY` - n8n API key
- `N8N_MCP_MOCK_MODE` - Enable mock mode
