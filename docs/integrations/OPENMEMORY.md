# OpenMemory MCP Integration Guide

**Integration Tier:** Tier 2 (High Value for Multi-Project CTOs)
**Best Paired With:** Sensei (Session Memory) + Context7 (Standards)
**Primary Use Cases:** Cross-project patterns, global preferences, team-wide standards, organizational knowledge

---

## 🎯 Why Sensei + OpenMemory

### The Memory Hierarchy

```
OpenMemory: GLOBAL memory across ALL projects
    ↓
Sensei Session Memory: PER-PROJECT memory
    ↓
Individual Conversation: TEMPORARY context
```

**OpenMemory provides:**
- Cross-project patterns and standards
- Personal preferences that apply everywhere
- Team-wide architectural decisions
- Organizational knowledge base

**Sensei Session Memory provides:**
- Project-specific decisions
- Active constraints for this codebase
- Session-level consultation history

**Together they enable:**
- Consistent patterns across all your projects
- Project-specific customization when needed
- Organizational learning that persists

---

## 🚀 Quick Start

### Prerequisites

```bash
# Ensure Sensei MCP is installed
uvx sensei-mcp

# Install OpenMemory MCP
npm install -g @openmemory/mcp-server
```

### Configuration

Add both servers to your MCP configuration:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    },
    "openmemory": {
      "command": "npx",
      "args": ["-y", "@openmemory/mcp-server"]
    }
  }
}
```

### Verify Setup

```python
# Check Sensei is available
get_session_summary(session_id="test")

# Check OpenMemory is available
mcp__openmemory__list-memories()
```

---

## 🔄 Multi-MCP Workflows

### Workflow 1: Cross-Project Pattern Enforcement

**Scenario:** Enforce "Always use PostgreSQL RLS for multi-tenancy" across all projects

**Multi-MCP Flow:**

```
User: "Remember: all my projects must use PostgreSQL RLS for multi-tenancy"

Step 1: OpenMemory Stores Global Rule
├─ add-memory(content="All projects MUST use PostgreSQL RLS for tenant isolation")
└─ This applies to EVERY project you work on

Step 2: Sensei Records Project-Specific Implementation
├─ record_decision(
│   category="architecture",
│   description="Using PostgreSQL RLS for multi-tenancy",
│   rationale="Global org standard + project-specific implementation"
│  )
└─ Project-specific decision references global standard

Later in ANY project:

Step 3: OpenMemory Retrieves Global Standard
├─ search-memories(query="multi-tenant")
├─ Returns: "All projects MUST use PostgreSQL RLS"
└─ Applies across all your codebases

Step 4: Sensei Enforces in Current Project
├─ check_consistency(proposed_change="Using shared database")
├─ Validates against BOTH global standard AND project decisions
└─ Warns if violating global pattern
```

**Result:** Consistent multi-tenancy approach across all projects

**Code Example:**
```python
# Store global preference (applies to ALL projects)
mcp__openmemory__add-memory(
    content="Always use PostgreSQL Row-Level Security (RLS) for multi-tenant applications. Never use schema-per-tenant or database-per-tenant."
)

# In project A
record_decision(
    category="architecture",
    description="Using PostgreSQL RLS for tenant isolation",
    rationale="Follows org-wide standard for multi-tenancy"
)

# In project B (weeks later)
search_result = mcp__openmemory__search-memories(query="multi-tenant")
# Returns: "Always use PostgreSQL RLS..."

# Sensei checks consistency
check_consistency(proposed_change="Using schema-per-tenant approach")
# Warns: "Violates global standard: PostgreSQL RLS required"
```

---

### Workflow 2: Personal Preferences + Project Context

**Scenario:** Global code style preferences with project-specific overrides

**Multi-MCP Flow:**

```
Global Preferences (OpenMemory):
├─ "I prefer functional programming over OOP"
├─ "Always use TypeScript strict mode"
├─ "Favor composition over inheritance"
└─ Applies to ALL projects

Project-Specific Context (Sensei):
├─ Session: "legacy-java-monolith"
├─ Constraint: "Must maintain OOP patterns for consistency"
└─ Overrides global OOP preference

