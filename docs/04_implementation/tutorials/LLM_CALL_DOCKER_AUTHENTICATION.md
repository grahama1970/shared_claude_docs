# LLM Call Docker Authentication Guide

## Overview

The llm_call project includes Docker support with special handling for Claude Max/Opus authentication. This guide covers the streamlined authentication process for Claude CLI within Docker containers.

## Quick Start

### 1. Start Docker Services

```bash
cd llm_call
docker compose up -d
```

### 2. Authenticate Claude (First Time Only)

```bash
# Use the authentication helper
./docker/claude-proxy/authenticate.sh

# Inside the container:
# 1. Type 'claude' to launch Claude Code
# 2. Authenticate with your Claude account
# 3. Exit with Ctrl+C
# 4. Type 'exit' to leave container
```

### 3. Verify Authentication

```bash
# Run the test script
./docker/claude-proxy/test_claude.sh

# Or check status directly
curl http://localhost:3010/health | jq .claude_authenticated
```

## Features

### Shell Enhancements

When you enter the Claude proxy container, you'll see:

```
================================================
🤖 Claude CLI Proxy Container
================================================

✅ Claude is authenticated and ready!

Helpful commands:
  • auth       - Authenticate with Claude
  • test-auth  - Test authentication status
  • claude     - Launch Claude Code
  • exit       - Leave container

================================================
```

### Convenient Aliases

Install host machine aliases for easier access:

```bash
./scripts/install_claude_aliases.sh
source ~/.zshrc  # or ~/.bashrc

# Now you can use:
claude-auth    # Authenticate Claude in Docker
claude-test    # Test authentication status
claude-shell   # Open shell in container
claude-status  # Check auth status (JSON)
```

## Authentication Details

### Method: OAuth via Claude Code

- Uses Claude Max subscription (NOT Anthropic API keys)
- Credentials stored in `~/.claude/` (mounted from host)
- Persists across container restarts
- One-time setup per Claude account

### Health Endpoint

The Claude proxy provides a health endpoint with authentication status:

```bash
curl http://localhost:3010/health
```

Response includes:
- `claude_authenticated`: boolean
- `auth_status`: detailed status message

## Troubleshooting

### "Not authenticated" Error
```bash
./docker/claude-proxy/authenticate.sh
```

### Container Not Running
```bash
docker compose ps
docker compose up -d claude-proxy
```

### Port 3010 Already in Use
```bash
# Find and stop the process using port 3010
lsof -i :3010
# Or change the port in docker-compose.yml
```

### Authentication Fails Inside Container
- Ensure you have a valid Claude Max subscription
- Try logging out and back in:
  ```bash
  docker exec -it llm-call-claude-proxy /bin/bash
  claude auth logout
  claude auth login
  ```

## Architecture

The Docker setup includes:
- **API Service**: Main llm_call API (port 8001)
- **Claude Proxy**: Handles Claude CLI requests (port 3010)
- **Redis**: Caching and state management
- **Ollama** (optional): Local model inference

## Environment Variables

Key variables for Claude proxy:
```bash
CLAUDE_PROXY_URL=http://claude-proxy:3010
ENABLE_LLM_VALIDATION=false  # Disable for Claude Max
```

## Related Documentation

- [Docker Compose Setup](../../03_modules/spokes/005_Describe_llm_call.md)
- [LLM Call Overview](../../../README.md)
- [Authentication Guide](llm_call/docker/claude-proxy/AUTHENTICATION.md)