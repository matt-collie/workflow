# VFX Pipeline Multi-Agent System

A collection of specialized Claude Code agents designed for visual effects production pipelines.

## Overview

This repository provides specialized AI agents for different aspects of VFX production. Each agent is an expert in a specific domain, helping artists, TDs, and coordinators with their daily workflows.

## Claude Code Agents

Agents are defined as markdown files in `.claude/agents/` and can be invoked within Claude Code for specialized assistance.

### Available Agents

1. **Asset Agent** (`.claude/agents/asset-agent.md`)
   - Asset publishing and versioning
   - Naming convention validation
   - Dependency tracking
   - Asset library management

2. **Shot Agent** (`.claude/agents/shot-agent.md`)
   - Shot setup and breakdown
   - Task assignment and tracking
   - Department coordination
   - Production scheduling

3. **Render Agent** (`.claude/agents/render-agent.md`)
   - Render job submission and monitoring
   - Farm resource optimization
   - Error troubleshooting
   - Priority management

4. **Review Agent** (`.claude/agents/review-agent.md`)
   - Review session coordination
   - Feedback collection and routing
   - Approval tracking
   - Dailies management

5. **Pipeline Agent** (`.claude/agents/pipeline-agent.md`)
   - Technical troubleshooting
   - Tool development assistance
   - Environment validation
   - Integration support

6. **Production Agent** (`.claude/agents/production-agent.md`)
   - Production tracking and reporting
   - Resource allocation
   - Schedule management
   - Progress metrics

See [.claude/README.md](.claude/README.md) for detailed agent documentation.

## Directory Structure

```
.
├── .claude/
│   ├── agents/              # Claude Code agent definitions (markdown)
│   │   ├── asset-agent.md
│   │   ├── shot-agent.md
│   │   ├── render-agent.md
│   │   ├── review-agent.md
│   │   ├── pipeline-agent.md
│   │   └── production-agent.md
│   └── README.md            # Agent usage guide
├── agents/                  # Reference Python implementations
├── shared/                  # Shared utilities and models
├── config/                  # Configuration examples
├── docs/                    # Architecture documentation
└── examples/                # Example workflows
```

## Getting Started

### Using Claude Code Agents

The agents in `.claude/agents/` are ready to use with Claude Code. Simply invoke the appropriate agent when you need specialized help with VFX tasks.

**Examples:**
- Need help publishing an asset? Use the Asset Agent
- Setting up a new shot? Use the Shot Agent
- Troubleshooting render issues? Use the Render Agent

### Reference Implementation

The `agents/` directory contains Python reference implementations showing how you might build automation tools around these agent concepts. See `examples/` for workflow demonstrations.

## Typical Workflows

### Asset Publishing
1. Asset Agent helps validate naming and structure
2. Asset Agent guides through publishing process
3. Production Agent updates tracking

### Shot Production
1. Shot Agent sets up shot and breaks down tasks
2. Department artists complete work
3. Render Agent manages render submissions
4. Review Agent coordinates feedback
5. Production Agent tracks progress

### Technical Support
1. Pipeline Agent helps diagnose issues
2. Pipeline Agent suggests solutions
3. Pipeline Agent validates fixes

## Integration Points

These agents are designed to work with industry-standard VFX tools:
- **Shotgun/Flow Production Tracking**
- **Deadline/Tractor** (render management)
- **RV/Syncsketch** (review tools)
- **Maya/Houdini/Nuke** (DCC applications)
- **Git/Perforce** (version control)

## Customization

You can customize agents for your studio by editing the markdown files in `.claude/agents/`:
- Update naming conventions
- Add studio-specific tools
- Include custom workflows
- Add department guidelines

## License

[Your License]

## Contact

[Your Contact Information]
