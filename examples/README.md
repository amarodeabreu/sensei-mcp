# Sensei MCP Demonstration Examples

This directory contains example outputs from executable demo workflows that showcase Sensei's multi-MCP orchestration capabilities.

## Available Demos

### 1. Authentication Security Review (`auth-review`)

**What it demonstrates:**
- Multi-MCP synthesis (Sensei + Context7 + Tavily + Playwright)
- Persona selection based on security context
- Live documentation fetching (OWASP, OAuth standards)
- Recent vulnerability search (CVEs, security advisories)
- Optional live system inspection

**Example output:** [`auth-security-review-example.md`](./auth-security-review-example.md)

**How to run:**
```python
run_demo(demo_type="auth-review")

# With custom parameters
run_demo(
    demo_type="auth-review",
    custom_params={
        "user_query": "Review OAuth implementation",
        "app_url": "https://myapp.com/login",
        "framework": "Django"
    }
)
```

**MCPs involved:** Sensei, Context7, Tavily, Playwright
**Cost estimate:** $0.05-0.10
**Time estimate:** 30-60 seconds

---

### 2. Performance Debugging (`performance-debug`)

**What it demonstrates:**
- Live performance measurement with Playwright
- Core Web Vitals analysis
- Network request inspection
- Performance optimization recommendations from Context7

**How to run:**
```python
run_demo(demo_type="performance-debug")
```

**MCPs involved:** Sensei, Playwright, Context7
**Cost estimate:** $0.00-0.05
**Time estimate:** 45-90 seconds

---

### 3. Cloud Cost Optimization (`cost-analysis`)

**What it demonstrates:**
- Cost analysis with Sensei FinOps persona
- Real-time pricing data from Tavily
- Optimization recommendations

**How to run:**
```python
run_demo(demo_type="cost-analysis")
```

**MCPs involved:** Sensei, Tavily
**Cost estimate:** $0.01-0.03
**Time estimate:** 20-40 seconds

---

### 4. API Design Review (`api-review`)

**What it demonstrates:**
- API design best practices from Context7
- Current API standards (OpenAPI, REST, GraphQL)
- Recent trends and patterns from Tavily
- Multi-persona analysis (API Engineer, Architect, Security)

**How to run:**
```python
run_demo(demo_type="api-review")
```

**MCPs involved:** Sensei, Context7, Tavily
**Cost estimate:** $0.01-0.03
**Time estimate:** 20-40 seconds

---

### 5. Architecture Refactoring (`architecture-refactoring`) 🔥 **NEW!**

**What it demonstrates:**
- Architecture-driven refactoring with Sensei + Serena
- Strategic guidance (Sensei) → Tactical execution (Serena)
- Dependency injection pattern application
- SOLID principles enforcement

**Example output:** [`architecture-refactoring-example.md`](./architecture-refactoring-example.md)

**How to run:**
```python
run_demo(demo_type="architecture-refactoring")

# With custom parameters
run_demo(
    demo_type="architecture-refactoring",
    custom_params={
        "user_query": "Refactor payment handler to use DI",
        "target_file": "src/payments/handler.py"
    }
)
```

**MCPs involved:** Sensei, Serena, Context7
**Cost estimate:** $0.00
**Time estimate:** 30-60 seconds

---

### 6. Code Navigation (`code-navigation`) 🔥 **NEW!**

**What it demonstrates:**
- Semantic code search with Serena
- Multi-tenancy security audit with Sensei
- Pattern violation discovery
- Impact analysis and remediation planning

**Example output:** [`code-navigation-example.md`](./code-navigation-example.md)

**How to run:**
```python
run_demo(demo_type="code-navigation")

# With custom parameters
run_demo(
    demo_type="code-navigation",
    custom_params={
        "user_query": "Find SQL injection vulnerabilities",
        "violation_pattern": 'execute\\(f".*\\{.*\\}"\\)'
    }
)
```

**MCPs involved:** Sensei, Serena
**Cost estimate:** $0.00
**Time estimate:** 20-40 seconds

---

### 7. Pattern Enforcement (`pattern-enforcement`) 🔥 **NEW!**

**What it demonstrates:**
- Automated pattern enforcement with Serena
- API consistency validation with Sensei
- RFC 7807 Problem Details standardization
- Codebase-wide refactoring

**Example output:** [`pattern-enforcement-example.md`](./pattern-enforcement-example.md)

**How to run:**
```python
run_demo(demo_type="pattern-enforcement")

# With custom parameters
run_demo(
    demo_type="pattern-enforcement",
    custom_params={
        "user_query": "Enforce consistent logging format",
        "violation_pattern": "print\\(.*\\)",
        "pattern_name": "Structured logging"
    }
)
```

**MCPs involved:** Sensei, Serena, Context7
**Cost estimate:** $0.00-0.01
**Time estimate:** 20-40 seconds

---

### 8. PR Security Review (`pr-review`) 🔥 **NEW!**

**What it demonstrates:**
- Multi-persona PR review with GitHub + Sensei
- Security and architectural analysis of pull requests
- OWASP standards validation with Context7
- CI/CD status checking

