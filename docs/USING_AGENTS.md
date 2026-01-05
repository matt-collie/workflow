# Using Claude Code Agents - Practical Guide

This guide shows you how to actually use the Claude Code agents in your daily workflow.

## How Agents Work

Claude Code agents are **specialized AI assistants** that provide expert help for specific domains. When you invoke an agent, it loads that agent's knowledge and expertise to help you with domain-specific tasks.

## How to Invoke an Agent

In Claude Code, you can invoke agents by referencing them in your conversation. The agent's markdown file contains specialized instructions that guide Claude's responses.

### Method 1: Direct Mention (Recommended)
Simply ask Claude Code to use a specific agent:

```
"Use the Development Agent to help me implement user authentication"
"Switch to the Git Workflow Agent to help me create a PR"
"I need the Code Review Agent to review this file"
```

### Method 2: Context-Based
Claude Code can automatically suggest the right agent based on your task:

```
"Help me design a REST API for user management"
→ Claude may engage the Design Agent

"Why is my test failing?"
→ Claude may engage the Testing Agent
```

## Practical Examples

### Example 1: Adding a New Feature

**Scenario**: You need to add user authentication to your app.

**Step 1: Research** (Research Agent)
```
You: "Use the Research Agent. I need to add authentication to our Node.js API.
     Compare JWT vs session-based auth and recommend which to use for our use case."

Agent: [Provides comparison of JWT vs sessions, pros/cons, recommendations]
```

**Step 2: Design** (Design Agent)
```
You: "Use the Design Agent. Design the authentication flow and API endpoints
     for JWT-based authentication with refresh tokens."

Agent: [Provides architecture diagram, API endpoint specs, data models]
```

**Step 3: Implement** (Development Agent)
```
You: "Use the Development Agent. Help me implement the /login endpoint with
     JWT token generation."

Agent: [Provides code implementation, error handling, best practices]
```

**Step 4: Test** (Testing Agent)
```
You: "Use the Testing Agent. Write unit tests for the authentication service."

Agent: [Provides test cases, test code, coverage guidance]
```

**Step 5: Review** (Code Review Agent)
```
You: "Use the Code Review Agent. Review the authentication implementation for
     security issues and best practices."

Agent: [Provides security review, identifies issues, suggests improvements]
```

**Step 6: Create PR** (Git Workflow Agent)
```
You: "Use the Git Workflow Agent. Help me create a proper PR for this feature."

Agent: [Provides branch naming, commit message format, PR description template]
```

### Example 2: Fixing a Bug

**Scenario**: Production bug - users can't upload files larger than 1MB.

**Step 1: Debug** (Development Agent)
```
You: "Use the Development Agent. Help me debug this file upload issue.
     Here's the error: [paste error]"

Agent: [Analyzes error, suggests debugging steps, identifies potential causes]
```

**Step 2: Fix** (Development Agent)
```
You: "Help me fix the file size limit configuration."

Agent: [Provides fix, explains the solution, adds proper error handling]
```

**Step 3: Test** (Testing Agent)
```
You: "Use the Testing Agent. Write a test to prevent this regression."

Agent: [Creates integration test for file uploads with various sizes]
```

**Step 4: Hotfix PR** (Git Workflow Agent)
```
You: "Use the Git Workflow Agent. This is a critical bug. Help me create a hotfix."

Agent: [Guides through hotfix branch creation, expedited PR process]
```

### Example 3: VFX Asset Publishing

**Scenario**: Publishing a character asset to the library.

**Step 1: Validate** (Asset Agent)
```
You: "Use the Asset Agent. I need to publish character_hero_v003.ma.
     Help me validate it follows our naming conventions."

Agent: [Checks naming, validates structure, identifies any issues]
```

**Step 2: Publish** (Asset Agent)
```
You: "Guide me through the publishing process."

Agent: [Provides step-by-step publishing workflow, checks dependencies]
```

**Step 3: Track** (Production Agent)
```
You: "Use the Production Agent. Update the tracking system that hero character is published."

Agent: [Guides updating production database, status updates]
```

### Example 4: Code Review

**Scenario**: Reviewing a teammate's pull request.

