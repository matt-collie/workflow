# Agent-Driven Development Workflow

This document describes how to use Claude Code agents to automate the entire development workflow, from feature implementation to pull request creation.

## Overview

The agent-driven workflow enables autonomous development where:
1. Agents design, implement, test, and review code
2. Agents automatically create pull requests
3. You receive notifications when PRs are ready
4. (Future) Agents can review and approve simple PRs

## Current Workflow

### Phase 1: Development (Automated)

Agents handle the entire development process:

```
Git Workflow Agent → Create feature branch
         ↓
Design Agent → Design the feature
         ↓
Development Agent → Implement the code
         ↓
Testing Agent → Write tests
         ↓
Code Review Agent → Self-review
         ↓
Git Workflow Agent → Commit and push
         ↓
[Automated PR Creation] → Create pull request
         ↓
[You] → Review and merge
```

### Phase 2: Review (Manual - for now)

You review and merge PRs through GitHub's interface.

### Phase 3: Future - Automated Review

Simple, low-risk PRs can be reviewed by the Code Review Agent automatically.

## Setup

### 1. GitHub Personal Access Token

For agents to create PRs automatically, you need a GitHub token:

**Create Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a descriptive name: `Claude Code Agents`
4. Select scopes:
   - `repo` (full control of private repositories)
   - `workflow` (if updating GitHub Actions)
