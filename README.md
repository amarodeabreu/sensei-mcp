# Sensei MCP 🥋

![PyPI](https://img.shields.io/pypi/v/sensei-mcp)

![Python](https://img.shields.io/badge/python-3.10+-blue)

![License](https://img.shields.io/badge/license-Apache%202.0-blue)

> Your engineering standards mentor - Active context injection for 50+ file types with session memory

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

Sensei provides 7 MCP tools:

### 1. get_engineering_context

Smart context injection - loads relevant standards based on files and operation.

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

### 2. record_decision

Save architectural decisions to prevent re-litigation.

```python
record_decision(
  category="architecture",
  description="Use PostgreSQL for primary data store",
  rationale="Team expertise, ACID guarantees, proven at scale",
  session_id="saas-backend"
)
```

### 3. validate_against_standards

Pre-implementation validation check.

```python
validate_against_standards(
  design_description="REST API with JWT auth",
  focus_areas=["security", "multi-tenant"],
  session_id="saas-backend"
)
```

### 4. get_session_summary

Review all decisions and constraints for current project.

```python
get_session_summary(session_id="saas-backend")
```

### 5. list_sessions

Manage multiple projects with separate session states.

```python
list_sessions()
```

### 6. query_specific_standard

Direct access to specific rulebook sections.

```python
query_specific_standard(
  section_name="multi_tenancy",
  session_id="saas-backend"
)
```

### 7. check_consistency

Validate proposed changes against past decisions.

```python
check_consistency(
  proposed_change="Switch from Postgres to MongoDB",
  session_id="saas-backend"
)
```

### 8. analyze_changes

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

### Starting a New Feature

```python
# 1. Get context for the feature
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
