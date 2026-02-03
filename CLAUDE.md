# CLAUDE.md - AI Assistant Guide

This document provides essential context for AI assistants working with this repository.

## Project Overview

This is a **Multi-Agent Development and VFX Production System** providing specialized Claude Code agents for software development and VFX production workflows. The repository contains:

- **12 specialized AI agent definitions** (markdown-based)
- **Python reference implementations** for VFX agents
- **Comprehensive documentation** for workflows and architecture

## Quick Reference

| Task | Agent to Use |
|------|--------------|
| Technology research | `.claude/agents/research-agent.md` |
| Writing code/features | `.claude/agents/development-agent.md` |
| System architecture | `.claude/agents/design-agent.md` |
| Code review | `.claude/agents/code-review-agent.md` |
| Git/version control | `.claude/agents/git-workflow-agent.md` |
| Writing tests | `.claude/agents/testing-agent.md` |
| VFX asset management | `.claude/agents/asset-agent.md` |
| VFX shot production | `.claude/agents/shot-agent.md` |
| Render farm operations | `.claude/agents/render-agent.md` |
| Review/feedback | `.claude/agents/review-agent.md` |
| Pipeline/technical | `.claude/agents/pipeline-agent.md` |
| Production tracking | `.claude/agents/production-agent.md` |

## Directory Structure

```
.
├── .claude/                    # Claude Code agent definitions
│   ├── agents/                 # 12 agent markdown files
│   │   ├── research-agent.md       # Technology research
│   │   ├── development-agent.md    # Code implementation
│   │   ├── design-agent.md         # Architecture design
│   │   ├── code-review-agent.md    # Code quality review
│   │   ├── git-workflow-agent.md   # Git workflows
│   │   ├── testing-agent.md        # Testing strategies
│   │   ├── asset-agent.md          # VFX asset management
│   │   ├── shot-agent.md           # VFX shot production
│   │   ├── render-agent.md         # Render farm management
│   │   ├── review-agent.md         # Review workflows
│   │   ├── pipeline-agent.md       # Pipeline support
│   │   └── production-agent.md     # Production tracking
│   └── README.md               # Agent usage guide
├── agents/                     # Python reference implementations
│   ├── asset/                  # AssetAgent implementation
│   ├── shot/                   # ShotAgent implementation
│   ├── render/                 # RenderAgent implementation
│   ├── review/                 # ReviewAgent implementation
│   ├── pipeline/               # PipelineAgent implementation
│   └── production/             # ProductionAgent implementation
├── shared/                     # Shared utilities and data models
│   ├── base_agent.py           # BaseAgent abstract class
│   └── models/base.py          # Data models (Task, Asset, Shot, etc.)
├── config/
│   └── agents.yaml             # Agent configurations
├── docs/
│   ├── ARCHITECTURE.md         # System architecture
│   └── GIT_WORKFLOW.md         # Git workflow guide
├── examples/                   # Example workflows
│   ├── example_asset_workflow.py
│   ├── example_shot_workflow.py
│   └── example_multi_agent_workflow.py
├── agent_coordinator.py        # Central orchestration
├── requirements.txt            # Python dependencies
└── README.md                   # Main documentation
```

## Git Workflow

This repository follows **GitHub Flow** with a protected main branch.

### Branch Naming Convention

```
<type>/<description>-<issue-number>
```

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New features | `feature/add-testing-agent-123` |
| `bugfix/` | Bug fixes | `bugfix/fix-agent-import-456` |
| `hotfix/` | Critical fixes | `hotfix/security-patch-789` |
| `refactor/` | Code refactoring | `refactor/cleanup-agents-234` |
| `docs/` | Documentation | `docs/update-readme-567` |
| `test/` | Test additions | `test/add-unit-tests-890` |
| `chore/` | Maintenance | `chore/update-deps-345` |

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`

**Examples**:
```
feat(agents): add deployment agent for CI/CD

Implement new deployment agent with support for multiple targets.

Closes #123
```

```
fix(render): resolve frame chunking calculation

The frame chunk size was incorrectly computed for sequences
with non-standard frame ranges.