Intelligent Synthesis:
1. OpenMemory: Retrieve global preferences
2. Sensei: Load project context and constraints
3. Claude: Synthesize appropriate for THIS project
   - Use TypeScript strict mode (global ✓)
   - Use OOP patterns (project override ✓)
   - Favor composition (global ✓, compatible with OOP)
```

**Result:** Smart context-aware recommendations

**Code Example:**
```python
# Store global preferences
mcp__openmemory__add-memory(
    content="My coding preferences: Prefer functional programming, always use TypeScript strict mode, favor composition over inheritance"
)

# In legacy Java project
get_session_context(session_id="legacy-java")
# Returns: active_constraints=["Maintain OOP patterns"]

# Claude synthesizes both:
# ✓ Use strict typing (from global)
# ✓ Use OOP (from project constraint)
# ✓ Use composition where possible (from global, compatible)
```

---

### Workflow 3: Team Knowledge Base

**Scenario:** Capture and reuse organizational architectural decisions

**Multi-MCP Flow:**

```
Team Lead: "Our team decided: microservices only when >5 engineers"

OpenMemory (Team Knowledge):
├─ add-memory(content="Team Standard: Only use microservices when team >5 engineers")
└─ Shared across all team members

Developer on Project A:
├─ search-memories(query="microservices")
├─ Finds: "Only use microservices when team >5 engineers"
├─ Current team: 3 engineers
└─ Recommendation: Use modular monolith

Developer on Project B:
├─ search-memories(query="microservices")
├─ Same standard applies
├─ Current team: 8 engineers
└─ Recommendation: Microservices appropriate

Sensei Integration:
├─ validate_against_standards(design_description="Proposing microservices for 3-person team")
├─ Cross-checks OpenMemory knowledge
└─ Warns: "Team standard suggests modular monolith for teams <5"
```

**Result:** Consistent team decisions without meetings

**Code Example:**
```python
# Team lead records decision
mcp__openmemory__add-memory(
    content="Team Architectural Standard: Only use microservices architecture when team size exceeds 5 engineers. For smaller teams, use modular monolith with clear bounded contexts."
)

# Developer weeks later
team_standard = mcp__openmemory__search-memories(query="microservices")

# Sensei validates against team standard
validate_against_standards(
    design_description="Proposing microservices for authentication service",
    focus_areas=["architecture"]
)
```

---

### Workflow 4: Learning from Past Projects

**Scenario:** Remember lessons learned and apply to new projects

**Multi-MCP Flow:**

```
After Project A (e-commerce):
OpenMemory: "Lesson: Stripe webhooks need idempotency keys and retry logic"

After Project B (SaaS billing):
OpenMemory: "Lesson: Always implement webhook signature verification"

New Project C (marketplace):
Developer: "Integrating Stripe webhooks"

OpenMemory Retrieval:
├─ search-memories(query="Stripe webhooks")
├─ Returns BOTH lessons from past projects
└─ Applies accumulated wisdom

Sensei Analysis:
├─ get_persona_content(persona_name="api-platform-engineer")
├─ Synthesizes with retrieved lessons
└─ Recommends: idempotency + signature verification

Result: New project benefits from past experience
```

**Code Example:**
```python
# After completing Project A
mcp__openmemory__add-memory(
    content="Lesson Learned: Stripe webhooks must use idempotency keys to handle retries. We had duplicate charges without this."
)

# After completing Project B
mcp__openmemory__add-memory(
    content="Lesson Learned: Always verify Stripe webhook signatures. We had a security incident from accepting unsigned webhooks."
)

# In new Project C
lessons = mcp__openmemory__search-memories(query="Stripe webhooks")
# Returns BOTH lessons

# Sensei applies lessons
get_engineering_guidance(
    query="How to implement Stripe webhooks securely?",
    mode="orchestrated"
)
# Includes both lessons in recommendation
```

---

## 🔧 OpenMemory MCP Tool Reference

### Memory Management

#### `add-memory(content)`
Store new memory in global knowledge base
```python
mcp__openmemory__add-memory(
    content="Always use environment variables for secrets, never hard-code"
)
```

#### `search-memories(query)`
Search through stored memories
```python
results = mcp__openmemory__search-memories(
    query="authentication best practices"
)
```

#### `list-memories()`
List all stored memories
```python
all_memories = mcp__openmemory__list-memories()
```

#### `delete-all-memories()`
Clear all memories (use with caution!)
```python
mcp__openmemory__delete-all-memories()
```

---

## 🎯 Integration Patterns

### Pattern 1: Global + Local Memory Hierarchy

**Use when:** You want consistent patterns across projects with project-specific flexibility

```python
# 1. Check global preferences
global_prefs = mcp__openmemory__search-memories(query="coding standards")

