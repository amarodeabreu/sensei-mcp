# Sensei MCP 🥋

![PyPI](https://img.shields.io/pypi/v/sensei-mcp)

![Python](https://img.shields.io/badge/python-3.10+-blue)

![License](https://img.shields.io/badge/license-Apache%202.0-blue)

> Multi-persona engineering mentor with 22 specialized AI skills orchestrating collaborative guidance

**NEW in v0.4.0:** Analytics & Team Collaboration - Track persona effectiveness, export session summaries as ADRs, and share engineering decisions with your team.

**v0.3.0:** Sensei features a **Skill Orchestrator** with 22 specialized personas (Snarky Senior Engineer, Pragmatic Architect, Security Sentinel, FinOps Optimizer, and 18 more) that collaborate to provide nuanced, multi-perspective engineering guidance.

Sensei transforms your engineering standards from passive documentation into an active mentor that injects relevant guidelines **before** Claude reasons, maintaining session memory of architectural decisions.

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

- 🎭 **22 Specialized Personas** - Skill Orchestrator coordinates expert perspectives:
  - **Core Skills:** Snarky Senior Engineer, Pragmatic Architect, Legacy Archaeologist
  - **Specialized Skills:** Security Sentinel, FinOps Optimizer, Performance Engineer, Product Engineering Lead, API Architect
  - **Operations:** Incident Commander, SRE, Executive Liaison, Compliance Guardian
  - **Plus 10+ more:** DevX Advocate, Tech Debt Wrangler, Data Platform Engineer, Frontend Performance, Staff+ Mentor, etc.
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

Sensei provides **13 MCP tools** (3 new in v0.4.0, 3 in v0.3.0):

### NEW v0.4.0 Tools - Analytics & Collaboration

#### 1. get_session_insights (NEW)

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

#### 2. export_consultation (NEW)

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

#### 3. export_session_summary (NEW)

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

#### 4. get_engineering_guidance (Primary Tool)

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

#### 5. consult_skill

Consult a single persona directly for targeted expertise.

```python
consult_skill(
  skill_name="security-sentinel",
  query="Review this authentication implementation for vulnerabilities",
  session_id="saas-backend"
)
```

#### 6. list_available_skills

Discover all 22 available personas organized by category.

```python
# List all personas
list_available_skills()

# List by category
list_available_skills(category="operations")  # SRE, Incident Commander, etc.
list_available_skills(category="specialized")  # Security, FinOps, Performance, etc.
```

### Core Tools (v0.2.x) - Still Supported

#### 7. get_engineering_context (Legacy)

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

#### 8. record_decision

Save architectural decisions to prevent re-litigation.

```python
record_decision(
  category="architecture",
  description="Use PostgreSQL for primary data store",
  rationale="Team expertise, ACID guarantees, proven at scale",
  session_id="saas-backend"
)
```

#### 9. validate_against_standards

Pre-implementation validation check.

```python
validate_against_standards(
  design_description="REST API with JWT auth",
  focus_areas=["security", "multi-tenant"],
  session_id="saas-backend"
)
```

#### 10. get_session_summary

Review all decisions and constraints for current project.

```python
get_session_summary(session_id="saas-backend")
```

#### 11. list_sessions

Manage multiple projects with separate session states.

```python
list_sessions()
```

#### 12. query_specific_standard

Direct access to specific rulebook sections.

```python
query_specific_standard(
  section_name="multi_tenancy",
  session_id="saas-backend"
)
```

#### 13. check_consistency

Validate proposed changes against past decisions.

```python
check_consistency(
  proposed_change="Switch from Postgres to MongoDB",
  session_id="saas-backend"
)
```

#### 14. analyze_changes

Automatically infer context from staged git changes.

```python
analyze_changes(project_root="/path/to/repo")
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

- **[Quick Start Guide](docs/QUICKSTART.md)** - 5-minute fast start
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
