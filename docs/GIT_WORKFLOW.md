# Git Workflow Guide

This document describes the git branching and collaboration workflow for this repository.

## Branching Strategy

We follow **GitHub Flow**, a simple and effective branching model suitable for continuous delivery.

### Branch Structure

```
main (protected)
  ├── feature/add-new-agent
  ├── bugfix/fix-agent-loading
  ├── hotfix/critical-security-patch
  └── docs/update-readme
```

## Protected Branches

### Main Branch
- **Purpose**: Production-ready code
- **Protection**: Requires PR approval before merge
- **Rules**:
  - Require pull request reviews (minimum 1 approval)
  - Require status checks to pass (CI/CD)
  - Require branches to be up to date before merging
  - No direct pushes allowed
  - No force pushes allowed

## Branch Naming Conventions

### Format
```
<type>/<description>-<issue-number>
```

### Branch Types

| Type | Purpose | Example |
|------|---------|---------|
| `feature/` | New features or enhancements | `feature/add-deployment-agent-123` |
| `bugfix/` | Bug fixes | `bugfix/fix-agent-import-error-456` |
| `hotfix/` | Critical production fixes | `hotfix/security-patch-789` |
| `refactor/` | Code refactoring | `refactor/cleanup-agent-structure-234` |
| `docs/` | Documentation updates | `docs/update-workflow-guide-567` |
| `test/` | Test additions or improvements | `test/add-agent-tests-890` |
| `chore/` | Maintenance tasks | `chore/update-dependencies-345` |

### Examples
```bash
feature/add-testing-agent-101
bugfix/fix-markdown-parsing-202
hotfix/critical-security-fix-303
refactor/improve-agent-loading-404
docs/add-git-workflow-guide-505
test/add-integration-tests-606
chore/update-python-deps-707
```

## Workflow Steps

### 1. Create a Feature Branch

```bash
# Ensure you're on main and up to date
git checkout main
git pull origin main

# Create and checkout your feature branch
git checkout -b feature/your-feature-name-123
```

### 2. Make Changes and Commit

```bash
# Make your changes
# ...

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add new deployment agent

Implement deployment agent for CI/CD workflows with support
for multiple deployment targets and rollback capabilities.

Closes #123"
```

### 3. Keep Branch Updated

```bash
# Fetch latest changes
git fetch origin

# Rebase onto main (preferred for clean history)
git rebase origin/main

# Or merge if you prefer
# git merge origin/main
```

### 4. Push Branch to Remote

```bash
# First push
git push -u origin feature/your-feature-name-123

# Subsequent pushes
git push

# After rebase (use with caution)
git push --force-with-lease
```

### 5. Create Pull Request

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Fill out PR template:
   - Clear title following convention
   - Description of changes
   - Related issue numbers
   - Testing performed
   - Checklist items

### 6. Code Review Process

1. **Request reviews** from team members
2. **Address feedback**:
   ```bash
   # Make changes based on feedback
   git add .
   git commit -m "fix: address review comments"
   git push
   ```
3. **Resolve conversations** on GitHub
4. **Get approval** from required reviewers

### 7. Merge to Main

Once approved and CI passes:

1. **Ensure branch is up to date**:
   ```bash
   git fetch origin
   git rebase origin/main
   git push --force-with-lease
   ```

2. **Merge via GitHub**:
   - Use "Squash and merge" for clean history
   - Or "Rebase and merge" to preserve commits
   - Delete branch after merge

3. **Pull latest main locally**:
   ```bash
   git checkout main
   git pull origin main
   git branch -d feature/your-feature-name-123
   ```

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/).

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```
feat(agents): add deployment agent for CI/CD

Implement new deployment agent with support for:
- Multiple deployment targets
- Rollback capabilities
- Deployment health checks

Closes #123
```

```
fix(git-workflow): resolve branch naming validation

The branch naming regex was too strict and rejected
valid branch names. Updated to allow alphanumeric
characters and hyphens.

Fixes #456
```

```
docs(readme): update agent usage examples

Add more comprehensive examples for each agent type
and clarify the invocation process.
```

## Pull Request Guidelines

### PR Title
- Follow commit message format
- Include issue number
- Be clear and descriptive

```
feat: Add deployment agent (#123)
fix: Resolve agent loading error (#456)
docs: Update git workflow guide (#789)
```

### PR Description Template

Use this template when creating PRs:

```markdown
## Description
Brief summary of what this PR accomplishes

## Changes
- Specific change 1
- Specific change 2
- Specific change 3

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Test addition/update

## Testing Performed
Describe how you tested these changes:
- [ ] Manual testing steps
- [ ] Automated tests added/updated
- [ ] Tested on different environments

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged and published

## Related Issues
Closes #issue-number
Relates to #other-issue
```

