# Claude Code Agents

This directory contains specialized Claude Code agents for VFX production workflows and software development.

## What are Claude Agents?

Claude Code agents are specialized AI assistants defined using markdown files. Each agent has specific expertise and capabilities tailored to different domains.

## Available Agents

### Software Development Agents

#### Research Agent (`research-agent.md`)
**Expertise**: Technical research and investigation

**Use for**:
- Technology evaluation and comparison
- Library and framework research
- Problem investigation
- Solution feasibility analysis

**Example**: "Compare React vs Vue for our frontend project and recommend which to use"

---

#### Development Agent (`development-agent.md`)
**Expertise**: Software development and coding

**Use for**:
- Implementing new features
- Fixing bugs and defects
- Refactoring code
- Writing tests
- Code optimization

**Example**: "Help me implement JWT authentication for the API"

---

#### Design Agent (`design-agent.md`)
**Expertise**: System architecture and design

**Use for**:
- Architecture design
- API design and specification
- Database schema design
- Design pattern selection
- Technical planning

**Example**: "Design a microservices architecture for our e-commerce platform"

---

#### Code Review Agent (`code-review-agent.md`)
**Expertise**: Code review and quality assurance

**Use for**:
- Reviewing pull requests
- Identifying bugs and issues
- Security review
- Best practices verification
- Suggesting improvements

**Example**: "Review this PR for security vulnerabilities and code quality issues"

---

#### Git Workflow Agent (`git-workflow-agent.md`)
**Expertise**: Version control and collaboration workflows

**Use for**:
- Git branching strategies
- Pull request workflows
- Merge conflict resolution
- Commit message standards
- Release management

**Example**: "Help me resolve this merge conflict and update my branch"

---

#### Testing Agent (`testing-agent.md`)
**Expertise**: Software testing and quality assurance

**Use for**:
- Writing unit and integration tests
- Test strategy design
- Test automation
- Debugging test failures
- Coverage analysis

**Example**: "Write unit tests for this authentication service"

---

### VFX Production Agents

#### Asset Agent (`asset-agent.md`)
**Expertise**: Asset management and publishing workflows

**Use for**:
- Publishing and versioning assets
- Validating asset naming conventions
- Checking asset dependencies
- Organizing asset libraries

**Example**: "Help me publish this character asset and validate it follows our naming convention"

---

### Shot Agent (`shot-agent.md`)
**Expertise**: Shot production and task management

**Use for**:
- Setting up new shots
- Breaking down shots into department tasks
- Tracking shot progress
- Coordinating between departments

**Example**: "Break down SQ010_SH0030 into tasks for layout, animation, and lighting"

---

### Render Agent (`render-agent.md`)
**Expertise**: Render farm management and optimization

**Use for**:
- Submitting render jobs
- Monitoring render progress
- Troubleshooting render errors
- Optimizing render settings

**Example**: "Help me diagnose why frames 1050-1075 are failing to render"

---

### Review Agent (`review-agent.md`)
**Expertise**: Review sessions and feedback management

**Use for**:
- Organizing review sessions
- Collecting and categorizing feedback
- Tracking approvals
- Managing revision requests

**Example**: "Create a dailies playlist for all shots in SQ020 that are ready for review"

---

### Pipeline Agent (`pipeline-agent.md`)
**Expertise**: Technical support and pipeline development

**Use for**:
- Troubleshooting technical issues
- Developing pipeline tools
- Environment setup
- Integration support

**Example**: "My Maya environment variables aren't loading correctly, help me debug"

---

### Production Agent (`production-agent.md`)
**Expertise**: Production tracking and reporting

**Use for**:
- Tracking project progress
- Generating status reports
- Managing schedules
- Resource allocation

**Example**: "Generate a weekly status report for Project Alpha showing progress by department"

---

## How to Use Agents

### In Claude Code

When you need specialized help with a specific VFX task, you can invoke the appropriate agent:

```
# The agent will be loaded with specialized knowledge for that domain
# and will help you with domain-specific tasks
```

### Choosing the Right Agent

#### Software Development Tasks
| Task Type | Use This Agent |
|-----------|----------------|
| Technology research/comparison | Research Agent |
| Writing code/implementing features | Development Agent |
| Architecture/API design | Design Agent |
| Code review/quality check | Code Review Agent |
| Git workflow/branching | Git Workflow Agent |
| Writing tests/test strategy | Testing Agent |

#### VFX Production Tasks
| Task Type | Use This Agent |
|-----------|----------------|
| Asset publishing/versioning | Asset Agent |
| Shot setup/tracking | Shot Agent |
| Render submissions/issues | Render Agent |
| Reviews/feedback/approvals | Review Agent |
| Technical issues/tools | Pipeline Agent |
| Schedules/reports/tracking | Production Agent |

### When to Use Multiple Agents

Some workflows may benefit from multiple agents:

**Software Development Workflows:**
- **New Feature**: Research Agent → Design Agent → Development Agent → Testing Agent → Code Review Agent
- **Bug Fix**: Development Agent → Testing Agent → Code Review Agent
- **Architecture Change**: Research Agent → Design Agent → Code Review Agent

**VFX Production Workflows:**
- **Asset to Shot**: Asset Agent → Shot Agent
- **Shot to Render**: Shot Agent → Render Agent → Review Agent
- **Full Pipeline**: All agents in sequence

**Cross-Domain Workflows:**
- **Pipeline Tool Development**: Research Agent → Design Agent → Development Agent → Pipeline Agent
- **Automation Script**: Development Agent → Testing Agent → Pipeline Agent

## Customization

You can customize these agents for your studio by editing the markdown files:

1. Update naming conventions to match your studio
2. Add studio-specific tools and integrations
3. Include custom workflows and procedures
4. Add department-specific guidelines

## Best Practices

- Use the most specific agent for your task
- Provide context about your studio's pipeline when relevant
- Reference specific shots, assets, or sequences
- Include error messages or logs when troubleshooting
- Ask for clarification if the agent's suggestions don't fit your workflow

## Integration with Studio Pipeline

These agents are designed to work with common VFX tools:
- **Shotgun/Flow Production Tracking**
- **Deadline/Tractor** (render management)
- **RV/Syncsketch** (review tools)
- **Maya/Houdini/Nuke** (DCC applications)
- **Git/Perforce** (version control)

Customize the agent definitions to match your specific tool stack and workflows.