Fixes #456
```

### Pull Request Guidelines

- **PR Size**: Keep PRs under 500 lines (ideally < 200)
- **Require**: At least 1 approval before merge
- **Ensure**: CI passes before merging
- **Prefer**: Squash and merge for clean history
- **Always**: Delete branch after merge

## Code Conventions

### Python Style

- **Formatter**: Black (`black>=23.0.0`)
- **Linter**: Flake8 (`flake8>=6.0.0`)
- **Type Checking**: mypy (`mypy>=1.4.0`)
- **Testing**: pytest (`pytest>=7.4.0`)

### Running Quality Checks

```bash
# Format code
black .

# Lint code
flake8 .

# Type check
mypy .

# Run tests
pytest

# Run tests with coverage
pytest --cov
```

### Agent Development Pattern

When creating new agents, follow the `BaseAgent` pattern:

```python
from shared.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def __init__(self, config_path):
        super().__init__(config_path, "new_agent")

    def _define_capabilities(self):
        return ["action1", "action2"]

    def process_request(self, request):
        # Handle request based on action
        pass
```

### Data Models

Use the shared data models from `shared/models/base.py`:

- `Status`: PENDING, IN_PROGRESS, WAITING, REVIEW, APPROVED, FINAL, ON_HOLD, CANCELLED
- `Priority`: LOW, MEDIUM, HIGH, CRITICAL
- `Task`: Production tasks with dependencies
- `Asset`: VFX assets with versioning
- `Shot`: Production shots
- `RenderJob`: Render job tracking
- `AgentRequest` / `AgentResponse`: Agent communication

## Configuration

Agent settings are in `config/agents.yaml`:

- Asset paths and naming conventions
- Shot templates and department workflows
- Render farm settings
- Review tool configurations
- Pipeline integrations (Shotgun, Deadline, Perforce)
- Global settings (logging, database, caching)

## Key Workflows

### Software Development Flow

1. **Research** → Technology evaluation
2. **Design** → Architecture planning
3. **Development** → Feature implementation
4. **Testing** → Test writing and coverage
5. **Code Review** → Quality verification
6. **Git Workflow** → PR and merge

### VFX Production Flow

1. **Asset Agent** → Publish and validate assets
2. **Shot Agent** → Set up shots, break down tasks
3. **Render Agent** → Submit and monitor renders
4. **Review Agent** → Collect feedback, track approvals
5. **Production Agent** → Track progress, generate reports

### Pipeline Tool Development (Cross-Domain)

1. **Research Agent** → Research best approach
2. **Design Agent** → Design tool architecture
3. **Development Agent** → Implement the tool
4. **Testing Agent** → Write tests
5. **Pipeline Agent** → Deploy and integrate

## Important Files to Know

| File | Purpose |
|------|---------|
| `agent_coordinator.py` | Central orchestration for multi-agent workflows |
| `shared/base_agent.py` | Abstract base class all agents extend |
| `shared/models/base.py` | Core data models and enums |
| `config/agents.yaml` | All agent configurations |
| `docs/GIT_WORKFLOW.md` | Complete git workflow documentation |
| `docs/ARCHITECTURE.md` | System architecture details |

## Testing Requirements

- Write tests for new functionality
- Maintain test coverage
- Tests live alongside code or in `tests/` directory
- Use pytest fixtures for setup

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run example workflows
python examples/example_asset_workflow.py
python examples/example_shot_workflow.py
python examples/example_multi_agent_workflow.py

# Format and lint
black . && flake8 .

# Type check
mypy .

# Run tests
pytest -v
```

## Integration Points

### Software Development
- Git, GitHub, GitLab
- GitHub Actions, Jenkins, CircleCI
- Jest, Pytest, Playwright, Cypress
- React, Vue, Node.js, FastAPI, Django

### VFX Production
- Shotgun/Flow Production Tracking, ftrack
- Deadline, Tractor (render management)
- RV, Syncsketch (review tools)
- Maya, Houdini, Nuke, Blender, Substance, ZBrush

## Do's and Don'ts

### Do
- Use appropriate agent for the task
- Follow conventional commit messages
- Keep PRs small and focused
- Write tests for new functionality
- Update documentation when adding features
- Use shared data models for consistency

### Don't
- Commit directly to main
- Force push to shared branches
- Commit sensitive data (secrets, API keys)
- Skip code review
- Create large monolithic PRs
- Ignore type hints in Python code

## Getting Help

1. Check agent definitions in `.claude/agents/`
2. Review documentation in `docs/`
3. Examine examples in `examples/`
4. Reference `shared/` for data models and base classes
