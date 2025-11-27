# Sensei MCP 🥋

![PyPI](https://img.shields.io/pypi/v/sensei-mcp)

![Python](https://img.shields.io/badge/python-3.10+-blue)

![License](https://img.shields.io/badge/license-Apache%202.0-blue)

> Multi-persona engineering mentor with 64 specialized AI personas orchestrating collaborative guidance

**🚀 NEW in v0.9.0:** Complete Third-Party MCP Integration Suite - Multi-MCP orchestration with 6 integrated MCP servers (Serena, OpenMemory, GitHub, Context7, Tavily, Playwright), 13 workflow templates, and 10 executable demos! Tactical code execution (Sensei → Serena), cross-project memory (OpenMemory), and GitHub-integrated workflows (PR reviews, commit analysis, issue triage). See [Integration Guides](docs/integrations/README.md) for complete workflows.

**NEW in v0.8.0:** Complete Persona Portfolio (64 Personas) - All personas from claude-skills repository now integrated! Added 17 new personas including complete Design & UX team (6), Strategic Expansion skills (5), Critical Infrastructure gaps (5), and Meta-Navigation personas (2).

**🌟 MCP Ecosystem Integration:** Sensei MCP is designed to work seamlessly with other MCP servers (Context7, Tavily, Playwright, GitHub, OpenMemory, Sequential Thinking) to create a comprehensive CTO co-pilot. See [MCP Integration Architecture](docs/MCP_INTEGRATION_ARCHITECTURE.md) for the complete vision.

**v0.6.0:** Granular Persona Content Access (Option B Architecture) - Fixed orchestrator placeholder bug with new content-provider architecture. MCP now provides persona SKILL.md content for Claude to analyze, instead of trying to perform analysis itself. 4 new granular tools for persona discovery, content access, session context, and consultation recording.

**v0.5.0:** Enhanced Discovery, CI/CD Integration, Team Collaboration & Database Expertise - Interactive demo mode, GitHub Actions/GitLab CI templates, session merging for teams.

**v0.4.0:** Analytics & Team Collaboration - Track persona effectiveness, export session summaries as ADRs, and share engineering decisions with your team.

Sensei transforms your engineering standards from passive documentation into an active mentor that injects relevant guidelines **before** Claude reasons, maintaining session memory of architectural decisions.

### 🤝 Human-LLM Partnership (The Killer Insight)

**Human provides:** Domain expertise, judgment, context, business constraints, strategic direction

**LLM provides:** Synthesis across 64 expert personas, pattern matching against 32,000 lines of wisdom, consistency checking, real-time intelligence

**Together:** CTO-level decisions at code-writing speed with multi-perspective analysis and no weak links

---

## 🚀 Quick Install

### One-Click Install

#### Cursor

[`<img src="https://cursor.com/deeplink/mcp-install-dark.svg" alt="Install in Cursor">`](https://cursor.com/en/install-mcp?name=Sensei&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyJzZW5zZWktbWNwIl19)

### CLI Install

#### Claude Code

```bash
claude mcp add sensei -- uvx sensei-mcp
```

### Manual Configuration

<details>
<summary><b>📱 Claude Desktop</b></summary>

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart Claude Desktop after saving.

</details>

<details>
<summary><b>🌊 Windsurf</b></summary>

Add to your Windsurf MCP config:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart Windsurf after saving.

</details>

<details>
<summary><b>🔧 Cline (VS Code)</b></summary>

1. Install [Cline extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Open Cline sidebar → MCP Servers icon → Configure MCP Servers
3. Add:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart VS Code after saving.

</details>

<details>
<summary><b>🦘 Roo Code (VS Code)</b></summary>

1. Install [Roo Code extension](https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline)
2. Configure MCP servers through Roo Code settings
3. Add:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart VS Code after saving.

</details>

<details>
<summary><b>⚡ Zed Editor</b></summary>

**Note:** Requires [Zed Preview version](https://zed.dev/releases/preview)

Add to Zed's context servers config:

```json
{
  "context_servers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart Zed after saving.

</details>

<details>
<summary><b>💻 VS Code (with MCP Extension)</b></summary>

1. Install an MCP extension from VS Code marketplace
2. Configure MCP servers in extension settings
3. Add:

```json
{
  "mcpServers": {
    "sensei": {
      "command": "uvx",
      "args": ["sensei-mcp"]
    }
  }
}
```

Restart VS Code after saving.

</details>

---

## 🎯 What is Sensei?

**The Problem:** Output styles and custom instructions are cosmetic—applied **AFTER** Claude has already reasoned.

**The Solution:** Sensei injects engineering standards **BEFORE** reasoning based on:

- **50+ file types** (Python, JS/TS, Go, Java, Kotlin, Swift, Rust, GraphQL, Docker, k8s, etc.)
- **Operation context** (CREATE, REFACTOR, DEBUG, SECURITY, etc.)
- **Keywords** (multi-tenant, payment, async, etc.)
- **Session memory** of architectural decisions

**Result:** Standards actually influence behavior, not just formatting.

### Why This Matters

**Output Styles (Cosmetic):**

```
User: "Write an API endpoint"
Claude: [reasons about design]
Claude: [writes code]
Output Style: [formats the response]  ← Too late!
```

**Sensei MCP (Active):**

```
User: "Write an API endpoint"
Sensei: [injects API contracts, security, multi-tenancy standards]
Claude: [reasons WITH standards in context]
Claude: [writes code that follows standards]
```

---

## ⚡ Key Features

### v0.6.0 - Granular Persona Content Access (Option B Architecture) 🎭

- 🔧 **Fixed Critical Bug**: Orchestrator was returning placeholder text instead of real analysis
- 🏗️ **New Architecture**: MCP as content provider (not analysis engine)
  - MCP provides persona SKILL.md content
  - Claude (calling LLM) performs analysis using that content
  - Mirrors `.claude/skills/` pattern for consistency
- 🛠️ **4 New Granular Tools**:
  - `get_persona_content()` - Returns full SKILL.md for a specific persona
  - `suggest_personas_for_query()` - Intelligent persona selection with relevance scores
  - `get_session_context()` - Returns session memory (constraints, decisions, patterns) as JSON
  - `record_consultation()` - Records consultations after Claude performs analysis
- 📊 **Benefits**:
  - No LLM needed in MCP (no API keys, no costs, no latency)
  - Claude does what it's best at (analysis)
  - Predictable, deterministic MCP behavior
  - Extensible (just add SKILL.md files)

### v0.5.0 - Enhanced Discovery, CI/CD Integration, Team Collaboration & Database Expertise 🚀

- 🔍 **Interactive Persona Discovery** - Find the right expert faster:
  - Enhanced `list_available_skills()` with 3 format modes (standard, detailed, quick)
  - CLI demo mode (`sensei-mcp --demo`) with 5 real-world scenarios
  - Intelligent context hints when <2 personas selected
  - Technology keyword detection (database, api, security, frontend, mobile, ml)
- 🔧 **CI/CD Integration Pack** - Integrate Sensei into your development workflow:
  - GitHub Actions workflows for PR reviews and architecture checks
  - Pre-commit hooks (consistency, security, cost analysis)
  - GitLab CI pipeline with 3-stage validation
  - Enhanced `analyze_changes()` with persona suggestions
  - Comprehensive integration guide (500+ lines)
- 🤝 **Session Merge & Team Sync** - Collaborate on architectural decisions:
  - Merge multiple developer sessions with conflict resolution
  - 4 merge strategies (latest, oldest, all, manual)
  - Session comparison for side-by-side analysis
  - Attribution tracking for all decisions
- 🗄️ **Database Architect Persona** - Specialized database expert joins the team:
  - Schema design and normalization expertise
  - Query optimization and indexing strategies
  - Migration planning and scalability patterns
  - Multi-tenancy architecture guidance

### v0.4.0 - Analytics & Team Collaboration 📊

- 📊 **Session Analytics** - Data-driven insights into persona usage and decision patterns:
  - Track which personas are most/least used
  - Context distribution (SECURITY, CRISIS, ARCHITECTURAL, etc.)
  - Decision velocity and consultation patterns
  - Time-based filtering (last 7 days, last 30 days, all time)
  - Export as markdown, JSON, or text
- 📄 **Consultation Export** - Share individual consultations as professional reports:
  - Markdown format with metadata (ID, timestamp, mode, context)
  - JSON format for CI/CD integration
  - Plain text for communication tools
- 📋 **Session Summaries** - Export comprehensive ADRs (Architecture Decision Records):
  - Full decision history with rationale
  - Active constraints and agreed patterns
  - Recent consultation history
  - Configurable includes (decisions, consultations, constraints, patterns)
  - Perfect for team onboarding and alignment

### v0.3.0 - Multi-Persona Orchestrator 🎭

- 🎭 **47 Specialized Personas** - Skill Orchestrator coordinates expert perspectives across 12 categories:
  - **Core (3):** Snarky Senior Engineer, Pragmatic Architect, Legacy Archaeologist
  - **Specialized (6):** API Platform Engineer, Data Engineer, Database Architect, Frontend UX Specialist, ML Pragmatist, Mobile Platform Engineer
  - **Operations (3):** Site Reliability Engineer, Incident Commander, Observability Engineer
  - **Security (2):** Security Sentinel, Compliance Guardian
  - **Platform (3):** DevEx Champion, Platform Builder, QA Automation Engineer
  - **Cost (1):** FinOps Optimizer
  - **Leadership (4):** Empathetic Team Lead, Product Engineering Lead, Executive Liaison, Technical Writer
  - **DevRel (4):** Developer Advocate, Solutions Architect, Staff IC Advisor, Open Source Strategist
  - **Strategic (6):** M&A Due Diligence, Vendor Management, Technical Recruiting, Engineering Transformation, AI Ethics Governance, Data Strategy
  - **Management (3):** Engineering Manager, Director of Engineering, VP Engineering
  - **Technical Leadership (2):** Chief Architect, Principal Engineer
  - **Coordination (3):** Technical Program Manager, Technical Product Manager, Engineering Operations
  - **Infrastructure (6):** Database Reliability Engineer, Release Engineering Lead, Performance Engineer, Cloud Architect, Test Engineering Lead, Customer Success Engineer
  - **Meta (1):** Skill Orchestrator
- 🧠 **Context Detection** - Intelligently routes queries to relevant personas (CRISIS, SECURITY, POLITICAL, ARCHITECTURAL, COST, TEAM, TECHNICAL)
- 🤝 **Collaborative Synthesis** - Multiple perspectives with conflict resolution and consensus building
- 📊 **Consultation Tracking** - Session memory records which personas were consulted and why
- ⚡ **Multiple Modes:**
  - `orchestrated` (default): 2-5 persona collaboration
  - `quick`: Just Snarky Senior Engineer for fast answers
  - `crisis`: Emergency team (Incident Commander, SRE, Executive Liaison)
  - `standards`: Legacy single-voice mode for backwards compatibility

### Core Features (v0.2.x)

- 🎯 **Context-aware loading** - Only 5-15% of rulebook per request (87.5% token savings)
- 🧠 **Session memory** - Remembers architectural decisions across conversations
- 🤝 **Team Sync** - Share decisions and rules via `.sensei` folder in your repo
- 🕵️ **Git Awareness** - Automatically infer context from staged files
- 📦 **50+ file types** - Comprehensive tech stack coverage
- 🔍 **Smart inference** - Automatically determines relevant standards
- 🛡️ **Consistent enforcement** - No more re-litigating patterns
- 🚀 **Zero configuration** - Works immediately after install
- 🔒 **Privacy-first** - Runs locally, no external services

---

## 📚 Supported File Types

### Programming Languages (20+)

Python, JavaScript, TypeScript, Go, Java, **Kotlin**, **Swift**, Ruby, Rust, PHP, C#, **Scala**, **C/C++**, **Dart**, **Elixir**, **Clojure**, **Elm**, **Julia**, **R**

### Frontend & Web

React (JSX/TSX), Vue, Svelte, **Astro**, **HTML**, **CSS**, **SCSS**, **SASS**, **LESS**

### Infrastructure & DevOps

Terraform, **Docker**, **Kubernetes**, **nginx**, **Apache**, **Shell scripts** (bash/zsh), Makefiles, **HCL**

### Data & APIs

SQL, Prisma, **GraphQL**, **Protobuf**, **Avro**, **CSV**, **XML**, **Jupyter notebooks**

### Config & Tools

YAML, JSON, TOML, **ESLint**, **Prettier**, **Jest**, **Playwright**, **Cypress**, **Webpack**, **Vite**, tsconfig.json

### CI/CD

**GitHub Actions**, **GitLab CI**, **Jenkins**, **CircleCI**, **Azure Pipelines**

### Mobile

**Android** (AndroidManifest.xml, build.gradle), **iOS** (Info.plist, Podfile)

### Package Managers

package.json, Gemfile, **Cargo.toml**, **go.mod**, requirements.txt, **Pipfile**

### Monitoring

**Prometheus**, **Grafana**, **Datadog**, **New Relic**, **Sentry**

---

## 🛠️ Usage

> **📖 NEW: [Complete Usage Guide with Real-World Examples](docs/USAGE_GUIDE.md)**
>
> See detailed use cases including API design review, production crisis response, cost optimization, code review, and session-aware architecture decisions.

Sensei provides **20 MCP tools** (4 new in v0.6.0, 2 in v0.5.0, 3 in v0.4.0, 3 in v0.3.0) + **CLI demo mode**:

### NEW v0.6.0 - Granular Persona Content Tools

#### 1. get_persona_content (NEW)

Get full SKILL.md content for a specific persona. Claude uses this content to analyze queries from that persona's perspective.

```python
# Get full Security Sentinel content
content = get_persona_content(
  persona_name="security-sentinel",
  include_metadata=True  # Optional: includes description and expertise
)
# Returns: Complete SKILL.md with principles, personality, expertise, guidelines

# Claude then uses this content as context to analyze your query
# Example workflow:
# 1. Claude suggests personas → ["security-sentinel", "api-platform-engineer"]
# 2. Claude gets content for each → Full SKILL.md files
# 3. Claude analyzes from each perspective using the content
# 4. Claude synthesizes all perspectives into recommendation
```

#### 2. suggest_personas_for_query (NEW)

Intelligent persona selection based on query analysis with relevance scores and rationale.

```python
# Get persona suggestions for a query
suggestions = suggest_personas_for_query(
  query="How should we handle authentication for our API?",
  max_suggestions=5,  # Maximum number of suggestions (default: 5)
  context_hint="SECURITY"  # Optional: force specific context
)
# Returns JSON:
# {
#   "query": "How should we handle authentication...",
#   "detected_context": "SECURITY",
#   "suggestions": [
#     {
#       "name": "security-sentinel",
#       "display_name": "Security Sentinel",
#       "relevance": 0.95,
#       "rationale": "Expert in authentication, security"
#     },
#     {
#       "name": "api-platform-engineer",
#       "display_name": "API Platform Engineer",
#       "relevance": 0.82,
#       "rationale": "Expert in API design, contracts"
#     }
#   ]
# }

# Auto-detect context from query
suggest_personas_for_query(
  query="Our AWS bill is too high",
  max_suggestions=3
)
# Returns: finops-optimizer, pragmatic-architect, site-reliability-engineer
```

#### 3. get_session_context (NEW)

Get session memory (constraints, decisions, patterns) as JSON for context-aware analysis.

```python
# Get full session context
context = get_session_context(
  session_id="saas-backend",
  project_root="/path/to/repo"  # Optional: for project-local sessions
)
# Returns JSON:
# {
#   "session_id": "saas-backend",
#   "active_constraints": ["AWS only", "Python 3.11+", "PostgreSQL"],
#   "patterns_agreed": ["Use FastAPI", "JWT auth"],
#   "recent_decisions": [
#     {
#       "id": "dec-001",
#       "category": "architecture",
#       "description": "Use PostgreSQL for primary data store",
#       "rationale": "Team expertise, ACID guarantees",
#       "timestamp": "2025-01-23T10:30:00"
#     }
#   ]
# }

# Claude includes this context when analyzing to ensure consistency
```

#### 4. record_consultation (NEW)

Record consultations in session history after Claude performs analysis.

```python
# After Claude analyzes using persona content
record_consultation(
  query="Should we migrate to microservices?",
  personas_used=["pragmatic-architect", "site-reliability-engineer", "finops-optimizer"],
  session_id="saas-backend",
  project_root="/path/to/repo",  # Optional
  synthesis="[Claude's complete analysis and recommendation]"  # Optional
)
# Returns: "✅ Consultation recorded: consult_42"

# This consultation is now in session history for:
# - Analytics (get_session_insights)
# - Export (export_session_summary)
# - Future context
```

### v0.5.0 - Enhanced Discovery & Team Merge

#### CLI Demo Mode

Interactive walkthrough of Sensei's multi-persona capabilities.

```bash
# Run the interactive demo
sensei-mcp --demo

# Shows 5 real-world scenarios:
# - Architecture Decision (microservices migration)
# - Production Crisis (database outage)
# - Security Review (authentication audit)
# - Cost Optimization (cloud spending)
# - Code Quality (technical debt)
```

#### 5. merge_sessions

Merge multiple developer sessions with intelligent conflict resolution.

```python
# Merge two developer sessions
merge_sessions(
  session_ids=["alice-frontend", "bob-backend"],
  target_session_id="sprint-23",
  conflict_strategy="latest",  # "latest", "oldest", "all", "manual"
  session_id="sprint-23",
  project_root="/path/to/repo"
)
# Returns: MergeResult with decisions merged, conflicts detected, attribution tracking

# Manual conflict resolution
merge_sessions(
  session_ids=["alice-session", "bob-session"],
  target_session_id="team-session",
  conflict_strategy="manual"  # Returns conflicts for human resolution
)
```

#### 6. compare_sessions

Compare two sessions side-by-side before merging.

```python
compare_sessions(
  session_a_id="alice-session",
  session_b_id="bob-session",
  session_id="default",
  project_root="/path/to/repo"
)
# Returns: Markdown comparison with decisions, constraints, patterns diff
```

### v0.4.0 Tools - Analytics & Collaboration

#### 7. get_session_insights

Get data-driven insights into persona usage, consultation patterns, and decision velocity.

```python
# Get insights for last 7 days
get_session_insights(
  session_id="saas-backend",
  time_range="last_7_days",  # "last_7_days", "last_30_days", "all_time"
  format="markdown",  # "markdown", "json", "text"
  min_consultations=2  # Only include personas with 2+ consultations
)
# Returns: Most/least used personas, context distribution, decision metrics

# Get JSON for CI/CD integration
get_session_insights(
  session_id="saas-backend",
  format="json"
)
```

#### 8. export_consultation

Export a single consultation as a shareable report.

```python
# Export as markdown with full metadata
export_consultation(
  consultation_id="c-2025-01-22-001",
  session_id="saas-backend",
  format="markdown",  # "markdown", "json", "text"
  include_metadata=True
)
# Returns: Professional report with query, personas consulted, synthesis, linked decision

# Export as JSON for API integration
export_consultation(
  consultation_id="c-2025-01-22-001",
  format="json"
)
```

#### 9. export_session_summary

Export comprehensive ADRs and session summaries for team sharing.

```python
# Full session export with all sections
export_session_summary(
  session_id="saas-backend",
  format="markdown",  # "markdown", "json", "text"
  include=["decisions", "consultations", "constraints", "patterns"],
  max_consultations=10
)
# Returns: ADRs, consultation history, constraints, patterns in markdown

# Export only decisions as JSON
export_session_summary(
  session_id="saas-backend",
  format="json",
  include=["decisions"]
)
```

### v0.3.0 Tools - Multi-Persona Orchestrator

> **Note:** `get_engineering_guidance()` and `consult_skill()` will be deprecated in v0.7.0. Use the new v0.6.0 granular tools instead (`get_persona_content`, `suggest_personas_for_query`, `get_session_context`, `record_consultation`).

#### 10. get_engineering_guidance

Get collaborative multi-persona guidance on any engineering question.

```python
# Example: Architecture decision
get_engineering_guidance(
  query="Should we use microservices or a monolith for our SaaS app?",
  mode="orchestrated",  # default: auto-selects 2-5 relevant personas
  session_id="saas-backend",
  output_format="standard"
)
# Returns: Synthesis from Pragmatic Architect, Snarky Senior Engineer,
#          Product Engineering Lead with consensus and tensions

# Quick mode - fast answer from just Snarky
get_engineering_guidance(
  query="How do I fix this API bug?",
  mode="quick"  # Only Snarky Senior Engineer responds
)

# Crisis mode - emergency team
get_engineering_guidance(
  query="Production database is down!",
  mode="crisis"  # Incident Commander, SRE, Executive Liaison
)

# Request specific personas
get_engineering_guidance(
  query="How do we reduce our AWS bill?",
  specific_personas=["finops-optimizer", "pragmatic-architect"]
)
```

#### 11. consult_skill

Consult a single persona directly for targeted expertise.

```python
consult_skill(
  skill_name="security-sentinel",
  query="Review this authentication implementation for vulnerabilities",
  session_id="saas-backend"
)
```

#### 12. list_available_skills

Discover all 64 available personas organized by category.

```python
# List all personas (standard format)
list_available_skills()

# Detailed format with examples and metadata
list_available_skills(format="detailed")

# Quick format (names only)
list_available_skills(format="quick")

# List by category
list_available_skills(category="operations")  # SRE, Incident Commander, etc.
list_available_skills(category="specialized")  # Security, FinOps, Database Architect, etc.
```

### Core Tools (v0.2.x) - Still Supported

#### 13. get_engineering_context (Legacy)

Smart context injection - loads relevant standards based on files and operation.

**Note:** In v0.3.0, this is now called via `get_engineering_guidance(..., mode="standards")` for backwards compatibility.

```python
# Example: Working on payment API
get_engineering_context(
  operation="CREATE",
  file_paths=["api/payments.py"],
  description="Building Stripe payment endpoint",
  session_id="saas-backend"
)
# Returns: API contracts, security, multi-tenancy, idempotency standards
```

#### 14. record_decision

Save architectural decisions to prevent re-litigation.

```python
record_decision(
  category="architecture",
  description="Use PostgreSQL for primary data store",
  rationale="Team expertise, ACID guarantees, proven at scale",
  session_id="saas-backend"
)
```

#### 15. validate_against_standards

Pre-implementation validation check.

```python
validate_against_standards(
  design_description="REST API with JWT auth",
  focus_areas=["security", "multi-tenant"],
  session_id="saas-backend"
)
```

#### 16. get_session_summary

Review all decisions and constraints for current project.

```python
get_session_summary(session_id="saas-backend")
```

#### 17. list_sessions

Manage multiple projects with separate session states.

```python
list_sessions()
```

#### 18. query_specific_standard

Direct access to specific rulebook sections.

```python
query_specific_standard(
  section_name="multi_tenancy",
  session_id="saas-backend"
)
```

#### 19. check_consistency

Validate proposed changes against past decisions.

```python
check_consistency(
  proposed_change="Switch from Postgres to MongoDB",
  session_id="saas-backend"
)
```

#### 20. analyze_changes

Automatically infer context from staged git changes (enhanced in v0.5.0 with persona suggestions).

```python
analyze_changes(project_root="/path/to/repo")
# Returns: File changes, diff stats, and suggested personas based on file patterns
```

---

## 🤝 Team Sync & Project Isolation

Sensei supports sharing decisions and rules with your team:

1.  **Create a `.sensei` folder** in your project root.
2.  **Add `rules.md`** for custom project-specific rules.
3.  **Run tools with `project_root`**: Decisions will be saved to `.sensei/decisions.md`.

This allows you to commit your engineering memory to Git!

---

## 🏗️ How It Works

1. **Context Inference Engine** analyzes:

   - File patterns (API routes, DB schemas, tests, etc.)
   - Operation type (CREATE, REFACTOR, DEBUG, etc.)
   - Keywords (tenant, payment, async, etc.)
2. **Rulebook Loader** extracts relevant sections:

   - 57 total sections mapped to 32 file patterns
   - Core sections always loaded (principles, philosophy)
   - Task-specific sections loaded on demand
3. **Session Manager** persists decisions:

   - Stored in `$HOME/.sensei/sessions/<project>.json`
   - Human-readable JSON format
   - Loaded automatically on each tool call

### File Pattern Examples

| File Type                | Triggers                                  | Example Files                                       |
| ------------------------ | ----------------------------------------- | --------------------------------------------------- |
| **API Files**      | API contracts, security, multi-tenancy    | `api/billing.py`, `routes/users.ts`             |
| **Database**       | Data persistence, security, multi-tenancy | `migrations/001.sql`, `schema.prisma`           |
| **Tests**          | Testing standards, code quality           | `test_api.py`, `api.spec.ts`                    |
| **Infrastructure** | Cloud platform, compliance, cost          | `main.tf`, `docker-compose.yml`, `k8s/*.yaml` |
| **CI/CD**          | Delivery, testing, observability          | `.github/workflows/*.yml`, `Jenkinsfile`        |
| **Frontend**       | Performance, i18n, security (XSS)         | `App.tsx`, `index.html`, `styles.css`         |
| **Mobile**         | Cloud, dependencies, compliance           | `AndroidManifest.xml`, `Podfile`                |

---

## 💡 Example Workflows

### Architecture Decision (v0.3.0 Multi-Persona)

```python
# 1. Get multi-persona guidance on architecture
result = get_engineering_guidance(
  query="Should we migrate from a monolith to microservices? We have 5 engineers and 10K users.",
  mode="orchestrated",  # Auto-selects relevant personas
  session_id="saas-backend"
)
# Personas consulted: Pragmatic Architect, Snarky Senior Engineer, Product Engineering Lead
# Synthesis includes: Consensus points, tensions/trade-offs, recommendation

# 2. Consult specific expert for follow-up
consult_skill(
  skill_name="finops-optimizer",
  query="What's the cost impact of microservices vs monolith?",
  session_id="saas-backend"
)

# 3. Record the decision
record_decision(
  category="architecture",
  description="Stay monolith for now, plan modular architecture",
  rationale="Team size and user scale don't justify microservices complexity yet",
  session_id="saas-backend"
)
```

### Production Incident (Crisis Mode)

```python
# Crisis mode activates emergency response team
get_engineering_guidance(
  query="Production database has 10K connections and is timing out!",
  mode="crisis",  # Incident Commander, SRE, Executive Liaison
  session_id="saas-backend"
)
# Returns: Immediate triage steps, communication plan, root cause analysis
```

### Starting a New Feature (v0.2.x Legacy Mode)

```python
# 1. Get context for the feature (legacy standards mode)
get_engineering_context(
  operation="CREATE",
  file_paths=["api/webhooks.py"],
  description="Stripe webhook handler for subscription events",
  session_id="saas-backend"
)

# 2. Record key decisions
record_decision(
  category="architecture",
  description="Use idempotent webhook processing with deduplication",
  rationale="Webhooks can be retried, need to handle duplicates safely",
  session_id="saas-backend"
)

# 3. Validate before implementation
validate_against_standards(
  design_description="POST /webhooks/stripe with signature verification",
  focus_areas=["security", "api"],
  session_id="saas-backend"
)
```

### Code Review

```python
# Load relevant standards for review
get_engineering_context(
  operation="REVIEW",
  file_paths=["api/users.py", "db/queries.sql"],
  description="User management PR - check multi-tenancy",
  session_id="saas-backend"
)

# Check consistency with past decisions
check_consistency(
  proposed_change="Add user_id index without tenant_id",
  session_id="saas-backend"
)
```

### Debugging Production Issue

```python
# Get observability and debugging context
get_engineering_context(
  operation="DEBUG",
  file_paths=["services/payment_processor.py"],
  description="Investigating payment timeout issues",
  session_id="saas-backend"
)

# Query specific standards
query_specific_standard(
  section_name="observability",
  session_id="saas-backend"
)
```

---

## 📖 Documentation

### Getting Started
- **[Quick Start Guide](docs/QUICKSTART.md)** - 5-minute fast start
- **[Usage Guide](docs/USAGE_GUIDE.md)** - Comprehensive usage examples

### MCP Ecosystem Integration (NEW)
- **[MCP Integration Architecture](docs/MCP_INTEGRATION_ARCHITECTURE.md)** - Complete vision for human-LLM partnership
- **[MCP Integration Examples](docs/MCP_INTEGRATION_EXAMPLES.md)** - Real-world workflows combining multiple MCP servers
- **[CI/CD Integration Guide](integrations/INTEGRATION_GUIDE.md)** - GitHub Actions, GitLab CI, pre-commit hooks

### Technical Documentation
- **[Architecture Deep Dive](docs/ARCHITECTURE.md)** - Technical implementation details
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Publishing Guide](PUBLISHING.md)** - PyPI publishing workflow

---

## 🔧 Development

### Local Setup

```bash
git clone https://github.com/amarodeabreu/sensei-mcp.git
cd sensei-mcp
pip install -e .
```

### Run Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
isort src/ tests/
```

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development setup
- Running tests
- Code style guidelines
- PR submission process

---

## 📊 Comparison: Before & After

### Before Sensei

❌ Output styles applied **after** reasoning
❌ Repeating same context every conversation
❌ Re-litigating architectural decisions
❌ Forgetting past constraints
❌ Loading entire rulebook (40% of tokens)

### After Sensei

✅ Standards influence reasoning **before** code is written
✅ Context-aware loading (5-15% of rulebook)
✅ Session memory persists decisions
✅ Consistent enforcement across conversations
✅ Multi-project support with isolation

---

## 🏆 ROI Calculation

**Team of 5 engineers:**

- 10 mins/day saved per engineer avoiding re-explanation
- 5 architectural re-litigations prevented/week
- 30 mins/incident saved with better observability

**Annual Savings:** ~500 hours of engineering time

---

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE) for details

---

## 🔗 Links

- **GitHub:** https://github.com/amarodeabreu/sensei-mcp
- **PyPI:** https://pypi.org/project/sensei-mcp/
- **Issues:** https://github.com/amarodeabreu/sensei-mcp/issues

---

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Model Context Protocol](https://modelcontextprotocol.io/)
- Inspired by the need for consistent engineering standards

---

Made with 🥋 by [amarodeabreu](https://github.com/amarodeabreu)
