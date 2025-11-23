# Sensei MCP CI/CD Integration Guide

**Version:** 0.5.0
**Last Updated:** 2025-01-23

This guide shows you how to integrate Sensei's multi-persona engineering guidance into your development workflow through CI/CD pipelines and pre-commit hooks.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [GitHub Actions Integration](#github-actions-integration)
3. [GitLab CI Integration](#gitlab-ci-integration)
4. [Pre-Commit Hooks](#pre-commit-hooks)
5. [Configuration](#configuration)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Sensei MCP can be integrated into your development workflow in three ways:

| Integration | Use Case | When to Use |
|-------------|----------|-------------|
| **Pre-Commit Hooks** | Local validation before commit | Every commit, instant feedback |
| **GitHub Actions** | PR reviews and architecture checks | Pull requests, main branch |
| **GitLab CI** | MR reviews and scheduled audits | Merge requests, scheduled jobs |

### What Gets Checked?

- **Architecture Consistency:** Changes align with documented decisions
- **Security Review:** Potential vulnerabilities and security anti-patterns
- **Cost Impact:** Infrastructure changes and cloud cost implications
- **Code Quality:** Maintainability, technical debt, patterns

---

## GitHub Actions Integration

### Quick Start

1. Copy workflow files to your repository:
   ```bash
   mkdir -p .github/workflows
   cp integrations/github-actions/sensei-pr-review.yml .github/workflows/
   cp integrations/github-actions/sensei-architecture-check.yml .github/workflows/
   ```

2. Commit and push:
   ```bash
   git add .github/workflows/
   git commit -m "Add Sensei MCP CI/CD integration"
   git push
   ```

3. Create a PR to see Sensei in action!

### Available Workflows

#### 1. PR Review Workflow (`sensei-pr-review.yml`)

**Triggers:** Pull requests to main/develop
**What it does:**
- Analyzes changed files for context (architecture, security, cost)
- Consults relevant personas based on file types
- Posts multi-persona review as PR comment

**Example Output:**
```markdown
## 🎭 Sensei Multi-Persona PR Review

### 🏗️ Architecture Review
**Personas consulted:** Pragmatic Architect, Snarky Senior Engineer

✅ Changes align with established architectural patterns
💡 Consider documenting this pattern for future reference

### 🔒 Security Review
**Personas consulted:** Security Sentinel, Compliance Guardian

⚠️  Minor: Consider adding rate limiting to new API endpoints
```

**Configuration:**
```yaml
# In .github/workflows/sensei-pr-review.yml
env:
  SENSEI_SESSION_ID: ${{ github.repository }}
  SENSEI_MODE: "orchestrated"  # or "quick" for faster reviews
```

#### 2. Architecture Check Workflow (`sensei-architecture-check.yml`)

**Triggers:** Push to any branch
**What it does:**
- Validates changes against session decisions
- Generates architecture health report
- Fails build on critical violations

**Configuration:**
```yaml
env:
  SENSEI_SESSION_ID: ${{ github.repository }}
  SENSEI_PROJECT_ROOT: ${{ github.workspace }}
```

### Customizing GitHub Actions

**Option 1: Specific Personas**
```yaml
- name: Security Review with Specific Personas
  run: |
    python -c "
    from sensei_mcp.server import get_engineering_guidance
    result = get_engineering_guidance(
        query='Review API security',
        specific_personas=['security-sentinel', 'api-platform-engineer']
    )
    print(result)
    "
```

**Option 2: Different Modes**
```yaml
# Quick mode for faster feedback
env:
  SENSEI_MODE: "quick"

# Crisis mode for production issues
env:
  SENSEI_MODE: "crisis"
```

**Option 3: Custom Triggers**
```yaml
on:
  pull_request:
    paths:
      - 'src/api/**'  # Only run on API changes
      - 'src/security/**'  # Or security changes
```

---

## GitLab CI Integration

### Quick Start

1. Copy configuration to your repository:
   ```bash
   cp integrations/gitlab-ci/.gitlab-ci.yml .gitlab-ci.yml
   ```

2. Commit and push:
   ```bash
   git add .gitlab-ci.yml
   git commit -m "Add Sensei MCP CI/CD integration"
   git push
   ```

3. Create an MR to trigger Sensei review!

### Pipeline Stages

The GitLab CI configuration includes 3 stages:

```
validate → review → report
```

#### Stage 1: Validate
- **consistency-check:** Validates against architectural decisions
- **architecture-analysis:** Analyzes change contexts

#### Stage 2: Review
- **security-review:** Security Sentinel + Compliance Guardian
- **cost-impact-review:** FinOps Optimizer analysis
- **code-quality-review:** Code quality assessment

#### Stage 3: Report
- **generate-sensei-report:** Comprehensive MR review report
- **weekly-architecture-audit:** Scheduled health checks

### Configuration Variables

Set these in GitLab CI/CD settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `SENSEI_VERSION` | Sensei MCP version | `0.5.0` |
| `SENSEI_SESSION_ID` | Project session ID | `$CI_PROJECT_PATH` |
| `SENSEI_MODE` | Review mode | `orchestrated` |
| `SENSEI_FAIL_ON_VIOLATIONS` | Fail on violations | `false` |

### Scheduled Audits

To enable weekly architecture audits:

1. Go to CI/CD → Schedules
2. Create new schedule:
   - Interval: Weekly (Monday 9am)
   - Target branch: main
   - Variables: None needed

The `weekly-architecture-audit` job will run automatically.

---

## Pre-Commit Hooks

Pre-commit hooks provide instant local feedback before you even commit code.

### Quick Start

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Copy configuration:
   ```bash
   cp integrations/pre-commit/.pre-commit-config.yaml .pre-commit-config.yaml
   cp -r integrations/pre-commit/*.py .
   ```

3. Install hooks:
   ```bash
   pre-commit install
   ```

4. Test on all files:
   ```bash
   pre-commit run --all-files
   ```

### Available Hooks

#### 1. Consistency Check

**What it checks:**
- Changes align with architectural decisions
- Database migrations exist for schema changes
- API specs updated for API changes
- Infrastructure changes documented

**Example Output:**
```
🎭 Sensei Consistency Check
============================================================
📊 Analyzed 5 staged files

⚠️  Warnings:
  • API changes detected but no OpenAPI spec update found

💡 Tip: Update your changes to align with architectural decisions
============================================================
```

#### 2. Security Review

**What it checks:**
- Hardcoded secrets (passwords, API keys, tokens)
- SQL injection vulnerabilities
- Use of dangerous functions (eval, pickle)
- Weak cryptography (MD5, SHA1)
- Unsafe deserialization

**Example Output:**
```
🎭 Sensei Security Review
🔒 Persona: Security Sentinel
======================================================================
🔴 HIGH SEVERITY:
  • src/api/auth.py:45
    Potential hardcoded secret detected
    Code: API_KEY = "sk_live_abc123def456"

💡 Recommendations from Security Sentinel:
  • Use environment variables for secrets
  • Use parameterized queries to prevent SQL injection
======================================================================
```

**Exit Code:** Fails on HIGH severity issues

#### 3. Cost Impact Check

**What it checks:**
- EC2 instances
- RDS databases
- Lambda functions
- S3 buckets
- Load balancers
- NAT gateways

**Example Output:**
```
🎭 Sensei Cost Impact Analysis
💰 Persona: FinOps Optimizer
======================================================================
📊 Found 3 cost-impacting resource(s):

🔴 HIGH COST IMPACT:
  • Database: rds_instances
    File: terraform/main.tf

💵 Estimated Monthly Cost Impact:
   $150 - $1,000 USD/month

💡 Recommendations from FinOps Optimizer:
  • Consider Reserved Instances for long-running resources
  • Use Spot Instances where possible
======================================================================
```

**Exit Code:** Warning only (doesn't fail commit)

### Customizing Pre-Commit Hooks

**Option 1: Skip Specific Hooks**
```bash
SKIP=sensei-security-review git commit -m "message"
```

**Option 2: Bypass All Hooks** (not recommended)
```bash
git commit --no-verify -m "message"
```

**Option 3: Configure .sensei.yml**

Create `.sensei.yml` in your repo root:
```yaml
session_id: "my-awesome-project"
mode: "quick"  # Faster feedback
fail_on_violations: true  # Strict mode

personas:
  security:
    - security-sentinel
    - compliance-guardian
  architecture:
    - pragmatic-architect
    - snarky-senior-engineer
  cost:
    - finops-optimizer
```

---

## Configuration

### Session ID

The session ID links your CI/CD runs to a persistent Sensei session with architectural decisions and patterns.

**GitHub Actions:**
```yaml
env:
  SENSEI_SESSION_ID: ${{ github.repository }}  # e.g., "myorg/myrepo"
```

**GitLab CI:**
```yaml
variables:
  SENSEI_SESSION_ID: "$CI_PROJECT_PATH"  # e.g., "myorg/myrepo"
```

**Pre-Commit:**
```yaml
# .sensei.yml
session_id: "my-project"
```

### Persona Selection

**Auto-Selection (Recommended):**
Let Sensei choose personas based on context:
```yaml
env:
  SENSEI_MODE: "orchestrated"
```

**Specific Personas:**
Override for specialized reviews:
```python
get_engineering_guidance(
    query="Review this database migration",
    specific_personas=["data-engineer", "pragmatic-architect"]
)
```

**Crisis Mode:**
For production incidents:
```yaml
env:
  SENSEI_MODE: "crisis"  # Activates Incident Commander, SRE, Executive Liaison
```

---

## Best Practices

### 1. Start with PR Reviews

Begin with GitHub Actions/GitLab CI on pull requests before adding pre-commit hooks. This allows your team to get familiar with Sensei's feedback without blocking local development.

**Recommended rollout:**
1. Week 1: Enable PR review workflow (informational only)
2. Week 2: Add architecture check workflow
3. Week 3: Enable pre-commit hooks for security
4. Week 4: Enable all pre-commit hooks

### 2. Use Session Consistency

Maintain a consistent session ID across all integrations:
```yaml
# All environments use same session
SENSEI_SESSION_ID: "myorg-myrepo"
```

This ensures:
- Architectural decisions are consistent
- Pattern recognition improves over time
- Recommendations become more relevant

### 3. Configure Failure Policies

**Development Branches:** Warning only
```yaml
allow_failure: true  # Don't block on warnings
```

**Production/Main Branch:** Strict validation
```yaml
allow_failure: false  # Block on violations
```

**Pre-Commit:** Fail on security, warn on cost
```python
# sensei_security_review.py
return 1 if high_severity_issues else 0  # Fail on HIGH

# sensei_cost_check.py
return 0  # Always warn, never fail
```

### 4. Cache Sensei Installation

**GitHub Actions:**
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'
```

**GitLab CI:**
```yaml
cache:
  paths:
    - .cache/pip
    - venv/
```

This reduces pipeline time by 50-70%.

### 5. Scheduled Audits

Run weekly architecture health audits:

**GitHub Actions:**
```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9am
```

**GitLab CI:**
Use CI/CD Schedules (Settings → CI/CD → Schedules)

### 6. Gradual Rollout

**Phase 1: Observe (2 weeks)**
- Enable reviews, don't fail builds
- Collect feedback from team
- Adjust persona selection

**Phase 2: Warn (2 weeks)**
- Fail on critical security issues only
- Warn on architecture violations
- Refine rules based on false positives

**Phase 3: Enforce (ongoing)**
- Fail on all violations
- Team is familiar with Sensei
- Rules are well-tuned

---

## Troubleshooting

### Pre-Commit Hook Issues

**Problem:** Hook fails with "command not found: python"

**Solution:** Specify Python path in `.pre-commit-config.yaml`:
```yaml
- id: sensei-consistency-check
  entry: /usr/bin/python3 integrations/pre-commit/sensei_consistency_check.py
```

**Problem:** Hook is too slow (>10 seconds)

**Solution:** Use quick mode:
```yaml
# .sensei.yml
mode: "quick"  # Single persona (Snarky Senior Engineer)
```

### GitHub Actions Issues

**Problem:** Workflow fails with "sensei-mcp not found"

**Solution:** Ensure pip install step runs:
```yaml
- name: Install Sensei MCP
  run: pip install sensei-mcp
```

**Problem:** PR comments not posting

**Solution:** Check permissions:
```yaml
permissions:
  contents: read
  pull-requests: write  # Required for comments
```

### GitLab CI Issues

**Problem:** Pipeline fails with import error

**Solution:** Activate venv before running Python:
```yaml
script:
  - source venv/bin/activate
  - python script.py
```

**Problem:** Artifacts not uploading

**Solution:** Ensure paths exist:
```yaml
artifacts:
  paths:
    - sensei_report.md  # File must be created in script
  when: always  # Upload even on failure
```

### General Issues

**Problem:** Reviews are not relevant to changes

**Solution:** Use context detection or specific personas:
```python
# Let Sensei detect context
mode="orchestrated"

# Or specify explicitly
specific_personas=["security-sentinel", "api-platform-engineer"]
```

**Problem:** False positives in security review

**Solution:** Update security patterns in `sensei_security_review.py`:
```python
# Add exceptions for your codebase
if 'test' in current_file.lower():
    continue  # Skip test files
```

---

## Examples

### Example 1: Simple GitHub PR Review

```yaml
name: Sensei Review
on: pull_request

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install sensei-mcp
      - run: python << 'EOF'
        from sensei_mcp.server import get_engineering_guidance
        result = get_engineering_guidance(
            query="Review this PR for architecture and security",
            mode="orchestrated"
        )
        print(result)
        EOF
```

### Example 2: Minimal Pre-Commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: sensei-security
        name: Sensei Security Check
        entry: python integrations/pre-commit/sensei_security_review.py
        language: system
        files: \.(py|js|ts)$
```

### Example 3: GitLab MR Review

```yaml
sensei-review:
  image: python:3.11
  script:
    - pip install sensei-mcp
    - python << 'EOF'
      from sensei_mcp.server import get_engineering_guidance
      result = get_engineering_guidance(
          query="Review MR !$CI_MERGE_REQUEST_IID",
          mode="orchestrated"
      )
      print(result)
      EOF
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

---

## Next Steps

1. **Choose your integration:** Start with PR/MR reviews for least friction
2. **Configure session:** Set `SENSEI_SESSION_ID` to track decisions
3. **Test on sample PR:** Create a test PR to see Sensei in action
4. **Tune and iterate:** Adjust personas and thresholds based on feedback
5. **Roll out gradually:** Enable more checks as team adopts

---

## Resources

- **Integration Templates:** `integrations/` directory
- **Sensei Documentation:** See main README.md
- **MCP Tools Reference:** [tool documentation]
- **Support:** GitHub Issues

---

**Made with 🎭 by the Sensei Multi-Persona Team**
