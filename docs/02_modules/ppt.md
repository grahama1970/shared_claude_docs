# PPT - PowerPoint Automation Module

**Purpose:** Autonomous PowerPoint presentation generation and updates  
**Path:** `/home/graham/workspace/experiments/ppt/`  
**Status:** Active  
**Version:** v0.1.0  

## Overview

PPT is a GRANGER ecosystem module that enables autonomous PowerPoint presentation creation and updates. It monitors data sources through granger_hub and automatically keeps presentations synchronized with the latest ecosystem data.

## Key Features

### 🎯 Core Capabilities
- **Autonomous Updates**: Monitors ArangoDB collections and updates presentations automatically
- **Natural Language Commands**: Agent interface for AI-driven modifications via llm_call
- **Template Support**: Pre-designed templates for consistent styling
- **Data Visualization**: Automatic chart and table generation from data
- **Incremental Updates**: Smart updating of only changed content
- **GRANGER Hub Integration**: Event-driven updates from ecosystem changes

### 🔧 Technical Features
- Built on python-pptx for robust PowerPoint manipulation
- Async monitoring with configurable update intervals
- Message-based communication with granger_hub
- Fallback behavior when dependencies unavailable
- Comprehensive test coverage (no mocks)

## Architecture

```
ppt/
├── core/
│   ├── autonomous.py      # Autonomous monitoring and updates
│   ├── agent_interface.py # Natural language command processing
│   ├── builder.py         # Presentation creation
│   ├── editor.py          # Presentation modification
│   ├── message_handler.py # GRANGER Hub communication
│   └── hub_integration.py # Hub module implementation
├── cli/
│   └── app.py            # Command-line interface
└── mcp/
    └── server.py         # MCP server (future)
```

## Usage

### Command Line Interface

```bash
# Create new presentation
granger-ppt create --title "Q1 Report" --template modern

# Update existing presentation
granger-ppt edit report.pptx --find "2023" --replace "2024"

# Monitor for updates
granger-ppt monitor --config monitor.json
```

### Slash Commands

```bash
# Create presentation
/ppt-create "Research Overview" --template academic --slides 15

# Update presentation
/ppt-update deck.pptx --add-slide --title "New Results"

# Monitor presentations
/ppt-monitor --presentation report.pptx --collections papers,metrics
```

### Python API

```python
from ppt import PresentationBuilder, PresentationEditor, AutonomousPresenter

# Create presentation
builder = PresentationBuilder(template="modern")
builder.add_title_slide("AI Research Overview")
builder.add_content_slide("Key Findings", bullets=findings)
builder.save("research.pptx")

# Edit presentation
editor = PresentationEditor("existing.pptx")
editor.update_text("old text", "new text")
editor.add_chart(data, chart_type="bar")
editor.save()

# Autonomous monitoring
config = {
    "presentation_mappings": {
        "report.pptx": ["papers", "metrics"]
    }
}
presenter = AutonomousPresenter(config)
await presenter.start_monitoring()
```

## Integration with GRANGER Hub

PPT integrates with granger_hub as a ConversationModule:

```python
from ppt.core.hub_integration import PPTModule

# Module registration happens automatically
ppt_module = PPTModule()

# Handles messages from hub
await ppt_module.handle_conversation_message(message)
```

### Message Types Supported
- `create_presentation`: Generate new presentations
- `update_presentation`: Modify existing presentations  
- `extract_content`: Extract content from presentations
- `monitor_updates`: Set up autonomous monitoring

## Configuration

### Monitor Configuration (JSON)

```json
{
  "presentation_mappings": {
    "research_overview.pptx": ["papers", "findings"],
    "metrics_dashboard.pptx": ["metrics", "performance"],
    "quarterly_report.pptx": ["papers", "metrics", "milestones"]
  },
  "update_strategy": "incremental",
  "check_interval": 300,
  "llm_config": {
    "provider": "granger_hub",
    "model": "gpt-4"
  }
}
```

### Update Strategies
- **incremental**: Update only changed slides (default)
- **full_rebuild**: Regenerate entire presentation
- **smart**: AI decides based on change scope

## Dependencies

### Required
- python-pptx: PowerPoint file manipulation
- typer: CLI framework
- pydantic: Data validation
- loguru: Logging

### Optional (via granger_hub)
- llm_call: AI-powered content generation
- arangodb: Data source for content
- granger_hub: Event monitoring and orchestration

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/test_honeypot.py
```

All tests use real file I/O operations - no mocking per CLAUDE.md standards.

## Examples

### Example 1: Research Report Automation

```python
# Configure autonomous presenter
config = {
    "presentation_mappings": {
        "ai_research_2024.pptx": ["papers", "experiments", "results"]
    },
    "update_strategy": "smart",
    "templates": {
        "papers": "research_slide",
        "experiments": "data_slide",
        "results": "chart_slide"
    }
}

# Start monitoring
presenter = AutonomousPresenter(config)
await presenter.start_monitoring()
```

### Example 2: Natural Language Updates

```python
from ppt.core.agent_interface import AgentInterface

agent = AgentInterface()

# Natural language commands
agent.execute("Update the Q1 report with latest metrics from January")
agent.execute("Add a new slide showing revenue growth chart")
agent.execute("Change all instances of '2023' to '2024' in the presentation")
```

### Example 3: Data-Driven Charts

```python
from ppt import PresentationBuilder
import pandas as pd

# Load data
df = pd.read_csv("metrics.csv")

# Create presentation with charts
builder = PresentationBuilder()
builder.add_title_slide("Performance Metrics")
builder.add_chart_slide(
    title="Monthly Revenue",
    data=df,
    chart_type="line",
    x_column="month",
    y_column="revenue"
)
builder.save("metrics_report.pptx")
```

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'pptx'**
   ```bash
   pip install python-pptx
   ```

2. **granger_hub not available**
   - PPT will work in standalone mode
   - Natural language features may be limited
   - Install granger_hub for full functionality

3. **ArangoDB connection failed**
   - Check credentials in .env file
   - Ensure ArangoDB is running
   - Verify ARANGO_* environment variables

## Future Enhancements

- [ ] MCP server implementation
- [ ] Real-time collaboration features
- [ ] Advanced animation support
- [ ] PDF export functionality
- [ ] Web-based preview interface
- [ ] Integration with more data sources
- [ ] Custom theme designer

## Related Modules

- **granger_hub**: Provides orchestration and LLM access
- **arangodb**: Data source for presentation content
- **marker**: Extract content from existing presentations
- **llm_call**: Generate intelligent content and summaries

## License

MIT License - Part of the GRANGER ecosystem