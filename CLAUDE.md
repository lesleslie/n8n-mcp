# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

**n8n-mcp** is an MCP server for n8n workflow automation, providing workflow management and execution capabilities via the Model Context Protocol.

**Key Dependencies**: Python 3.13+, mcp-common, httpx/aiohttp

## Core Features

- **Workflow Management**: List, create, update, delete, activate/deactivate workflows
- **Execution Control**: Execute workflows, list executions, get execution details
- **Credential Management**: List, create, get, delete credentials
- **Mock Mode**: Testing without real n8n instance

## Most Common Commands

```bash
# Run server (stdio mode)
n8n-mcp serve

# Run server (HTTP mode)
n8n-mcp serve --http --port 3044

# With mock mode for testing
n8n-mcp serve --mock

# With custom n8n URL
n8n-mcp serve --n8n-url http://localhost:5678
```

## Critical Rules

### 1. SECURITY IS NON-NEGOTIABLE

- **NEVER** expose API keys in code
- **ALWAYS** use environment variables for credentials
- **NEVER** log credential values
- **ALWAYS** validate API responses

### 2. N8N API INTEGRATION

- Use `N8N_MCP_N8N_URL` for instance URL
- Use `N8N_MCP_API_KEY` for authentication
- Handle connection errors gracefully

### 3. NO PLACEHOLDERS - EVER

- **NEVER** use dummy workflow IDs or placeholder data
- **ALWAYS** use proper variable references

### 4. MCP-COMMON PATTERNS

- Follow mcp-common patterns for server lifecycle
- Use MCPServerCLIFactory for CLI commands
- Inherit from base settings classes

## Configuration

Set via environment variables with `N8N_MCP_` prefix:

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_MCP_N8N_URL` | n8n instance URL | http://localhost:5678 |
| `N8N_MCP_API_KEY` | n8n API key | - |
| `N8N_MCP_MOCK_MODE` | Enable mock mode | false |

## Tools Provided

**Workflows:**
| Tool | Description |
|------|-------------|
| `list_workflows` | List all workflows |
| `get_workflow` | Get workflow details |
| `create_workflow` | Create new workflow |
| `update_workflow` | Update workflow |
| `delete_workflow` | Delete workflow |
| `activate_workflow` | Activate workflow |
| `deactivate_workflow` | Deactivate workflow |

**Executions:**
| Tool | Description |
|------|-------------|
| `execute_workflow` | Execute a workflow |
| `list_executions` | List executions |
| `get_execution` | Get execution details |
| `delete_execution` | Delete execution |

**Credentials:**
| Tool | Description |
|------|-------------|
| `list_credentials` | List credentials |
| `get_credential` | Get credential details |
| `create_credential` | Create credential |
| `delete_credential` | Delete credential |

## Additional Resources

- **[README.md](./README.md)**: Complete project documentation
- **[mcp-common](../mcp-common)**: Shared MCP utilities