5. Click "Generate token"
6. Copy the token immediately (you won't see it again!)

**Set Environment Variable:**

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Or for a single session:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### 2. Repository Configuration

Ensure your repository name is correct in scripts:
```bash
# Update if needed
REPO_OWNER="matt-collie"
REPO_NAME="workflow"
```

### 3. Test PR Creation

Test the automated PR script:
```bash
python scripts/create_pr.py \
  "${REPO_OWNER}/${REPO_NAME}" \
  --title "test: Automated PR creation" \
  --body "Testing automated PR workflow" \
  --head "test-branch" \
  --base "main"
```

## Agent Usage

### Requesting a Feature with Automated PR

**Your request:**
```
Create a feature to [description]. Use the full agent workflow and
automatically create a PR when done.
```

**What happens:**
1. **Git Workflow Agent** creates feature branch
2. **Design Agent** (optional) designs the solution
3. **Development Agent** implements the code
4. **Testing Agent** writes tests
5. **Code Review Agent** reviews the implementation
6. **Git Workflow Agent** commits and pushes
7. **Automated PR creation** using `scripts/create_pr.py`
8. **You receive notification** via GitHub

### Example Session

```
You: "Add a script to validate agent markdown files. Use the complete
      workflow and create a PR automatically."

[Agents work through Design → Develop → Test → Review]

Agent: "✓ Feature complete. Creating pull request..."

[PR created automatically]

Agent: "Pull request created: #42
        URL: https://github.com/matt-collie/workflow/pull/42

        You'll receive a GitHub notification. Please review when ready."
```

## Notifications

### GitHub Notifications

You'll receive notifications for:
- New pull requests created by agents
- PR status checks (if CI/CD is configured)
- Comments or reviews needed

**Configure notifications:**
- GitHub → Settings → Notifications
- Enable: "Participating" and "Watching"
- Choose delivery method: Email, Web, Mobile

### Email Notifications

GitHub sends emails for:
- New PRs
- PR comments
- Review requests
- Merged PRs

### Slack/Discord Integration (Optional)

Set up webhooks to get notifications in chat:

**Slack:**
1. Create incoming webhook in Slack
2. Add to repository: Settings → Webhooks
3. Select events: Pull requests, Pull request reviews

**Discord:**
1. Create webhook in Discord channel
2. Use GitHub Discord webhook integration
3. Configure for PR events

## Pull Request Templates

### Standard PR Template

Location: `.github/pull_request_template.md`

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation

## Agent Workflow
- [ ] Design Agent
- [ ] Development Agent
- [ ] Testing Agent
- [ ] Code Review Agent

## Testing
- [ ] Tests added
- [ ] Tests passing
- [ ] Manual testing done

## Checklist
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No breaking changes
```

## Review Process

### Manual Review (Current)

1. **Notification received** → GitHub email/notification
2. **Open PR** → Click link in notification
3. **Review changes** → Check files, tests, docs
4. **Approve or request changes** → Use GitHub review tools
5. **Merge** → Squash and merge (recommended)

### Review Criteria

**Auto-approve candidates** (future):
- Documentation updates
- Test additions
- Minor bug fixes
- Dependency updates

**Always manual review**:
- Breaking changes
- Security-related changes
- Major refactors
- New features with complexity

## Future: Automated Reviews

### Phase 1: Simple PRs

Code Review Agent can auto-approve:
- Documentation-only changes
- Adding tests
- Fixing typos
- Updating comments

### Phase 2: Complex PRs

Code Review Agent reviews and comments, but requires your approval:
- New features
- Bug fixes
- Refactoring

### Phase 3: Full Automation

For trusted, low-risk changes:
- Agent reviews
- Agent approves
- Auto-merge if checks pass
- You receive summary notification

## PR Creation Script

### Basic Usage

```bash
# Create PR with title and body
python scripts/create_pr.py \
  matt-collie/workflow \
  --title "feat: Add new feature" \
  --body "Feature description" \
  --head "feature-branch" \
  --base "main"

# Create PR with body from file
python scripts/create_pr.py \
  matt-collie/workflow \
  --title "feat: Add new feature" \
  --body-file /tmp/pr_description.md \
  --head "feature-branch"
```

### From Agents

Agents use the script like this:

```python
import subprocess

# Prepare PR details
pr_body = """
## Description
Feature implementation

## Changes
- Added X
- Updated Y
"""

# Save to temp file
with open("/tmp/pr_body.md", "w") as f:
    f.write(pr_body)

# Create PR
result = subprocess.run([
    "python", "scripts/create_pr.py",
    "matt-collie/workflow",
    "--title", "feat: Implement feature X",
    "--body-file", "/tmp/pr_body.md",
    "--head", branch_name,
    "--base", "main"
], capture_output=True, text=True)

if result.returncode == 0:
    print("PR created successfully!")
    print(result.stdout)
else:
    print(f"Failed to create PR: {result.stderr}")
```

## Security Considerations

### GitHub Token Security

**Do:**
- ✓ Use environment variables
- ✓ Rotate tokens periodically
- ✓ Use minimum required scopes
- ✓ Keep token secret

**Don't:**
- ✗ Commit tokens to git
- ✗ Share tokens
- ✗ Use tokens with excessive permissions
- ✗ Store in plaintext files

### PR Review Security

**Always manually review:**
- Changes to authentication/authorization
- Security-related code
- API changes
- Database migrations
- Dependency updates

## Troubleshooting

### Token Issues

**Error: "Bad credentials"**
- Verify `GITHUB_TOKEN` is set correctly
- Check token hasn't expired
- Ensure token has `repo` scope

**Error: "Resource not accessible by integration"**
- Token needs additional scopes
- Check repository permissions

### PR Creation Issues

**Error: "Validation Failed"**
- Branch must exist on remote
- Base branch must exist
- No existing PR with same head/base

**Error: "Not Found"**
- Check repository name format: `owner/repo`
- Verify you have access to the repository

## Best Practices

### For Agents

1. **Always create feature branches** from main
2. **Use conventional commit messages**
3. **Include comprehensive PR descriptions**
4. **Self-review before creating PR**
5. **Run tests before pushing**

### For Reviewers

1. **Review promptly** to keep development moving
2. **Provide constructive feedback**
3. **Approve simple changes quickly**
4. **Request changes for issues**
5. **Merge using "Squash and merge"**

## Metrics

Track agent-driven development effectiveness:

- **Time to PR**: Branch creation → PR created
- **Review time**: PR created → Merged
- **PR quality**: Changes requested ratio
- **Auto-approve rate**: Simple PRs auto-approved
- **Test coverage**: Coverage per PR

## Examples

### Example 1: Documentation Update

```
You: "Update the README to include the new script. Create PR automatically."

[Development Agent updates README]
[Git Workflow Agent creates PR]

Result: PR #43 created, auto-approved (docs-only), merged
```

### Example 2: New Feature

```
You: "Add email validation to user registration. Full workflow with PR."

[Complete agent workflow]
[PR created with comprehensive description]

Result: PR #44 created, you review, approve, merge
```

### Example 3: Bug Fix

```
You: "Fix the JSON output bug in list_agents.py. Create PR."

[Development Agent fixes bug]
[Testing Agent adds regression test]
[Code Review Agent verifies fix]
[PR created]

Result: PR #45 created, you review security implications, merge
```

## Integration with CI/CD

Future: PRs can trigger:
- Automated tests
- Code quality checks
- Security scans
- Deployment to staging

Agents wait for checks to pass before requesting review.

## Conclusion

Agent-driven development with automated PR creation streamlines the workflow:
- Agents handle routine development tasks
- You focus on architectural decisions and reviews
- Quality is maintained through automated testing and review
- Development velocity increases

As trust builds, more PRs can be auto-approved, further automating the workflow.
