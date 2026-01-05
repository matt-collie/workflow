# Multi-Agent VFX Pipeline System

A modular multi-agent architecture designed for visual effects production pipelines.

## Overview

This system implements specialized agents for different aspects of VFX production, enabling automated workflows, intelligent task management, and seamless department coordination.

## Architecture

### Agent Types

1. **Asset Agent** (`agents/asset/`)
   - Asset creation and versioning
   - Asset publishing and approval
   - Library management and search
   - Dependency tracking

2. **Shot Agent** (`agents/shot/`)
   - Shot tracking and status updates
   - Task assignment and scheduling
   - Shot breakdown and planning
   - Sequence management

3. **Render Agent** (`agents/render/`)
   - Render job submission and monitoring
   - Farm resource allocation
   - Priority management
   - Error detection and recovery

4. **Review Agent** (`agents/review/`)
   - Dailies session management
   - Client review coordination
   - Feedback collection and routing
   - Version comparison

5. **Pipeline Agent** (`agents/pipeline/`)
   - Tool development assistance
   - Technical troubleshooting
   - Pipeline optimization
   - Integration management

6. **Production Agent** (`agents/production/`)
   - Production tracking and reporting
   - Resource allocation
   - Schedule management
   - Deliverable tracking

## Directory Structure

```
.
├── agents/              # Individual agent implementations
│   ├── asset/          # Asset management agent
│   ├── shot/           # Shot production agent
│   ├── render/         # Render farm agent
│   ├── review/         # Review & approval agent
│   ├── pipeline/       # Pipeline TD agent
│   └── production/     # Production management agent
├── shared/             # Shared resources
│   ├── utils/          # Common utilities
│   ├── models/         # Data models
│   └── database/       # Database interfaces
├── config/             # Configuration files
├── docs/               # Documentation
├── examples/           # Example workflows
├── scripts/            # Utility scripts
└── tests/              # Test suite
```

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit `config/agents.yaml` to customize agent settings for your pipeline.

### Running Agents

```python
from agents.asset.agent import AssetAgent

# Initialize agent
agent = AssetAgent(config_path="config/agents.yaml")

# Execute task
result = agent.process_request("publish asset: character_hero_v003")
```

## Typical Workflows

### Asset Publishing Workflow
1. Artist completes asset
2. Asset Agent validates structure and naming
3. Asset Agent publishes to library
4. Review Agent notifies stakeholders
5. Production Agent updates tracking

### Shot Production Workflow
1. Shot Agent receives shot assignment
2. Shot Agent breaks down tasks by department
3. Render Agent monitors render completion
4. Review Agent collects feedback
5. Production Agent tracks milestones

### Render Management Workflow
1. Render Agent receives submission
2. Render Agent allocates farm resources
3. Render Agent monitors progress
4. Render Agent handles errors/retries
5. Render Agent notifies on completion

## Integration Points

- **Shotgun/Flow Production Tracking**: Production database integration
- **Deadline/Tractor**: Render farm management
- **RV/Syncsketch**: Review and playback tools
- **Perforce/Git**: Version control systems
- **Maya/Houdini/Nuke**: DCC applications

## Development

### Adding New Agents

1. Create directory under `agents/`
2. Implement agent class extending `BaseAgent`
3. Define capabilities in agent config
4. Add tests in `tests/`

### Testing

```bash
pytest tests/
```

## License

[Your License]

## Contact

[Your Contact Information]