### PR Size Guidelines

| Size | Lines Changed | Recommendation |
|------|---------------|----------------|
| **XS** | < 50 | Perfect! |
| **S** | 50-200 | Great size |
| **M** | 200-500 | Good, but consider splitting |
| **L** | 500-1000 | Too large, should split |
| **XL** | > 1000 | Definitely split into multiple PRs |

**Tips for large changes:**
- Split into logical, reviewable chunks
- Use draft PRs for work-in-progress
- Create meta-issue to track related PRs

## Merge Strategies

### Squash and Merge (Recommended)
- **When**: Most feature branches
- **Result**: Single commit in main
- **Pros**: Clean, linear history
- **Cons**: Loses intermediate commits

### Rebase and Merge
- **When**: Well-organized commit history
- **Result**: All commits replayed on main
- **Pros**: Preserves commit history
- **Cons**: Can clutter main if commits are messy

### Merge Commit
- **When**: Tracking branch history is important
- **Result**: Merge commit created
- **Pros**: Shows branch existence
- **Cons**: Non-linear history

## Handling Merge Conflicts

### Process

1. **Update your branch**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Git will pause on conflicts**:
   ```
   CONFLICT (content): Merge conflict in file.py
   ```

3. **Resolve conflicts in editor**:
   - Look for conflict markers: `<<<<<<<`, `=======`, `>>>>>>>`
   - Choose correct code or combine both
   - Remove conflict markers

4. **Mark as resolved**:
   ```bash
   git add file.py
   git rebase --continue
   ```

5. **Push updated branch**:
   ```bash
   git push --force-with-lease
   ```

### Conflict Resolution Tools
- VS Code built-in merge editor
- GitKraken, SourceTree
- `git mergetool` with configured editor

## Hotfix Process

For critical production issues:

1. **Create hotfix branch from main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-fix-123
   ```

2. **Make minimal fix**:
   - Only fix the critical issue
   - Don't include unrelated changes
   - Add test to prevent regression

3. **Fast-track review**:
   - Request immediate review
   - Prioritize approval
   - Ensure CI passes

4. **Merge and deploy immediately**:
   ```bash
   # After approval
   git checkout main
   git merge hotfix/critical-fix-123
   git push origin main
   git tag -a v1.2.1 -m "Hotfix: Critical security patch"
   git push origin v1.2.1
   ```

## Release Management

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features, backwards compatible (1.1.0)
- **PATCH**: Bug fixes, backwards compatible (1.0.1)

### Creating a Release

1. **Tag the release**:
   ```bash
   git checkout main
   git pull origin main
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin v1.2.0
   ```

2. **Create GitHub Release**:
   - Go to Releases → Create new release
   - Select tag
   - Generate release notes
   - Add highlights and breaking changes
   - Publish release

3. **Release Notes Template**:
   ```markdown
   ## 🎉 What's New
   - Feature 1
   - Feature 2

   ## 🐛 Bug Fixes
   - Fix 1
   - Fix 2

   ## ⚠️ Breaking Changes
   - Breaking change 1 (migration guide)

   ## 📚 Documentation
   - Doc update 1

   ## 🙏 Contributors
   Thanks to @contributor1, @contributor2
   ```

## Best Practices

### Do's ✅
- Keep branches short-lived (< 2 weeks)
- Commit early and often
- Write clear commit messages
- Keep PRs small and focused
- Respond to reviews promptly
- Delete merged branches
- Pull main regularly

### Don'ts ❌
- Don't commit directly to main
- Don't force push to shared branches
- Don't commit sensitive data (secrets, keys)
- Don't leave PRs open indefinitely
- Don't merge without review
- Don't include unrelated changes
- Don't push broken code

## Troubleshooting

### "My branch is behind main"
```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

### "I committed to wrong branch"
```bash
# Create correct branch
git checkout -b correct-branch

# Reset wrong branch
git checkout wrong-branch
git reset --hard origin/wrong-branch
```

### "I need to undo last commit"
```bash
# Undo but keep changes
git reset --soft HEAD~1

# Undo and discard changes
git reset --hard HEAD~1
```

### "I accidentally pushed sensitive data"
1. Remove from code immediately
2. Force push corrected version
3. Rotate any exposed secrets
4. Consider using `git-filter-repo` for history cleanup

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Documentation](https://git-scm.com/doc)

## Questions?

If you have questions about this workflow:
1. Check the Git Workflow Agent (`.claude/agents/git-workflow-agent.md`)
2. Ask in team chat
3. Create a discussion on GitHub
