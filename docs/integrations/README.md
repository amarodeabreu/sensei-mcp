# Sensei MCP Integration Guides

This directory contains comprehensive integration guides for combining Sensei MCP with other MCP servers to create a world-class CTO co-pilot system.

---

## 🎬 Try Executable Demos First!

Before diving into the guides, try our **executable demonstration workflows** that showcase multi-MCP orchestration in action:

```python
# List available demos
list_demos()

# Run auth security review demo (Sensei + Context7 + Tavily + Playwright)
run_demo(demo_type="auth-review")

# Run with custom parameters
run_demo(
    demo_type="auth-review",
    custom_params={
        "user_query": "Review OAuth implementation",
        "framework": "Django"
    }
)
```

**Available demos:**
- `auth-review` - Authentication security review (4 MCPs)
- `performance-debug` - Performance debugging workflow
- `cost-analysis` - Cloud cost optimization
- `api-review` - API design review
- `architecture-refactoring` - Architecture-driven refactoring with Serena
- `code-navigation` - Semantic code navigation with Serena
- `pattern-enforcement` - Code pattern enforcement with Serena
- `pr-review` - PR security & architecture review with GitHub 🔥 **NEW!**
- `commit-analysis` - Commit pattern analysis with GitHub 🔥 **NEW!**
- `issue-triage` - Issue triage & prioritization with GitHub 🔥 **NEW!**

**See full examples:** [`../../examples/`](../../examples/)

These demos show exactly how Sensei orchestrates multiple MCP servers to create comprehensive, multi-perspective analysis workflows.

---

## 📚 Available Integration Guides

### Tier 1: Essential Integrations (Integrate First)

#### 1. [Context7 MCP](./CONTEXT7.md)
**Purpose:** Up-to-date library and framework documentation

**Key Use Cases:**
- Security reviews with current OWASP standards
- Framework upgrade decisions (React, FastAPI, etc.)
- Library comparisons with latest benchmarks

**Quick Start:**
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

**Best For:**
- Security Sentinel + current vulnerability standards
- API Platform Engineer + latest framework docs
- Pragmatic Architect + migration guides

---

#### 2. [Tavily MCP](./TAVILY.md)
**Purpose:** Real-time web search and intelligence gathering

**Key Use Cases:**
- Recent CVE lookups (last 7 days)
- Current cloud pricing (AWS/GCP/Azure)
- Incident intelligence (recent outages)
- Technology due diligence

**Quick Start:**
```bash
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxx"
claude mcp add tavily -- npx -y @tavily/mcp-server
```

**Best For:**
- Security Sentinel + recent vulnerability data
- FinOps Optimizer + current pricing
- SRE + incident postmortems

**💸 Cost:** $0.005-0.01 per search (1,000 free/month)

---

#### 3. [Playwright MCP](./PLAYWRIGHT.md)
**Purpose:** Live system inspection, performance analysis, debugging

**Key Use Cases:**
- Performance debugging (Core Web Vitals)
- UI/UX inspection and comparison
- Security audits (network traffic analysis)
- Accessibility compliance (WCAG)

**Quick Start:**
```bash
npx playwright install chromium
claude mcp add playwright -- npx -y @playwright/mcp-server
```

**Best For:**
- Performance Engineer + live measurements
- Frontend UX Specialist + visual inspection
- Security Sentinel + network analysis
- Accessibility Specialist + WCAG audits

---

#### 4. [Serena MCP](./SERENA.md) 🔥 **NEW!**
**Purpose:** Semantic code analysis, refactoring, and surgical code changes

**Key Use Cases:**
- Architecture-driven refactoring (Sensei designs → Serena executes)
- Code pattern enforcement across codebase
- Multi-tenancy migration and validation
- Dependency injection migration

**Quick Start:**
```bash
pip install serena-mcp
claude mcp add serena -- python -m serena_mcp
```

**Best For:**
- Pragmatic Architect + code refactoring
- Security Sentinel + pattern violations
- API Platform Engineer + consistency enforcement
- Any persona + tactical code execution

**Why Essential:** Serena completes the loop - Sensei provides strategic intelligence ("what to do"), Serena provides tactical execution ("how to do it").

---

## 🎯 Integration Patterns

### Pattern 1: Security Review (Multi-MCP)

**Query:** "Review our authentication implementation for security issues"