# 2. Load project context
project_context = get_session_context(session_id="current-project")

# 3. Synthesize appropriate recommendation
get_engineering_guidance(
    query="How should I structure this API?",
    mode="orchestrated"
)
# Claude uses BOTH global + project context
```

### Pattern 2: Store Once, Apply Everywhere

**Use when:** You learn something valuable that applies to all future work

```python
# After solving a tricky bug
mcp__openmemory__add-memory(
    content="PostgreSQL connection pooling: Always set max_connections conservatively. We had cascading failures with too many connections."
)

# Months later in different project
lessons = mcp__openmemory__search-memories(query="PostgreSQL connection")
# Automatically applies lesson learned
```

### Pattern 3: Team Knowledge Sharing

**Use when:** Multiple team members need consistent guidance

```python
# Team lead or senior engineer
mcp__openmemory__add-memory(
    content="Our API versioning strategy: Use URL versioning (/api/v1) not header versioning. Easier for clients and debugging."
)

# Any team member later
strategy = mcp__openmemory__search-memories(query="API versioning")
# Entire team gets consistent guidance
```

---

## ⚡ Best Practices

### 1. Use OpenMemory for Persistent Wisdom

**Good uses:**
- Architectural patterns that apply everywhere
- Lessons learned from production incidents
- Team standards and conventions
- Personal coding preferences
- Technology choices and rationale

**Bad uses:**
- Project-specific implementation details (use Sensei session)
- Temporary notes (use conversation context)
- Sensitive information (use proper secret management)

### 2. Write Clear, Actionable Memories

**Good:**
```python
mcp__openmemory__add-memory(
    content="Multi-tenancy: Always use PostgreSQL RLS with tenant_id column. Add indexes on (tenant_id, other_columns) for performance."
)
```

**Bad:**
```python
mcp__openmemory__add-memory(
    content="Something about tenants and databases"  # Too vague
)
```

### 3. Organize with Context

**Good:**
```python
mcp__openmemory__add-memory(
    content="Security: Rate limiting - Use exponential backoff starting at 1 req/sec after 5 failures. Reset after 1 hour of good behavior."
)

mcp__openmemory__add-memory(
    content="Performance: N+1 queries - Always use eager loading (SELECT with JOINs) for has-many relationships displayed in lists."
)
```

### 4. Combine with Sensei Validation

**Pattern:**
```python
# 1. Retrieve global knowledge
standards = mcp__openmemory__search-memories(query="security standards")

# 2. Apply to current project
validate_against_standards(
    code_snippet="<code>",
    focus_areas=["security"]
)

# 3. Record project-specific implementation
record_decision(
    category="security",
    description="Applied org security standards",
    rationale=f"Follows: {standards}"
)
```

---

## 🚨 Common Pitfalls

### ❌ Pitfall 1: Storing Project-Specific Details in Global Memory

**Problem:**
```python
# This is project-specific, not global!
mcp__openmemory__add-memory(
    content="UserRepository is in src/repositories/user.py"
)
```

**Solution:**
```python
# Use Sensei memory for project-specific
mcp__serena__write_memory(
    memory_file_name="repository-locations",
    content="UserRepository: src/repositories/user.py"
)

# Use OpenMemory for patterns
mcp__openmemory__add-memory(
    content="Repository Pattern: All data access should go through repository interfaces for testability"
)
```

### ❌ Pitfall 2: Conflicting Memories

**Problem:**
```python
# Memory 1
mcp__openmemory__add-memory(content="Always use OOP")

# Memory 2 (contradicts)
mcp__openmemory__add-memory(content="Always use functional programming")
```

**Solution:**
```python
# Be specific about context
mcp__openmemory__add-memory(
    content="For backend services: Prefer functional programming for business logic"
)