**Example output:** [`github-workflows-example.md`](./github-workflows-example.md) (Example 1)

**How to run:**
```python
run_demo(demo_type="pr-review")

# With custom parameters
run_demo(
    demo_type="pr-review",
    custom_params={
        "pr_number": "456",
        "pr_title": "Add payment gateway integration"
    }
)
```

**MCPs involved:** Sensei, GitHub, Context7
**Cost estimate:** $0.01-0.03
**Time estimate:** 20-40 seconds

---

### 9. Commit Pattern Analysis (`commit-analysis`) 🔥 **NEW!**

**What it demonstrates:**
- Architectural drift detection via commit history
- Pattern violation discovery with Serena
- Session consistency checking with Sensei
- Historical code evolution tracking

**Example output:** [`github-workflows-example.md`](./github-workflows-example.md) (Example 2)

**How to run:**
```python
run_demo(demo_type="commit-analysis")

# With custom parameters
run_demo(
    demo_type="commit-analysis",
    custom_params={
        "owner": "your-org",
        "repo": "your-repo",
        "commit_count": "100"
    }
)
```

**MCPs involved:** Sensei, GitHub, Serena
**Cost estimate:** $0.00
**Time estimate:** 30-60 seconds

---

### 10. Issue Triage (`issue-triage`) 🔥 **NEW!**

**What it demonstrates:**
- Smart issue categorization with GitHub
- Persona-based team assignment
- Priority and severity assessment
- Similar issue discovery with Tavily

**Example output:** [`github-workflows-example.md`](./github-workflows-example.md) (Example 3)

**How to run:**
```python
run_demo(demo_type="issue-triage")

# With custom parameters
run_demo(
    demo_type="issue-triage",
    custom_params={
        "issue_number": "789",
        "issue_title": "Memory leak in worker process"
    }
)
```

**MCPs involved:** Sensei, GitHub, Tavily
**Cost estimate:** $0.01-0.03
**Time estimate:** 15-30 seconds

---

## List All Available Demos

```python
list_demos()
```

Returns JSON with all available demos:
```json
[
  {
    "id": "auth-review",
    "name": "Authentication Security Review Demo",
    "description": "Demonstrates comprehensive auth security review...",
    "template": "auth-security-review",
    "example_params": ["user_query", "app_url", "framework"]
  },
  ...
]
```

## Understanding Demo Outputs

Each demo generates a comprehensive report with:

1. **Overview** - Demo description, workflow template, MCPs involved
2. **Parameters** - Input parameters used for the workflow
3. **Execution Plan** - Step-by-step workflow showing MCP coordination
4. **Example Findings** - Simulated multi-MCP synthesis results
5. **MCP Coordination** - How different MCPs worked together
6. **Expected Sections** - What a real execution would include

## Output Formats

Demos support three output formats:

```python
# Markdown (default) - human-readable report
run_demo(demo_type="auth-review", output_format="markdown")

# JSON - structured data for programmatic use
run_demo(demo_type="auth-review", output_format="json")

# Text - plain text for terminal output
run_demo(demo_type="auth-review", output_format="text")
```

## Use Cases

### 1. Testing Multi-MCP Coordination
Run demos to verify that multiple MCP servers work together correctly:
```python
# Verify Sensei + Context7 + Tavily coordination
run_demo(demo_type="auth-review")
```

### 2. Generating Documentation Examples
Create realistic examples for integration guides:
```python
# Generate markdown example
result = run_demo(demo_type="auth-review", output_format="markdown")
# Save to file for documentation
```

### 3. Demonstrating Capabilities
Show potential users how Sensei orchestrates multiple MCPs:
```python
# Quick demo during presentation
run_demo(demo_type="api-review")
```

### 4. Training and Onboarding
Help new users understand multi-MCP workflows:
```python
# Walk through each demo
for demo_type in ["auth-review", "performance-debug", "cost-analysis", "api-review"]:
    run_demo(demo_type=demo_type)
```

## Design Philosophy

These demos are **executable examples** that:
- Use real workflow templates from the MCP orchestrator
- Show realistic parameter substitution
- Demonstrate multi-MCP coordination patterns
- Provide example findings showing how MCPs complement each other
- Generate outputs suitable for documentation

They are **not** live integrations (they don't actually call external MCPs), but they show exactly what a real execution would look like.

## Next Steps

After exploring demos:
1. Review the [MCP Integration Architecture](../docs/MCP_INTEGRATION_ARCHITECTURE.md)
2. Read integration guides in [`docs/integrations/`](../docs/integrations/)
3. Set up your own MCP configurations
4. Run real multi-MCP workflows

## Contributing

To add a new demo:
1. Add configuration to `DemoExecutor.DEMO_CONFIGS` in `src/sensei_mcp/demo_executor.py`
2. Create corresponding workflow template in `MCPOrchestrator.WORKFLOW_TEMPLATES`
3. Generate example output with `run_demo(demo_type="your-demo")`
4. Save example to `examples/your-demo-example.md`
5. Update this README with demo description

---

**Generated with Sensei MCP v0.8.0**
