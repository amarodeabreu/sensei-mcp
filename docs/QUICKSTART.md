# Sensei MCP - Quick Start Guide

*Get running in 5 minutes with practical examples*

## Installation (2 minutes)

See the [main README](../README.md) for installation instructions. Quick summary:

### Cursor (One-Click)
Click the install button in the README.

### Claude Code (CLI)
```bash
claude mcp add sensei -- uvx sensei-mcp
```

### Manual Install
```bash
pip install sensei-mcp
# Or for development:
pip install -e .
```

This will:
- ✅ Install FastMCP and Pydantic dependencies
- ✅ Create `~/.sensei/sessions/` directory on first use
- ✅ Make sensei-mcp command available

That's it! The MCP server is now active in your supported client.

## First Use (3 minutes)

### Scenario 1: API Security Review

You're reviewing a billing API endpoint for security issues.

**Your file:** `api/billing.py`

**What happens automatically:**

1. **Claude detects context:**
   - File: `api/billing.py`
   - Operation: REVIEW

2. **MCP server is called:**
   ```
   get_engineering_context(
     file_paths=["api/billing.py"],
     operation="REVIEW for security"
   )
   ```

3. **Relevant sections loaded:**
   - Section 0: Core Principles (always)
   - Section 1: Personality (always)
   - Section 4: APIs & Contracts
   - Section 6: Security & Privacy
   - Section 25: Multi-Tenancy
   - Section 36: Always-On Defaults
   - Section 39: Concurrency & Idempotency

4. **Claude now has YOUR standards** and generates review:

   ```
   Found 3 issues in api/billing.py:

   1. ⚠️ Missing tenant_id in WHERE clause (line 45)
      Violates: Section 25 (Multi-Tenancy) - Every query must filter by tenant

   2. ⚠️ No input validation on amount field (line 52)
      Violates: Section 6 (Security) - All external input is hostile until validated

   3. ⚠️ No idempotency key for charge endpoint (line 67)
      Violates: Section 39 (Idempotency) - Payment operations must be idempotent
   ```

**Without MCP server:**
- Generic security advice
- Might mention multi-tenancy, might not
- No specific section references

