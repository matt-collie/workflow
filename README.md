# Multi-Agent Development System

A comprehensive collection of specialized Claude Code agents for software development and VFX production workflows.

## Overview

This repository provides specialized AI agents for different aspects of software development and VFX production. Each agent is an expert in a specific domain, providing targeted assistance for development teams and production studios.

## Claude Code Agents

Agents are defined as markdown files in `.claude/agents/` and can be invoked within Claude Code for specialized assistance.

### Software Development Agents

1. **Research Agent** (`.claude/agents/research-agent.md`)
   - Technology evaluation and comparison
   - Library and framework research
   - Problem investigation
   - Solution feasibility analysis

2. **Development Agent** (`.claude/agents/development-agent.md`)
   - Feature implementation
   - Bug fixes and debugging
   - Code refactoring
   - Best practices

3. **Design Agent** (`.claude/agents/design-agent.md`)
   - System architecture design
   - API design and specification
   - Database schema design
   - Design pattern selection

4. **Code Review Agent** (`.claude/agents/code-review-agent.md`)
   - Pull request reviews
   - Security and quality checks
   - Best practices verification
   - Improvement suggestions

5. **Git Workflow Agent** (`.claude/agents/git-workflow-agent.md`)
   - Branching strategies
   - Pull request workflows
   - Merge conflict resolution
   - Release management

6. **Testing Agent** (`.claude/agents/testing-agent.md`)
   - Unit and integration testing
   - Test strategy design
   - Test automation
   - Coverage analysis

### VFX Production Agents

7. **Asset Agent** (`.claude/agents/asset-agent.md`)
   - Asset publishing and versioning
   - Naming convention validation
   - Dependency tracking
   - Asset library management

8. **Shot Agent** (`.claude/agents/shot-agent.md`)
   - Shot setup and breakdown
   - Task assignment and tracking
   - Department coordination
   - Production scheduling

9. **Render Agent** (`.claude/agents/render-agent.md`)
   - Render job submission and monitoring
   - Farm resource optimization
   - Error troubleshooting
   - Priority management

10. **Review Agent** (`.claude/agents/review-agent.md`)
    - Review session coordination
    - Feedback collection and routing
    - Approval tracking
    - Dailies management

11. **Pipeline Agent** (`.claude/agents/pipeline-agent.md`)
    - Technical troubleshooting
    - Tool development assistance
    - Environment validation
    - Integration support

12. **Production Agent** (`.claude/agents/production-agent.md`)
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

### Git Workflow

This repository follows **GitHub Flow** with a protected main branch:

1. **Create feature branch** from main: `feature/my-feature-123`
2. **Make changes** and commit with conventional commit messages
3. **Push branch** and create pull request
4. **Code review** and approval required
5. **Merge to main** after approval and CI passes

See [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) for complete workflow documentation.

**Branch Naming:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Test additions

### Using Claude Code Agents

The agents in `.claude/agents/` are ready to use with Claude Code. Simply invoke the appropriate agent when you need specialized assistance.

**Software Development Examples:**
- Need to research a technology? Use the Research Agent
- Implementing a new feature? Use the Development Agent
- Designing an API? Use the Design Agent
- Reviewing code? Use the Code Review Agent
- Git workflow question? Use the Git Workflow Agent
- Writing tests? Use the Testing Agent

**VFX Production Examples:**
- Publishing an asset? Use the Asset Agent
- Setting up a shot? Use the Shot Agent
- Render troubleshooting? Use the Render Agent
- Review coordination? Use the Review Agent

### Reference Implementation

The `agents/` directory contains Python reference implementations showing how you might build automation tools around these agent concepts. See `examples/` for workflow demonstrations.

## Typical Workflows

### Software Development Workflows

#### New Feature Development
1. **Research Agent**: Evaluate technology options
2. **Design Agent**: Design architecture and APIs
3. **Development Agent**: Implement the feature
4. **Testing Agent**: Write tests and ensure coverage
5. **Code Review Agent**: Review before submitting PR
6. **Git Workflow Agent**: Create PR and merge

#### Bug Fix Workflow
1. **Development Agent**: Diagnose and fix the bug
2. **Testing Agent**: Add regression tests
3. **Code Review Agent**: Review the fix
4. **Git Workflow Agent**: Submit hotfix PR

### VFX Production Workflows

#### Asset Publishing
1. **Asset Agent**: Validate naming and structure
2. **Asset Agent**: Guide through publishing process
3. **Production Agent**: Update tracking

#### Shot Production
1. **Shot Agent**: Set up shot and break down tasks
2. Department artists complete work
3. **Render Agent**: Manage render submissions
4. **Review Agent**: Coordinate feedback
5. **Production Agent**: Track progress

### Cross-Domain Workflows

#### Pipeline Tool Development
1. **Research Agent**: Research best approach
2. **Design Agent**: Design tool architecture
3. **Development Agent**: Implement the tool
4. **Testing Agent**: Test the tool
5. **Pipeline Agent**: Deploy and integrate
6. **Code Review Agent**: Review and approve

## Integration Points

### Software Development Tools
- **Version Control**: Git, GitHub, GitLab
- **CI/CD**: GitHub Actions, Jenkins, CircleCI
- **Testing**: Jest, Pytest, Playwright, Cypress
- **Languages**: Python, JavaScript/TypeScript, Go, Rust
- **Frameworks**: React, Vue, Node.js, FastAPI, Django

### VFX Production Tools
- **Production Tracking**: Shotgun/Flow Production Tracking, ftrack
- **Render Management**: Deadline, Tractor
- **Review Tools**: RV, Syncsketch
- **DCC Applications**: Maya, Houdini, Nuke, Blender
- **Version Control**: Git, Perforce

## Customization

You can customize agents by editing the markdown files in `.claude/agents/`:

**For Software Development:**
- Add language-specific guidelines
- Include team coding standards
- Add project-specific workflows
- Reference internal tools and APIs

**For VFX Production:**
- Update naming conventions for your studio
- Add studio-specific tools and integrations
- Include department-specific workflows
- Reference your pipeline tools

## Documentation

- [Agent Usage Guide](.claude/README.md) - Detailed agent documentation
- [Git Workflow Guide](docs/GIT_WORKFLOW.md) - Complete git workflow
- [Architecture](docs/ARCHITECTURE.md) - System architecture (reference implementation)

## Contributing

1. Create a feature branch: `feature/your-feature-123`
2. Make your changes
3. Write tests if applicable
4. Submit a pull request
5. Ensure CI passes and get approval

See [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md) for detailed workflow.

## License

[Your License]

## Contact

[Your Contact Information]
