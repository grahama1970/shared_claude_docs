# Claude Bot - Telegram Interface for Granger

## Overview

Claude Bot (`claude_bot`) is a Telegram bot that serves as a mobile interface to the Granger ecosystem. It enables users to control and monitor the entire Granger system from their phones, execute Claude CLI commands, and run any slash command from `~/.claude/commands`.

## Key Features

### 1. **Claude CLI Integration**
- Execute Claude prompts remotely via Telegram
- Support for all Claude models
- Local or SSH execution modes
- Configurable timeouts for long operations

### 2. **Granger Hub Integration**
- WebSocket connection to Granger Hub
- Module registration and heartbeat
- Inter-module messaging
- Real-time status monitoring

### 3. **Slash Command Execution**
- Access to all commands in `~/.claude/commands`
- Including `/granger-verify`, `/arxiv-search`, etc.
- Full parameter support
- Async execution for long-running commands

### 4. **Security Features**
- User ID allowlist (only authorized Telegram users)
- Secure local/SSH execution
- Environment variable isolation
- Audit logging

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Telegram App   │────▶│   claude_bot     │────▶│  Granger Hub    │
│  (Mobile/PC)    │     │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │                         │
                               ▼                         ▼
                        ┌─────────────┐          ┌──────────────┐
                        │ Claude CLI  │          │ Spoke Modules│
                        │             │          │              │
                        └─────────────┘          └──────────────┘
```

## Module Structure

```
claude_bot/
├── core/               # Business logic
│   ├── ssh_executor.py # Claude CLI execution
│   └── slash_executor.py # Slash command handling
├── cli/                # Interface layer
│   ├── telegram_bot.py # Main bot implementation
│   └── granger_commands.py # /granger command handlers
├── granger/            # Granger integration
│   ├── hub_client.py   # WebSocket client
│   ├── message_format.py # Message protocols
│   └── module_registry.py # Module tracking
└── config.py           # Configuration management
```

## Commands

### Telegram Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message and instructions | `/start` |
| `/help` | Show all available commands | `/help` |
| `/model` | Set Claude model for session | `/model opus` |
| `/reset` | Reset to default model | `/reset` |
| `/granger` | Granger ecosystem commands | `/granger status` |
| `/commands` | List available slash commands | `/commands` |

### Granger Subcommands

- `/granger status` - Hub connection and module status
- `/granger test` - Test Hub communication
- `/granger verify` - Verify ecosystem health
- `/granger modules` - List connected modules
- `/granger sync` - Sync with Hub state

## Configuration

### Environment Variables

```env
# Telegram Configuration
TELEGRAM_BOT_NAME=horus9_bot
TELEGRAM_TOKEN=your_bot_token
ALLOWED_TELEGRAM_IDS=7957197311,other_id

# Execution Mode
SSH_TARGET=local  # or hostname for remote
DEFAULT_CLAUDE_MODEL=opus

# Granger Integration
GRANGER_HUB_URL=http://localhost:8000
REDIS_URL=redis://localhost:6379
ARANGO_HOST=http://localhost:8529
```

### Model Shortcuts

The bot supports convenient model shortcuts:
- `haiku` → `claude-3-haiku-20240307`
- `sonnet` → `claude-3-5-sonnet-20241022`
- `opus` → `claude-3-opus-20240229`

## Integration Points

### 1. **Granger Hub**
- Registers as module type "telegram_bot"
- Capabilities: ["claude", "llm_routing", "task_management", "slash_commands"]
- Maintains WebSocket connection with heartbeat

### 2. **Claude CLI**
- Direct execution for local mode
- SSH execution for remote workstations
- Supports all Claude CLI parameters

### 3. **Slash Commands**
- Discovers commands from `~/.claude/commands`
- Executes with full parameter support
- Returns formatted output to Telegram

## Testing

The project includes comprehensive REAL integration tests:

### Test Categories
1. **Honeypot Tests** - Designed to fail, verify framework integrity
2. **Integration Tests** - Real API calls, no mocks
3. **Duration Tests** - Verify operations take realistic time

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific categories
pytest tests/test_honeypot.py -v
pytest tests/integration/test_real_telegram_bot.py -v

# Test verification
python run_test_verification.py
```

## Usage Examples

### Basic Claude Query
```
User: Explain quantum computing
Bot: ⌛ Processing your prompt...
Bot: Quantum computing uses quantum bits (qubits) that can exist in superposition...
```

### Granger Status Check
```
User: /granger status
Bot: 🌐 Granger Hub Status:
Connection: ✅ Connected
Modules: 5 active
- claude_bot: ✅ Active
- arxiv_mcp_server: ✅ Active
...
```

### Slash Command Execution
```
User: /granger-verify --project granger_hub --quick
Bot: ⌛ Executing slash command...
Bot: ✅ Verification complete:
- Tests: 45/45 passed
- Coverage: 87%
```

## Deployment

### Systemd Service
```ini
[Unit]
Description=Claude Telegram Bot for Granger
After=network.target

[Service]
Type=simple
User=graham
WorkingDirectory=/home/graham/workspace/experiments/claude_bot
ExecStart=/home/graham/workspace/experiments/claude_bot/.venv/bin/python -m claude_bot.bot
Restart=always

[Install]
WantedBy=multi-user.target
```

### Docker (Planned)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["python", "-m", "claude_bot.bot"]
```

## Security Considerations

1. **Access Control**
   - Only whitelisted Telegram user IDs can use the bot
   - Each user's commands are isolated
   - No command injection vulnerabilities

2. **Execution Safety**
   - Commands run with bot user permissions
   - Timeout limits prevent runaway processes
   - Output sanitized for Telegram

3. **Data Privacy**
   - No conversation history stored
   - Environment variables isolated
   - Secure WebSocket for Hub communication

## Roadmap

### Completed ✅
- Basic Claude CLI integration
- Telegram bot interface
- Granger Hub connection
- Slash command execution
- Module registry integration
- Comprehensive test suite

### In Progress 🚧
- Task management with ArangoDB
- Multi-LLM routing (Gemini, GPT-4)
- Enhanced mobile UI with inline keyboards

### Planned 📋
- Voice command support
- Scheduled task automation
- Advanced security features
- Performance optimization
- Docker deployment

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check Telegram token
   - Verify user ID in allowlist
   - Check systemd logs

2. **Claude Errors**
   - Verify Claude CLI installed
   - Check PATH configuration
   - Test SSH connection manually

3. **Hub Connection Issues**
   - Ensure Hub is running
   - Check WebSocket port
   - Verify network connectivity

## Related Modules

- **granger_hub** - Central orchestration
- **llm_call** - Multi-LLM routing (planned integration)
- **arangodb** - Task storage (planned integration)
- **world_model** - Predictive capabilities (future)

## Contributing

1. Follow NO MOCKS testing policy
2. Maintain 3-layer architecture
3. Add tests for new features
4. Update documentation

## License

MIT License - Part of the Granger Ecosystem