**With MCP server:**
- YOUR specific standards
- Cites exact sections
- Catches multi-tenancy (because it's always loaded for API + DB work)

### Scenario 2: Recording a Decision

You and Claude agree on an architectural pattern.

**You:** "Let's use async queues for all payment processing to handle retries gracefully."

**Claude:** "Good choice. Let me record this decision."

**Claude automatically calls:**
```python
record_decision(
  category="architecture",
  description="Use async queues for payment processing",
  rationale="Reliability and automatic retry handling",
  constraint="async-payment-queue",
  session_id="my-saas-project"
)
```

**Result:**
- ✅ Decision saved to `~/.sensei/sessions/my-saas-project.json`
- ✅ Future conversations remember this
- ✅ No re-litigating "why did we choose async queues?"

### Scenario 3: Validating Before Implementation

Before implementing a new feature, check against standards.

**You:** "I'm thinking of adding a new endpoint: POST /api/users/{id}/delete. Thoughts?"

**Claude calls:**
```python
validate_against_standards(
  design_description="POST /api/users/{id}/delete endpoint",
  focus_areas=["api-design", "security", "multi-tenant"]
)
```

**Claude responds:**
```
⚠️ Standards Validation Issues:

1. HTTP Method Mismatch (Section 4: APIs & Contracts)
   - DELETE operations should use DELETE, not POST
   - Suggestion: DELETE /api/users/{id}

2. Tenant Isolation (Section 25: Multi-Tenancy)
   - How is tenant_id enforced? User must belong to caller's tenant
   - Recommendation: Add tenant_id check in authorization

3. Soft vs Hard Delete (Section 5: Data & Persistence)
   - Is this soft delete (recommended for audit trail)?
   - Hard delete makes data recovery impossible

Recommendation: Use DELETE /api/users/{id} with tenant_id validation
and soft delete (deleted_at timestamp).
```

**This catches issues BEFORE you write code.**

## Common Usage Patterns

### Pattern 1: Starting a New Session

```
You: "Starting work on the payment service. We're using Postgres with
     row-level security for multi-tenant isolation, and deploying to GCP Cloud Run."

Claude: "Let me record these constraints."
```

Claude calls:
```python
record_decision(
  category="constraint",
  description="Postgres with RLS for multi-tenant isolation",
  constraint="postgres-rls",
  session_id="payment-service"
)

record_decision(
  category="constraint",
  description="Deploy to GCP Cloud Run",
  constraint="gcp-cloud-run",
  session_id="payment-service"
)
```

Now every future interaction in this session remembers these constraints.

### Pattern 2: Reviewing Session State

```
You: "What decisions have we made so far?"

Claude: "Let me check the session."
```

Claude calls:
```python
get_session_summary(session_id="payment-service")
```

Response:
```markdown
# Session Summary: payment-service

**Started:** 2025-01-20T09:00:00
**Last updated:** 2025-01-20T14:30:00

## Active Constraints
- postgres-rls
- gcp-cloud-run
- multi-tenant-by-default

## Agreed Patterns
- async-payment-queue
- hexagonal-architecture

## Decisions (5)

### dec_1 - 2025-01-20T09:15:00
**Category:** constraint
**Decision:** Postgres with RLS for multi-tenant isolation
**Rationale:** DB-level isolation, proven at scale

[... 4 more decisions ...]
```

### Pattern 3: Direct Section Query

```
You: "What does the rulebook say about concurrency and idempotency?"

Claude: "Let me get that specific section."
```

Claude calls:
```python
query_specific_standard(
  section_name="concurrency",
  session_id="payment-service"
)
```

Returns Section 39 (Concurrency, Idempotency & Workflows) directly.

### Pattern 4: Multi-Project Management

```
You: "Switch to my other project, the analytics service."

Claude: "Switching sessions."
```

Use different `session_id` for each project:
- `payment-service` - Has Postgres, GCP constraints
- `analytics-service` - Has BigQuery, batch processing constraints
- `auth-service` - Has Auth0 integration constraints

Each maintains its own decisions, constraints, and patterns.

## Quick Reference

### Available Tools

| Tool | Purpose | When Claude Calls It |
|------|---------|---------------------|
| `get_engineering_context()` | Load relevant standards | Start of any task |
| `record_decision()` | Save architectural choice | You agree on pattern/constraint |
| `validate_against_standards()` | Pre-implementation check | Before writing code |
| `get_session_summary()` | Review session state | You ask "what did we decide?" |
| `list_sessions()` | See all projects | You ask "what sessions exist?" |
| `query_specific_standard()` | Get specific section | You ask about specific standard |
| `check_consistency()` | Validate against decisions | Check if change conflicts with past |

### File Triggers

| File Pattern | Sections Loaded |
|--------------|----------------|
| `api/*.py` | APIs, Security, Multi-Tenancy, Idempotency |
| `*.sql` | Data Persistence, Multi-Tenancy, Security |
| `*.tf` | Cloud Platform, Cost, Observability |
| `*auth*` | Security, Multi-Tenancy, Always-On Defaults |
| `*test*` | Testing, Code Quality, Anti-Patterns |
| `*.md` | Documentation, Communication, Formatting |

### Operation Triggers

| Operation | Sections Loaded |
|-----------|----------------|
| CREATE | Core Philosophy, Prototype Mode, Quality Bar |
| REFACTOR | Code Quality, Mantras, Self-Consistency |
| DEBUG | Observability, Tests/Linters |
| DESIGN | Architecture, Task Shaping |
| REVIEW | Code Review, Anti-Patterns, Sanity Checklist |
| SECURITY | Security, Multi-Tenancy, AI Safety |

## Tips & Tricks

### Tip 1: Be Explicit About Context

**Better:**
```
"Review api/billing.py for security and multi-tenant isolation issues"
```

**Not as good:**
```
"Look at this code"
```

Explicit context triggers better section loading.

### Tip 2: Use Session IDs for Projects

**Do:**
```
session_id="saas-backend"
session_id="mobile-api"
session_id="data-pipeline"
```

**Don't:**
```
session_id="default"  # for everything
```

Separate sessions keep decisions isolated.

### Tip 3: Record Decisions Early

As soon as you agree on something architectural:
- "We're using Postgres" → record it
- "Multi-tenant by default" → record it
- "GCP Cloud Run" → record it

Future conversations will remember and enforce.

### Tip 4: Validate Early

Before implementing something non-trivial:
```
"Before I implement this, validate against our standards"
```

Catches issues when they're cheap to fix.

## Troubleshooting

### Server Not Loading

```bash
# Test the package installation
uvx sensei-mcp --help

# Or if installed with pip
python -c "import sensei_mcp; print('OK')"
```

### Tools Not Being Called

1. Check your MCP client configuration is correct
2. Restart your MCP client (Cursor, Claude Code, etc.)
3. Check `~/.sensei/sessions/` directory exists and is writable

### Run Tests

```bash
pytest tests/
```

Should show:
```
✅ All tests passed!
```

## Next Steps

- **Daily use:** Just use your MCP client normally - tools are called automatically
- **Advanced usage:** See [README.md](../README.md) for all 7 MCP tools
- **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- **Contributing:** See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup

---

**That's it!** Sensei is now actively injecting your engineering standards before Claude reasons about code.