mcp__openmemory__add-memory(
    content="For UI components: Use React functional components with hooks"
)
```

### ❌ Pitfall 3: Not Updating Stale Memories

**Problem:**
Old memory says "Use JWT for all auth" but team switched to session tokens

**Solution:**
```python
# Delete outdated memory
mcp__openmemory__delete-all-memories()  # If necessary

# Add updated guidance
mcp__openmemory__add-memory(
    content="Authentication: Use session tokens (not JWT) for web apps. JWTs only for mobile/API clients."
)
```

---

## 📊 Memory Organization Strategy

### Recommended Categories

**1. Architectural Patterns**
```python
mcp__openmemory__add-memory(
    content="Architecture: Use CQRS for write-heavy domains. Separate read and write models."
)
```

**2. Security Standards**
```python
mcp__openmemory__add-memory(
    content="Security: All API endpoints must validate tenant_id before data access"
)
```

**3. Performance Guidelines**
```python
mcp__openmemory__add-memory(
    content="Performance: Cache expensive queries for 5 minutes. Invalidate on writes."
)
```

**4. Lessons Learned**
```python
mcp__openmemory__add-memory(
    content="Lesson: Database migrations must be backward compatible for zero-downtime deploys"
)
```

**5. Technology Decisions**
```python
mcp__openmemory__add-memory(
    content="Tech Stack: PostgreSQL for relational, Redis for cache, RabbitMQ for async"
)
```

---

## 🎓 Learning Path

### Beginner: Store Personal Preferences

**Week 1:** Store 3-5 coding preferences
```python
mcp__openmemory__add-memory(content="I prefer snake_case for Python")
mcp__openmemory__add-memory(content="I always use type hints in Python")
mcp__openmemory__add-memory(content="I prefer async/await over callbacks")
```

### Intermediate: Capture Lessons Learned

**Week 2-3:** After solving problems, store lessons
```python
# After debugging production issue
mcp__openmemory__add-memory(
    content="Lesson: Always set database connection timeouts. Default infinite timeout caused cascading failures."
)
```

### Advanced: Build Team Knowledge Base

**Month 2+:** Coordinate team-wide standards
```python
# Team architectural decisions
mcp__openmemory__add-memory(
    content="Team Standard: All services must expose /health and /metrics endpoints"
)
```

---

## 🔮 Advanced Use Cases

### Use Case 1: Multi-Project Consistency Audit

**Goal:** Ensure all projects follow organizational standards

```python
# 1. Define standard
mcp__openmemory__add-memory(
    content="All APIs must return RFC 7807 Problem Details for errors"
)

# 2. In each project, validate
standard = mcp__openmemory__search-memories(query="API error format")

# 3. Sensei checks compliance
validate_against_standards(
    code_snippet="<error handling code>",
    focus_areas=["api-design"]
)

# 4. Record per-project status
record_decision(
    category="compliance",
    description=f"Validated against: {standard}"
)
```

### Use Case 2: Personal Best Practices Library

**Goal:** Build your own engineering handbook

```python
# Store accumulated wisdom
mcp__openmemory__add-memory(
    content="Testing: Write integration tests for happy path, unit tests for edge cases"
)

mcp__openmemory__add-memory(
    content="Deployment: Always use blue-green deploys for user-facing services"
)

mcp__openmemory__add-memory(
    content="Monitoring: Alert on error rate >1%, latency p99 >500ms"
)

# Later retrieve relevant wisdom
wisdom = mcp__openmemory__search-memories(query="testing strategy")
```

---

## 📚 Related Documentation

- **Sensei Session Memory:** Project-specific decisions and context
- **Serena Memory:** Implementation details and code patterns
- **OpenMemory:** Cross-project wisdom and team standards

---

## 🎉 Success Stories

### Case Study: Multi-Project Multi-Tenancy Consistency

**Challenge:** 5 projects with different multi-tenancy implementations

**Solution:**
```python
# Defined org-wide standard
mcp__openmemory__add-memory(
    content="Multi-tenancy: PostgreSQL RLS with tenant_id column"
)

# Applied across all 5 projects
# Each project used Sensei to track implementation
# Result: 100% consistency, faster onboarding
```

**Impact:**
- Reduced multi-tenancy bugs by 80%
- New project setup time: 2 days → 4 hours
- Team-wide consistency achieved

---

**Made with 🥋 by Sensei + OpenMemory**

*Cross-project wisdom meets project-specific context.*