**MCP Flow:**
```
1. Sensei → Suggest personas: [security-sentinel, api-platform-engineer, privacy-engineer]
2. Context7 → Fetch OWASP ASVS, OAuth 2.0 Security BCP
3. Tavily → Search "OAuth vulnerabilities 2025"
4. Playwright → Inspect live /login page (network traffic, cookies)
5. Claude → Synthesize: 3 personas + docs + recent CVEs + live analysis
```

**Output:** Production-ready security review with prioritized fixes

**See:** [Context7 Workflow 1](./CONTEXT7.md#workflow-1-security-review-with-current-standards)

---

### Pattern 2: Performance Optimization (Sensei + Playwright)

**Query:** "Why is our checkout page slow?"

**MCP Flow:**
```
1. Sensei → Suggest: [performance-engineer, frontend-ux-specialist]
2. Playwright → Navigate to /checkout, start performance trace
3. Playwright → Measure: LCP, CLS, FID, network waterfall
4. Context7 → Fetch latest performance best practices
5. Claude → Synthesize: Real metrics + expert recommendations
```

**Output:** Bottleneck analysis with measured improvements

**See:** [Playwright Workflow 1](./PLAYWRIGHT.md#workflow-1-performance-debugging)

---

### Pattern 3: Architecture Refactoring (Sensei + Serena + Context7) 🔥 **NEW!**

**Query:** "Refactor authentication to use dependency injection"

**MCP Flow:**
```
1. Sensei → Suggest: [pragmatic-architect, security-sentinel]
2. Context7 → Fetch SOLID principles, DI patterns
3. Serena → Analyze current code structure (find symbols, dependencies)
4. Sensei → Design DI approach (validate against standards)
5. Serena → Execute refactoring (replace symbols, insert interfaces)
6. Sensei → Validate refactored code (check consistency)
```

**Output:** Production-ready refactored code with architectural validation

**See:** [Serena Workflow 1](./SERENA.md#workflow-1-architecture-driven-refactoring)

---

### Pattern 4: Technology Due Diligence (Sensei + Tavily + Context7)

**Query:** "Should we adopt Bun for our Node.js services?"

**MCP Flow:**
```
1. Sensei → Suggest: [pragmatic-architect, snarky-senior-engineer]
2. Tavily → Search "Bun production ready 2025", "Bun vs Node.js benchmarks"
3. Context7 → Fetch Bun and Node.js official docs
4. Claude → Synthesize: Current status + expert assessment + official docs
```

**Output:** Informed adopt/pilot/avoid recommendation with timeline

**See:** [Tavily Workflow 3](./TAVILY.md#workflow-3-technology-due-diligence)

---

## 🚀 Quick Start: Your First Multi-MCP Workflow

### 1. Install Tier 1 MCPs (15 minutes)

```bash
# Context7 (no API key needed)
npx -y @upstash/context7-mcp

# Serena (no API key needed) - NEW!
pip install serena-mcp

# Tavily (requires free API key)
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxx"
npx -y @tavily/mcp-server

# Playwright (requires browser install)
npx playwright install chromium
npx -y @playwright/mcp-server
```

### 2. Configure Claude Code

```bash
# Add all four Tier 1 MCP servers
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add serena -- python -m serena_mcp
claude mcp add tavily -- npx -y @tavily/mcp-server
claude mcp add playwright -- npx -y @playwright/mcp-server
```

### 3. Test Multi-MCP Workflow

```
You: "Review my authentication implementation at https://app.example.com/login for security issues"

Expected:
✅ Sensei suggests 3 security personas
✅ Context7 fetches OWASP standards
✅ Tavily finds recent OAuth CVEs
✅ Playwright inspects live login page
✅ Claude synthesizes comprehensive security review
```

---

## 💡 Best Practices

### 1. Let Sensei Orchestrate

**❌ Don't micromanage:**
```
"Use Security Sentinel, fetch OWASP docs, search for CVEs..."
```

**✅ Let Sensei decide:**
```
"Review my authentication for security issues"
// Sensei automatically:
// - Selects relevant personas
// - Determines which MCP servers to use
// - Orchestrates the workflow
```

### 2. Combine Complementary MCP Servers

| Use Case | Primary | Secondary | Tertiary |
|----------|---------|-----------|----------|
| Security Review | Sensei | Context7 (standards) | Tavily (CVEs) + Playwright (live) |
| Code Refactoring | Sensei | Serena (execution) | Context7 (patterns) |
| Performance Debug | Sensei | Playwright (metrics) | Context7 (best practices) |
| Pattern Enforcement | Sensei | Serena (search+fix) | Context7 (standards) |
| Library Choice | Sensei | Context7 (docs) | Tavily (maintenance status) |
| Cost Optimization | Sensei | Tavily (pricing) | Context7 (docs) |

### 3. Cache Results to Save Cost

```python
# Tavily costs $0.005-0.01 per search
# Cache results in Sensei session memory

1. First query: Tavily search "AWS pricing"
2. Record in session memory (TTL: 1 hour)
3. Second query: Use cached pricing → $0 cost
```

### 4. Start Simple, Add Complexity

**Week 1:** Sensei alone (learn persona suggestions)
**Week 2:** + Context7 (current docs)
**Week 3:** + Tavily (recent data)
**Week 4:** + Playwright (live inspection)

---

## 🎯 Success Metrics

Track integration effectiveness with Sensei analytics:

```python
get_session_insights(session_id="my-project")

# Target metrics:
{
  "mcp_usage": {
    "context7": 45,  # Used in 45 consultations
    "tavily": 28,    # $0.28 spent
    "playwright": 12  # 12 live inspections
  },
  "multi_mcp_consultations": 34,  # 34 used 2+ MCP servers
  "avg_quality_score": 4.7/5,
  "time_saved_estimate": "23 hours"  # vs manual research
}
```

**Good Indicators:**
- ✅ 60%+ consultations use 2+ MCP servers
- ✅ Quality score >4.5/5
- ✅ Reduced "is this current?" follow-ups
- ✅ Faster decision-making (measured in session insights)

---

## 🐛 Common Issues

### "MCP server not found"

**Solution:** Restart MCP client after config changes

```bash
# Claude Code
claude mcp list  # Verify servers are registered

# Claude Desktop
# Quit and restart Claude Desktop app
```

---

### "Integration works separately but not together"

**Cause:** MCP server initialization order

**Solution:** Order doesn't matter, but all must start successfully

```bash
# Test each server independently
npx @upstash/context7-mcp  # Should start
npx @tavily/mcp-server  # Should start (check API key)
npx @playwright/mcp-server  # Should start (check browser install)
```

---

### "Tavily costs are too high"

**Solution:** Implement caching and rate limiting

See [Tavily Cost Management](./TAVILY.md#cost-management)

---

## 📖 Next Steps

### Tier 2 Integrations (High Value)

#### [GitHub MCP](./GITHUB.md) 🔥 **NEW!**
**Purpose:** PR reviews, commit analysis, issue triage with GitHub context

**Key Use Cases:**
- Multi-persona PR code reviews
- Architectural drift detection via commit history
- Smart issue categorization and prioritization

**Quick Start:**
```bash
gh auth login  # Authenticate GitHub CLI
# GitHub MCP is built into Claude Code
```

**Best For:**
- Security Sentinel + PR security reviews
- Pragmatic Architect + commit pattern analysis
- SRE + issue triage and prioritization

---

#### [OpenMemory MCP](./OPENMEMORY.md) 🔥 **NEW!**
**Purpose:** Cross-project memory and organizational knowledge

**Key Use Cases:**
- Store team standards across all projects
- Remember architectural lessons learned
- Share patterns between team members

**Quick Start:**
```bash
# OpenMemory is typically pre-installed with Claude Code
```

**Best For:**
- Any persona + cross-project wisdom
- Team standardization
- Architectural pattern reuse

---

### Future Integrations

- **Sequential Thinking MCP:** Complex multi-step reasoning

### Advanced Workflows

- **Multi-repo security audits:** Sensei + Context7 + Tavily + GitHub
- **Performance regression detection:** Playwright + Sensei analytics
- **Cost optimization dashboard:** Tavily pricing + FinOps persona + session insights

---

## 🤝 Contributing

Help improve these integration guides!

**Found a great workflow?**
1. Open issue: https://github.com/amarodeabreu/sensei-mcp/issues
2. Add example to appropriate guide via PR
3. Tag with `integration-example`

**Found a bug or gap?**
1. Open issue with clear reproduction steps
2. Tag with `integration-bug`

---

## 📚 Additional Resources

- [MCP Integration Architecture](../MCP_INTEGRATION_ARCHITECTURE.md) - Overall vision
- [MCP Integration Examples](../MCP_INTEGRATION_EXAMPLES.md) - Full workflow examples
- [Sensei Usage Guide](../USAGE_GUIDE.md) - Core Sensei features
- [Sensei Quickstart](../QUICKSTART.md) - Getting started

---

**Made with 🥋 by the Sensei MCP community**

*Multi-perspective intelligence. Single interface.*