```
You: "Use the Code Review Agent. Review this PR: [paste code or file path]

Check for:
- Security vulnerabilities
- Code quality issues
- Performance problems
- Test coverage"

Agent: [Provides systematic review with categorized feedback:
- 🔴 Critical issues
- 🟡 Important improvements
- 🔵 Suggestions
- 💡 Questions]
```

## Agent Chaining

You can work with multiple agents in sequence for complex workflows:

```
You: "I need to add a caching layer to our API.

1. First, use the Research Agent to compare Redis vs Memcached
2. Then use the Design Agent to design the caching architecture
3. Then use the Development Agent to help implement it
4. Finally use the Testing Agent to help write tests"

[Work through each step sequentially]
```

## Tips for Effective Agent Use

### 1. Be Specific
❌ Bad: "Help me with git"
✅ Good: "Use the Git Workflow Agent. Help me resolve this merge conflict in the main.py file"

### 2. Provide Context
❌ Bad: "Review my code"
✅ Good: "Use the Code Review Agent. Review this authentication middleware for security issues. We're using JWT tokens and this runs on every API request."

### 3. State Your Goal
❌ Bad: "What database should I use?"
✅ Good: "Use the Research Agent. Compare PostgreSQL vs MongoDB for an e-commerce application with high write volume and complex relationships."

### 4. Reference Files
When working with code in your repository:
```
You: "Use the Development Agent. Help me refactor the UserService class in
     src/services/user.service.ts to use dependency injection."
```

### 5. Ask for Specific Deliverables
```
You: "Use the Design Agent. Design a REST API for inventory management.
     Provide:
     - API endpoint specifications
     - Database schema
     - Sequence diagrams for key flows"
```

## Quick Reference: Which Agent When?

| I need to... | Use this Agent |
|--------------|---------------|
| Compare technologies or libraries | Research Agent |
| Write or fix code | Development Agent |
| Design architecture or APIs | Design Agent |
| Review code or PRs | Code Review Agent |
| Handle git/branches/PRs | Git Workflow Agent |
| Write or debug tests | Testing Agent |
| Publish VFX assets | Asset Agent |
| Set up shots | Shot Agent |
| Submit/debug renders | Render Agent |
| Coordinate reviews | Review Agent |
| Fix pipeline/tool issues | Pipeline Agent |
| Track production progress | Production Agent |

## Common Workflows

### Daily Development
```bash
Morning:
- Git Workflow Agent: Update branch from main
- Development Agent: Start implementing feature

Afternoon:
- Testing Agent: Write tests for new code
- Code Review Agent: Self-review before pushing

Evening:
- Git Workflow Agent: Create PR
- Code Review Agent: Review teammate's PR
```

### Sprint Planning
```bash
- Research Agent: Evaluate new technologies
- Design Agent: Design upcoming features
- Production Agent: Track sprint progress
```

### Bug Fixing
```bash
- Development Agent: Debug and fix
- Testing Agent: Add regression tests
- Code Review Agent: Validate fix
- Git Workflow Agent: Create hotfix PR
```

## Advanced Usage

### Switching Between Agents
You can switch agents mid-conversation:
```
You: "Use the Design Agent to design this API."
[Agent provides design]

You: "Now switch to the Development Agent and implement the first endpoint."
[Agent helps with implementation]

You: "Switch to the Testing Agent and write tests for it."
[Agent helps with tests]
```

### Combining Agents
For complex tasks, combine multiple agents:
```
You: "I need to add real-time notifications to our app.

Research Agent: Compare WebSockets vs Server-Sent Events
Design Agent: Design the notification architecture
Development Agent: Help implement the WebSocket server
Testing Agent: Write integration tests
Code Review Agent: Review for security and scalability"
```

## Getting Help

If you're unsure which agent to use:
```
You: "I need to [describe your task]. Which agent should I use?"
```

Claude will recommend the most appropriate agent for your needs.

## Next Steps

1. Try invoking an agent for your current task
2. Experiment with agent chaining for complex workflows
3. Customize agent definitions in `.claude/agents/` for your team's needs
4. Share successful workflows with your team

Remember: Agents are here to help you work more efficiently. Don't hesitate to ask for their assistance!
